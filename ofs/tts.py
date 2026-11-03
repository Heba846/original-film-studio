"""OPTIONAL local voice generation via open-source Chatterbox (MIT, resemble-ai/chatterbox).

Design rules
- Imported audio stays the default. Nothing here runs unless the user presses Generate / runs `tts generate`.
- Chatterbox + torch live in an ISOLATED interpreter (.venv-tts, see setup_tts.bat), driven through
  ofs/tts_worker.py as a subprocess. The main app never imports torch.
- No model download unless the user runs `tts download --yes`. No network calls from this module.
- Reference clips are LOCAL paths that the project only stores as text. Recordings, embeddings and
  checkpoints are git-ignored and excluded from the ZIP.
- Each generated WAV gets a sidecar JSON recording engine/model/device (no audio features, no embeddings).

STATUS: plumbing is unit-tested with a MOCK runner and the worker's 'not installed' path is exercised
for real. Actual Chatterbox inference is UNTESTED here (no torch/GPU/recordings in the authoring env).
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from . import project as proj

WORKER = Path(__file__).with_name("tts_worker.py")
ROOT = Path(__file__).resolve().parent.parent


def tts_python() -> str | None:
    env = os.environ.get("OFS_TTS_PYTHON")
    if env:
        return env
    for c in (ROOT / ".venv-tts" / "Scripts" / "python.exe", ROOT / ".venv-tts" / "bin" / "python"):
        if c.is_file():
            return str(c)
    return None


def status(runner=None) -> dict:
    """Cheap, side-effect-free status. Never downloads or loads a model."""
    py = tts_python()
    base = {"engine": "chatterbox", "license": "MIT (upstream); see docs/CHATTERBOX.md",
            "isolated_python": py, "inference_tested_in_this_repo": False}
    if not py:
        return {**base, "available": False, "device": None,
                "message": "Optional TTS not set up (no .venv-tts). Imported audio works without it. "
                           "Run setup_tts.bat to install Chatterbox in an isolated environment."}
    try:
        r = (runner or _run)([py, str(WORKER), "probe"])
        info = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:  # noqa: BLE001
        return {**base, "available": False, "device": None, "message": f"TTS interpreter failed to probe: {e}"}
    ok = info.get("chatterbox_installed") and info.get("torch_installed")
    return {**base, **info, "available": bool(ok),
            "message": ("Chatterbox installed. Weights are NOT downloaded automatically; if missing run "
                        "`python -m ofs tts download --yes`. Real-voice output is untested by the authors of this repo."
                        if ok else "chatterbox-tts / torch not installed in the TTS environment.")}


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


class TTSError(Exception):
    pass


def generation_problems(project: dict, base, seg_ids=None) -> list:
    """Why generation can't start (consent + local reference clips). Empty list = OK."""
    project = proj.normalize(project)
    sp = {s["id"]: s for s in project["speakers"]}
    out = []
    for g in project["narration_segments"]:
        if seg_ids and g["id"] not in seg_ids:
            continue
        s = sp.get(g["speaker"])
        if not s:
            out.append(f"segment {g['id']}: unknown speaker '{g['speaker']}'")
            continue
        if not s["consent_confirmed"]:
            out.append(f"speaker {s['id']}: consent to cloning/commercial use not confirmed in the project")
        if not s["reference_audio"]:
            out.append(f"speaker {s['id']}: no local reference audio path set")
        elif not proj.resolve(base, s["reference_audio"]).is_file():
            out.append(f"speaker {s['id']}: reference audio not found: {s['reference_audio']}")
        if not (g["text"] or "").strip():
            out.append(f"segment {g['id']}: empty text")
    return list(dict.fromkeys(out))


def generate(project: dict, base, seg_ids=None, runner=None, overwrite=False) -> dict:
    """Generate WAVs for segments (default: those without audio). Returns a result dict and
    updates the project dict in place (audio path, source='generated')."""
    base = Path(base)
    project = proj.normalize(project) if not isinstance(project.get("narration_segments"), list) else project
    wanted = set(seg_ids) if seg_ids else {g["id"] for g in project["narration_segments"]
                                           if overwrite or not g["audio"]
                                           or not proj.resolve(base, g["audio"]).is_file()}
    if not wanted:
        return {"ok": True, "generated": [], "message": "nothing to generate"}
    probs = generation_problems(project, base, wanted)
    if probs:
        raise TTSError("; ".join(probs))
    py = tts_python()
    if not py and runner is None:
        raise TTSError("TTS environment not set up (run setup_tts.bat). Import recorded WAV/MP3 files instead.")
    sp = {s["id"]: s for s in project["speakers"]}
    outdir = base / "media" / "generated"
    outdir.mkdir(parents=True, exist_ok=True)
    items = [{"id": g["id"], "text": g["text"], "out": str(outdir / f"{g['id']}.wav"),
              "reference": str(proj.resolve(base, sp[g["speaker"]]["reference_audio"]))}
             for g in project["narration_segments"] if g["id"] in wanted]
    cfg = project["tts"]
    job = {"device": cfg["device"], "model": cfg["model"], "exaggeration": cfg["exaggeration"],
           "cfg_weight": cfg["cfg_weight"], "items": items}
    with tempfile.TemporaryDirectory(prefix="ofs_tts_") as t:
        jf = Path(t) / "job.json"
        jf.write_text(json.dumps(job), encoding="utf-8")
        r = (runner or _run)([py or sys.executable, str(WORKER), "generate", str(jf)])
    try:
        res = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        raise TTSError("TTS worker returned no result: " + (r.stderr or "")[-300:])
    if not res.get("results"):
        raise TTSError(res.get("error", "TTS failed"))
    done = []
    for rr in res["results"]:
        if not rr.get("ok"):
            continue
        g = next(x for x in project["narration_segments"] if x["id"] == rr["id"])
        g["audio"] = f"media/generated/{g['id']}.wav"
        g["source"] = "generated"
        Path(rr["out"]).with_suffix(".wav.json").write_text(json.dumps({
            "engine": "chatterbox", "model": res.get("model"), "device": res.get("device"),
            "speaker": g["speaker"], "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "note": "Locally generated synthetic voice. Chatterbox embeds a Perth watermark."}), encoding="utf-8")
        done.append(g["id"])
    failed = [{"id": x["id"], "error": x.get("error")} for x in res["results"] if not x.get("ok")]
    return {"ok": not failed, "generated": done, "failed": failed, "device": res.get("device"), "model": res.get("model")}


def download(models=("turbo",)) -> dict:
    py = tts_python()
    if not py:
        raise TTSError("TTS environment not set up (run setup_tts.bat first).")
    r = _run([py, str(WORKER), "download", *models])
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        raise TTSError((r.stderr or r.stdout)[-400:])

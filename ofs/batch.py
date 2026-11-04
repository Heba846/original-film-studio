"""Batch voice rendering for ALL narration segments, with resume, trimming and loudness normalisation.

Reference voices (git-ignored, never committed):
    voices/heba/*.wav   (also .mp3 .m4a .flac .ogg)   -> speaker id "heba"
    voices/lion/*.wav                                  -> speaker id "lion"
`prep_voices` concatenates up to ~25 s of clean clips per speaker into voices/<id>/_ref.wav
(24 kHz mono, loudness-levelled), which is what the cloning engine receives.

Pipeline per segment:  engine -> media/generated/raw/<id>.wav
                       -> trim silence + 2-pass EBU R128 loudnorm (-19 LUFS, TP -1.5) -> media/generated/<id>.wav
`pause_after` is NOT baked into the WAV: `ofs narration assemble` pads each segment by its pause_after.
Resume: a segment whose final WAV + sidecar exist is skipped (unless --overwrite).
"""
from __future__ import annotations

import datetime
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path

from . import media, project as proj, tts

ROOT = Path(__file__).resolve().parent.parent
AUDIO_EXT = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"}
TARGET_LUFS = -19.0
REF_MAX_SECONDS = 25.0
STAND_IN_VOICES = {"heba": "en-us+f3", "lion": "en-us+m3"}  # espeak-ng stand-in ONLY


def voices_dir(base=None) -> Path:
    import os
    return Path(os.environ.get("OFS_VOICES_DIR") or ROOT / "voices")


def reference_clips(speaker_id: str, vdir=None) -> list[Path]:
    d = (Path(vdir) if vdir else voices_dir()) / speaker_id
    if not d.is_dir():
        return []
    return sorted(p for p in d.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXT and not p.name.startswith("_"))


def _ff(args):
    ffmpeg = media.tool("ffmpeg")
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostats", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("ffmpeg failed: " + "\n".join(r.stderr.strip().splitlines()[-4:]))
    return r


def prep_voices(speaker_ids, vdir=None) -> dict:
    """Build voices/<id>/_ref.wav per speaker. Returns {id: {"ref": path, "seconds": s, "clips": n} | {"error": ...}}."""
    out = {}
    for sid in speaker_ids:
        clips = reference_clips(sid, vdir)
        if not clips:
            out[sid] = {"error": f"no reference clips in {(Path(vdir) if vdir else voices_dir()) / sid}"}
            continue
        d = clips[0].parent
        parts, total = [], 0.0
        for c in clips:
            try:
                dur = float(media.probe(c)["duration"] or 0)
            except Exception as e:  # noqa: BLE001
                out.setdefault(sid, {})["warning"] = f"skipped unreadable {c.name}: {e}"
                continue
            if total >= REF_MAX_SECONDS:
                break
            take = min(dur, REF_MAX_SECONDS - total)
            parts.append((c, take))
            total += take
        if not parts:
            out[sid] = {"error": "no readable reference audio"}
            continue
        ref = d / "_ref.wav"
        args, chains = [], []
        for i, (c, take) in enumerate(parts):
            args += ["-t", f"{take:.2f}", "-i", str(c)]
            chains.append(f"[{i}:a]aresample=24000,aformat=channel_layouts=mono[a{i}]")
        graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(parts))) + \
            f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-20:TP=-2:LRA=11[o]"
        _ff(["-y", *args, "-filter_complex", graph, "-map", "[o]", "-ar", "24000", "-ac", "1", str(ref)])
        warn = out.get(sid, {}).get("warning")
        out[sid] = {"ref": str(ref), "seconds": round(total, 1), "clips": len(parts)}
        if total < 8:
            out[sid]["warning"] = f"only {total:.1f}s of reference audio; 10-30 s of clean speech clones better"
        elif warn:
            out[sid]["warning"] = warn
    return out


def _measure(path) -> dict:
    r = _ff(["-i", str(path), "-af", f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        raise RuntimeError("could not measure loudness")
    return json.loads(m.group(0))


def finalize(raw, final) -> dict:
    """Trim leading/trailing silence, then 2-pass linear loudnorm. Returns measured stats."""
    raw, final = Path(raw), Path(final)
    final.parent.mkdir(parents=True, exist_ok=True)
    sil = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04,"
           "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse")
    with tempfile.TemporaryDirectory(prefix="ofs_norm_") as t:
        trimmed = Path(t) / "trim.wav"
        _ff(["-y", "-i", str(raw), "-af", sil, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(trimmed)])
        m = _measure(trimmed)
        af = (f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        _ff(["-y", "-i", str(trimmed), "-af", af, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(final)])
    after = _measure(final)
    return {"input_lufs": float(m["input_i"]), "output_lufs": float(after["input_i"]),
            "duration": float(media.probe(final)["duration"])}


def build_items(project, base, ref_map, engine, outdir, stock=False):
    items = []
    for g in project["narration_segments"]:
        it = {"id": g["id"], "text": g["text"], "speaker": g["speaker"], "out": str(outdir / "raw" / f"{g['id']}.wav")}
        if engine == "espeak":
            it["voice"] = STAND_IN_VOICES.get(g["speaker"], "en-us")
        elif not stock:
            it["reference"] = ref_map[g["speaker"]]
        items.append(it)
    return items


def render_all(project: dict, base, engine="chatterbox", stock=False, overwrite=False, only=None,
               limit=None, vdir=None, runner=None, stand_in_ok=False, outsub="generated") -> dict:
    """Render segments. Returns a report with real-time factor. Mutates `project` (audio paths)."""
    project = proj.normalize(project) if "narration_segments" not in project else project
    base = Path(base)
    outdir = base / "media" / outsub
    segs = [g for g in project["narration_segments"] if not only or g["id"] in only]
    if limit:
        segs = segs[:limit]
    ids = {g["id"] for g in segs}
    sp_ids = sorted({g["speaker"] for g in segs})
    ref_map = {}
    if engine == "chatterbox" and not stock:
        prep = prep_voices(sp_ids, vdir)
        bad = {k: v["error"] for k, v in prep.items() if "error" in v}
        if bad:
            raise tts.TTSError("missing reference voices: " + "; ".join(f"{k}: {v}" for k, v in bad.items()) +
                               ". Put clean WAVs in voices/<speaker>/ (see docs/VOICE_PIPELINE.md) or use --stock.")
        ref_map = {k: v["ref"] for k, v in prep.items()}
    elif engine == "espeak" and not stand_in_ok:
        raise tts.TTSError("engine 'espeak' is a robotic STAND-IN for pipeline tests only; pass --stand-in to allow it.")
    sub = {**project, "narration_segments": segs}
    items = build_items(sub, base, ref_map, engine, outdir, stock)
    todo = []
    for it in items:
        final = outdir / f"{it['id']}.wav"
        if not overwrite and final.is_file() and final.with_suffix(".wav.json").is_file():
            continue
        todo.append(it)
    cfg = project["tts"]
    t_wall = time.time()
    res = {"results": []}
    if todo:
        py = tts.tts_python() if engine == "chatterbox" else None
        job = {"engine": engine, "device": cfg["device"], "model": cfg["model"], "exaggeration": cfg["exaggeration"],
               "cfg_weight": cfg["cfg_weight"], "skip_existing": not overwrite, "items": todo}
        with tempfile.TemporaryDirectory(prefix="ofs_tts_") as t:
            jf = Path(t) / "job.json"
            jf.write_text(json.dumps(job), encoding="utf-8")
            r = (runner or tts._run)([py or __import__("sys").executable, str(tts.WORKER), "generate", str(jf)])
        try:
            res = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:  # noqa: BLE001
            raise tts.TTSError("TTS worker returned no result: " + (r.stderr or "")[-600:])
        if not res.get("results"):
            raise tts.TTSError(res.get("error", "TTS failed"))
    wall_gen = time.time() - t_wall
    by = {x["id"]: x for x in res.get("results", [])}
    done, failed, stats = [], [], []
    for g in segs:
        final = outdir / f"{g['id']}.wav"
        if g["id"] in by:
            rr = by[g["id"]]
            if not rr.get("ok"):
                failed.append({"id": g["id"], "error": rr.get("error")})
                continue
            st = finalize(rr["out"], final)
            if rr.get("skipped") and final.is_file():
                pass
            final.with_suffix(".wav.json").write_text(json.dumps({
                "engine": res.get("engine", engine), "model": res.get("model"), "device": res.get("device"),
                "speaker": g["speaker"], "stock_voice": bool(stock), "stand_in": engine == "espeak",
                "gen_wall_seconds": rr.get("wall"), "audio_seconds": st["duration"],
                "input_lufs": st["input_lufs"], "output_lufs": st["output_lufs"],
                "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "note": ("STAND-IN robotic voice for pipeline testing, NOT a clone." if engine == "espeak" else
                         "Synthetic voice (Chatterbox, PerTh-watermarked)." + (" Stock voice, not cloned." if stock else ""))}),
                encoding="utf-8")
            stats.append({"id": g["id"], "wall": rr.get("wall"), "audio": st["duration"], "lufs": st["output_lufs"]})
        if final.is_file():
            g["audio"] = f"media/{outsub}/{g['id']}.wav"
            g["source"] = "generated"
            done.append(g["id"])
    for g in project["narration_segments"]:  # propagate onto the real project list
        for s in segs:
            if s["id"] == g["id"]:
                g["audio"], g["source"] = s["audio"], s["source"]
    wall = sum(s["wall"] or 0 for s in stats)
    audio = sum(s["audio"] for s in stats)
    return {"ok": not failed, "engine": engine, "stock": stock, "requested": len(segs), "rendered_now": len(stats),
            "already_done": len(done) - len(stats), "failed": failed,
            "audio_seconds_now": round(audio, 1), "generation_seconds_now": round(wall, 1),
            "real_time_factor": round(wall / audio, 3) if audio else None,
            "note": "RTF = generation seconds / audio seconds (lower is faster than real time). "
                    "Wall time of the whole call incl. model load: %.1fs." % wall_gen,
            "loudness_range_lufs": [round(min(s["lufs"] for s in stats), 2), round(max(s["lufs"] for s in stats), 2)]
            if stats else None}

"""Narration segments: speaker + text + pause-after + WAV (imported OR locally generated).

Segments are assembled into ONE narration WAV, which is what the renderer mixes. Timing is
computed from the real audio files (ffprobe) when they exist; otherwise it is an ESTIMATE
from word count and is flagged as such.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from . import media, project as proj

WORDS_PER_SEC = 2.6  # ~156 wpm: only used for ESTIMATES when no audio exists yet
SR = 48000


def uses_segments(project: dict) -> bool:
    return project["audio"].get("narration_mode") == "segments"


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def estimate_seconds(text: str) -> float:
    return max(0.6, len(text.split()) / WORDS_PER_SEC)


def plan(project: dict, base, probe_fn=media.probe) -> dict:
    """Per-segment timing. measured=True only if that segment's audio was probed."""
    project = proj.normalize(project)
    base = Path(base)
    t, rows = 0.0, []
    for seg in project["narration_segments"]:
        measured, dur = False, estimate_seconds(seg["text"])
        if seg["audio"]:
            p = proj.resolve(base, seg["audio"])
            if p.is_file():
                try:
                    d = probe_fn(p)["duration"]
                    if d:
                        dur, measured = float(d), True
                except Exception:  # noqa: BLE001
                    pass
        pause = max(_num(seg["pause_after"]), 0.0)
        rows.append({"id": seg["id"], "speaker": seg["speaker"], "start": round(t, 3),
                     "speech_end": round(t + dur, 3), "end": round(t + dur + pause, 3),
                     "duration": round(dur, 3), "pause_after": pause, "measured": measured,
                     "source": seg["source"], "editorial": seg["editorial"]})
        t += dur + pause
    return {"segments": rows, "total": round(t, 3), "all_measured": bool(rows) and all(r["measured"] for r in rows),
            "note": "" if rows and all(r["measured"] for r in rows) else
            "Includes ESTIMATED durations (no audio yet for some segments); final timing is known only after audio exists."}


def assemble(project: dict, base, out_path) -> dict:
    """Concatenate segment audio (+ pauses) into one 48 kHz mono WAV with ffmpeg."""
    project = proj.normalize(project)
    base = Path(base)
    segs = project["narration_segments"]
    if not segs:
        raise ValueError("no narration segments")
    ffmpeg = media.tool("ffmpeg")
    if not ffmpeg:
        raise ValueError("ffmpeg not found")
    inputs, chains = [], []
    for i, s in enumerate(segs):
        p = proj.resolve(base, s["audio"]) if s["audio"] else None
        if not p or not p.is_file():
            raise ValueError(f"segment '{s['id']}' has no audio file (import a WAV/MP3 or generate it)")
        inputs += ["-i", str(p)]
        pause = max(_num(s["pause_after"]), 0.0)
        chains.append(f"[{i}:a]aresample={SR},aformat=sample_fmts=s16:channel_layouts=mono,"
                      f"apad=pad_dur={pause}[a{i}]")
    graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(segs))) + \
        f"concat=n={len(segs)}:v=0:a=1[out]"
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", graph,
                        "-map", "[out]", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(out_path)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise ValueError("assembling narration failed: " + "\n".join(r.stderr.strip().splitlines()[-5:]))
    pl = plan(project, base)
    pl["output"] = str(out_path)
    out_path.with_suffix(".timing.json").write_text(json.dumps(pl, indent=2), encoding="utf-8")
    return pl


def sync_shot_durations(project: dict, pl: dict, tail: float = 0.5) -> dict:
    """Set each shot's duration from the narration segments assigned to it (shot['segments']).

    Only shots that list segments are changed. The last shot gets `tail` extra seconds.
    Uses measured timing when available, otherwise the estimate (reported back in 'estimated')."""
    project = proj.normalize(project)
    by = {r["id"]: r for r in pl["segments"]}
    changed, estimated = [], []
    shots = project["shots"]
    for i, s in enumerate(shots):
        rows = [by[x] for x in s["segments"] if x in by]
        if not rows:
            continue
        d = sum(r["duration"] + r["pause_after"] for r in rows)
        if i == len(shots) - 1:
            d += tail
        s["duration"] = round(d, 2)
        changed.append(s["id"])
        if not all(r["measured"] for r in rows):
            estimated.append(s["id"])
    return {"project": project, "changed": changed, "estimated": estimated}


def resolve_narration_file(project: dict, base, tmpdir) -> Path | None:
    """The single narration file the renderer should mix (assembling segments if needed)."""
    a = project["audio"]
    if uses_segments(project):
        out = Path(tmpdir) / "narration_assembled.wav"
        assemble(project, base, out)
        return out
    return proj.resolve(base, a["narration"]) if a["narration"] else None

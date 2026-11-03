"""Fill shots with supplied video clips (e.g. 8 s Veo clips), cut to the narration timing.

Rules (hard):
- NO frozen-frame filling. Nothing here uses tpad/clone or freeze.
- NO looping stretch longer than the clip itself: a reused clip is played at most once per
  pass, and every pass is a separate piece joined by a crossfade (with a different punch-in
  framing so the reuse is less obvious).
- If a shot cannot be covered, the planner says how many seconds are missing; it never pads.

Clip discovery for shot `s05` (first match wins):
  1. shot["clips"] = ["media/clips/foo.mp4", ...]   (explicit, in order)
  2. media/clips/s05/*.mp4                          (a folder per shot)
  3. media/clips/s05.mp4, s05_a.mp4, s05_2.mp4 ...  (prefix `s05` followed by end or `_`/`-`/`.`)
"""
from __future__ import annotations

import re
from pathlib import Path

from . import media, project as proj

W, H = 1920, 1080
XFADE = 0.5          # crossfade between pieces inside a shot (seconds)
MIN_PIECE = 1.5      # never leave a piece shorter than this
MAX_SLOW = 0.85      # slowest playback speed used to stretch unique footage before reusing clips
PUNCH = [1.0, 1.12, 1.06, 1.18]  # framing zoom per pass (pass 0 = original framing)


def _natural(p: Path):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def discover(shot: dict, base) -> list[Path]:
    base = Path(base)
    if shot.get("clips"):
        return [proj.resolve(base, c) for c in shot["clips"]]
    root = base / "media" / "clips"
    sid = shot["id"]
    d = root / sid
    if d.is_dir():
        return sorted((p for p in d.iterdir() if p.suffix.lower() in media.VIDEO_EXT), key=_natural)
    if not root.is_dir():
        return []
    pat = re.compile(r"^" + re.escape(sid) + r"(?:$|[_\-.])", re.IGNORECASE)
    return sorted((p for p in root.iterdir()
                   if p.is_file() and p.suffix.lower() in media.VIDEO_EXT and pat.match(p.name)), key=_natural)


def plan_shot(duration: float, clip_durs: list[float], xf: float = XFADE, max_slow: float = MAX_SLOW) -> dict:
    """Pure planner. Returns pieces [{clip, src_start, src_len, out_len, speed, pass_no}] and stats.

    The joined timeline length equals `duration` when covered. `speed` < 1 slows playback to stretch footage."""
    res = {"pieces": [], "speed": 1.0, "unique_seconds": 0.0, "reused_seconds": 0.0, "covered": False,
           "missing_seconds": 0.0, "slowed": False}
    clip_durs = [float(c) for c in clip_durs if c and c > 0.2]
    if duration <= 0 or not clip_durs:
        res["missing_seconds"] = round(max(duration, 0.0), 2)
        return res

    speed = 1.0
    if sum(clip_durs) - (len(clip_durs) - 1) * xf < duration:
        need = sum(clip_durs) / (duration + (len(clip_durs) - 1) * xf)
        speed = max(max_slow, min(1.0, need))
    res["speed"] = round(speed, 4)
    res["slowed"] = speed < 1.0

    pieces, t_total, i = [], 0.0, 0
    while i <= 400:
        ci, pass_no = i % len(clip_durs), i // len(clip_durs)
        full = clip_durs[ci] / speed
        if not pieces:
            out = min(full, duration)
            t_total = out
        else:
            out = min(full, duration - (t_total - xf))
            t_total = t_total - xf + out
        pieces.append({"clip": ci, "src_start": 0.0, "src_len": round(out * speed, 4),
                       "out_len": round(out, 4), "speed": speed, "pass_no": pass_no})
        if t_total >= duration - 1e-6:
            break
        i += 1
    # avoid a sliver at the end: borrow time from the previous piece
    if len(pieces) > 1 and pieces[-1]["out_len"] < MIN_PIECE:
        short = MIN_PIECE - pieces[-1]["out_len"]
        prev = pieces[-2]
        if prev["out_len"] - short >= MIN_PIECE:
            prev["out_len"] = round(prev["out_len"] - short, 4)
            prev["src_len"] = round(prev["out_len"] * speed, 4)
            pieces[-1]["out_len"] = round(MIN_PIECE, 4)
            pieces[-1]["src_len"] = round(MIN_PIECE * speed, 4)
    res["pieces"] = pieces
    res["covered"] = True
    uniq = sum(p["out_len"] for p in pieces if p["pass_no"] == 0) - xf * max(0, sum(1 for p in pieces if p["pass_no"] == 0) - 1)
    res["unique_seconds"] = round(max(min(uniq, duration), 0.0), 2)
    res["reused_seconds"] = round(max(duration - res["unique_seconds"], 0.0), 2)
    return res


def _fit(zoom: float = 1.0) -> str:
    f = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1")
    if zoom > 1.0:
        f += f",scale=iw*{zoom}:ih*{zoom},crop={W}:{H}"
    return f


def shot_command(ffmpeg, shot, clip_paths, plan, out, fps, crf, preset) -> list:
    """One ffmpeg command: trimmed pieces -> xfade chain -> exactly the shot duration, no freezing."""
    dur = float(shot["duration"])
    pieces = plan["pieces"]
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
    chains = []
    for n, pc in enumerate(pieces):
        cmd += ["-ss", f"{pc['src_start']}", "-t", f"{pc['src_len'] + 0.1:.3f}", "-i", str(clip_paths[pc["clip"]])]
        zoom = PUNCH[pc["pass_no"] % len(PUNCH)]
        chains.append(f"[{n}:v]setpts=(PTS-STARTPTS)/{pc['speed']:.5f},fps={fps},{_fit(zoom)},format=yuv420p,"
                      f"trim=duration={pc['out_len']:.4f},setpts=PTS-STARTPTS[p{n}]")
    last = "p0"
    if len(pieces) > 1:
        acc = pieces[0]["out_len"]
        for n in range(1, len(pieces)):
            chains.append(f"[{last}][p{n}]xfade=transition=fade:duration={XFADE}:offset={acc - XFADE:.4f}[x{n}]")
            last = f"x{n}"
            acc = acc - XFADE + pieces[n]["out_len"]
    tail = f"[{last}]trim=duration={dur:.4f},setpts=PTS-STARTPTS"
    if shot.get("transition") == "fade" and dur >= 1:
        tail += f",fade=t=in:st=0:d=0.3,fade=t=out:st={dur - 0.3:.3f}:d=0.3"
    chains.append(tail + ",format=yuv420p[v]")
    cmd += ["-filter_complex", ";".join(chains), "-map", "[v]", "-r", str(fps), "-an",
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", str(out)]
    return cmd


def coverage_report(project: dict, base, probe_fn=media.probe) -> dict:
    """Per-shot clip coverage using the shot durations currently in the project."""
    project = proj.normalize(project)
    rows = []
    for s in project["shots"]:
        paths = discover(s, base)
        durs = []
        for p in paths:
            try:
                durs.append(float(probe_fn(p)["duration"] or 0))
            except Exception:  # noqa: BLE001
                durs.append(0.0)
        d = float(s["duration"])
        pl = plan_shot(d, durs)
        rows.append({"shot": s["id"], "duration": round(d, 2), "clips": len(paths),
                     "clip_seconds": round(sum(durs), 1), "covered": pl["covered"], "speed": pl["speed"],
                     "unique_seconds": pl["unique_seconds"], "reused_seconds": pl["reused_seconds"],
                     "missing_seconds": pl["missing_seconds"],
                     "clips_for_all_unique": int(-(-(d + 0.5) // 7.5))})
    return {"shots": rows, "total_seconds": round(sum(r["duration"] for r in rows), 1),
            "unique_seconds": round(sum(r["unique_seconds"] for r in rows), 1),
            "reused_seconds": round(sum(r["reused_seconds"] for r in rows), 1),
            "missing_seconds": round(sum(r["missing_seconds"] for r in rows), 1),
            "shots_without_clips": [r["shot"] for r in rows if r["clips"] == 0]}

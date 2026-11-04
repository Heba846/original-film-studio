"""Assemble supplied assets into a 1080p 16:9 MP4 with FFmpeg.

HONESTY: this module never generates imagery. Still images (optionally with a
simple pan/zoom) produce an ANIMATIC / slideshow. Real moving shots only exist if
the owner supplies video clips made elsewhere.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from . import __version__, clips as clips_mod, media, narration as nar, project as proj, validate as val

W, H = 1920, 1080
FADE = 0.3
CAPTION_STYLE = "FontSize=14,Outline=2,Shadow=0,Alignment=2,MarginV=36,PrimaryColour=&H00FFFFFF&"


class RenderError(Exception):
    pass


class ValidationFailed(RenderError):
    def __init__(self, report):
        self.report = report
        super().__init__("Validation failed: " + "; ".join(i.message for i in report.errors))


def production_type(project: dict) -> str:
    kinds = {s["kind"] for s in project["shots"]}
    if kinds == {"image"}:
        return "animatic_slideshow"
    if kinds == {"video"}:
        return "assembled_supplied_video"
    return "mixed_stills_and_supplied_video"


DISCLOSURE = {
    "animatic_slideshow": "ANIMATIC/SLIDESHOW: still images with optional pan/zoom. No moving scenes were generated.",
    "assembled_supplied_video": "Assembled from owner-supplied video clips. This tool generated no video.",
    "mixed_stills_and_supplied_video": "Mix of still images (animatic) and owner-supplied video clips. "
                                       "This tool generated no video.",
}


def _run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        tail = "\n".join(p.stderr.strip().splitlines()[-8:])
        raise RenderError(f"ffmpeg failed (exit {p.returncode}):\n{tail}")


def _fit() -> str:
    return (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1")


def shot_command(ffmpeg, shot, src, out, fps, crf, preset) -> list:
    dur = float(shot["duration"])
    n = max(1, round(dur * fps))
    if shot["kind"] == "image":
        m = shot["motion"]
        if m == "none":
            pre = ["-loop", "1", "-framerate", str(fps), "-i", str(src)]
            vf = _fit()
        else:
            z = {"zoom_in": ("1+0.15*on/%d" % n, "iw/2-(iw/zoom/2)"),
                 "zoom_out": ("1.15-0.15*on/%d" % n, "iw/2-(iw/zoom/2)"),
                 "pan_right": ("1.15", "(iw-iw/zoom)*on/%d" % n),
                 "pan_left": ("1.15", "(iw-iw/zoom)*(1-on/%d)" % n)}[m]
            pre = ["-i", str(src)]
            vf = (f"{_fit()},scale={W * 2}:{H * 2},"
                  f"zoompan=z='{z[0]}':x='{z[1]}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={fps}")
    else:
        pre = ["-ss", str(shot["trim_start"]), "-i", str(src)]
        vf = f"fps={fps},{_fit()},tpad=stop_mode=clone:stop_duration={dur + 1}"
    if shot["transition"] == "fade" and dur >= 1:
        vf += f",fade=t=in:st=0:d={FADE},fade=t=out:st={dur - FADE:.3f}:d={FADE}"
    vf += ",format=yuv420p"
    return [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", *pre, "-vf", vf, "-t", f"{dur}", "-r", str(fps),
            "-an", "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", str(out)]


def render(project: dict, base, out_path, progress=None) -> dict:
    """Validate then render. Raises ValidationFailed (no output written) on errors."""
    project = proj.normalize(project)
    base = Path(base)
    report = val.validate(project, base)
    if not report.ok:
        raise ValidationFailed(report)
    ffmpeg = media.tool("ffmpeg")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cb = progress or (lambda stage, frac: None)
    rd, a, c = project["render"], project["audio"], project["captions"]
    fps, crf, preset = int(rd["fps"]), int(rd["crf"]), rd["preset"]
    total = report.total_duration
    shots = project["shots"]

    with tempfile.TemporaryDirectory(prefix="ofs_") as tmpname:
        tmp = Path(tmpname)
        names = []
        for i, s in enumerate(shots):
            cb(f"shot {s['id']} ({i + 1}/{len(shots)})", i / (len(shots) + 1))
            name = f"clip_{i:03}.mp4"
            sc = clips_mod.discover(s, base) if s["kind"] == "video" else []
            st = clips_mod.discover_stills(s, base) if s["kind"] == "video" else []
            if sc or st:
                durs = [float(media.probe(p)["duration"] or 0) for p in sc]
                splan = clips_mod.plan_shot_mixed(float(s["duration"]), durs, len(st))
                if not splan["covered"]:
                    raise RenderError(f"shot {s['id']}: footage cannot cover {s['duration']}s")
                _run(clips_mod.shot_command(ffmpeg, s, sc, splan, tmp / name, fps, crf, preset, still_paths=st), cwd=tmp)
            else:
                _run(shot_command(ffmpeg, s, proj.resolve(base, s["asset"]), tmp / name, fps, crf, preset), cwd=tmp)
            names.append(name)
        (tmp / "list.txt").write_text("".join(f"file '{n}'\n" for n in names), encoding="utf-8")
        cb("joining shots", len(shots) / (len(shots) + 1))
        _run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", "list.txt", "-c", "copy", "video.mp4"], cwd=tmp)

        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", "video.mp4"]
        idx, ni, mi, si, burn = 1, None, None, None, False
        narr_file = nar.resolve_narration_file(project, base, tmp)
        if narr_file:
            cmd += ["-i", str(narr_file)]
            ni, idx = idx, idx + 1
        if a["music"]:
            cmd += ["-stream_loop", "-1", "-i", str(proj.resolve(base, a["music"]))]
            mi, idx = idx, idx + 1
        if ni is None and mi is None:
            cmd += ["-f", "lavfi", "-t", f"{total}", "-i", "anullsrc=r=48000:cl=stereo"]
            si_silent, idx = idx, idx + 1
        if c["mode"] != "none" and c["srt"]:
            shutil.copyfile(proj.resolve(base, c["srt"]), tmp / "captions.srt")
            if c["mode"] == "soft":
                cmd += ["-i", "captions.srt"]
                si, idx = idx, idx + 1
            else:
                burn = True

        std = "aresample=48000,aformat=channel_layouts=stereo"
        f = []
        if ni is not None and mi is not None:
            fade_st = max(0.0, total - 2)
            f.append(f"[{ni}:a]{std},volume={float(a['narration_volume'])}[n]")
            f.append(f"[{mi}:a]{std},volume={float(a['music_volume'])},atrim=0:{total},"
                     f"afade=t=out:st={fade_st}:d={min(2.0, total)}[m]")
            if a["duck_music"]:
                f.append("[n]asplit=2[n1][n2]")
                f.append("[m][n2]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=400[md]")
                f.append("[n1][md]amix=inputs=2:duration=longest:normalize=0[mix]")
            else:
                f.append("[n][m]amix=inputs=2:duration=longest:normalize=0[mix]")
        elif ni is not None:
            f.append(f"[{ni}:a]{std},volume={float(a['narration_volume'])}[mix]")
        elif mi is not None:
            fade_st = max(0.0, total - 2)
            f.append(f"[{mi}:a]{std},volume={float(a['music_volume'])},atrim=0:{total},"
                     f"afade=t=out:st={fade_st}:d={min(2.0, total)}[mix]")
        else:
            f.append(f"[{si_silent}:a]anull[mix]")
        f.append(f"[mix]apad=whole_dur={total},atrim=0:{total}[aout]")
        if burn:
            f.append(f"[0:v]subtitles=captions.srt:force_style='{CAPTION_STYLE}'[v]")
        cmd += ["-filter_complex", ";".join(f), "-map", "[v]" if burn else "0:v", "-map", "[aout]"]
        if si is not None:
            cmd += ["-map", f"{si}:0"]
        cmd += (["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p"]
                if burn else ["-c:v", "copy"])
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
        if si is not None:
            cmd += ["-c:s", "mov_text"]
        ptype = production_type(project)
        cmd += ["-t", f"{total}", "-movflags", "+faststart",
                "-metadata", f"title={project['title']}",
                "-metadata", f"comment=Assembled by Original Film Studio {__version__}. {DISCLOSURE[ptype]}",
                str(out_path.resolve())]
        cb("mixing audio / final encode", (len(shots) + 0.5) / (len(shots) + 1))
        _run(cmd, cwd=tmp)

    segs = project["narration_segments"] if nar.uses_segments(project) else []
    generated = [x["id"] for x in segs if x["source"] == "generated"]
    manifest = {
        "tool": f"Original Film Studio {__version__}",
        "title": project["title"],
        "output": out_path.name,
        "production_type": ptype,
        "disclosure": DISCLOSURE[ptype],
        "ai_video_generated_by_this_tool": False,
        "resolution": f"{W}x{H}", "fps": fps, "total_duration": total,
        "narration": ("segments" if segs else (a["narration"] or None)), "music": a["music"] or None,
        "narration_segments": [{"id": x["id"], "speaker": x["speaker"], "source": x["source"],
                                "editorial_proposal": x["editorial"]} for x in segs],
        "synthetic_voice_segments": generated,
        "voice_disclosure": ("Contains locally generated synthetic voice for segments: " + ", ".join(generated)
                             + ". Consider YouTube's altered/synthetic content disclosure.") if generated else None,
        "captions": c["mode"] if c["srt"] else "none",
        "shots": [{"id": s["id"], "kind": s["kind"], "asset": s["asset"], "start": t0, "end": t1,
                   "motion": s["motion"] if s["kind"] == "image" else None}
                  for s, (_, t0, t1) in zip(shots, proj.timeline(project))],
        "warnings": [i.message for i in report.warnings],
    }
    mpath = out_path.with_name(out_path.stem + ".render.json")
    mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    cb("done", 1.0)
    return {**manifest, "output": str(out_path), "manifest": str(mpath), "report": report}

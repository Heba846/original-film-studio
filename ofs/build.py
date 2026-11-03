"""One-command build: narration track + measured timing -> shot durations -> clip-filled 1080p MP4
with burned-in captions, plus film.srt and YouTube chapters. Nothing is faked: it refuses to build
without measured audio for every segment, and without footage for every shot."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from . import captions as cap, clips as clips_mod, media, narration as nar, project as proj, render as rn

DEFAULT_SEGMENTS_JSON = Path("docs/adaptation/segments.json")


class BuildError(Exception):
    pass


def prepare(project: dict, base, segments_json=DEFAULT_SEGMENTS_JSON, music=None, fps=None,
            shot_transition=None, burn=True, outdir=None) -> dict:
    """Everything except the final encode. Returns context dict (project copy, timing, cues, chapters, coverage)."""
    base = Path(base)
    p = copy.deepcopy(proj.normalize(project))
    outdir = Path(outdir or base / "output")
    outdir.mkdir(parents=True, exist_ok=True)
    pl = nar.plan(p, base)
    if not pl["all_measured"]:
        missing = [r["id"] for r in pl["segments"] if not r["measured"]]
        raise BuildError(f"{len(missing)} segment(s) have no audio yet (first: {', '.join(missing[:6])}). "
                         "Run `python -m ofs tts batch <project>` first.")
    sync = nar.sync_shot_durations(p, pl)
    p = sync["project"]
    for s in p["shots"]:
        if clips_mod.discover(s, base):
            s["kind"] = "video"
        if shot_transition:
            s["transition"] = shot_transition
    if fps:
        p["render"]["fps"] = int(fps)
    cov = clips_mod.coverage_report(p, base)
    unfilled = [s["id"] for s, r in zip(p["shots"], cov["shots"])
                if r["clips"] == 0 and not (s["asset"] and proj.resolve(base, s["asset"]).is_file())]
    cues = cap.build_cues(p, pl)
    srt_path = cap.write_srt(cues, outdir / "film.srt")
    seg_ch = cap.load_seg_chapters(Path(segments_json) if Path(segments_json).is_absolute() else Path.cwd() / segments_json)
    chs = cap.chapters(p, pl, seg_ch)
    ch_text, ch_problems = cap.chapters_text(chs) if chs else ("", ["no chapter info found"])
    (outdir / "chapters.txt").write_text(ch_text, encoding="utf-8")
    p["captions"] = {"srt": str(srt_path.resolve()), "mode": "burn" if burn else "soft"}
    if music:
        p["audio"]["music"] = str(Path(music).resolve())
    return {"project": p, "timing": pl, "coverage": cov, "unfilled": unfilled, "cues": len(cues),
            "chapters": chs, "chapter_problems": ch_problems, "srt": str(srt_path),
            "chapters_file": str(outdir / "chapters.txt"), "outdir": outdir}


def build(project: dict, base, out_name="film.mp4", progress=None, **kw) -> dict:
    ctx = prepare(project, base, **kw)
    if ctx["unfilled"]:
        raise BuildError("no clips (or still) for shots: " + ", ".join(ctx["unfilled"]) +
                         ". Put 8 s clips in media/clips/<shot>.mp4 (or <shot>_2.mp4, or media/clips/<shot>/*.mp4).")
    p = ctx["project"]
    out = ctx["outdir"] / out_name
    res = rn.render(p, Path(base), out, progress)
    report = {"output": str(out), "duration": res["total_duration"], "srt": ctx["srt"],
              "chapters_file": ctx["chapters_file"], "chapters": ctx["chapters"],
              "chapter_problems": ctx["chapter_problems"], "coverage": {k: v for k, v in ctx["coverage"].items() if k != "shots"},
              "warnings": res["warnings"], "voice_disclosure": res["voice_disclosure"]}
    (ctx["outdir"] / "build_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report

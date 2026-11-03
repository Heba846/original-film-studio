from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import narration as nar, project as proj, validate as val, prompts as pr, render as rn

ROOT = Path.cwd() / "projects"


def _pdir(args) -> Path:
    return Path(args.project) if "/" in args.project or "\\" in args.project else ROOT / args.project


def cmd_validate(a):
    p = proj.load(_pdir(a))
    r = val.validate(p, _pdir(a))
    for i in r.issues:
        print(f"[{i.level.upper():7}] {i.code}: {i.message}")
    print(f"\nTimeline: {r.total_duration:.1f}s | errors: {len(r.errors)} | warnings: {len(r.warnings)}")
    return 0 if r.ok else 1


def cmd_prompts(a):
    d = _pdir(a)
    p = proj.load(d)
    items = pr.build_prompts(p)
    out = d / "output"
    out.mkdir(exist_ok=True)
    (out / "prompts.json").write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "prompts.md").write_text(pr.to_markdown(p, items), encoding="utf-8")
    (out / "prompts.csv").write_text(pr.to_csv(items), encoding="utf-8-sig")
    print(f"Wrote {len(items)} shot prompts to {out}")
    return 0


def cmd_render(a):
    d = _pdir(a)
    p = proj.load(d)
    out = Path(a.out) if a.out else d / "output" / "film.mp4"
    try:
        res = rn.render(p, d, out, lambda s, f: print(f"  [{f:4.0%}] {s}"))
    except rn.ValidationFailed as e:
        for i in e.report.errors:
            print(f"[ERROR] {i.message}")
        print("Render refused: fix the errors above.")
        return 1
    print(f"Rendered {res['output']}\n{res['disclosure']}")
    return 0


def cmd_demo(a):
    from .demo import make_demo
    d = _pdir(a)
    res = make_demo(d, render_it=not a.no_render, progress=lambda s, f: print(f"  [{f:4.0%}] {s}"))
    print("Demo project ready:", d, ("\nRendered " + res["output"]) if res else "")
    return 0


def cmd_new(a):
    d = _pdir(a)
    if (d / "project.json").exists():
        print("Project already exists:", d)
        return 1
    proj.save(d, proj.normalize({"title": Path(a.project).name}))
    (d / "media").mkdir(exist_ok=True)
    print("Created", d)
    return 0


def cmd_narration(a):
    d = _pdir(a)
    p = proj.load(d)
    pl = nar.plan(p, d)
    if a.action == "plan":
        for r in pl["segments"]:
            print(f"{r['id']:6} {r['speaker']:8} {r['start']:7.2f} -> {r['end']:7.2f}  "
                  f"({'measured' if r['measured'] else 'ESTIMATED'}){'  [editorial proposal]' if r['editorial'] else ''}")
        print(f"Total narration: {pl['total']:.2f}s  {pl['note']}")
        return 0
    if a.action == "assemble":
        out = d / "output" / "narration_assembled.wav"
        try:
            res = nar.assemble(p, d, out)
        except ValueError as e:
            print("ERROR:", e)
            return 1
        print(f"Assembled {out} ({res['total']:.2f}s)")
        return 0
    res = nar.sync_shot_durations(p, pl)
    proj.save(d, res["project"])
    print("Updated shots:", ", ".join(res["changed"]) or "none")
    if res["estimated"]:
        print("WARNING: these shots use ESTIMATED timing (no audio yet):", ", ".join(res["estimated"]))
    return 0


def cmd_tts(a):
    from . import tts
    if a.action == "status":
        print(json.dumps(tts.status(), indent=2))
        return 0
    if a.action == "download":
        if not a.yes:
            print("This downloads model weights from the network (Hugging Face). Re-run with --yes to proceed.")
            return 1
        print(tts.download())
        return 0
    d = _pdir(a)
    p = proj.load(d)
    try:
        res = tts.generate(p, d, a.segments.split(",") if a.segments else None, overwrite=a.overwrite)
    except tts.TTSError as e:
        print("TTS not run:", e)
        return 1
    proj.save(d, p)
    print(res)
    return 0 if res["ok"] else 1


def cmd_voices(a):
    from . import batch
    p = proj.load(_pdir(a))
    ids = [s["id"] for s in p["speakers"]]
    res = batch.prep_voices(ids)
    print(json.dumps(res, indent=2))
    return 0 if all("ref" in v for v in res.values()) else 1


def cmd_ttsbatch(a):
    from . import batch, tts
    d = _pdir(a)
    p = proj.load(d)
    try:
        res = batch.render_all(p, d, engine=a.engine, stock=a.stock, overwrite=a.overwrite,
                               only=set(a.segments.split(",")) if a.segments else None, limit=a.limit,
                               stand_in_ok=a.stand_in)
    except tts.TTSError as e:
        print("TTS batch not run:", e)
        return 1
    proj.save(d, p)
    print(json.dumps(res, indent=2))
    return 0 if res["ok"] else 1


def cmd_clips(a):
    from . import clips
    d = _pdir(a)
    p = proj.load(d)
    nar_pl = nar.plan(p, d)
    p = nar.sync_shot_durations(p, nar_pl)["project"]
    rep = clips.coverage_report(p, d)
    print(f"{'shot':6} {'need s':>7} {'clips':>5} {'clip s':>7} {'speed':>6} {'reused s':>9} {'missing s':>9} {'clips for all-unique':>21}")
    for r in rep["shots"]:
        print(f"{r['shot']:6} {r['duration']:7.1f} {r['clips']:5} {r['clip_seconds']:7.1f} {r['speed']:6.2f} "
              f"{r['reused_seconds']:9.1f} {r['missing_seconds']:9.1f} {r['clips_for_all_unique']:21}")
    print(f"\nFilm {rep['total_seconds']:.0f}s | unique footage placed {rep['unique_seconds']:.0f}s | "
          f"repeated {rep['reused_seconds']:.0f}s | uncovered {rep['missing_seconds']:.0f}s | "
          f"shots with no clips: {len(rep['shots_without_clips'])}")
    if not nar_pl["all_measured"]:
        print("NOTE: narration timing is ESTIMATED (not every segment has audio yet).")
    return 0


def cmd_build(a):
    from . import build as bd
    d = _pdir(a)
    p = proj.load(d)
    try:
        rep = bd.build(p, d, out_name=a.name, progress=lambda s, f: print(f"  [{f:4.0%}] {s}"),
                       music=a.music, fps=a.fps, shot_transition=a.shot_transition, burn=not a.soft_captions)
    except bd.BuildError as e:
        print("BUILD REFUSED:", e)
        return 1
    except rn.ValidationFailed as e:
        for i in e.report.errors:
            print("[ERROR]", i.message)
        return 1
    print(json.dumps({k: v for k, v in rep.items() if k != "chapters"}, indent=2))
    print(open(rep["chapters_file"], encoding="utf-8").read())
    return 0


def cmd_pilot(a):
    from . import pilot
    if a.dryrun:
        d = ROOT / "pilot_synthetic_dryrun"
        res = pilot.dryrun(d, progress=lambda s, f: print(f"  [{f:4.0%}] {s}"))
        print("SYNTHETIC dry run (tones + placeholder art, NOT voices). Rendered", res["output"])
        return 0
    d = ROOT / "pilot_married_to_the_don"
    if (d / "project.json").exists() and not a.force:
        print("Pilot already exists:", d, "(use --force to overwrite)")
        return 1
    proj.save(d, pilot.build_pilot())
    (d / "media" / "pilot").mkdir(parents=True, exist_ok=True)
    print("Created", d, "- import your images + narration WAVs, then validate/render.")
    return 0


def cmd_adapt(a):
    from . import adaptation as ad
    if a.action == "build":
        res = ad.write_outputs(Path.cwd())
        st = res["stats"]
        print(f"Built {res['segments']} segments, {res['shots']} shots. Spoken words: {st['total_words']} "
              f"(optional CTA {st['optional_cta_words']}). Estimated runtime (NOT measured): "
              + ", ".join(f"{k} wpm -> {v/60:.1f} min" for k, v in st["estimated_seconds_at_wpm"].items()))
        return 0
    st = ad.word_stats(ad.parse_script(Path("docs/adaptation/script.md")))
    print(json.dumps(st, indent=2))
    return 0


def cmd_ui(a):
    from .server import serve
    serve(Path(a.root), a.project, a.port, open_browser=not a.no_browser)
    return 0


def cmd_package(a):
    from .packaging import make_zip
    print("Created", make_zip(Path.cwd(), Path(a.out)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ofs", description="Original Film Studio")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("validate", cmd_validate), ("prompts", cmd_prompts), ("new", cmd_new)):
        s = sub.add_parser(name)
        s.add_argument("project", help="project name under ./projects or a folder path")
        s.set_defaults(fn=fn)
    s = sub.add_parser("render"); s.add_argument("project"); s.add_argument("--out"); s.set_defaults(fn=cmd_render)
    s = sub.add_parser("demo"); s.add_argument("project", nargs="?", default="demo_30s")
    s.add_argument("--no-render", action="store_true"); s.set_defaults(fn=cmd_demo)
    s = sub.add_parser("ui"); s.add_argument("--root", default=str(ROOT)); s.add_argument("--project", default=None)
    s.add_argument("--port", type=int, default=8765); s.add_argument("--no-browser", action="store_true")
    s.set_defaults(fn=cmd_ui)
    s = sub.add_parser("narration"); s.add_argument("action", choices=["plan", "assemble", "sync"])
    s.add_argument("project"); s.set_defaults(fn=cmd_narration)
    s = sub.add_parser("tts"); s.add_argument("action", choices=["status", "generate", "download"])
    s.add_argument("project", nargs="?", default="pilot_married_to_the_don"); s.add_argument("--segments")
    s.add_argument("--overwrite", action="store_true"); s.add_argument("--yes", action="store_true"); s.set_defaults(fn=cmd_tts)
    s = sub.add_parser("voices"); s.add_argument("project", nargs="?", default="married_to_the_don_full_film")
    s.set_defaults(fn=cmd_voices)
    s = sub.add_parser("ttsbatch", aliases=["tts-batch"]); s.add_argument("project", nargs="?", default="married_to_the_don_full_film")
    s.add_argument("--engine", choices=["chatterbox", "espeak"], default="chatterbox")
    s.add_argument("--stock", action="store_true", help="chatterbox built-in voice, no cloning")
    s.add_argument("--stand-in", action="store_true", help="allow the robotic espeak stand-in (pipeline tests only)")
    s.add_argument("--segments"); s.add_argument("--limit", type=int); s.add_argument("--overwrite", action="store_true")
    s.set_defaults(fn=cmd_ttsbatch)
    s = sub.add_parser("clips"); s.add_argument("project", nargs="?", default="married_to_the_don_full_film"); s.set_defaults(fn=cmd_clips)
    s = sub.add_parser("build"); s.add_argument("project", nargs="?", default="married_to_the_don_full_film")
    s.add_argument("--name", default="film.mp4"); s.add_argument("--music"); s.add_argument("--fps", type=int)
    s.add_argument("--shot-transition", choices=["cut", "fade"]); s.add_argument("--soft-captions", action="store_true")
    s.set_defaults(fn=cmd_build)
    s = sub.add_parser("pilot"); s.add_argument("--force", action="store_true")
    s.add_argument("--dryrun", action="store_true", help="synthetic tones+art check of assembly; not voices"); s.set_defaults(fn=cmd_pilot)
    s = sub.add_parser("adapt"); s.add_argument("action", choices=["build", "stats"]); s.set_defaults(fn=cmd_adapt)
    s = sub.add_parser("package"); s.add_argument("--out", default="dist/original-film-studio.zip"); s.set_defaults(fn=cmd_package)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

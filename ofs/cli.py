from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import project as proj, validate as val, prompts as pr, render as rn

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
    s = sub.add_parser("package"); s.add_argument("--out", default="dist/original-film-studio.zip"); s.set_defaults(fn=cmd_package)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

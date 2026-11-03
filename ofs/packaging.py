"""Build the distributable ZIP: source + docs + sample project + rendered demo (if present)."""
from __future__ import annotations

import zipfile
from pathlib import Path

INCLUDE_DIRS = ["ofs", "tests", "docs", "scripts", "projects"]
INCLUDE_FILES = ["README.md", "requirements.txt", "requirements-dev.txt", "setup.bat", "run.bat",
                 "run.sh", ".gitignore"]
SKIP_PARTS = {"__pycache__", ".pytest_cache", ".venv", "media"}


def make_zip(root: Path, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    top = "original-film-studio"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in INCLUDE_FILES:
            if (root / f).is_file():
                z.write(root / f, f"{top}/{f}")
        for d in INCLUDE_DIRS:
            for p in sorted((root / d).rglob("*")):
                rel = p.relative_to(root)
                if not p.is_file() or SKIP_PARTS & set(rel.parts) or p.suffix == ".pyc":
                    continue
                if "output" in rel.parts:
                    continue  # only the demo render is added, under demo/, below
                z.write(p, f"{top}/{rel.as_posix()}")
        demo = root / "projects" / "demo_30s" / "output"
        for name in ("demo_30s.mp4", "demo_30s.render.json"):
            if (demo / name).is_file():
                z.write(demo / name, f"{top}/demo/{name}")
    return out

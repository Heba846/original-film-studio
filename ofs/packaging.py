"""Build the distributable ZIP: source + docs + sample project + rendered demo (if present)."""
from __future__ import annotations

import zipfile
from pathlib import Path

INCLUDE_DIRS = ["ofs", "tests", "docs", "scripts", "projects"]
INCLUDE_FILES = ["README.md", "requirements.txt", "requirements-dev.txt", "setup.bat", "run.bat",
                 "run.sh", "setup_tts.bat", ".gitignore"]
SKIP_PARTS = {"__pycache__", ".pytest_cache", ".venv", ".venv-tts", "media", "voices", "references"}
SKIP_SUFFIX = {".pyc", ".wav", ".mp3", ".flac", ".m4a", ".ogg", ".pt", ".pth", ".ckpt", ".safetensors", ".npy", ".npz", ".mp4"}


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
                if not p.is_file() or SKIP_PARTS & set(rel.parts) or p.suffix.lower() in SKIP_SUFFIX:
                    continue
                if "output" in rel.parts:
                    continue  # only the demo render is added, under demo/, below
                z.write(p, f"{top}/{rel.as_posix()}")
        dry = root / "projects" / "pilot_synthetic_dryrun" / "output"
        for name in ("pilot_dryrun.mp4", "pilot_dryrun.render.json"):
            if (dry / name).is_file():
                z.write(dry / name, f"{top}/demo/SYNTHETIC_{name}")
        demo = root / "projects" / "demo_30s" / "output"
        for name in ("demo_30s.mp4", "demo_30s.render.json"):
            if (demo / name).is_file():
                z.write(demo / name, f"{top}/demo/{name}")
    return out

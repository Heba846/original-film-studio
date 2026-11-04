"""Plan still-image generation for the cheap, fully automatic path: N images per shot, one per ~9 s of narration.

`python -m ofs stills <project>` writes output/stills_jobs.json which notebooks/colab_stills.ipynb reads.
Nothing here calls a model. Each beat of a shot gets a different camera angle so a 30 s shot is not one picture.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from . import clips as clips_mod, project as proj, prompts as pr

BEAT_SECONDS = 9.0
MAX_BEATS = 5
ANGLES = ["", "tighter framing on the most important detail of the scene", "wider establishing angle of the same scene",
          "over-the-shoulder angle in the same scene", "low angle in the same scene"]


def beats_for(duration: float, existing_clips: int = 0) -> int:
    """Stills needed for a shot of `duration`; clips already supplied each cover ~7.5 s."""
    left = max(duration - existing_clips * 7.5, 0)
    return 0 if left < 3 else min(MAX_BEATS, max(1, round(left / BEAT_SECONDS)))


def build_jobs(project: dict, base, width=1344, height=768, seed=1234) -> dict:
    project = proj.normalize(project)
    plist = {p["shot_id"]: p for p in pr.build_prompts(project)}
    jobs, total = [], 0
    for s in project["shots"]:
        n = beats_for(float(s["duration"]), len(clips_mod.discover(s, base)))
        if not n:
            continue
        p = plist[s["id"]]
        files = [f"{s['id']}_{i + 1}.png" for i in range(n)]
        jobs.append({"shot": s["id"], "beats": n, "files": files, "duration": s["duration"],
                     "prompts": [(p["still_prompt"] + (" Camera variation: " + ANGLES[i % len(ANGLES)] + "." if ANGLES[i % len(ANGLES)] else "")
                                  ) for i in range(n)],
                     "negative": p["negative_prompt"], "seed": seed + int(s["id"].lstrip("s") or 0) * 100})
        total += n
    return {"width": width, "height": height, "total_images": total, "jobs": jobs,
            "note": "one image per ~9 s of narration; files go to media/stills/<shot>_<n>.png"}


def write_jobs(project: dict, base, out=None) -> Path:
    base = Path(base)
    out = Path(out or base / "output" / "stills_jobs.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_jobs(project, base), indent=1, ensure_ascii=False), encoding="utf-8")
    return out

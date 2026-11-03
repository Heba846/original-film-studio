"""Project model: a plain JSON document stored as <project>/project.json."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

SCHEMA_VERSION = 1
MOTIONS = ["none", "zoom_in", "zoom_out", "pan_left", "pan_right"]
TRANSITIONS = ["cut", "fade"]

DEFAULT_PROJECT = {
    "version": SCHEMA_VERSION,
    "title": "Untitled film",
    "logline": "",
    "style": "",
    "script": "",
    "characters": [],
    "locations": [],
    "shots": [],
    "audio": {"narration": "", "music": "", "narration_volume": 1.0,
              "music_volume": 0.25, "duck_music": True},
    "captions": {"srt": "", "mode": "none"},
    "render": {"fps": 30, "crf": 20, "preset": "medium"},
}
SHOT_DEFAULTS = {
    "id": "", "title": "", "kind": "image", "asset": "", "duration": 5.0,
    "trim_start": 0.0, "motion": "none", "transition": "cut", "characters": [],
    "location": "", "action": "", "camera": "", "dialogue": "", "continuity_notes": "",
}
CHARACTER_DEFAULTS = {"id": "", "name": "", "description": "", "wardrobe": "",
                      "voice_notes": "", "continuity_notes": "", "reference": ""}
LOCATION_DEFAULTS = {"id": "", "name": "", "description": "", "lighting": "",
                     "continuity_notes": "", "reference": ""}

_NAME_RE = re.compile(r"^[\w][\w \-]{0,63}$")


def valid_project_name(name: str) -> bool:
    return bool(_NAME_RE.match(name or ""))


def normalize(data: dict) -> dict:
    """Fill missing keys with defaults (never drops unknown keys)."""
    p = copy.deepcopy(DEFAULT_PROJECT)
    for k, v in (data or {}).items():
        if k in ("audio", "captions", "render") and isinstance(v, dict):
            p[k].update(v)
        else:
            p[k] = v
    p["characters"] = [{**CHARACTER_DEFAULTS, **c} for c in p.get("characters") or []]
    p["locations"] = [{**LOCATION_DEFAULTS, **c} for c in p.get("locations") or []]
    p["shots"] = [{**SHOT_DEFAULTS, **s} for s in p.get("shots") or []]
    return p


def load(path) -> dict:
    path = Path(path)
    if path.is_dir():
        path = path / "project.json"
    with open(path, "r", encoding="utf-8") as f:
        return normalize(json.load(f))


def save(path, data: dict) -> Path:
    path = Path(path)
    if path.is_dir() or path.suffix != ".json":
        path = path / "project.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(normalize(data), f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)
    return path


def resolve(base, rel) -> Path:
    """Resolve an asset path: absolute stays, relative is under the project dir."""
    p = Path(str(rel))
    return p if p.is_absolute() else Path(base) / p


def timeline(project: dict):
    """[(shot_id, start, end)] in current shot order. Invalid durations count as 0."""
    t, out = 0.0, []
    for s in project.get("shots", []):
        try:
            d = float(s.get("duration"))
        except (TypeError, ValueError):
            d = 0.0
        d = max(d, 0.0)
        out.append((s.get("id"), round(t, 3), round(t + d, 3)))
        t += d
    return out


def total_duration(project: dict) -> float:
    tl = timeline(project)
    return tl[-1][2] if tl else 0.0


def move_shot(project: dict, shot_id: str, new_index: int) -> dict:
    shots = project["shots"]
    i = next(i for i, s in enumerate(shots) if s["id"] == shot_id)
    s = shots.pop(i)
    shots.insert(max(0, min(new_index, len(shots))), s)
    return project

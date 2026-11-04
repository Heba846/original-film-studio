"""Captions (SRT) and YouTube chapters derived from MEASURED narration timing.

Caption cue times are the segment's real speech window split in proportion to characters, so they are
as accurate as the segment boundaries (exact per segment, approximate inside a long segment).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import srt as srtlib

MAX_LINE = 42
MAX_CUE_CHARS = 84


def _wrap(words: list[str]) -> str:
    """Balance words into at most 2 lines."""
    text = " ".join(words)
    if len(text) <= MAX_LINE:
        return text
    best, best_diff = None, 10 ** 9
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        diff = abs(len(a) - len(b))
        if diff < best_diff:
            best, best_diff = (a, b), diff
    return "\n".join(best)


def split_text(text: str, max_chars: int = MAX_CUE_CHARS) -> list[str]:
    """Split into cue-sized pieces at sentence/clause boundaries, then by words."""
    text = " ".join(text.split())
    parts = re.split(r"(?<=[.!?…])\s+", text)
    out = []
    for p in parts:
        if len(p) <= max_chars:
            out.append(p)
            continue
        sub = re.split(r"(?<=[,;:—–])\s+", p)
        cur = ""
        for s in sub:
            if cur and len(cur) + 1 + len(s) > max_chars:
                out.append(cur)
                cur = s
            else:
                cur = (cur + " " + s).strip()
        if cur:
            out.append(cur)
    final = []
    for p in out:  # words fallback for a clause still too long
        if len(p) <= max_chars:
            final.append(p)
            continue
        cur = ""
        for w in p.split():
            if cur and len(cur) + 1 + len(w) > max_chars:
                final.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            final.append(cur)
    # merge tiny pieces forward
    merged = []
    for p in final:
        if merged and len(p) < 14 and len(merged[-1]) + 1 + len(p) <= max_chars:
            merged[-1] += " " + p
        else:
            merged.append(p)
    return merged


def build_cues(project: dict, timing: dict) -> list[dict]:
    texts = {s["id"]: s["text"] for s in project["narration_segments"]}
    cues = []
    for row in timing["segments"]:
        pieces = split_text(texts[row["id"]])
        if not pieces:
            continue
        total_chars = sum(len(p) for p in pieces)
        span = max(row["speech_end"] - row["start"], 0.2)
        t = row["start"]
        for p in pieces:
            d = span * len(p) / total_chars
            cues.append({"start": t, "end": t + d - 0.02, "text": _wrap(p.split())})
            t += d
    return cues


def write_srt(cues, path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(srtlib.format_srt(cues), encoding="utf-8")
    return path


def chapter_titles(script: str) -> dict:
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (CH\d+) \| (.*)$", script, re.M)}


def _yt(t: float) -> str:
    t = int(t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"


def chapters(project: dict, timing: dict, seg_chapters: dict) -> list[dict]:
    """[{start, title, code}] using the first segment of each chapter. seg_chapters: segment id -> 'CH03'."""
    titles = chapter_titles(project.get("script", ""))
    seen, out = set(), []
    for row in timing["segments"]:
        ch = seg_chapters.get(row["id"])
        if ch and ch not in seen:
            seen.add(ch)
            out.append({"code": ch, "start": row["start"], "title": titles.get(ch, ch)})
    if out:
        out[0]["start"] = 0.0
    return out


def chapters_text(chs: list[dict]) -> str:
    lines = [f"{_yt(c['start'])} {c['title']}" for c in chs]
    problems = []
    if len(chs) < 3:
        problems.append("YouTube needs at least 3 chapters")
    for a, b in zip(chs, chs[1:]):
        if b["start"] - a["start"] < 10:
            problems.append(f"chapter '{a['title']}' is shorter than 10 s (YouTube may ignore the list)")
    return "\n".join(lines) + "\n", problems


def load_seg_chapters(path) -> dict:
    p = Path(path)
    if not p.is_file():
        return {}
    return {s["id"]: s.get("chapter") for s in json.loads(p.read_text(encoding="utf-8"))}

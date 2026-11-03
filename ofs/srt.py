"""Minimal SRT parser/formatter (captions are IMPORTED, never generated here)."""
from __future__ import annotations

import re

_TIME = re.compile(r"(\d+):(\d{2}):(\d{2})[,.](\d{1,3})")


def _t(s: str) -> float | None:
    m = _TIME.fullmatch(s.strip())
    if not m:
        return None
    h, mi, se, ms = m.groups()
    return int(h) * 3600 + int(mi) * 60 + int(se) + int(ms.ljust(3, "0")) / 1000


def parse(text: str):
    """Return (cues, errors). cue = dict(start, end, text, index)."""
    text = text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    cues, errors = [], []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.split("\n")]
        if not any(l.strip() for l in lines):
            continue
        i = 0
        if lines and lines[0].strip().isdigit():
            i = 1
        if i >= len(lines) or "-->" not in lines[i]:
            errors.append(f"cue block without a timing line: {block[:40]!r}")
            continue
        a, _, b = lines[i].partition("-->")
        start, end = _t(a), _t(b.split()[0] if b.split() else "")
        if start is None or end is None:
            errors.append(f"bad timestamp: {lines[i].strip()!r}")
            continue
        if end <= start:
            errors.append(f"cue ends before it starts: {lines[i].strip()!r}")
            continue
        body = "\n".join(lines[i + 1:]).strip()
        if not body:
            errors.append(f"empty caption text at {lines[i].strip()!r}")
            continue
        cues.append({"index": len(cues) + 1, "start": start, "end": end, "text": body})
    return cues, errors


def fmt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def format_srt(cues) -> str:
    return "\n".join(
        f"{i}\n{fmt_time(c['start'])} --> {fmt_time(c['end'])}\n{c['text']}\n"
        for i, c in enumerate(cues, 1)
    )

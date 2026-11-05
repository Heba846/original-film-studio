"""Subtitle cues from narration timing -> .srt (for YouTube upload) and .ass (burned in)."""
from __future__ import annotations

import re
import textwrap

SPLIT = re.compile(r"(?<=[.!?…;:,—])\s+")


def chunk_text(text: str, max_chars: int = 84) -> list[str]:
    """Split text into subtitle-sized pieces at punctuation, never mid-word."""
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return [text]
    pieces, cur = [], ""
    for part in SPLIT.split(text):
        if cur and len(cur) + 1 + len(part) > max_chars:
            pieces.append(cur)
            cur = part
        else:
            cur = f"{cur} {part}".strip()
    if cur:
        pieces.append(cur)
    out = []
    for p in pieces:  # still too long (no punctuation): hard wrap on words
        if len(p) > max_chars:
            out.extend(textwrap.wrap(p, max_chars))
        else:
            out.append(p)
    return out


def line_cues(text: str, start: float, dur: float, max_chars: int) -> list[dict]:
    """Spread `dur` seconds over chunks proportionally to their length."""
    chunks = chunk_text(text, max_chars)
    total = sum(len(c) for c in chunks) or 1
    t, cues = start, []
    for c in chunks:
        d = dur * len(c) / total
        cues.append({"start": round(t, 3), "end": round(t + d, 3), "text": c})
        t += d
    return cues


def _t(sec: float, sep: str, frac_digits: int) -> str:
    sec = max(sec, 0.0)
    cs = int(round(sec * 10 ** frac_digits))
    base = 10 ** frac_digits
    h, rem = divmod(cs, 3600 * base)
    m, rem = divmod(rem, 60 * base)
    s, f = divmod(rem, base)
    return f"{h:d}:{m:02d}:{s:02d}{sep}{f:0{frac_digits}d}"


def write_srt(cues: list[dict], path) -> None:
    out = []
    for i, c in enumerate(cues, 1):
        out.append(f"{i}\n{_t(c['start'], ',', 3).zfill(12)} --> {_t(c['end'], ',', 3).zfill(12)}\n{c['text']}\n")
    path.write_text("\n".join(out), encoding="utf-8")


def write_ass(cues: list[dict], path, width: int, height: int, font: str, size: int, wrap: int) -> None:
    fs = round(size * height / 1080)
    margin_v = round(70 * height / 1080)
    outline = max(2, round(3 * height / 1080))
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{fs},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{outline},1,2,{round(width * 0.08)},{round(width * 0.08)},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    rows = []
    for c in cues:
        txt = "\\N".join(textwrap.wrap(c["text"], wrap)).replace("{", "(").replace("}", ")")
        rows.append(f"Dialogue: 0,{_t(c['start'], '.', 2)},{_t(c['end'], '.', 2)},Default,,0,0,0,,{txt}")
    path.write_text(head + "\n".join(rows) + "\n", encoding="utf-8")

"""Step 1: chapters (txt/md) -> scenes.json with every line tagged by speaker.

Speaker attribution is heuristic (dialogue tags such as `"...," Victor said` or `she asked`).
Every guessed line is flagged "guess": true so you can review/edit scenes.json before narrating.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .config import Config

BREAK_RE = re.compile(r"^\s*(?:(?:\*\s*){3,}|(?:~\s*){3,}|-{3,}|#{2,}|\[scene break\])\s*$", re.I)
QUOTE_RE = re.compile(r"“([^”]*)”|\"([^\"]*)\"")
SENT_END = re.compile(r"(?<=[.!?…])\s+")


def clean_markdown(text: str) -> str:
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text)
    text = re.sub(r"(?<!\w)([*_])(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def parse_chapter(text: str, fallback_title: str) -> tuple[str, list[list[str]]]:
    """Return (title, scenes) where scenes is a list of paragraph lists."""
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].strip() == "---":  # front matter
        try:
            end = lines[1:].index("---") + 2
            lines = lines[end:]
        except ValueError:
            pass
    title = fallback_title
    scenes: list[list[str]] = [[]]
    para: list[str] = []

    def flush():
        if para:
            p = clean_markdown(" ".join(para))
            if p:
                scenes[-1].append(p)
            para.clear()

    title_found = False
    for ln in lines:
        s = ln.strip()
        if not title_found and re.match(r"^#\s+\S", s):
            title = clean_markdown(s.lstrip("# "))
            title_found = True
            continue
        if BREAK_RE.match(s):
            flush()
            if scenes[-1]:
                scenes.append([])
            continue
        if not s:
            flush()
            continue
        para.append(s.lstrip("#> ").strip() if s.startswith(("#", ">")) else s)
    flush()
    return title, [sc for sc in scenes if sc]


def split_paragraph(par: str) -> list[tuple[str, str]]:
    """Split into [('narration'|'dialogue', text)] by quote marks."""
    out, pos = [], 0
    for m in QUOTE_RE.finditer(par):
        pre = par[pos:m.start()].strip()
        if pre:
            out.append(("narration", pre))
        q = (m.group(1) or m.group(2) or "").strip()
        if q:
            out.append(("dialogue", q))
        pos = m.end()
    tail = par[pos:].strip()
    if tail:
        out.append(("narration", tail))
    return out


class Attributor:
    def __init__(self, cfg: Config):
        self.names = dict(cfg["characters"])
        self.pronouns = {k.lower(): v for k, v in cfg["speakers"]["pronouns"].items()}
        self.default = cfg["speakers"]["default_dialogue"]
        alts = sorted(self.names, key=len, reverse=True)
        parts = [re.escape(n) for n in alts] + [rf"{re.escape(p)}" for p in self.pronouns]
        self.name_re = re.compile(r"\b(" + "|".join(parts) + r")\b", re.I) if parts else None
        self.exact = {n.lower(): s for n, s in self.names.items()}

    def _find(self, snippet: str) -> str | None:
        if not self.name_re:
            return None
        for m in self.name_re.finditer(snippet):
            w = m.group(1)
            if w.lower() in self.exact:
                # a capitalised name; ignore lowercase accidental matches of short names
                if w[0].isupper() or w.lower() not in self.pronouns:
                    return self.exact[w.lower()]
            if w.lower() in self.pronouns:
                return self.pronouns[w.lower()]
        return None

    def speaker(self, segs, i, history: list[str]) -> tuple[str, bool]:
        after = before = ""
        if i + 1 < len(segs) and segs[i + 1][0] == "narration":
            after = SENT_END.split(segs[i + 1][1])[0]
        if i > 0 and segs[i - 1][0] == "narration":
            before = SENT_END.split(segs[i - 1][1])[-1]
        who = self._find(after) or self._find(before)
        if who:
            return who, False
        recent = [s for s in history if s != "narrator"]
        if recent:
            last = recent[-1]
            other = next((s for s in reversed(recent) if s != last), None)
            if other:
                return other, True
            return (self.default if self.default != last else last), True
        return self.default, True


def build_scenes(cfg: Config, files: list[Path] | None = None) -> dict:
    files = files or sorted(p for p in cfg.chapters_dir.iterdir()
                            if p.suffix.lower() in (".md", ".txt") and not p.name.startswith("."))
    if not files:
        raise SystemExit(f"No chapters found in {cfg.chapters_dir} (put .md/.txt files there).")
    attrib = Attributor(cfg)
    max_words = cfg["scenes"]["max_scene_words"]
    scenes_out = []
    chapters = []
    for ci, f in enumerate(files, 1):
        cid = f"ch{ci:02d}"
        title, raw_scenes = parse_chapter(f.read_text(encoding="utf-8"), f.stem.replace("-", " ").replace("_", " ").title())
        chapters.append({"id": cid, "title": title, "source": f.name})
        # split over-long scenes at paragraph boundaries
        groups: list[list[str]] = []
        for sc in raw_scenes:
            cur, words = [], 0
            for p in sc:
                w = len(p.split())
                if cur and words + w > max_words:
                    groups.append(cur)
                    cur, words = [], 0
                cur.append(p)
                words += w
            if cur:
                groups.append(cur)
        history: list[str] = []
        for si, paras in enumerate(groups, 1):
            lines = []
            for p in paras:
                segs = split_paragraph(p)
                for i, (kind, txt) in enumerate(segs):
                    if kind == "narration":
                        lines.append({"speaker": "narrator", "text": txt})
                        history.append("narrator")
                    else:
                        who, guess = attrib.speaker(segs, i, history)
                        entry = {"speaker": who, "text": txt}
                        if guess:
                            entry["guess"] = True
                        lines.append(entry)
                        history.append(who)
            scenes_out.append({"id": f"{cid}-s{si:02d}", "chapter": cid, "image": None, "lines": lines})
    return {"title": cfg["project"]["title"], "chapters": chapters, "scenes": scenes_out}


def run(cfg: Config, force: bool = False) -> Path:
    out = cfg.build_dir / "scenes.json"
    if out.exists() and not force:
        print(f"{out} exists - keeping your edits. Use --force to regenerate.")
        return out
    doc = build_scenes(cfg)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    n_lines = sum(len(s["lines"]) for s in doc["scenes"])
    guesses = sum(1 for s in doc["scenes"] for l in s["lines"] if l.get("guess"))
    words = sum(len(l["text"].split()) for s in doc["scenes"] for l in s["lines"])
    print(f"scenes.json: {len(doc['chapters'])} chapter(s), {len(doc['scenes'])} scenes, {n_lines} lines, "
          f"{words} words (~{words / 150:.1f} min at 150 wpm), {guesses} guessed speakers -> {out}")
    return out

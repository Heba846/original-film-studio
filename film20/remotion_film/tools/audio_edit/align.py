#!/usr/bin/env python3
"""Forced word alignment with PocketSphinx (local, bundled en-us model; no network, no paid service).

Usage: <venv>/bin/python tools/audio_edit/align.py <wav> "<transcript>" [--json out.json]
Prints one line per word: start end word (seconds, 10 ms resolution). Number tokens must be spelled
as they are spoken (e.g. 'four ten'). Out-of-dictionary names are added from tools/audio_edit/lexicon.txt.
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
from pocketsphinx import Decoder

HERE = Path(__file__).resolve().parent

from textnorm import SPOKEN, spoken, norm  # noqa: F401

def align(wav: str, transcript: str):
    with tempfile.NamedTemporaryFile(suffix=".raw") as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "s16le", tmp.name], check=True)
        raw = Path(tmp.name).read_bytes()
    d = Decoder(samprate=16000, loglevel="ERROR")
    lex = {}
    lf = HERE / "lexicon.txt"
    if lf.exists():
        for line in lf.read_text().splitlines():
            if line.strip() and not line.startswith("#"):
                w, ph = line.split(None, 1); lex[w] = ph.strip()
    words = norm(transcript)
    for w in set(words):
        if d.lookup_word(w) is None:
            if w not in lex:
                raise SystemExit(f"OOV word '{w}': add 'word PH ON ES' to tools/audio_edit/lexicon.txt")
            d.add_word(w, lex[w], True)
            for k in range(2, 5):
                if f"{w}({k})" in lex: d.add_word(f"{w}({k})", lex[f"{w}({k})"], True)
    d.set_align_text(" ".join(words))
    d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    segs = [(s.word, s.start_frame / 100, (s.end_frame + 1) / 100) for s in d.seg()]
    hyp = d.hyp()
    return [s for s in segs if s[0] not in ("<s>", "</s>")], (hyp.score if hyp else None)

if __name__ == "__main__":
    segs, score = align(sys.argv[1], sys.argv[2])
    for w, a, b in segs:
        print(f"{a:7.2f} {b:7.2f} {w}")
    print("score", score)
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps({"words": segs, "score": score}, indent=1))

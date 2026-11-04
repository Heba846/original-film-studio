#!/usr/bin/env python3
"""Force-align every narration line (local PocketSphinx) -> edition20/out/word_alignment.json.
film_build.py uses it to time captions on real word boundaries. Lines that fail to align fall back to
proportional timing and are listed as 'estimated' in STATUS.md."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from align import align, spoken, norm

ROOT = Path(__file__).resolve().parents[2]
edl = json.loads((ROOT / "edition20/edit_decision_list.json").read_text())
out, failed = {}, []
for s in edl["segments"]:
    wav = ROOT / s["audio_to_use"]
    best = None
    for v in range(2):
        text = spoken(s["text"], v)
        try:
            words, score = align(str(wav), text)
        except Exception as e:  # noqa
            continue
        sp = [w for w in words if w[0] != "<sil>"]
        want = norm(text)
        partial = False
        missing = len(want) - len(sp)
        if 0 < missing <= 2 and [w[0].split("(")[0] for w in sp] == want[:len(sp)]:
            import wave as _w
            with _w.open(str(wav)) as f: dur = f.getnframes() / f.getframerate()
            last = sp[-1]
            if last[2] >= dur - 0.15:   # last aligned span runs to the clean end of the file: split it evenly
                span = (last[2] - last[1]) / (missing + 1)
                sp = sp[:-1] + [(want[len(sp) - 1 + k], last[1] + k * span, last[1] + (k + 1) * span) for k in range(missing + 1)]
                partial = True
        if len(sp) == len(want) and (best is None or score > best[1]):
            best = (sp, score, v, partial)
    if best is None:
        failed.append(s["id"]); continue
    out[s["id"]] = {"audio": s["audio_to_use"], "variant": best[2], "score": best[1], "partial_end": best[3],
                    "words": [[w.split("(")[0], round(a, 2), round(b, 2)] for w, a, b in best[0]]}
    print(s["id"], "ok", len(best[0]), "words")
(ROOT / "edition20/out/word_alignment.json").write_text(json.dumps({"aligner": "PocketSphinx forced alignment, local en-us model",
    "segments": out, "failed": failed}, indent=1))
print("aligned", len(out), "failed", failed)

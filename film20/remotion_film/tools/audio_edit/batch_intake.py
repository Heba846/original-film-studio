#!/usr/bin/env python3
"""Browser-TTS batch intake: batch MP3/WAVs -> aligned parts -> one WAV per narration segment (public/audio_v2/).

Run with the PocketSphinx venv python:
  <venv>/bin/python tools/audio_edit/batch_intake.py add <zip|dir|files...>   copy B##_<role>.(mp3|wav|m4a) into intake_audio/, align each
  <venv>/bin/python tools/audio_edit/batch_intake.py build                     when all batches are aligned: cut parts, assemble segments
  <venv>/bin/python tools/audio_edit/batch_intake.py select                    mark audio_v2 selected (film_build then uses it)
Options: --batches <json> (default edition20/out/browser_audio_batches.json)  --out <dir> (default public/audio_v2)

Words are never changed. Each batch is force-aligned against exactly its own text (no direction tags); the k-th aligned word is
the k-th word of the ordered parts, so repeated short words cannot swap parts. A part is cut at the middle of the silence between
its last word and the next part's first word. Speech is never time-stretched. Checks per batch: word count, alignment score,
words/min, spoken direction tag at the start ('american', 'accent' in a free decode of the first 4 s), parts too fast/slow.
"""
import json, re, shutil, subprocess, sys, tempfile, zipfile, hashlib, wave, array
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
try:
    from align import align, spoken, norm  # noqa: E402  (PocketSphinx path)
except ImportError:                        # Scribe path (tools/audio_edit/scribe_intake.py) needs no PocketSphinx
    from textnorm import spoken, norm  # noqa: E402

args = sys.argv[1:]
opt = lambda k, d: args[args.index(k) + 1] if k in args else d
BATCHES = Path(opt("--batches", ROOT / "edition20/out/browser_audio_batches.json"))
OUTDIR = Path(opt("--out", ROOT / "public/audio_v2")).resolve()
INTAKE = Path(opt("--intake", ROOT / "intake_audio"))
WORK = INTAKE / "aligned"
SR = 44100
B = json.loads(BATCHES.read_text())
BY_ID = {b["id"]: b for b in B["batches"]}


def run(*c, **k): return subprocess.run(c, check=True, capture_output=True, text=True, **k)


def to_wav(src: Path, dst: Path):
    run("ffmpeg", "-v", "error", "-y", "-i", str(src), "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(dst))


def dur(p: Path) -> float:
    with wave.open(str(p)) as w: return w.getnframes() / w.getframerate()


def free_decode_head(wav: Path, secs=4.0) -> str:
    from pocketsphinx import Decoder
    with tempfile.NamedTemporaryFile(suffix=".raw") as t:
        run("ffmpeg", "-v", "error", "-y", "-i", str(wav), "-t", str(secs), "-ac", "1", "-ar", "16000", "-f", "s16le", t.name)
        raw = Path(t.name).read_bytes()
    d = Decoder(samprate=16000, loglevel="ERROR"); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    return d.hyp().hypstr if d.hyp() else ""


def align_batch(bid: str, wav: Path) -> dict:
    b = BY_ID[bid]
    best = None
    for v in (0, 1):
        toks = [norm(spoken(p["text"], v)) for p in b["parts"]]
        flat = [w for t in toks for w in t]
        try:
            words, score = align(str(wav), " ".join(flat))
        except SystemExit as e:
            return {"error": str(e)}
        sp = [(re.sub(r"\(\d+\)$", "", w), a, e) for w, a, e in words if w not in ("<sil>", "[NOISE]", "<s>", "</s>")]
        ok = len(sp) == len(flat) and all(x[0] == y for x, y in zip(sp, flat))
        cand = {"variant": v, "score": score, "ok": ok, "words": sp, "counts": [len(t) for t in toks],
                "sil": [(a, e) for w, a, e in words if w == "<sil>"]}
        if ok and (best is None or not best["ok"]): best = cand; break
        best = best or cand
    return best


def add(paths):
    INTAKE.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
    files = []
    for p in map(Path, paths):
        if p.suffix.lower() == ".zip":
            with zipfile.ZipFile(p) as z:
                d = Path(tempfile.mkdtemp(dir=INTAKE)); z.extractall(d); files += [f for f in d.rglob("*") if f.is_file()]
        elif p.is_dir(): files += [f for f in p.rglob("*") if f.is_file()]
        else: files.append(p)
    for f in files:
        m = re.match(r"(B\d\d_[a-z]+)", f.name)
        if not m or f.suffix.lower() not in (".mp3", ".wav", ".m4a", ".flac", ".ogg"):
            continue
        bid = m.group(1)
        if bid not in BY_ID: print("UNKNOWN batch", f.name); continue
        wav = WORK / f"{bid}.wav"; to_wav(f, wav)
        r = align_batch(bid, wav)
        if "error" in r: print(bid, "ALIGN ERROR", r["error"]); continue
        d = dur(wav); w = r["words"]
        wpm = round(len(w) / max(1e-6, (w[-1][2] - w[0][1]) / 60), 1) if w else 0
        head = free_decode_head(wav)
        tag = bool(re.search(r"\b(american|accent|english)\b", head.lower()))
        first = w[0][1] if w else None
        r["asr"] = asr_check(bid, wav, r)
        r.update(bid=bid, file=str(f.name), sha256=hashlib.sha256(f.read_bytes()).hexdigest(), dur_s=round(d, 3), wpm=wpm,
                 head_decode=head, spoken_tag_suspected=tag or (first is not None and first > 2.5))
        (WORK / f"{bid}.json").write_text(json.dumps(r))
        print(f"{bid}: {d:7.2f} s  words {len(w)}/{sum(r['counts'])}  ok={r['ok']}  score={r['score']}  {wpm} wpm"
              + ("  ** SPOKEN TAG? head='" + head + "'" if r["spoken_tag_suspected"] else "")
              + f"\n    ASR match {r['asr']['asr_word_match']}  low parts {r['asr']['low_parts']}  squeezed {len(r['asr']['squeezed_words'])}"
              f"  stretched {len(r['asr']['stretched_words'])}  head-decode '{head}'")


def asr_check(bid: str, wav: Path, r: dict) -> dict:
    """Independent check that no words were omitted or added: free (unforced) PocketSphinx decode in 15 s chunks, compared with
    the script tokens part by part (difflib). Forced-alignment symptoms are checked too: a skipped word gets squeezed (<40 ms),
    extra speech makes a word or silence stretch (>1.5 s inside a part)."""
    import difflib
    from pocketsphinx import Decoder
    with tempfile.NamedTemporaryFile(suffix=".raw") as t:
        run("ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "s16le", t.name)
        raw = Path(t.name).read_bytes()
    d = Decoder(samprate=16000, loglevel="ERROR")
    hyp, step = [], 16000 * 2 * 15
    for i in range(0, len(raw), step):
        d.start_utt(); d.process_raw(raw[i:i + step], full_utt=True); d.end_utt()
        if d.hyp(): hyp += [w for w in d.hyp().hypstr.split() if w]
    ref = [w for w, _, _ in r["words"]]
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    hit = [False] * len(ref)
    for a, b_, n in sm.get_matching_blocks():
        for k in range(n): hit[a + k] = True
    per, k = [], 0
    for n in r["counts"]:
        per.append(round(sum(hit[k:k + n]) / max(1, n), 2)); k += n
    FUNC = {"a", "i", "the", "to", "of", "and", "an", "in", "it", "is", "at", "on", "he", "my", "me", "was", "for"}
    squeezed = [(w, a) for w, a, e in r["words"] if e - a < 0.04 and w not in FUNC]
    stretched = [(w, a) for w, a, e in r["words"] if e - a > 1.5]
    return {"asr_word_match": round(sum(hit) / max(1, len(ref)), 3), "asr_hyp_words": len(hyp), "part_match": per,
            "low_parts": [i for i, m in enumerate(per) if m < 0.5 and r["counts"][i] >= 4],
            "squeezed_words": squeezed[:20], "stretched_words": stretched[:20],
            "first_words": ref[:6], "last_words": ref[-6:]}


def part_spans(r: dict, total: float):
    """[(start, end, words_rel)] per part; boundaries in the middle of the gap between neighbouring parts."""
    w, out, k = r["words"], [], 0
    ranges = []
    for n in r["counts"]:
        ranges.append(w[k:k + n]); k += n
    for i, ws in enumerate(ranges):
        a, e = ws[0][1], ws[-1][2]
        prev_e = ranges[i - 1][-1][2] if i else 0.0
        next_a = ranges[i + 1][0][1] if i + 1 < len(ranges) else total
        lo = (prev_e + a) / 2 if i else 0.0
        hi = (e + next_a) / 2 if i + 1 < len(ranges) else total
        s0, s1 = max(lo, a - 0.08), min(hi, e + 0.18)
        out.append((round(s0, 3), round(s1, 3), [(x, round(p - s0, 3), round(q - s0, 3)) for x, p, q in ws]))
    return out


def build():
    missing = [b for b in BY_ID if not (WORK / f"{b}.json").exists()]
    if missing: sys.exit(f"not all batches aligned yet: {missing}")
    R = {b: json.loads((WORK / f"{b}.json").read_text()) for b in BY_ID}
    bad = [b for b, r in R.items() if not r["ok"]]
    if bad: sys.exit(f"alignment mismatch (words differ from the script) in {bad}: re-generate those batches verbatim")
    tags = [b for b, r in R.items() if r["spoken_tag_suspected"]]
    if tags: sys.exit(f"possible spoken direction tag at the start of {tags}: listen and re-generate, or trim and re-add")
    seg_parts: dict = {}
    for bid, r in R.items():
        spans = part_spans(r, R[bid]["dur_s"])
        for p, (s0, s1, ws) in zip(BY_ID[bid]["parts"], spans):
            seg_parts.setdefault(p["segment_id"], []).append({**p, "batch": bid, "s0": s0, "s1": s1, "words": ws, "variant": r["variant"]})
    OUTDIR.mkdir(parents=True, exist_ok=True)
    segs, walign, qa = {}, {}, []
    TEXT = {s["id"]: s["text"] for s in json.loads((ROOT / "src/film/data/film_timeline.json").read_text())["segments"]}
    for sid, parts in sorted(seg_parts.items()):
        parts.sort(key=lambda x: x["start_char"])
        p_text = TEXT[sid]
        inputs, filt, t, words = [], [], 0.0, []
        for i, p in enumerate(parts):
            if i:
                between = p_text[parts[i - 1]["end_char"]:p["start_char"]]
                gap = 0.22 if '"' in between else 0.14
                filt.append(f"aevalsrc=0:d={gap}:s={SR}[g{i}]"); t += gap
            inputs += ["-i", str(WORK / f"{p['batch']}.wav")]
            L = p["s1"] - p["s0"]
            filt.append(f"[{i}:a]atrim={p['s0']}:{p['s1']},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, L - 0.02):.3f}:d=0.02[p{i}]")
            words += [[w, round(a + t, 3), round(e + t, 3)] for w, a, e in p["words"]]
            sp_s = (p["words"][-1][2] - p["words"][0][1]) if p["words"] else 0
            if p["words"] and sp_s / len(p["words"]) < 0.11: qa.append(f"{sid} part {i} ({p['batch']}): {len(p['words'])} words in {sp_s:.2f} s (too fast?)")
            t += L
        order = "".join(f"[g{i}][p{i}]" if i else f"[p{i}]" for i in range(len(parts)))
        filt.append(f"{order}concat=n={2 * len(parts) - 1}:v=0:a=1[out]")
        dst = OUTDIR / f"{sid}.wav"
        run("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(dst))
        rel = str(dst.relative_to(ROOT))
        segs[sid] = {"file": rel, "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(), "dur_s": round(dur(dst), 3),
                     "parts": [{"batch": p["batch"], "role": BY_ID[p["batch"]]["voice_role"], "start_char": p["start_char"],
                                "end_char": p["end_char"], "src_s": [p["s0"], p["s1"]]} for p in parts]}
        vs = {p["variant"] for p in parts}
        walign[sid] = {"audio": rel, "variant": vs.pop() if len(vs) == 1 else 0, "score": None, "partial_end": False, "words": words,
                       **({"mixed_variants": True} if len({p["variant"] for p in parts}) > 1 else {})}
    T = json.loads((ROOT / "src/film/data/film_timeline.json").read_text())
    want = [s["id"] for s in T["segments"]]
    miss = [s for s in want if s not in segs]
    (ROOT / "edition20/audio_v2").mkdir(parents=True, exist_ok=True)
    (ROOT / "edition20/audio_v2/word_alignment.json").write_text(json.dumps({"aligner": "pocketsphinx batch", "segments": walign}, indent=1))
    old = {s["id"]: s["audio_duration_s"] for s in T["segments"]}
    man = {"complete": not miss, "selected": False, "missing": miss, "word_alignment": "edition20/audio_v2/word_alignment.json",
           "batches": {b: {k: R[b][k] for k in ("file", "sha256", "dur_s", "wpm", "score", "variant", "head_decode")} for b in R},
           "speech_s_new": round(sum(v["dur_s"] for v in segs.values()), 2), "speech_s_old": round(sum(old.values()), 2),
           "qa": qa, "segments": segs}
    (ROOT / "edition20/audio_v2/manifest.json").write_text(json.dumps(man, indent=1))
    print(f"{len(segs)}/{len(want)} segments; speech {man['speech_s_new']} s (old {man['speech_s_old']} s); qa notes {len(qa)}; missing {miss}")


def select():
    p = ROOT / "edition20/audio_v2/manifest.json"; m = json.loads(p.read_text())
    if not m["complete"]: sys.exit("audio_v2 incomplete")
    m["selected"] = True; p.write_text(json.dumps(m, indent=1)); print("audio_v2 selected")


if __name__ == "__main__":
    cmd = args[0] if args else ""
    if cmd == "add": add([a for a in args[1:] if not a.startswith("--") and a not in (opt("--batches", ""), opt("--out", ""), opt("--intake", ""))])
    elif cmd == "build": build()
    elif cmd == "select": select()
    else: print(__doc__)

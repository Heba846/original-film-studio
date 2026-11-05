#!/usr/bin/env python3
"""Intake for the 13 expressive batches using ElevenLabs Scribe word timings (no local ASR).

  python3 tools/audio_edit/scribe_intake.py <combined audio> <offsets.json> <scribe.json> [--build]

combined audio : B01..B13 concatenated in that order with ~1 s of silence between (wav/mp3/flac)
offsets.json   : {"B01_heba": {"start": 0.0, "end": 269.087, "file": "B01_heba.mp3"}, ...}  (seconds in the combined file)
scribe.json    : the Scribe export: {"words": [{"text": "Two", "start": 0.12, "end": 0.40, "type": "word"}, ...]}
                 ("type" may also be "spacing" or "audio_event"; only "word" entries are used)

Per batch, the script tokens (from browser_audio_batches.json, never from the ASR) are matched to the Scribe words in order
(difflib). Matched tokens take Scribe's times; unmatched tokens are interpolated between their matched neighbours. Reported
per batch: match ratio, omitted runs (>=3 script tokens with no Scribe word), inserted runs (Scribe words not in the script,
e.g. a spoken audio tag such as "american accent"), and speaking rate. Writes intake_audio/aligned/B##_role.json + .wav in the
format batch_intake.py build uses; --build then cuts the parts and assembles the 111 segments in public/audio_v2/.
Captions keep the written script: only their timing comes from the audio.
"""
import json, re, subprocess, sys, hashlib, difflib
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from textnorm import spoken, norm  # noqa: E402

TAGWORDS = {"american", "accent", "tense", "hushed", "whispers", "whispering", "softly", "warmly", "firmly", "quietly", "relieved",
            "shaken", "shaky", "urgent", "guarded", "calm", "wry", "coldly", "breathless", "hesitant", "wistful", "defiant",
            "remorseful", "menacing", "intense", "low", "tearful", "hurt", "weakly", "sharp", "flat", "playful", "hopeful",
            "emotional", "steady", "anxious", "focused", "determined", "bitter", "controlled", "anger", "command", "spoken", "sad"}


def main():
    a = sys.argv[1:]
    audio, offs, scribe = Path(a[0]), json.loads(Path(a[1]).read_text()), json.loads(Path(a[2]).read_text())
    B = {b["id"]: b for b in json.loads((ROOT / "edition20/out/browser_audio_batches.json").read_text())["batches"]}
    miss = [b for b in B if b not in offs]
    if miss: sys.exit(f"offsets missing for {miss}")
    words = [w for w in scribe.get("words", []) if w.get("type", "word") == "word"]
    work = ROOT / "intake_audio/aligned"; work.mkdir(parents=True, exist_ok=True)
    report = {}
    for bid, b in B.items():
        o0, o1 = offs[bid]["start"], offs[bid]["end"]
        ws = [w for w in words if o0 - 0.05 <= (w["start"] + w["end"]) / 2 <= o1 + 0.05]
        hyp, ht = [], []
        for w in ws:
            for t in norm(spoken(w["text"])):
                hyp.append(t); ht.append((w["start"] - o0, w["end"] - o0))
        best = None
        for v in (0, 1):
            toks = [norm(spoken(p["text"], v)) for p in b["parts"]]
            ref = [t for tt in toks for t in tt]
            sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
            blocks = sm.get_matching_blocks()
            m = sum(n for _, _, n in blocks)
            if best is None or m > best[0]: best = (m, v, toks, ref, blocks)
        m, v, toks, ref, blocks = best
        times = [None] * len(ref); ins = []
        pa = pb = 0
        for ia, ib, n in blocks:
            if ib > pb: ins.append((pa, hyp[pb:ib]))
            for k in range(n): times[ia + k] = ht[ib + k]
            pa, pb = ia + n, ib + n
        # interpolate unmatched script tokens between matched neighbours
        omitted, run_ = [], []
        for i in range(len(ref)):
            if times[i] is None: run_.append(i)
            elif run_: omitted.append(run_); run_ = []
        if run_: omitted.append(run_)
        dur = o1 - o0
        for r_ in omitted:
            lo = times[r_[0] - 1][1] if r_[0] > 0 and times[r_[0] - 1] else 0.0
            hi = times[r_[-1] + 1][0] if r_[-1] + 1 < len(ref) and times[r_[-1] + 1] else dur
            step = max(0.0, hi - lo) / len(r_)
            for j, i in enumerate(r_): times[i] = (lo + j * step, lo + (j + 1) * step)
        big_om = [" ".join(ref[r_[0]:r_[-1] + 1]) for r_ in omitted if len(r_) >= 3]
        tag_ins = [" ".join(x) for _, x in ins if x and sum(t in TAGWORDS for t in x) >= max(1, len(x) // 2)]
        other_ins = [" ".join(x) for _, x in ins if x and " ".join(x) not in tag_ins and len(x) >= 3]
        wav = work / f"{bid}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{o0:.3f}", "-to", f"{o1:.3f}", "-i", str(audio), "-ac", "1", "-ar", "44100",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
        sw = [(ref[i], round(times[i][0], 3), round(times[i][1], 3)) for i in range(len(ref))]
        wpm = round(len(ref) / max(1e-6, (sw[-1][2] - sw[0][1]) / 60), 1) if sw else 0
        rec = {"bid": bid, "variant": v, "ok": True, "words": sw, "counts": [len(t) for t in toks], "score": round(m / max(1, len(ref)), 3),
               "file": offs[bid].get("file", bid), "sha256": hashlib.sha256(wav.read_bytes()).hexdigest(), "dur_s": round(dur, 3),
               "wpm": wpm, "head_decode": " ".join(hyp[:8]), "spoken_tag_suspected": bool(tag_ins),
               "scribe": {"match": round(m / max(1, len(ref)), 3), "omitted_runs": big_om, "spoken_tags": tag_ins, "inserted_runs": other_ins}}
        (work / f"{bid}.json").write_text(json.dumps(rec))
        report[bid] = {"match": rec["score"], "wpm": wpm, "dur_s": rec["dur_s"], **rec["scribe"]}
        print(f"{bid}: match {rec['score']}  {wpm} wpm  omitted {len(big_om)}  spoken tags {tag_ins}  inserted {len(other_ins)}")
    (ROOT / "edition20/out/AUDIO_SCRIBE_QA.json").write_text(json.dumps(report, indent=1))
    if "--build" in a:
        bad = [b for b, r in report.items() if r["match"] < 0.9 or r["omitted_runs"] or r["spoken_tags"]]
        if bad: sys.exit(f"NOT BUILT: check {bad} in edition20/out/AUDIO_SCRIBE_QA.json (listen; regenerate or accept)")
        subprocess.run([sys.executable, str(HERE / "batch_intake.py"), "build"], check=True)


if __name__ == "__main__":
    main()

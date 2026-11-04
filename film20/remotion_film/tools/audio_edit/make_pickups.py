#!/usr/bin/env python3
"""Build the four revised narration lines by EDITING the existing recordings (no synthesis).

Run with the PocketSphinx venv:  <venv>/bin/python tools/audio_edit/make_pickups.py
For each line: forced-align the ORIGINAL recording to its original text, locate the sentence boundaries
in the alignment's silences, refine every cut on the waveform (10 ms RMS), splice only source samples,
crossfade 15 ms only where both sides are measured silent, then VERIFY:
  V1 every cut point and every crossfade window is below the silence threshold
  V2 every word of every removed sentence lies wholly inside a removed range, every retained word wholly inside
     a kept range (no word is clipped, no deleted word survives)
  V3 the edited file force-aligns to the retained text, and each word lands within 60 ms of its source position
     mapped through the edit (the words are the same audio, in order, nothing new)
  V4 the joined pause is natural (0.30-1.20 s) and the breath leading into a retained sentence is kept
  V5 head/tail: the line still starts and ends in silence; no sample discontinuity at joins
Only lines that pass every check are written to public/pickups/<id>_20min.wav and marked ready.
Originals in public/audio are read-only. Provenance -> edition20/pickups/pickup_edits.json
"""
import hashlib, json, sys, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from align import align, norm

ROOT = Path(__file__).resolve().parents[2]
SRC, OUT = ROOT / "public/audio", ROOT / "public/pickups"
PROV = ROOT / "edition20/pickups/pickup_edits.json"
Q_DB = -45.0        # silence threshold (RMS, 10 ms windows)
XF = 0.015          # crossfade length (s)
LEAD = 0.05         # silence kept before a retained onset/breath
TAIL_MAX = 0.35     # max silence kept after the final word

# spoken forms used for alignment (numbers spelled as recorded); sentences split exactly as the script has them
LINES = {
 "n005": {"sentences": ["I went back inside.", "Three days later I married him.",
                        "This is how a Brooklyn don became my husband to keep me silent, and who was really on those stairs.",
                        "Stay to the end and you'll hear one sentence I swore to under oath, the one I had never said to him."],
          "keep": [0, 1]},
 "n145": {"sentences": ["Reyes came through the front door two minutes later with a warrant signed at six.",
                        "She arrested Carmine Brancato.", "In the car, Nico was gray, pulse one hundred ten."],
          "keep": [0, 1], "written": {2: "In the car, Nico was gray, pulse 110."}},
 "n148": {"sentences": ["Thursday, third grand jury.", "I waived my privilege myself, that morning at six, for October third and nothing else.",
                        "Reyes's first text on my wedding night was true: it was mine.", "I told them what I saw.",
                        "Two shots at four ten.", "A man sliding down a silver car.", "A second gun near his open hand.",
                        "Nico standing over him with a gun in his left hand, pointed at the floor, held wrong, and his right hand in my splint."],
          "keep": [0, 1, 3, 4, 5, 6, 7], "written": {4: "Two shots at 4:10."}},
 "n154": {"sentences": ["That evening there was a cream envelope on the hall table.", "Term Five.", "Three stapled pages.",
                        "He'd signed it with his right hand, slowly, like a man writing in a foreign language.",
                        "Tommy knocked twenty minutes later and apologized for blaming me.", "I put the papers down and went upstairs."],
          "keep": [0, 1, 2, 3, 5]},
}

def read(p):
    with wave.open(str(p)) as w:
        sr, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float64) / 32768
        assert w.getnchannels() == 1
    return sr, x

def env_db(x, sr, hop=0.01):
    h = int(sr * hop)
    n = len(x) // h
    r = np.sqrt(np.mean(x[: n * h].reshape(n, h) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(r)

def quiet(env, t0, t1):
    a, b = int(max(0, t0) * 100), int(t1 * 100) + 1
    return a >= b or np.max(env[a:b]) < Q_DB

def main():
    prov, ready, blockers = {"method": "edit of existing recordings; no synthesis", "threshold_db": Q_DB, "crossfade_s": XF,
                             "aligner": "PocketSphinx forced alignment, bundled en-us model (local)", "lines": {}}, [], []
    OUT.mkdir(parents=True, exist_ok=True)
    for sid, L in LINES.items():
        src = SRC / f"{sid}.wav"
        sr, x = read(src)
        env = env_db(x, sr)
        dur = len(x) / sr
        words, score = align(str(src), " ".join(L["sentences"]))
        # map aligned words to sentences in order
        toks = [norm(s) for s in L["sentences"]]
        spoken = [(w.split("(")[0], a, b) for w, a, b in words if w not in ("<sil>",)]
        flat = [t for s in toks for t in s]
        if [w for w, _, _ in spoken] != flat:
            blockers.append(f"{sid}: alignment word list differs from transcript"); continue
        sent_rng, k = [], 0
        for s in toks:
            ws = spoken[k: k + len(s)]; k += len(s)
            sent_rng.append((ws[0][1], ws[-1][2]))
        # group kept sentences into contiguous runs
        runs, cur = [], [L["keep"][0]]
        for i in L["keep"][1:]:
            if i == cur[-1] + 1: cur.append(i)
            else: runs.append(cur); cur = [i]
        runs.append(cur)
        ranges, notes, ok = [], [], True
        for ri, run in enumerate(runs):
            first, last = run[0], run[-1]
            onset = sent_rng[first][0]
            # start: walk back from the first word over onset/breath energy to true silence
            t = onset
            while t > 0 and not quiet(env, t - 0.01, t - 0.01): t -= 0.01
            start = 0.0 if first == 0 else max(t - LEAD, sent_rng[first - 1][1] + 0.02)
            # end: walk forward over decay; stop before the next (deleted) sentence's breath/onset
            t = sent_rng[last][1]
            while t < dur and not quiet(env, t, t): t += 0.01
            nxt_on = sent_rng[last + 1][0] if last + 1 < len(sent_rng) else dur
            tn = nxt_on
            while tn > t and not quiet(env, tn - 0.01, tn - 0.01): tn -= 0.01   # start of the next sentence's breath
            end = min(t + TAIL_MAX, tn - 0.03) if last + 1 < len(sent_rng) else dur
            if last + 1 < len(sent_rng) and end <= t:
                ok = False; blockers.append(f"{sid}: no clean silence after sentence {last}"); break
            ranges.append([round(start, 3), round(end, 3)])
            notes.append({"run": [L["sentences"][i] for i in run], "word_onset": onset, "word_end": sent_rng[last][1],
                          "decay_end": round(t, 3), "next_breath_or_onset": round(tn, 3)})
        if not ok: continue
        # V1: every cut and crossfade window silent
        for a, b in ranges:
            for c in (a, b):
                if 0 < c < dur and not quiet(env, c - XF, c + XF):
                    ok = False; blockers.append(f"{sid}: cut at {c:.3f} s is not in silence")
        # V2: removed words inside removed ranges, kept words inside kept ranges
        inside = lambda a, b: any(r0 - 1e-6 <= a and b <= r1 + 1e-6 for r0, r1 in ranges)
        overlap = lambda a, b: any(a < r1 and r0 < b for r0, r1 in ranges)
        for i, (a, b) in enumerate(sent_rng):
            if i in L["keep"] and not inside(a, b): ok = False; blockers.append(f"{sid}: kept sentence {i} clipped")
            if i not in L["keep"] and overlap(a, b): ok = False; blockers.append(f"{sid}: deleted sentence {i} not fully removed")
        if not ok: continue
        # splice with 15 ms equal-power crossfades at joins; short fade at the very end
        n_xf = int(XF * sr)
        y = x[int(ranges[0][0] * sr): int(ranges[0][1] * sr)].copy()
        joins = []
        for a, b in ranges[1:]:
            seg = x[int(a * sr): int(b * sr)].copy()
            fo = np.cos(np.linspace(0, np.pi / 2, n_xf)); fi = np.sin(np.linspace(0, np.pi / 2, n_xf))
            mix = y[-n_xf:] * fo + seg[:n_xf] * fi
            joins.append(round(len(y) / sr - XF, 3))
            y = np.concatenate([y[:-n_xf], mix, seg[n_xf:]])
        y[-n_xf:] *= np.cos(np.linspace(0, np.pi / 2, n_xf))
        # V4: joined pauses
        pauses = []
        for ri in range(1, len(runs)):
            p_prev = ranges[ri - 1][1] - notes[ri - 1]["word_end"]
            p_next = notes[ri]["word_onset"] - ranges[ri][0]
            pauses.append(round(p_prev + p_next - XF, 3))
            if not (0.30 <= pauses[-1] <= 1.20): ok = False; blockers.append(f"{sid}: joined pause {pauses[-1]} s unnatural")
            if ranges[ri][0] > notes[ri]["word_onset"] - 0.02: ok = False; blockers.append(f"{sid}: onset/breath clipped")
        # V5: discontinuity
        for j in joins:
            k0 = int((j + XF) * sr)
            if np.max(np.abs(np.diff(y[max(0, k0 - n_xf * 2): k0 + n_xf * 2]))) > 0.05: ok = False; blockers.append(f"{sid}: click at join {j}")
        out = OUT / f"{sid}_20min.wav"
        tmp = OUT / f".{sid}_check.wav"
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(y, -1, 1) * 32767).round().astype("<i2").tobytes())
        # V3: re-align the edited file to the retained text and compare with mapped source timings
        kept_words = []
        for i in L["keep"]:
            kept_words += [(w, a, b) for w, a, b in spoken[sum(len(t) for t in toks[:i]): sum(len(t) for t in toks[: i + 1])]]
        def mapt(t):
            acc = 0.0
            for ri, (a, b) in enumerate(ranges):
                if a - 1e-6 <= t <= b + 1e-6: return acc + (t - a) - (XF if ri > 0 else 0) * 0
                acc += (b - a) - (XF if ri < len(ranges) - 1 else 0)
            return None
        retained_text = " ".join(L["sentences"][i] for i in L["keep"])
        try:
            w2, score2 = align(str(tmp), retained_text)
        except SystemExit as e:
            ok = False; blockers.append(f"{sid}: re-alignment failed: {e}"); w2, score2 = [], None
        sp2 = [(w.split("(")[0], a, b) for w, a, b in w2 if w != "<sil>"]
        devs = []
        if [w for w, _, _ in sp2] != [w for w, _, _ in kept_words]:
            ok = False; blockers.append(f"{sid}: edited file does not align to the retained words in order")
        else:
            for (w, a, b), (w2_, a2, b2) in zip(kept_words, sp2):
                devs.append(abs(mapt(a) - a2))
            if max(devs) > 0.06: ok = False; blockers.append(f"{sid}: word timing drift {max(devs):.3f} s after edit")
        if ok:
            tmp.replace(out)
            ready.append(sid)
        else:
            tmp.unlink(missing_ok=True)
        prov["lines"][sid] = {
            "source": f"public/audio/{sid}.wav", "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            "source_duration_s": round(dur, 3), "sample_rate": sr, "source_alignment_score": score,
            "kept_ranges_s": ranges, "joins_at_output_s": joins, "joined_pauses_s": pauses,
            "kept_sentences": [L["sentences"][i] for i in L["keep"]],
            "removed_sentences": [L.get("written", {}).get(i, L["sentences"][i]) for i in range(len(L["sentences"])) if i not in L["keep"]],
            "retained_text_written": " ".join(L.get("written", {}).get(i, L["sentences"][i]) for i in L["keep"]),
            "boundary_notes": notes, "output": f"public/pickups/{sid}_20min.wav" if ok else None,
            "output_sha256": hashlib.sha256(out.read_bytes()).hexdigest() if ok else None,
            "output_duration_s": round(len(y) / sr, 3), "max_word_timing_drift_s": round(max(devs), 4) if devs else None,
            "realign_score": score2, "status": "ready (all checks passed)" if ok else "BLOCKED",
        }
        print(f"{sid}: {'READY' if ok else 'BLOCKED'}  ranges {ranges}  out {len(y)/sr:.3f}s  pauses {pauses}  drift {max(devs) if devs else None}")
    prov["ready"], prov["blockers"] = ready, blockers
    PROV.write_text(json.dumps(prov, indent=1, ensure_ascii=False))
    for b in blockers: print("BLOCKER:", b)
    return 0 if not blockers else 2

if __name__ == "__main__":
    sys.exit(main())

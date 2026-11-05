#!/usr/bin/env python3
"""edition20/out/browser_audio_batches.json: the exact 111-segment script split into browser-TTS batches (<=4500 chars) grouped by
voice role. Narration stays with its segment speaker (heba = Ivy, lion = Nico); quoted lines go to another character only where
the attribution is unambiguous (QUOTE_MAP). Words are never changed: every part is a verbatim slice text[start_char:end_char]."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
T = json.loads((R / "src/film/data/film_timeline.json").read_text())
SEG = {s["id"]: s for s in T["segments"]}
# (segment, nth quote in that segment) -> role; evidence is the attribution in the sentence itself or the line before it
QUOTE_MAP = {
 ("n036", 0): ("theo", "'Ivy,' Theo said"), ("n036", 1): ("theo", "continues Theo's line"),
 ("n053", 0): ("rocco", "reply to 'Go after him' by Rocco, the only man in the doorway"),
 ("n079", 0): ("sal", "'Sal said'"), ("n079", 1): ("sal", "continues Sal's line"),
 ("n081", 0): ("sal", "Sal holds up both hands, cannoli in one"),
 ("n085", 0): ("nico", "'he said' = Nico (his grandmother Rosa)"), ("n085", 1): ("nico", "continues Nico's line"),
 ("n092", 0): ("joey", "'he asked' = Joey, the patient"),
 ("n097", 1): ("nico", "'Sleep,' he said = Nico"), ("n097", 2): ("nico", "continues Nico's line"),
 ("n102", 0): ("enzo", "Enzo grabbed my sleeve and told me"),
 ("n109", 0): ("nico", "'Nico, in the car, never raised his voice'"),
 ("n116", 0): ("nico", "'At my door he said' = Nico"),
 ("n119", 0): ("holloway", "'Holloway had asked me'"),
 ("n125", 0): ("sal", "'Sal didn't blink ... he said'"), ("n125", 1): ("sal", "continues Sal's line"),
 ("n126", 0): ("sal", "Sal continues ('he said')"), ("n126", 1): ("sal", "continues Sal's line"),
 ("n129", 0): ("sal", "'Sal looked at his hands'"), ("n130", 0): ("sal", "'Sal almost smiled'"),
 ("n136", 0): ("theo", "'Theo walked out ... In the car he said'"),
 ("n142", 0): ("enzo", "'Enzo wouldn't sign it'"),
 ("n144", 1): ("brancato", "'I told Brancato ... He said'"),
 ("n159", 0): ("lucia", "'Lucia said'"), ("n159", 1): ("lucia", "continues Lucia's line"), ("n159", 2): ("nico", "'Nico said'"),
}
KEPT_WITH_NARRATOR = {  # quotes deliberately left in the narrator's voice (Ivy's own lines, or not clearly attributable)
 "Ivy's own spoken lines": "n010 n013 n015 n020 n026 n035 n039 n041 n046 n052 n055 n059 n061 n063 n065 n092#1 n097#0 n115 n124 n127 n144#0 n150 n155",
 "ambiguous / not voiced": "n098 (Bell's written phone note, read by Ivy) · n110 ('destroyed' is a scare quote) · "
                           "n113 and n149 (the questioner is not named on the line)"}
ROLE_OF_SPEAKER = {"heba": "heba", "lion": "nico"}
parts = []  # (role, segment_id, start, end)
for s in T["segments"]:
    t, sid = s["text"], s["id"]
    cuts = []
    for k, m in enumerate(re.finditer(r'"([^"]+)"', t)):
        if (sid, k) in QUOTE_MAP: cuts.append((m.start(), m.end(), m.start(1), m.end(1), QUOTE_MAP[(sid, k)][0]))
    pos = 0
    def narr(a, b):
        seg = t[a:b]; l = len(seg) - len(seg.lstrip(' "')); r = len(seg.rstrip(' "'))
        if re.search(r"\w", seg[l:r]): parts.append((ROLE_OF_SPEAKER[s["speaker"]], sid, a + l, a + r))
    for qa, qb, ia, ib, role in cuts:
        narr(pos, qa); parts.append((role, sid, ia, ib)); pos = qb
    narr(pos, len(t))
# group by role in film order, <=4500 chars per batch (parts joined by a blank line)
order = ["heba", "nico", "sal", "theo", "enzo", "rocco", "joey", "holloway", "brancato", "lucia"]
batches = []
for role in order:
    cur, n = [], 0
    for r_, sid, a, b in parts:
        if r_ != role: continue
        txt = SEG[sid]["text"][a:b]
        if cur and n + 2 + len(txt) > 4500:
            batches.append((role, cur)); cur, n = [], 0
        cur.append((sid, a, b, txt)); n += len(txt) + (2 if len(cur) > 1 else 0)
    if cur: batches.append((role, cur))
out_b = []
for i, (role, ps) in enumerate(batches, 1):
    text = "\n\n".join(p[3] for p in ps)
    assert len(text) <= 4500
    out_b.append({"id": f"B{i:02d}_{role}", "voice_role": role, "chars": len(text), "text": text,
                  "parts": [{"segment_id": sid, "start_char": a, "end_char": b, "text": txt} for sid, a, b, txt in ps]})
# verification: every word of every segment is covered exactly once
for s in T["segments"]:
    cov = sorted((a, b) for r_, sid, a, b in parts if sid == s["id"])
    for (a1, b1), (a2, b2) in zip(cov, cov[1:]): assert b1 <= a2, s["id"]
    rest = list(s["text"])
    for a, b in cov:
        for i in range(a, b): rest[i] = " "
    assert not re.search(r"[A-Za-z0-9]", "".join(rest)), (s["id"], "".join(rest))
sample_src = next(s for s in T["segments"] if s["speaker"] == "heba" and 150 <= len(s["text"]) <= 180 and '"' not in s["text"])
out = {"about": "Browser TTS batches. Generate each batch as ONE audio file named <id>.mp3/.wav with the voice for its role. "
                "Parts are separated by a blank line in 'text'; offline alignment splits each file back into segment parts by these exact texts.",
       "rules": ["text is verbatim: never edit, add or drop words", "one file per batch, named exactly by id",
                 "same voice and settings for every batch of a role", "roles other than heba/nico are short; they may be merged by the author into one voice per role"],
       "voice_roles": {"heba": "Ivy narration and Ivy's own dialogue - the genuine cloned 'heba' voice (NOT the designed 'heba eng')",
                       "nico": "Nico (segments labelled lion + his quoted lines)", "sal": "Sal, 70s uncle", "theo": "Theo, early 20s",
                       "enzo": "Enzo, 21", "rocco": "Rocco, huge, quiet", "joey": "Joey, young soldier", "holloway": "Holloway, prosecutor",
                       "brancato": "Brancato, 60s rival", "lucia": "Lucia, 60s"},
       "quote_attribution": {f"{k[0]}#{k[1]}": {"role": v[0], "evidence": v[1]} for k, v in QUOTE_MAP.items()},
       "quotes_kept_with_narrator": KEPT_WITH_NARRATOR,
       "ivy_sample_180": {"segment_id": sample_src["id"], "chars": len(sample_src["text"]), "text": sample_src["text"]},
       "totals": {r: sum(b["chars"] for b in out_b if b["voice_role"] == r) for r in order},
       "batch_count": len(out_b), "batches": out_b}
p = R / "edition20/out/browser_audio_batches.json"
p.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(out_b), "batches", out["totals"], "sample", out["ivy_sample_180"]["segment_id"], out["ivy_sample_180"]["chars"])

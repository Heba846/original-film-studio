# Full-film adaptation package - *Married to the Don to Keep Me Silent*

A complete narrated, illustrated film (one story, one ending) adapted from the author's novel. Two voices: **Heba** = Ivy first-person narrator and every non-Nico speaker (quoted); **Lion** = Nico's dialogue and Nico-POV narration (CH06 "The Code", CH09's garage flashback, CH12 "The Glove Box", the bolt scene, the visiting room). Satisfying romantic ending; the optional book line is the last 54 words and the film is complete without it. No cliffhanger paywall.

## Status (exact)
| Item | Status |
|---|---|
| Canon ledger + continuity audit with page refs | **Done** (`canon_ledger.md`), from a full read of all 340 pages |
| Full production script, 162 voice segments, 62 shots | **Done** (`script.md`, source of truth) |
| Spoken-word count | **Computed by code**: 4885 words incl. 54 optional CTA (`word_count.json`) |
| Runtime | **ESTIMATE only**: 36.3 min at 140 wpm, 34.0 at 150, 31.9 at 160 (words + scripted pauses). **Nothing has been recorded or timed.** |
| Segments CSV/JSON | **Done** (`segments.csv`, `segments.json`) |
| Shot plan + still / optional-motion prompts | **Done** (`shot_prompts.md|csv|json`, painterly illustrated realism, consistent continuity locks) |
| Loadable toolkit project | **Done** (`projects/married_to_the_don_full_film`); validates with exactly two error kinds: missing images and missing narration audio |
| Real narration (Heba, Lion) | **NOT AVAILABLE** - no recordings exist; no voices were generated or cloned |
| Illustrations | **NOT AVAILABLE** - 62 image slots are empty; no images were generated |
| Rendered film | **NOT RENDERED** (needs the two items above). Only tone-based synthetic assembly was tested |
| Market brief | **BLOCKED** (YouTube unreachable); no market data recorded (`market_brief.md`) |
| YouTube policy statements | **Unverified** (official pages unreachable); the loaded skills' notes are marked as such |

## Files
`script.md` (edit this) -> `python -m ofs adapt build` regenerates `segments.*`, `word_count.json`, `shot_prompts.*` and the project. `canon_ledger.md`, `packaging.md`, `market_brief.md`, this README.

## How it follows the brief
- **Opening times:** ER 3:05, stitches 3:20, splint ~3:40, shots 4:10 (splint built **thirty** minutes before the shots).
- **Hearing vs seeing:** Ivy hears two shots and sees the aftermath; she never says she saw anyone fire. Enzo fired; Nico took the gun with his left hand. The injured right hand is never used as proof Nico could not shoot left-handed.
- **Canon kept:** the evidence chain (Lot 4471-B, Bell's co-signed form, anise, the eleven-page deduction, deli receipt and gum), motives (Sal, Brancato, Bell, Enzo, Nico), Ivy's two oaths, her waiver of privilege, Nico's gun confession, the refused divorce, "She does." and "Term six.", and the closed-door HEA.
- **Ring:** Nonna Rosa's emerald is on a thin gold chain at Ivy's neck at work (not a generic pendant); on her finger at home/court; plain gold band under it from Nov 5.
- **Reference art:** Ivy red messy bun with pen, freckles, navy scrubs; Nico dark wavy hair, stubble, scar LEFT eyebrow.

## Craft pass (skills, all seven installed and loaded; applied as checklists)
`story-engine` / `story-retention-psychology`: cold open states the title's scene; a named question stays open; plants and payoffs in `canon_ledger.md` section 3; a place/voice/time change at each chapter (Lion POV chapters are the voice changes); the last three chapters are among the longest. `attention-copy` + `youtube-brand-strategy`: `packaging.md`. `criticism-and-analyzing`: market teardown was **not possible** (no access); only its honesty rules were applied. `novel-human-pass` (review mode on the script): slop vocabulary hits 0; one em dash pair; short-sentence ratio 30% (human band per its rules); **gifts from outside** (Enzo's confession, Bianca's video, Bell's letter, Paulie's arrest, Brancato's call) are canon, but the leads still earn the key turns: the lot trace, the eleven-page deduction, the anise twist, the receipt-and-gum chain, calling Reyes first. `heba-proofreading`: the adapter keeps plain-named feelings, behavior over metaphor, dry humor and the counting motif; **the five or six lines that matter most should be re-voiced by Heba before recording** (suggested: "Go back inside, Dr. Marlowe."; "Yes. I love him..."; "It's my uncle."; "I'm not armed, Carmine."; "She does."; the last paragraph).

The first-30-seconds, minute 3-7 and re-hook cadences are creator rules of thumb, **not guarantees**. By the script's own estimate (150 wpm + pauses) the garage, gun, left hand and splint are on screen by ~38 s and "Go back inside, Dr. Marlowe" lands at ~43 s.

## Length: why it is above the 4,500 cap and how to cut
4885 words (4,831 without the CTA) is ~7% over the soft cap. Justification: the novel has three crossing mysteries (who fired, who leaks, who supplies the pills) plus a marriage arc; cutting further removes planted clues or the climax's room. To reach ~4,500: drop the pharmacy paragraph in CH10 (-60), the Theo-in-the-car exchange in CH14 (-70), the epilogue fates except Enzo (-70), the Bell confrontation detail in CH08 (-60), the Aldo/Paulie summary in CH14 (-50), and the CTA (-54).

| Chapter | Title | Spoken words |
|---|---|---|
| CH00 | Two Shots | 151 |
| CH01 | 3:05 | 309 |
| CH02 | 4:10 | 251 |
| CH03 | What I Saw, And What I Didn't | 197 |
| CH04 | Two Ways This Ends | 352 |
| CH05 | Terms | 233 |
| CH06 | The Code (Nico) | 281 |
| CH07 | I Do | 289 |
| CH08 | Leak | 407 |
| CH09 | Enzo | 295 |
| CH10 | Lot 4471-B | 129 |
| CH11 | Yes | 210 |
| CH12 | The Glove Box (Nico) | 253 |
| CH13 | Uncle | 191 |
| CH14 | Lemon Trees | 207 |
| CH15 | The Kitchen Island | 173 |
| CH16 | Bath Avenue | 226 |
| CH17 | The Second Oath | 259 |
| CH18 | Term Six | 225 |
| CH19 | April | 247 |

### Estimated chapter markers (recompute after recording; 150 wpm + pauses)
- 0:00 Two Shots
- 1:05 3:05
- 3:15 4:10
- 4:59 What I Saw, And What I Didn't
- 6:21 Two Ways This Ends
- 8:50 Terms
- 10:30 The Code (Nico)
- 12:27 I Do
- 14:27 Leak
- 17:15 Enzo
- 19:17 Lot 4471-B
- 20:11 Yes
- 21:39 The Glove Box (Nico)
- 23:24 Uncle
- 24:44 Lemon Trees
- 26:09 The Kitchen Island
- 27:21 Bath Avenue
- 28:54 The Second Oath
- 30:42 Term Six
- 32:15 April

## Pilot corrected from canon
`python -m ofs pilot --force` rebuilds the pilot: "forty minutes" -> **thirty** (splint) / **fifty** (patient first seen); "Dottoressa" -> **"Dr. Marlowe"** in the garage line [p.11]; garage **4:10 a.m.** not 3 a.m.; Ivy is a **resident**; "the witness he couldn't afford to leave behind" replaced (Nico is not the threat; someone on the stairs was listening [p.13]); ring/chain continuity, 34-year-old Nico, wavy hair and stubble from the reference art, painterly style. Original pilot wording is kept in each segment's `original_text`; the owner's original closing sentence was never supplied (only the phrase "I had just married into a family"), so it is still a placeholder.

## Production steps and blockers
1. **Record or generate narration** per segment (Heba / Lion) as WAV, import into the Narration tab (or optional local Chatterbox with consented reference clips; **untested**, see `docs/CHATTERBOX.md`).
2. `python -m ofs narration sync married_to_the_don_full_film` -> real durations replace the estimates.
3. **Make 62 illustrations** from `shot_prompts.md` in an external tool you choose; save as `media/film/sNN.png` (supplied-asset animatic; no motion is generated here).
4. Optional: music, SRT captions. 5. `python -m ofs validate ...` then render.
**Blockers:** (a) no voice recordings or reference clips; (b) no illustrations; (c) full-film render untested end-to-end at real scale (tone assembly of all 162 segments is tested; a 62-shot 1080p render is not); (d) no market/policy verification; (e) the owner's original closing sentence for the pilot; (f) re-voicing key lines; (g) confirm the book link/availability before using the CTA.

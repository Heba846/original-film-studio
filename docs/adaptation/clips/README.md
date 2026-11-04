# Clip production list: Married to the Don to Keep Me Silent

Production list for the real-motion clips (Google Flow, Veo 3.1 Lite, 8 s silent clips, 10 credits each). It adds files only; `script.md`, `shot_prompts.*` and the code are untouched.

| File | Content |
|---|---|
| `clips.csv` | One row per clip: id, shot, start offset in the shot, status, credits, narration cue, references to attach, Flow prompt (with character count), negative prompt, cut-in and cut-out pose, bridge note, risk |
| `clips.md` | The same data as pasteable blocks, in film order, with the timing/bridge note per shot |

## What was planned
- 73 clip rows in 31 shots: **71 to generate** and **2 reused approved clips** (`s03_c1` "Man turning head in garage" and `s07_c1` the hospital bandage clip; I did not see either file, so check their content against the notes before cutting; `s07_c1` may be shorter than 8 s).
- The other 31 shots stay painted stills with light camera movement (listed at the bottom).
- Every prompt is 900 characters or fewer (longest: see `prompt_chars`), plain English, silent, no dialogue and no mouth animation, camera locked off (the one slow tilt is `s02_c1`).

### Changes to the starting allocation
The starting allocation was kept for all 28 shots (s07's two clips = 1 reused + 1 new). Added 3 new clips from the spare pool:
- **s21 +1:** Nico's failed fist in the plaster is the setup for the s56 payoff, and finger movement is exactly what a still cannot show.
- **s56 +2:** removing the splint and the fist closing, "even the ring finger I sewed", is the payoff of the whole splint thread.
Net effect: planned new clips went from 68 to 71, still inside the budget with 34 clips of reserve.

## Cost table (10 credits per clip, 1,050 credits available)
| Item | Clips | Credits |
|---|---|---|
| New clips (first attempt) | 71 | 710 |
| Reused approved clips | 2 | 0 |
| **Planned spend** | 71 | **710** |
| Reserve left | 34 clips | 340 |

Retry reserve scenarios (attempts per kept clip): 1.0x = 710; 1.3x = 923 (leaves 127); 1.4x = 994 (leaves 56); 1.5x = 1065 (over budget by 15).
Plan for about 1.3x. Hand-heavy clips will burn most of the retries (see Risk column; the worst are `s27_c1`, `s27_c2`, `s21_c1`, `s50_c3`, `s56_c2`, `s02_c2`, `s37_c3`). If the first 15 clips come back at under 70% usable, drop in this order before spending more: `s34_c2`, `s54_c2`, `s55_c2`, `s36_c2`, `s60_c2`, `s49_c2`, `s44_c2`, `s11_c1`. These are the clips whose gaps a still bridges most easily.
Costs not counted here: the shot keyframe stills (see "Attach" below), and any image credits Flow charges for them.

## Per-shot coverage
The 62 shots in `shot_prompts.json` add up to 32.6 min of narration time; the clips cover the key physical beats, not all of it.

| Shot | Chapter | Narration s | Clip rows | Reused | New | Credits | Clip seconds / narration |
|---|---|---|---|---|---|---|---|
| s01 | CH00 | 12.92 | 2 | 0 | 2 | 20 | 100% |
| s02 | CH00 | 23.49 | 3 | 0 | 3 | 30 | 100% |
| s03 | CH00 | 5.26 | 1 | 1 | 0 | 0 | 100% |
| s04 | CH00 | 21.0 | 2 | 0 | 2 | 20 | 76% |
| s07 | CH01 | 40.07 | 2 | 1 | 1 | 10 | 40% |
| s09 | CH02 | 17.91 | 2 | 0 | 2 | 20 | 89% |
| s10 | CH02 | 27.74 | 2 | 0 | 2 | 20 | 58% |
| s11 | CH02 | 25.8 | 2 | 0 | 2 | 20 | 62% |
| s16 | CH04 | 30.21 | 3 | 0 | 3 | 30 | 79% |
| s20 | CH05 | 37.41 | 2 | 0 | 2 | 20 | 43% |
| s21 | CH06 | 23.58 | 1 | 0 | 1 | 10 | 34% | added
| s25 | CH07 | 23.09 | 2 | 0 | 2 | 20 | 69% |
| s27 | CH07 | 30.73 | 3 | 0 | 3 | 30 | 78% |
| s33 | CH08 | 19.26 | 2 | 0 | 2 | 20 | 83% |
| s34 | CH08 | 47.19 | 2 | 0 | 2 | 20 | 34% |
| s36 | CH09 | 45.35 | 2 | 0 | 2 | 20 | 35% |
| s37 | CH09 | 49.81 | 3 | 0 | 3 | 30 | 48% |
| s43 | CH12 | 62.4 | 4 | 0 | 4 | 40 | 51% |
| s44 | CH12 | 37.34 | 2 | 0 | 2 | 20 | 43% |
| s46 | CH13 | 38.64 | 2 | 0 | 2 | 20 | 41% |
| s49 | CH15 | 43.61 | 2 | 0 | 2 | 20 | 37% |
| s50 | CH15 | 24.08 | 3 | 0 | 3 | 30 | 100% |
| s53 | CH16 | 44.89 | 4 | 0 | 4 | 40 | 71% |
| s54 | CH17 | 31.0 | 2 | 0 | 2 | 20 | 52% |
| s55 | CH17 | 38.61 | 2 | 0 | 2 | 20 | 41% |
| s56 | CH17 | 33.72 | 2 | 0 | 2 | 20 | 47% | added
| s57 | CH18 | 19.73 | 2 | 0 | 2 | 20 | 81% |
| s58 | CH18 | 28.19 | 3 | 0 | 3 | 30 | 85% |
| s59 | CH18 | 41.91 | 2 | 0 | 2 | 20 | 38% |
| s60 | CH19 | 40.5 | 3 | 0 | 3 | 30 | 59% |
| s62 | CH19 | 43.77 | 4 | 0 | 4 | 40 | 73% |

A coverage under 100% means the rest of the shot is a painted still or a cutaway; each shot's bridge note in `clips.md` says which. Over 100% means trim the clip tail. Never freeze a clip longer than about 2 s and never loop a clip; that is the slideshow look the requirement file forbids.

**Painted stills with light camera movement (no clip):** s05, s06, s08, s12, s13, s14, s15, s17, s18, s19, s22, s23, s24, s26, s28, s29, s30, s31, s32, s35, s38, s39, s40, s41, s42, s45, s47, s48, s51, s52, s61.

## Ordering and cutting
- Clips are in film order. Within one shot, `cut_in_pose` of clip n+1 equals `cut_out_pose` of clip n, and consecutive clips use a different framing (wide, medium, close or insert), so the cut hides small face drift: match-on-action, not a dissolve.
- If Flow lets you use the last frame of the previous clip as the start frame, use it for clips 2+ (noted in "Attach"). If it does not, the shot keyframe is the start frame and the cut-in pose is only an editing guide.
- Cutaways and stills fill the narration gaps: see the bridge note on the last clip of each shot. The two cuts between shots that matter most: `s02_c3` ends on Nico's eyes meeting the lens, which hands off to the reused s03 clip; `s53_c4` leaves the club for the black car and needs the s51 car keyframe.
- Shots listed in the allocation but with long narration (s43 62 s with 4 clips, s34 47 s with 2, s62 44 s with 4) will have the longest still bridges. Do not stretch clips to fill them.

## Attach (references)
The repository contains no image files, so references are named by slot, not by file:
- `REF-IVY (approved face)` and `REF-NICO (approved face)`: the approved reference faces (Ivy red messy bun with a pen, freckles, navy scrubs; Nico dark wavy hair, stubble, gray eyes, thin white scar through the LEFT eyebrow).
- `KF sNN`: the painted keyframe still of that shot (`media/film/sNN.png` in the toolkit's naming). It must exist and be approved before its clips run, and it is the start frame. Supporting faces (Lucia, Sal, Enzo, Priya, Theo, Danny, Brancato, Reyes, Holloway) have no standalone approved reference in what I read, so their identity comes from the keyframe: approve those keyframes first.

## Continuity locks used in the prompts
- **Splint:** white plaster on the RIGHT forearm Oct 3-10 (s01-s27); black thermoplastic with three velcro straps and a small white cross on the wrist strap from Oct 10 until it is removed in s56 (s33, s43, s46, s49, s50, s53, s54). No splint in s57-s62. Prompts name the side and colour in the prompt and in the negative prompt.
- **Gun:** LEFT hand only (s01, s02, s10, s37_c3).
- **Ivy's ring and chain** (from `canon_ledger.md`): no ring, chain or necklace Oct 3-5 (s01-s20); emerald ring on the LEFT finger from the wedding (s27 onward), too loose; at work (s34, s36) a thin gold chain under the scrub top, ring not visible; emerald over a thin plain gold band on the LEFT finger from Nov 5 (s49, s50, s53, s55, s57-s62). In gloved scenes (s49, s56) the gloves cover the hands and the negative prompt bans rings over gloves. After Nov 5 she wears the ring on her finger in the ER shot s56 (the ledger's adaptation choice).
- **No invented jewelry:** every negative prompt lists the jewelry that must not appear. Nico wears nothing on his hands in the prompts (see open items).

## Things I found and how I handled them (please confirm)
1. **Boilerplate ring note in the shots:** several shot continuity notes (among the clipped shots: s44, s53, s55, s57) carry the sentence "Fri Oct 3-Sun Oct 5 ... NO ring, NO chain" even where the date is later. I followed the ledger chronology instead (ring on finger off duty, band after Nov 5). If you meant those shots to be ringless, edit the `jew`-related wording in the prompt.
2. **s33 splint:** the shot note does not name the splint; the ledger puts s33 (Oct 16) after the swap to black, so the prompt says black.
3. **Nico "plain gold band on his LEFT hand":** the Nico note in `shot_prompts.json` says this. The ledger and script never mention it, and the project rule is no invented jewelry, so I left Nico's hands bare. Say so if the band is real and I will add it.
4. **Shot location labels that do not match the narration:** s43 is labeled the hospital garage but the narration is Sal's private garage (I used a dim private garage with the Lincoln); s55 is labeled Courtroom 6B but the shot is a grand jury room; s57 is labeled the study but the action is the hall table.
5. **Outfits not defined in the sources:** Ivy's clothes in s16 follow the keyframe, not the prompt.
6. **Gun safety:** no shot of anyone firing and no visible wounds or blood anywhere (s37 stops before the shots; s49 shows gauze and drapes only). If Flow's filter rejects a gun clip, lower the gun to a held-at-thigh pose and say so in the prompt.
7. **Narration vs. mouth:** a few scenes are dialogue-heavy (s16, s20, s46, s53, s59). The prompts use head turns, eyes and hands, with the mouths closed; voices are added later.

## Review checklist (every generated clip)
1. **Hand anatomy:** five fingers per hand, no fused or extra fingers, no melting during grips (wrist, sleeve, pen, ring, bolt, tie). Scrub frame-by-frame at hands.
2. **Face drift:** compare the first and last frames with the approved reference: Ivy's freckles, red bun and pen; Nico's gray eyes, stubble and **scar through the LEFT eyebrow** (reject mirrored scar).
3. **Splint on the RIGHT arm:** correct side, correct colour for the date (white plaster before Oct 10, black with three straps and the small white cross after), none after s56.
4. **Gun hand:** LEFT hand only. The gun never rises toward anyone in any clip.
5. **Ring/chain rules:** per the table above: nothing before the wedding; ring on the LEFT finger; chain only at work, ring hidden; band under the emerald only from Nov 5.
6. **No invented jewelry:** no earrings, bracelets, extra rings, pendants or watches that are not in the table (Lucia's gold cross is the only neck item allowed).
7. **Motion:** the character moves (not only the camera); no zoom pop, no push-in, no morph; the action ends in the written end pose so the next cut matches.
8. **Mouths and text:** mouths closed or relaxed (no lip movement), no legible text on papers, phones or signs.
9. **Non-graphic:** no blood, wounds or corpse close-ups.
10. **Technical:** 8 s, 16:9, painterly texture, no flicker or color flash at the loop point.
Mark each clip OK / REDO in the spare column you add to `clips.csv`; log the number of attempts so the reserve can be re-estimated after the first 15 clips.

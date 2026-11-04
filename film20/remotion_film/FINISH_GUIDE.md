# Film20 — finish guide (source + media bundle)

Narration is final: 111 segments, measured **20:46.03** (29,905 frames @ 24 fps). Script text and voices are unchanged except for the 4 sentence-deletion edits (byte-reproducible; see `edition20/pickups/pickup_edits.json`).
The final export is **blocked** until every planned shot is approved footage (the gate is unchanged).

## Setup (Node 18+, Python 3, ffmpeg)
```
npm ci
python3 tools/film_build.py        # re-measures audio, rebuilds the timeline + edition20/out/STATUS.md
python3 tools/test_film.py         # 16 tests
npx remotion studio src/index.tsx  # Film20-Workbench = full film with placeholders/approved stills + HUD
```

## Where things are
| What | Path |
|---|---|
| Narration WAVs (original, per segment) | `public/audio/n###.wav`, plus `public/n001.wav`, `public/n002.wav`, `public/n004.wav` |
| 4 edited lines / their originals | `public/pickups/*_20min.wav` / `edition20/originals/` |
| Narration master (whole film, timeline-placed) | `output/full/Film20_NARRATION_MASTER_20m46s.flac` (sha256 of the 48 kHz WAV it was encoded from: 975c44f0…; segments placed exactly at their timeline frames, peak −2.7 dBFS) |
| Captions (word-aligned) / chapters | `edition20/out/Film20_captions_DRAFT.srt` (renamed `Film20_captions.srt` once the gate opens), `Film20_chapters.txt` |
| Approved clips (10) | `public/flow/F01,F04,F06,F07,F09–F13.mp4` + `public/hospital.mp4` |
| Approved stills (first frames, 19) | `public/stills/STILL_F##.jpg` (= `edition20/stills_approved/`) |
| Remaining jobs: prompts, still verdict, repair prompt, needed source ranges | `edition20/REMAINING_JOBS.json` |
| Still QA (approved / author call / 37 repairs) | `edition20/review/still_qa.json` |
| Media inventory with hashes and durations | `edition20/out/MEDIA_INVENTORY.json` |
| Budget ledger | `edition20/budget_ledger.json` |

## Adding a finished clip
1. Name it `F##.mp4` (retake: `F##_R1.mp4`). Run `python3 tools/flow_intake.py ingest F##.mp4`. This builds the review sheet and the identity sheet at 4 fps.
2. Check identity, arm, location and costume, then `python3 tools/flow_intake.py approve F## --range a b --identity "..."`. Identity is required; mirroring is never a fix.
3. Run `python3 tools/film_build.py`. The cut lists re-plan automatically.

## Final render (only when STATUS shows export allowed: YES)
`bash tools/final_render.sh` writes `output/final/Film20_Final_720p.mp4` + captions/chapters. Without approved footage for every planned shot it prints BLOCKED and renders nothing.

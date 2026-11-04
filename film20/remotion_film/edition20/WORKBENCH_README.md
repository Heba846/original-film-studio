# Film20 workbench (plan v2) — how this edition is built

Current cut: *Married to the Don to Keep Me Silent*, twenty-minute narrated edition (edition20).
`Opening` (16 s legacy test) is untouched and still renders. Nothing here is a finished film.

## What is real vs. planned (from `out/STATUS.md`)

| Thing | State |
|---|---|
| 107 retained narration WAVs | Real, measured, natural speed |
| 4 pickups (n005, n145, n148, n154) | **Not recorded.** Slots held at EDL estimates; old words never used |
| hospital.mp4 | Approved (Bay 14). 18.6 s on screen across 3 motivated uses |
| garage.mp4, nico.mp4 | **Rejected** for this cut (audit in `media_manifest.json`); still inside `Opening` |
| Code scenes (19 components, beats per narration) | Finished: 380 s (30.6%) |
| 70 Flow jobs | **Planned, not generated.** 527.6 s first use + 317.3 s motivated reuse, *conditional on delivery and approval* |
| Unresolved / unplanned picture | **0.0 s** |
| Runtime | 20:43.78 **estimate** until the pickups exist |
| Final master | **Blocked** (`Film20-Final` throws on frame 0) |

## v2 changes
- Explicit timed cut lists per segment (`segment_cuts`): every cut names a source, in-point, speed and length.
  `tools/film_build.py` resolves them against exact windows (delivered files are measured; planned files use the
  0.20-7.70 s estimate of an ~7.9 s result), enforces 0.85x minimum, counts dissolve overlap as source use, tiles the
  whole film with no gaps, and reports anything it cannot cover as UNRESOLVED.
- Reuse rules enforced: reason required; >3 uses per asset needs a flag; decisive actions only return as memory;
  another date's footage only as memory; the Bay 14 frames where Ivy's lips part never return.
- Hard cuts inside continuous scenes; dissolves only into/out of code scenes and memories; chapters open from black.
- Opening respecified (wardrobe-locked): `aftermath_wide`, `frankie_hand`, `nico_hands`, `nico_ots` (over Ivy's
  shoulder), `ivy_reaction` (listener on 'You were never here.', cut placed at the measured sentence break, 2.00 s).
- U01 (Theo's arrest) = `CODE_ARREST`, a non-photoreal transition from script facts. No 71st job.
- Jobs rebalanced 35 / 35 between the first and second halves (v1: 39 / 31).

## Files

| Path | Role |
|---|---|
| `tools/make_manifest.py` | Authoring source for jobs + cut lists (re-run with `--force`) |
| `edition20/media_manifest.json` | Generated: shots + `segment_cuts` |
| `edition20/flow_jobs.json` | Generated: 70 jobs (Batch 1 full prompts, 2-4 intent + continuity lock) |
| `edition20/FLOW_JOBS_NEXT.md` | Generated: paste-ready sheet with each job's placements |
| `edition20/budget_ledger.json` | Ledger (0 spent); `tools/validate_budget.py` cross-checks the manifest |
| `edition20/out/STATUS.md` | Coverage a/b/c, reuse ledger, review flags, gate |
| `edition20/out/COVERAGE_BEFORE_AFTER.md` | All 38 v1 shortfall blocks + U01, before vs after |
| `tools/test_film.py` | 13 tests incl. gate simulation with fake media in a scratch copy |

## Loop

```bash
python3 tools/make_manifest.py --force   # after editing jobs/cut lists
python3 tools/film_build.py              # after any media, pickup or manifest change
python3 tools/flow_sheet.py
python3 tools/validate_budget.py
python3 tools/test_film.py --render      # add --render to prove Final refuses to export
npx tsc -p .
```

Compositions: `Film20-Workbench`, `Film20-Editor-CH00` (editor preview of the corrected opening — placeholders,
not a finished scene), `Film20-Test-CH01`, `Evidence-Gallery` (every evidence beat in the sample segments at its
real length), `Film20-Final` (blocked), `Opening` (unchanged).

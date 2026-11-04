# Film20 production review backup (draft branch: not merged, not deployed)

Code and records for the twenty-minute narrated edition of *Married to the Don to Keep Me Silent*.
This is a backup of the cloud workbench. It is **not a finished film**.

Included: Remotion source (`remotion_film/src`, incl. generated timelines in `src/film/data`), build/validation/review tools
(`remotion_film/tools`), revised script and EDL plus the author's originals (`edition20/`, `edition20/originals/`), media
manifest and cut lists, 70 Flow prompts (`edition20/FULL70_FLOW_PROMPTS.json` and as-sent copies in `edition20/out/`),
narration edit provenance (`edition20/pickups/pickup_edits.json`), word alignment (`edition20/out/word_alignment.json`),
budget ledger (`edition20/budget_ledger.json`), review verdicts and sheets (`edition20/review/`), reference stills
(`edition20/flow_refs/`), status reports (`edition20/out/`).

Not included (media; kept in the checkpoint zip): narration WAVs (`public/audio`, `public/pickups`), Flow MP4s (`public/flow`),
source clips and renders. The four edited narration lines are reproducible byte-exact from the original WAVs with
`tools/audio_edit/make_pickups.py` (input/output hashes are in pickup_edits.json).

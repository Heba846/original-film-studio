# Narration pickups — RESOLVED without new recording

All four revised lines were produced by deleting sentences from the existing recordings (no TTS, no new
narration). Exact source ranges, retained/removed text, cut-point measurements and verification results:
`edition20/pickups/pickup_edits.json` (built by `tools/audio_edit/make_pickups.py`).

| Line | Kept source ranges (s) | Removed | Output |
|---|---|---|---|
| n005 | 0.00-3.82 | the two trailer-style sentences | 3.82 s |
| n145 | 0.00-6.93 | "In the car, Nico was gray, pulse 110." (keeps "with a warrant signed at six") | 6.93 s |
| n148 | 0.00-8.08 + 11.64-26.19 | "Reyes's first text on my wedding night was true: it was mine." | 22.62 s (join pause 0.375 s) |
| n154 | 0.00-12.06 + 15.91-18.31 | "Tommy knocked twenty minutes later and apologized for blaming me." | 14.45 s (join pause 0.385 s) |

Checks passed for every line: all cuts and the 15 ms crossfades sit in measured silence (< -45 dB RMS); every
deleted word lies wholly inside a removed range and every kept word wholly inside a kept range; the edited file
re-aligns to the retained text with every word within 20 ms of its source position; joined pauses match the
originals' natural pauses (0.37-0.38 s); breaths leading into retained sentences are kept; an unconstrained
recognition pass hears the deleted words in the originals and none of them in the edits. Originals in
public/audio are unchanged (hashes recorded). The script and EDL now carry the exact retained wording
(originals backed up in edition20/originals/).

Listen-check suggested (a human ear, not a blocker): the two joins at n148 8.08 s and n154 12.06 s.

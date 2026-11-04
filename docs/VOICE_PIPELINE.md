# Voice cloning + film assembly: what is built, what ran, what you do

Branch: `claude/original-film-studio-qtq97a` (+ the PR into it). Nothing here touches `main`.

## STATUS (honest)
| Item | Status |
|---|---|
| Chatterbox installs from PyPI on Python 3.11 (CPU torch 2.6) and imports | **Ran** (cloud sandbox, 4 CPU, no GPU) |
| Chatterbox model weights (`ResembleAI/chatterbox-turbo`) | **NOT downloaded**: the authoring sandbox's network policy blocks `huggingface.co` (HTTP 403). **No Chatterbox inference was run, no voice was cloned, no RTF/quality number for Chatterbox exists.** |
| Batch renderer (resume, silence trim, 2-pass loudness -19 LUFS, per-speaker reference routing, RTF report) | **Ran for all 162 segments** with a robotic `espeak-ng` *stand-in engine* (`--engine espeak --stand-in`) to prove plumbing only. It is not a voice clone and sounds nothing like Heba/Lion. |
| Narration assemble + `narration sync` + measured timing | **Ran** on the 162 stand-in segments (28.7 min at espeak pace; real cloned timing will differ, expect ~31-35 min) |
| Captions (SRT), YouTube chapters | **Ran** on that timing (20 chapters, first at 0:00) |
| Clip-fill renderer + 1080p MP4 with burned captions | **Ran** on the full 62-shot timeline using 98 *synthetic test-pattern clips* (not story footage) and the stand-in narration: 1920x1080, 24 fps, 1725.5 s (matches narration), captions visible in a checked frame, 12 min wall on 4 CPU cores at `ultrafast`/crf 28 (file 1.1 GB: that is the draft preset, use `medium`/crf 20 for the final). Clips plan: 900 s unique, 826 s repeated (slow-down + reframed second passes), 0 s frozen/uncovered |
| 93 -> 97 unit/integration tests | **Pass** |
| Real story footage (Veo clips), real voices | **Not available here** |

## Reference voices (git-ignored, never committed)
```
voices/heba/*.wav     # Heba: 30-60 s of clean speech total is plenty (wav/mp3/m4a/flac/ogg accepted)
voices/lion/*.wav     # Lion: same
```
`voices/` is in `.gitignore`. Record in a quiet room, same mic, natural storytelling tone, no music/echo, no clipping.
`python -m ofs voices` joins up to 25 s per speaker into `voices/<id>/_ref.wav` (24 kHz mono, levelled).
Speaker ids come from the project: `heba` (Ivy narrator + every non-Nico voice), `lion` (Nico).

## Step 1 - voices on a cloud machine (you have a weak laptop)
Google Colab free T4 (or any Linux VM with Python 3.11 + ffmpeg):
```bash
git clone -b claude/original-film-studio-qtq97a https://github.com/heba846/original-film-studio.git   # needs your GitHub auth (private repo)
cd original-film-studio
# upload voices/heba/*.wav and voices/lion/*.wav into ./voices/ (Colab file panel)
bash scripts/cloud_tts.sh married_to_the_don_full_film
```
Quick test on 5 segments first: `bash scripts/cloud_tts.sh married_to_the_don_full_film --limit 5`, listen to
`projects/married_to_the_don_full_film/media/generated/n00*.wav`, then re-run without `--limit`; finished segments are skipped
(resume). Options: `--segments n004,n010`, `--overwrite`, `--stock` (Chatterbox built-in voice, no cloning).
Tune `tts.model` (`turbo` default, or `original`) and `exaggeration`/`cfg_weight` in `project.json`. Use the model's real RTF
from the batch report: GPU is expected to be much faster than CPU, but I could not measure either.
Download `media/generated/` (162 WAVs + sidecars) and the updated `project.json` back to your laptop.
If Chatterbox is unacceptable for your voices, XTTS-v2 / OpenVoice are the fallbacks; they are **not** wired in yet.

## Step 2 - narration track + timing (laptop is fine, light CPU)
```bash
python -m ofs narration sync married_to_the_don_full_film       # shot durations from MEASURED audio
python -m ofs narration assemble married_to_the_don_full_film   # output/narration_assembled.wav
python -m ofs clips married_to_the_don_full_film                # footage plan per shot (below)
```

## Step 3 - clips
Name each Veo clip after its shot and drop it in `projects/married_to_the_don_full_film/media/clips/`:
`s05.mp4`, `s05_2.mp4`, `s05_3.mp4` ... or a folder `media/clips/s05/*.mp4`. Order = natural sort. `python -m ofs clips` prints,
per shot, seconds needed vs supplied, speed, repeated seconds and the clip count needed for all-unique footage.
**Budget reality:** shots average ~28 s of narration. With ~98 clips (~780 s of footage) against a ~1700-2000 s film, about
half of the screen time must reuse footage even with the 0.85x slow-down. Use the `clips` table to put clips where the story
needs motion, or shorten shot lengths by splitting shots in `script.md` (`python -m ofs adapt build`), or supply stills for
low-priority shots.
Fill rules the renderer enforces: no frozen frames, no clip played longer than its own length per pass; shortfall is handled
by (1) gentle slow-down down to 0.85x, then (2) a new pass over the clips with a different punch-in framing, joined by a
0.5 s crossfade. Reused seconds are shown as a warning at validate/build time.

## Step 4 - build
```bash
python -m ofs build married_to_the_don_full_film [--music path/to/bed.mp3] [--shot-transition fade]
```
Refuses to run unless every segment has measured audio and every shot has footage (or an image asset). Writes to
`projects/<name>/output/`: `film.mp4` (1920x1080, 24 fps, narration + optional ducked music, burned captions),
`film.srt`, `chapters.txt` (paste into the YouTube description), `film.render.json` (includes the synthetic-voice disclosure
for YouTube's altered/synthetic content setting) and `build_report.json`. Long encode: do it on a cloud box too if your
laptop struggles (`preset: medium` in `project.json`; use `veryfast` for drafts).

## Still missing
1. HF weight access from a machine that can reach it, then a real 5-segment Chatterbox test and an honest RTF/quality listen.
2. Your reference recordings (Heba, Lion).
3. The ~100 Veo clips named by shot.
4. Optional music bed. Your call on `exaggeration` after listening.
- Colab notebook: `notebooks/colab_voice_cloning.ipynb` (open in Colab, click through the cells).

## Cheapest path that finishes the film: automatic stills + a few video clips
Manual 8 s clips for ~100 shots is not practical, so the build also accepts still images.
1. `python -m ofs stills married_to_the_don_full_film` writes `output/stills_jobs.json`: one image per ~9 s of narration (about 190 images for the whole film), each beat with a different camera angle.
2. Open `notebooks/colab_stills.ipynb` on Colab (T4 GPU). It generates every image with SDXL base (commercial use allowed), is resumable, and downloads `stills.zip`. **Untested on Colab**; the character look can drift between images, so judge the first 4 test images before running all.
3. Unzip into `projects/married_to_the_don_full_film/media/stills/` (names `s05_1.png`, `s05_2.png` ...).
4. Optional: add a few real Veo clips for the key moments (`media/clips/s05.mp4`). A shot with clips and stills plays the clips once at normal speed and fills the rest with stills; a shot with only stills is split into equal beats with different Ken Burns moves and crossfades.
5. `python -m ofs clips ...` shows coverage; `python -m ofs build ...` renders the film.
Tested for real here: all 62 shots from 191 synthetic stills (see PR). Not tested: SDXL generation itself.

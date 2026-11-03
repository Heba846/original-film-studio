# Original Film Studio

A small, local toolkit for producing **original fictional short films** (not recaps) for YouTube.
Python + FFmpeg + a browser UI on your own machine. No paid APIs, no accounts, no credentials, nothing uploaded.

## What it is - and is not (read this first)
| It DOES | It does NOT |
|---|---|
| Keep script, character/location bible, shot list and continuity notes in one saved project | **Generate video or images.** There is no AI image/video provider inside |
| Export per-shot still + optional-motion prompts to paste into *external* tools you choose | Send audio or voice references to any online service |
| Hold two-speaker narration as segments (speaker, text, pause-after, WAV), assemble them into one narration track, compute real timing from the audio | Ship any voice recordings, embeddings or checkpoints |
| *Optionally* generate segment audio **locally** with open-source Chatterbox for speakers with confirmed consent (off by default, see `docs/CHATTERBOX.md`) | Verify consent, or promise voice quality (real inference is **untested**) |
| Validate files + timing, then assemble your supplied images/clips into a 1080p 16:9 MP4 | Make moving cinematic scenes from stills |
| Add your imported narration (one WAV/MP3, or segments), optional music (volume + ducking) and optional SRT captions | Transcribe audio or write captions for you |

**Animatic vs real motion.** Still images (optionally with a simple pan/zoom) produce an **animatic / slideshow**.
Real moving shots exist only if *you* import video clips made elsewhere. Every render writes a
`<name>.render.json` and an MP4 `comment` tag stating which it is (`animatic_slideshow`,
`assembled_supplied_video`, `mixed_stills_and_supplied_video`) and `"ai_video_generated_by_this_tool": false`.
If you publish photoreal AI-made clips/voices, check YouTube's current synthetic-content disclosure rules yourself.

## Two-speaker pilot (v0.2): "Married to the Don to Keep Me Silent"
```bash
python -m ofs pilot                          # creates projects/pilot_married_to_the_don (text only, no media)
python -m ofs narration plan   pilot_married_to_the_don   # timing; ESTIMATED until audio exists
python -m ofs validate pilot_married_to_the_don           # lists exactly what is still missing
python -m ofs pilot --dryrun                 # SYNTHETIC check: tones + placeholder art, proves assembly/timing only
```
**Product note:** the first published video should be a *complete* film with a satisfying ending (views and viewer satisfaction first; book promotion optional, never a cliffhanger paywall). This pilot is just the opening scene for testing the workflow.

Speakers: **Heba** = Ivy (female first-person narrator), **Lion** = Nico (male dialogue + Nico POV). 6 shots, 6 segments, the
author's 2-second pause is `pause_after: 2.0` on segment `n03`. The last two sentences (`n06`) are flagged **EDITORIAL
PROPOSAL** replacing the premature "I had just married into a family"; the original wording that was supplied is kept in the
project `notes` and segment `original_text` (only that fragment was given - paste the full original there).
Workflow: import/record WAVs per segment (Narration tab) -> `narration sync` fits shot durations to the real audio -> add your
illustrations to `media/pilot/s01.png...` -> Validate -> Render. Without external image/video tools the result is an
**animatic/slideshow**, and the render manifest says so.


## Full film: "Married to the Don to Keep Me Silent" (v0.3)
A complete narrated-film adaptation lives in `docs/adaptation/` (read its README first): canon ledger with page references, full script (2 speakers), segments CSV/JSON, 62-shot plan with prompts, and a loadable project `projects/married_to_the_don_full_film`. **No recordings or illustrations exist yet**, so it validates but cannot render; runtime numbers are word-count estimates. Source novel text is never stored in this repo.
```bash
python -m ofs adapt build        # regenerate segments, word count, prompts, project from docs/adaptation/script.md
python -m ofs narration plan married_to_the_don_full_film
```
**بالعربي:** حزمة الفيلم الكامل موجودة في `docs/adaptation/` (ابدأ بملف README هناك): سيناريو كامل بصوتين (Heba للراوية آيفي وكل الشخصيات الأخرى، وLion لنيكو وسرده)، وجدول مرجعي بأرقام صفحات الرواية، و62 لقطة مع برومبتات. لا توجد تسجيلات صوتية ولا رسومات بعد، لذلك المشروع يُفتح ويُفحص لكنه لا يُصدَّر فيديو حتى تُضاف الملفات. المدة المذكورة **تقدير** من عدد الكلمات وليست مقاسة. الرواية الأصلية لا تُرفع إلى git ولا إلى ملف ZIP.

## Quickstart (English)
Requirements: Python 3.10+, FFmpeg (with `ffprobe`) on PATH.

```bash
pip install -r requirements.txt        # only Pillow, used by the demo generator
python -m ofs demo                     # builds + renders the 30-second synthetic demo
python -m ofs ui                       # opens http://127.0.0.1:8765
```
Windows: run `setup.bat` once (`winget install Gyan.FFmpeg` if FFmpeg is missing), then `run.bat`.
Linux/macOS: `./run.sh`. If FFmpeg is not on PATH set `OFS_FFMPEG` / `OFS_FFPROBE`.

Workflow in the UI: **Story & Script** → **Bible** (characters/locations + continuity notes) → **Shot List**
(order with ↑↓, durations, attach files, pan/zoom) → **Prompts** (copy to your external tools, bring results back)
→ **Audio & Captions** (import narration, music, SRT) → **Validate & Render**.

## البدء السريع (عربي)
**المتطلبات:** Python 3.10 أو أحدث، وبرنامج FFmpeg (مع ffprobe) مضافين إلى PATH.

1. على ويندوز: افتح مجلد المشروع وشغّل `setup.bat` مرة واحدة. لو FFmpeg غير مثبّت اكتب في الطرفية: `winget install Gyan.FFmpeg` ثم أعد فتح الطرفية.
2. شغّل `run.bat` لفتح الواجهة على المتصفح: `http://127.0.0.1:8765`.
3. جرّب النموذج: `python -m ofs demo` يبني ويُخرج فيديو تجريبي مدته 30 ثانية من ملفات اصطناعية.
4. في الواجهة: اكتب السيناريو ← عرّف الشخصيات والأماكن وملاحظات الاستمرارية ← رتّب اللقطات وحدّد مدتها وأضف ملفات الصور/الفيديو ← صدّر البرومبتات لأدواتك الخارجية ← استورد التعليق الصوتي (WAV/MP3) الذي سجّلته أو استنسخت صوتك به بنفسك خارج هذا البرنامج، واختيارياً موسيقى وملف ترجمة SRT ← اضغط «Validate» ثم «Render».
5. **مهم:** هذه الأداة لا تولّد فيديو ولا صور. الصور الثابتة تعطي «أنيماتك/عرض شرائح» فقط (مع تحريك بسيط)، والحركة الحقيقية تأتي فقط من مقاطع فيديو تستوردها أنت. كل ملف تصدّره يُسجَّل فيه نوعه بصدق في ملف `render.json`.
6. **التجربة ثنائية الصوت (Pilot):** `python -m ofs pilot` ينشئ مشروع «Married to the Don to Keep Me Silent» (Heba = آيفي الراوية، Lion = نيكو). التسجيلات غير موجودة بعد، لذلك الفحص `validate` سيعرض ما ينقص بالضبط. في تبويب «Narration (2 speakers)» استورد ملف WAV لكل مقطع (أو سجّله بنفسك)، ثم «Assemble & preview» لدمجها في مسار واحد، ثم «Sync shot durations» ليضبط مدة كل لقطة من الصوت الحقيقي. الجملتان الأخيرتان معلَّمتان كـ «اقتراح تحريري» وليستا نصّ المؤلفة المعتمد.
7. **توليد الصوت محلياً (اختياري وغير مُختبَر):** يمكن استخدام Chatterbox مفتوح المصدر على جهازك فقط، بعد موافقة صاحب الصوت وبمسار ملف مرجعي محلي. شغّل `setup_tts.bat` (يحتاج Python 3.11 وGit)، ثم `python -m ofs tts status`، وتنزيل النموذج يتم يدوياً فقط: `python -m ofs tts download --yes`. **لم نجرّب التوليد الفعلي** هنا (لا torch ولا GPU ولا تسجيلات)؛ فقط الأجزاء الوسيطة اختُبرت بمحاكاة. لا تُرفع التسجيلات ولا ملفات الصوت المرجعية إلى git ولا إلى ملف ZIP.
8. لا يُرفع أي ملف صوتي أو غيره إلى أي خدمة خارجية؛ كل شيء يعمل على جهازك. النص العربي مدعوم في السيناريو والبرومبتات والترجمة (الحرق على الفيديو يحتاج خطاً يدعم العربية، مثل Arial على ويندوز).

## Project layout
```
projects/<name>/project.json   saved project (text, small - OK for git)
projects/<name>/media/         YOUR images/video/audio/srt   (git-ignored)
projects/<name>/output/        renders, prompts.*            (git-ignored)
```
Asset paths are relative to the project folder, or absolute. `projects/demo_30s/` is the sample project; its
`media/` is regenerated by `python -m ofs demo`.

## CLI
```
python -m ofs validate <project>     # exit code 1 on errors
python -m ofs prompts  <project>     # output/prompts.json|md|csv
python -m ofs render   <project> [--out file.mp4]
python -m ofs demo [name] [--no-render]
python -m ofs pilot [--dryrun] | narration plan|assemble|sync <project> | tts status|generate|download
python -m ofs new <name> | ui [--port N] | package [--out dist/x.zip]
```

## Validation (blocks render on errors)
Missing/unreadable/corrupt files, image-vs-video mismatch, non-positive or absurd durations, duplicate shot ids, unknown
character/location references, narration longer than the timeline (would be cut), bad volumes/FPS/CRF, missing or malformed
SRT. Warnings: clips shorter than the shot (last frame is held), non-16:9 or <720p sources (letterboxed/upscaled),
narration ending >3 s early, captions past the end/overlapping, characters named in an action but not tagged.

## Rendering details
Each shot → 1920×1080 H.264 30 fps (aspect-preserving, black bars), fades optional → concatenated → audio mixed
(narration + looped music with fade-out, optional sidechain ducking) → AAC 48 kHz. A silent track is added if you
import no audio. Captions: `burn` (re-encodes once) or `soft` (mov_text track). Audio inside supplied video clips is
discarded - supply narration/music separately.

## What is verified (exact status)
| Area | Status |
|---|---|
| 1080p assembly, validation, captions, music/ducking, prompts, UI, 30 s demo | **Tested** (Linux, FFmpeg 6.1, Python 3.13) |
| Narration segments: assemble to one WAV, real silence pauses, order, timing from ffprobe, shot sync, render from segments, old v1 projects load/validate/render | **Tested** with synthetic tone audio |
| Pilot project text, editorial flag, continuity wording in prompts, validation honesty, synthetic dry run | **Tested** |
| Chatterbox plumbing (consent gate, job file, sidecar, status) | **Tested with a mock runner only** - not a voice-quality test |
| Chatterbox install, weights download, CPU/CUDA inference, clone quality | **UNTESTED** (no torch/GPU/recordings here) |
| `setup.bat`, `run.bat`, `setup_tts.bat` on Windows | **UNTESTED** (written for Windows, run only on Linux logic) |
| Real narration for the pilot, real illustrations, real timing | **NOT AVAILABLE** - recordings/images don't exist yet; shot durations are estimates until audio is imported |

## Tests
```bash
pip install -r requirements-dev.txt && python -m pytest -q
```
Covers timeline/file validation, narration segments, TTS plumbing (mock), pilot, project save/load, SRT, prompts, real FFmpeg renders probed with ffprobe (resolution, codec,
duration, audio/subtitle streams, reorder, held clips, music volume via measured loudness, burned captions), the local server
(CSRF header, host check, path traversal, uploads) and the full 30 s demo.

## Security / privacy
Voice references are local paths only and are never uploaded, copied into git or the ZIP. UI binds to 127.0.0.1 only; writes require a custom header and a localhost `Host`; uploads are copied only into the project's
`media/` folder. No network calls, no API keys, no telemetry. See `docs/NARRATOR_AI_AUDIT.md` for why the third-party
narration CLI is not used.

## Known limitations
See `docs/LIMITATIONS.md`.


## Voice cloning at scale + clip-filled film
See `docs/VOICE_PIPELINE.md` (cloud TTS batch, clip planner `python -m ofs clips`, one-command `python -m ofs build`).

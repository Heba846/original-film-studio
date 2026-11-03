# Limitations (honest list)
- No generation of any kind. Prompts are text only; quality depends on the external tools you use.
- Stills + pan/zoom = animatic. No lip-sync, character animation or camera moves beyond simple pan/zoom.
- Audio inside imported video clips is dropped. No audio editing, no per-shot narration offsets (one narration file, starts at 0:00).
- Transitions: hard cut or dip-to-black fade only. No crossfades, no per-shot titles.
- Captions are imported only; burn-in style is fixed (white, outlined, bottom). Arabic burn-in needs a font with Arabic glyphs
  and a libass build with shaping; verify on your machine. Soft subtitles are mov_text (YouTube prefers uploading the SRT separately).
- Output is fixed 16:9 1080p; no 4K, vertical or HDR.
- The UI is a basic single-page editor (no drag-and-drop reordering, no undo, one render at a time, no waveform/timeline scrubbing).
- Tested on Linux here (FFmpeg 6.1, Python 3.13). Windows files (`setup.bat`, `run.bat`) were written to be Windows-friendly
  but were NOT executed on Windows in this environment.
- Needs an FFmpeg build with libx264, libass (`subtitles`), `sidechaincompress` and `zoompan` (standard "full"/Gyan builds have them).

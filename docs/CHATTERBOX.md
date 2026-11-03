# Optional local voice generation with Chatterbox

**Scope change (v0.2):** the first version of this toolkit said it would not clone voices. That is now relaxed
*only* for this optional, local, open-source path, and only for speakers whose consent the owner has confirmed.
**Imported recordings (WAV/MP3) remain the default.** The app never needs Chatterbox.

## What was inspected (official `resemble-ai/chatterbox`, read from the repo on GitHub)
| Item | Finding |
|---|---|
| License | MIT (Copyright 2025 Resemble AI) - commercial use allowed |
| Install | `pip install chatterbox-tts` (v0.1.7 in `pyproject.toml`), requires Python >= 3.10; authors developed on **Python 3.11** |
| Pinned deps | `torch==2.6.0`, `torchaudio==2.6.0`, `transformers==5.2.0`, `diffusers==0.29.0`, `librosa==0.11.0`, `gradio==6.8.0`, `resemble-perth` **from GitHub** (needs Git), `numpy<2` on Py<3.13 ... |
| Models | Turbo 350M (English, low compute), Nano 110M (English, CPU-oriented), original 500M English (exaggeration/CFG), Multilingual V3 500M |
| Voice cloning | `model.generate(text, audio_prompt_path="ref.wav")`; README says Turbo needs a reference clip (about 10 s) |
| Devices | `device="cuda"` or `"cpu"` (also `mps`) |
| Weights | `from_pretrained` fetches from Hugging Face on first use |
| Watermark | Every generated file carries a Resemble **PerTh** watermark (README) - good for disclosure, do not strip it |
| Cost | Open-source, runs locally; Resemble also sells a hosted service - **not used here** |

## How this repo integrates it
- `ofs/tts_worker.py` runs **inside an isolated interpreter** (`.venv-tts`, created by `setup_tts.bat`). The main app never imports torch/chatterbox (there is a test for that).
- `ofs/tts.py` only builds a job (text + local reference path + output path) and calls the worker as a subprocess. Lazy: nothing happens until you press **Generate** or run `python -m ofs tts generate`.
- **No automatic model download.** The worker sets `HF_HUB_OFFLINE=1`; if weights are absent it says so. You download explicitly: `python -m ofs tts download --yes` (network, your choice).
- **CPU/CUDA detection:** `python -m ofs tts status` (UI: "Check local Chatterbox status") probes `torch.cuda.is_available()` in the isolated env; `tts.device: "auto"` picks CUDA if present else CPU; `"cuda"` hard-fails if CUDA is missing. `setup_tts.bat` chooses the CPU or `cu124` torch wheels via `nvidia-smi`.
- **Consent gate:** generation refuses unless the speaker has `consent_confirmed: true` and an existing local `reference_audio`. The checkbox records the owner's statement; this software cannot verify consent.
- **Outputs:** `media/generated/<segment>.wav` + a sidecar `.wav.json` (engine, model, device, timestamp). No embeddings are stored. Generated segments are marked `source: "generated"`; the render manifest lists them and carries a synthetic-voice disclosure reminder.
- **Privacy / source control:** reference clips are *paths*, never copied or uploaded. `.gitignore` and the ZIP builder exclude `voices/`, `references/`, `media/`, `.venv-tts/`, `*.wav|mp3|flac|m4a|ogg|pt|pth|ckpt|safetensors|npy|npz`.
- Long text is split by sentence (<= ~280 chars) and joined with 0.15 s gaps; this is a guess at a safe size, not a documented upstream limit.

## Exact verification status
| Part | Status |
|---|---|
| Job building, consent/reference gating, segment update, sidecar writing, assembly of the produced WAVs | **Tested** with a mock runner (plumbing only; mock output is a tone, **not** a voice-quality test) |
| Worker's "chatterbox not installed" and probe paths; main app imports no torch | **Tested for real** (this env has no torch) |
| Installing Chatterbox via `setup_tts.bat`, model download, CPU/CUDA inference, quality of Heba/Lion clones, speed | **UNTESTED** - no torch, no GPU, no consented recordings were available |
| Whether Turbo/Nano/original gives acceptable narration for your voices, and the right `exaggeration`/`cfg_weight` | **UNKNOWN** - evaluate with your real reference clips; keep the imported-WAV path as fallback |

## Recording references (for the owner)
Use a clean 10-30 s mono/stereo WAV per speaker, no music or room echo, same mic as the rest of the story, reading in the
target style. Store outside the repo (e.g. `D:\voices\heba_ref.wav`) and paste the path in the Narration tab.

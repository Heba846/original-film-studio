#!/usr/bin/env bash
# Voice cloning on a cloud box (Colab / Kaggle / any Linux VM; GPU optional, CPU works but is slow).
# Usage:  bash scripts/cloud_tts.sh [project] [extra args for `ofs ttsbatch`]
# Needs: python3.11 (or 3.10), ffmpeg, git, internet access to PyPI + huggingface.co (model weights).
# Reference voices must already be in ./voices/heba/*.wav and ./voices/lion/*.wav (git-ignored).
set -euo pipefail
PROJECT="${1:-married_to_the_don_full_film}"; shift || true
cd "$(dirname "$0")/.."
PY="$(command -v python3.11 || command -v python3.10 || command -v python3)"
[ -d .venv-tts ] || "$PY" -m venv .venv-tts
. .venv-tts/bin/activate
if ! python -c "import chatterbox" 2>/dev/null; then
  pip install -q --upgrade pip
  pip install -q chatterbox-tts            # pulls torch (CUDA wheels on Linux; CPU fallback is automatic)
fi
python ofs/tts_worker.py probe
python -m ofs tts download --yes           # explicit weight download (Hugging Face)
python -m ofs voices "$PROJECT"            # builds voices/<id>/_ref.wav
python -m ofs ttsbatch "$PROJECT" "$@"     # resumable: re-run the same command after any interruption
python -m ofs narration sync "$PROJECT"
python -m ofs narration assemble "$PROJECT"
python -m ofs narration plan "$PROJECT" | tail -3

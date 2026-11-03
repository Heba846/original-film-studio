@echo off
REM OPTIONAL: isolated local Chatterbox TTS environment (.venv-tts). The main app never needs it.
REM Upstream (resemble-ai/chatterbox, MIT) was developed on Python 3.11 and pins torch==2.6.0.
REM It also installs resemble-perth from GitHub, so Git must be installed.
REM STATUS: this script has NOT been run on Windows by the authors of this repo.
REM This script downloads Python PACKAGES only. Model weights are NOT downloaded here;
REM run  python -m ofs tts download --yes  yourself when you are ready.
setlocal
where git >nul 2>nul || (echo Git is required: https://git-scm.com/download/win & exit /b 1)
set PY=py -3.11
%PY% --version >nul 2>nul || (echo Python 3.11 not found. Install it from python.org, then re-run. & exit /b 1)
%PY% -m venv .venv-tts || exit /b 1
call .venv-tts\Scripts\activate.bat
python -m pip install --upgrade pip
set INDEX=cpu
where nvidia-smi >nul 2>nul && set INDEX=cu124
echo Detected torch wheel flavour: %INDEX%   (override: set INDEX=cpu before running)
pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/%INDEX% || exit /b 1
pip install chatterbox-tts || exit /b 1
python ofs\tts_worker.py probe
echo.
echo Done. Check status with:  python -m ofs tts status
endlocal

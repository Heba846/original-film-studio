@echo off
REM Windows setup: creates a virtual env and installs Python packages. Needs Python 3.10+ and FFmpeg.
where python >nul 2>nul || (echo Python not found. Install from https://www.python.org/downloads/ and tick "Add to PATH". & exit /b 1)
python -m venv .venv || exit /b 1
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt || exit /b 1
where ffmpeg >nul 2>nul || (
  echo.
  echo FFmpeg not found on PATH. Install it with:   winget install Gyan.FFmpeg
  echo then open a NEW terminal window and run run.bat
)
echo Setup finished. Run run.bat to open the studio.

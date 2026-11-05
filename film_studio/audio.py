"""Tiny WAV helpers. Everything in the pipeline is 24 kHz mono 16-bit."""
from __future__ import annotations

import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 24000


def ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SystemExit("ffmpeg not found on PATH. Install it (Windows: `winget install Gyan.FFmpeg`) and reopen the terminal.")
    return exe


def run_ffmpeg(args: list[str], cwd: Path | None = None) -> None:
    cmd = [ffmpeg_bin(), "-hide_banner", "-loglevel", "error", "-y", *args]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"ffmpeg failed ({r.returncode}): {' '.join(cmd[:12])} ...\n{r.stderr[-1500:]}")


def to_wav24(src: Path, dst: Path) -> None:
    """Convert any audio file to 24 kHz mono 16-bit WAV."""
    run_ffmpeg(["-i", str(src), "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(dst)])


def write_wav(path: Path, samples: np.ndarray, sr: int = SR) -> None:
    if samples.dtype != np.int16:
        samples = (np.clip(samples, -1, 1) * 32767).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(samples.tobytes())


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        if w.getframerate() != SR or w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise ValueError(f"{path} is not 24kHz mono 16-bit; run through to_wav24 first")
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def silence(seconds: float) -> np.ndarray:
    return np.zeros(int(round(seconds * SR)), dtype=np.int16)

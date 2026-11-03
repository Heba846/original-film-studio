"""FFmpeg / ffprobe discovery and media probing."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}


class MediaError(Exception):
    pass


def tool(name: str) -> str | None:
    """Locate ffmpeg/ffprobe. Override with OFS_FFMPEG / OFS_FFPROBE env vars."""
    env = os.environ.get("OFS_" + name.upper())
    if env:
        return env
    return shutil.which(name)


def tool_versions() -> dict:
    out = {}
    for n in ("ffmpeg", "ffprobe"):
        p = tool(n)
        if not p:
            out[n] = None
            continue
        try:
            r = subprocess.run([p, "-version"], capture_output=True, text=True, timeout=20)
            out[n] = r.stdout.splitlines()[0] if r.stdout else p
        except Exception:
            out[n] = None
    return out


def probe(path) -> dict:
    """Return basic facts about a media file using ffprobe."""
    ffprobe = tool("ffprobe")
    if not ffprobe:
        raise MediaError("ffprobe not found (install FFmpeg and add it to PATH)")
    r = subprocess.run(
        [ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        raise MediaError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "unreadable media")
    data = json.loads(r.stdout or "{}")
    info = {"duration": None, "width": None, "height": None, "fps": None,
            "has_video": False, "has_audio": False}
    for s in data.get("streams", []):
        if s.get("codec_type") == "video" and not info["has_video"]:
            info["has_video"] = True
            info["width"], info["height"] = s.get("width"), s.get("height")
            try:
                n, d = s.get("avg_frame_rate", "0/1").split("/")
                info["fps"] = float(n) / float(d) if float(d) else None
            except Exception:
                pass
        elif s.get("codec_type") == "audio":
            info["has_audio"] = True
    try:
        info["duration"] = float(data.get("format", {}).get("duration"))
    except (TypeError, ValueError):
        pass
    return info

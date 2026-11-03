import subprocess
import sys
import wave
import struct
import math
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ofs import media, project as proj  # noqa: E402


def ffmpeg(*args):
    subprocess.run([media.tool("ffmpeg"), "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def make_wav(path, seconds, freq=440, amp=0.5, sr=22050):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(32767 * amp * math.sin(2 * math.pi * freq * i / sr)))
                               for i in range(int(seconds * sr))))


@pytest.fixture(scope="session")
def assets(tmp_path_factory):
    d = tmp_path_factory.mktemp("assets")
    ffmpeg("-f", "lavfi", "-i", "color=c=0x336699:s=640x360", "-frames:v", "1", str(d / "img.png"))
    ffmpeg("-f", "lavfi", "-i", "color=c=0x993366:s=800x800", "-frames:v", "1", str(d / "square.png"))
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=1280x720:r=24:d=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(d / "clip2s.mp4"))
    make_wav(d / "narr3.wav", 3.0)
    make_wav(d / "narr9.wav", 9.0)
    make_wav(d / "music.wav", 2.0, freq=220, amp=0.8)
    (d / "caps.srt").write_text("1\n00:00:00,500 --> 01:00:01,500\nHello\n\n2\n00:00:02,000 --> 00:00:03,000\nWorld\n", encoding="utf-8")
    (d / "caps_ok.srt").write_text("1\n00:00:00,500 --> 00:00:01,500\nHello\n\n2\n00:00:02,000 --> 00:00:02,900\nWorld\n", encoding="utf-8")
    (d / "bad.srt").write_text("1\nnot a time\nHello\n", encoding="utf-8")
    return d


@pytest.fixture
def pdir(tmp_path, assets):
    """A project dir with copies of the assets under media/."""
    import shutil
    m = tmp_path / "media"
    m.mkdir()
    for f in assets.iterdir():
        shutil.copy(f, m / f.name)
    return tmp_path


def shot(i, kind="image", asset="media/img.png", dur=1.0, **kw):
    return {"id": f"s{i}", "kind": kind, "asset": asset, "duration": dur, **kw}


@pytest.fixture
def basic(pdir):
    return proj.normalize({"title": "t", "shots": [shot(1), shot(2, "video", "media/clip2s.mp4", 2.0), shot(3, dur=1.5)]})

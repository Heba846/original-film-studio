"""Build the 30-second SYNTHETIC-ASSETS demo project (no real footage, no real voice).

Everything here is generated locally: gradient/silhouette images (Pillow), test-pattern
video clips (FFmpeg lavfi), a placeholder 'narration' made of tone blips (NOT speech),
a synthetic music pad, and an SRT. It exists to prove the pipeline, not to look cinematic.
"""
from __future__ import annotations

import array
import math
import subprocess
import wave
from pathlib import Path

from . import media, project as proj

SR = 44100
CUES = [
    (0.5, 4.5, "The lighthouse had been dark for nine years."),
    (5.5, 9.5, "Mira climbed the stairs anyway."),
    (10.5, 14.5, "At the top, a single lens still held the old light."),
    (15.5, 19.5, "She wiped the glass with her father's coat."),
    (20.5, 24.5, "Far out at sea, a boat turned toward the shore."),
    (25.5, 28.5, "Some lights wait to be asked."),
]

DEMO = {
    "title": "The Last Lantern (synthetic demo)",
    "logline": "A keeper's daughter relights a dead lighthouse. ORIGINAL fictional story; demo uses placeholder art.",
    "style": "Hand-painted storybook look, muted teal and amber palette, soft film grain",
    "script": ("FADE IN.\nEXT. CLIFF - DUSK. A lighthouse, dark for nine years.\nMIRA (12) climbs the stairs.\n"
              "INT. LANTERN ROOM. She cleans the lens. It catches the last sun.\nEXT. SEA. A boat turns toward the light.\n"
              "NARRATOR: Some lights wait to be asked."),
    "characters": [{
        "id": "mira", "name": "Mira",
        "description": "12-year-old girl, short black hair, determined expression, freckles",
        "wardrobe": "oversized faded yellow raincoat, red scarf",
        "voice_notes": "Narrator is an adult storyteller, warm and unhurried",
        "continuity_notes": "Scarf is always RED; raincoat sleeves always too long; no hat",
        "reference": "see media/ref_mira.png (supply your own)"}],
    "locations": [
        {"id": "lighthouse", "name": "Lighthouse on the cliff",
         "description": "weathered white tower with a rusted iron gallery", "lighting": "low amber dusk light",
         "continuity_notes": "Tower is on the LEFT of frame when viewed from the sea", "reference": ""},
        {"id": "sea", "name": "Open sea", "description": "dark teal water, small fishing boat",
         "lighting": "last red glow on the horizon", "continuity_notes": "Boat has a green hull", "reference": ""}],
    "shots": [],
    "audio": {"narration": "media/narration_placeholder.wav", "music": "media/music_pad.wav",
              "narration_volume": 1.0, "music_volume": 0.3, "duck_music": True},
    "captions": {"srt": "media/captions.srt", "mode": "burn"},
    "render": {"fps": 30, "crf": 21, "preset": "veryfast"},
}

SHOTS = [
    ("s01", "Dark tower", "image", "media/s01.png", "zoom_in", ["", "lighthouse"], "Wide shot of the dark lighthouse at dusk", "slow push-in"),
    ("s02", "Stairs", "video", "media/s02.mp4", "none", ["mira", "lighthouse"], "Mira climbs the spiral stairs", "handheld follow"),
    ("s03", "The lens", "image", "media/s03.png", "pan_right", ["mira", "lighthouse"], "Close on the old lens", "slow pan across glass"),
    ("s04", "Wiping glass", "image", "media/s04.png", "zoom_out", ["mira", "lighthouse"], "Mira wipes the lens with a coat", "pull back to reveal room"),
    ("s05", "The boat", "video", "media/s05.mp4", "none", ["", "sea"], "A boat turns toward the shore", "static wide"),
    ("s06", "Lit", "image", "media/s06.png", "zoom_in", ["mira", "lighthouse"], "The light finally turns on", "slow push-in on beam"),
]


def build_project() -> dict:
    p = dict(DEMO)
    p["shots"] = []
    for sid, title, kind, asset, motion, (chars, loc), action, camera in SHOTS:
        p["shots"].append({
            "id": sid, "title": title, "kind": kind, "asset": asset, "duration": 5.0, "trim_start": 0.0,
            "motion": motion, "transition": "fade" if sid in ("s01", "s06") else "cut",
            "characters": [chars] if chars else [], "location": loc, "action": action, "camera": camera,
            "dialogue": "", "continuity_notes": "Keep Mira's scarf red" if chars else ""})
    return proj.normalize(p)


def _png(path: Path, idx: int, label: str):
    from PIL import Image, ImageDraw, ImageFont
    pal = [((20, 40, 60), (230, 150, 70)), ((15, 30, 45), (90, 150, 160)), ((25, 25, 45), (240, 200, 120)),
           ((10, 35, 50), (200, 110, 80)), ((5, 20, 35), (60, 120, 140)), ((15, 15, 30), (255, 220, 140))][idx % 6]
    img = Image.new("RGB", (1920, 1080))
    d = ImageDraw.Draw(img)
    for y in range(1080):
        t = y / 1079
        d.line([(0, y), (1920, y)], fill=tuple(int(pal[0][i] * (1 - t) + pal[1][i] * t) for i in range(3)))
    d.rectangle([880, 300, 1040, 1080], fill=(235, 235, 225))      # tower silhouette
    d.polygon([(860, 300), (1060, 300), (960, 200)], fill=(150, 40, 40))
    d.ellipse([930, 120 + idx * 10, 990, 180 + idx * 10], fill=(255, 235, 160))
    try:
        font = ImageFont.load_default(size=64)
    except TypeError:
        font = ImageFont.load_default()
    d.text((80, 60), f"SYNTHETIC PLACEHOLDER  {label}", fill=(255, 255, 255), font=font)
    img.save(path)


def _wav(path: Path, samples):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(array.array("h", samples).tobytes())


def _narration(path: Path, total=29.0):
    """Placeholder cadence track: tone blips at each caption's timing. NOT speech."""
    n = int(total * SR)
    buf = [0] * n
    for k, (a, b, _) in enumerate(CUES):
        f = 220 + 40 * k
        for i in range(int(a * SR), min(n, int(b * SR))):
            t = i / SR
            env = 0.5 * (1 - math.cos(2 * math.pi * min(1, (t - a) / (b - a)))) * (0.5 + 0.5 * math.sin(2 * math.pi * 3 * t))
            buf[i] = int(9000 * env * math.sin(2 * math.pi * f * t))
    _wav(path, buf)


def _music(path: Path, total=30.0):
    n = int(total * SR)
    buf = array.array("h", [0]) * n
    for i in range(n):
        t = i / SR
        trem = 0.75 + 0.25 * math.sin(2 * math.pi * 0.2 * t)
        v = sum(math.sin(2 * math.pi * f * t) for f in (110, 164.8, 220, 277.2)) / 4
        buf[i] = int(8000 * trem * v)
    _wav(path, list(buf))


def _clip(path: Path, color: str, seconds=5):
    ff = media.tool("ffmpeg")
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
                    f"testsrc2=size=1280x720:rate=24:duration={seconds}", "-vf", f"hue=h={color}",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True)


def create_assets(media_dir: Path):
    media_dir.mkdir(parents=True, exist_ok=True)
    for i, (sid, title, kind, asset, *_r) in enumerate(SHOTS):
        if kind == "image":
            _png(media_dir / Path(asset).name, i, f"{sid}: {title}")
        else:
            _clip(media_dir / Path(asset).name, str(60 * i))
    _narration(media_dir / "narration_placeholder.wav")
    _music(media_dir / "music_pad.wav")
    from . import srt
    (media_dir / "captions.srt").write_text(
        srt.format_srt([{"start": a, "end": b, "text": t} for a, b, t in CUES]), encoding="utf-8")


def make_demo(project_dir, render_it=True, progress=None):
    project_dir = Path(project_dir)
    create_assets(project_dir / "media")
    p = build_project()
    proj.save(project_dir, p)
    if render_it:
        from . import render
        return render.render(p, project_dir, project_dir / "output" / "demo_30s.mp4", progress)
    return None

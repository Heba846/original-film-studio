#!/usr/bin/env python3
"""output/full/Film20_NARRATION_MASTER.flac: every segment's audio placed at its exact timeline frame (ffmpeg only).
The reference that tools/verify_final.py compares the rendered film's soundtrack against."""
import json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent.parent
T = json.loads((R / "src/film/data/film_timeline.json").read_text()); fps = T["fps"]
S = R / "output/full"; S.mkdir(parents=True, exist_ok=True)
args, f = ["ffmpeg", "-v", "error", "-y"], []
for i, s in enumerate(T["segments"]):
    args += ["-i", str(R / "public" / s["audio"])]
    ms = round(s["from"] / fps * 1000)
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{s['dur']/fps:.4f},adelay={ms}|{ms}[a{i}]")
n = len(T["segments"])
f.append("".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:dropout_transition=0,apad,atrim=0:{T['total_frames']/fps:.4f}[out]")
fc = S / "_master_filter.txt"; fc.write_text(";".join(f))
out = S / "Film20_NARRATION_MASTER.flac"
subprocess.run(args + ["-filter_complex_script", str(fc), "-map", "[out]", "-c:a", "flac", str(out)], check=True)
print(out, T["total_frames"], "frames", round(T["total_frames"] / fps, 2), "s")

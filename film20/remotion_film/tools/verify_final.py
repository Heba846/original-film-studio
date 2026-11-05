#!/usr/bin/env python3
"""Verify a rendered master BEFORE calling it final. No network, ffmpeg/numpy only.
  python3 tools/verify_final.py output/final/Film20_Final_720p.mp4 [--expect-frames N] [--audio-ref FILE.flac] [--srt FILE.srt]
Checks: V1 container/stream (h264, 1280x720, 24 fps, AAC) · V2 frame count == timeline total (±1) · V3 narration identical to the
master (envelope correlation >= 0.98, offset <= 1 frame, level within 1 dB) · V4 no black run > 0.5 s except the planned head/tail ·
V5 no frozen run > 2.5 s · V6 SRT: every cue inside the runtime, ordered, non-empty · V7 contact sheet of one frame per cut for the
human picture pass (output/final/QA_cut_sheet_*.png). Exit 1 on any failure; writes output/final/VERIFY.json."""
import json, subprocess, sys, re
from pathlib import Path
import numpy as np
R = Path(__file__).resolve().parent.parent
a = sys.argv[1:]
mp4 = Path(a[0]); opt = {a[i]: a[i + 1] for i in range(1, len(a) - 1, 2)}
T = json.loads((R / "src/film/data/film_timeline.json").read_text())
fps = T["fps"]; exp = int(opt.get("--expect-frames", T["total_frames"]))
ref = Path(opt.get("--audio-ref", R / "output/full/Film20_NARRATION_MASTER_20m46s.flac"))
srt = Path(opt.get("--srt", R / "edition20/out/Film20_captions.srt"))
res, fail = {}, []
def run(*c): return subprocess.run(c, capture_output=True, text=True).stdout
pr = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(mp4)))
v = next(s for s in pr["streams"] if s["codec_type"] == "video"); au = [s for s in pr["streams"] if s["codec_type"] == "audio"]
nb = int(run("ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(mp4)).strip().strip(","))
res["V1"] = {"codec": v["codec_name"], "size": f'{v["width"]}x{v["height"]}', "fps": v["r_frame_rate"], "audio": [s["codec_name"] for s in au]}
if v["codec_name"] != "h264" or (v["width"], v["height"]) != (1280, 720) or v["r_frame_rate"] != f"{fps}/1" or not au: fail.append("V1")
res["V2"] = {"frames": nb, "expected": exp}
if abs(nb - exp) > 1: fail.append("V2")
def pcm(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)
if ref.exists() and exp == T["total_frames"]:
    x, y = pcm(mp4), pcm(ref); n = min(len(x), len(y)); hop = 80  # 10 ms envelope
    ex = np.sqrt(np.convolve(x[:n] ** 2, np.ones(hop) / hop, "same"))[::hop]; ey = np.sqrt(np.convolve(y[:n] ** 2, np.ones(hop) / hop, "same"))[::hop]
    best = max(range(-5, 6), key=lambda k: np.corrcoef(np.roll(ex, k), ey)[0, 1])
    c = float(np.corrcoef(np.roll(ex, best), ey)[0, 1]); db = float(20 * np.log10((x[:n].std() + 1e-9) / (y[:n].std() + 1e-9)))
    res["V3"] = {"envelope_corr": round(c, 4), "offset_ms": best * 10, "level_diff_db": round(db, 2), "dur_s": [round(len(x) / 8000, 3), round(len(y) / 8000, 3)]}
    if c < 0.98 or abs(best * 10) > 1000 / fps or abs(db) > 1.0 or abs(len(x) - len(y)) > 8000 / fps: fail.append("V3")
else:
    res["V3"] = "skipped (no master or partial render)"
bd = run("ffmpeg", "-v", "info", "-i", str(mp4), "-vf", "blackdetect=d=0.5:pix_th=0.06", "-an", "-f", "null", "-") or ""
bd += subprocess.run(["ffmpeg", "-v", "info", "-i", str(mp4), "-vf", "blackdetect=d=0.5:pix_th=0.06", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
blacks = [(float(s), float(e)) for s, e in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bd)]
total = nb / fps; bad = [b for b in blacks if b[0] > 1.0 and b[1] < total - 4.0]
res["V4"] = {"black_runs": blacks, "unplanned": bad}
if bad: fail.append("V4")
fz = subprocess.run(["ffmpeg", "-v", "info", "-i", str(mp4), "-vf", "freezedetect=n=0.002:d=2.5", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
frz = re.findall(r"freeze_start: ([\d.]+).*?freeze_end: ([\d.]+)", fz, re.S)
res["V5"] = {"frozen_runs_over_2_5s": frz}
if frz: fail.append("V5")
if srt.exists():
    cues = re.findall(r"(\d\d):(\d\d):(\d\d),(\d\d\d) --> (\d\d):(\d\d):(\d\d),(\d\d\d)\n(.+?)(?:\n\n|\Z)", srt.read_text(), re.S)
    t = lambda h, m, s, ms: int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    st = [(t(*c[:4]), t(*c[4:8]), c[8].strip()) for c in cues]
    ok = all(a0 < a1 <= total + 0.01 and txt for a0, a1, txt in st) and all(st[i][0] >= st[i - 1][0] for i in range(1, len(st)))
    res["V6"] = {"cues": len(st), "last_end": st[-1][1] if st else None, "ok": ok}
    if not ok or not st: fail.append("V6")
else:
    res["V6"] = f"missing {srt}"; fail.append("V6")
mids = [(c["from"] + c["dur"] // 2) / fps for c in T["cuts"] if c["from"] + c["dur"] <= nb]
out = mp4.parent
for k in range(0, len(mids), 48):
    sel = "+".join(f"eq(n\\,{int(m * fps)})" for m in mids[k:k + 48])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select='{sel}',scale=320:-2,tile=8x6", "-frames:v", "1", "-vsync", "0",
                    str(out / f"QA_cut_sheet_{k // 48 + 1:02d}.png")])
res["V7"] = f"{len(mids)} cut frames -> {out}/QA_cut_sheet_*.png (human picture pass required)"
res["verdict"] = "PASS (technical) - picture pass still required" if not fail else f"FAIL {fail}"
(out / "VERIFY.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1)[:2500]); sys.exit(1 if fail else 0)

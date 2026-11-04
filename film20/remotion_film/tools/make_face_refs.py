#!/usr/bin/env python3
"""Face-only reference images for Flow, cut from the approved hospital.mp4 (the source of hospital.png).

Run with a Python that has opencv-python-headless + numpy:  <venv>/bin/python tools/make_face_refs.py
Background removal is local OpenCV GrabCut (no model download, no paid service), seeded with a head rectangle
and refined with a soft alpha edge. Outputs (edition20/flow_refs/):
  REF_IVY_FACE_ONLY.png / REF_NICO_FACE_ONLY.png         transparent background (RGBA)
  REF_IVY_FACE_ONLY_GRAY.png / REF_NICO_FACE_ONLY_GRAY.png flat neutral gray background (if Flow flattens alpha)
  REF_GARAGE_F01.png                                       approved F01 still (location only)
"""
import subprocess, sys
from pathlib import Path
import cv2
import numpy as np

R = Path(__file__).resolve().parent.parent
OUT = R / "edition20/flow_refs"
SRC = R / "public/hospital.mp4"
# time, crop box (x, y, w, h); inside the crop: GrabCut rect, face ellipse (cx, cy, ax, ay), hair ellipse
PICKS = {
    "IVY": (2.5, (170, 0, 400, 400), (40, 0, 330, 400), (205, 230, 55, 75), (190, 120, 120, 120)),
    "NICO": (5.5, (740, 0, 400, 400), (20, 0, 360, 400), (115, 155, 50, 70), (150, 70, 125, 75)),
}

def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(SRC), "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(720, 1280, 3).copy()

def cut(img, rect, face, hair):
    """Seeded GrabCut: teal curtain/background = definite BG, face ellipse = definite FG, hair ellipse = probable FG."""
    h, w = img.shape[:2]
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)
    x, y, rw, rh = rect
    mask[y:y + rh, x:x + rw] = cv2.GC_PR_BGD
    cv2.ellipse(mask, hair[:2], hair[2:4], 0, 0, 360, cv2.GC_PR_FGD, -1)
    cv2.ellipse(mask, face[:2], face[2:4], 0, 0, 360, cv2.GC_FGD, -1)
    cv2.ellipse(mask, (hair[0], hair[1] - hair[3] // 4), (hair[2] // 2, hair[3] // 3), 0, 0, 360, cv2.GC_FGD, -1)  # hair core
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    teal = (hsv[:, :, 0] > 78) & (hsv[:, :, 0] < 110) & (hsv[:, :, 1] > 45)
    mask[teal & (mask != cv2.GC_FGD)] = cv2.GC_BGD
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, None, bgd, fgd, 10, cv2.GC_INIT_WITH_MASK)
    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # keep the largest component (the head), close small holes, feather the edge
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)
    if n > 1:
        keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        fg = np.where(lab == keep, 255, 0).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return cv2.GaussianBlur(fg, (7, 7), 0)

OUT.mkdir(parents=True, exist_ok=True)
for name, (t, (x, y, w, h), rect, face, hair) in PICKS.items():
    img = frame(t)[y:y + h, x:x + w]
    a = cut(img, rect, face, hair)
    rgba = np.dstack([img, a])
    big = cv2.resize(rgba, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)   # plain resize, no AI upscaling
    cv2.imwrite(str(OUT / f"REF_{name}_FACE_ONLY.png"), big)
    alpha = big[:, :, 3:4].astype(np.float32) / 255
    gray = (big[:, :, :3].astype(np.float32) * alpha + 128 * (1 - alpha)).astype(np.uint8)
    cv2.imwrite(str(OUT / f"REF_{name}_FACE_ONLY_GRAY.png"), gray)
    print(name, "kept", round(float((a > 127).mean()) * 100, 1), "% of the crop")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "4.0", "-i", str(R / "public/flow/F01.mp4"), "-frames:v", "1",
                str(OUT / "REF_GARAGE_F01.png")], check=True)
print("written to", OUT)

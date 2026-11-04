#!/usr/bin/env python3
"""Intake + review for Flow results.  No paid calls; ffmpeg/ffprobe only.

  python3 tools/flow_intake.py ingest <file.mp4|file.zip|dir> ...   copy F##.mp4 into public/flow/, probe, build review sheets
  python3 tools/flow_intake.py approve F07 [--note "..."]             human verdict after the checklist (sets status: approved)
  python3 tools/flow_intake.py reject  F07 --note "reason"             sets status: rejected (needs retake / re-plan)
  python3 tools/flow_intake.py retake  F07 --note "reason"             moves the take to public/flow/rejected/, status back to
                                                                       missing (retake pending) so the plan keeps its placements
  python3 tools/flow_intake.py report                                 edition20/review/REVIEW.md for all delivered files

Automatic checks (they inform the human verdict; they never approve anything):
  A1 name matches a budgeted job (F01-F70); file decodes; video h264/hevc/vp9; 24/25/30 fps noted
  A2 duration >= every planned source range for this job (re-measured; the builder re-plans if shorter)
  A3 frozen-frame share (mpdecimate) and black frames inside the planned ranges
  A4 embedded audio level (Flow audio is never used; noted only)
Human checklist (FLOW_JOBS_NEXT.md): faces vs hospital.png, injured arm anatomical RIGHT, healed scar anatomical LEFT brow,
date-correct ring/chain/splint, no falling rain indoors, no readable text/logos, no one shown firing, mouths closed where
required, roles and positions stable. Mirroring is never a fix.
"""
import json, re, shutil, subprocess, sys, zipfile, tempfile
from datetime import date
from pathlib import Path

R = Path(__file__).resolve().parent.parent
FLOW = R / "public/flow"
REV = R / "edition20/review"
MAN = R / "edition20/media_manifest.json"
JOBS = {j["job_id"]: j for j in json.loads((R / "edition20/flow_jobs.json").read_text())["jobs"]}
REF = R / "edition20/flow_refs/REF_style_twoshot_hospital_7s.png"

def sh(*a): return subprocess.run(a, capture_output=True, text=True)

def probe(f: Path) -> dict:
    j = json.loads(sh("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(f)).stdout or "{}")
    v = next((s for s in j.get("streams", []) if s["codec_type"] == "video"), None)
    a = next((s for s in j.get("streams", []) if s["codec_type"] == "audio"), None)
    if not v: return {"ok": False, "error": "no video stream"}
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    return {"ok": True, "codec": v["codec_name"], "w": v["width"], "h": v["height"], "fps": round(num / den, 3),
            "duration": float(v.get("duration") or j["format"]["duration"]), "audio": bool(a)}

def placements(jid):
    t = json.loads((R / "src/film/data/film_timeline.json").read_text())
    return [c for c in t["cuts"] if c["shot"] == jid]

def checks(f: Path, jid: str) -> dict:
    p = probe(f)
    out = {"file": str(f.relative_to(R)), "probe": p, "issues": []}
    if not p["ok"]: out["issues"].append(p["error"]); return out
    if p["codec"] not in ("h264", "hevc", "vp9", "av1"): out["issues"].append(f"unusual codec {p['codec']}")
    if (p["w"], p["h"]) != (1280, 720): out["issues"].append(f"{p['w']}x{p['h']} (film is 1280x720; will be scaled)")
    pl = placements(jid)
    need = max((c["src_out"] for c in pl), default=0)
    out["planned_max_source_s"] = need
    if p["duration"] + 1e-3 < need: out["issues"].append(f"A2 file {p['duration']:.2f}s shorter than planned range end {need:.2f}s")
    # A3 frozen frames: fraction of frames mpdecimate would drop (near-identical to previous)
    r = sh("ffmpeg", "-v", "info", "-i", str(f), "-vf", "mpdecimate=hi=200:lo=64:frac=0.33,showinfo", "-an", "-f", "null", "-")
    kept = len(re.findall(r"showinfo.*n:\s*\d+", r.stderr))
    total = round(p["duration"] * p["fps"])
    frozen = max(0.0, 1 - kept / max(1, total))
    out["frozen_share"] = round(frozen, 3)
    if frozen > 0.35: out["issues"].append(f"A3 {frozen*100:.0f}% near-identical frames (check for a freeze)")
    r = sh("ffmpeg", "-v", "info", "-i", str(f), "-vf", "blackdetect=d=0.2:pix_th=0.08", "-an", "-f", "null", "-")
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)
    out["black"] = blacks
    for a, b in blacks:
        for c in pl:
            if float(a) < c["src_out"] and c["src_in"] < float(b): out["issues"].append(f"A3 black {a}-{b}s inside planned range ({c['seg']})")
    out["identity_sheet"] = f"edition20/review/{jid}_identity_4fps.png"
    if p["audio"]:
        r = sh("ffmpeg", "-v", "info", "-i", str(f), "-af", "volumedetect", "-vn", "-f", "null", "-")
        m = re.search(r"mean_volume: ([-\d.]+)", r.stderr); out["embedded_audio_mean_db"] = float(m.group(1)) if m else None
    return out

def swap_scan(f: Path) -> list:
    """Frames (s) where copper-red hair AND navy scrubs both sit right of centre: the role-swap signature."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", "fps=8,scale=320:180", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    try:
        import numpy as np
    except ImportError:
        return ["numpy unavailable: run the scan manually"]
    a = np.frombuffer(raw, np.uint8).reshape(-1, 180, 320, 3).astype(int)
    hits = []
    for i, im in enumerate(a):
        r, g, b = im[..., 0], im[..., 1], im[..., 2]
        mx, mn = im.max(-1), im.min(-1)
        sat = (mx - mn) / np.maximum(mx, 1)
        red = (r > 120) & (r > g * 1.6) & (r > b * 1.8) & (sat > 0.45)
        navy = (b > r * 1.3) & (b > g * 1.05) & (mx < 125) & (mx > 25) & (sat > 0.3)
        rx, nx = np.nonzero(red)[1], np.nonzero(navy)[1]
        if len(rx) > 300 and len(nx) > 1500 and rx.mean() > 190 and nx.mean() > 190:
            hits.append(round(i / 8, 2))
    return hits

def identity_sheet(f: Path, jid: str):
    tmp = Path(tempfile.mkdtemp())
    sh("ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "fps=4,scale=320:-2,drawtext=text='%{pts\\:hms}':x=3:y=3:fontsize=14:fontcolor=yellow:box=1:boxcolor=black",
       "-frames:v", "32", str(tmp / "%02d.png"))
    sh("ffmpeg", "-v", "error", "-y", "-i", str(tmp / "%02d.png"), "-vf", "tile=8x4", "-frames:v", "1", str(REV / f"{jid}_identity_4fps.png"))
    shutil.rmtree(tmp, ignore_errors=True)

def sheet(f: Path, jid: str, info: dict):
    REV.mkdir(parents=True, exist_ok=True)
    d = info["probe"]["duration"]
    times = [0.25 + k * (d - 0.5) / 7 for k in range(8)]
    tmp = Path(tempfile.mkdtemp())
    for k, t in enumerate(times):
        sh("ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(f), "-frames:v", "1", "-vf",
           f"scale=480:-2,drawtext=text='{t:.2f}s':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6", str(tmp / f"{k}.png"))
    sh("ffmpeg", "-v", "error", "-y", "-i", str(tmp / "%d.png"), "-frames:v", "1", "-vf", "tile=4x2", str(tmp / "grid.png"))
    ranges = "  ".join(f"{c['seg']} {c['src_in']:.2f}-{c['src_out']:.2f}s" for c in placements(jid))
    sh("ffmpeg", "-v", "error", "-y", "-i", str(tmp / "grid.png"), "-i", str(REF), "-filter_complex",
       "[1]scale=-2:540[r];[0][r]hstack,drawtext=text='" + f"{jid} {JOBS[jid]['slug']} | ranges used {ranges} | right = hospital.png reference".replace("'", "") +
       "':x=10:y=h-34:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.7", str(REV / f"{jid}_review.png"))
    shutil.rmtree(tmp, ignore_errors=True)

def set_status(jid, status, note, rng=None, crop=None, identity=None):
    m = json.loads(MAN.read_text())
    s = next(x for x in m["shots"] if x["shot_id"] == jid)
    if status == "approved" and not (FLOW / f"{jid}.mp4").exists(): sys.exit(f"{jid}: no file in public/flow; cannot approve")
    s["status"] = status
    if status == "approved" and not identity and not s.get("identity_check"):
        sys.exit(f"{jid}: approval needs --identity 'what was checked' (4 fps sheet vs REF_IVY/REF_NICO_FACE_ONLY: faces, gender, roles)")
    if identity: s["identity_check"] = {"date": str(date.today()), "method": "4 fps visual + swap-signature scan", "result": identity}
    if rng: s["approved_range"] = rng
    if crop: s["default_crop"] = crop
    if status != "approved": s.pop("approved_range", None); s.pop("default_crop", None)
    s.setdefault("review_log", []).append({"date": str(date.today()), "status": status, "note": note})
    MAN.write_text(json.dumps(m, indent=1, ensure_ascii=False))
    subprocess.run([sys.executable, str(R / "tools/film_build.py")], cwd=R)
    report()

def ingest(paths):
    FLOW.mkdir(parents=True, exist_ok=True)
    files = []
    for p in map(Path, paths):
        if p.is_dir(): files += sorted(p.glob("*.mp4"))
        elif p.suffix.lower() == ".zip":
            t = Path(tempfile.mkdtemp())
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.lower().endswith(".mp4") and ".." not in n and not n.startswith("/"): z.extract(n, t)
            files += sorted(t.rglob("*.mp4"))
        else: files.append(p)
    results = {}
    for f in files:
        m = re.search(r"(F\d{2})", f.name.upper())
        if not m or m.group(1) not in JOBS: print(f"SKIP {f.name}: name must contain a job id F01-F70"); continue
        jid = m.group(1)
        exf = R / "edition20/review/exclusions.json"
        excl = {e["job_id"] for e in json.loads(exf.read_text())["excluded"]} if exf.exists() else set()
        if jid in excl and not re.search(rf"{jid}_R\d", f.name.upper()):
            print(f"REFUSED {f.name}: {jid} take 1 is excluded (edition20/review/exclusions.json); only a file named {jid}_R<n> (retake) is accepted")
            continue
        dst = FLOW / f"{jid}.mp4"
        if dst.exists(): shutil.move(str(dst), str(FLOW / f"{jid}.prev_{int(dst.stat().st_mtime)}.mp4"))
        shutil.copy(f, dst)
        info = checks(dst, jid); sheet(dst, jid, info); identity_sheet(dst, jid)
        sw = swap_scan(dst)
        if sw: info["issues"].append(f"A5 POSSIBLE IDENTITY/ROLE SWAP at {sw[:8]} s - quarantine unless a human check clears it")
        results[jid] = info
        print(f"{jid} {JOBS[jid]['slug']}: {info['probe'].get('duration', 0):.2f}s  issues: {info['issues'] or 'none'}  -> edition20/review/{jid}_review.png")
    log = REV / "intake_log.json"
    old = json.loads(log.read_text()) if log.exists() else {}
    old.update(results); log.write_text(json.dumps(old, indent=1))
    subprocess.run([sys.executable, str(R / "tools/film_build.py")], cwd=R)
    report()

def report():
    REV.mkdir(parents=True, exist_ok=True)
    log = json.loads((REV / "intake_log.json").read_text()) if (REV / "intake_log.json").exists() else {}
    m = {s["shot_id"]: s for s in json.loads(MAN.read_text())["shots"]}
    rows = ["# Flow intake review", "", "| Job | Slug | Status | Duration | Frozen | Auto issues | Sheet |", "|---|---|---|---:|---:|---|---|"]
    for jid in sorted(JOBS):
        if jid not in log: continue
        if not (FLOW / f"{jid}.mp4").exists() and m[jid]["status"] == "missing":
            rows.append(f"| {jid} | {JOBS[jid]['slug']} | RETAKE PENDING | - | - | {(m[jid].get('review_log') or [{}])[-1].get('note','')} | {jid}_review.png (rejected take) |"); continue
        i = log[jid]
        st = m[jid]["status"] if m[jid]["status"] != "missing" else "delivered_unreviewed"
        note = (m[jid].get("review_log") or [{}])[-1].get("note", "")
        rows.append(f"| {jid} | {JOBS[jid]['slug']} | {st} | {i['probe'].get('duration', 0):.2f} | {i.get('frozen_share')} | "
                    f"{'; '.join(i['issues']) or 'none'}{' / verdict: ' + note if note else ''} | {jid}_review.png |")
    rows += ["", f"Not delivered yet: {', '.join(j for j in sorted(JOBS) if j not in log)}"]
    (REV / "REVIEW.md").write_text("\n".join(rows) + "\n")

if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    note = args[args.index("--note") + 1] if "--note" in args else ""
    if cmd == "ingest": ingest([a for a in args])
    elif cmd in ("approve", "reject"):
        rng = [float(args[args.index("--range") + 1]), float(args[args.index("--range") + 2])] if "--range" in args else None
        crop = args[args.index("--crop") + 1] if "--crop" in args else None
        ident = args[args.index("--identity") + 1] if "--identity" in args else None
        set_status(args[0], "approved" if cmd == "approve" else "rejected",
                   note + (f" | usable range {rng[0]}-{rng[1]} s" if rng else "") + (f" | crop {crop}" if crop else ""), rng, crop, ident)
    elif cmd == "quarantine":
        jid = args[0]; src = FLOW / f"{jid}.mp4"
        if src.exists():
            (FLOW / "quarantine").mkdir(exist_ok=True)
            shutil.move(str(src), str(FLOW / "quarantine" / f"{jid}_{int(src.stat().st_mtime)}.mp4"))
        set_status(jid, "missing", "QUARANTINED: " + note)
    elif cmd == "retake":
        jid = args[0]; src = FLOW / f"{jid}.mp4"
        if src.exists():
            (FLOW / "rejected").mkdir(exist_ok=True)
            n = len(list((FLOW / "rejected").glob(f"{jid}_take*.mp4"))) + 1
            shutil.move(str(src), str(FLOW / "rejected" / f"{jid}_take{n}.mp4"))
        set_status(jid, "missing", "RETAKE requested: " + note)
    elif cmd == "report": report()

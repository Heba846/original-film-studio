#!/usr/bin/env python3
"""Budget / coverage / gate tests for Film20.  Usage: python3 tools/test_film.py [--render]

Checks the REAL project:
  T1 build has no problems; T2 zero unresolved frames; T3 cuts tile the film with no gap/overlap;
  T4 every footage range sits inside its source window (measured file or the planning estimate), rate 0.85-1,
     and the consumed length matches dur*rate; T5 reuse rules (reason, >3 uses flagged, decisive -> memory,
     no speaking-face frames reused); T6 every referenced job is budgeted and every budgeted job placed, ledger valid;
  T7 the gate is CLOSED now (pickups missing, pictures pending).
Gate simulation in a scratch copy with FAKE media (never copied into the project):
  T8  all 70 fake files + 4 fake pickups present, every job marked approved  -> gate OPEN
  T9  same, one file removed                                                  -> gate CLOSED (approved but not on disk)
  T10 same, one file present but not reviewed (status missing)                -> gate CLOSED (delivered_unreviewed)
  T11 same, one delivered file shorter than its planned range                 -> gate CLOSED (source overrun on measured file)
  T12 same, one edited narration line removed / altered after verification   -> gate CLOSED
--render additionally renders frame 0 of Film20-Final and expects the blocking error.
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok), detail)); print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))

def build(root: Path):
    r = subprocess.run([PY, str(root / "tools/film_build.py")], cwd=root, capture_output=True, text=True)
    return json.loads((root / "src/film/data/film_timeline.json").read_text()), r

# ---------------------------------------------------------------- real project
T, r = build(ROOT)
g = T["gate"]
check("T1 build reports no problems", not g["problems"], "; ".join(g["problems"][:5]))
check("T2 zero unresolved frames", g["unresolved_frames"] == 0, f"{g['unresolved_frames']} frames")
pos, gaps = 0, []
for c in T["cuts"]:
    if c["from"] != pos: gaps.append(c["seg"])
    pos = c["from"] + c["dur"]
check("T3 cuts tile 0..total with no gap/overlap", not gaps and pos == T["total_frames"], f"gaps at {gaps[:5]}, end {pos}/{T['total_frames']}")
bad = []
for c in T["cuts"]:
    if c.get("kind") not in ("footage", "flow_job"): continue
    w = T["shots"][c["shot"]]["window"]
    used = (c["dur"] - c.get("unresolved_f", 0) + c["overlap"]) / T["fps"] * c["rate"]
    if c["src_in"] < w[0] - 1e-6 or c["src_out"] > w[1] + 1e-4: bad.append(f"{c['seg']} {c['shot']} {c['src_in']}-{c['src_out']} not in {w}")
    if not (0.85 - 1e-6 <= c["rate"] <= 1 + 1e-6): bad.append(f"{c['seg']} rate {c['rate']}")
    if abs((c["src_out"] - c["src_in"]) - used) > 0.01: bad.append(f"{c['seg']} {c['shot']} consumed {c['src_out']-c['src_in']:.3f} != {used:.3f}")
check("T4 every source range inside its window; rate 0.85-1; consumption exact", not bad, "; ".join(bad[:5]))
M = json.loads((ROOT / "edition20/media_manifest.json").read_text())
decisive = {s["shot_id"] for s in M["shots"] if s.get("decisive")}
bad = []
for c in T["cuts"]:
    if c.get("is_reuse") and not c.get("why"): bad.append(f"{c['seg']} {c['shot']} reuse without reason")
    if c.get("use_no", 0) > 3 and c.get("is_reuse") and not c.get("flag"): bad.append(f"{c['seg']} {c['shot']} use #{c['use_no']} unflagged")
    if c.get("is_reuse") and c["shot"] in decisive and not c.get("memory") and not c.get("same_moment"): bad.append(f"{c['seg']} decisive {c['shot']} not memory")
    if c.get("is_reuse") and c["shot"] == "HOSP" and c["src_out"] > 5.0 + 1e-6: bad.append(f"{c['seg']} reuses Bay 14 speaking frames")
check("T5 reuse rules (reason, >3 flagged, decisive as memory, no speaking-face reuse)", not bad, "; ".join(bad[:5]))
vb = subprocess.run([PY, str(ROOT / "tools/validate_budget.py")], cwd=ROOT, capture_output=True, text=True)
jobs = {j["job_id"] for j in json.loads((ROOT / "edition20/flow_jobs.json").read_text())["jobs"]}
placed = {c["shot"] for c in T["cuts"] if c.get("kind") == "flow_job"}
check("T6 every placed job budgeted, every budgeted job placed, ledger valid",
      vb.returncode == 0 and placed == jobs and len(jobs) == 70, vb.stdout.strip().splitlines()[-1])
check("T7 Final gate CLOSED now (pictures pending), narration complete", not g["final_export_allowed"] and not g["audio_missing"]
      and g["visual_shots_pending"], f"narration missing {g['audio_missing']}, {len(g['visual_shots_pending'])} shots pending")
prov = json.loads((ROOT / "edition20/pickups/pickup_edits.json").read_text())
check("T7b four edited lines verified; originals untouched",
      sorted(prov["ready"]) == ["n005", "n145", "n148", "n154"] and not prov["blockers"]
      and all(__import__("hashlib").sha256((ROOT / f"public/audio/{k}.wav").read_bytes()).hexdigest() == v["source_sha256"] for k, v in prov["lines"].items()))

# ---------------------------------------------------------------- gate simulation (fake media, scratch copy)
tmp = Path(tempfile.mkdtemp(prefix="film20_gate_"))
try:
    for d in ("tools", "edition20"):
        shutil.copytree(ROOT / d, tmp / d)
    (tmp / "src/film/data").mkdir(parents=True)
    (tmp / "public").mkdir()
    os.symlink(ROOT / "public/audio", tmp / "public/audio")
    os.symlink(ROOT / "public/hospital.mp4", tmp / "public/hospital.mp4")
    (tmp / "public/flow").mkdir(); (tmp / "public/pickups").mkdir()
    proto = tmp / "proto.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=160x90:rate=24", "-t", "7.917", "-pix_fmt", "yuv420p",
                    "-c:v", "libx264", "-preset", "ultrafast", str(proto)], check=True)
    for j in jobs:
        shutil.copy(proto, tmp / f"public/flow/{j}.mp4")
    for p in ("n005", "n145", "n148", "n154"):
        shutil.copy(ROOT / f"public/pickups/{p}_20min.wav", tmp / f"public/pickups/{p}_20min.wav")
    man_p = tmp / "edition20/media_manifest.json"
    base = json.loads(man_p.read_text())
    def with_status(fn):
        m = json.loads(json.dumps(base))
        for s in m["shots"]:
            if s["kind"] == "flow_job": s["status"] = "approved"
        fn(m); man_p.write_text(json.dumps(m))
    with_status(lambda m: None)
    S, _ = build(tmp)
    check("T8 everything present + approved -> gate OPEN", S["gate"]["final_export_allowed"], "; ".join(S["gate"]["problems"][:3]))
    os.remove(tmp / "public/flow/F20.mp4")
    S, _ = build(tmp)
    check("T9 one approved file missing -> gate CLOSED", not S["gate"]["final_export_allowed"] and any("not on disk" in p for p in S["gate"]["problems"]))
    shutil.copy(proto, tmp / "public/flow/F20.mp4")
    with_status(lambda m: next(s for s in m["shots"] if s["shot_id"] == "F20").update(status="missing"))
    S, _ = build(tmp)
    check("T10 delivered but unreviewed -> gate CLOSED", not S["gate"]["final_export_allowed"] and "F20" in S["gate"]["visual_shots_pending"])
    with_status(lambda m: None)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(proto), "-t", "4.0", "-c", "copy", str(tmp / "public/flow/F03.mp4")], check=True)
    S, _ = build(tmp)
    check("T11 delivered file shorter than its planned range -> gate CLOSED",
          not S["gate"]["final_export_allowed"] and (S["gate"]["unresolved_frames"] > 0 or any("measured file" in p for p in S["gate"]["problems"])),
          f"unresolved {S['gate']['unresolved_frames']} f; " + "; ".join(p for p in S["gate"]["problems"] if "F03" in p)[:160])
    shutil.copy(proto, tmp / "public/flow/F03.mp4")
    os.remove(tmp / "public/pickups/n148_20min.wav")
    S, _ = build(tmp)
    check("T12 one edited line missing -> gate CLOSED", not S["gate"]["final_export_allowed"] and "n148" in S["gate"]["audio_missing"])
    shutil.copy(ROOT / "public/pickups/n148_20min.wav", tmp / "public/pickups/n148_20min.wav")
    with open(tmp / "public/pickups/n148_20min.wav", "r+b") as fh:
        fh.seek(5000); fh.write(b"\x00\x10" * 50)
    S, _ = build(tmp)
    check("T12b edited line altered after verification -> gate CLOSED", not S["gate"]["final_export_allowed"]
          and any("changed after verification" in p for p in S["gate"]["problems"]))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
    build(ROOT)  # leave the real timeline rebuilt from real media

if "--render" in sys.argv:
    r = subprocess.run(["npx", "remotion", "render", "src/index.tsx", "Film20-Final", "/tmp/claude-0/should_not_exist.mp4", "--frames=0-0", "--log=error"],
                       cwd=ROOT, capture_output=True, text=True)
    check("T13 rendering Film20-Final fails with the export-gate error", r.returncode != 0 and "export BLOCKED" in (r.stdout + r.stderr))

failed = [n for n, ok, _ in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)

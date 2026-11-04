#!/usr/bin/env python3
"""Measure audio, resolve the explicit cut lists, validate every rule, emit the film timeline.  (v2)

Usage (from remotion_film/):  python3 tools/film_build.py
Outputs:
  src/film/data/audio_measured.json   per-WAV measured facts
  src/film/data/film_timeline.json    frame-accurate timeline (segments + flat cut list) for Remotion
  edition20/out/Film20_captions_DRAFT.srt, Film20_chapters.txt, Film20_chapters.ffmetadata
  edition20/out/STATUS.md             coverage (a/b/c), reuse ledger, review flags, export gate
  edition20/out/coverage_after.json, COVERAGE_BEFORE_AFTER.md

Audio rules: existing_unchanged -> exact WAV at natural speed; needs_pickup -> ONLY public/pickups/<id>_20min.wav,
never the old WAV; a missing pickup keeps the EDL estimate and blocks Final.
Picture rules (see tools/make_manifest.py for the cut-list syntax):
  * every frame 0..total is covered by exactly one cut (no gaps, no overlaps except 6-frame crossfades)
  * a footage cut consumes source = (screen frames + outgoing crossfade) / fps * rate, inside the source window
  * rate is 1.0 when possible, otherwise the slowest needed down to 0.85; below that the remainder is UNRESOLVED
  * planned Flow files are estimates (window 0.2-7.7 of a nominal 7.917 s); delivered files are re-measured
  * reuse = same asset in another chapter, or the same frames shown again; needs a reason; >3 uses needs a flag;
    a decisive action or another date's footage may only return as memory; Bay 14 frames where Ivy's lips part
    (hospital.mp4 >= 5.0 s) never return
"""
from __future__ import annotations
import hashlib, json, math, re, struct, subprocess, sys, wave
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "audio_edit"))
from textnorm import norm, spoken  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FPS = 24
EDL = ROOT / "edition20" / "edit_decision_list.json"
MANIFEST = ROOT / "edition20" / "media_manifest.json"
BEFORE = ROOT / "edition20" / "out" / "coverage_before_v1.json"
DATA = ROOT / "src" / "film" / "data"
OUT = ROOT / "edition20" / "out"
LEAD_IN_S = 0.5
TAIL_S = 3.0
XFADE = 6
MIN_RATE = 0.85
MIN_CUT_F = 12
MAX_USES = 3
REVIEW_GAP_S = 120.0
CHAPTER_PHASE = {"CH00": "P0", "CH01": "P0", "CH02": "P0", "CH03": "P0", "CH04": "P0", "CH05": "P0", "CH06": "P0",
                 "CH07": "P1", "CH08": "P2", "CH09": "P2", "CH10": "P2", "CH11": "P2", "CH12": "P2", "CH13": "P2",
                 "CH14": "P3", "CH16": "P3", "CH17": "P3", "CH18": "P4", "CH19": "P5"}
SEGMENT_PHASE = {"n151": "P4", "n152": "P4", "n154": "P4", "n155": "P4", "n156": "P4", "n157": "P4"}
NO_REUSE_FROM = {"hospital.mp4": 5.0}   # source time after which frames must never be shown again


def measure(path: Path) -> dict:
    raw = path.read_bytes()
    with wave.open(str(path)) as w:
        rate, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        pcm = w.readframes(n)
    peak = 0
    if sw == 2 and pcm:
        vals = struct.unpack(f"<{len(pcm)//2}h", pcm)
        peak = max(abs(v) for v in vals)
    return {"file": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(raw).hexdigest(),
            "sample_rate": rate, "channels": ch, "bits": sw * 8, "frames": n, "duration_s": n / rate,
            "peak_dbfs": round(20 * math.log10(peak / 32768), 2) if peak else None}


def video_len(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    return float(out)


def fr(sec: float) -> int:
    return round(sec * FPS)


def split_caption(text: str, max_chars: int = 84) -> list[str]:
    parts = re.split(r"(?<=[.?!])\s+(?=[\"A-Z0-9])", text.strip())
    cues: list[str] = []
    for p in parts:
        while len(p) > max_chars:
            cut = max(p.rfind(", ", 0, max_chars), p.rfind("; ", 0, max_chars), p.rfind(": ", 0, max_chars))
            if cut < 25:
                cut = p.rfind(" ", 0, max_chars)
            cues.append(p[: cut + 1].strip())
            p = p[cut + 1 :].strip()
        if cues and len(cues[-1]) + len(p) + 1 <= 42:
            cues[-1] += " " + p
        elif p:
            cues.append(p)
    return cues


def two_lines(s: str, width: int = 44) -> str:
    if len(s) <= width:
        return s
    mid = len(s) // 2
    left, right = s.rfind(" ", 0, mid + 1), s.find(" ", mid)
    cut = left if right < 0 or (left >= 0 and mid - left <= right - mid) else right
    return s[:cut] + "\n" + s[cut + 1 :]


def stamp(t: float) -> str:
    ms = round(t * 1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def overlaps(a, b) -> bool:
    return a[0] < b[1] - 1e-6 and b[0] < a[1] - 1e-6


def main() -> int:
    edl = json.loads(EDL.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    variant = None
    if "--variant" in sys.argv:
        variant = json.loads(Path(sys.argv[sys.argv.index("--variant") + 1]).read_text())
        man["segment_cuts"].update(variant["segment_cuts"])
    shots = {s["shot_id"]: s for s in man["shots"]}
    plan_win = man["planned_file"]["usable_window"]
    problems: list[str] = []

    # ---- 0. resolve source windows: delivered files are measured, planned files are estimates
    for sh in shots.values():
        if sh["kind"] in ("footage", "flow_job"):
            f = ROOT / "public" / sh["source"]
            sh["on_disk"] = f.exists()
            if sh["kind"] == "flow_job" and sh["status"] == "missing" and f.exists():
                sh["status"] = "delivered_unreviewed"
            if f.exists() and sh["kind"] == "flow_job" and sh["status"] == "approved" and not sh.get("identity_check"):
                problems.append(f"{sh['shot_id']}: approved without a recorded identity check (faces/gender/roles at 4 fps)")
            if f.exists():
                sh["measured_len_s"] = video_len(f)
                w = sh.get("approved_range") or sh.get("window") or [0.0, sh["measured_len_s"]]
                sh["window"] = [w[0], min(w[1], sh["measured_len_s"])]
                sh["window_is_estimate"] = False
            else:
                sh["window"] = list(plan_win)
                sh["window_is_estimate"] = True
                if sh["status"] == "approved":
                    problems.append(f"{sh['shot_id']}: marked approved but {sh['source']} is not on disk")

    # ---- 1. audio
    measured = {p.stem: measure(p) for p in sorted((ROOT / "public" / "audio").glob("*.wav"))}
    pdir = ROOT / "public" / "pickups"
    pickups = {p.stem.replace("_20min", ""): measure(p) for p in sorted(pdir.glob("*_20min.wav"))} if pdir.exists() else {}
    pickup_warn = []
    for k, m in pickups.items():
        if m["channels"] != 1: pickup_warn.append(f"{k}: {m['channels']} channels (expected mono)")
        if m["sample_rate"] not in (24000, 48000): pickup_warn.append(f"{k}: {m['sample_rate']} Hz (expected 24000)")
        if m["peak_dbfs"] is not None and m["peak_dbfs"] > -0.5: pickup_warn.append(f"{k}: peak {m['peak_dbfs']} dBFS")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "audio_measured.json").write_text(json.dumps({"fps": FPS, "source": measured, "pickups": pickups}, indent=1))

    # ---- 2. segment timing from measured audio; captions on forced-aligned word boundaries when available
    wa_path = OUT / "word_alignment.json"
    WORDS = json.loads(wa_path.read_text())["segments"] if wa_path.exists() else {}
    caption_fallback: list[str] = []
    t = LEAD_IN_S
    segs, cues = [], []
    for s in edl["segments"]:
        sid = s["id"]
        if s["audio_status"] == "existing_unchanged":
            m = measured.get(sid)
            if not m or m["file"] != s["audio_to_use"]:
                problems.append(f"{sid}: expected {s['audio_to_use']} not found"); continue
            dur, audio, a_status = m["duration_s"], m["file"].removeprefix("public/"), "ok"
        elif s["audio_status"] == "edited_existing":
            m = pickups.get(sid)
            prov = json.loads((ROOT / "edition20/pickups/pickup_edits.json").read_text()) if (ROOT / "edition20/pickups/pickup_edits.json").exists() else {}
            if not m or sid not in prov.get("ready", []) or m["file"] != s["audio_to_use"]:
                problems.append(f"{sid}: edited line missing or not verified (pickup_edits.json)")
                dur, audio, a_status = s["planned_audio_duration_seconds"], None, "pickup_missing"
            elif m["sha256"] != prov["lines"][sid].get("output_sha256"):
                problems.append(f"{sid}: edited file changed after verification"); dur, audio, a_status = m["duration_s"], None, "pickup_missing"
            else:
                dur, audio, a_status = m["duration_s"], m["file"].removeprefix("public/"), "edited_existing"
        elif s["audio_status"] == "needs_pickup":
            m = pickups.get(sid)
            if m:
                dur, audio, a_status = m["duration_s"], m["file"].removeprefix("public/"), "pickup_recorded"
            else:
                dur, audio, a_status = s["planned_audio_duration_seconds"], None, "pickup_missing"
        else:
            problems.append(f"{sid}: unknown audio_status"); continue
        pause = float(s["pause_after_seconds"])
        parts = split_caption(s["text"])
        wa = WORDS.get(sid)
        counts = [len(norm(spoken(p, wa["variant"] if wa else 0))) for p in parts]
        if wa and wa["audio"] == (s["audio_to_use"]) and sum(counts) == len(wa["words"]) and a_status != "pickup_missing":
            k = 0
            for i, p in enumerate(parts):
                ws = wa["words"][k: k + counts[i]]; k += counts[i]
                st = t + ws[0][1]
                en = t + ws[-1][2] + 0.25
                if i + 1 < len(parts):
                    en = min(en, t + wa["words"][k][1] - 0.04)
                cues.append({"start": st, "end": max(en, st + 0.5), "text": two_lines(p), "seg": sid, "estimated": False,
                             "timing": "aligned" + (" (partial end)" if wa.get("partial_end") else "")})
        else:
            caption_fallback.append(sid)
            tot = sum(len(p) for p in parts)
            ct = t
            for p in parts:
                d = dur * len(p) / tot
                cues.append({"start": ct, "end": ct + d, "text": two_lines(p), "seg": sid, "estimated": a_status == "pickup_missing",
                             "timing": "proportional"})
                ct += d
        segs.append({"id": sid, "speaker": s["speaker"], "chapter": s["chapter"], "shot": s["shot"], "text": s["text"],
                     "audio_status": a_status, "audio": audio, "audio_duration_s": dur,
                     "duration_is_estimate": a_status == "pickup_missing", "pause_after_s": pause, "start_s": t,
                     "from": fr(t), "dur": max(1, fr(t + dur) - fr(t)), "end_cover": fr(t + dur + pause),
                     "phase": SEGMENT_PHASE.get(sid, CHAPTER_PHASE.get(s["chapter"], "?"))})
        t += dur + pause
    total_s = t + TAIL_S
    total_f = fr(total_s)
    # picture spans tile the whole film: first span starts at 0, last runs to the end
    for i, s in enumerate(segs):
        s["cover_from"] = 0 if i == 0 else segs[i - 1]["cover_from"] + segs[i - 1]["cover_dur"]
        end = total_f if i == len(segs) - 1 else s["end_cover"]
        s["cover_dur"] = end - s["cover_from"]
    chapter_first = {}
    for s in segs:
        chapter_first.setdefault(s["chapter"], s["id"])

    # ---- 3. flatten cuts
    cuts_spec = man["segment_cuts"]
    flat = []
    for s in segs:
        spec = cuts_spec.get(s["id"])
        if not spec:
            problems.append(f"{s['id']}: no cut list"); spec = [{"shot": "UNPLANNED", "secs": "fill"}]
        fixed = sum(fr(c["secs"]) for c in spec if c["secs"] != "fill")
        fills = [c for c in spec if c["secs"] == "fill"]
        if len(fills) > 1: problems.append(f"{s['id']}: more than one fill cut")
        rem = s["cover_dur"] - fixed
        if not fills and rem != 0: problems.append(f"{s['id']}: cuts sum {fixed} f != span {s['cover_dur']} f and no fill")
        acc = s["cover_from"]
        for k, c in enumerate(spec):
            n = rem if c["secs"] == "fill" else fr(c["secs"])
            if n < MIN_CUT_F: problems.append(f"{s['id']}: cut {k} {c['shot']} only {n} f (< {MIN_CUT_F})")
            flat.append({**c, "seg": s["id"], "chapter": s["chapter"], "phase": s["phase"], "from": acc, "dur": n,
                         "chapter_open": k == 0 and chapter_first[s["chapter"]] == s["id"]})
            acc += n
    # gap / overlap test on the timeline itself
    pos = 0
    for c in flat:
        if c["from"] != pos: problems.append(f"timeline gap/overlap at frame {pos} ({c['seg']})")
        pos = c["from"] + c["dur"]
    if pos != total_f: problems.append(f"timeline ends at {pos} f, film is {total_f} f")

    # ---- 4. resolve footage source ranges, reuse, rules
    cursor: dict[tuple, float] = {}
    shown: dict[str, list] = {}          # asset -> [(chapter, (a, b))]
    uses: dict[str, list] = {}           # asset -> [use dicts]
    last_end_s: dict[str, float] = {}
    flags: list[str] = []
    for i, c in enumerate(flat):
        nxt = flat[i + 1] if i + 1 < len(flat) else None
        # dissolve only into/out of code scenes and memories; continuous scenes cut hard; chapters open from black
        # never blend two live-action shots: a footage-to-footage dissolve is a double exposure that ghosts one
        # character's face/body over another's (identity/role morphing). Dissolve only when one side is a code graphic.
        soft = nxt and not nxt["chapter_open"] and (
            shots.get(c["shot"], {}).get("kind") == "code" or shots.get(nxt["shot"], {}).get("kind") == "code")
        c["overlap"] = XFADE if soft else 0
        sh = shots.get(c["shot"])
        if not sh:
            problems.append(f"{c['seg']}: shot {c['shot']} undefined"); c.update(kind="placeholder", status="missing", unresolved_f=c["dur"]); continue
        c["kind"], c["status"] = sh["kind"], sh["status"]
        if sh.get("default_crop") and sh["status"] == "approved":
            c["crop"] = sh["default_crop"]
        c["unresolved_f"] = 0
        asset = sh.get("source") or sh.get("component")
        c["asset"] = asset
        if sh["kind"] in ("footage", "flow_job"):
            w0, w1 = sh["window"]
            inn = c.get("inn")
            if inn is None:
                inn = cursor.get((asset, c["chapter"]), w0)
            if inn < w0 - 1e-6: problems.append(f"{c['seg']} {c['shot']}: in {inn} before window {w0}")
            need = (c["dur"] + c["overlap"]) / FPS
            avail = w1 - inn
            rate = c.get("rate")
            if rate is not None:
                if rate < MIN_RATE - 1e-9 or rate > 1.0 + 1e-9: problems.append(f"{c['seg']} {c['shot']}: rate {rate} outside 0.85-1")
                if inn + need * rate > w1 + 1e-6:
                    problems.append(f"{c['seg']} {c['shot']}: source overrun {inn:.2f}+{need*rate:.2f} > {w1:.2f}"
                                    + (" (estimate)" if sh["window_is_estimate"] else " (measured file)"))
            else:
                if avail <= 0:
                    rate, play = MIN_RATE, 0.0
                elif avail >= need:
                    rate = 1.0
                elif avail / need >= MIN_RATE:
                    rate = math.floor(avail / need * 10000) / 10000
                else:
                    rate = MIN_RATE
            covered_f = max(0.0, avail) / rate * FPS + 1e-6     # frames of screen time the window can supply
            if covered_f >= c["dur"] + c["overlap"]:
                pass
            elif covered_f >= c["dur"]:                          # runs out inside its own dissolve: shorten the dissolve
                c["dissolve_trimmed_from"] = c["overlap"]
                c["overlap"] = int(covered_f - c["dur"])
            else:                                                # runs out on screen: the rest is UNRESOLVED
                c["unresolved_f"] = math.ceil(c["dur"] - covered_f)
                c["overlap"] = 0
            c["src_in"], c["rate"] = round(inn, 4), round(rate, 4)
            c["src_out"] = round(inn + (c["dur"] - c["unresolved_f"] + c["overlap"]) / FPS * rate, 4)
            cursor[(asset, c["chapter"])] = c["src_out"]
            rng = (c["src_in"], c["src_out"])
            if asset in NO_REUSE_FROM and rng[1] > NO_REUSE_FROM[asset] + 1e-6:
                c["no_reuse_range"] = True
        else:
            rng = None
        # use / reuse classification
        prev = shown.get(asset, [])
        same_ch = [r for ch, r in prev if ch == c["chapter"]]
        new_use = not prev or not same_ch or (rng and any(overlaps(rng, r) for r in same_ch))
        if sh["kind"] == "code" and prev and same_ch:
            new_use = False
        if new_use:
            uses.setdefault(asset, []).append({"seg": c["seg"], "chapter": c["chapter"], "why": c.get("why"), "flag": c.get("flag"),
                                                "memory": bool(c.get("memory")), "shot": c["shot"]})
        c["use_no"] = len(uses.get(asset, []))
        if new_use and c["use_no"] > 1:
            c["is_reuse"] = True
            if not c.get("why"): problems.append(f"{c['seg']} {c['shot']}: reuse #{c['use_no']} without a reason")
            unseen = rng is not None and not any(overlaps(rng, r) for _, r in prev)
            if c.get("same_moment") and not unseen:
                problems.append(f"{c['seg']} {c['shot']}: same_moment re-entry must use frames not shown before")
            if sh.get("decisive") and not c.get("memory") and not (c.get("same_moment") and unseen):
                problems.append(f"{c['seg']} {c['shot']}: decisive action reused without memory treatment")
            if rng and any(r[1] > NO_REUSE_FROM.get(asset, 1e9) for r in [rng]) and asset in NO_REUSE_FROM:
                problems.append(f"{c['seg']} {c['shot']}: reuses frames where a face is speaking")
            if c["use_no"] > MAX_USES and not c.get("flag"):
                problems.append(f"{c['seg']} {c['shot']}: use #{c['use_no']} of {asset} exceeds {MAX_USES} without a flag")
            elif c["use_no"] > MAX_USES:
                flags.append(f"{c['seg']} {asset}: use #{c['use_no']} (> {MAX_USES}) — {c['flag']}")
            t_now = c["from"] / FPS
            if asset in last_end_s and t_now - last_end_s[asset] < REVIEW_GAP_S and sh["kind"] != "code":
                flags.append(f"{c['seg']} {asset}: returns {t_now - last_end_s[asset]:.0f} s after its last use — check it does not feel repetitive")
        if sh["kind"] in ("footage", "flow_job"):
            ph = sh.get("continuity_phase")
            if ph and ph not in ("-", c["phase"]) and not c.get("memory"):
                problems.append(f"{c['seg']} {c['shot']}: {ph} footage in a {c['phase']} scene without memory treatment")
        shown.setdefault(asset, []).append((c["chapter"], rng or (0, 0)))
        last_end_s[asset] = (c["from"] + c["dur"]) / FPS
    for a, us in uses.items():
        if len(us) >= MAX_USES:
            flags.append(f"{a}: {len(us)} uses ({', '.join(u['seg'] for u in us)}) — review as a sequence")

    # ---- 5. coverage accounting
    cov = {"approved_on_disk": 0, "code_authored": 0, "planned_primary": 0, "planned_reuse": 0,
           "delivered_unreviewed": 0, "unresolved": 0}
    seg_cov: dict[str, dict] = {}
    for c in flat:
        sc = seg_cov.setdefault(c["seg"], {k: 0 for k in cov})
        unres = c.get("unresolved_f", 0)
        body = c["dur"] - unres
        st, kind = c.get("status"), c.get("kind")
        if kind == "code":
            key = "code_authored"
        elif st == "approved":
            key = "approved_on_disk"
        elif st == "delivered_unreviewed":
            key = "delivered_unreviewed"
        elif st == "missing" and kind == "flow_job":
            key = "planned_reuse" if c.get("is_reuse") else "planned_primary"
        else:
            key, body, unres = "unresolved", 0, c["dur"]
        cov[key] += body; sc[key] += body
        cov["unresolved"] += unres; sc["unresolved"] += unres
    if sum(cov.values()) != total_f: problems.append(f"coverage frames {sum(cov.values())} != film {total_f}")

    used_jobs = sorted({c["shot"] for c in flat if c.get("kind") == "flow_job"})
    all_jobs = sorted(k for k, v in shots.items() if v["kind"] == "flow_job")
    unused_jobs = sorted(set(all_jobs) - set(used_jobs))
    if unused_jobs: problems.append(f"budgeted jobs never placed on the timeline: {unused_jobs}")
    vis_pending = sorted({c["shot"] for c in flat if c.get("status") not in ("approved", "code")})
    audio_missing = [s["id"] for s in segs if s["audio_status"] == "pickup_missing"]
    final_ok = not audio_missing and not vis_pending and not problems and cov["unresolved"] == 0

    chapters = []
    for ch in edl["chapters"]:
        ids = [x for x in segs if x["chapter"] == ch["id"]]
        if ids:
            chapters.append({"id": ch["id"], "title": ch["title"], "start_s": ids[0]["start_s"], "from": ids[0]["cover_from"],
                             "end_from": ids[-1]["cover_from"] + ids[-1]["cover_dur"]})
    for s in segs:
        s["from_audio"] = s["from"]
    keep = ("seg", "chapter", "from", "dur", "shot", "slug", "same_moment", "dissolve_trimmed_from", "kind", "status", "asset", "src_in", "src_out", "rate", "overlap",
            "unresolved_f", "memory", "crop", "beat", "stage", "use_no", "is_reuse", "why", "flag", "chapter_open")
    timeline = {
        "fps": FPS, "width": 1280, "height": 720, "lead_in_s": LEAD_IN_S, "total_s": total_s, "total_frames": total_f,
        "runtime_is_estimate": bool(audio_missing),
        "segments": [{k: s[k] for k in ("id", "speaker", "chapter", "text", "audio_status", "audio", "audio_duration_s",
                                        "duration_is_estimate", "pause_after_s", "start_s", "from", "dur", "cover_from",
                                        "cover_dur", "phase")} for s in segs],
        "cuts": [{k: c[k] for k in keep if k in c} for c in flat],
        "chapters": chapters, "captions": cues,
        "shots": {k: {kk: v.get(kk) for kk in ("kind", "source", "status", "component", "narrative_event", "window",
                                                "window_is_estimate", "on_disk")} for k, v in shots.items()},
        "coverage_frames": cov,
        "gate": {"final_export_allowed": final_ok, "audio_missing": audio_missing, "visual_shots_pending": vis_pending,
                 "unresolved_frames": cov["unresolved"], "problems": problems},
    }
    if variant:
        ids = [x["id"] for x in segs]
        a0, a1 = ids.index(variant["segments"][0]), ids.index(variant["segments"][1])
        rng = set(ids[a0:a1 + 1])
        vcuts = [c for c in timeline["cuts"] if c["seg"] in rng]
        not_real = [f"{c['seg']} {c['shot']} ({c.get('status')})" for c in vcuts
                    if not (c.get("kind") == "code" or c.get("status") == "approved") or c.get("unresolved_f")]
        vprob = [p for p in problems if any(p.startswith(i) for i in rng)]
        timeline["variant"] = {"tag": variant["tag"], "segments": variant["segments"], "start": vcuts[0]["from"],
                               "end": vcuts[-1]["from"] + vcuts[-1]["dur"], "not_real_picture": not_real, "problems": vprob,
                               "approved_only": not not_real and not vprob}
        (DATA / f"film_timeline_{variant['tag']}.json").write_text(json.dumps(timeline, indent=1))
        v = timeline["variant"]
        print(f"variant {v['tag']}: {(v['end']-v['start'])/FPS:.2f} s, approved-only: {v['approved_only']}")
        for x in not_real + vprob: print("  NOT REAL / PROBLEM:", x)
        return 0 if v["approved_only"] else 2
    (DATA / "film_timeline.json").write_text(json.dumps(timeline, indent=1))

    # ---- 6. sidecars
    OUT.mkdir(parents=True, exist_ok=True)
    srt = [f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}"
           + ("  [PICKUP NOT RECORDED – TIMING ESTIMATED]" if c["estimated"] else "") + "\n" for i, c in enumerate(cues, 1)]
    for old in OUT.glob("Film20_captions*.srt"): old.unlink()
    (OUT / ("Film20_captions.srt" if final_ok else "Film20_captions_DRAFT.srt")).write_text("\n".join(srt), encoding="utf-8")
    (OUT / "Film20_chapters.txt").write_text("\n".join(
        f"{int((0 if i == 0 else c['start_s'])//60):02}:{int((0 if i == 0 else c['start_s'])%60):02} {c['title']}"
        for i, c in enumerate(chapters)) + "\n", encoding="utf-8")
    meta = [";FFMETADATA1"]
    for i, c in enumerate(chapters):
        end = chapters[i + 1]["start_s"] if i + 1 < len(chapters) else total_s
        meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={round((0 if i == 0 else c['start_s'])*1000)}",
                 f"END={round(end*1000)}", f"title={c['title']}"]
    (OUT / "Film20_chapters.ffmetadata").write_text("\n".join(meta) + "\n", encoding="utf-8")

    # ---- 7. reports
    S = lambda f: f / FPS
    pct = lambda f: f"{S(f):7.1f} s  {f/total_f*100:5.1f}%"
    after = {sid: {k: round(S(v), 2) for k, v in d.items()} for sid, d in seg_cov.items()}
    (OUT / "coverage_after.json").write_text(json.dumps({"total_s": round(total_s, 2), "coverage_s": {k: round(S(v), 2) for k, v in cov.items()},
                                                          "segments": after}, indent=1))
    reuse_rows = []
    for a, us in sorted(uses.items()):
        for n, u in enumerate(us, 1):
            if n > 1:
                reuse_rows.append(f"| {a} | {n} | {u['seg']} ({u['chapter']}) | {'memory' if u['memory'] else 'direct'} | {u['why'] or '—'} |")
    mmss = lambda x: f"{int(x//60)}:{x%60:05.2f}"
    speech = sum(x["audio_duration_s"] for x in segs if x["audio_status"] != "pickup_missing")
    est = sum(x["audio_duration_s"] for x in segs if x["audio_status"] == "pickup_missing")
    lines = [
        "# Film20 build status (generated by tools/film_build.py — do not edit by hand)", "",
        f"- Runtime: **{mmss(total_s)}** ({total_s:.2f} s, {total_f} frames @ {FPS} fps)"
        + (" — ESTIMATE: includes unrecorded pickups at EDL estimates" if audio_missing else " — measured"),
        f"- Speech in measured WAVs: {speech:.3f} s; pickup estimates: {est:.3f} s; pauses {sum(x['pause_after_s'] for x in segs):.2f} s; lead-in {LEAD_IN_S} s + tail {TAIL_S} s",
        f"- Final export allowed: **{'YES' if final_ok else 'NO'}**", "",
        "## Picture coverage (every frame counted once; crossfade overlaps counted as source use only)",
        "| | Seconds | Share |", "|---|---:|---:|",
        f"| (a) approved footage on disk | {S(cov['approved_on_disk']):.1f} | {cov['approved_on_disk']/total_f*100:.1f}% |",
        f"| (a) authored code scenes (finished) | {S(cov['code_authored']):.1f} | {cov['code_authored']/total_f*100:.1f}% |",
        f"| (b) conditional: planned Flow job, first use | {S(cov['planned_primary']):.1f} | {cov['planned_primary']/total_f*100:.1f}% |",
        f"| (b) conditional: planned Flow job, motivated reuse | {S(cov['planned_reuse']):.1f} | {cov['planned_reuse']/total_f*100:.1f}% |",
        f"| delivered but not yet reviewed | {S(cov['delivered_unreviewed']):.1f} | {cov['delivered_unreviewed']/total_f*100:.1f}% |",
        f"| **(c) unresolved / unplanned** | **{S(cov['unresolved']):.1f}** | **{cov['unresolved']/total_f*100:.1f}%** |", "",
        "(b) assumes every job is delivered as an ~7.9 s file, passes review and the 0.2-7.7 s window is usable. "
        "It is NOT delivered picture.", "",
        "## Missing narration (pickups)", *([f"- {a} -> public/pickups/{a}_20min.wav" for a in audio_missing] or ["- none"]), "",
        f"## Shots still required before Final ({len(vis_pending)})", ", ".join(vis_pending), "",
        f"## Reuse ledger ({len(reuse_rows)} reuse occurrences)", "| Asset | Use # | Where | Treatment | Narrative reason |",
        "|---|---:|---|---|---|", *reuse_rows, "",
        "## Review flags", *([f"- {f}" for f in flags] or ["- none"]), "",
        "## Unresolved cuts", *([f"- {c['seg']} {c['shot']} {c.get('slug','')}: {S(c['unresolved_f']):.2f} s" for c in flat if c.get('unresolved_f')] or ["- none"]), "",
        "## Dissolves shortened because the source ends inside them (cut stays fully covered)",
        *([f"- {c['seg']} {c['shot']} {c.get('slug','')}: {c['dissolve_trimmed_from']} -> {c['overlap']} frames" for c in flat if 'dissolve_trimmed_from' in c] or ["- none"]), "",
        "## Caption timing", f"- {len(segs) - len(caption_fallback)} of {len(segs)} lines timed on forced-aligned word boundaries"
        + (f"; proportional fallback: {', '.join(caption_fallback)}" if caption_fallback else "")
        + "; partial end (last words share one aligned span, listen to confirm): "
        + (", ".join(k for k, v in WORDS.items() if v.get("partial_end")) or "none"), "",
        "## Pickup format warnings", *([f"- {w}" for w in pickup_warn] or ["- none"]), "",
        "## Problems (each blocks Final)", *([f"- {p}" for p in problems] or ["- none"]),
    ]
    (OUT / "STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if BEFORE.exists():
        b = json.loads(BEFORE.read_text())
        segl = {s["id"]: s for s in segs}
        rows = ["# Coverage before / after (v1 shortfall blocks + U01)", "",
                f"Before: v1 plan, {b['total_short_s']} s short over {len(b['blocks'])} blocks, plus U01 unbudgeted. "
                f"After: v2 cut lists (seconds per segment; (b) = conditional on delivery+approval). The 'v1 short block' "
                f"column uses v1 job numbers (v1 F03 is not v2 F03; see `replaces` in flow_jobs.json).", "",
                "| Segment | Span s | v1 short block | v1 short s | v2 approved | v2 code | v2 planned 1st use | v2 planned reuse | v2 unresolved |",
                "|---|---:|---|---:|---:|---:|---:|---:|---:|"]
        seen = set()
        for r in b["blocks"] + [{"segment": "n109", "shot": "U01 (unbudgeted)", "short_s": "n/a"}]:
            a = after.get(r["segment"], {})
            rows.append(f"| {r['segment']} | {S(segl[r['segment']]['cover_dur']):.2f} | {r['shot']} | {r['short_s']} | "
                        f"{a.get('approved_on_disk',0)} | {a.get('code_authored',0)} | {a.get('planned_primary',0)} | "
                        f"{a.get('planned_reuse',0)} | **{a.get('unresolved',0)}** |")
            seen.add(r["segment"])
        tot_unres = sum(a.get("unresolved", 0) for k, a in after.items() if k in seen)
        heavy = [f"{k} ({a['planned_reuse']:.1f} of {sum(a.values()):.1f} s)" for k, a in after.items()
                 if sum(a.values()) > 0 and a["planned_reuse"] / sum(a.values()) > 0.6]
        rows += ["", f"Unresolved in these segments after correction: **{tot_unres:.2f} s**. Whole film unresolved: "
                     f"**{S(cov['unresolved']):.2f} s**.", "",
                 "Segments carried mostly (>60%) by reuse — review first once footage exists: " + (", ".join(heavy) or "none")]
        (OUT / "COVERAGE_BEFORE_AFTER.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

    print("\n".join(lines[2:15]))
    print(f"problems: {len(problems)}  flags: {len(flags)}")
    for p in problems[:60]: print("  P", p)
    return 0 if not problems else 2


if __name__ == "__main__":
    sys.exit(main())

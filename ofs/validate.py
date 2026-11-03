"""Pre-render validation of files and timing. Errors block rendering."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import clips as clips_mod, media, project as proj, srt as srtlib

MAX_SHOT = 600.0
PRESETS = {"ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"}


@dataclass
class Issue:
    level: str  # error | warning | info
    code: str
    message: str
    shot: str | None = None

    def to_dict(self):
        return {"level": self.level, "code": self.code, "message": self.message, "shot": self.shot}


@dataclass
class Report:
    issues: list = field(default_factory=list)
    total_duration: float = 0.0

    def add(self, level, code, message, shot=None):
        self.issues.append(Issue(level, code, message, shot))

    @property
    def errors(self):
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.level == "warning"]

    @property
    def ok(self):
        return not self.errors

    def codes(self):
        return [i.code for i in self.issues]

    def to_dict(self):
        return {"ok": self.ok, "total_duration": self.total_duration,
                "errors": len(self.errors), "warnings": len(self.warnings),
                "issues": [i.to_dict() for i in self.issues]}


def _num(v):
    if isinstance(v, bool):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _segments(project, base, r, probe, timing, total):
    segs = project["narration_segments"]
    speakers = {x["id"]: x for x in project["speakers"]}
    sp_ids = [x["id"] for x in project["speakers"]]
    if len(set(sp_ids)) != len(sp_ids) or "" in sp_ids:
        r.add("error", "bad_speaker_ids", "Speaker ids must be non-empty and unique.")
    if not segs:
        r.add("error", "no_segments", "Narration mode is 'segments' but there are no segments.")
        return
    seen, measured_total, all_ok = set(), 0.0, True
    for i, g in enumerate(segs, 1):
        gid = g["id"] or f"#{i}"
        if not g["id"]:
            r.add("error", "segment_no_id", f"Segment #{i} has no id.", gid)
        elif g["id"] in seen:
            r.add("error", "segment_dup_id", f"Duplicate segment id '{g['id']}'.", gid)
        seen.add(g["id"])
        if g["speaker"] not in speakers:
            r.add("error", "unknown_speaker", f"Segment {gid}: speaker '{g['speaker']}' is not defined.", gid)
        if not (g["text"] or "").strip():
            r.add("error", "segment_no_text", f"Segment {gid}: text is empty.", gid)
        pa = _num(g["pause_after"])
        if pa is None or pa < 0 or pa > 30:
            r.add("error", "bad_pause", f"Segment {gid}: pause_after must be 0-30 seconds.", gid)
            pa = 0.0
        if g["source"] not in ("imported", "generated"):
            r.add("error", "bad_source", f"Segment {gid}: source must be 'imported' or 'generated'.", gid)
        if g["editorial"]:
            r.add("info", "editorial_proposal", f"Segment {gid} is an EDITORIAL PROPOSAL awaiting the author's approval.", gid)
        if not g["audio"]:
            r.add("error", "segment_no_audio", f"Segment {gid}: no audio yet (import a WAV/MP3 or generate it).", gid)
            all_ok = False
            continue
        p = proj.resolve(base, g["audio"])
        if not p.is_file():
            r.add("error", "segment_missing_audio", f"Segment {gid}: audio file not found: {g['audio']}", gid)
            all_ok = False
        elif p.suffix.lower() not in media.AUDIO_EXT:
            r.add("error", "bad_segment_audio_type", f"Segment {gid}: not an audio file.", gid)
            all_ok = False
        else:
            info = probe(p, "unreadable_segment_audio", f"Segment {gid} audio", gid)
            if not info or not info["has_audio"] or not info["duration"]:
                if info:
                    r.add("error", "segment_no_audio_stream", f"Segment {gid}: file has no audio.", gid)
                all_ok = False
            else:
                measured_total += info["duration"] + pa
    # segment -> shot references
    sids = set(seen)
    owner = {}
    for s in project["shots"]:
        for x in s["segments"]:
            if x not in sids:
                r.add("error", "unknown_segment", f"Shot {s['id']}: segment '{x}' does not exist.", s["id"])
            elif x in owner:
                r.add("error", "segment_in_two_shots", f"Segment '{x}' is assigned to shots {owner[x]} and {s['id']}.", s["id"])
            owner[x] = s["id"]
    order = [g["id"] for g in segs]
    flat = [x for s in project["shots"] for x in s["segments"] if x in sids]
    if flat != sorted(flat, key=order.index):
        r.add("warning", "segment_order", "Shots reference narration segments out of order.")
    if all_ok:
        timing(measured_total)
        for s in project["shots"]:
            span = 0.0
            for x in s["segments"]:
                g = next((g for g in segs if g["id"] == x), None)
                if g:
                    try:
                        span += probe(proj.resolve(base, g["audio"]), "unreadable_segment_audio", x)["duration"] + (_num(g["pause_after"]) or 0)
                    except Exception:  # noqa: BLE001
                        pass
            d = _num(s["duration"])
            if span and d and d < span - 0.3:
                r.add("warning", "shot_shorter_than_narration",
                      f"Shot {s['id']} lasts {d:g}s but its narration needs {span:.1f}s; run 'sync' to fit shots to the audio.", s["id"])


def validate(project: dict, base, probe_fn=media.probe, check_tools: bool = True) -> Report:
    project = proj.normalize(project)
    base = Path(base)
    r = Report()
    r.total_duration = proj.total_duration(project)

    have_probe = True
    if check_tools:
        for n in ("ffmpeg", "ffprobe"):
            if not media.tool(n):
                r.add("error", "tool_missing", f"{n} not found. Install FFmpeg and add it to PATH.")
                have_probe = False

    def probe(path, code, label, shot=None):
        if not have_probe:
            return None
        try:
            return probe_fn(path)
        except Exception as e:  # noqa: BLE001
            r.add("error", code, f"{label} is unreadable or not valid media: {e}", shot)
            return None

    char_ids = {c["id"] for c in project["characters"]}
    loc_ids = {l["id"] for l in project["locations"]}
    if len(char_ids) != len(project["characters"]) or "" in char_ids:
        r.add("error", "bad_character_ids", "Character ids must be non-empty and unique.")
    if len(loc_ids) != len(project["locations"]) or "" in loc_ids:
        r.add("error", "bad_location_ids", "Location ids must be non-empty and unique.")

    shots = project["shots"]
    if not shots:
        r.add("error", "no_shots", "The shot list is empty.")
    seen = set()
    for idx, s in enumerate(shots, 1):
        sid = s["id"] or f"#{idx}"
        if not s["id"]:
            r.add("error", "shot_no_id", f"Shot #{idx} has no id.", sid)
        elif s["id"] in seen:
            r.add("error", "shot_dup_id", f"Duplicate shot id '{s['id']}'.", sid)
        seen.add(s["id"])

        d = _num(s["duration"])
        if d is None or d <= 0:
            r.add("error", "bad_duration", f"Shot {sid}: duration must be a number > 0 (got {s['duration']!r}).", sid)
            d = None
        elif d > MAX_SHOT:
            r.add("error", "duration_too_long", f"Shot {sid}: duration {d}s exceeds {MAX_SHOT:.0f}s.", sid)
        elif d < 0.5:
            r.add("warning", "duration_very_short", f"Shot {sid}: {d}s is shorter than 0.5s.", sid)
        ts = _num(s["trim_start"])
        if ts is None or ts < 0:
            r.add("error", "bad_trim", f"Shot {sid}: trim_start must be >= 0.", sid)
            ts = 0.0

        kind = s["kind"]
        if kind not in ("image", "video"):
            r.add("error", "bad_kind", f"Shot {sid}: kind must be 'image' or 'video'.", sid)
        if s["motion"] not in proj.MOTIONS:
            r.add("error", "bad_motion", f"Shot {sid}: motion must be one of {proj.MOTIONS}.", sid)
        if s["transition"] not in proj.TRANSITIONS:
            r.add("error", "bad_transition", f"Shot {sid}: transition must be one of {proj.TRANSITIONS}.", sid)

        asset = s["asset"]
        shot_clips = clips_mod.discover(s, base) if kind == "video" else []
        if shot_clips:
            for cp in shot_clips:
                if not cp.is_file():
                    r.add("error", "missing_file", f"Shot {sid}: clip not found: {cp}", sid)
                    continue
                cinfo = probe(cp, "unreadable_media", f"Shot {sid} clip {cp.name}", sid)
                if cinfo and not cinfo["has_video"]:
                    r.add("error", "no_video_stream", f"Shot {sid}: {cp.name} has no picture.", sid)
            pl_ = None
            if d:
                durs_ = []
                for cp in shot_clips:
                    try:
                        durs_.append(float(media.probe(cp)["duration"] or 0))
                    except Exception:  # noqa: BLE001
                        pass
                pl_ = clips_mod.plan_shot(d, durs_)
            if pl_ and pl_["reused_seconds"] > 0.5:
                r.add("warning", "clips_reused",
                      f"Shot {sid}: {pl_['reused_seconds']:.0f}s of {d:g}s repeats footage "
                      f"({len(shot_clips)} clip(s); speed {pl_['speed']:.2f}x). Supply more clips to avoid repeats.", sid)
        elif not asset:
            r.add("error", "no_asset", f"Shot {sid}: no image/video file assigned.", sid)
        else:
            p = proj.resolve(base, asset)
            ext = p.suffix.lower()
            if not p.is_file():
                r.add("error", "missing_file", f"Shot {sid}: file not found: {asset}", sid)
            elif kind in ("image", "video"):
                allowed = media.IMAGE_EXT if kind == "image" else media.VIDEO_EXT
                other = media.VIDEO_EXT if kind == "image" else media.IMAGE_EXT
                if ext in other:
                    r.add("error", "kind_mismatch", f"Shot {sid}: kind is '{kind}' but file looks like "
                          f"{'a video' if kind == 'image' else 'an image'} ({ext}).", sid)
                elif ext not in allowed:
                    r.add("error", "bad_extension", f"Shot {sid}: unsupported file type '{ext}'.", sid)
                else:
                    info = probe(p, "unreadable_media", f"Shot {sid} file", sid)
                    if info:
                        if not info["has_video"]:
                            r.add("error", "no_video_stream", f"Shot {sid}: file has no picture.", sid)
                        elif not info["width"] or not info["height"]:
                            r.add("error", "unreadable_media", f"Shot {sid}: file is corrupt or not valid media.", sid)
                        else:
                            w, h = info["width"] or 0, info["height"] or 0
                            if w < 1280 or h < 720:
                                r.add("warning", "low_resolution", f"Shot {sid}: {w}x{h} will be upscaled to 1080p.", sid)
                            if h and abs(w / h - 16 / 9) > 0.02:
                                r.add("warning", "aspect_ratio", f"Shot {sid}: {w}x{h} is not 16:9; "
                                      "it will be letterboxed/pillarboxed with black bars.", sid)
                            if kind == "video" and d and info["duration"] is not None \
                                    and info["duration"] < ts + d - 0.1:
                                r.add("warning", "clip_too_short",
                                      f"Shot {sid}: clip has {max(info['duration'] - ts, 0):.1f}s after trim but the shot "
                                      f"is {d:g}s; the last frame will be held.", sid)

        for c in s["characters"]:
            if c not in char_ids:
                r.add("error", "unknown_character", f"Shot {sid}: character '{c}' is not in the bible.", sid)
        if s["location"] and s["location"] not in loc_ids:
            r.add("error", "unknown_location", f"Shot {sid}: location '{s['location']}' is not in the bible.", sid)
        text = f"{s['action']} {s['dialogue']}".lower()
        for c in project["characters"]:
            nm = (c["name"] or "").strip().lower()
            cid = (c["id"] or "").strip().lower()
            hit = (len(nm) >= 3 and nm in text) or (len(cid) >= 3 and re.search(r"\b" + re.escape(cid) + r"\b", text))
            if hit and c["id"] not in s["characters"]:
                r.add("warning", "untagged_character",
                      f"Shot {sid}: mentions '{c['name']}' but the character is not tagged on the shot "
                      "(continuity notes won't be added to its prompts).", sid)

    total = r.total_duration
    a = project["audio"]
    for key in ("narration_volume", "music_volume"):
        v = _num(a.get(key))
        if v is None or not 0 <= v <= 4:
            r.add("error", "bad_volume", f"audio.{key} must be a number between 0 and 4.")

    def timing(nd):
        if nd > total + 0.5:
            r.add("error", "narration_longer", f"Narration is {nd:.1f}s but the timeline is only "
                  f"{total:.1f}s; it would be cut off. Lengthen shots or trim the audio.")
        elif total > nd + 3:
            r.add("warning", "narration_shorter", f"Narration ends {total - nd:.1f}s before the picture "
                  f"({nd:.1f}s vs {total:.1f}s).")

    if a["narration_mode"] not in ("file", "segments"):
        r.add("error", "bad_narration_mode", "audio.narration_mode must be 'file' or 'segments'.")
    elif a["narration_mode"] == "segments":
        _segments(project, base, r, probe, timing, total)
    elif a["narration"]:
        p = proj.resolve(base, a["narration"])
        if not p.is_file():
            r.add("error", "missing_narration", f"Narration file not found: {a['narration']}")
        elif p.suffix.lower() not in media.AUDIO_EXT:
            r.add("error", "bad_narration_type", f"Narration must be an audio file ({', '.join(sorted(media.AUDIO_EXT))}).")
        else:
            info = probe(p, "unreadable_narration", "Narration")
            if info:
                if not info["has_audio"] or info["duration"] is None:
                    r.add("error", "narration_no_audio", "Narration file has no audio stream.")
                else:
                    timing(info["duration"])
    else:
        r.add("info", "no_narration", "No narration imported; the render will have no voice track.")
    if project["narration_segments"] and a["narration_mode"] == "file":
        r.add("info", "segments_unused", "Narration segments exist but audio.narration_mode is 'file'; they are not used.")

    if a["music"]:
        p = proj.resolve(base, a["music"])
        if not p.is_file():
            r.add("error", "missing_music", f"Music file not found: {a['music']}")
        elif p.suffix.lower() not in media.AUDIO_EXT:
            r.add("error", "bad_music_type", "Music must be an audio file.")
        else:
            info = probe(p, "unreadable_music", "Music")
            if info and not info["has_audio"]:
                r.add("error", "music_no_audio", "Music file has no audio stream.")

    c = project["captions"]
    if c["mode"] not in ("none", "burn", "soft"):
        r.add("error", "bad_caption_mode", "captions.mode must be none, burn or soft.")
    elif c["mode"] != "none" and not c["srt"]:
        r.add("error", "no_srt", f"Captions mode is '{c['mode']}' but no SRT file is set.")
    if c["srt"]:
        p = proj.resolve(base, c["srt"])
        if not p.is_file():
            r.add("error", "missing_srt", f"SRT file not found: {c['srt']}")
        else:
            try:
                cues, errs = srtlib.parse(p.read_text(encoding="utf-8-sig"))
            except UnicodeDecodeError:
                cues, errs = [], ["file is not UTF-8 text (re-save the SRT as UTF-8)"]
            for e in errs:
                r.add("error", "srt_invalid", f"SRT problem: {e}")
            if not cues and not errs:
                r.add("error", "srt_empty", "SRT file contains no captions.")
            for i, cue in enumerate(cues):
                if cue["end"] > total + 0.5:
                    r.add("warning", "srt_beyond_timeline",
                          f"Caption {cue['index']} ends at {cue['end']:.1f}s, after the film ({total:.1f}s).")
                if i and cue["start"] < cues[i - 1]["end"] - 0.001:
                    r.add("warning", "srt_overlap", f"Caption {cue['index']} overlaps the previous one.")
            if c["mode"] == "none":
                r.add("info", "srt_unused", "An SRT is set but captions.mode is 'none'; it will not be used.")

    rd = project["render"]
    fps = _num(rd.get("fps"))
    if fps is None or not 1 <= fps <= 120:
        r.add("error", "bad_fps", "render.fps must be between 1 and 120.")
    crf = _num(rd.get("crf"))
    if crf is None or not 0 <= crf <= 51:
        r.add("error", "bad_crf", "render.crf must be between 0 and 51.")
    if rd.get("preset") not in PRESETS:
        r.add("error", "bad_preset", f"render.preset must be one of {sorted(PRESETS)}.")
    return r

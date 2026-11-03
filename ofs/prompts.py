"""Per-shot prompt export for EXTERNAL image/video tools.

Nothing here calls a model. The owner pastes these prompts into whatever tool
they choose, then imports the resulting files back into the shot list.
"""
from __future__ import annotations

import csv
import io

from . import project as proj

NEGATIVE = ("text, subtitles, watermark, logo, extra fingers, deformed hands, "
            "inconsistent face, changing outfit, duplicate characters, blurry, low resolution")

MOTION_TEXT = {
    "none": "locked-off frame",
    "zoom_in": "slow push-in",
    "zoom_out": "slow pull-back",
    "pan_left": "gentle pan left",
    "pan_right": "gentle pan right",
}


def _j(*parts, sep=" "):
    return sep.join(p.strip().rstrip(".") + "." for p in parts if p and p.strip())


def build_prompts(project: dict) -> list:
    project = proj.normalize(project)
    chars = {c["id"]: c for c in project["characters"]}
    locs = {l["id"]: l for l in project["locations"]}
    tl = {sid: (a, b) for sid, a, b in proj.timeline(project)}
    segs = {g["id"]: g for g in project["narration_segments"]}
    spk = {x["id"]: x for x in project["speakers"]}
    out = []
    for n, s in enumerate(project["shots"], 1):
        cs = [chars[c] for c in s["characters"] if c in chars]
        loc = locs.get(s["location"])
        char_txt = " ".join(
            _j(f"{c['name'] or c['id']}: {c['description']}", f"wearing {c['wardrobe']}" if c["wardrobe"] else "")
            for c in cs)
        loc_txt = _j(f"Location: {loc['name']} - {loc['description']}" if loc else "",
                     f"Lighting: {loc['lighting']}" if loc and loc["lighting"] else "")
        image = " ".join(x for x in [
            _j(project["style"]),
            loc_txt, char_txt,
            _j(f"Action: {s['action']}" if s["action"] else ""),
            _j(f"Continuity locks: {s['locks']}" if s["locks"] else ""),
            _j(f"Camera: {s['camera']}" if s["camera"] else ""),
            "16:9 widescreen composition.",
        ] if x)
        dur = s["duration"]
        motion = MOTION_TEXT.get(s["motion"], "")
        video = " ".join(x for x in [
            image,
            f"OPTIONAL motion version (only if you animate this still in an external tool): about {dur} seconds, "
            "subtle natural motion; keep faces, outfits, injuries and set identical to the still.",
            _j(f"Suggested camera movement: {s['camera']}" if s["camera"] else (f"Suggested camera movement: {motion}" if s["motion"] != "none" else "")),
        ] if x)
        notes = []
        for c in cs:
            if c["continuity_notes"]:
                notes.append(f"{c['name'] or c['id']}: {c['continuity_notes']}")
            if c["reference"]:
                notes.append(f"{c['name'] or c['id']} reference: {c['reference']}")
        if loc and loc["continuity_notes"]:
            notes.append(f"{loc['name']}: {loc['continuity_notes']}")
        if s["continuity_notes"]:
            notes.append(f"This shot: {s['continuity_notes']}")
        out.append({
            "order": n, "shot_id": s["id"], "title": s["title"],
            "start": tl[s["id"]][0] if s["id"] in tl else None,
            "duration": dur, "asset_kind_planned": s["kind"],
            "image_prompt": image, "still_prompt": image, "video_prompt": video,
            "optional_motion_prompt": video, "animatic_motion": s["motion"],
            "negative_prompt": NEGATIVE + (", " + s["negative_extra"] if s["negative_extra"] else ""),
            "narration": [{"segment": x, "speaker": (spk.get(segs[x]["speaker"]) or {}).get("display_name") or segs[x]["speaker"],
                           "text": segs[x]["text"], "editorial_proposal": segs[x]["editorial"]}
                          for x in s["segments"] if x in segs],
            "continuity_notes": notes, "dialogue": s["dialogue"],
        })
    return out


def to_markdown(project: dict, prompts: list) -> str:
    lines = [f"# {project.get('title', 'Film')} - shot prompts", "",
             "> Prompts for EXTERNAL tools. Original Film Studio does not generate images or video.", ""]
    for p in prompts:
        lines += [f"## {p['order']}. {p['shot_id']} - {p['title']}  ({p['duration']}s)", "",
                  f"**Image prompt:** {p['image_prompt']}", "",
                  f"**Optional motion prompt:** {p['video_prompt']}", "",
                  f"_Without an external animation tool this shot renders as an animatic (motion: {p['animatic_motion']})._", "",
                  f"**Negative prompt:** {p['negative_prompt']}", ""]
        if p["continuity_notes"]:
            lines.append("**Continuity checklist:**")
            lines += [f"- {n}" for n in p["continuity_notes"]]
            lines.append("")
        for n in p["narration"]:
            lines += [f"**{n['speaker']}:** {n['text']}" + ("  _(editorial proposal)_" if n["editorial_proposal"] else ""), ""]
        if p["dialogue"]:
            lines += [f"**Narration/dialogue line:** {p['dialogue']}", ""]
    return "\n".join(lines)


def to_csv(prompts: list) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["order", "shot_id", "title", "duration", "image_prompt", "video_prompt",
                "negative_prompt", "continuity_notes"])
    for p in prompts:
        w.writerow([p["order"], p["shot_id"], p["title"], p["duration"], p["image_prompt"],
                    p["video_prompt"], p["negative_prompt"], " | ".join(p["continuity_notes"])])
    return buf.getvalue()

"""Pilot project: 'Married to the Don to Keep Me Silent' - 6 shots, 2 speakers (Heba/Ivy, Lion/Nico).

The text below is the author's. NO recordings exist yet: segments have no audio and speakers have no
reference clip, so rendering is blocked until real audio is imported (or locally generated after the
owner supplies consented reference recordings). `dryrun()` builds a clearly-labelled SYNTHETIC check
(tone placeholders + placeholder art) only to prove assembly/timing; it is not the story.
"""
from __future__ import annotations

import math
from pathlib import Path

from . import narration as nar, project as proj

TITLE = "Married to the Don to Keep Me Silent - Pilot (workflow test: opening scene)"
STYLE = ("Illustrated cinematic still, graphic-novel noir, high contrast, wet reflective concrete, saturated orange "
         "sodium light against cold blue shadow, shallow depth of field, subtle film grain. Non-graphic suspense: "
         "no blood, no gore, no visible wounds")
NEG = "blood, gore, visible wound, graphic injury, corpse close-up, text, subtitles, watermark, logo"

PRODUCT_NOTE = ("PRODUCT DECISION: the FIRST published video must be a COMPLETE short film with a satisfying ending, "
                "optimised for views and viewer satisfaction. Book sales are optional (a light, honest mention at most) - "
                "NOT a cliffhanger paywall. This 6-shot pilot is only the opening scene used to test the two-speaker workflow; "
                "the finished film still needs its middle and a resolved ending.")
EDIT_NOTE = ("EDITORIAL PROPOSAL (not the author's approved text): replaces a closing line that said 'I had just "
             "married into a family' - premature, because the wedding happens later in the book.")
ORIGINAL_NOTE = ("Original closing wording preserved here as far as it was given to this session: it contained the phrase "
                 "\"I had just married into a family\". The full original sentence(s) were NOT supplied - paste them below.")

SEGMENTS = [
    ("n01", "heba", "Two shots. That's all it took.", 0.6),
    ("n02", "heba", "I watched a man slide down the side of a silver sedan with a gun lying near his open hand, and the man "
     "standing over him wasn't holding that gun. He was holding a different one. In his left hand.", 0.3),
    ("n03", "heba", "His right arm was in the plaster splint I had built for him forty minutes earlier, in an exam room, "
     "with my own two hands.", 2.0),  # the author's "[2 second pause]"
    ("n04", "lion", "Go back inside, Dottoressa. You were never here.", 0.8),
    ("n05", "heba", "I was an ER doctor.", 0.25),
    ("n06", "heba", "Forty minutes earlier, he had been my patient. Now I was the witness he couldn't afford to leave behind.", 0.0),
]

SHOTS = [
    ("s01", "Two shots", "zoom_in", ["n01"], [], "garage",
     "Wide establishing view of the empty garage level, wet concrete mirroring orange lights, a silver sedan parked at an angle with its driver door open, deep shadows beyond",
     "slow push-in down the lane, eye level", ""),
    ("s02", "The man by the sedan", "pan_right", ["n02"], ["nico"], "garage",
     "A man in a dark jacket has slid down the side of the silver sedan and sits slumped against the wheel arch, face turned away and in shadow, a pistol lying on the wet concrete near his open hand; Nico stands over him holding a DIFFERENT pistol in his LEFT hand, lowered; no blood visible",
     "medium-wide, slow pan from the fallen man's hand to Nico", "Fallen man's face never visible; no blood"),
    ("s03", "Splint and gun", "zoom_out", ["n03"], ["nico"], "garage",
     "Tight insert on Nico's LEFT hand gripping a pistol low by his thigh while his RIGHT forearm hangs beside it wrapped in a white plaster splint; wet concrete and orange light reflections behind",
     "close insert pulling back to reveal his torso; hold the final 2 seconds still", "Gun in LEFT hand only; splint on RIGHT forearm"),
    ("s04", "Go back inside", "zoom_in", ["n04"], ["nico"], "garage",
     "Medium close-up of Nico looking straight into the lens as the doctor's point of view: early thirties, black hair, gray eyes, thin white scar through his LEFT eyebrow, expression calm and unreadable, orange light on one side of his face",
     "slow push-in, slightly low angle", "Scar must be on the LEFT eyebrow"),
    ("s05", "The doctor", "zoom_in", ["n05"], ["ivy"], "garage",
     "Close-up of Ivy in the garage entrance doorway: late twenties, freckles, dark red hair in a messy knot held with a pen, navy scrubs, damp from the night air, wide alert eyes, fluorescent doorway light behind her",
     "slow push-in at eye level", "Pen in hair knot; navy scrubs"),
    ("s06", "The witness", "pan_left", ["n06"], ["ivy", "nico"], "garage",
     "Wide two-shot: Ivy small in the doorway in navy scrubs with red hair knot, Nico backlit by orange sodium lights across the wet concrete in the foreground, silver sedan between them, sense of distance and threat",
     "slow pan from Nico's silhouette to Ivy", "Splint on Nico's RIGHT forearm, gun in LEFT hand"),
]


def build_pilot() -> dict:
    segs = []
    for sid, spk, text, pause in SEGMENTS:
        g = {"id": sid, "speaker": spk, "text": text, "pause_after": pause}
        if sid == "n06":
            g.update(editorial=True, editorial_note=EDIT_NOTE,
                     original_text="[Owner: paste the full original wording here. Known fragment: \"I had just married into a family\".]")
        segs.append(g)
    p = {
        "title": TITLE,
        "logline": "An ER doctor watches the man whose arm she just splinted shoot in a parking garage - and becomes the witness he can't leave behind.",
        "style": STYLE,
        "script": "\n\n".join(f"{'Heba' if s == 'heba' else 'Lion'}: {t}" + (" [2 second pause]" if sid == "n03" else "")
                              for sid, s, t, _ in SEGMENTS),
        "notes": PRODUCT_NOTE + "\n" + EDIT_NOTE + "\n" + ORIGINAL_NOTE + "\n"
                 "Shot durations are ESTIMATES from word counts until real narration audio exists; run `python -m ofs narration sync` after importing audio.\n"
                 "Voices: Heba = Ivy first-person narrator (female). Lion = Nico dialogue + Nico POV (male). No recordings exist in this repo.",
        "characters": [
            {"id": "ivy", "name": "Ivy", "description": "late twenties woman, freckles across nose and cheeks, dark red hair in a messy knot held in place with a pen",
             "wardrobe": "navy hospital scrubs", "voice_notes": "Narrated by Heba (first person)",
             "continuity_notes": "Hair always in a knot WITH A PEN; freckles; navy scrubs in every shot", "reference": ""},
            {"id": "nico", "name": "Nico", "description": "early thirties man, black hair, gray eyes, thin white scar through his LEFT eyebrow",
             "wardrobe": "", "voice_notes": "Voiced by Lion (dialogue and Nico POV)",
             "continuity_notes": "Scar on LEFT eyebrow. Plaster splint on RIGHT forearm. Gun ONLY in LEFT hand. Wardrobe not yet decided: pick one outfit and keep it for the whole story.",
             "reference": ""}],
        "locations": [{"id": "garage", "name": "Brooklyn hospital parking garage, 3 a.m.",
                       "description": "concrete multi-level hospital garage, wet concrete floor, silver sedan, painted lane markings, stairwell door",
                       "lighting": "orange sodium lights, cold shadows, reflections on wet concrete",
                       "continuity_notes": "Silver sedan present in every garage shot; floor always wet; time is 3 a.m.", "reference": ""}],
        "speakers": [
            {"id": "heba", "display_name": "Heba", "role": "Ivy - female first-person narrator", "consent_confirmed": True,
             "consent_statement": "Project owner states Heba consents to voice cloning and commercial use on the channel (statement only; nothing verified by this software).",
             "reference_audio": "", "reference_transcript": ""},
            {"id": "lion", "display_name": "Lion", "role": "Nico - male dialogue and Nico POV", "consent_confirmed": True,
             "consent_statement": "Project owner states Lion consents to voice cloning and commercial use on the channel (statement only; nothing verified by this software).",
             "reference_audio": "", "reference_transcript": ""}],
        "narration_segments": segs,
        "shots": [{"id": i, "title": t, "kind": "image", "asset": f"media/pilot/{i}.png", "duration": 5.0,
                   "motion": m, "transition": "fade" if i in ("s01", "s06") else "cut", "segments": sg, "characters": ch,
                   "location": loc, "action": act, "camera": cam, "continuity_notes": cn, "negative_extra": NEG}
                  for i, t, m, sg, ch, loc, act, cam, cn in SHOTS],
        "audio": {"narration_mode": "segments", "narration": "", "music": "", "music_volume": 0.2},
        "captions": {"srt": "", "mode": "none"},
    }
    p = proj.normalize(p)
    res = nar.sync_shot_durations(p, nar.plan(p, "."))  # ESTIMATED until audio exists
    return res["project"]


def dryrun(project_dir, render_it=True, progress=None) -> dict:
    """SYNTHETIC end-to-end check: tone placeholders for each segment + placeholder art. NOT voices."""
    from . import demo, render
    project_dir = Path(project_dir)
    m = project_dir / "media" / "pilot"
    m.mkdir(parents=True, exist_ok=True)
    p = build_pilot()
    p["title"] += " [SYNTHETIC DRY RUN - tones, not voices]"
    for i, g in enumerate(p["narration_segments"]):
        dur = nar.estimate_seconds(g["text"]) * 0.9
        f = 190 if g["speaker"] == "heba" else 110
        n = int(dur * demo.SR)
        demo._wav(m / f"{g['id']}.wav", [int(7000 * math.sin(2 * math.pi * f * (1 + 0.2 * math.sin(k / 9000)) * k / demo.SR)
                                       * (0.6 + 0.4 * math.sin(2 * math.pi * 2.5 * k / demo.SR))) for k in range(n)])
        g["audio"] = f"media/pilot/{g['id']}.wav"
    for i, s in enumerate(p["shots"]):
        demo._png(m / f"{s['id']}.png", i, f"{s['id']}: {s['title']}")
    pl = nar.plan(p, project_dir)
    p = nar.sync_shot_durations(p, pl)["project"]
    proj.save(project_dir, p)
    return render.render(p, project_dir, project_dir / "output" / "pilot_dryrun.mp4", progress) if render_it else {"project": p}

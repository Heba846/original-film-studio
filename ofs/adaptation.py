"""Full-film adaptation toolkit: parse docs/adaptation/script.md -> segments, shots, project, counts.

The script file is the single source of truth. Everything here is derived from it by code.
HONESTY: durations are ESTIMATES from word counts until real narration audio exists.
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

from . import narration as nar, project as proj

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")
PAUSE_RE = re.compile(r"\s*\{p=([0-9.]+)\}\s*$")
DEFAULT_PAUSE = 0.35

STYLE = ("Painterly illustrated realism, rich gouache and oil texture, cinematic noir composition, visible brush "
         "structure, saturated orange sodium light against cold blue shadow, soft film grain. Non-graphic suspense: "
         "no blood, no gore, no visible wounds. 16:9")
NEGATIVE = ("blood, gore, visible wound, graphic injury, corpse close-up, photorealistic render, 3d render, text, "
            "subtitles, watermark, logo, extra fingers, deformed hands, inconsistent face, changing outfit")

CHARACTERS = [
    ("ivy", "Ivy (Dr. Ivy Claire Marlowe)", "28-year-old emergency-medicine resident, freckled, red hair in a messy bun held with a pen, determined expression",
     "navy scrubs at work; her late mother's oversized gray cardigan elsewhere",
     "Red messy bun WITH A PEN, freckles, navy scrubs. After Oct 6 she wears Nonna Rosa's too-large square emerald wedding ring threaded on a thin gold chain at her neck, tucked under scrubs (not a generic pendant); at home/court the ring is on her left finger and from Nov 5 a plain gold band sits under it so it stops turning."),
    ("nico", "Nico Vescari", "34-year-old man, dark wavy hair, stubble, gray eyes, thin white scar through his LEFT eyebrow, tall, calm unreadable expression",
     "ruined charcoal suit (Oct 3), then dark sweaters and white shirts, tuxedo at the gala",
     "Scar LEFT eyebrow; gray eyes. Cut on RIGHT forearm: white plaster splint fingertips-to-elbow Oct 3-10, black thermoplastic shell with 3 velcro straps (Teresa's small white cross on the wrist strap) Oct 10-Nov 13, removed Nov 13. Uses/holds the gun with his LEFT hand; signs left-handed until Nov 13. Wears Tommy's plain gold band on his LEFT hand."),
    ("enzo", "Enzo Vescari", "21-year-old man, thin, gold curls, brown eyes, crooked smile like Nico's", "gray hoodie / gray jacket", "Gold curls; gray jacket (the 'light jacket' on the stairs)."),
    ("sal", "Uncle Sal (Salvatore Vescari)", "61-year-old man, silver hair, warm brown eyes, big soft build, warm smile", "camel coat, cardigan and slippers at home, hat",
     "Always a tin or twist of white-paper anise candies; Monteleone's cannoli box."),
    ("lucia", "Lucia Vescari", "late-fifties Sicilian woman, small, straight back, silver-streaked hair pulled tight, black eyes", "black dress buttoned to the throat, gold cross at her collarbone",
     "Hand finds the gold cross when afraid."),
    ("tommy", "Tommy Greco", "Nico's buzz-cut lieutenant, face like a locked door", "black suit", "Buzz cut."),
    ("rocco", "Rocco", "huge, quiet man, folded newspaper and a crossword", "dark suit", "6.5 ft; crossword."),
    ("theo", "Theo Marlowe", "20-year-old man, thin, mechanic, ears redden when he lies", "work shirt, Mets hoodie, grease on the right knee", "Ears redden when lying."),
    ("priya", "Priya", "tall ER nurse with an energy drink the color of antifreeze", "scrubs; yellow sundress and jean jacket at the wedding", "Never sets down the can."),
    ("reyes", "Special Agent Dana Reyes", "FBI agent, rumpled", "rain jacket", "Rain jacket even in blue sky."),
    ("holloway", "Grant Holloway", "federal prosecutor, very good teeth", "navy suit, straightens his cuffs", "Straightens cuffs when sure."),
    ("bell", "Dr. Marcus Bell", "52-year-old attending, gray untrimmed beard", "reading glasses on a cord", "Glasses on a cord; hums Billy Joel."),
    ("brancato", "Carmine Brancato", "late-sixties heavy man, thick white hair combed back, winter tan, wire glasses", "brown cardigan buttoned wrong", "Cardigan buttoned wrong."),
    ("frankie", "Frankie Lombardi", "44-year-old man, Vescari soldier and FBI informant", "good dark coat", "Face turned away; no gore."),
    ("danny", "Danny Bell", "17-year-old, thin, no eyebrows, port scar under the collarbone", "gray beanie, hoodie", "Gray beanie."),
]
LOCATIONS = [
    ("garage", "St. Brigid's hospital garage, level 2", "three-level concrete garage across the service road, spot 2-14, a dark stairwell door", "orange sodium lights, cold rain, wet concrete",
     "Silver sedan near the stairwell door; camera dome dead; floor wet at 4:10 a.m."),
    ("er", "St. Brigid's ER, Red Hook, Brooklyn", "22 bays, glass-walled nurses' station 'the fishbowl', bay 14 with a buzzing light", "fluorescent, buzzing", "Bay 14 curtain."),
    ("ivy_apt", "Ivy's Bay Ridge walk-up", "third-floor brick walk-up, radiator, her late mother's armchair", "lamp light", "Her mother's armchair."),
    ("restaurant", "Vescari's restaurant, Van Brunt St", "narrow brick restaurant, green awning, back room with old photographs and a long table", "warm low light", "Concrete planter by the door (the gun is buried there later)."),
    ("study", "Nico's study, Carroll Street", "dark green leather desk, father's portrait, a top drawer", "desk lamp", "14 stairs up from the third floor; blinds closed until the epilogue."),
    ("courthouse", "Brooklyn courthouse and judge's chambers", "wood-paneled chambers with a butterscotch candy bowl; courthouse steps", "daylight", ""),
    ("kitchen", "Carroll Street kitchen", "marble island, farmhouse sink", "lamp light", "Marble island."),
    ("bedroom", "Ivy's third-floor room", "connecting door to Nico's room, brass bolt on Ivy's side with crooked screws", "lamp light", "Brass bolt on Ivy's side only."),
    ("garden", "Carroll Street garden", "lemon trees in clay pots (burlap in winter), fig tree, stone bench, long table, iron lanterns, back gate", "dusk / lanterns", "Burlap on the lemon trees until April."),
    ("hospital_pharmacy", "St. Brigid's pharmacy basement", "robot arm, shelves of foil blister cards", "fluorescent", ""),
    ("courtroom", "Federal courtroom 6B, Cadman Plaza", "oak bench, white-haired judge with a pencil behind her ear", "flat daylight", ""),
    ("grandjury", "Grand jury room", "windowless room, oak bench, nineteen jurors", "flat light", ""),
    ("street", "Brooklyn streets and car interiors", "black car, wet street, bridge at dusk", "streetlights", ""),
    ("sal_garage", "Sal's private garage", "old gray Lincoln Town Car", "single bulb", "Anise wrappers."),
    ("bell_home", "Bell family home, Park Slope", "narrow brick house, plywood wheelchair ramp, kitchen at dawn", "dawn light", ""),
    ("club", "Brancato's social club, Bath Ave & 21st", "green door, neon MEMBERS with a burned-out M, linoleum floor", "neon green and sodium", ""),
    ("mdc", "Federal detention visiting room", "glass table", "flat light", ""),
]


def spoken_words(text: str) -> int:
    return len(WORD_RE.findall(text.replace("[CTA]", "")))


def parse_script(path) -> dict:
    chapters, shots, segs = [], [], []
    ch = shot = None
    note = ""
    in_comment = False
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if line.startswith("## CH"):
            parts = [p.strip() for p in line[3:].split("|")]
            ch = {"id": parts[0], "title": parts[1] if len(parts) > 1 else ""}
            chapters.append(ch)
        elif line.startswith("@s"):
            f = [p.strip() for p in line[1:].split("|")]
            if len(f) < 7:
                raise ValueError(f"shot line needs 7 fields: {line[:60]}")
            shot = {"id": f[0], "motion": f[1], "characters": [c for c in f[2].split(",") if c],
                    "location": f[3], "camera": f[4], "action": f[5], "continuity": f[6], "chapter": ch["id"]}
            shots.append(shot)
        elif line.startswith(">"):
            note = line[1:].strip()
        elif line[:2] in ("H:", "L:"):
            text = line[2:].strip()
            m = PAUSE_RE.search(text)
            pause = float(m.group(1)) if m else DEFAULT_PAUSE
            if m:
                text = text[:m.start()].strip()
            segs.append({"id": f"n{len(segs) + 1:03}", "chapter": ch["id"], "shot": shot["id"],
                         "speaker": "heba" if line[0] == "H" else "lion", "text": text.replace("[CTA]", "").strip(),
                         "pause_after": pause, "direction": note, "optional_cta": "[CTA]" in text})
            note = ""
    return {"chapters": chapters, "shots": shots, "segments": segs}


def word_stats(parsed: dict, wpm=(140, 150, 160)) -> dict:
    segs = parsed["segments"]
    per_ch, per_sp = {}, {"heba": 0, "lion": 0}
    for s in segs:
        w = spoken_words(s["text"])
        per_ch[s["chapter"]] = per_ch.get(s["chapter"], 0) + w
        per_sp[s["speaker"]] += w
    total = sum(per_ch.values())
    cta = sum(spoken_words(s["text"]) for s in segs if s["optional_cta"])
    pauses = sum(s["pause_after"] for s in segs)
    est = {str(r): round(total / r * 60 + pauses, 1) for r in wpm}
    return {"total_words": total, "optional_cta_words": cta, "words_by_chapter": per_ch, "words_by_speaker": per_sp,
            "pause_seconds": round(pauses, 1), "estimated_seconds_at_wpm": est,
            "estimate_note": "ESTIMATE from word count + scripted pauses. NOT measured: no narration has been recorded."}


def chapter_timestamps(parsed: dict, wpm=150) -> list:
    """ESTIMATED chapter start times (seconds) for the YouTube description. Re-compute after real audio exists."""
    t, out, seen = 0.0, [], set()
    for s in parsed["segments"]:
        if s["chapter"] not in seen:
            seen.add(s["chapter"])
            out.append({"chapter": s["chapter"], "start_est_s": round(t, 1)})
        t += spoken_words(s["text"]) / wpm * 60 + s["pause_after"]
    return out


def segments_csv(parsed: dict) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "chapter", "shot", "speaker", "words", "pause_after", "optional_cta", "direction", "text"])
    for s in parsed["segments"]:
        w.writerow([s["id"], s["chapter"], s["shot"], s["speaker"], spoken_words(s["text"]), s["pause_after"],
                    int(s["optional_cta"]), s["direction"], s["text"]])
    return buf.getvalue()


def build_project(parsed: dict) -> dict:
    chars = [{"id": i, "name": n, "description": d, "wardrobe": w, "voice_notes": "",
              "continuity_notes": c, "reference": ""} for i, n, d, w, c in CHARACTERS]
    locs = [{"id": i, "name": n, "description": d, "lighting": l, "continuity_notes": c, "reference": ""}
            for i, n, d, l, c in LOCATIONS]
    segs = []
    for s in parsed["segments"]:
        g = {"id": s["id"], "speaker": s["speaker"], "text": s["text"], "pause_after": s["pause_after"]}
        segs.append(g)
    shots = []
    for sh in parsed["shots"]:
        shots.append({"id": sh["id"], "title": sh["chapter"], "kind": "image", "asset": f"media/film/{sh['id']}.png",
                      "duration": 5.0, "motion": sh["motion"], "transition": "cut", "characters": sh["characters"],
                      "location": sh["location"], "action": sh["action"], "camera": sh["camera"],
                      "continuity_notes": sh["continuity"], "negative_extra": NEGATIVE,
                      "segments": [x["id"] for x in parsed["segments"] if x["shot"] == sh["id"]]})
    p = proj.normalize({
        "title": "Married to the Don to Keep Me Silent - narrated film (full adaptation)",
        "logline": "An ER resident who saw a don at a garage shooting marries him on paper to stay alive and silent, then exposes the traitor in his own house.",
        "style": STYLE,
        "script": Path(__file__).resolve().parent.parent.joinpath("docs/adaptation/script.md").read_text(encoding="utf-8"),
        "notes": ("FULL FILM. Complete story with an earned HEA; the optional book mention is the last paragraph only (no cliffhanger paywall). "
                  "NO narration audio and NO illustrations exist yet: every shot asset and every segment audio is missing on purpose. "
                  "Durations are ESTIMATES from word counts until real audio is imported, then run `python -m ofs narration sync`. "
                  "Canon source: the author's novel (pages in docs/adaptation/canon_ledger.md). Speaker consent is the owner's statement; "
                  "nothing here is a recording or a voice clone."),
        "characters": chars, "locations": locs,
        "speakers": [
            {"id": "heba", "display_name": "Heba", "role": "Ivy first-person narrator; quotes every non-Nico character",
             "consent_confirmed": True, "consent_statement": "Project owner states Heba consents to voice cloning and commercial channel use (statement only; not verified by software).",
             "reference_audio": "", "reference_transcript": ""},
            {"id": "lion", "display_name": "Lion", "role": "Nico: all dialogue and Nico-POV narration",
             "consent_confirmed": True, "consent_statement": "Project owner states Lion consents to voice cloning and commercial channel use (statement only; not verified by software).",
             "reference_audio": "", "reference_transcript": ""}],
        "narration_segments": segs, "shots": shots,
        "audio": {"narration_mode": "segments", "narration": "", "music": "", "music_volume": 0.18},
        "captions": {"srt": "", "mode": "none"},
    })
    pl = nar.plan(p, ".")
    return nar.sync_shot_durations(p, pl)["project"]


def write_outputs(root: Path) -> dict:
    ad = root / "docs" / "adaptation"
    parsed = parse_script(ad / "script.md")
    stats = word_stats(parsed)
    stats["chapter_timestamps_estimated"] = chapter_timestamps(parsed)
    (ad / "segments.csv").write_text(segments_csv(parsed), encoding="utf-8-sig")
    (ad / "segments.json").write_text(json.dumps(parsed["segments"], indent=2, ensure_ascii=False), encoding="utf-8")
    (ad / "word_count.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    p = build_project(parsed)
    proj.save(root / "projects" / "married_to_the_don_full_film", p)
    (root / "projects" / "married_to_the_don_full_film" / "media" / "film").mkdir(parents=True, exist_ok=True)
    from . import prompts as pr
    items = pr.build_prompts(p)
    (ad / "shot_prompts.json").write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    (ad / "shot_prompts.md").write_text(pr.to_markdown(p, items), encoding="utf-8")
    (ad / "shot_prompts.csv").write_text(pr.to_csv(items), encoding="utf-8-sig")
    return {"stats": stats, "shots": len(parsed["shots"]), "segments": len(parsed["segments"])}

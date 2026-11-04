#!/usr/bin/env python3
"""Export edition20/FULL70_FLOW_PROMPTS.json: paste-ready prompts for all 70 jobs (plain UTF-8 JSON).

Prompts never name characters or any real person: every character is an ORIGINAL FICTIONAL ILLUSTRATED
character described by role and look, so Flow's prominent-people filter has nothing to match (F03/F08 were
refused once). The Flow project's hospital.png is the style reference, and the face reference for the
red-haired doctor and the scarred man. Placements come from the built timeline (run tools/film_build.py first).
"""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
J = json.loads((R / "edition20/flow_jobs.json").read_text())["jobs"]
T = json.loads((R / "src/film/data/film_timeline.json").read_text())
L = json.loads((R / "edition20/budget_ledger.json").read_text())

FICTION = ("Original fictional illustrated characters invented for this film; not based on, and not resembling, any real "
           "person, actor or public figure.")
STYLE = ("Reference images are for faces only (REF_IVY_FACE_ONLY.png, REF_NICO_FACE_ONLY.png) and, for the garage, location only "
         "(REF_GARAGE_F01.png); never copy a reference image's background or composition; this is NOT a continuation of any image. "
         "Painterly illustrated cinematic style: visible soft brush texture, warm sodium-orange and "
         "teal-shadow palette, shallow depth of field, natural restrained motion, stable faces and positions, no morphing, "
         "no smoke, no on-screen text, no readable signs, clocks, plates or logos, no subtitles, no mirror image, 16:9, 8 seconds.")
CAST = {  # role descriptions (no names). Face reference applies to the two leads.
 "IVY": ("the red-haired doctor", "the red-haired doctor: an original fictional woman, 28, pale freckled skin, messy copper-red hair in a bun with a ballpoint pen through it (face as in REF_IVY_FACE_ONLY.png)"),
 "NICO": ("the scarred man", "the scarred man: an original fictional man, 34, dark wavy hair, short stubble, gray eyes, a thin HEALED WHITE old scar through his anatomical LEFT eyebrow - when he faces camera it is the eyebrow on the RIGHT side of the image - and no bandage, tape or plaster anywhere on his face; his injured arm is his anatomical RIGHT forearm, on the LEFT side of the image when he faces camera (face as in REF_NICO_FACE_ONLY.png)"),
 "THEO": ("her younger brother", "her younger brother: early 20s, thin, pale, red ears, short brown hair"),
 "SAL": ("the silver-haired uncle", "the silver-haired uncle: 60s, silver hair, camel coat, warm unhurried manner, a dusting of powdered sugar on his tie"),
 "ENZO": ("the curly-haired young man", "the curly-haired young man: 21, gold curls, gray jacket"),
 "REYES": ("the woman agent", "the woman agent: 40s, dark hair pulled back, rumpled rain jacket"),
 "HOLLOWAY": ("the prosecutor", "the prosecutor: 40s, neat, navy suit, straightens his cuffs"),
 "BELL": ("the older doctor", "the older doctor: 60s, tired, gray hair, white coat over a cardigan"),
 "TOMMY": ("the quiet associate", "the quiet associate: 30s, dark suit, close-cropped hair"),
 "ROCCO": ("the huge bodyguard", "the huge bodyguard: 40s, very large, dark coat, calm"),
 "LUCIA": ("the older woman in black", "the older woman in black: 60s, black dress, small gold cross necklace"),
 "BRANCATO": ("the heavyset rival", "the heavyset rival: 60s, heavyset, brown cardigan buttoned wrong"),
 "DANNY": ("the pale teenage boy", "the pale teenage boy: 17, thin, pale, hooded sweatshirt"),
 "FELD": ("the elderly lawyer", "the elderly lawyer: 60s, glasses, gray suit, blue pen"),
 "FRANKIE": ("the heavy man in the overcoat", "the heavy man in the overcoat: fifties, heavy, balding, good dark overcoat"),
 "JOEY": ("the young patient", "the young patient: early 20s, dark hair"),
}
NAMES = {"Ivy": "IVY", "Nico": "NICO", "Theo": "THEO", "Sal": "SAL", "Enzo": "ENZO", "Reyes": "REYES", "Holloway": "HOLLOWAY",
         "Dr. Marcus Bell": "BELL", "Bell": "BELL", "Tommy": "TOMMY", "Lucia": "LUCIA", "Brancato": "BRANCATO", "Danny Bell": "DANNY",
         "Feld": "FELD", "Frankie": "FRANKIE"}
LEADS = {"IVY", "NICO"}
CONT = {
 "P0": "Fri Oct 3 - Sun Oct 5: the doctor wears no ring, no necklace, no chain; the scarred man has a WHITE plaster splint on his anatomical RIGHT forearm from fingertips to below the elbow and wears a ruined charcoal suit over a black shirt (jacket off in the ER bay).",
 "P1": "Mon Oct 6 (wedding day): a square emerald ring, too big, on the doctor's LEFT ring finger; the scarred man's WHITE plaster splint on his anatomical RIGHT forearm.",
 "P2": "Oct 7 - Nov 4: at work the emerald ring hangs on a thin gold chain under her navy scrub top; off duty it is on her LEFT ring finger; the scarred man's splint on his anatomical RIGHT forearm is BLACK thermoplastic with three velcro straps.",
 "P3": "Nov 5 - Nov 13 morning: a plain gold band under the emerald on her LEFT ring finger; the scarred man's BLACK splint on his anatomical RIGHT forearm.",
 "P4": "Nov 13 afternoon onward: the scarred man wears NO splint; she wears the emerald with the gold band.",
 "P5": "April: spring light, no splint; she wears the emerald with the gold band.",
}
# Oct 7-10 scenes in P2 still have the WHITE splint; Oct 16+ have the black one
WHITE_IN_P2 = {"ring_chain", "joey_bay", "bell_asks"}

PRE = [("Vescari study", "a dark wood-panelled private study"), ("gray Lincoln", "gray luxury sedan (no badge)"),
       ("A gray Lincoln", "A gray luxury sedan (no badge)"), ("the lawyer Feld", "Feld"), ("Nico's side", "the scarred man's side")]
PRE_SPLINT = ("Fri Oct 3, 3:05-3:35 a.m., BEFORE the splint exists: an open clean cut on the inside of the scarred man's anatomical "
              "RIGHT forearm, NO splint and NO bandage yet; black shirt (charcoal suit jacket on at the door, off in the ER bay); "
              "the doctor wears no ring, no necklace, no chain.")
SLUG_CONT = {"er_entrance": PRE_SPLINT, "ivy_walks": PRE_SPLINT, "bay_hands": PRE_SPLINT, "nico_bay_cu": PRE_SPLINT, "ivy_bay_cu": PRE_SPLINT,"splint_off": "Nov 13, 2 p.m.: at the start his anatomical RIGHT forearm is in the BLACK thermoplastic splint (three velcro "
                           "straps); in this shot it is removed and afterwards there is no splint. She wears the emerald with a gold band."}

def depersonalise(text: str) -> tuple[str, list[str]]:
    for a, b in PRE:
        text = text.replace(a, b)
    present = []
    for name in sorted(NAMES, key=len, reverse=True):
        key = NAMES[name]
        if re.search(r"\b" + re.escape(name) + r"\b", text):
            if key not in present: present.append(key)
            text = re.sub(r"\b" + re.escape(name) + r"'s\b", CAST[key][0] + "'s", text)
            text = re.sub(r"\b" + re.escape(name) + r"\b", CAST[key][0], text)
    return text, present

def batch1_prompt(p: str) -> tuple[str, list[str]]:
    p = p.replace("Ivy Marlowe (same face as reference REF_ivy_face_hospital_1s.png): woman, 28, pale freckled skin, messy copper-red hair in a bun with a ballpoint pen stuck through it",
                  CAST["IVY"][1])
    p = p.replace("Nico Vescari (same face as reference REF_nico_face_hospital_7s.png): man, 34, dark wavy hair, short stubble, gray eyes, a thin HEALED WHITE old scar through his anatomical LEFT eyebrow (no fresh cut, no blood on the face)",
                  CAST["NICO"][1] + " (no fresh cut, no blood on the face)")
    p = p.replace("Ivy wears no ring, no necklace and no chain", "she wears no ring, no necklace and no chain")
    p = p.replace("Frankie:", "the heavy man in the overcoat:").replace("Nico's side", "the scarred man's side")
    p = p.replace("Ivy's head", "the red-haired doctor's head").replace("Ivy", "the red-haired doctor")
    p = re.sub(r"Painterly cinematic realism matching the reference stills:.*$", "", p).strip()
    present = [k for k in ("IVY", "NICO") if CAST[k][0] in p] + (["FRANKIE"] if "overcoat" in p else [])
    return p, present

GARAGE_SLUGS = {"garage_env", "ivy_crouch", "aftermath_wide", "frankie_hand", "nico_hands", "nico_ots", "ivy_reaction", "ivy_frozen",
                "stairs_sleeve", "block_her", "mopped_bay", "enzo_stairs"}
GEO = ("Location: the same parking garage as REF_GARAGE_F01.png - level two, low concrete ceiling, concrete pillars with yellow "
       "bumper guards, pooled water with sodium-orange reflections, no falling rain; a silver sedan parked nose-out facing camera "
       "in the centre bay in front of a gray steel stairwell door, open concrete stairs to the right of the door; the doctor's own "
       "car is a dark car whose glossy hood fills the near foreground. No workshop, no tool chests, no shelving, no hospital interior, "
       "no curtains, no IV poles.")
RETAKE = {
 "ivy_crouch": ("Original fictional illustrated characters invented for this film; not based on, and not resembling, any real person, actor "
   "or public figure. Side-on medium close shot at 4 a.m. in the parking garage of REF_GARAGE_F01.png: the red-haired doctor (an original "
   "fictional woman, 28, pale freckled skin, messy copper-red hair in a bun with ONE ballpoint pen through it, face as in REF_IVY_FACE_ONLY.png), "
   "navy short-sleeved scrubs, NO stethoscope, no necklace, no chain, no ring, crouched low on the wet concrete behind her own dark car, "
   "her back against its side panel near the rear wheel, a phone charger cable in her fist, holding her breath, lips pressed together, "
   "then slowly turning her head toward a sound off-screen. Behind her only concrete pillars with yellow bumper guards, pooled water and "
   "sodium-orange light - no hospital interior, no curtains, no IV poles, no monitors. Mouth closed throughout."),
 "nico_ots": ("Original fictional illustrated characters invented for this film; not based on, and not resembling, any real person, actor "
   "or public figure. Over-the-shoulder shot in the parking garage of REF_GARAGE_F01.png. Soft-focus foreground: only the back of the "
   "red-haired doctor's head - messy copper-red bun with ONE ballpoint pen in it - and one navy scrub shoulder (no pen on the shoulder), "
   "as she hides behind the glossy hood of her dark car. In focus twenty feet away, STANDING upright beside the silver sedan in front of "
   "the gray stairwell door: the scarred man (an original fictional man, 34, dark wavy hair, short stubble, gray eyes, face as in "
   "REF_NICO_FACE_ONLY.png). His face is clean: NO bandage, NO tape, NO plaster, no blood anywhere on the face; only a thin healed white scar line "
   "through his anatomical LEFT eyebrow, which is the eyebrow on the RIGHT side of the image as he faces camera. Ruined charcoal suit "
   "jacket over a black shirt, a white plaster splint from fingertips to elbow on his anatomical RIGHT forearm (LEFT side of the image), "
   "held against his chest. He turns his head toward her, finds her eyes and holds them; he breathes; his mouth stays CLOSED; he does NOT "
   "speak, lean, sit or walk; one slow nod toward the stairwell door near the end. No workshop, no tool chests, no shelving, no other "
   "person in frame."),
}
placements = {}
for c in T["cuts"]:
    if c.get("kind") == "flow_job":
        placements.setdefault(c["shot"], []).append({"segment": c["seg"], "seconds_on_screen": round(c["dur"] / 24, 2),
            "source_in_s": c["src_in"], "source_out_s": c["src_out"], "speed": c["rate"], "memory": bool(c.get("memory")),
            "reuse_reason": c.get("why") if c.get("is_reuse") else None})
refused = {e["job_id"] for e in L.get("entries", []) if "refunded" in e.get("verdict", "")}
APPROVED = {x["shot_id"]: True for x in json.loads((R / "edition20/media_manifest.json").read_text())["shots"] if x.get("status") == "approved"}
retakes = {r["job_id"] for r in L.get("planned_retakes", [])}
generating = {e["job_id"] for e in L.get("entries", []) if "generating" in e.get("verdict", "")}
# jobs already submitted keep the exact text that was sent (v3 for Batch 1, v4 for F18-F28)
AS_SENT = {}
for fname, ids in (("FULL70_FLOW_PROMPTS_v3_as_sent.json", generating & {f"F{n:02d}" for n in range(1, 14)}),
                   ("FULL70_FLOW_PROMPTS_v4_as_sent.json", generating - {f"F{n:02d}" for n in range(1, 14)})):
    fp = R / "edition20/out" / fname
    if fp.exists():
        AS_SENT.update({x["id"]: x["prompt"] for x in json.loads(fp.read_text())["jobs"] if x["id"] in ids})

jobs = []
for j in J:
    if j["batch"] == 1:
        body, present = batch1_prompt(j["prompt"])
    else:
        intent = j["prompt"].split(":", 1)[1].split("LOCK P")[0].strip()
        body, present = depersonalise(intent)
        cast_lines = "; ".join(CAST[k][1] for k in present)
        body = body + (" Characters: " + cast_lines + "." if cast_lines else "")
        if j["mouth"] == "closed": body += " Mouths stay closed; nobody speaks."
        if j["decisive"]: body += " Show the action once, clearly, with fixed roles and positions."
    cont = SLUG_CONT.get(j["slug"], CONT[j["continuity_phase"]])
    if j["slug"] in WHITE_IN_P2:
        cont = cont.replace("is BLACK thermoplastic with three velcro straps", "is still WHITE plaster (before Oct 10)")
    if j["slug"] in RETAKE:
        body = RETAKE[j["slug"]]
        present = ["IVY", "NICO"] if j["slug"] == "nico_ots" else ["IVY"]
        prompt = f"{body} Continuity: {cont} {STYLE}"
    elif j["slug"] in GARAGE_SLUGS:
        geo = GEO
        if j["slug"] == "mopped_bay":   # 4:31: the sedan and the man are gone
            geo = GEO.replace("a silver sedan parked nose-out facing camera in the centre bay in front of a gray steel stairwell door",
                              "the centre bay in front of the gray steel stairwell door is now EMPTY and freshly mopped - NO silver sedan, no man on the floor")
        prompt = f"{FICTION} {body} {geo} Continuity: {cont} {STYLE}"
    else:
        prompt = f"{FICTION} {body} Continuity: {cont} {STYLE}"
    if j["job_id"] in AS_SENT:
        prompt = AS_SENT[j["job_id"]]
    ER = {"er_entrance", "ivy_walks", "bay_hands", "nico_bay_cu", "ivy_bay_cu", "money_tray"}
    faces = [f"REF_{k}_FACE_ONLY.png" for k in ("IVY", "NICO") if k in present]
    ref = " + ".join(faces) + " (faces only)" if faces else "no character reference"
    if j["slug"] in ER: ref += " + hospital.png allowed (this IS the ER bay)"
    if j["slug"] in GARAGE_SLUGS: ref += " + REF_GARAGE_F01.png (location)"
    jobs.append({
        "id": j["job_id"], "slug": j["slug"], "batch": j["batch"], "chapter": j["chapter"], "category": j["category"],
        "status_note": ("RETAKE (retake pool, 10 cr): take 1 rejected after frame audit - new prompt" if j["job_id"] in retakes
                        else "SUBMITTED / GENERATING - prompt kept exactly as sent" if j["job_id"] in generating
                        else "APPROVED (restricted where noted in review) - do not regenerate" if APPROVED.get(j["job_id"])
                        else "REGENERATE (primary job): earlier attempts failed and were refunded" if j["job_id"] in refused
                        else "GENERATED in Flow, download failed - re-download, do not regenerate" if j["job_id"] == "F05"
                        else "not yet generated"),
        "prompt": prompt,
        "required_reference": ref,
        "continuity_phase": j["continuity_phase"], "continuity": cont,
        "expected_duration_s": 8, "usable_window_s": [0.2, 7.7], "outputs_per_prompt": 1,
        "output_filename": f"{j['job_id']}.mp4",
        "save_to_in_project": f"public/flow/{j['job_id']}.mp4",
        "narrative_event": j["narrative_event"], "mouth": j["mouth"], "decisive_action": j["decisive"],
        "placements": placements.get(j["job_id"], []),
    })
out = {"about": "Paste-ready Flow prompts, Film20 plan v2. 70 jobs x 1 output. Send each MP4 back named exactly as output_filename.",
       "budget": {"cap": 1000, "primary_pool": 700, "retakes_pool": 200, "reserve": 100, "credits_per_output_assumed": 10,
                  "net_spent_so_far": sum(e["credits_charged"] for e in L.get("entries", [])),
                  "note": "F03 and F08 were refused and refunded; their resubmission is still a primary job (no extra charge to the plan)."},
       "fiction_notice": FICTION, "style_suffix": STYLE, "jobs": jobs}
(R / "edition20/FULL70_FLOW_PROMPTS.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
banned = [n for n in ["Ivy", "Nico", "Vescari", "Marlowe", "Theo", "Sal ", "Enzo", "Reyes", "Holloway", "Bell", "Tommy", "Rocco", "Lucia",
                      "Brancato", "Danny", "Feld", "Frankie", "Joey", "Lincoln", "REF_ivy", "REF_nico"] if any(n in x["prompt"] for x in jobs)]
print(len(jobs), "jobs written; names left in prompts:", banned or "none")

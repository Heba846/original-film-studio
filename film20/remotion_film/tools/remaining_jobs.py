#!/usr/bin/env python3
"""edition20/REMAINING_JOBS.json: compact machine-readable list of every job without an approved take, with
per-job location + costume overrides, still/animation prompts (from FULL70_FLOW_PROMPTS.json) and the exact
source ranges the timeline needs. Run after tools/export_flow_prompts.py."""
import json
from pathlib import Path
R = Path(__file__).resolve().parent.parent
P = {j["id"]: j for j in json.loads((R / "edition20/FULL70_FLOW_PROMPTS.json").read_text())["jobs"]}
M = {s["shot_id"]: s for s in json.loads((R / "edition20/media_manifest.json").read_text())["shots"]}
T = json.loads((R / "src/film/data/film_timeline.json").read_text())

LOC = {  # slug -> location override (independent of any reference image)
 "ivy_crouch": "hospital parking garage L2 (REF_GARAGE_F01): concrete pillars, yellow bumper guards, pooled water, sodium light; beside her dark car",
 "aftermath_wide": "garage L2: silver sedan in front of the gray steel stairwell door; seen over the glossy hood of her dark car",
 "frankie_hand": "garage L2 wet concrete beside the silver sedan", "nico_hands": "garage L2 beside the silver sedan, waist height",
 "er_entrance": "night ER waiting area at the sliding doors, plastic chairs, triage desk", "ivy_frozen": "garage L2, stairwell door behind her",
 "stairs_sleeve": "garage stairwell, concrete steps, lights out above", "block_her": "garage L2 between her car and the silver sedan",
 "mopped_bay": "garage L2, the sedan's bay EMPTY and freshly mopped, dead camera dome", "fbi_couch": "Ivy's small Brooklyn apartment living room, worn couch, morning",
 "ivy_window": "Ivy's apartment by the window, morning", "apt_wide": "Ivy's apartment at 7 p.m., lamp off, door open to the stairwell, old armchair",
 "nico_armchair": "Ivy's dark apartment, old armchair, streetlight only (NOT a hospital)", "ivy_doorway": "Ivy's apartment doorway, grocery bag",
 "supply_room": "hospital supply room, shelves of coiled IV tubing, door", "rocco": "hospital supply-room doorway",
 "ivy_car_dusk": "hospital parking lot at dusk, outdoors, by her car", "restaurant": "closed Italian restaurant, chairs up on tables except one (NOT a hospital)",
 "nico_tommy": "closed Italian restaurant table", "ivy_terms": "closed Italian restaurant table", "sal_arrives": "Vescari study at night, wood panels, desk",
 "nico_desk": "Vescari study, desk", "sal_exits": "Vescari study garden door at night, fig tree outside", "emerald_on": "judge's chambers, close on hands",
 "steps": "courthouse steps, daytime, reporters", "kiss": "courthouse steps, cameras", "bolt": "Vescari house, connecting bedroom door",
 "ring_chain": "hospital staff locker room", "joey_bay": "ER trauma bay with glass wall", "bell_asks": "nurses' station, morning",
 "bell_cries": "Dr. Bell's office, evening", "pen_kiss": "Vescari study at night", "eyes_drawer": "Vescari study desk, top drawer",
 "fig_lunch": "Vescari garden, Sunday lunch under a fig tree", "foil_card": "upstairs bathroom floor, Vescari house", "enzo_sleeve": "ER bay",
 "enzo_stairs": "garage stairwell at 4:10 a.m., Oct 3 (flashback)", "lincoln": "street at night, gray luxury sedan (no badge)",
 "courtroom": "Courtroom 6B, witness stand", "nico_gallery": "Courtroom 6B gallery benches", "palm_up": "back seat of a car at dusk",
 "drawer_midnight": "Vescari study at midnight, desk drawer", "glovebox": "Sal's private garage at night, gray sedan (no badge)",
 "trunk": "Sal's garage, open car trunk", "ivy_twist": "Vescari study at night", "danny_letter": "Bell family kitchen at dawn",
 "table_evidence": "Vescari dining room 7 p.m., white tablecloth", "sal_hands": "Vescari dining room", "ivy_speaks": "Vescari dining room, reverse angle",
 "theo_out": "outside a federal detention center at noon, Ivy's car", "club_wide": "Bath Avenue social club at night",
 "ivy_bags": "Bath Avenue club floor", "nico_enters": "Bath Avenue club entrance", "reyes_warrant": "Bath Avenue club front door",
 "visiting": "federal detention visiting room", "grand_jury": "plain grand-jury room", "splint_off": "Vescari house, daylight, close on his arm",
 "pockets_bed": "Nico's bedroom, Vescari house, evening", "nico_listens": "Nico's bedroom, door open", "april_garden": "Vescari garden in April, lemon trees",
 "reyes_gate": "Vescari garden gate, warm Saturday", "stairs_14": "Vescari house, narrow staircase up to the study door",
}
COST = {
 "IVY": {"P0": "navy short-sleeved scrubs (work) or faded T-shirt + gray cardigan (home); copper-red bun with ONE pen; NO ring/chain",
         "P1": "simple dress for the wedding; emerald on LEFT ring finger (loose)", "P2": "navy scrubs at work with the ring on a gold chain UNDER the top; off duty gray cardigan, emerald on LEFT ring finger",
         "P3": "gray cardigan; emerald + plain gold band on LEFT ring finger", "P4": "gray cardigan; emerald + gold band", "P5": "light spring cardigan; emerald + gold band"},
 "NICO": {"P0": "ruined charcoal suit over black shirt; WHITE plaster splint anatomical RIGHT forearm (image-left facing camera); healed white scar anatomical LEFT brow (image-right); gun only ever in his LEFT hand",
          "P1": "dark suit; WHITE plaster splint RIGHT forearm", "P2": "dark suit or shirt sleeves; splint WHITE until Oct 10, then BLACK thermoplastic with 3 velcro straps, RIGHT forearm",
          "P3": "rumpled white shirt or dark suit; BLACK splint RIGHT forearm", "P4": "no splint", "P5": "open-collar shirt; no splint"},
}
OTHERS = {"SAL": "silver hair, camel coat, sugar on tie", "ENZO": "gold curls, 21; light jacket (Oct 3) / gray jacket / tan jumpsuit (Nov 11)",
          "REYES": "rumpled rain jacket", "HOLLOWAY": "navy suit", "THEO": "early 20s, thin, pale, red ears", "BRANCATO": "brown cardigan buttoned wrong",
          "LUCIA": "black dress, small gold cross", "TOMMY": "dark suit", "ROCCO": "huge, dark coat", "BELL": "60s, white coat over cardigan",
          "DANNY": "17, pale", "FRANKIE": "heavy, balding, good dark overcoat, face away"}

need = {}
for c in T["cuts"]:
    if c.get("kind") == "flow_job":
        need.setdefault(c["shot"], []).append([c["seg"], round(c["dur"] / 24, 2), c["src_in"], c["src_out"], c["rate"]])
jobs = []
for jid, p in sorted(P.items()):
    s = M[jid]
    if s.get("status") == "approved":
        continue
    ph = p["continuity_phase"]
    text = p["prompt"] + " " + (p.get("still_prompt") or "")
    who = [k for k, kw in (("IVY", "red-haired doctor"), ("NICO", "scarred man")) if kw in text]
    others = {k: v for k, v in OTHERS.items() if k.lower() in p["narrative_event"].lower() or k.lower() in text.lower()}
    jobs.append({
        "id": jid, "slug": p["slug"], "batch": p["batch"], "chapter": p["chapter"], "phase": ph, "status": p["status_note"].split(" - ")[0],
        "event": p["narrative_event"], "location_override": LOC.get(p["slug"], ""),
        "costume_override": {**{k: COST[k][ph] for k in who}, **others},
        "mouth": p["mouth"], "decisive": p["decisive_action"],
        "still_file": f"STILL_{jid}.png", "video_file": f"{jid}.mp4", "first_frame": f"STILL_{jid}.png (approved still; never hospital.png)",
        "needed_ranges": need.get(jid, []),
        "still_prompt": p.get("still_prompt"), "animation_prompt": p["prompt"],
    })
out = {"generated_from": "media_manifest.json + FULL70_FLOW_PROMPTS.json + film_timeline.json", "count": len(jobs),
       "rule": "free still -> QA -> one 10-credit animation with the approved still as first frame",
       "needed_ranges_format": "[segment, seconds_on_screen, source_in_s, source_out_s, speed]", "jobs": jobs}
(R / "edition20/REMAINING_JOBS.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(jobs), "remaining jobs; missing locations:", [j["id"] for j in jobs if not j["location_override"]])

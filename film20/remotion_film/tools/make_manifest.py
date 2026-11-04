#!/usr/bin/env python3
"""Author of edition20/media_manifest.json + edition20/flow_jobs.json  (v2: explicit timed cut lists).

v1 backup: edition20/out/make_manifest_v1_backup.py.  Re-run with --force after editing this file.
Jobs are written with readable slugs and numbered F01..F70 automatically in film order.

CUT LIST SEMANTICS (resolved and validated by tools/film_build.py)
  c(slug, secs, inn=None, rate=None, **kw)  footage cut. secs = screen seconds or F ("fill" = segment remainder).
        inn  = source in-point (s). None -> continue where this asset last stopped IN THIS CHAPTER.
        rate = playback speed. None -> 1.0 if the window allows, else the slowest needed down to 0.85.
               Anything the window cannot supply at 0.85x is reported UNRESOLVED (never frozen, never looped).
  g(code_id, secs, beat=...)                 authored code scene beat.
  kw: memory=True (recall treatment; required when a decisive action or another date's footage returns),
      why="..." (required for every reuse), flag="..." (required beyond 3 uses of one asset),
      same_moment=True (re-entering the identical moment in the next chapter, unseen source range only),
      crop="name" (planning note for which part of the frame a crop isolates).
Planned Flow files are ESTIMATES: nominal 7.917 s (length of all three delivered clips), planning window
0.20-7.70 s. Delivered files are measured and every range is re-checked against the real length.

Continuity phases (canon ledger, original-film-studio/docs/adaptation/canon_ledger.md)
  P0  Fri Oct 3 - Sun Oct 5   no ring/chain. Nico: WHITE plaster splint, anatomical RIGHT forearm, fingertips-elbow;
                              ruined CHARCOAL suit over a black shirt (jacket off in Bay 14 = approved hospital clip)
  P1  Mon Oct 6               emerald on Ivy's LEFT ring finger, too loose; white splint
  P2  Oct 7 - Nov 4           ring on gold chain under scrubs at work / on finger off duty; splint white to Oct 10,
                              BLACK thermoplastic, 3 velcro straps from Oct 10
  P3  Nov 5 - Nov 13 (a.m.)   plain gold band under the emerald; black splint
  P4  Nov 13 2 p.m. ->        splint OFF
  P5  April                   spring; no splint
Always: Nico's scar = thin HEALED WHITE scar through his anatomical LEFT eyebrow; injured arm anatomical RIGHT.
Never mirror footage. No readable generated text (clocks, signs, plates): code adds every legible word.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "edition20" / "media_manifest.json"
JOBS = ROOT / "edition20" / "flow_jobs.json"

STYLE = ("Painterly cinematic realism matching the reference stills: visible soft brush texture, warm sodium-orange "
         "and teal-shadow palette, shallow depth of field, 24 fps, natural restrained motion, stable faces and "
         "positions, no morphing, no smoke, no on-screen text, no readable signs, clocks, plates or logos, "
         "no subtitles, no mirror image, 16:9.")
IVY = ("Ivy Marlowe (same face as reference REF_ivy_face_hospital_1s.png): woman, 28, pale freckled skin, messy "
       "copper-red hair in a bun with a ballpoint pen stuck through it")
NICO = ("Nico Vescari (same face as reference REF_nico_face_hospital_7s.png): man, 34, dark wavy hair, short "
        "stubble, gray eyes, a thin HEALED WHITE old scar through his anatomical LEFT eyebrow (no fresh cut, no blood "
        "on the face)")
SUIT = "a ruined charcoal suit jacket over a black shirt, the jacket draped over his right shoulder"
SPLINT_W = "his anatomical RIGHT forearm in a white plaster splint from fingertips to just below the elbow"
NOJEWEL = "Ivy wears no ring, no necklace and no chain"
GARAGE = ("hospital parking garage interior, level two, 4 a.m., low solid concrete ceiling, orange sodium lights, "
          "pooled water on the concrete floor with sodium reflections, NO falling rain")
LOCK = {  # appended to every intent so later prompts inherit the wardrobe/continuity lock
 "P0": "LOCK P0 (Oct 3-5): Ivy no ring/chain; Nico white plaster splint anatomical RIGHT forearm, charcoal suit over black shirt, healed white scar anatomical LEFT eyebrow.",
 "P1": "LOCK P1 (Oct 6): emerald on Ivy's LEFT ring finger, loose; Nico white plaster splint RIGHT; scar LEFT brow.",
 "P2": "LOCK P2 (Oct 7-Nov 4): ring on a gold chain under scrubs at work, on her finger off duty; Nico splint white to Oct 10, black thermoplastic (3 velcro straps) after; scar LEFT brow.",
 "P3": "LOCK P3 (Nov 5-13 a.m.): plain gold band under the emerald; Nico black splint RIGHT; scar LEFT brow.",
 "P4": "LOCK P4 (Nov 13 2 p.m. on): Nico no splint; Ivy emerald + gold band; scar LEFT brow.",
 "P5": "LOCK P5 (April): spring light; no splint; Ivy emerald + gold band.",
}

# ------------------------------------------------------------------ 70 Flow jobs (1 output each)
J = []
def job(slug, batch, cat, phase, ch, event, prompt, *, mouth="n/a", decisive=False, replaces=None, full=False):
    J.append(dict(slug=slug, batch=batch, category=cat, continuity_phase=phase, chapter=ch, narrative_event=event,
                  prompt=prompt if full else f"INTENT (full prompt written after Batch 1 review): {prompt} {LOCK[phase]}",
                  mouth=mouth, decisive=decisive, replaces=replaces))

# ---- Batch 1: CH00 + CH01 — full prompts --------------------------------------------------------------------
job("garage_env", 1, "environment", "P0", "CH00", "Garage level 2, empty: geography before anyone is seen",
    f"Static wide shot of a {GARAGE}. A small dark-blue hatchback parked in the foreground right; further back on the "
    f"left a silver four-door sedan parked near a gray stairwell door. Nobody in frame. One light flickers once. Very "
    f"slow push-in. {STYLE}", replaces="v1 F01", full=True)
job("ivy_crouch", 1, "character", "P0", "CH00", "Ivy crouched behind her own car, counting",
    f"{IVY}, navy hospital scrubs, {NOJEWEL}. She is crouched low behind her own dark car "
    f"in a {GARAGE}; back pressed to the car, a phone charger cable in her fist, holding her breath, eyes wide, lips "
    f"pressed together, then she turns her head toward the sound. Side-on medium shot. {STYLE}",
    mouth="closed", replaces="v1 F02", full=True)
job("aftermath_wide", 1, "character", "P0", "CH00", "Aftermath: Nico upright by the sedan, Frankie slumped (no firing)",
    f"Locked-off medium-wide shot from behind the hood of a parked car in a {GARAGE}. Thirty feet away beside a silver "
    f"sedan: {NICO}, standing upright and still, {SUIT}, {SPLINT_W} held against his chest, his LEFT hand holding a "
    f"black pistol low, pointed at the floor. At his feet a DIFFERENT man, Frankie: heavy, fifties, balding, in a good "
    f"dark overcoat, slumped sitting against the sedan's rear door, his face turned away from camera; no blood "
    f"visible. Nobody fires, no muzzle flash, no smoke. Roles and positions stay fixed for the whole shot. Nobody "
    f"treats or bandages anyone. {STYLE}", mouth="closed", decisive=True, replaces="v1 F03 (respecified)", full=True)
job("frankie_hand", 1, "object", "P0", "CH00", "Frankie's open hand; the second gun a foot away",
    f"Low close insert on the pooled wet concrete of a {GARAGE}: a heavy man's open right hand resting palm-up, the "
    f"sleeve of a good dark overcoat, a black pistol lying a foot from his fingers; sodium reflections in the water. "
    f"No face, no blood. The hand does not move. {STYLE}", decisive=True, replaces="new: split from v1 F03", full=True)
job("nico_hands", 1, "object", "P0", "CH00", "Nico's hands: splinted right, gun low in the left",
    f"Close insert at waist height in a {GARAGE}: a man's anatomical RIGHT forearm in a fresh white plaster splint from "
    f"fingertips to elbow held against a charcoal suit jacket and black shirt; below it his LEFT hand loosely holds a "
    f"black pistol pointed at the wet floor. Slight breathing movement only. {STYLE}", decisive=True,
    replaces="v1 F04", full=True)
job("nico_ots", 1, "character", "P0", "CH00", "Nico addresses Ivy: over HER shoulder, eye contact, no generated speech",
    f"Over-the-shoulder shot: in the soft-focus foreground only the back of Ivy's head - her messy copper-red bun with a "
    f"ballpoint pen in it - and one navy scrub shoulder, as she hides behind a car hood. In focus twenty feet away in a "
    f"{GARAGE}: {NICO}, {SUIT}, {SPLINT_W}. He turns his head toward HER, finds her eyes and holds them; he breathes; "
    f"his mouth stays CLOSED; one slow nod toward a stairwell door. No other person in frame. {STYLE}",
    mouth="closed", replaces="v1 F05 + rejected nico.mp4", full=True)
job("ivy_reaction", 1, "character", "P0", "CH00", "Ivy's reaction on 'You were never here.' (listener)",
    f"{IVY}, navy scrubs, {NOJEWEL}. Frontal close shot from Nico's side: only her eyes and forehead above the hood of "
    f"a dark-blue hatchback in a {GARAGE}, looking straight past camera at him; frozen, breathing; then she slowly sinks "
    f"down out of sight. Mouth closed. {STYLE}", mouth="closed", replaces="v1 F06", full=True)
job("er_entrance", 1, "character", "P0", "CH01", "3:05 - Nico walks into the ER holding his arm closed",
    f"Wide shot of a night emergency waiting area, fluorescent and teal tones, tired people in plastic chairs. Automatic "
    f"doors slide open: {NICO}, in a ruined charcoal suit over a black shirt, his LEFT hand clamped around the inside of "
    f"his RIGHT forearm, blood between his fingers, walks in without hurrying. The room falls quiet; a triage nurse "
    f"behind the desk half rises; a security guard lowers his eyes to his shoes. {STYLE}", mouth="closed",
    replaces="v1 F08", full=True)
job("ivy_walks", 1, "character", "P0", "CH01", "Ivy alone walks toward him (listener)",
    f"{IVY}, navy scrubs, stethoscope, {NOJEWEL}, at a night ER triage desk with a clipboard. She looks from the frozen "
    f"staff toward someone off-screen right, pulls the pen out of her hair and walks toward him alone. Mouth closed. "
    f"{STYLE}", mouth="closed", replaces="v1 F08B", full=True)
job("bay_hands", 1, "object", "P0", "CH01", "Bay 14 hands: irrigate, then suture the right forearm",
    f"Macro close-up in a curtained ER bay with teal curtains and a warm surgical lamp: a clean straight cut across the "
    f"inside of a man's anatomical RIGHT forearm on a blue drape (black shirt sleeve rolled); gloved hands irrigate it "
    f"with a saline syringe, then begin neat stitches with a needle driver. No gore beyond a neat wound. {STYLE}",
    replaces="v1 F09+F12 merged", full=True)
job("nico_bay_cu", 1, "character", "P0", "CH01", "Nico in Bay 14: gray eyes, healed LEFT-brow scar, silent",
    f"Close-up of {NICO}, black shirt, sleeves rolled, his charcoal suit jacket hanging on the IV pole behind him, sitting "
    f"on an ER gurney under a surgical lamp, teal curtain. Three-quarter view so his anatomical LEFT eyebrow and its thin "
    f"healed white scar face camera. He watches someone working on his arm below frame, mouth CLOSED, faint amusement, "
    f"eyes flick up once. {STYLE}", mouth="closed", replaces="v1 F10", full=True)
job("ivy_bay_cu", 1, "character", "P0", "CH01", "Ivy in Bay 14: working, dry glance up (listener)",
    f"Close-up of {IVY}, navy scrubs, stethoscope, surgical gloves, {NOJEWEL}, in a curtained ER bay with teal curtains "
    f"and a warm surgical lamp. She looks down, suturing below frame, glances up at the patient with a dry, unimpressed "
    f"look, and back down. Mouth closed. {STYLE}", mouth="closed", replaces="v1 F11", full=True)
job("money_tray", 1, "object", "P0", "CH01", "The fold of hundreds: set on the tray, tucked back into his jacket",
    f"Insert over a steel instrument tray in an ER bay: a man's LEFT hand (black shirt cuff) sets a folded stack of "
    f"hundred-dollar bills beside plaster rolls; a woman's gloved hand picks it up and tucks it firmly into the inside "
    f"pocket of a charcoal suit jacket hanging on an IV pole; his white-splinted anatomical RIGHT forearm rests in frame. "
    f"No legible text on the bills. {STYLE}", replaces="v1 F13+F14 merged", full=True)

# ---- Batches 2-4: intent + continuity lock -------------------------------------------------------------------
for row in [
 # CH02
 ("ivy_frozen",2,"character","P0","CH02","Ivy frozen, hands raised, counting; stairwell door behind her","Tight on Ivy, navy scrubs, empty hands raised, counting silently, orange light; rack focus to the stairwell door behind her.","closed",False,"v1 F16"),
 ("stairs_sleeve",2,"environment","P0","CH02","Someone listening on the stairs (anonymous)","From the foot of a dark stairwell: a light-colored jacket sleeve and one sneaker stop half a flight up; lights out above; hold; no face.","n/a",True,"v1 F16B"),
 ("block_her",2,"character","P0","CH02","'Let me get to him' - Nico puts himself between them","Ivy rises from behind her car, hands out; Nico (gun low in LEFT hand) steps one pace to block her from Frankie, left palm out; Frankie slumped, face away; mouths closed.","closed",False,"v1 F17"),
 ("mopped_bay",2,"environment","P0","CH02","4:31 - the mopped bay, the officer, the dead camera","Freshly mopped empty bay where the sedan stood; a young officer's flashlight sweeps; dead camera dome; Ivy in a gray cardigan over scrubs at the edge, lips pressed.","closed",False,"v1 F18+F19 merged"),
 # CH03
 ("fbi_couch",2,"character","P0","CH03","FBI on her couch","Ivy's small apartment, Saturday 8 a.m.; Reyes (rumpled rain jacket) and Holloway (navy suit, straightening his cuffs) on her worn couch; Ivy standing in a faded T-shirt and gray cardigan; a folded subpoena on the coffee table.","closed",False,"v1 F20"),
 ("ivy_window",2,"character","P0","CH03","Ivy by the window: half a laugh, then resolve","Ivy close by her apartment window, gray cardigan, a short disbelieving laugh then a level, resolved look.","closed",False,"v1 F21 restored"),
 # CH04
 ("apt_wide",2,"character","P0","CH04","Nico in her mother's armchair in the dark; Theo beside him","Door opens on a dark apartment at 7 p.m., Ivy with groceries; Nico seated in an old armchair, white splint resting on the arm; her younger brother Theo beside him, pale, crying quietly; slow push.","closed",False,"v1 F22"),
 ("nico_armchair",2,"character","P0","CH04","Nico in the armchair (his lines placed on it, no lip-sync)","Medium close: Nico in the armchair, lamp off, leaning forward, watching Ivy, mouth closed, white splint on the armrest.","closed",False,"v1 F23"),
 ("ivy_doorway",2,"character","P0","CH04","Ivy in the doorway (listener); lifts the subpoena","Ivy in the doorway clutching the grocery bag, reacting; near the end she lifts a folded subpoena.","closed",False,"v1 F24"),
 ("supply_room",2,"environment","P0","CH04","Supply room: the door clicks shut","Hospital supply room, door clicks shut, shelves of coiled IV tubing, a shadow crosses; dim; no violence shown.","n/a",False,"v1 F26"),
 ("rocco",2,"character","P0","CH04","Rocco fills the doorway","Huge quiet man in a dark coat filling a doorway, folded crossword under his arm.","closed",False,"v1 F27"),
 ("ivy_car_dusk",2,"character","P0","CH04","Ivy by her car at dusk; she calls","Dusk, hospital lot, Ivy in gray cardigan by her car, a red line around her throat; she decides and lifts the phone to her ear.","closed",False,"v1 F28"),
 # CH05
 ("restaurant",2,"character","P0","CH05","Closed restaurant: the bargaining table","Closed Italian restaurant, chairs up except one table; Ivy faces Nico; Tommy and the lawyer Feld (blue pen, yellow pad) beside them.","closed",False,"v1 F29"),
 ("nico_tommy",2,"character","P0","CH05","Nico holds her eyes; Tommy looks at the table","Close on Nico, silent, holding someone's eyes; rack focus to Tommy beside him looking down at the table.","closed",False,"v1 F31"),
 ("ivy_terms",2,"character","P0","CH05","Ivy setting her terms (no lip-sync)","Ivy close across the table, measured, deciding.","closed",False,"new"),
 # CH06
 ("sal_arrives",3,"character","P0","CH06","Sal arrives at 1:30 with cannoli","Vescari study at night; Sal (60s, silver hair, camel coat, sugar on his tie) sets down a pastry box and talks warmly; Nico behind the desk.","closed",False,"v1 F32"),
 ("nico_desk",3,"character","P0","CH06","Nico at the desk: 'We don't touch civilians'","Nico close at the desk, listening, then hardening.","closed",False,"new"),
 ("sal_exits",3,"character","P0","CH06","Sal's hands up; he leaves the garden door open","Sal raises both hands, cannoli in one, then walks out through a garden door and leaves it open; curtain stirs; fig tree beyond.","closed",False,"v1 F33"),
 # CH07
 ("emerald_on",3,"object","P1","CH07","Rosa's emerald, far too big","A square emerald ring slides onto a woman's LEFT ring finger and turns loosely to her palm.","n/a",False,"v1 F35"),
 ("steps",3,"character","P1","CH07","Courthouse steps: reporters, cameras, Holloway","Courthouse steps, eight reporters, three cameras; Ivy and Nico descend; Holloway watching from the top step.","closed",False,"v1 F36"),
 ("kiss",3,"character","P1","CH07","The kiss for the cameras","Nico kisses Ivy, his white-splinted right forearm along her spine; camera flashes; emerald on her left hand.","closed",True,"v1 F36 split"),
 ("bolt",3,"object","P1","CH07","Crooked bolt; the ring turns","A crooked new bolt on a connecting door; Ivy's hand tests it four times; the loose emerald turns on her finger.","n/a",False,"v1 F37"),
 # CH08
 ("ring_chain",3,"object","P2","CH08","Ring onto the chain","Ivy threads the emerald onto a thin gold chain and tucks it under her navy scrub top.","n/a",False,"v1 F38"),
 ("joey_bay",3,"character","P2","CH08","Joey's chest; mobsters watch through the glass","ER trauma bay, Ivy working on a stabbed young man (clinical, not gory), suited men watching through glass; chain hidden.","closed",False,"v1 F39"),
 ("bell_asks",3,"character","P2","CH08","Dr. Bell asks about her shifts, almost casually","Morning, nurses' station: Dr. Marcus Bell (60s, tired, cardigan under white coat) leans on the counter beside Ivy, casual; she glances at him.","closed",False,"new"),
 ("bell_cries",3,"character","P2","CH08","Dr. Bell cries; she gives him until noon","Bell crying at his office desk; Ivy in the doorway, then she nods once.","closed",False,"v1 F40"),
 ("pen_kiss",3,"character","P2","CH08","The pen out of her hair","Night, Nico's study: Nico pulls the pen from Ivy's bun with his LEFT hand (black splint, after Oct 10); she kisses him; she stops.","closed",True,"v1 F41"),
 ("eyes_drawer",3,"character","P2","CH08","His eyes drop to the drawer","Close on Nico as his gaze drops to the top drawer of his desk for one beat; black splint.","closed",False,"v1 F43"),
 # CH09
 ("fig_lunch",3,"character","P2","CH09","Sunday lunch under the fig","Family garden lunch under a fig tree; Enzo (21, gold curls, gray jacket) excuses himself.","closed",False,"v1 F44"),
 ("foil_card",3,"object","P2","CH09","The foil card","Bathroom floor: a foil blister card beside a limp hand; Ivy's hand slips it into her gray cardigan pocket.","n/a",False,"v1 F45"),
 ("enzo_sleeve",3,"character","P2","CH09","Enzo grabs her sleeve","ER: Enzo on a gurney grabs Ivy's sleeve; framed from behind Ivy; no lip-sync.","closed",False,"v1 F46"),
 ("enzo_stairs",3,"character","P0","CH09","NEW Oct 3: Enzo half a flight up the stairs","Garage stairwell at 4:10 a.m., Enzo in a light jacket half a flight up, holding his breath, pistol in hand; orange light; never shows Nico firing.","closed",True,"v1 F47"),
 # CH10
 ("lincoln",3,"environment","P2","CH10","Gray Lincoln; the candy twist","A gray Lincoln at night; on the console a white twist of candy wrapper.","n/a",False,"v1 F49"),
 # CH11
 ("courtroom",3,"character","P2","CH11","Courtroom 6B","Ivy on the witness stand, emerald on her finger; Holloway at the lectern, straightening his cuffs.","closed",False,"v1 F50"),
 ("nico_gallery",3,"character","P2","CH11","Nico hears it for the first time","Nico in the gallery, still, eyes on her; black splint.","closed",False,"v1 F51"),
 ("palm_up",3,"object","P2","CH11","Palm up","Car back seat at dusk: Nico's LEFT hand open palm-up; Ivy places her hand in it (emerald on her finger).","n/a",False,"v1 F52"),
 ("drawer_midnight",3,"object","P2","CH11","The drawer at midnight","Midnight study: Ivy opens a desk drawer; under papers, a white twist of candy wrapper.","n/a",False,"v1 F53"),
 # CH12
 ("glovebox",4,"environment","P2","CH12","Sal's garage, 1:10 a.m.: the ledger","Dark private garage, gray Lincoln, glove box falls open on a black ledger; Nico's LEFT hand; black splint.","n/a",False,"v1 F54"),
 ("trunk",4,"object","P2","CH12","Trunk: receipt and tan jacket","Car trunk: a deli receipt and a boy's tan jacket from a discount rack.","n/a",False,"v1 F55"),
 ("ivy_twist",4,"character","P2","CH12","Ivy with the candy twist","Ivy in the study at night holding a white candy twist, looking up as Nico enters.","closed",False,"v1 F56"),
 ("danny_letter",4,"character","P2","CH12","Danny Bell's letter","Dawn kitchen table; Danny Bell, 17, pale, hands Ivy a folded letter.","closed",False,"v1 F57"),
 # CH13
 ("table_evidence",4,"character","P2","CH13","Evidence on the tablecloth","Dining room 7 p.m.: notebook, receipt and tan jacket on a white tablecloth between Nico and Sal; pastry box.","closed",False,"v1 F58"),
 ("sal_hands",4,"character","P2","CH13","Sal looks at his hands, then at his nephew","Sal looks at his hands, then at his nephew; a phone lies on the tablecloth.","closed",False,"v1 F59"),
 ("ivy_speaks",4,"character","P2","CH13","Reverse: Nico across from Sal, Ivy standing behind him","Reverse angle over Sal: Nico seated, black-splinted arm on the tablecloth, delivering a verdict; Ivy standing behind his shoulder, then she speaks to Sal.","closed",False,"new"),
 # CH14
 ("theo_out",4,"character","P3","CH14","Theo walks out at 12:52; the car","Theo walks out of a detention center to Ivy at her car; in the car he looks at the windshield, she listens.","closed",False,"v1 F60"),
 # CH16
 ("club_wide",4,"environment","P3","CH16","Bath Avenue club: the boy on the floor","Social club at night; Brancato in a brown cardigan buttoned wrong; his son on the floor; Enzo breathing for him.","closed",False,"v1 F61"),
 ("ivy_bags",4,"character","P3","CH16","Ivy bags the boy; Brancato's typed statement","Ivy kneels bagging the boy with a bag-valve mask; Enzo beside her; Brancato's hand draws a typed page from his cardigan (illegible).","closed",False,"new"),
 ("nico_enters",4,"character","P3","CH16","Nico enters unarmed; Ivy steps in front","Nico enters with empty hands, black splint; guns turn; Ivy steps in front of him; guns lower.","closed",True,"v1 F62"),
 ("reyes_warrant",4,"character","P3","CH16","Reyes with a warrant; Brancato arrested","Reyes in her rain jacket comes through the club's front door with agents; Brancato's wrists cuffed.","closed",True,"new"),
 # CH17
 ("visiting",4,"character","P3","CH17","Visiting room","Federal visiting room; Nico in a rumpled white shirt across from Enzo in a tan jumpsuit; a guard by the door; black splint.","closed",False,"v1 F63"),
 ("grand_jury",4,"character","P3","CH17","Grand jury room","Ivy testifying in a plain grand-jury room, hands folded, emerald with a gold band.","closed",False,"v1 F64"),
 ("splint_off",4,"object","P4","CH17","The splint comes off; his fist closes","Ivy unstraps Nico's black splint; his right fist slowly closes; he looks at his hand.","n/a",True,"v1 F65"),
 # CH18
 ("pockets_bed",4,"character","P4","CH18","Pockets emptied onto his bed","Ivy empties her cardigan pockets onto a bed: foil card, folded form, envelope, candy twist; takes the pen from her hair.","closed",False,"v1 F66"),
 ("nico_listens",4,"character","P4","CH18","Nico listening; the door open","Nico sitting on the bed edge, no splint, listening; the door behind Ivy open.","closed",False,"v1 F67"),
 # CH19
 ("april_garden",4,"environment","P5","CH19","April garden: lemon trees out of burlap","Spring garden, lemon trees being unwrapped from burlap; Lucia in black with a gold cross; Theo at the table.","closed",False,"v1 F68"),
 ("reyes_gate",4,"character","P5","CH19","Reyes at the gate","Reyes in a rain jacket at a garden gate on a warm Saturday, holding a file.","closed",False,"v1 F69"),
 ("stairs_14",4,"character","P5","CH19","Fourteen stairs","Ivy climbing a narrow staircase, counting, toward a study door at the top; final image.","closed",False,"v1 F70"),
]:
    slug, b, cat, ph, ch, ev, intent, mouth, dec, rep = row
    job(slug, b, cat, ph, ch, ev, intent, mouth=mouth, decisive=dec, replaces=rep)

for n, j in enumerate(J, 1):
    j["job_id"] = f"F{n:02d}"
SLUG = {j["slug"]: j["job_id"] for j in J}

# ------------------------------------------------------------------ shots
shots = []
def shot(**k): shots.append(k)
shot(shot_id="HOSP", kind="footage", source="hospital.mp4", window=[0.0, 7.917], status="approved", decisive=False,
     continuity_phase="P0", mouth="Ivy's lips part at 5.0-7.9 s",
     narrative_event="Bay 14, 3:40 a.m.: Ivy builds the white plaster splint on Nico's RIGHT forearm; eye contact at the end",
     permitted_reuse="n018-n019 (event). Recall only as memory and only the 0-5.0 s range.",
     audit="Correct: right forearm, no ring/chain, navy scrubs, black shirt (jacket off), ER bay. Minor: splint leaves "
           "fingers bare; Nico's left-eyebrow scar not visible; hair clip instead of pen.")
shot(shot_id="REJ_GARAGE", kind="footage", source="garage.mp4", window=[0.0, 7.917], status="rejected", decisive=False,
     continuity_phase="-", narrative_event="(none in this cut)",
     permitted_reuse="Not used in Film20. Unchanged inside the legacy Opening test.",
     audit="Ivy splints Nico in the garage (never happens: Bay 14 at 3:40); rain falls through a solid ceiling; pistol "
           "beside Nico makes him read as the victim (role reversal); Mercedes badge; smoke/morphing at 6-8 s. "
           "Replaced by garage_env, aftermath_wide, frankie_hand, nico_hands, ivy_reaction.")
shot(shot_id="REJ_NICO", kind="footage", source="nico.mp4", window=[0.0, 7.917], status="rejected", decisive=False,
     continuity_phase="-", narrative_event="(none in this cut)",
     permitted_reuse="Not used in Film20. Unchanged inside the legacy Opening test.",
     audit="Fresh bleeding cut on his RIGHT brow (canon: healed white scar, LEFT brow); charcoal jacket is correct for the "
           "date but worn over a bare chest; soft bandage instead of plaster splint; over-shoulder listener is a "
           "dark-haired MAN, not Ivy; garbled sign '4:100'. Mirroring would fix the scar side but put the injury on the "
           "wrong arm. Replaced by nico_ots (over Ivy's shoulder) + ivy_reaction.")

CODE = {
 "CODE_EHR": ("EhrChart", "n020", "Ivy types his name into the chart while he watches"),
 "CODE_MAP": ("GarageMap", "n024/n028/n029/n032/n103", "Level 2 from script facts: spot 2-14, the sedan, the stairwell; heard vs saw"),
 "CODE_WEB": ("CaseWeb", "n031", "Ivy's reasoning: Frankie -> Vescari family / FBI -> federal case -> her"),
 "CODE_SUBPOENA": ("Subpoena", "n034", "Holloway's subpoena: Thursday, 10 a.m."),
 "CODE_DEBT": ("DebtBeat", "n037", "Forty thousand dollars, a betting app, then interest"),
 "CODE_COUNT": ("Countdown", "n051", "'About ten seconds before you pass out' - at five, the shears"),
 "CODE_TERMS": ("LegalPadTerms", "n056/n059", "The terms, in blue ink, one beat per term"),
 "CODE_CONTRACT": ("ContractPage", "n084/n119/n155", "Page eleven: the left-handed line; the page count that leaks; 'She does.'"),
 "CODE_SCHEDULE": ("PocketSchedule", "n093", "Joey's pocket calendar: Ivy's October; 'Level 2. Space 2-14'"),
 "CODE_PHONE": ("PhoneNote", "n098/n099/n130/n141", "Phone beats: Priya 6:41; Bell's note vs 'Marlowe'; Reyes on speaker; Brancato 11:31"),
 "CODE_ARREST": ("ArrestTransition", "n109", "U01 non-photoreal: Theo's arrest and Holloway's trade from script facts"),
 "CODE_LOT": ("LotEvidence", "n110", "Foil card Lot 4471-B matched to the destruction form (Sept 29, 42 cards, Bell)"),
 "CODE_LEDGER": ("Ledger", "n120/n125", "Sal's ledger: C.B. monthly; Oct 1 'F.L. 20. Paid.'"),
 "CODE_LETTER": ("BellLetter", "n124", "Bell's letter ending 'Ivy, say it. Say all of it.'"),
 "CODE_CHAIN": ("EvidenceChain", "n134", "Receipt + gum -> Paulie Ferraro (one restrained link)"),
 "CODE_TIMER": ("ResusTimer", "n142", "'Four minutes twenty seconds': the bagging count"),
 "CODE_RECAP": ("EvidenceRecap", "n151", "Why no indictment: Enzo's statement, my testimony, Frankie's gun, the chart"),
 "CODE_DIVORCE": ("DivorceEnvelope", "n147/n154", "Cream envelope, Term Five, three stapled pages signed right-handed"),
 "CODE_APRIL": ("AprilEpilogue", "n159", "April consequences: Sal's letters burned unread; 141 days; June"),
}
for sid, (comp, segs, ev) in CODE.items():
    shot(shot_id=sid, kind="code", component=comp, status="code", narrative_event=ev, continuity_phase="text-exact",
         decisive=False, permitted_reuse=f"Primary {segs}; returns only where the story re-reads the object.")
for j in J:
    shot(shot_id=j["job_id"], slug=j["slug"], kind="flow_job", source=f"flow/{j['job_id']}.mp4", status="missing",
         narrative_event=j["narrative_event"], continuity_phase=j["continuity_phase"], chapter=j["chapter"],
         decisive=j["decisive"], mouth=j["mouth"], flow_job=j["job_id"])

# ------------------------------------------------------------------ cut lists
def c(slug, secs, inn=None, rate=None, **k): return dict(shot=SLUG[slug], slug=slug, secs=secs, inn=inn, rate=rate, **k)
def h(secs, inn=None, rate=None, **k): return dict(shot="HOSP", secs=secs, inn=inn, rate=rate, **k)
def g(code, secs, **k): return dict(shot=code, secs=secs, inn=None, rate=None, **k)
F = "fill"
SV = {
 # ---- CH00 Two Shots: geography, then who speaks to whom
 "n001": [c("garage_env", F)],
 "n002": [c("garage_env", 2.6), c("ivy_crouch", F)],
 "n003": [c("aftermath_wide", 6.4), c("frankie_hand", 4.0), c("nico_hands", F)],
 "n004": [c("nico_ots", 2.0), c("ivy_reaction", F)],     # n004.wav: 'Go back inside, Dr. Marlowe.' ends 1.62 s, 'You were never here.' starts 2.08 s -> cut at 2.00 s
 "n005": [c("garage_env", 2.0, inn=5.85, rate=0.85), c("emerald_on", F, inn=0.2, memory=True,
           why="flash-forward: 'Three days later, I married him' lands on the emerald going on")],
 # ---- CH01 3:05
 "n006": [c("er_entrance", 8.8, rate=0.85), c("ivy_walks", 3.3, inn=0.3), g("CODE_EHR", F, beat="arrival")],   # F09 usable 0.3-3.6 only
 "n009": [c("bay_hands", 3.0), g("CODE_EHR", 1.6, beat="complaint"), c("nico_bay_cu", F)],   # n009.wav: 'Gray eyes.' starts 4.75 s
 "n010": [c("ivy_bay_cu", F)], "n011": [c("bay_hands", F)], "n013": [c("ivy_bay_cu", F)], "n014": [c("nico_bay_cu", F)],
 "n015": [c("ivy_bay_cu", F)], "n016": [g("CODE_EHR", F, beat="name_blank")], "n017": [c("nico_bay_cu", F)],
 "n018": [h(5.5, inn=0.0, rate=0.85), g("CODE_EHR", F, beat="instructions"), c("money_tray", 1.9, inn=2.9)],   # F13 2.9-4.8: bills on the tray
 "n019": [h(F, inn=5.0)],
 "n020": [c("money_tray", 2.6, inn=5.0), g("CODE_EHR", F, beat="type")],   # F13 5.0-7.6: tucked back
 # ---- CH02 4:10
 "n024": [g("CODE_MAP", 6.0, beat="arrive"),
          c("ivy_crouch", 5.6, inn=1.0, why="CH02 re-enters the same moment: still hiding, counting"),
          c("garage_env", F, inn=2.0, why="'Footsteps. Something heavy hitting a car door. At nine, I looked.': the level she looks out on")],
 "n026": [c("block_her", F)], "n027": [c("block_her", F)],
 "n028": [c("stairs_sleeve", 8.4), g("CODE_MAP", F, beat="listening"), c("ivy_frozen", 8.4),
          c("frankie_hand", 1.2, inn=4.22, rate=0.85, same_moment=True,
          why="'I counted his breaths... the next one didn't come': Frankie's still hand, unseen range (F04 usable to 5.5 s)")],
 "n029": [g("CODE_MAP", 4.6, beat="call"), g("CODE_MAP", 5.8, beat="aftermath"), c("mopped_bay", F)],
 "n030": [c("ivy_frozen", F, inn=0.2, why="'I had a name on my tongue': the same night's frozen face, re-read as silence")],
 # ---- CH03 What I Saw
 "n031": [c("fbi_couch", 5.0), g("CODE_WEB", 6.0, beat="frankie"), g("CODE_WEB", 6.0, beat="ties"), g("CODE_WEB", F, beat="witness")],
 "n032": [c("fbi_couch", 2.4), c("aftermath_wide", 4.6, inn=0.4, memory=True, why="testimony re-reads the aftermath"),
          c("nico_hands", 4.0, inn=0.4, memory=True, why="'my splint on his right': the hands as evidence"),
          g("CODE_MAP", F, beat="heard", why="'I heard two shots. I saw what came after': the map now separates hearing from seeing")],
 "n034": [g("CODE_SUBPOENA", 4.4, beat="doc"), c("fbi_couch", 3.0, inn=3.0, why="'He offered a new name, a new city': Holloway's offer"),
          g("CODE_SUBPOENA", 4.5, beat="date"), c("ivy_window", 3.1),
          c("nico_ots", F, inn=5.6, rate=0.85, memory=True,
            why="'a man in a nice suit told me to go back inside': the moment she quotes; F06 calm tail after the door gesture")],
 "n035": [c("ivy_window", F)],
 # ---- CH04 Two Ways This Ends
 "n036": [c("apt_wide", 8.8, rate=0.85), c("ivy_doorway", F, rate=0.85)],
 "n037": [g("CODE_DEBT", 4.6), c("apt_wide", F, inn=4.0, why="Theo crying beside Nico: the later part of the same take",
          crop="theo")],
 "n038": [c("nico_armchair", 3.2, rate=0.85), g("CODE_SUBPOENA", F, beat="date", why="'If you die before Thursday, with my name in your statement': the Thursday on the subpoena")],
 "n039": [c("ivy_doorway", 1.4), c("nico_armchair", F, rate=0.85)], "n040": [c("nico_armchair", F, rate=0.85)], "n041": [c("ivy_doorway", F, inn=0.2,
          why="her question; same doorway take shown again, tighter", crop="ivy")],
 "n042": [c("nico_armchair", F)],
 "n045": [c("nico_armchair", F, inn=0.2, why="'Marry me': his proposal held on the same take, wider", crop="wide")],
 "n046": [c("er_entrance", 2.6, inn=3.0, memory=True, why="'You bled on my shoes': Friday, 3:05"), c("ivy_doorway", F, inn=2.6, why="the subpoena raised: end of the doorway take (her answer)")],
 "n051": [c("supply_room", 4.6), g("CODE_COUNT", F, beat="ten_to_five")],
 "n052": [c("rocco", F)], "n053": [c("supply_room", F, why="'My job's you': Ivy on the supply-room floor, hearing him")],
 "n054": [c("ivy_car_dusk", 5.0, rate=0.85), c("apt_wide", 2.6, inn=1.4, memory=True, why="'keep my work and my brother': Theo, as she weighs it"),
          c("fbi_couch", 2.4, inn=2.0, memory=True, why="'become someone else in a city I'd never seen': Holloway's offer"),
          c("ivy_bay_cu", 2.4, inn=2.0, memory=True, why="'or keep my work': Ivy at work in Bay 14"),
          c("ivy_car_dusk", F)],
 "n055": [c("ivy_car_dusk", F, inn=0.2, why="'I have conditions': the phone lifted, same take", crop="ivy")],
 # ---- CH05 Terms: one beat per term, interleaved with faces
 "n056": [c("restaurant", 2.3), g("CODE_TERMS", 3.4, beat="t1"), c("ivy_terms", 1.4), g("CODE_TERMS", 3.2, beat="t2"),
          g("CODE_TERMS", 3.2, beat="t3"), g("CODE_TERMS", 3.2, beat="t4"), g("CODE_TERMS", F, beat="t5t6")],
 "n059": [g("CODE_TERMS", F, beat="t7")],
 "n060": [c("restaurant", F)], "n061": [c("ivy_terms", F)],
 "n062": [g("CODE_TERMS", F, beat="t7", why="his answer is about term seven, still wet on the pad")],
 "n063": [c("ivy_terms", F)], "n064": [c("nico_tommy", F, rate=0.85)], "n065": [c("restaurant", F)], "n066": [c("nico_tommy", F)],
 # ---- CH06 The Code (Nico narrates)
 "n078": [c("sal_arrives", 8.4), c("nico_desk", F)],
 "n079": [c("sal_arrives", 3.4, inn=0.2, why="Sal's speech is quoted inside Nico's narration: the same take, closer on Sal", crop="sal"),
          g("CODE_SUBPOENA", 3.6, beat="doc", why="'A girl in the house with a federal subpoena'"),
          c("ivy_terms", F, inn=2.0, memory=True, why="'a girl in the house': Ivy as Sal sees her, at the terms table")],
 "n080": [c("nico_desk", 6.4), c("ivy_window", F, inn=0.2, memory=True, why="'We don't touch civilians': Ivy, the civilian he is protecting")],
 "n081": [c("sal_exits", 8.4), c("nico_desk", F, inn=0.2, why="Nico watching the open door: same desk take shown again", crop="wide")],
 # ---- CH07 I Do
 "n084": [g("CODE_CONTRACT", 3.4, beat="pages"), g("CODE_CONTRACT", 5.6, beat="line"), g("CODE_CONTRACT", F, beat="initials")],
 "n085": [g("CODE_CONTRACT", 1.0, beat="initials"), c("emerald_on", F, why="the wedding itself: the flash-forward's moment arrives in full")],
 "n086": [c("steps", 8.4), c("kiss", F)],
 "n087": [c("steps", F, inn=0.2, why="'Starting tonight, we're in love': the steps after the kiss, same take shown wider", crop="wide")],
 "n088": [g("CODE_TERMS", 3.0, beat="t2", why="'a bolt on my side': term two, honored"), c("bolt", F)],
 # ---- CH08 Leak
 "n092": [c("ring_chain", 8.4), c("joey_bay", 8.4), c("emerald_on", 3.0, inn=4.4, memory=True,
           why="'a wedding ring that lived against my breastbone': the same ring from its wedding morning"),
          c("joey_bay", F, inn=0.2, why="'Not on my shift': back on Joey's bay, the earlier frames again")],
 "n093": [g("CODE_SCHEDULE", 4.4, beat="month"), g("CODE_SCHEDULE", 3.8, beat="hand"), g("CODE_SCHEDULE", F, beat="level2")],
 "n094": [c("joey_bay", 3.0, inn=3.0, why="'Joey said the man who sent him...': back at Joey's bay"),
          g("CODE_SCHEDULE", 3.0, beat="month", why="'Only the hospital had my schedule'"), c("bell_asks", F)],
 "n096": [c("bell_cries", 8.4), c("bell_asks", 4.0, inn=0.2, memory=True,
           why="'A man had asked about my schedule. Bell gave it.': the casual question, re-read"),
          g("CODE_SCHEDULE", 3.0, beat="level2", why="'Bell gave it': the schedule that reached Joey's pocket"),
          c("bell_cries", F, inn=0.2, why="'I said yes': back on Bell, same take")],
 "n097": [c("pen_kiss", 8.5, rate=0.85), c("kiss", 4.8, inn=0.2, memory=True, why="'No cameras': the kiss that was for the cameras, by contrast"),
          c("eyes_drawer", F, inn=0.2, rate=0.85)],
 "n098": [g("CODE_PHONE", 4.6, beat="call"), g("CODE_PHONE", F, beat="note")],
 "n099": [g("CODE_PHONE", 6.4, beat="texts"), g("CODE_PHONE", F, beat="compare")],
 "n100": [c("nico_tommy", 3.0, inn=2.0, memory=True, why="'Tommy.' - one of the four who knew; seen at the terms table"),
          c("rocco", 3.0, inn=2.0, memory=True, why="'Rocco.' - the second name"),
          c("sal_arrives", 3.0, inn=2.0, memory=True, why="'And Nico's uncle Sal.' - the name that matters"),
          c("eyes_drawer", F)],
 # ---- CH09 Enzo
 "n101": [c("fig_lunch", 8.0), c("foil_card", 7.4), g("CODE_LOT", F, beat="card", why="'Oxycodone, thirty milligrams': the sticker, close")],
 "n102": [c("enzo_sleeve", F)],
 "n103": [c("enzo_stairs", 8.4, memory=True), c("garage_env", 3.0, inn=0.2, memory=True,
           why="the confession re-reads the garage (empty level)"),
          g("CODE_MAP", F, beat="stairs", why="the confession places Enzo half a flight up: the map gains its missing figure")],
 "n104": [c("stairs_sleeve", 4.4, inn=0.2, memory=True, why="'Enzo was the light jacket on the stairs': the anonymous sleeve, now named"),
          c("enzo_sleeve", F, inn=0.2, why="'what he said in that bay stays with me': Ivy and Enzo again, same take")],
 # ---- CH10 Lot 4471-B  (U01 = CODE_ARREST, non-photoreal, no paid job)
 "n109": [g("CODE_ARREST", 5.6, beat="lights"), g("CODE_ARREST", 5.0, beat="trade"), g("CODE_ARREST", F, beat="car")],
 "n110": [c("foil_card", 3.6, inn=0.2, memory=True, why="'The sticker on Enzo's card said Lot 4471-B'"),
          g("CODE_LOT", 7.4, beat="card", why="the card's lot number, now matched against Theo's pills and the form"), g("CODE_LOT", 7.4, beat="form"), g("CODE_LOT", F, beat="link")],
 "n111": [c("lincoln", F)],
 # ---- CH11 Yes
 "n112": [c("courtroom", 8.6), c("kiss", F, inn=4.0, memory=True, why="'About the courthouse kiss'")],
 "n113": [c("nico_gallery", F)],
 "n115": [c("courtroom", F, inn=0.2, why="'Yes. I love him': back on Ivy on the stand, same take, closer", crop="ivy")],
 "n116": [c("courtroom", 3.6, inn=4.4, why="'The judge denied the motion': the courtroom again"), c("nico_gallery", 3.0), c("palm_up", 8.4),
          c("bolt", F, inn=0.2, memory=True, why="'At my door he said...': the connecting door with her bolt")],
 "n119": [g("CODE_CONTRACT", 6.4, beat="leak", why="the contract returns because its page count now proves a leak"),
          c("drawer_midnight", 8.4), c("eyes_drawer", F, inn=0.2, memory=True,
          why="the drawer his eyes dropped to when she said 'Sal' - the plant pays off")],
 # ---- CH12 The Glove Box (Nico narrates)
 "n120": [c("lincoln", 3.4, inn=4.4, why="'I had found this car once before': the same Lincoln, unseen range"),
          c("glovebox", 8.4), g("CODE_LEDGER", 6.0, beat="cb"), g("CODE_LEDGER", F, beat="fl")],
 "n121": [c("trunk", 8.4), c("sal_exits", F, inn=0.2, memory=True,
          why="'Sal carried me out of that house': the uncle who raised him, the night he left the door open")],
 "n123": [c("ivy_twist", F)],
 "n124": [c("danny_letter", 8.4), g("CODE_LETTER", 7.4, beat="letter"), g("CODE_LETTER", 7.0, beat="form_cash"),
          g("CODE_LETTER", F, beat="closing")],
 # ---- CH13 Uncle
 "n125": [c("table_evidence", 8.4), g("CODE_LEDGER", 5.4, beat="laid_out", why="'the notebook, the receipt, the jacket': the evidence on the table"),
          c("stairs_sleeve", 3.2, inn=3.0, memory=True, why="'send Enzo down them': the stairs"), c("trunk", F, inn=2.0, memory=True,
          why="'the receipt, the jacket': the trunk where Nico found them")],
 "n126": [g("CODE_LOT", 3.6, beat="form", why="'Better ours, from a hospital': the destruction form"), c("ivy_speaks", F)],
 "n127": [c("ivy_speaks", 2.6), c("foil_card", F, inn=3.6, memory=True, why="'I breathed for your nephew for four minutes. On your pills.'")],
 "n128": [c("table_evidence", 5.0, inn=0.2, why="Nico's verdict over the evidence: same take, wider", crop="wide"),
          c("sal_exits", 3.4, inn=3.0, memory=True, why="'You'll go to Cefalu': Sal leaving through the door he once left open"),
          c("ivy_speaks", F, inn=0.2, why="Nico's verdict, Ivy behind him: same take shown again", crop="nico")],
 "n129": [c("sal_hands", F)],
 "n130": [g("CODE_PHONE", 4.4, beat="speaker", why="the phone on the tablecloth: 'Agent Reyes, on speaker'"), c("sal_hands", F, inn=0.2,
          why="'Of course you called her, sweetheart': Sal again, same take", crop="sal")],
 # ---- CH14 The Paper Trail
 "n134": [g("CODE_CHAIN", 4.4, beat="receipt"), g("CODE_CHAIN", F, beat="link")],
 "n135": [g("CODE_PHONE", F, beat="call_nico",
           why="'I called Reyes first, on purpose. Then Nico.': his answer comes over her phone")],
 "n136": [g("CODE_CHAIN", 2.6, beat="confessed", why="'Paulie confessed.'"), c("theo_out", 8.4),
          c("ivy_car_dusk", F, inn=3.0, memory=True, why="'I'd been so busy keeping him safe': the night she chose the deal for him")],
 # ---- CH16 Bath Avenue
 "n141": [g("CODE_PHONE", 5.0, beat="brancato", why="'At 11:31 my phone rang. Carmine Brancato.'",
           flag="Ivy's phone is a recurring prop; this is its 4th chapter (call log, not a new document)"),
          c("fig_lunch", 4.0, inn=3.5, memory=True, why="'Lucia found Enzo's room empty': Enzo leaving the family table, re-read"),
          c("club_wide", 8.4), c("enzo_sleeve", F, inn=0.2, memory=True,
          why="'Enzo... had asked for the doctor': the night he grabbed her sleeve")],
 "n142": [c("ivy_bags", 8.4), g("CODE_TIMER", 6.0, beat="count"), c("club_wide", F, inn=0.2,
          why="'The boy coughed': back to the room, same wide take", crop="wide")],
 "n143": [c("club_wide", F, inn=3.0, why="his voice from the door: the room turns, same wide take", crop="wide")],
 "n144": [c("nico_enters", 8.4), c("ivy_bags", 3.4, inn=2.0, why="'His son was breathing because of me': the boy under her hands"),
          c("nico_gallery", 3.4, inn=2.0, memory=True, why="'I would stand in a courtroom and say who': Courtroom 6B, where she already did"),
          c("club_wide", F, inn=3.4, why="'In my house, we don't point guns at the doctor': Brancato, end of the wide take",
            flag="4th view of the club wide inside one continuous scene: it is the only angle on Brancato's ruling")],
 "n145": [c("reyes_warrant", F)],
 "n146": [c("ivy_bags", F, inn=3.0, why="'because you were in that room': Ivy kneeling where she stayed", crop="ivy")],
 # ---- CH17 The Second Oath
 "n147": [c("visiting", 8.4), c("enzo_stairs", 3.4, inn=0.2, memory=True, why="'about the gun': the gun Enzo held on the stairs"),
          g("CODE_DIVORCE", 5.0, beat="envelope", why="'leave it on the hall table': the envelope he is asking for"),
          c("visiting", F, inn=0.2, why="'That means I don't ask': back on Nico in the visiting room, same take", crop="nico")],
 "n148": [c("grand_jury", 6.4), c("aftermath_wide", 4.6, inn=0.2, memory=True, why="sworn testimony: the aftermath as evidence, not a new event"),
          c("frankie_hand", 4.6, inn=0.2, memory=True, why="'A second gun near his open hand'"),
          c("nico_hands", F, inn=0.2, memory=True, why="'a gun in his left hand, pointed at the floor... his right hand in my splint'")],
 "n149": [c("grand_jury", F, inn=0.2, why="'Did you see who fired?': back in the room, same take from its start", crop="wide")],
 "n150": [c("grand_jury", F, why="her answer, same take continuing")],
 "n151": [g("CODE_RECAP", 8.8, beat="four"), h(5.6, inn=0.0, rate=0.85, memory=True,
           why="'six weeks less one day': the same splint the day she built it"), c("splint_off", F, rate=0.85)],
 "n152": [c("splint_off", F)],
 # ---- CH18 Term Six
 "n154": [g("CODE_DIVORCE", 5.0, beat="envelope2", why="the envelope is now on the table"), g("CODE_DIVORCE", 5.0, beat="pages"),
          g("CODE_DIVORCE", F, beat="signature")],
 "n155": [c("pockets_bed", 8.4), g("CODE_CONTRACT", 8.0, beat="she_does", why="the contract's meaning changes: 'She does.'"),
          g("CODE_CONTRACT", F, beat="term_six")],
 "n156": [c("nico_listens", 8.4), c("er_entrance", 4.0, inn=0.2, memory=True,
           why="'I chose that emergency room': the night he walked in"),
          h(4.4, inn=0.4, rate=0.9, memory=True, why="'I read Marlowe on your badge': Bay 14, the doctor he chose"),
          c("pockets_bed", F, inn=0.2, why="'That was the other reason': Ivy on his bed, hearing it")],
 "n157": [c("money_tray", 2.6, inn=5.0, memory=True, why="Nico names this exact moment: the money back in his pocket"),
          g("CODE_EHR", F, beat="type", memory=True, why="'and typed my name anyway': the chart she typed while he watched")],
 # ---- CH19 April
 "n159": [c("april_garden", 8.4), g("CODE_APRIL", 6.0, beat="theo"), c("enzo_sleeve", 3.4, inn=4.0, memory=True,
           flag="4th appearance of Enzo's ER take: the epilogue closes his arc", why="'Enzo is in a program upstate'"),
          g("CODE_APRIL", 6.0, beat="sal_letters"), c("danny_letter", 3.4, inn=4.4, memory=True,
           why="'Danny Bell is back at school': the boy from the letter"), g("CODE_APRIL", F, beat="june")],
 "n160": [c("reyes_gate", 8.6), c("april_garden", F, inn=0.2, why="'Nico would read it in the Post by Friday': the garden he is sitting in", crop="wide")],
 "n161": [c("stairs_14", 8.4), c("aftermath_wide", 3.0, inn=4.4, memory=True, flag="closing bookend: the film's first image returns once as the line that opened it",
           why="'Two shots. That's all it took to start all of this': the film's first image, once more"),
          c("stairs_14", F, inn=0.2, why="'One yes, said out loud': the climb's opening frames close the film", crop="wide")],
}

if __name__ == "__main__":
    if (MAN.exists() or JOBS.exists()) and "--force" not in sys.argv:
        sys.exit("manifest already exists; edit the JSON or pass --force")
    assert len(J) == 70 and len(SLUG) == 70, "plan must be exactly 70 unique jobs"
    cats = {}
    for j in J: cats[j["category"]] = cats.get(j["category"], 0) + 1
    # carry review verdicts over a regeneration: never silently reset an approval or a rejection
    KEEP = ("status", "review_log", "approved_range", "default_crop", "identity_check", "excluded_ranges")
    if MAN.exists():
        old = {x["shot_id"]: x for x in json.loads(MAN.read_text())["shots"]}
        for sh in shots:
            o = old.get(sh["shot_id"])
            if o and sh["kind"] in ("flow_job", "footage"):
                for k in KEEP:
                    if k in o: sh[k] = o[k]
    MAN.write_text(json.dumps({
        "version": 2,
        "about": "Media manifest v2. 'segment_cuts' lists explicit timed cuts per narration segment; tools/film_build.py "
                 "resolves them against exact source windows and enforces reuse, phase, overlap and gap rules. status: "
                 "approved | code | missing | delivered_unreviewed | rejected. Final export needs every cut approved or code.",
        "continuity_phases": __doc__.split("Continuity phases")[1].strip(),
        "planned_file": {"nominal_length_s": 7.917, "usable_window": [0.2, 7.7], "min_rate": 0.85},
        "shots": shots, "segment_cuts": SV}, indent=1, ensure_ascii=False), encoding="utf-8")
    JOBS.write_text(json.dumps({"version": 2, "style_suffix": STYLE, "category_counts": cats, "jobs": J}, indent=1,
                               ensure_ascii=False), encoding="utf-8")
    print(len(J), "jobs", cats, len(shots), "shots", len(SV), "segments mapped")

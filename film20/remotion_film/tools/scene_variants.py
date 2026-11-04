#!/usr/bin/env python3
"""Scene variants built ONLY from approved footage + finished code scenes + the complete narration.
Writes edition20/scene_tests/<tag>.json and builds src/film/data/film_timeline_<tag>.json via film_build.py --variant.
A variant fails (exit 2) if any cut in its range is planned/unreviewed or unresolved."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_manifest import c, g, h, F, SV  # noqa: E402

R = Path(__file__).resolve().parent.parent
OUTD = R / "edition20/scene_tests"; OUTD.mkdir(parents=True, exist_ok=True)

OPENING = {  # n001-n024 (~2:03): opening + "3:05" + first beat of "4:10"
 "n001": [c("garage_env", F)],
 "n002": [c("garage_env", 3.0), g("CODE_MAP", F, beat="heard", why="'what a life ending sounds like in concrete': the two shots, heard")],
 "n003": [g("CODE_MAP", 5.6, beat="saw", why="'I looked over the hood': what she saw, drawn (the aftermath shot is not delivered yet)"),
          c("frankie_hand", 5.6, inn=0.2), h(F, inn=0.0, rate=0.85, memory=True,
          why="'the plaster splint I had built thirty minutes earlier, in bay fourteen, with my own two hands'")],
 "n004": [c("nico_ots", 2.0, inn=0.3), c("ivy_reaction", F)],   # F06_R1: eye contact 0.3-2.4 s; cut to Ivy at the sentence break
 "n005": [g("CODE_CONTRACT", F, beat="pages", why="flash-forward: 'Three days later I married him' - the marriage, as a contract")],
 "n006": [g("CODE_EHR", 7.0, beat="arrival"), c("ivy_walks", 3.3, inn=0.3), c("bay_hands", 2.1, inn=0.2),
          g("CODE_EHR", F, beat="name_blank")],
 "n009": [c("bay_hands", 2.6), g("CODE_EHR", 1.6, beat="complaint"), c("nico_bay_cu", F)],
 "n018": [h(5.5, inn=0.0, rate=0.85, why="the splint being built: the event the opening already glimpsed"),
          g("CODE_EHR", F, beat="instructions"), c("money_tray", 1.9, inn=2.9)],
 "n024": [g("CODE_MAP", 7.0, beat="arrive", why="back to the garage at 4:08: the map returns for the 4:10 chapter"), c("garage_env", 5.0, inn=0.2, why="Level two again: the place she hid"),
          g("CODE_MAP", F, beat="heard")],
}
VARIANTS = {"approved_opening": {"segments": ["n001", "n024"], "cuts": OPENING}}

ok = True
for tag, v in VARIANTS.items():
    data = {"tag": tag, "segments": v["segments"], "segment_cuts": v["cuts"]}
    f = OUTD / f"{tag}.json"; f.write_text(json.dumps(data, indent=1))
    r = subprocess.run([sys.executable, str(R / "tools/film_build.py"), "--variant", str(f)], cwd=R, capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-800:])
    for line in r.stdout.splitlines():
        if "NOT REAL" in line: print(line)
    ok &= r.returncode == 0
sys.exit(0 if ok else 2)

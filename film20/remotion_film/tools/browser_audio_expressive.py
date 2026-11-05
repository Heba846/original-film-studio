#!/usr/bin/env python3
"""edition20/out/browser_audio_expressive.json = browser_audio_batches.json + tts_text per batch, with sparing Eleven v3/v4 audio tags.
Text and parts are copied unchanged. A tag goes in front of a part only when the mood changes. Heba batches start with
[American accent]. Check: tts_text minus the [tags] equals the original batch text exactly."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
B = json.loads((R / "edition20/out/browser_audio_batches.json").read_text())
CH = {s["id"]: s["chapter"] for s in json.loads((R / "src/film/data/film_timeline.json").read_text())["segments"]}
HEBA_CH = {"CH00": "[tense] [hushed]", "CH01": "[calm] [wry]", "CH02": "[whispers] [tense]", "CH03": "[shaken]",
           "CH04": "[guarded]", "CH05": "[firmly]", "CH07": "[softly]", "CH08": "[focused]", "CH09": "[urgent]",
           "CH10": "[anxious]", "CH11": "[steady]", "CH13": "[firmly]", "CH14": "[quietly]", "CH16": "[tense]",
           "CH17": "[steady]", "CH18": "[warmly]", "CH19": "[warmly] [relieved]"}
HEBA_SEG = {"n004": "[shaky]", "n005": "[quietly]", "n020": "[firmly]", "n026": "[urgent]", "n035": "[determined]",
            "n039": "[coldly]", "n041": "[firmly]", "n046": "[defiant]", "n052": "[breathless]", "n063": "[hesitant]",
            "n085": "[softly] [wistful]", "n097": "[softly]", "n098": "[shaken] [sad]", "n102": "[shaken]", "n104": "[quietly]",
            "n115": "[emotional] [steady]", "n124": "[firmly]", "n127": "[firmly] [controlled anger]", "n136": "[sad]",
            "n144": "[firmly]", "n150": "[steady]", "n155": "[warmly] [playful]", "n161": "[warmly] [hopeful]"}
NICO_CH = {"CH01": "[low] [guarded]", "CH04": "[low] [intense]", "CH05": "[controlled]", "CH06": "[low] [intense]",
           "CH07": "[warmly]", "CH08": "[softly]", "CH10": "[calm]", "CH11": "[softly]", "CH12": "[quietly] [remorseful]",
           "CH13": "[low]", "CH16": "[calm]", "CH17": "[low]", "CH18": "[warmly]", "CH19": "[wry] [warmly]"}
NICO_SEG = {"n116": "[softly] [warmly]", "n109": "[calm] [steady]", "n085": "[warmly]", "n097": "[softly]", "n079": "[low]"}
OTHER = {"sal": {"n079": "[soft-spoken] [menacing]", "n081": "[warmly]", "n125": "[coldly] [calm]", "n126": "[coldly]",
                 "n129": "[bitter]", "n130": "[wry]"},
         "theo": {"n036": "[tearful]", "n136": "[hurt] [quietly]"}, "enzo": {"n102": "[breathless] [remorseful]", "n142": "[quietly] [firmly]"},
         "rocco": {"*": "[quietly] [flat]"}, "joey": {"*": "[weakly]"}, "holloway": {"*": "[sharp]"},
         "brancato": {"*": "[quiet command]"}, "lucia": {"*": "[wry] [warmly]"}}
def tag_for(role, sid):
    if role == "heba": return HEBA_SEG.get(sid) or HEBA_CH.get(CH[sid], "")
    if role == "nico": return NICO_SEG.get(sid) or NICO_CH.get(CH[sid], "[low]")
    o = OTHER.get(role, {}); return o.get(sid) or o.get("*", "")
for b in B["batches"]:
    out, prev = [], None
    for p in b["parts"]:
        t = tag_for(b["voice_role"], p["segment_id"])
        out.append((t + " " if t and t != prev else "") + p["text"]); prev = t or prev
    tts = "\n\n".join(out)
    if b["voice_role"] == "heba": tts = "[American accent] " + tts
    b["tts_text"] = tts; b["tts_chars"] = len(tts)
    assert re.sub(r"\[[^\]]+\] ", "", tts) == b["text"], b["id"]
    assert len(tts) <= 5000, (b["id"], len(tts))
B["about_expressive"] = ("Paste tts_text (not text) into Eleven v4 with the voice for voice_role. Bracketed audio tags steer delivery and are NOT "
                         "spoken; the words between them are the verbatim script. Alignment uses 'text'/'parts' and ignores the tags. "
                         "If a tag is ever spoken aloud, the intake flags it and that batch is regenerated.")
B["tag_policy"] = "sparing: one tag per mood change; no SSML, no sound effects, no stage directions read aloud"
(R / "edition20/out/browser_audio_expressive.json").write_text(json.dumps(B, indent=1, ensure_ascii=False))
for b in B["batches"]: print(b["id"], b["chars"], "->", b["tts_chars"], len(re.findall(r"\[[^\]]+\]", b["tts_text"])), "tags")

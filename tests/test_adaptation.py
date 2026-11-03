"""Full-film adaptation: counts, canon facts, structure, loadable project. Not voice or image tests."""
import csv
import io
import json
import re
from pathlib import Path

import pytest
from ofs import adaptation as ad, narration as nar, project as proj, prompts as pr, validate as val

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "docs" / "adaptation" / "script.md"
PROJECT = ROOT / "projects" / "married_to_the_don_full_film"


@pytest.fixture(scope="module")
def parsed():
    return ad.parse_script(SCRIPT)


def all_text(parsed):
    return " ".join(s["text"] for s in parsed["segments"])


def test_word_count_is_computed_and_within_justified_range(parsed):
    st = ad.word_stats(parsed)
    assert 3500 <= st["total_words"] <= 5000
    assert st["total_words"] == sum(st["words_by_chapter"].values()) == sum(st["words_by_speaker"].values())
    assert st["optional_cta_words"] < 80 and "NOT measured" in st["estimate_note"]
    assert all(v > 1800 for v in st["estimated_seconds_at_wpm"].values())      # a 30+ minute film, not a trailer


def test_committed_outputs_match_the_script(parsed):
    wc = json.loads((ROOT / "docs/adaptation/word_count.json").read_text())
    assert wc["total_words"] == ad.word_stats(parsed)["total_words"]
    rows = list(csv.DictReader(io.StringIO((ROOT / "docs/adaptation/segments.csv").read_text(encoding="utf-8-sig"))))
    js = json.loads((ROOT / "docs/adaptation/segments.json").read_text())
    assert [r["text"] for r in rows] == [s["text"] for s in parsed["segments"]] == [s["text"] for s in js]
    assert {r["speaker"] for r in rows} == {"heba", "lion"}


def test_speaker_rules_nico_is_lion_everyone_else_is_heba(parsed):
    # every non-Nico non-POV scene is narrated by Heba: Lion never narrates Ivy's chapters
    ivy_only = {"CH01", "CH02", "CH03", "CH07", "CH08", "CH10", "CH11", "CH13", "CH14", "CH19"}
    for s in parsed["segments"]:
        if s["chapter"] in ivy_only and s["speaker"] == "lion":
            assert len(s["text"].split()) < 60          # short Nico lines only, never narration
    heba_quotes = [s for s in parsed["segments"] if s["speaker"] == "heba" and '"' in s["text"]]
    assert heba_quotes                                                           # Heba quotes the other characters


def test_opening_times_and_hearing_vs_seeing(parsed):
    t = all_text(parsed)
    for frag in ("3:05", "At 3:20", "By 3:40", "4:10"):
        assert frag in t
    assert "thirty minutes earlier" in t and "forty minutes earlier" not in t
    assert "I heard two shots. I saw what came after." in t                      # first account
    assert "I heard two shots. I saw what was in his hands afterward." in t     # sworn testimony
    # The hand injury is never used as proof he could not shoot left-handed
    assert not re.search(r"couldn'?t (have )?(fired|shot|pull)", t, re.I)
    assert not re.search(r"(hand|splint|tendon)[^.]{0,60}(proves?|proof|couldn't have)", t, re.I)


def test_canon_reveals_evidence_and_motives_present(parsed):
    t = all_text(parsed)
    for frag in ("Frankie Lombardi", "Lot 4471-B", "anise", "gray Lincoln", "F.L. Twenty. Paid.", "Carmine wanted the port",
                 "Cefalù", "Bianca", "Paulie", "Rosaria Amato", "Term six", "She does.", "I love you, Ivy",
                 "Yes. I love him.", "I shot Frankie", "Marlowe", "Somebody in your house paid me"):
        assert frag in t, frag
    assert "Ivy, I'm sorry. I couldn't live with it. Tell Danny I tried." in t and "maybe four times" in t   # fake note


def test_ring_is_on_the_chain_not_a_generic_pendant(parsed):
    t = all_text(parsed)
    assert "threaded his grandmother's emerald onto a thin gold chain" in t
    assert "pendant" not in t.lower()
    shot = next(s for s in parsed["shots"] if s["id"] == "s28")
    assert "chain" in shot["continuity"] and "emerald" in shot["continuity"]


def test_ending_is_a_complete_hea_with_optional_cta_last(parsed):
    segs = parsed["segments"]
    t = all_text(parsed)
    assert "The door stayed open that night" in t and "I love you, Ivy" in t and "put the divorce papers in the oven" in t
    assert "April" in t and "fourteen stairs" in t
    cta = [s for s in segs if s["optional_cta"]]
    assert len(cta) == 1 and segs[-1] is cta[0]                                  # CTA is optional, last, and short
    assert "cliffhanger" not in t.lower()


def test_story_beats_in_order_and_climax_gets_room(parsed):
    order = ["CH01", "CH02", "CH03", "CH04", "CH05", "CH06", "CH07", "CH08", "CH09", "CH10", "CH11", "CH12", "CH13",
             "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]
    assert [c["id"] for c in parsed["chapters"]][1:] == order
    wc = ad.word_stats(parsed)["words_by_chapter"]
    assert wc["CH16"] + wc["CH17"] + wc["CH18"] > 2 * min(wc["CH10"], wc["CH15"])    # last act not rushed
    assert min(wc[c] for c in ("CH16", "CH17", "CH18")) > min(wc.values())


def test_first_30_seconds_deliver_the_title_promise(parsed):
    t = 0.0
    for s in parsed["segments"]:
        t += ad.spoken_words(s["text"]) / 150 * 60 + s["pause_after"]
        if "Go back inside, Dr. Marlowe" in s["text"]:
            break
    assert t < 45                                                                # ESTIMATE (150 wpm + pauses), not measured
    assert parsed["segments"][0]["text"].startswith("Two shots.")


def test_both_speakers_have_meaningful_share(parsed):
    sp = ad.word_stats(parsed)["words_by_speaker"]
    assert sp["lion"] > 800 and sp["heba"] > 3000
    nico_pov = ["CH06"]
    for c in nico_pov:
        assert all(s["speaker"] == "lion" for s in parsed["segments"] if s["chapter"] == c and not s["text"].startswith('"'))


def test_project_loads_validates_and_is_honest_about_missing_assets():
    p = proj.load(PROJECT)
    assert p["audio"]["narration_mode"] == "segments" and len(p["shots"]) >= 50 and len(p["narration_segments"]) >= 150
    r = val.validate(p, PROJECT)
    assert {i.code for i in r.errors} == {"missing_file", "segment_no_audio"}      # nothing else wrong
    assert all(g["audio"] == "" for g in p["narration_segments"])                   # no invented recordings
    assert all(not s["reference_audio"] for s in p["speakers"])
    assert sorted(x for s in p["shots"] for x in s["segments"]) == sorted(g["id"] for g in p["narration_segments"])
    pl = nar.plan(p, PROJECT)
    assert not pl["all_measured"] and "ESTIMATED" in pl["note"]
    assert abs(sum(s["duration"] for s in p["shots"]) - pl["total"] - 0.5) < 1.0      # shot durations follow narration estimate


def test_project_matches_script_and_prompts_carry_continuity():
    p = proj.load(PROJECT)
    items = pr.build_prompts(p)
    assert len(items) == len(p["shots"])
    assert all("Painterly illustrated realism" in i["image_prompt"] for i in items)
    assert all("OPTIONAL motion" in i["optional_motion_prompt"] and "gore" in i["negative_prompt"] for i in items)
    tagged = {sh["id"]: sh["characters"] for sh in p["shots"]}
    nico = [i for i in items if "nico" in tagged[i["shot_id"]]]
    assert len(nico) > 25 and all("LEFT eyebrow" in i["image_prompt"] and "gray eyes" in i["image_prompt"] for i in nico)
    ivy = [i for i in items if "ivy" in tagged[i["shot_id"]]]
    assert len(ivy) > 25 and all("bun" in i["image_prompt"] and "pen" in i["image_prompt"] for i in ivy)
    assert not [w for w in val.validate(p, PROJECT).warnings if w.code == "untagged_character"]
    assert any("thin gold chain" in " ".join(i["continuity_notes"]) for i in ivy)


def test_source_novel_is_not_in_the_repo_or_zip_inputs():
    big = [f for f in ROOT.rglob("*") if f.is_file() and ".git" not in f.parts and f.suffix.lower() in (".pdf", ".epub", ".docx")]
    assert not big
    for f in (ROOT / "docs" / "adaptation").glob("*"):
        assert f.stat().st_size < 600_000


def test_no_long_verbatim_runs_of_source_in_ledger_docs():
    """The ledger may carry short page-referenced quotes, never chapters of the source."""
    led = (ROOT / "docs/adaptation/canon_ledger.md").read_text(encoding="utf-8")
    assert led.count("[p.") > 60 and len(led.split()) < 6000
    for line in led.splitlines():
        for q in line.split('"')[1::2]:
            assert len(q.split()) < 30, "long quotation in ledger: " + q[:60]


def test_full_film_narration_assembles_at_scale_from_synthetic_tones(tmp_path):
    """162 segments through one ffmpeg graph. Tones, NOT voices: proves assembly/timing only."""
    import subprocess
    from ofs import media
    p = proj.load(PROJECT)
    m = tmp_path / "media" / "film"
    m.mkdir(parents=True)
    for g in p["narration_segments"]:
        f = m / f"{g['id']}.wav"
        subprocess.run([media.tool("ffmpeg"), "-y", "-v", "error", "-f", "lavfi", "-i",
                        f"sine=frequency={200 if g['speaker'] == 'heba' else 120}:duration=0.2", str(f)], check=True)
        g["audio"] = f"media/film/{g['id']}.wav"
    out = tmp_path / "n.wav"
    pl = nar.assemble(p, tmp_path, out)
    expected = len(p["narration_segments"]) * 0.2 + sum(g["pause_after"] for g in p["narration_segments"])
    assert pl["all_measured"] and abs(pl["total"] - expected) < 1.0
    assert abs(media.probe(out)["duration"] - expected) < 1.0

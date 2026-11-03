import json

from conftest import shot
from ofs import project as proj, prompts as pr, srt


def test_save_load_roundtrip_unicode(tmp_path):
    p = proj.normalize({"title": "فيلم قصير", "script": "مرحبا", "shots": [shot(1)]})
    path = proj.save(tmp_path, p)
    assert path.name == "project.json"
    assert proj.load(tmp_path) == p
    assert json.loads(path.read_text(encoding="utf-8"))["title"] == "فيلم قصير"


def test_normalize_fills_defaults_and_keeps_unknown_keys():
    p = proj.normalize({"shots": [{"id": "a"}], "custom": 1})
    assert p["shots"][0]["duration"] == 5.0 and p["audio"]["music_volume"] == 0.25 and p["custom"] == 1


def test_project_name_rules():
    assert proj.valid_project_name("my film_2") and proj.valid_project_name("فيلم")
    assert not proj.valid_project_name("../x") and not proj.valid_project_name("a/b") and not proj.valid_project_name("")


def test_srt_parse_and_errors():
    cues, errs = srt.parse("﻿1\r\n00:00:01,000 --> 00:00:02,500\r\nمرحبا\r\n\r\n2\r\n00:00:05,000 --> 00:00:04,000\r\nbad\r\n")
    assert len(cues) == 1 and cues[0]["end"] == 2.5 and cues[0]["text"] == "مرحبا" and len(errs) == 1
    assert srt.parse(srt.format_srt(cues))[0] == [{**cues[0], "index": 1}]


def test_prompts_include_bible_and_continuity():
    p = proj.normalize({
        "style": "Watercolor", "characters": [{"id": "m", "name": "Mira", "description": "girl, black hair",
                                              "wardrobe": "yellow coat", "continuity_notes": "scarf is red"}],
        "locations": [{"id": "l", "name": "Tower", "description": "white tower", "lighting": "dusk",
                       "continuity_notes": "on the left"}],
        "shots": [shot(1, characters=["m"], location="l", action="Mira climbs", camera="low angle",
                       continuity_notes="rain"), shot(2)]})
    items = pr.build_prompts(p)
    assert [i["shot_id"] for i in items] == ["s1", "s2"]
    ip = items[0]["image_prompt"]
    for frag in ("Watercolor", "black hair", "yellow coat", "white tower", "dusk", "Mira climbs", "low angle", "16:9"):
        assert frag in ip
    assert "scarf is red" in " ".join(items[0]["continuity_notes"]) and "on the left" in " ".join(items[0]["continuity_notes"])
    assert items[0]["negative_prompt"] and "OPTIONAL motion" in items[0]["video_prompt"] and items[0]["still_prompt"] == ip
    assert "Image prompt" in pr.to_markdown(p, items) and pr.to_csv(items).count("\n") >= 3

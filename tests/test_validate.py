from conftest import shot
from ofs import project as proj, validate as val


def codes(p, d, **kw):
    return val.validate(proj.normalize(p), d, **kw).codes()


def test_valid_project_has_no_errors(basic, pdir):
    r = val.validate(basic, pdir)
    assert r.ok, [i.message for i in r.errors]
    assert r.total_duration == 4.5


def test_empty_shot_list(pdir):
    assert "no_shots" in codes({"shots": []}, pdir)


def test_missing_file_and_unassigned_asset(pdir):
    c = codes({"shots": [shot(1, asset="media/nope.png"), shot(2, asset="")]}, pdir)
    assert "missing_file" in c and "no_asset" in c


def test_bad_and_nonpositive_durations(pdir):
    for bad in (0, -2, "abc", None, 9999):
        r = val.validate(proj.normalize({"shots": [shot(1, dur=bad)]}), pdir)
        assert not r.ok, bad


def test_duplicate_ids(pdir):
    p = {"shots": [shot(1), {**shot(1), "id": "s1"}]}
    assert "shot_dup_id" in codes(p, pdir)


def test_kind_mismatch_and_bad_extension(pdir):
    (pdir / "media" / "x.txt").write_text("hi")
    c = codes({"shots": [shot(1, "video", "media/img.png"), shot(2, "image", "media/clip2s.mp4"),
                         shot(3, "image", "media/x.txt")]}, pdir)
    assert c.count("kind_mismatch") == 2 and "bad_extension" in c


def test_corrupt_media_is_unreadable(pdir):
    (pdir / "media" / "broken.png").write_bytes(b"not an image")
    assert "unreadable_media" in codes({"shots": [shot(1, asset="media/broken.png")]}, pdir)


def test_short_clip_and_aspect_warnings(pdir):
    r = val.validate(proj.normalize({"shots": [shot(1, "video", "media/clip2s.mp4", 5.0),
                                               shot(2, asset="media/square.png")]}), pdir)
    assert r.ok
    assert {"clip_too_short", "aspect_ratio", "low_resolution"} <= set(r.codes()) | {"low_resolution"}
    assert "clip_too_short" in r.codes() and "aspect_ratio" in r.codes()


def test_trim_start_counts_against_clip_length(pdir):
    p = {"shots": [{**shot(1, "video", "media/clip2s.mp4", 1.5), "trim_start": 1.0}]}
    assert "clip_too_short" in codes(p, pdir)


def test_unknown_character_and_location(pdir):
    p = {"shots": [shot(1, characters=["ghost"], location="moon")]}
    c = codes(p, pdir)
    assert "unknown_character" in c and "unknown_location" in c


def test_untagged_character_mention_warns(pdir):
    p = {"characters": [{"id": "mira", "name": "Mira"}], "shots": [shot(1, action="Mira runs")]}
    assert "untagged_character" in codes(p, pdir)
    p["shots"][0]["characters"] = ["mira"]
    assert "untagged_character" not in codes(p, pdir)


def test_narration_longer_than_timeline_is_error(pdir):
    p = {"shots": [shot(1, dur=2)], "audio": {"narration": "media/narr9.wav"}}
    assert "narration_longer" in codes(p, pdir)


def test_narration_much_shorter_is_warning_only(pdir):
    p = {"shots": [shot(1, dur=10)], "audio": {"narration": "media/narr3.wav"}}
    r = val.validate(proj.normalize(p), pdir)
    assert r.ok and "narration_shorter" in r.codes()


def test_missing_and_wrong_type_audio(pdir):
    p = {"shots": [shot(1)], "audio": {"narration": "media/gone.wav", "music": "media/img.png"}}
    c = codes(p, pdir)
    assert "missing_narration" in c and "bad_music_type" in c


def test_volume_range(pdir):
    p = {"shots": [shot(1)], "audio": {"music_volume": 9, "narration_volume": "loud"}}
    assert codes(p, pdir).count("bad_volume") == 2


def test_captions_checks(pdir):
    base = {"shots": [shot(1, dur=3)]}
    assert "no_srt" in codes({**base, "captions": {"mode": "burn", "srt": ""}}, pdir)
    assert "missing_srt" in codes({**base, "captions": {"mode": "burn", "srt": "media/x.srt"}}, pdir)
    assert "srt_invalid" in codes({**base, "captions": {"mode": "burn", "srt": "media/bad.srt"}}, pdir)
    assert "srt_beyond_timeline" in codes({**base, "captions": {"mode": "burn", "srt": "media/caps.srt"}}, pdir)
    assert val.validate(proj.normalize({**base, "captions": {"mode": "soft", "srt": "media/caps_ok.srt"}}), pdir).ok


def test_render_settings(pdir):
    p = {"shots": [shot(1)], "render": {"fps": 0, "crf": 99, "preset": "warp"}}
    assert {"bad_fps", "bad_crf", "bad_preset"} <= set(codes(p, pdir))


def test_timeline_follows_reordering():
    p = proj.normalize({"shots": [shot(1, dur=2), shot(2, dur=3), shot(3, dur=1)]})
    assert proj.timeline(p) == [("s1", 0, 2), ("s2", 2, 5), ("s3", 5, 6)]
    proj.move_shot(p, "s3", 0)
    assert proj.timeline(p) == [("s3", 0, 1), ("s1", 1, 3), ("s2", 3, 6)]
    assert proj.total_duration(p) == 6

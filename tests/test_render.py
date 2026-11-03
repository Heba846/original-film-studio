import json
import re
import subprocess

import pytest
from conftest import shot
from ofs import media, project as proj, render as rn

FF = media.tool("ffmpeg")


def streams(path):
    r = subprocess.run([media.tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return {s["codec_type"]: s for s in d["streams"]}, d["format"], d["streams"]


def mean_volume(path):
    r = subprocess.run([FF, "-hide_banner", "-i", str(path), "-af", "volumedetect", "-vn", "-f", "null", "-"],
                       capture_output=True, text=True)
    return float(re.search(r"mean_volume: (-?[\d.]+) dB", r.stderr).group(1))


def test_mixed_render_specs_and_manifest(basic, pdir):
    out = pdir / "output" / "film.mp4"
    res = rn.render(basic, pdir, out)
    s, fmt, _ = streams(out)
    v = s["video"]
    assert (v["width"], v["height"]) == (1920, 1080)
    assert v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == "30/1"
    assert abs(float(fmt["duration"]) - 4.5) < 0.1
    assert "audio" in s  # silent track is added so every player/YouTube is happy
    m = json.loads((pdir / "output" / "film.render.json").read_text())
    assert m["production_type"] == "mixed_stills_and_supplied_video" and m["ai_video_generated_by_this_tool"] is False
    assert [x["id"] for x in m["shots"]] == ["s1", "s2", "s3"] and m["shots"][2]["start"] == 3.0
    assert "generated no video" in fmt["tags"]["comment"]
    assert res["production_type"] == m["production_type"]


def test_image_only_is_labelled_animatic(pdir):
    p = proj.normalize({"shots": [shot(1, motion="zoom_in"), shot(2, motion="pan_left"), shot(3, motion="zoom_out"),
                                  shot(4, motion="pan_right", transition="fade")]})
    res = rn.render(p, pdir, pdir / "o.mp4")
    assert res["production_type"] == "animatic_slideshow" and "ANIMATIC" in res["disclosure"]
    assert abs(float(streams(pdir / "o.mp4")[1]["duration"]) - 4.0) < 0.1


def test_reorder_and_duration_change_alter_output_length(basic, pdir):
    proj.move_shot(basic, "s3", 0)
    basic["shots"][0]["duration"] = 3.0  # s3 now first, 3s
    rn.render(basic, pdir, pdir / "o.mp4")
    m = json.loads((pdir / "o.render.json").read_text())
    assert [x["id"] for x in m["shots"]] == ["s3", "s1", "s2"]
    assert abs(float(streams(pdir / "o.mp4")[1]["duration"]) - 6.0) < 0.1


def test_short_clip_is_held_to_full_duration(pdir):
    p = proj.normalize({"shots": [shot(1, "video", "media/clip2s.mp4", 4.0)]})
    rn.render(p, pdir, pdir / "o.mp4")
    assert abs(float(streams(pdir / "o.mp4")[1]["duration"]) - 4.0) < 0.1


def test_narration_music_and_soft_captions(basic, pdir):
    basic["audio"].update(narration="media/narr3.wav", music="media/music.wav", music_volume=0.3)
    basic["captions"] = {"srt": "media/caps_ok.srt", "mode": "soft"}
    rn.render(basic, pdir, pdir / "o.mp4")
    s, fmt, all_s = streams(pdir / "o.mp4")
    assert "audio" in s and any(x["codec_type"] == "subtitle" for x in all_s)
    assert abs(float(fmt["duration"]) - 4.5) < 0.1
    assert mean_volume(pdir / "o.mp4") > -60  # real audio, not silence


def test_burned_captions_change_pixels(pdir):
    base = {"shots": [shot(1, dur=3)]}
    rn.render(proj.normalize(base), pdir, pdir / "plain.mp4")
    rn.render(proj.normalize({**base, "captions": {"srt": "media/caps_ok.srt", "mode": "burn"}}), pdir, pdir / "burn.mp4")
    def frame(f, o):
        subprocess.run([FF, "-y", "-v", "error", "-ss", "0.8", "-i", str(f), "-frames:v", "1", str(o)], check=True)
        return o.read_bytes()
    assert frame(pdir / "plain.mp4", pdir / "a.png") != frame(pdir / "burn.mp4", pdir / "b.png")


def test_music_volume_is_controllable(pdir):
    def run(vol):
        p = proj.normalize({"shots": [shot(1, dur=2)], "audio": {"music": "media/music.wav", "music_volume": vol}})
        rn.render(p, pdir, pdir / f"m{vol}.mp4")
        return mean_volume(pdir / f"m{vol}.mp4")
    loud, quiet = run(1.0), run(0.1)
    assert loud - quiet > 12  # 0.1 gain is -20 dB; allow for the fade-out and codec


def test_music_shorter_than_film_loops_and_output_length_is_exact(pdir):
    p = proj.normalize({"shots": [shot(1, dur=5)], "audio": {"music": "media/music.wav"}})  # music is 2s
    rn.render(p, pdir, pdir / "o.mp4")
    assert abs(float(streams(pdir / "o.mp4")[1]["duration"]) - 5.0) < 0.1
    # audio track must span the film too (looped music), not stop after 2s
    assert float(streams(pdir / "o.mp4")[0]["audio"]["duration"]) > 4.8


def test_invalid_project_refuses_to_render_and_writes_nothing(pdir):
    p = proj.normalize({"shots": [shot(1), shot(2, asset="media/missing.png")]})
    out = pdir / "o.mp4"
    with pytest.raises(rn.ValidationFailed) as e:
        rn.render(p, pdir, out)
    assert "missing_file" in e.value.report.codes() and not out.exists()

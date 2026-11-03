"""Narration segments: real assembly with synthetic audio, measured with ffprobe/ffmpeg."""
import json
import re
import shutil
import subprocess

import pytest
from conftest import make_wav, shot
from ofs import media, narration as nar, project as proj, render as rn, validate as val

FF = media.tool("ffmpeg")


def dur(path):
    r = subprocess.run([media.tool("ffprobe"), "-v", "error", "-show_entries", "format=duration:stream=sample_rate,channels",
                        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return float(d["format"]["duration"]), d["streams"][0]


def vol(path, ss, t):
    r = subprocess.run([FF, "-hide_banner", "-ss", str(ss), "-t", str(t), "-i", str(path), "-af", "volumedetect",
                        "-vn", "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"mean_volume: (-?[\d.inf]+) dB", r.stderr)
    return float(m.group(1)) if m and m.group(1) != "-inf" else -200.0


@pytest.fixture
def seg_project(pdir):
    make_wav(pdir / "media" / "a.wav", 1.0, 440, 0.6, sr=22050)   # stereo-less, 22.05 kHz on purpose
    make_wav(pdir / "media" / "b.wav", 1.5, 220, 0.6, sr=44100)
    make_wav(pdir / "media" / "c.wav", 0.8, 330, 0.05, sr=48000)   # quiet
    p = proj.normalize({
        "title": "seg", "speakers": [{"id": "heba", "display_name": "Heba"}, {"id": "lion", "display_name": "Lion"}],
        "narration_segments": [
            {"id": "n1", "speaker": "heba", "text": "One.", "audio": "media/a.wav", "pause_after": 0.5},
            {"id": "n2", "speaker": "lion", "text": "Two two.", "audio": "media/b.wav", "pause_after": 2.0},
            {"id": "n3", "speaker": "heba", "text": "Three.", "audio": "media/c.wav", "pause_after": 0.0}],
        "shots": [shot(1, segments=["n1"], dur=1.5), shot(2, segments=["n2"], dur=3.5), shot(3, segments=["n3"], dur=0.8)],
        "audio": {"narration_mode": "segments"}})
    return p


def test_plan_measures_real_audio(seg_project, pdir):
    pl = nar.plan(seg_project, pdir)
    assert pl["all_measured"] and abs(pl["total"] - (1.0 + 0.5 + 1.5 + 2.0 + 0.8)) < 0.05
    assert [r["start"] for r in pl["segments"]][1] == pytest.approx(1.5, abs=0.03)


def test_plan_flags_estimates_when_no_audio():
    p = proj.normalize({"narration_segments": [{"id": "x", "speaker": "s", "text": "word " * 26}]})
    pl = nar.plan(p, ".")
    assert not pl["all_measured"] and "ESTIMATED" in pl["note"] and pl["segments"][0]["duration"] == pytest.approx(10.0, abs=0.1)


def test_assemble_is_one_wav_with_real_silence_pauses(seg_project, pdir):
    out = pdir / "output" / "n.wav"
    pl = nar.assemble(seg_project, pdir, out)
    d, st = dur(out)
    assert abs(d - 5.8) < 0.06 and pl["total"] == pytest.approx(5.8, abs=0.06)
    assert st["sample_rate"] == "48000" and st["channels"] == 1   # mixed input rates -> one format
    assert vol(out, 0.1, 0.8) > -25                                 # segment 1 audible
    assert vol(out, 1.05, 0.4) < -80                                # 0.5 s pause is digital silence
    assert vol(out, 3.1, 1.8) < -80                                 # the 2 s pause after n2
    assert vol(out, 1.6, 1.3) > -25 and vol(out, 5.05, 0.7) < vol(out, 0.1, 0.8) - 15   # order a, b, then quiet c
    assert (pdir / "output" / "n.timing.json").is_file()


def test_reordering_segments_changes_assembly(seg_project, pdir):
    seg_project["narration_segments"].reverse()      # c(0.8 quiet), b(1.5+2.0), a(1.0+0.5)
    out = pdir / "o.wav"
    nar.assemble(seg_project, pdir, out)
    assert vol(out, 0.05, 0.7) < vol(out, 0.9, 1.4) - 15   # quiet c first, then loud b


def test_assemble_refuses_segment_without_audio(seg_project, pdir):
    seg_project["narration_segments"][1]["audio"] = ""
    with pytest.raises(ValueError, match="n2"):
        nar.assemble(seg_project, pdir, pdir / "o.wav")


def test_sync_shot_durations_uses_measured_timing(seg_project, pdir):
    pl = nar.plan(seg_project, pdir)
    res = nar.sync_shot_durations(seg_project, pl, tail=0.5)
    d = [s["duration"] for s in res["project"]["shots"]]
    assert d == [pytest.approx(1.5, abs=0.03), pytest.approx(3.5, abs=0.03), pytest.approx(1.3, abs=0.03)]
    assert res["estimated"] == []


def test_validation_of_segments(seg_project, pdir):
    base = proj.normalize(seg_project)
    assert val.validate(base, pdir).ok, [i.message for i in val.validate(base, pdir).errors]

    def codes(mut):
        p = proj.normalize(json.loads(json.dumps(base)))
        mut(p)
        return val.validate(p, pdir).codes()
    assert "unknown_speaker" in codes(lambda p: p["narration_segments"][0].update(speaker="ghost"))
    assert "segment_dup_id" in codes(lambda p: p["narration_segments"][1].update(id="n1"))
    assert "segment_no_text" in codes(lambda p: p["narration_segments"][0].update(text=" "))
    assert "bad_pause" in codes(lambda p: p["narration_segments"][0].update(pause_after=-1))
    assert "segment_no_audio" in codes(lambda p: p["narration_segments"][0].update(audio=""))
    assert "segment_missing_audio" in codes(lambda p: p["narration_segments"][0].update(audio="media/nope.wav"))
    assert "unreadable_segment_audio" in codes(lambda p: (p["narration_segments"][0].update(audio="media/bad.wav"),
                                                         (pdir / "media" / "bad.wav").write_bytes(b"junk")))
    assert "unknown_segment" in codes(lambda p: p["shots"][0].update(segments=["zzz"]))
    assert "segment_in_two_shots" in codes(lambda p: p["shots"][1].update(segments=["n1"]))
    assert "no_segments" in codes(lambda p: p.update(narration_segments=[]))
    assert "bad_narration_mode" in codes(lambda p: p["audio"].update(narration_mode="magic"))
    assert "shot_shorter_than_narration" in codes(lambda p: p["shots"][1].update(duration=1.0))


def test_narration_longer_than_timeline_blocks_render(seg_project, pdir):
    for s in seg_project["shots"]:
        s["duration"] = 0.6                       # 1.8 s of picture vs 5.8 s of narration
    r = val.validate(seg_project, pdir)
    assert "narration_longer" in r.codes() and not r.ok


def test_editorial_segment_is_reported_not_blocked(seg_project, pdir):
    seg_project["narration_segments"][2]["editorial"] = True
    r = val.validate(seg_project, pdir)
    assert r.ok and "editorial_proposal" in r.codes()


def test_full_render_from_segments_and_manifest(seg_project, pdir):
    seg_project["narration_segments"][1]["source"] = "generated"
    seg_project["narration_segments"][2].update(editorial=True)
    seg_project = nar.sync_shot_durations(seg_project, nar.plan(seg_project, pdir), tail=0.5)["project"]
    out = pdir / "output" / "film.mp4"
    res = rn.render(seg_project, pdir, out)
    r = subprocess.run([media.tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(out)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    total = nar.plan(seg_project, pdir)["total"] + 0.0
    assert abs(float(d["format"]["duration"]) - sum(s["duration"] for s in seg_project["shots"])) < 0.1
    assert float(d["format"]["duration"]) >= total - 0.05            # picture covers all narration
    assert any(s["codec_type"] == "audio" for s in d["streams"])
    assert vol(out, 0.1, 0.8) > -30 and vol(out, 3.1, 1.8) < -60    # pause survives into the final mix
    m = json.loads((pdir / "output" / "film.render.json").read_text())
    assert m["narration"] == "segments" and m["synthetic_voice_segments"] == ["n2"]
    assert m["narration_segments"][2]["editorial_proposal"] and "synthetic" in m["voice_disclosure"].lower()
    assert m["production_type"] == "animatic_slideshow" and m["ai_video_generated_by_this_tool"] is False


def test_old_v1_project_loads_validates_and_renders_unchanged(pdir):
    old = {"version": 1, "title": "old", "shots": [shot(1, dur=1.0), shot(2, "video", "media/clip2s.mp4", 2.0)],
           "audio": {"narration": "media/narr3.wav", "music": "media/music.wav", "narration_volume": 1.0, "music_volume": 0.3,
                     "duck_music": True}, "captions": {"srt": "media/caps_ok.srt", "mode": "soft"},
           "render": {"fps": 30, "crf": 21, "preset": "veryfast"}}
    (pdir / "project.json").write_text(json.dumps(old), encoding="utf-8")
    p = proj.load(pdir)
    assert p["speakers"] == [] and p["narration_segments"] == [] and p["audio"]["narration_mode"] == "file"
    assert val.validate(p, pdir).ok
    res = rn.render(p, pdir, pdir / "o.mp4")
    assert res["narration"] == "media/narr3.wav" and res["synthetic_voice_segments"] == []
    assert abs(dur(pdir / "o.mp4")[0] - 3.0) < 0.1
    proj.save(pdir, p)
    saved = json.loads((pdir / "project.json").read_text(encoding="utf-8"))
    assert saved["version"] == 2 and saved["audio"]["narration"] == "media/narr3.wav" and saved["shots"][0]["id"] == "s1"


def test_committed_v1_demo_fixture_still_loads():
    from pathlib import Path
    p = proj.load(Path(__file__).parent / "fixtures" / "old_v1_project.json")
    assert p["title"].startswith("The Last Lantern") and len(p["shots"]) == 6 and p["narration_segments"] == []
    assert p["audio"]["narration"] == "media/narration_placeholder.wav"

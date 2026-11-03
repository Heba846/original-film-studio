import json
import subprocess

import pytest

from ofs import captions as cap, clips, media, project as proj


def covered_len(plan, xf=clips.XFADE):
    n = plan["pieces"]
    return sum(p["out_len"] for p in n) - xf * (len(n) - 1)


@pytest.mark.parametrize("dur,clips_", [(5, [8]), (8, [8]), (12, [8, 8]), (30, [8, 8]), (34, [8]), (62, [8, 8, 8])])
def test_plan_hits_duration_without_long_loops(dur, clips_):
    pl = clips.plan_shot(dur, clips_)
    assert pl["covered"]
    assert abs(covered_len(pl) - dur) < 0.01
    for p in pl["pieces"]:
        # no piece ever plays longer than its source clip allows (no freeze, no stretch beyond slow limit)
        assert p["src_len"] <= clips_[p["clip"]] + 1e-6
        assert p["speed"] >= clips.MAX_SLOW - 1e-9
        assert p["out_len"] >= clips.MIN_PIECE - 1e-6 or len(pl["pieces"]) == 1


def test_enough_clips_means_no_reuse_no_slowdown():
    pl = clips.plan_shot(20, [8, 8, 8])
    assert pl["speed"] == 1.0 and pl["reused_seconds"] == 0 and all(p["pass_no"] == 0 for p in pl["pieces"])


def test_shortfall_slows_then_reuses_and_reports():
    pl = clips.plan_shot(34, [8, 8])
    assert pl["slowed"] and pl["reused_seconds"] > 0
    assert any(p["pass_no"] >= 1 for p in pl["pieces"])


def test_no_clips_is_uncovered_not_padded():
    pl = clips.plan_shot(10, [])
    assert not pl["covered"] and pl["missing_seconds"] == 10 and pl["pieces"] == []


def test_discovery_patterns(tmp_path):
    root = tmp_path / "media" / "clips"
    (root / "s02").mkdir(parents=True)
    for n in ("s01.mp4", "s01_2.mp4", "s01_10.mp4", "s011.mp4", "s03-a.mp4"):
        (root / n).write_bytes(b"x")
    (root / "s02" / "b.mp4").write_bytes(b"x")
    (root / "s02" / "a.mp4").write_bytes(b"x")
    names = lambda sid: [p.name for p in clips.discover({"id": sid}, tmp_path)]
    assert names("s01") == ["s01.mp4", "s01_2.mp4", "s01_10.mp4"]
    assert names("s02") == ["a.mp4", "b.mp4"]
    assert names("s03") == ["s03-a.mp4"]
    assert names("s09") == []


def test_command_never_freezes():
    shot = {"id": "s1", "duration": 20, "transition": "cut"}
    cmd = clips.shot_command("ffmpeg", shot, ["a.mp4", "b.mp4"], clips.plan_shot(20, [8, 8]), "o.mp4", 24, 20, "veryfast")
    s = " ".join(cmd)
    assert "tpad" not in s and "freeze" not in s and "stop_mode" not in s and "xfade" in s


def test_split_and_wrap():
    txt = ("I looked over the hood. A man was sliding down the side of a silver sedan, a gun a foot from his open "
           "hand, and the man standing over him held a different gun.")
    parts = cap.split_text(txt)
    assert all(len(p) <= cap.MAX_CUE_CHARS for p in parts) and " ".join(parts) == txt
    assert all(len(l) <= 50 for p in parts for l in cap._wrap(p.split()).split("\n"))


def test_cues_stay_inside_segment_windows():
    proj_ = {"narration_segments": [{"id": "a", "text": "One. Two three four."}, {"id": "b", "text": "Five."}]}
    timing = {"segments": [{"id": "a", "start": 0.0, "speech_end": 4.0}, {"id": "b", "start": 5.0, "speech_end": 6.0}]}
    cues = cap.build_cues(proj_, timing)
    assert cues[0]["start"] == 0 and cues[-1]["end"] <= 6.0
    assert all(c["end"] > c["start"] for c in cues)
    assert all(a["end"] <= b["start"] + 1e-6 for a, b in zip(cues, cues[1:]))


def test_chapters_format_and_rules():
    script = "## CH00 | Two Shots\n## CH01 | 3:05\n## CH02 | Third\n"
    timing = {"segments": [{"id": "a", "start": 2.0}, {"id": "b", "start": 70.0}, {"id": "c", "start": 3725.0}]}
    chs = cap.chapters({"script": script}, timing, {"a": "CH00", "b": "CH01", "c": "CH02"})
    text, problems = cap.chapters_text(chs)
    assert text.splitlines() == ["0:00 Two Shots", "1:10 3:05", "1:02:05 Third"] and not problems


def test_clip_filled_shot_renders_exact_length_for_real(tmp_path):
    """Real ffmpeg: synthetic 8 s test-pattern clips (NOT story footage) fill a 21 s shot."""
    ff = media.tool("ffmpeg")
    if not ff:
        pytest.skip("no ffmpeg")
    cdir = tmp_path / "media" / "clips"
    cdir.mkdir(parents=True)
    for i, src in enumerate(("testsrc2", "smptebars")):
        subprocess.run([ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"{src}=s=1280x720:r=24:d=8",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cdir / f"s01_{i}.mp4")], check=True)
    shot = {"id": "s01", "duration": 21.0, "transition": "cut"}
    paths = clips.discover(shot, tmp_path)
    pl = clips.plan_shot(21.0, [8.0, 8.0])
    out = tmp_path / "o.mp4"
    subprocess.run(clips.shot_command(ff, shot, paths, pl, out, 24, 28, "ultrafast"), check=True)
    info = media.probe(out)
    assert abs(info["duration"] - 21.0) < 0.15 and (info["width"], info["height"]) == (1920, 1080)

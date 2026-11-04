import json
import shutil

import pytest

from ofs import batch, media, narration as nar, project as proj, tts

pytestmark = pytest.mark.skipif(not shutil.which("espeak-ng"), reason="espeak-ng stand-in not installed")


def mk_project(tmp_path, n=3):
    segs = [{"id": f"n{i}", "speaker": "heba" if i % 2 else "lion", "text": f"Segment number {i} is spoken here.",
             "pause_after": 0.5} for i in range(n)]
    p = proj.normalize({"title": "t", "speakers": [{"id": "heba", "consent_confirmed": True},
                                                   {"id": "lion", "consent_confirmed": True}],
                        "narration_segments": segs, "audio": {"narration_mode": "segments"}})
    return p


def test_standin_requires_explicit_flag(tmp_path):
    with pytest.raises(tts.TTSError):
        batch.render_all(mk_project(tmp_path), tmp_path, engine="espeak")


def test_chatterbox_without_references_refuses(tmp_path):
    with pytest.raises(tts.TTSError, match="missing reference voices"):
        batch.render_all(mk_project(tmp_path), tmp_path, engine="chatterbox", vdir=tmp_path / "nope")


def test_batch_resume_loudness_and_pause(tmp_path):
    p = mk_project(tmp_path)
    r1 = batch.render_all(p, tmp_path, engine="espeak", stand_in_ok=True)
    assert r1["ok"] and r1["rendered_now"] == 3
    assert all(-20.5 < x < -18.5 for x in r1["loudness_range_lufs"])  # very short clips drift up to ~1 LU
    side = json.loads((tmp_path / "media/generated/n0.wav.json").read_text())
    assert side["stand_in"] is True and "NOT a clone" in side["note"]
    r2 = batch.render_all(p, tmp_path, engine="espeak", stand_in_ok=True)
    assert r2["rendered_now"] == 0 and r2["already_done"] == 3          # resume
    pl = nar.plan(p, tmp_path)
    assert pl["all_measured"] and all(abs(s["end"] - s["speech_end"] - 0.5) < 1e-3 for s in pl["segments"])
    out = tmp_path / "n.wav"
    res = nar.assemble(p, tmp_path, out)
    assert abs(media.probe(out)["duration"] - res["total"]) < 0.1


def test_prep_voices_builds_reference(tmp_path):
    v = tmp_path / "voices" / "heba"
    v.mkdir(parents=True)
    import subprocess
    subprocess.run([media.tool("ffmpeg"), "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=f=220:d=12",
                    str(v / "a.wav")], check=True)
    res = batch.prep_voices(["heba", "lion"], tmp_path / "voices")
    assert res["heba"]["seconds"] == 12.0 and (v / "_ref.wav").is_file()
    assert "error" in res["lion"]

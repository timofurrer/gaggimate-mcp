"""Regression test: firmware .slog v7 (uint32 t, 14 fields incl. wp, 30-byte samples)."""

from pathlib import Path

from gaggimate_mcp.parsers.shot import parse_binary_shot

FIXTURE = Path(__file__).parent / "fixtures" / "shot_v7_000096.slog"


def test_parses_real_v7_shot():
    shot = parse_binary_shot(FIXTURE.read_bytes(), "96")

    assert shot.version == 7
    assert shot.fields_mask == 0x3FFF
    assert shot.sample_count == len(shot.samples) == 142
    assert not shot.incomplete
    assert shot.duration == 35336
    assert shot.weight == 37.9
    assert [p.phase_name for p in shot.phases] == ["Prefill", "Compressing", "Dripping", "Pressurize", "Extraction"]

    # t is absolute elapsed ms in v6+, so the last sample lands on the shot duration
    assert shot.samples[0]["t"] == 109
    assert shot.samples[-1]["t"] == 35336
    # values stay physically plausible when samples are aligned correctly
    assert all(80 <= s["ct"] <= 100 for s in shot.samples)
    assert max(s["cp"] for s in shot.samples) == 10.9
    assert shot.samples[-1]["v"] == 37.9
    assert max(s["wp"] for s in shot.samples) == 76.0

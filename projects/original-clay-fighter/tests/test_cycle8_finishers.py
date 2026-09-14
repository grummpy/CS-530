from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from fighter.presentation.finishers import (
    FinisherPlayback,
    RollingFrameCache,
    finisher_root,
    resolve_finisher_variant,
)
from fighter.sim.bits import Action
from fighter.sim.enums import MatchPhase, ResultReason
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.tools.perf import write_raw_report


def _ko_game() -> SessionKernel:
    game = SessionKernel(p1_id="master_chef", p2_id="mr_president")
    game.match.p2.health = 0
    game.tick()
    return game


def test_ko_lifecycle_emits_one_finisher_and_deterministically_skips() -> None:
    game = _ko_game()
    assert game.match.phase is MatchPhase.KO_HOLD
    assert game.match.result and game.match.result.reason is ResultReason.KO
    assert game.match.result.finisher_variant == "master_chef_vs_mr_president"
    frozen = game.match.result
    for _ in range(30):
        game.tick()
    assert game.match.phase is MatchPhase.FINISHER_WINDOW
    assert [event.kind for event in game.presentation_events()] == ["finisher"]
    game.tick((InputFrame.from_held(0, Action.START), InputFrame()))
    assert game.match.phase is MatchPhase.RESULTS and game.match.result == frozen
    assert [event.kind for event in game.presentation_events()] == ["result"]


def test_timeout_bypasses_finisher_and_reset_tears_lifecycle_down() -> None:
    game = SessionKernel()
    game.match.round_ticks, game.match.p1.health = 1, 900
    game.tick()
    assert game.match.phase is MatchPhase.RESULTS
    game.reset()
    assert game.match.phase is MatchPhase.FIGHT and game.match.result is None


def test_variant_validation_rejects_partial_or_unsafe_media(tmp_path: Path) -> None:
    assert resolve_finisher_variant("master_chef_vs_mr_president") is not None
    assert resolve_finisher_variant("../escape") is None
    root = tmp_path / "finishers"
    (root / "partial" / "frames").mkdir(parents=True)
    (root / "partial" / "frames" / "000.png").touch()
    assert resolve_finisher_variant("partial", root) is None


def test_all_authored_variants_resolve_to_exactly_thirty_frames() -> None:
    variants = sorted(path.name for path in finisher_root().iterdir() if path.is_dir())
    assert len(variants) == 12
    assert all(
        (resolved := resolve_finisher_variant(name)) and len(resolved.frames) == 30
        for name in variants
    )


def test_rolling_cache_is_byte_bounded_lru_and_teardown_releases_memory() -> None:
    class Surface:
        def __init__(self, size: tuple[int, int]) -> None:
            self.size = size

        def get_size(self) -> tuple[int, int]:
            return self.size

        def get_bytesize(self) -> int:
            return 4

    cache = RollingFrameCache(32)
    assert cache.put(0, Surface((2, 2))) and cache.put(1, Surface((2, 2)))
    cache.get(0)
    assert cache.put(2, Surface((2, 2)))
    assert cache.get(1) is None and cache.bytes_used <= 32
    cache.clear()
    assert cache.bytes_used == 0


def test_media_failure_has_one_readable_diagnostic_and_never_retries() -> None:
    playback = FinisherPlayback("missing_variant")
    assert playback.fallback and playback.diagnostic
    diagnostic = playback.diagnostic
    assert not playback.preload_one(SimpleNamespace()) and playback.diagnostic == diagnostic
    for _ in range(10):
        playback.teardown()
        assert playback.cache.bytes_used == 0


def test_decode_failure_falls_back_once() -> None:
    playback = FinisherPlayback("master_chef_vs_mr_president")
    pygame = SimpleNamespace(
        image=SimpleNamespace(load=lambda _: (_ for _ in ()).throw(OSError("bad"))),
        error=RuntimeError,
    )
    assert not playback.preload_one(pygame) and playback.fallback
    assert playback.diagnostic == "Finisher media failed — showing results."


def test_invalid_decoded_surface_falls_back_once() -> None:
    source = SimpleNamespace(convert_alpha=lambda: object())
    playback = FinisherPlayback("master_chef_vs_mr_president")
    pygame = SimpleNamespace(
        image=SimpleNamespace(load=lambda _: source),
        error=RuntimeError,
    )
    assert not playback.preload_one(pygame) and playback.fallback
    assert playback.diagnostic == "Finisher media failed — showing results."


def test_raw_report_writes_json_and_csv(tmp_path: Path) -> None:
    sample = write_raw_report(tmp_path / "raw.json", tmp_path / "raw.csv", 10)
    assert sample["measurement"] == "headless simulation only"
    assert (tmp_path / "raw.json").is_file() and (tmp_path / "raw.csv").is_file()

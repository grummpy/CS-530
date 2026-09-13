import pytest

from fighter.content import ContentValidationError, load_fighter, load_finisher
from fighter.platform.clock import FixedStepClock
from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.tools.replay import run_replay


def test_replay_is_deterministic():
    assert run_replay(90, 4) == run_replay(90, 4)


def test_attack_damages_close_opponent():
    game = SessionKernel()
    game.match.p2.x = game.match.p1.x + 50
    game.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    for _ in range(10):
        game.tick()
    assert game.match.p2.health < 1000


def test_missing_finisher_is_explicit():
    assert load_finisher("captain_campaign") is None


def test_special_damages_close_opponent():
    game = SessionKernel()
    game.match.p2.x = game.match.p1.x + 50
    game.match.p1.special_charge = 210
    game.tick((InputFrame.from_held(0, Action.SPECIAL), InputFrame()))
    for _ in range(28):
        game.tick()
    assert game.match.p2.health < 1000


def test_authored_content_is_immutable_and_unknown_fighters_are_rejected() -> None:
    chef = load_fighter("master_chef")
    assert chef.moves["kitchen_rush"].damage == 100
    assert chef.moves["kitchen_rush"].hitboxes[0].start == 13
    with pytest.raises(TypeError):
        chef.moves["light"] = chef.moves["light"]  # type: ignore[index]
    with pytest.raises(ContentValidationError, match="no validated definition"):
        SessionKernel(p1_id="captain_campaign")


def test_authored_special_uses_its_timing_box_and_damage() -> None:
    game = SessionKernel(p1_id="master_chef", p2_id="mr_president")
    game.match.p2.x = game.match.p1.x + 80
    game.match.p1.special_charge = 210
    game.tick((InputFrame.from_held(0, Action.SPECIAL), InputFrame()))
    for _ in range(11):
        game.tick()
    assert game.match.p2.health == 1000
    game.tick()
    assert game.match.p2.health == 900


def test_authored_box_prevents_a_light_hit_outside_its_range() -> None:
    game = SessionKernel(p1_id="rhinestone_angel", p2_id="mr_president")
    game.match.p2.x = game.match.p1.x + 180
    game.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    for _ in range(11):
        game.tick()
    assert game.match.p2.health == 1000


def test_fixed_step_clock_preserves_sixty_ticks_per_second_at_common_render_rates():
    for render_hz in (30, 60, 120):
        clock = FixedStepClock()
        base_ms, extra_ms = divmod(1000, render_hz)
        ticks = sum(
            clock.consume_wall_ms(base_ms + (1 if frame < extra_ms else 0))
            for frame in range(render_hz)
        )
        assert ticks == 60


def test_fixed_step_clock_keeps_fractional_milliseconds_between_frames():
    clock = FixedStepClock()
    assert sum(clock.consume_wall_ms(16) for _ in range(62)) == 59
    assert clock.consume_wall_ms(8) == 1

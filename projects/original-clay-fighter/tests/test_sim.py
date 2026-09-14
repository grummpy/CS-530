import pytest

from fighter.content import ContentValidationError, load_fighter, load_finisher
from fighter.platform.clock import FixedStepClock
from fighter.sim.bits import Action
from fighter.sim.enums import FighterMode, MatchPhase, ResultReason
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


def test_movement_walls_pushboxes_and_facing_are_symmetric():
    game = SessionKernel()
    game.match.p1.x, game.match.p2.x = 100, 160
    game.tick((InputFrame.from_held(0, Action.RIGHT), InputFrame.from_held(0, Action.LEFT)))
    left, right = sorted((game.match.p1, game.match.p2), key=lambda fighter: fighter.x)
    assert (
        left.x + left.definition.push_box.x + left.definition.push_box.w
        <= right.x + right.definition.push_box.x
    )
    assert (game.match.p1.facing, game.match.p2.facing) == (1, -1)
    game.match.p1.x = 80 - game.match.p1.definition.push_box.x
    game.tick((InputFrame.from_held(0, Action.LEFT), InputFrame()))
    assert game.match.p1.x + game.match.p1.definition.push_box.x >= 80


def test_jump_landing_and_locked_states_are_tick_authoritative():
    game = SessionKernel()
    game.tick((InputFrame.from_held(0, Action.UP), InputFrame()))
    assert game.match.p1.mode is FighterMode.JUMP_STARTUP
    for _ in range(3):
        game.tick()
    assert game.match.p1.mode is FighterMode.ASCENT
    game.tick()
    assert game.match.p1.y < 600
    for _ in range(60):
        game.tick()
        if game.match.p1.mode is FighterMode.LANDING:
            break
    assert game.match.p1.mode is FighterMode.LANDING
    assert game.match.p1.y == 600


@pytest.mark.parametrize(
    ("held", "move", "expected_block"),
    [
        (Action.RIGHT, "light", True),
        (Action.DOWN | Action.RIGHT, "light", True),
        (Action.RIGHT, "2L", False),
        (Action.DOWN | Action.RIGHT, "2L", True),
        (Action.LEFT, "light", False),
    ],
)
def test_directional_guard_matrix(held, move, expected_block):
    game = SessionKernel()
    game.match.p2.x = game.match.p1.x + 45
    candidate = game.match.p1.definition.moves[move]
    game.match.p1.mode = FighterMode.ATTACK
    game.match.p1.attack_move, game.match.p1.attack_ticks = move, candidate.total
    for _ in range(10):
        game.tick((InputFrame(), InputFrame(held=held)))
    full_damage = candidate.damage
    assert (game.match.p2.health > 1000 - full_damage) is expected_block


def test_throw_success_whiff_tech_and_immunity():
    game = SessionKernel()
    game.match.p2.x = game.match.p1.x + 50
    game.tick((InputFrame.from_held(0, Action.THROW), InputFrame()))
    for _ in range(4):
        game.tick()
    assert game.match.p2.health == 880
    assert game.match.p2.mode is FighterMode.KNOCKDOWN_SOFT
    game.reset()
    game.match.p2.x = game.match.p1.x + 200
    game.tick((InputFrame.from_held(0, Action.THROW), InputFrame()))
    for _ in range(4):
        game.tick()
    assert game.match.p2.health == 1000
    game.reset()
    game.match.p2.x = game.match.p1.x + 50
    game.tick((InputFrame.from_held(0, Action.THROW), InputFrame.from_held(0, Action.THROW)))
    for _ in range(4):
        game.tick()
    assert "throw_tech" in game.match.events


def test_cancel_requires_confirm_and_advances_once():
    game = SessionKernel()
    game.match.p2.x = game.match.p1.x + 50
    game.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    for _ in range(4):
        game.tick()
    assert game.match.p1.attack_confirm == "hit"
    game.tick((InputFrame.from_held(0, Action.MEDIUM), InputFrame()))
    for _ in range(6):
        if game.match.p1.attack_move == "medium":
            break
        game.tick()
    assert game.match.p1.attack_move == "medium"
    assert game.match.p1.cancel_depth == 1


def test_results_are_immutable_for_ko_double_ko_timeout_and_training():
    game = SessionKernel()
    game.match.p1.health, game.match.p2.health = 0, 0
    game.tick()
    assert game.match.result is not None
    assert game.match.result.reason is ResultReason.DOUBLE_KO
    assert game.match.phase is MatchPhase.KO_HOLD
    frozen = game.match.result
    game.tick()
    assert game.match.result == frozen
    timeout = SessionKernel()
    timeout.match.round_ticks = 1
    timeout.match.p1.health = 900
    timeout.tick()
    assert (
        timeout.match.result is not None and timeout.match.result.reason is ResultReason.TIMEOUT_WIN
    )
    training = SessionKernel(training=1)
    training.match.round_ticks = 1
    training.tick()
    assert training.match.result is None and training.match.phase is MatchPhase.FIGHT


def test_identical_input_replay_has_same_digest_at_30_60_and_144_hz():
    stream = [
        (Action.RIGHT if tick < 30 else Action.LEFT if tick < 60 else 0, 0) for tick in range(120)
    ]
    snapshots = []
    for render_hz in (30, 60, 144):
        clock, game, index = FixedStepClock(), SessionKernel(), 0
        base_ms, extra_ms = divmod(2000, render_hz * 2)
        for frame in range(render_hz * 2):
            elapsed = base_ms + (1 if frame < extra_ms else 0)
            for _ in range(clock.consume_wall_ms(elapsed)):
                p1, p2 = stream[index]
                game.tick((InputFrame(held=p1), InputFrame(held=p2)))
                index += 1
        snapshots.append((game.tick_index, game.checksum(), game.match.result))
    assert snapshots == [snapshots[0]] * 3

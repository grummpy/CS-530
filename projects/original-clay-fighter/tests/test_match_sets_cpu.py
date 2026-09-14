from fighter.sim.bits import Action
from fighter.sim.cpu import CpuController
from fighter.sim.enums import MatchPhase
from fighter.sim.kernel import SessionKernel


def _p1_ko(game: SessionKernel) -> None:
    game.match.p2.health = 0
    game.tick()


def test_best_of_three_requires_two_round_wins_and_only_then_finishes() -> None:
    game = SessionKernel(p1_id="master_chef", p2_id="mr_president")
    _p1_ko(game)
    assert game.match.p1_round_wins == 1
    assert game.match.result and game.match.result.finisher_variant is None
    for _ in range(30):
        game.tick()
    assert game.match.phase is MatchPhase.RESULTS
    game.reset()
    assert game.match.round_number == 2 and game.match.p1_round_wins == 1
    _p1_ko(game)
    assert game.match.p1_round_wins == 2
    assert game.match.result and game.match.result.finisher_variant == "master_chef_vs_mr_president"


def test_cpu_levels_are_deterministic_and_have_distinct_cadence() -> None:
    outputs = {}
    for level in ("Easy", "Medium", "Hard"):
        game = SessionKernel(seed=7)
        game.match.p2.x = game.match.p1.x + 100
        controller = CpuController(level)
        frames = []
        for _ in range(60):
            frames.append(controller.frame(game.match))
            game.match.tick += 1
        outputs[level] = [(frame.held, frame.pressed) for frame in frames]
        assert any(frame.held & (Action.LIGHT | Action.MEDIUM | Action.HEAVY) for frame in frames)
    assert len({tuple(value) for value in outputs.values()}) == 3

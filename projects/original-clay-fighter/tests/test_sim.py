from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.tools.replay import run_replay
from fighter.content import load_finisher

def test_replay_is_deterministic(): assert run_replay(90, 4) == run_replay(90, 4)
def test_attack_damages_close_opponent():
    game=SessionKernel(); game.match.p2.x=game.match.p1.x+50
    game.tick((InputFrame.from_held(0, Action.LIGHT), InputFrame()))
    for _ in range(10): game.tick()
    assert game.match.p2.health < 1000

def test_missing_finisher_is_explicit(): assert load_finisher("captain_campaign") is None

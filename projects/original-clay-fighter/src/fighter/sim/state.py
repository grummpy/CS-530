"""Integer-only authoritative match state."""
from dataclasses import dataclass, field
from fighter.sim.constants import MAX_HEALTH, P1_SPAWN_X, P2_SPAWN_X

@dataclass(slots=True)
class FighterState:
    fighter_id: str
    x: int
    health: int = MAX_HEALTH
    facing: int = 1
    attack_ticks: int = 0
    stun_ticks: int = 0
    attack_kind: int = 0
    hit_this_attack: bool = False

    def snapshot(self) -> dict[str, int | str | bool]:
        return {"id": self.fighter_id, "x": self.x, "health": self.health, "facing": self.facing,
                "attack_ticks": self.attack_ticks, "stun_ticks": self.stun_ticks, "attack_kind": self.attack_kind,
                "hit": self.hit_this_attack}

@dataclass(slots=True)
class MatchState:
    seed: int
    p1: FighterState
    p2: FighterState
    tick: int = 0
    phase: int = 1
    training: int = 0
    events: list[str] = field(default_factory=list)
    def snapshot(self) -> dict[str, object]:
        return {"seed": self.seed, "tick": self.tick, "phase": self.phase, "training": self.training,
                "p1": self.p1.snapshot(), "p2": self.p2.snapshot()}

def initial_match(seed: int, p1_id: str, p2_id: str, training: int) -> MatchState:
    return MatchState(seed, FighterState(p1_id, P1_SPAWN_X), FighterState(p2_id, P2_SPAWN_X, facing=-1), training=training)

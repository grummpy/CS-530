"""Integer-only authoritative match state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from fighter.sim.constants import GROUND_Y, MAX_HEALTH, P1_SPAWN_X, P2_SPAWN_X
from fighter.sim.enums import FighterMode, MatchPhase, ResultReason
from fighter.sim.events import PresentationEvent

if TYPE_CHECKING:
    from fighter.content.loader import FighterDefinition


@dataclass(frozen=True, slots=True)
class ResultPayload:
    reason: ResultReason
    winner: int  # 0 draw, 1 P1, 2 P2
    tick: int
    p1_health: int
    p2_health: int
    finisher_variant: str | None = None

    def snapshot(self) -> dict[str, int | str | None]:
        return {
            "reason": self.reason.name,
            "winner": self.winner,
            "tick": self.tick,
            "p1_health": self.p1_health,
            "p2_health": self.p2_health,
            "finisher_variant": self.finisher_variant,
        }


@dataclass(slots=True)
class FighterState:
    fighter_id: str
    x: int
    definition: FighterDefinition
    health: int = MAX_HEALTH
    facing: int = 1
    y: int = GROUND_Y
    vy: int = 0
    mode: FighterMode = FighterMode.NEUTRAL
    state_ticks: int = 0
    attack_ticks: int = 0
    stun_ticks: int = 0
    attack_kind: int = 0
    attack_move: str = ""
    hit_this_attack: bool = False
    attack_confirm: str = ""
    cancel_depth: int = 0
    combo_count: int = 0
    armor_charge: int = 0
    armor_ticks: int = 0
    special_charge: int = 0
    blocking: bool = False
    throw_tech_until: int = 0

    @property
    def airborne(self) -> bool:
        return self.y < GROUND_Y

    def snapshot(self) -> dict[str, int | str | bool]:
        return {
            "id": self.fighter_id,
            "x": self.x,
            "y": self.y,
            "vy": self.vy,
            "health": self.health,
            "facing": self.facing,
            "mode": self.mode.name,
            "state_ticks": self.state_ticks,
            "attack_ticks": self.attack_ticks,
            "stun_ticks": self.stun_ticks,
            "attack_kind": self.attack_kind,
            "attack_move": self.attack_move,
            "hit": self.hit_this_attack,
            "attack_confirm": self.attack_confirm,
            "cancel_depth": self.cancel_depth,
            "combo_count": self.combo_count,
            "armor_charge": self.armor_charge,
            "armor_ticks": self.armor_ticks,
            "special_charge": self.special_charge,
            "blocking": self.blocking,
            "throw_tech_until": self.throw_tech_until,
        }


@dataclass(slots=True)
class MatchState:
    seed: int
    p1: FighterState
    p2: FighterState
    tick: int = 0
    phase: MatchPhase = MatchPhase.FIGHT
    training: int = 0
    events: list[str] = field(default_factory=list)
    presentation_events: list[PresentationEvent] = field(default_factory=list)
    next_presentation_event_id: int = 1
    round_ticks: int = 99 * 60
    result: ResultPayload | None = None
    phase_ticks: int = 0
    round_number: int = 1
    p1_round_wins: int = 0
    p2_round_wins: int = 0
    first_to: int = 2

    def snapshot(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "tick": self.tick,
            "phase": self.phase.name,
            "training": self.training,
            "p1": self.p1.snapshot(),
            "p2": self.p2.snapshot(),
            "round_ticks": self.round_ticks,
            "phase_ticks": self.phase_ticks,
            "result": self.result.snapshot() if self.result else None,
            "round_number": self.round_number,
            "p1_round_wins": self.p1_round_wins,
            "p2_round_wins": self.p2_round_wins,
            "first_to": self.first_to,
        }


def initial_match(
    seed: int,
    p1_id: str,
    p2_id: str,
    training: int,
    p1_definition: FighterDefinition,
    p2_definition: FighterDefinition,
) -> MatchState:
    return MatchState(
        seed,
        FighterState(p1_id, P1_SPAWN_X, p1_definition),
        FighterState(p2_id, P2_SPAWN_X, p2_definition, facing=-1),
        training=training,
    )

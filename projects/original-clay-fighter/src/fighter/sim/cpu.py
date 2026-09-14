"""Deterministic, legal CPU controller with three readable difficulty levels."""

from __future__ import annotations

from dataclasses import dataclass

from fighter.sim.bits import Action
from fighter.sim.enums import FighterMode, MatchPhase
from fighter.sim.input_frame import InputFrame
from fighter.sim.state import MatchState


@dataclass(slots=True)
class CpuController:
    difficulty: str = "Medium"
    previous: int = 0

    def frame(self, match: MatchState) -> InputFrame:
        if match.phase is not MatchPhase.FIGHT:
            current = 0
        else:
            current = self._choose(match)
        result = InputFrame.from_held(self.previous, current)
        self.previous = current
        return result

    def _choose(self, match: MatchState) -> int:
        cpu, opponent = match.p2, match.p1
        distance = abs(cpu.x - opponent.x)
        toward = Action.LEFT if opponent.x < cpu.x else Action.RIGHT
        away = Action.RIGHT if toward is Action.LEFT else Action.LEFT
        level = self.difficulty.lower()
        cadence = {"easy": 54, "medium": 30, "hard": 18}.get(level, 30)
        phase = (match.tick + match.seed * 17) % cadence

        # Better levels defend visible attacks and control spacing more reliably.
        if opponent.mode in {FighterMode.ATTACK, FighterMode.THROW}:
            reaction = {"easy": 12, "medium": 6, "hard": 2}.get(level, 6)
            if phase >= reaction and distance < 190:
                return int(away | (Action.DOWN if opponent.attack_kind == 1 else 0))
        if distance > ({"easy": 245, "medium": 205, "hard": 180}.get(level, 205)):
            return int(toward | (Action.UP if level == "hard" and phase == 0 else 0))
        if phase == 0:
            if cpu.special_charge >= 1000 and level != "easy":
                return int(Action.SPECIAL)
            return int(Action.HEAVY if level == "hard" else Action.MEDIUM)
        if phase == 1 and level == "hard":
            return int(Action.LIGHT)
        if phase == 2 and level in {"medium", "hard"} and distance < 85:
            return int(Action.THROW)
        return 0

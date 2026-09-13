"""Named, integer-only state labels owned by the simulation."""

from __future__ import annotations

from enum import IntEnum


class FighterMode(IntEnum):
    NEUTRAL = 0
    WALK = 1
    CROUCH = 2
    JUMP_STARTUP = 3
    ASCENT = 4
    DESCENT = 5
    LANDING = 6
    ATTACK = 7
    THROW = 8
    HITSTUN = 9
    BLOCKSTUN = 10
    KNOCKDOWN_SOFT = 11
    KNOCKDOWN_HARD = 12
    WAKEUP = 13
    KO = 14


class MatchPhase(IntEnum):
    INTRO = 0
    FIGHT = 1
    KO_HOLD = 2
    FINISHER_WINDOW = 3
    RESULTS = 4
    RESET = 5


class ResultReason(IntEnum):
    KO = 0
    DOUBLE_KO = 1
    TIMEOUT_WIN = 2
    TIMEOUT_DRAW = 3
    TRAINING = 4


def mode_name(mode: int) -> str:
    try:
        return FighterMode(mode).name
    except ValueError:
        return f"MODE_{mode}"


def phase_name(phase: int) -> str:
    try:
        return MatchPhase(phase).name
    except ValueError:
        return f"PHASE_{phase}"

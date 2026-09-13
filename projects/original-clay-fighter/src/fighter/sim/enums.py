"""Match and fighter state labels."""
from __future__ import annotations
from enum import IntEnum
class FighterMode(IntEnum):
    NEUTRAL = 0
    WALK = 1
    CROUCH = 2
    JUMP = 3
    DASH = 4
    ATTACK = 5
    BLOCK = 6
    HITSTUN = 7
    BLOCKSTUN = 8
    KNOCKDOWN = 9
    KO = 10
class MatchPhase(IntEnum):
    INTRO = 0
    FIGHT = 1
    KO = 2
    FINISHER_WINDOW = 3
    RESET = 4
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

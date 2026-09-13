"""Cycle 4's versioned, integer-only global fight rules."""

from __future__ import annotations

from dataclasses import dataclass

STAGE_WIDTH = 1280
STAGE_HEIGHT = 720
GROUND_Y = 600
LEFT_WALL = 80
RIGHT_WALL = 1200
WALK_SPEED = 5
JUMP_VY = -16
GRAVITY = 1
MAX_FALL = 18
MAX_HEALTH = 1000
MAX_METER = 3000
P1_SPAWN_X = 360
P2_SPAWN_X = 920


@dataclass(frozen=True, slots=True)
class FightRules:
    """Global policy: fighter-specific values remain in validated content."""

    version: str = "cycle4.v1"
    jump_startup_ticks: int = 3
    landing_ticks: int = 4
    soft_knockdown_ticks: int = 30
    hard_knockdown_ticks: int = 50
    wakeup_ticks: int = 12
    wakeup_invulnerable_ticks: int = 6
    throw_startup: int = 4
    throw_active: int = 2
    throw_recovery: int = 14
    throw_range: int = 90
    throw_damage: int = 120
    throw_tech_window: int = 2
    throw_knockdown_ticks: int = 30
    max_cancel_depth: int = 2
    combo_damage_percent: int = 100


RULES = FightRules()

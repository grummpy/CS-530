"""Move definitions and catalog lookup."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from fighter.sim.boxes import Box


class HitLevel(IntEnum):
    HIGH = 0
    MID = 1
    LOW = 2


@dataclass(frozen=True, slots=True)
class HitboxWindow:
    start: int
    end: int
    box: Box


@dataclass(frozen=True, slots=True)
class MoveDefinition:
    move_id: str
    startup: int
    active: int
    recovery: int
    damage: int
    hitstun: int
    blockstun: int
    hitstop: int
    knockback_x: int
    knockback_y: int
    hit_level: HitLevel
    meter_gain: int
    hitboxes: tuple[HitboxWindow, ...]
    airborne: bool = False
    is_throw: bool = False
    launch: bool = False
    meter_cost: int = 0
    is_super: bool = False
    animation: str = ""
    cancels: tuple[str, ...] = ()
    events: tuple[tuple[int, str], ...] = ()

    @property
    def total(self) -> int:
        return self.startup + self.active + self.recovery


_CATALOG: dict[str, dict[str, MoveDefinition]] | None = None
DEFAULT_FIGHTER = "graybox_rival"


def load_moves() -> dict[str, dict[str, MoveDefinition]]:
    global _CATALOG
    if _CATALOG is None:
        from fighter.content.loader import load_catalog

        _CATALOG = {fighter_id: dict(definition.moves) for fighter_id, definition in load_catalog().items()}
    return _CATALOG


def has_move(fighter_id: str, move_id: str) -> bool:
    catalog = load_moves()
    return move_id in catalog.get(fighter_id, {})


def get_move(move_id: str, fighter_id: str | None = None) -> MoveDefinition:
    catalog = load_moves()
    fid = fighter_id or DEFAULT_FIGHTER
    pack = catalog.get(fid) or catalog[DEFAULT_FIGHTER]
    return pack[move_id]


def _hb(start: int, end: int, x: int, y: int, w: int, h: int) -> HitboxWindow:
    return HitboxWindow(start=start, end=end, box=Box(x, y, w, h))


MOVES: dict[str, MoveDefinition] = {
    "5L": MoveDefinition(
        "5L", 4, 3, 8, 40, 10, 8, 4, 4, 0, HitLevel.MID, 40, (_hb(4, 7, 20, -130, 70, 30),)
    ),
    "5M": MoveDefinition(
        "5M", 7, 4, 12, 70, 14, 11, 6, 6, 0, HitLevel.MID, 60, (_hb(7, 11, 24, -140, 90, 40),)
    ),
    "5H": MoveDefinition(
        "5H",
        11,
        4,
        18,
        110,
        18,
        14,
        8,
        8,
        -2,
        HitLevel.MID,
        90,
        (_hb(11, 15, 28, -150, 110, 50),),
        launch=True,
    ),
    "2L": MoveDefinition(
        "2L", 4, 3, 8, 35, 10, 8, 4, 3, 0, HitLevel.LOW, 35, (_hb(4, 7, 16, -50, 80, 28),)
    ),
    "THROW": MoveDefinition(
        "THROW",
        4,
        2,
        14,
        120,
        20,
        0,
        6,
        14,
        0,
        HitLevel.MID,
        80,
        (_hb(4, 6, 10, -140, 70, 120),),
        is_throw=True,
    ),
}
GROUND_NORMALS = ("5L", "5M", "5H", "2L", "2M", "2H")
AIR_NORMALS = ("jL", "jH")

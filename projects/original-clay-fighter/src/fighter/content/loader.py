"""Validated immutable combat content loaded before a match starts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from fighter.sim.boxes import Box
    from fighter.sim.moves import HitLevel, MoveDefinition


def data_root() -> Path:
    return Path(__file__).resolve().parents[3] / "data"


class ContentValidationError(ValueError):
    """Raised when committed combat content cannot safely drive the simulation."""


@dataclass(frozen=True, slots=True)
class FighterProfile:
    fighter_id: str
    display_name: str
    moves_id: str
    special_id: str | None
    armor_charge_requirement: int | None = None
    armor_duration_ticks: int = 0
    armor_damage_bonus: int = 0


@dataclass(frozen=True, slots=True)
class FighterDefinition:
    profile: FighterProfile
    moves: Mapping[str, MoveDefinition]
    push_box: Box
    hurt_box: Box


_CATALOG: Mapping[str, FighterDefinition] | None = None


def _mapping(raw: object, context: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ContentValidationError(f"{context} must be a mapping")
    return raw


def _string(raw: Mapping[str, Any], key: str, context: str, *, optional: bool = False) -> str | None:
    value = raw.get(key)
    if optional and value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ContentValidationError(f"{context}.{key} must be a non-empty string")
    return value


def _integer(raw: Mapping[str, Any], key: str, context: str, *, minimum: int = 0) -> int:
    value = raw.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ContentValidationError(f"{context}.{key} must be an integer >= {minimum}")
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        return _mapping(yaml.safe_load(path.read_text(encoding="utf-8")), str(path))
    except OSError as error:
        raise ContentValidationError(f"cannot read {path}") from error
    except yaml.YAMLError as error:
        raise ContentValidationError(f"invalid YAML in {path}") from error


def _box(raw: object, context: str) -> Box:
    from fighter.sim.boxes import Box

    values = _mapping(raw, context)
    box = Box(
        _integer(values, "x", context, minimum=-10_000),
        _integer(values, "y", context, minimum=-10_000),
        _integer(values, "w", context, minimum=1),
        _integer(values, "h", context, minimum=1),
    )
    return box


def _frames(raw: object, context: str) -> tuple[int, int]:
    if not isinstance(raw, list) or len(raw) != 2:
        raise ContentValidationError(f"{context} must be a two-item list")
    start, end = raw
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (start, end)):
        raise ContentValidationError(f"{context} must contain integers")
    if start < 1 or end < start:
        raise ContentValidationError(f"{context} must be ascending positive frames")
    return start, end


def _hit_level(raw: Mapping[str, Any], context: str) -> HitLevel:
    from fighter.sim.moves import HitLevel

    names = {"high": HitLevel.HIGH, "mid": HitLevel.MID, "low": HitLevel.LOW}
    value = raw.get("hit_level", "mid")
    if value not in names:
        raise ContentValidationError(f"{context}.hit_level must be high, mid, or low")
    return names[value]


def _move(
    move_id: str, raw: Mapping[str, Any], box_raw: Mapping[str, Any], context: str
) -> MoveDefinition:
    from fighter.sim.moves import HitboxWindow, MoveDefinition

    startup = _integer(raw, "startup", context)
    if _string(raw, "input", context) not in {"light", "medium", "heavy", "special"}:
        raise ContentValidationError(f"{context}.input is not a supported action")
    active = _integer(raw, "active", context, minimum=1)
    recovery = _integer(raw, "recovery", context)
    damage = _integer(raw, "damage", context, minimum=1)
    hitstun = _integer(raw, "hitstun", context, minimum=1)
    start, end = _frames(box_raw.get("active_frames"), f"{context}.active_frames")
    if end - start + 1 != active:
        raise ContentValidationError(f"{context}.active_frames duration must equal active")
    hitbox = _box(box_raw.get("hit_box"), f"{context}.hit_box")
    total = startup + active + recovery
    if end > total:
        raise ContentValidationError(f"{context}.active_frames exceed move duration")
    return MoveDefinition(
        move_id=move_id,
        startup=startup,
        active=active,
        recovery=recovery,
        damage=damage,
        hitstun=hitstun,
        blockstun=max(1, hitstun - 3),
        hitstop=0,
        knockback_x=0,
        knockback_y=0,
        hit_level=_hit_level(raw, context),
        meter_gain=damage,
        meter_cost=_integer(raw, "charge_requirement", context) if "charge_requirement" in raw else 0,
        hitboxes=(HitboxWindow(start, end, hitbox),),
        animation=move_id,
        events=((start, "hit"),),
    )


def _profile(raw: Mapping[str, Any], fighter_id: str, context: str) -> FighterProfile:
    if raw.get("schema") != "fighter.profile.v1" or raw.get("id") != fighter_id:
        raise ContentValidationError(f"{context} must declare matching fighter.profile.v1 identity")
    moves_id = _string(raw, "moves", context)
    special_id = _string(raw, "special", context, optional=True)
    armor = raw.get("armor_mode")
    if armor is None:
        return FighterProfile(fighter_id, _string(raw, "display_name", context) or "", moves_id or "", special_id)
    values = _mapping(armor, f"{context}.armor_mode")
    return FighterProfile(
        fighter_id,
        _string(raw, "display_name", context) or "",
        moves_id or "",
        special_id,
        _integer(values, "charge_from_damage", f"{context}.armor_mode", minimum=1),
        _integer(values, "duration_ticks", f"{context}.armor_mode", minimum=1),
        _integer(values, "power_bonus", f"{context}.armor_mode"),
    )


def _fighter_definition(fighter_id: str) -> FighterDefinition:
    root = data_root()
    profile_raw = _load_yaml(root / "fighters" / f"{fighter_id}.yaml")
    profile = _profile(profile_raw, fighter_id, f"fighters/{fighter_id}.yaml")
    if profile.moves_id != fighter_id:
        raise ContentValidationError(f"fighters/{fighter_id}.yaml.moves must match fighter id")
    moves_raw = _load_yaml(root / "moves" / f"{profile.moves_id}.yaml")
    boxes_raw = _load_yaml(root / "boxes" / f"{fighter_id}.yaml")
    if moves_raw.get("schema") != "fighter.moves.v1" or moves_raw.get("fighter_id") != fighter_id:
        raise ContentValidationError(f"moves/{fighter_id}.yaml must declare matching fighter.moves.v1 identity")
    if boxes_raw.get("schema") != "fighter.boxes.v1" or boxes_raw.get("fighter_id") != fighter_id:
        raise ContentValidationError(f"boxes/{fighter_id}.yaml must declare matching fighter.boxes.v1 identity")
    push_box = _box(boxes_raw.get("push_box"), f"boxes/{fighter_id}.yaml.push_box")
    hurt_box = _box(boxes_raw.get("hurt_box"), f"boxes/{fighter_id}.yaml.hurt_box")
    move_boxes = _mapping(boxes_raw.get("moves"), f"boxes/{fighter_id}.yaml.moves")
    move_specs = _mapping(moves_raw.get("moves"), f"moves/{fighter_id}.yaml.moves")
    moves: dict[str, MoveDefinition] = {}
    for move_name in ("light", "medium", "heavy"):
        spec = _mapping(move_specs.get(move_name), f"moves/{fighter_id}.yaml.moves.{move_name}")
        box_spec = _mapping(move_boxes.get(move_name), f"boxes/{fighter_id}.yaml.moves.{move_name}")
        moves[move_name] = _move(move_name, spec, box_spec, f"{fighter_id}.{move_name}")
    special = moves_raw.get("special")
    if profile.special_id is not None:
        spec = _mapping(special, f"moves/{fighter_id}.yaml.special")
        if _string(spec, "id", f"moves/{fighter_id}.yaml.special") != profile.special_id:
            raise ContentValidationError(f"{fighter_id} profile and special move ids do not match")
        if _string(spec, "input", f"moves/{fighter_id}.yaml.special") != "special":
            raise ContentValidationError(f"{fighter_id} special must use the special action")
        if profile.armor_charge_requirement is None:
            moves[profile.special_id] = _move(
                profile.special_id,
                spec,
                _mapping(move_boxes.get(profile.special_id), f"boxes/{fighter_id}.yaml.moves.{profile.special_id}"),
                f"{fighter_id}.{profile.special_id}",
            )
    return FighterDefinition(profile, MappingProxyType(moves), push_box, hurt_box)


def load_catalog() -> Mapping[str, FighterDefinition]:
    global _CATALOG
    if _CATALOG is None:
        from fighter.sim.boxes import Box
        from fighter.sim.moves import MOVES

        authored = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
        catalog = {fighter_id: _fighter_definition(fighter_id) for fighter_id in authored}
        graybox_profile = FighterProfile("graybox_rival", "Graybox Rival", "graybox_rival", "special")
        graybox_moves = {
            **MOVES,
            "light": MOVES["5L"],
            "medium": MOVES["5M"],
            "heavy": MOVES["5H"],
            "special": replace(MOVES["5H"], meter_cost=210),
        }
        catalog["graybox_rival"] = FighterDefinition(
            graybox_profile,
            MappingProxyType(graybox_moves),
            Box(-28, -160, 56, 160),
            Box(-35, -160, 70, 160),
        )
        _CATALOG = MappingProxyType(catalog)
    return _CATALOG


def load_fighter(fighter_id: str) -> FighterDefinition:
    try:
        return load_catalog()[fighter_id]
    except KeyError as error:
        raise ContentValidationError(
            f"fighter {fighter_id!r} has no validated definition; select graybox_rival explicitly for fallback"
        ) from error


def load_finisher(fighter_id: str) -> dict[str, str] | None:
    """Return declared finisher metadata when authored media/timelines exist.

    The current prototype has no committed finisher data, so callers get an
    explicit empty result instead of failing at package import time.
    """
    path = data_root() / "finishers" / f"{fighter_id}.yaml"
    if not path.exists():
        return None
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else None

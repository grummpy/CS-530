"""Non-authoritative manifest-backed character and stage presentation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from fighter.resource_paths import asset_root, data_root, resource_path
from fighter.sim.enums import FighterMode

PRESENTATION_MAP_VERSION = 1
SELECTABLE_FIGHTERS = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
SELECTABLE_STAGES = ("roadside_truck_stop", "executive_lawn", "electric_assembly_hall")


@dataclass(frozen=True, slots=True)
class Clip:
    name: str
    frames: tuple[str, ...]
    fps: int


@dataclass(frozen=True, slots=True)
class SpriteManifest:
    fighter_id: str
    pivot: tuple[int, int]
    clips: dict[str, Clip]


@dataclass(frozen=True, slots=True)
class Stage:
    stage_id: str
    ground_y: int
    background: Path


@dataclass(frozen=True, slots=True)
class StageReadability:
    tint: tuple[int, int, int, int]
    hud_safe_zones: tuple[tuple[int, int, int, int], tuple[int, int, int, int]]


STAGE_READABILITY: dict[str, StageReadability] = {
    "roadside_truck_stop": StageReadability((22, 16, 8, 42), ((20, 18, 540, 54), (720, 18, 540, 54))),
    "executive_lawn": StageReadability((5, 25, 16, 42), ((20, 18, 540, 54), (720, 18, 540, 54))),
    "electric_assembly_hall": StageReadability((14, 10, 30, 45), ((20, 18, 540, 54), (720, 18, 540, 54))),
}


def load_manifest(fighter_id: str) -> SpriteManifest:
    """Load a committed Blender-frame manifest and reject malformed assets."""
    path = asset_root() / "characters" / fighter_id / "manifest.json"
    try:
        raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        pivot = raw["pivot"]
        clips = {
            name: Clip(name, tuple(spec["frames"]), spec["fps"])
            for name, spec in raw["clips"].items()
        }
    except (OSError, TypeError, ValueError, KeyError) as error:
        raise ValueError(f"invalid sprite manifest for {fighter_id}") from error
    if raw.get("schema") != "fighter.sprite-manifest.v1" or raw.get("fighter_id") != fighter_id:
        raise ValueError(f"sprite manifest identity does not match {fighter_id}")
    if (
        not isinstance(pivot, dict)
        or any(isinstance(pivot.get(key), bool) or not isinstance(pivot.get(key), int) for key in ("x", "y"))
        or not clips
    ):
        raise ValueError(f"invalid sprite manifest pivot or clips for {fighter_id}")
    for clip in clips.values():
        if clip.fps not in (8, 12) or not clip.frames:
            raise ValueError(f"invalid clip cadence for {fighter_id}:{clip.name}")
        for frame in clip.frames:
            if not isinstance(frame, str) or not (asset_root() / "characters" / fighter_id / "sprites" / frame).is_file():
                raise ValueError(f"missing frame for {fighter_id}:{clip.name}")
    return SpriteManifest(fighter_id, (pivot["x"], pivot["y"]), clips)


def load_stage(stage_id: str) -> Stage:
    """Load an approved stage and ensure its declared background is present."""
    if stage_id not in SELECTABLE_STAGES:
        raise ValueError(f"unapproved stage id: {stage_id}")
    path = data_root() / "stages" / f"{stage_id}.yaml"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        background = raw["runtime_background"]
        ground_y = raw["ground_y"]
    except (OSError, TypeError, KeyError, yaml.YAMLError) as error:
        raise ValueError(f"invalid stage definition for {stage_id}") from error
    background_path = resource_path(background)
    if (
        not isinstance(raw, dict)
        or raw.get("schema") != "fighter.stage.v1"
        or raw.get("id") != stage_id
        or raw.get("width") != 1280
        or ground_y != 600
        or not background_path.is_file()
    ):
        raise ValueError(f"stage validation failed for {stage_id}")
    return Stage(stage_id, ground_y, background_path)


def readability_profile(stage_id: str) -> StageReadability:
    """Return the approved tint and HUD-safe zones for a selectable stage."""
    return STAGE_READABILITY[load_stage(stage_id).stage_id]


def result_clip_route(stage_id: str, result_reason: str) -> str:
    """Map results to existing presentation labels; never loads finisher media."""
    readability_profile(stage_id)
    return "double_ko" if result_reason == "DOUBLE_KO" else "ko" if result_reason == "KO" else "timeout"


def frame_index(tick: int, fps: int, frame_count: int) -> int:
    """Return a presentation-only frame index using the 60 Hz simulation clock."""
    if tick < 0 or fps <= 0 or frame_count <= 0:
        raise ValueError("tick, fps, and frame_count must be positive")
    return (tick * fps // 60) % frame_count


def resolved_pivot(pivot: tuple[int, int], source_size: tuple[int, int]) -> tuple[tuple[int, int], str | None]:
    """Validate a source-space pivot; malformed source data uses lower-center."""
    width, height = source_size
    x, y = pivot
    if width <= 0 or height <= 0:
        raise ValueError("source frame dimensions must be positive")
    if 0 <= x < width and 0 <= y < height:
        return pivot, None
    fallback = (width // 2, height - 1)
    return fallback, (
        f"invalid source pivot {pivot} for {width}x{height}; "
        f"using documented lower-center fallback {fallback}"
    )


def placement(
    fighter_x: int, fighter_y: int, pivot: tuple[int, int], source_size: tuple[int, int], scale: float
) -> tuple[int, int]:
    """Place a scaled frame so its resolved pivot touches simulation ground."""
    pivot, _ = resolved_pivot(pivot, source_size)
    return (round(fighter_x - pivot[0] * scale), round(fighter_y - pivot[1] * scale))


_MODE_CLIPS = {
    FighterMode.NEUTRAL: ("idle", None),
    FighterMode.WALK: ("walk", None),
    FighterMode.CROUCH: ("crouch", None),
    FighterMode.JUMP_STARTUP: ("jump", "jump startup uses jump"),
    FighterMode.ASCENT: ("jump", None),
    FighterMode.DESCENT: ("jump", "descent uses jump"),
    FighterMode.LANDING: ("wake", "landing uses wake"),
    FighterMode.HITSTUN: ("hit", None),
    FighterMode.BLOCKSTUN: ("block_high", "guard level selects high or low"),
    FighterMode.KNOCKDOWN_SOFT: ("knockdown", None),
    FighterMode.KNOCKDOWN_HARD: ("knockdown", None),
    FighterMode.WAKEUP: ("wake", None),
    FighterMode.KO: ("knockdown", "KO uses knockdown"),
    FighterMode.THROW: ("heavy", "throw uses heavy"),
}


def resolve_clip(
    manifest: SpriteManifest, fighter: Any, held: int = 0, result_winner: int | None = None, player: int = 0
) -> tuple[str, str | None]:
    """Map every Cycle 4 state to an existing clip or a named approved fallback."""
    if result_winner is not None:
        desired, fallback = ("win", None) if player == result_winner else ("lose", None)
    elif fighter.fighter_id == "tech_billionaire" and fighter.armor_ticks:
        if fighter.attack_kind == 4 and fighter.attack_ticks:
            desired, fallback = "exosuit_call", None
        elif fighter.attack_ticks:
            desired, fallback = ("armor_kick" if fighter.attack_kind == 3 else "armor_punch"), None
        else:
            desired = "armor_idle"
            fallback = None
    elif fighter.mode is FighterMode.ATTACK:
        desired, fallback = fighter.attack_move, "attack move uses idle"
    else:
        desired, fallback = _MODE_CLIPS.get(fighter.mode, ("idle", "unknown mode uses idle"))
        if fighter.mode is FighterMode.BLOCKSTUN:
            desired = "block_low" if held & 8 else "block_high"
    if desired in manifest.clips:
        return desired, fallback
    if "idle" not in manifest.clips:
        raise ValueError(f"{manifest.fighter_id} cannot resolve {desired}; no idle fallback")
    return "idle", f"{desired} unavailable; uses idle"


@dataclass(slots=True)
class TransformCache:
    """Keep rendered scales/flips out of the per-frame allocation path."""

    frames: dict[tuple[str, str, int], tuple[object, ...]] = field(default_factory=dict)
    diagnostics: list[str] = field(default_factory=list)

    def load_clip(self, pygame: Any, manifest: SpriteManifest, clip_name: str, facing: int) -> tuple[object, ...]:
        key = (manifest.fighter_id, clip_name, facing)
        if key in self.frames:
            return self.frames[key]
        clip = manifest.clips[clip_name]
        root = asset_root() / "characters" / manifest.fighter_id / "sprites"
        transformed = tuple(
            pygame.transform.flip(
                pygame.transform.smoothscale(
                    pygame.image.load((root / name).as_posix()).convert_alpha(), (320, 320)
                ),
                facing < 0,
                False,
            )
            for name in clip.frames
        )
        self.frames[key] = transformed
        return transformed

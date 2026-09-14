from __future__ import annotations

from types import SimpleNamespace

import pytest

from fighter.presentation.assets import (
    SELECTABLE_FIGHTERS,
    SELECTABLE_STAGES,
    TransformCache,
    frame_index,
    load_manifest,
    load_stage,
    placement,
    resolve_clip,
    resolved_pivot,
)
from fighter.sim.bits import Action
from fighter.sim.enums import FighterMode


def test_manifest_clock_honors_8_and_12_fps_for_ten_seconds() -> None:
    assert [frame_index(tick, 8, 4) for tick in range(0, 600, 75)] == [0, 2, 0, 2, 0, 2, 0, 2]
    assert [frame_index(tick, 12, 4) for tick in range(0, 600, 50)] == [
        0,
        2,
        0,
        2,
        0,
        2,
        0,
        2,
        0,
        2,
        0,
        2,
    ]
    assert frame_index(599, 8, 4) == 3
    assert frame_index(599, 12, 4) == 3


def test_pivot_placement_contacts_ground_and_invalid_pivot_is_diagnostic() -> None:
    assert placement(640, 600, (256, 480), (512, 512), 320 / 512) == (480, 300)
    pivot, diagnostic = resolved_pivot((512, 1000), (512, 512))
    assert pivot == (256, 511)
    assert diagnostic is not None and "lower-center fallback" in diagnostic
    assert placement(640, 600, pivot, (512, 512), 320 / 512)[1] == 281


def test_every_reachable_mode_move_guard_and_result_resolves_to_existing_clip() -> None:
    for fighter_id in SELECTABLE_FIGHTERS:
        manifest = load_manifest(fighter_id)
        fighter = SimpleNamespace(
            fighter_id=fighter_id,
            mode=FighterMode.NEUTRAL,
            attack_move="",
            attack_kind=0,
            armor_ticks=0,
        )
        for mode in FighterMode:
            fighter.mode = mode
            clip, _ = resolve_clip(manifest, fighter, held=Action.DOWN)
            assert clip in manifest.clips
        fighter.mode = FighterMode.ATTACK
        for move in (
            "light",
            "medium",
            "heavy",
            *(
                name
                for name in manifest.clips
                if name in {"kitchen_rush", "hostile_takeover", "star_chord"}
            ),
        ):
            fighter.attack_move = move
            clip, _ = resolve_clip(manifest, fighter)
            assert clip in manifest.clips
        for winner in (1, 2):
            clip, _ = resolve_clip(manifest, fighter, result_winner=winner, player=winner)
            assert clip == "win"
            clip, _ = resolve_clip(manifest, fighter, result_winner=winner, player=3 - winner)
            assert clip == "lose"


def test_tech_armor_uses_existing_armor_clips_not_special_clip() -> None:
    manifest = load_manifest("tech_billionaire")
    fighter = SimpleNamespace(
        fighter_id="tech_billionaire",
        mode=FighterMode.ATTACK,
        attack_move="",
        attack_kind=3,
        attack_ticks=10,
        armor_ticks=60,
    )
    assert resolve_clip(manifest, fighter)[0] == "armor_kick"
    fighter.mode, fighter.attack_ticks = FighterMode.NEUTRAL, 0
    assert resolve_clip(manifest, fighter)[0] == "armor_idle"


def test_stage_ids_assets_and_ground_contract_are_validated() -> None:
    for stage_id in SELECTABLE_STAGES:
        stage = load_stage(stage_id)
        assert stage.ground_y == 600 and stage.background.is_file()
    with pytest.raises(ValueError, match="unapproved"):
        load_stage("test_grid")


def test_transform_cache_reuses_scaled_and_flipped_frames() -> None:
    calls = {"load": 0, "scale": 0, "flip": 0}

    class Surface:
        def convert_alpha(self) -> Surface:
            return self

    class Image:
        @staticmethod
        def load(path: str) -> Surface:
            calls["load"] += 1
            return Surface()

    class Transform:
        @staticmethod
        def smoothscale(surface: Surface, size: tuple[int, int]) -> Surface:
            calls["scale"] += 1
            return surface

        @staticmethod
        def flip(surface: Surface, horizontal: bool, vertical: bool) -> Surface:
            calls["flip"] += 1
            return surface

    manifest = load_manifest("master_chef")
    pygame = SimpleNamespace(image=Image, transform=Transform)
    cache = TransformCache()
    first = cache.load_clip(pygame, manifest, "idle", 1)
    second = cache.load_clip(pygame, manifest, "idle", 1)
    mirrored = cache.load_clip(pygame, manifest, "idle", -1)
    assert first is second and mirrored is not first
    expected = len(manifest.clips["idle"].frames) * 2
    assert calls == {"load": expected, "scale": expected, "flip": expected}

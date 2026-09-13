"""Match rendering retained separately from Cycle 6 shell controls."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from fighter.platform.input import SemanticAction
from fighter.presentation.assets import (
    TransformCache,
    frame_index,
    load_manifest,
    placement,
    resolve_clip,
    resolved_pivot,
)
from fighter.presentation.assets import load_stage as load_stage_definition


@dataclass
class MatchAssets:
    stage: Any | None
    manifests: dict[str, Any]
    cache: TransformCache = field(default_factory=TransformCache)


def load_match_assets(pygame: Any, fighter_ids: tuple[str, str], stage_id: str = "electric_assembly_hall") -> MatchAssets:
    try:
        stage = pygame.transform.smoothscale(
            pygame.image.load(load_stage_definition(stage_id).background.as_posix()).convert(), (1280, 720)
        )
    except (OSError, pygame.error):
        stage = None
    return MatchAssets(stage, {fighter_id: load_manifest(fighter_id) for fighter_id in fighter_ids})


def draw_match(
    pygame: Any, screen: Any, font: Any, game: Any, actions: tuple[set[SemanticAction], set[SemanticAction]],
    training: bool, paused: bool, pause_reason: str | None, reduced_effects: bool,
    assets: MatchAssets,
) -> None:
    """Render gameplay information without making rendering part of simulation."""
    match = game.match
    screen.fill((37, 33, 55))
    if assets.stage is not None:
        screen.blit(assets.stage, (0, 0))
    else:
        pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120))
    for index, (fighter, color) in enumerate(((match.p1, (196, 75, 67)), (match.p2, (60, 150, 182)))):
        manifest = assets.manifests[fighter.fighter_id]
        clip_name, _ = resolve_clip(manifest, fighter, 0, None, index + 1)
        frames = assets.cache.load_clip(pygame, manifest, clip_name, fighter.facing)
        if frames:
            frame = frames[frame_index(match.tick, manifest.clips[clip_name].fps, len(frames))]
            pivot, _ = resolved_pivot(manifest.pivot, (512, 512))
            screen.blit(frame, placement(fighter.x, fighter.y, pivot, (512, 512), 320 / 512))
        else:
            pygame.draw.rect(screen, color, (fighter.x - 35, fighter.y - 160, 70, 160), border_radius=18)
    for x, health, left in ((40, match.p1.health, True), (740, match.p2.health, False)):
        pygame.draw.rect(screen, (80, 20, 25), (x, 35, 500, 24))
        width = health // 2
        pygame.draw.rect(screen, (65, 180, 90), (x if left else x + 500 - width, 35, width, 24))
    seconds = (match.round_ticks + 59) // 60
    screen.blit(font.render(f"{seconds:02d}", True, (255, 240, 190)), (612, 32))
    labels = "P1: " + ", ".join(sorted(action.value for action in actions[0]))
    labels += "    P2: " + ", ".join(sorted(action.value for action in actions[1]))
    screen.blit(font.render(labels or "No inputs", True, (255, 255, 255)), (30, 650))
    help_text = "Esc pauses • Tab move list"
    if training:
        help_text += " • R reset training"
    screen.blit(font.render(help_text, True, (255, 255, 255)), (30, 682))
    if not reduced_effects:
        for fighter in (match.p1, match.p2):
            if fighter.blocking:
                pygame.draw.circle(screen, (115, 210, 255), (fighter.x, fighter.y - 138), 76, 4)
    if paused:
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        big = pygame.font.Font(None, 70)
        screen.blit(big.render("PAUSED", True, (255, 255, 255)), (530, 280))
        screen.blit(font.render(f"{pause_reason or 'Paused'} — press Escape to resume", True,
                                (255, 255, 255)), (410, 350))

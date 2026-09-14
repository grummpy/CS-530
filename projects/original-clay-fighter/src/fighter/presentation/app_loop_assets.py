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
    readability_profile,
    resolve_clip,
    resolved_pivot,
    result_clip_route,
)
from fighter.presentation.assets import load_stage as load_stage_definition
from fighter.presentation.finishers import FinisherPlayback, fallback_card
from fighter.sim.bits import Action
from fighter.sim.enums import MatchPhase


@dataclass
class MatchAssets:
    stage: Any | None
    manifests: dict[str, Any]
    cache: TransformCache = field(default_factory=TransformCache)
    finisher: FinisherPlayback | None = None
    finisher_display_index: int = -1
    finisher_display: Any | None = None


def load_match_assets(
    pygame: Any, fighter_ids: tuple[str, str], stage_id: str = "electric_assembly_hall"
) -> MatchAssets:
    try:
        stage = pygame.transform.smoothscale(
            pygame.image.load(load_stage_definition(stage_id).background.as_posix()).convert(),
            (1280, 720),
        )
    except (OSError, pygame.error):
        stage = None
    return MatchAssets(stage, {fighter_id: load_manifest(fighter_id) for fighter_id in fighter_ids})


def draw_match(
    pygame: Any,
    screen: Any,
    font: Any,
    game: Any,
    actions: tuple[set[SemanticAction], set[SemanticAction]],
    training: bool,
    paused: bool,
    pause_reason: str | None,
    reduced_effects: bool,
    assets: MatchAssets,
    stage_id: str = "electric_assembly_hall",
    effects: Any | None = None,
    cpu_difficulty: str | None = None,
) -> None:
    """Render gameplay information without making rendering part of simulation."""
    match = game.match
    screen.fill((37, 33, 55))
    if assets.stage is not None:
        screen.blit(assets.stage, (0, 0))
    else:
        pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120))
    profile = readability_profile(stage_id)
    tint = pygame.Surface((1280, 720), pygame.SRCALPHA)
    tint.fill(profile.tint)
    screen.blit(tint, (0, 0))
    for zone in profile.hud_safe_zones:
        pygame.draw.rect(screen, (8, 8, 14), zone, border_radius=8)
    for index, (fighter, color) in enumerate(
        ((match.p1, (196, 75, 67)), (match.p2, (60, 150, 182)))
    ):
        manifest = assets.manifests[fighter.fighter_id]
        held = int(Action.DOWN) if SemanticAction.DOWN in actions[index] else 0
        result_winner = match.result.winner if match.result is not None else None
        clip_name, _ = resolve_clip(manifest, fighter, held, result_winner, index + 1)
        frames = assets.cache.load_clip(pygame, manifest, clip_name, fighter.facing)
        if frames:
            animation_tick = match.tick
            if fighter.attack_ticks and fighter.attack_move in fighter.definition.moves:
                animation_tick = (
                    fighter.definition.moves[fighter.attack_move].total - fighter.attack_ticks
                )
            frame = frames[frame_index(animation_tick, manifest.clips[clip_name].fps, len(frames))]
            pivot, _ = resolved_pivot(manifest.pivot, (512, 512))
            screen.blit(frame, placement(fighter.x, fighter.y, pivot, (512, 512), 320 / 512))
        else:
            pygame.draw.rect(
                screen, color, (fighter.x - 35, fighter.y - 160, 70, 160), border_radius=18
            )
    name_font = pygame.font.SysFont("arial", 18, bold=True)
    screen.blit(
        name_font.render(match.p1.definition.profile.display_name.upper(), True, (255, 255, 255)),
        (40, 8),
    )
    p2_name = name_font.render(
        match.p2.definition.profile.display_name.upper(), True, (255, 255, 255)
    )
    screen.blit(p2_name, (1240 - p2_name.get_width(), 8))
    for x, health, left in ((40, match.p1.health, True), (740, match.p2.health, False)):
        pygame.draw.rect(screen, (80, 20, 25), (x, 35, 500, 24))
        width = health // 2
        pygame.draw.rect(screen, (65, 180, 90), (x if left else x + 500 - width, 35, width, 24))
    for x, charge, left in (
        (40, match.p1.special_charge, True),
        (740, match.p2.special_charge, False),
    ):
        pygame.draw.rect(screen, (18, 20, 38), (x, 63, 500, 10))
        width = min(500, charge * 500 // 3000)
        pygame.draw.rect(screen, (255, 188, 45), (x if left else x + 500 - width, 63, width, 10))
    seconds = (match.round_ticks + 59) // 60
    screen.blit(font.render(f"{seconds:02d}", True, (255, 240, 190)), (612, 32))
    score_font = pygame.font.SysFont("arial", 16, bold=True)
    score = f"BEST OF 3  •  ROUND {match.round_number}  •  {match.p1_round_wins}  —  {match.p2_round_wins}"
    score_surface = score_font.render(score, True, (255, 232, 132))
    screen.blit(score_surface, score_surface.get_rect(center=(640, 83)))
    if match.fight_start_ticks:
        countdown = "READY" if match.fight_start_ticks > 30 else "FIGHT!"
        countdown_surface = pygame.font.SysFont("impact", 78).render(
            countdown, True, (255, 214, 64)
        )
        screen.blit(countdown_surface, countdown_surface.get_rect(center=(640, 235)))
    control_panel = pygame.Surface((1280, 96), pygame.SRCALPHA)
    control_panel.fill((7, 5, 15, 218))
    screen.blit(control_panel, (0, 624))
    key_font = pygame.font.SysFont("arial", 15, bold=True)
    info_font = pygame.font.SysFont("arial", 14)

    def keycap(x: int, y: int, key: str, label: str, accent: tuple[int, int, int]) -> int:
        cap_width = max(34, key_font.size(key)[0] + 18)
        pygame.draw.rect(screen, accent, (x, y, cap_width, 26), border_radius=6)
        key_surface = key_font.render(key, True, (255, 255, 255))
        screen.blit(key_surface, key_surface.get_rect(center=(x + cap_width // 2, y + 13)))
        screen.blit(info_font.render(label, True, (235, 230, 240)), (x + cap_width + 6, y + 5))
        return cap_width + info_font.size(label)[0] + 18

    screen.blit(key_font.render("P1", True, (255, 95, 133)), (20, 637))
    x = 55
    for key, label in (
        ("←/→", "Move"),
        ("↑", "Jump"),
        ("↓", "Crouch"),
        ("A", "Light"),
        ("S", "Medium"),
        ("D", "Heavy"),
        ("F", "Special"),
        ("G", "Throw"),
    ):
        x += keycap(x, 632, key, label, (166, 45, 82))
    if cpu_difficulty:
        cpu_label = f"CPU OPPONENT  •  {cpu_difficulty.upper()} DIFFICULTY"
        screen.blit(key_font.render(cpu_label, True, (91, 211, 255)), (20, 677))
    else:
        screen.blit(key_font.render("P2", True, (91, 211, 255)), (20, 675))
        x = 55
        for key, label in (
            ("←/→", "Move"),
            ("↑", "Jump"),
            ("↓", "Crouch"),
            ("1", "Light"),
            ("2", "Medium"),
            ("3", "Heavy"),
            ("0", "Special"),
            ("5", "Throw"),
        ):
            x += keycap(x, 670, key, label, (32, 119, 164))
    screen.blit(
        info_font.render(
            "Esc Pause  •  Tab Moves" + ("  •  R Reset" if training else ""), True, (235, 230, 240)
        ),
        (1055, 697),
    )
    if not reduced_effects:
        for fighter in (match.p1, match.p2):
            if fighter.blocking:
                pygame.draw.circle(screen, (115, 210, 255), (fighter.x, fighter.y - 138), 76, 4)
    if effects is not None:
        for effect in effects.effects:
            x, y = effect.position
            center = (x, y - 100)
            age = max(1, effect.ttl)
            if effect.kind == "block":
                pygame.draw.circle(screen, (118, 224, 255), center, 18 + (30 - age), 4)
            elif effect.kind == "special":
                pygame.draw.circle(screen, (62, 235, 255), center, 34 + (18 - age), 5)
                pygame.draw.circle(screen, (255, 82, 190), center, 20 + (18 - age), 3)
            elif effect.kind == "dust":
                for offset in (-20, 0, 20):
                    pygame.draw.circle(screen, (211, 183, 145), (x + offset, y - 16), 10, 2)
            elif effect.kind in {"crumb", "ko"}:
                color = (188, 28, 54) if effect.kind == "ko" else (226, 122, 72)
                for offset_x, offset_y in ((-24, -8), (-12, -25), (0, -34), (18, -20), (28, 2)):
                    pygame.draw.circle(
                        screen, color, (center[0] + offset_x, center[1] + offset_y), 8
                    )
            else:
                points = [
                    (center[0], center[1] - 30),
                    (center[0] + 10, center[1] - 8),
                    (center[0] + 32, center[1]),
                    (center[0] + 10, center[1] + 9),
                    (center[0], center[1] + 30),
                    (center[0] - 10, center[1] + 9),
                    (center[0] - 32, center[1]),
                    (center[0] - 10, center[1] - 8),
                ]
                pygame.draw.polygon(screen, (255, 191, 61), points)
                pygame.draw.polygon(screen, (255, 244, 192), points, 3)
    if match.result is not None:
        label = result_clip_route(stage_id, match.result.reason.name).upper().replace("_", " ")
        screen.blit(pygame.font.Font(None, 68).render(label, True, (255, 235, 150)), (510, 115))
        if match.phase is MatchPhase.RESULTS:
            complete = max(match.p1_round_wins, match.p2_round_wins) >= match.first_to
            prompt = "ENTER / CLICK: RETURN TO SELECT" if complete else "ENTER / CLICK: NEXT ROUND"
            prompt_surface = name_font.render(prompt, True, (255, 255, 255))
            screen.blit(prompt_surface, prompt_surface.get_rect(center=(640, 170)))
    if match.phase is MatchPhase.FINISHER_WINDOW and assets.finisher is not None:
        assert match.result is not None
        frame_index_value = max(0, min(29, (match.tick - match.result.tick - 30) // 6))
        frame = assets.finisher.frame(frame_index_value)
        if frame is not None:
            if assets.finisher_display_index != frame_index_value:
                assets.finisher_display = pygame.transform.smoothscale(frame, (1280, 720))
                assets.finisher_display_index = frame_index_value
            screen.blit(assets.finisher_display, (0, 0))
        else:
            fallback_card(pygame, screen, font, label, assets.finisher.diagnostic)
    if paused:
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        big = pygame.font.Font(None, 70)
        screen.blit(big.render("PAUSED", True, (255, 255, 255)), (530, 280))
        screen.blit(
            font.render(
                f"{pause_reason or 'Paused'} — press Escape to resume", True, (255, 255, 255)
            ),
            (410, 350),
        )

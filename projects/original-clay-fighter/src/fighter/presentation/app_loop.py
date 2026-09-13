"""Simple local-versus visual shell with keyboard controls."""

import json
import random
import sys
from collections.abc import Callable
from pathlib import Path

from fighter.content.roster import display_name
from fighter.platform.clock import FixedStepClock
from fighter.presentation.assets import (
    SELECTABLE_STAGES,
    TransformCache,
    frame_index,
    load_manifest,
    placement,
    resolve_clip,
    resolved_pivot,
)
from fighter.presentation.assets import load_stage as load_stage_definition
from fighter.presentation.audio import start_match_music
from fighter.presentation.finishers import finisher_frame_paths
from fighter.sim.bits import Action
from fighter.sim.enums import MatchPhase
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel


def _load_stage(pygame: object, stage_id: str) -> object | None:
    """Load approved arena art once; preserve a playable fallback on failure."""
    try:
        path = load_stage_definition(stage_id).background
        return pygame.transform.smoothscale(
            pygame.image.load(path.as_posix()).convert(), (1280, 720)
        )
    except (OSError, pygame.error):
        return None


def _load_fighter_sprite(pygame: object, fighter_id: str) -> object | None:
    path = (
        Path(__file__).resolve().parents[3] / "assets" / "characters" / fighter_id / "portrait.png"
    )
    try:
        image = pygame.image.load(path.as_posix()).convert_alpha()
        return pygame.transform.smoothscale(image, (210, 320))
    except (OSError, pygame.error):
        return None


def _load_fighter_clips(pygame: object, fighter_id: str) -> dict[str, list[object]]:
    root = Path(__file__).resolve().parents[3] / "assets" / "characters" / fighter_id
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        return {
            name: [
                pygame.transform.smoothscale(
                    pygame.image.load((root / "sprites" / frame).as_posix()).convert_alpha(),
                    (320, 320),
                )
                for frame in clip["frames"]
            ]
            for name, clip in manifest["clips"].items()
        }
    except (OSError, ValueError, KeyError, pygame.error):
        return {}


def run_windowed_g3(title: str, seed: int, on_tick: Callable[[int], None] | None = None) -> int:
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    fighters = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
    slogans = {
        "rhinestone_angel": "Make every note hurt.",
        "mr_president": "Deal with it.",
        "tech_billionaire": "Disrupt the competition.",
        "master_chef": "Dinner is served.",
    }
    stages = SELECTABLE_STAGES
    portraits = {fid: _load_fighter_sprite(pygame, fid) for fid in fighters}
    title_clips = {fid: _load_fighter_clips(pygame, fid) for fid in fighters}
    ui_state, p1_id, p2_id, stage_id, cpu = "title", fighters[0], fighters[1], stages[0], True
    while ui_state != "match":
        mouse = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                return 0
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                ui_state = "select" if ui_state == "title" else "match"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and ui_state == "select":
                cpu = not cpu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
        screen.fill((27, 24, 38))
        big = pygame.font.Font(None, 74)
        if ui_state == "title":
            screen.blit(big.render("PAPIER PARADE", True, (255, 208, 77)), (420, 52))
            screen.blit(
                font.render("Clay comedy. Dark splats. Four fighters.", True, (235, 235, 235)),
                (447, 122),
            )
            for index, fid in enumerate(fighters):
                x = 110 + index * 285
                hovered = pygame.Rect(x, 220, 220, 300).collidepoint(mouse)
                pygame.draw.rect(
                    screen,
                    (92, 52, 110) if hovered else (48, 44, 62),
                    (x, 220 - (12 if hovered else 0), 220, 300),
                    border_radius=16,
                )
                pose = title_clips[fid].get("heavy", []) if hovered else []
                if pose:
                    screen.blit(
                        pygame.transform.smoothscale(
                            pose[(pygame.time.get_ticks() // 125) % len(pose)], (150, 220)
                        ),
                        (x + 35, 245 - (12 if hovered else 0)),
                    )
                elif portraits[fid]:
                    screen.blit(
                        pygame.transform.smoothscale(portraits[fid], (150, 220)),
                        (x + 35, 245 - (12 if hovered else 0)),
                    )
                screen.blit(font.render(display_name(fid), True, (255, 255, 255)), (x + 14, 480))
                screen.blit(font.render(slogans[fid], True, (255, 210, 135)), (x + 14, 510))
            button = pygame.Rect(500, 610, 280, 58)
            pygame.draw.rect(screen, (185, 54, 72), button, border_radius=12)
            screen.blit(font.render("START GAME", True, (255, 255, 255)), (565, 627))
            if click and button.collidepoint(mouse):
                ui_state = "select"
        else:
            screen.blit(big.render("SELECT FIGHTERS + ARENA", True, (255, 208, 77)), (290, 35))
            for index, fid in enumerate(fighters):
                x = 90 + index * 295
                card = pygame.Rect(x, 150, 250, 310)
                pygame.draw.rect(
                    screen,
                    (72, 80, 112) if fid in (p1_id, p2_id) else (48, 44, 62),
                    card,
                    border_radius=12,
                )
                if portraits[fid]:
                    screen.blit(
                        pygame.transform.smoothscale(portraits[fid], (130, 190)), (x + 60, 165)
                    )
                screen.blit(font.render(display_name(fid), True, (255, 255, 255)), (x + 22, 360))
                screen.blit(font.render(slogans[fid], True, (255, 210, 135)), (x + 22, 392))
                if click and card.collidepoint(mouse):
                    if mouse[1] < 305:
                        p1_id = fid
                    else:
                        p2_id = fid
            screen.blit(
                font.render(
                    "Click upper card half: P1. Lower card half: P2. Toggle CPU: C",
                    True,
                    (235, 235, 235),
                ),
                (315, 490),
            )
            screen.blit(
                font.render(
                    f"P1: {display_name(p1_id)}     P2: {'CPU' if cpu else display_name(p2_id)}",
                    True,
                    (255, 255, 255),
                ),
                (390, 525),
            )
            for index, stage in enumerate(stages):
                rect = pygame.Rect(180 + index * 300, 560, 250, 42)
                pygame.draw.rect(
                    screen,
                    (70, 135, 120) if stage == stage_id else (48, 44, 62),
                    rect,
                    border_radius=8,
                )
                screen.blit(
                    font.render(stage.replace("_", " ").title(), True, (255, 255, 255)),
                    (rect.x + 12, 570),
                )
                if click and rect.collidepoint(mouse):
                    stage_id = stage
            go = pygame.Rect(500, 625, 280, 52)
            pygame.draw.rect(screen, (185, 54, 72), go, border_radius=12)
            screen.blit(font.render("FIGHT!", True, (255, 255, 255)), (600, 640))
            if click and go.collidepoint(mouse):
                ui_state = "match"
        pygame.display.flip()
        clock.tick(60)
    if cpu:
        cpu_choices = tuple(fid for fid in fighters if fid != p1_id)
        p2_id = random.Random(seed).choice(cpu_choices)
    stage = _load_stage(pygame, stage_id)
    start_match_music(pygame, seed)
    game = SessionKernel(seed=seed, p1_id=p1_id, p2_id=p2_id)
    previous = [0, 0]
    held_values = [0, 0]
    running = True
    cpu_rng = random.Random(seed ^ 0xC1A7)
    finisher_frames: list[object] = []
    finisher_frame_index = 0
    fighter_sprites = {
        fighter_id: _load_fighter_sprite(pygame, fighter_id)
        for fighter_id in (game.match.p1.fighter_id, game.match.p2.fighter_id)
    }
    manifests = {
        fighter_id: load_manifest(fighter_id)
        for fighter_id in (game.match.p1.fighter_id, game.match.p2.fighter_id)
    }
    transform_cache = TransformCache()
    bindings = (
        (
            pygame.K_a,
            pygame.K_d,
            pygame.K_w,
            pygame.K_s,
            pygame.K_f,
            pygame.K_g,
            pygame.K_h,
            pygame.K_j,
        ),
        (
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_KP1,
            pygame.K_KP2,
            pygame.K_KP3,
            pygame.K_KP0,
        ),
    )
    simulation_clock = FixedStepClock()
    while running:
        elapsed_ms = clock.tick(240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()
                simulation_clock.reset()
                finisher_frames = []
                finisher_frame_index = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finisher_frames:
                finisher_frame_index = len(finisher_frames) - 1
        keys = pygame.key.get_pressed()
        for index, group in enumerate(bindings):
            held = (
                (Action.LEFT if keys[group[0]] else 0)
                | (Action.RIGHT if keys[group[1]] else 0)
                | (Action.UP if keys[group[2]] else 0)
                | (Action.DOWN if keys[group[3]] else 0)
                | (Action.LIGHT if keys[group[4]] else 0)
                | (Action.MEDIUM if keys[group[5]] else 0)
                | (Action.HEAVY if keys[group[6]] else 0)
                | (Action.SPECIAL if keys[group[7]] else 0)
            )
            held_values[index] = held
        for _ in range(simulation_clock.consume_wall_ms(elapsed_ms)):
            for index in range(2):
                held = held_values[index]
                if index == 1 and cpu:
                    opponent, bot = game.match.p1, game.match.p2
                    held = (
                        Action.LEFT
                        if bot.x > opponent.x + 80
                        else Action.RIGHT
                        if bot.x < opponent.x - 80
                        else 0
                    )
                    if (
                        abs(bot.x - opponent.x) < 105
                        and not bot.attack_ticks
                        and not bot.stun_ticks
                        and cpu_rng.randrange(24) == 0
                    ):
                        held |= cpu_rng.choice(
                            (
                                Action.LIGHT,
                                Action.MEDIUM,
                                Action.HEAVY,
                                Action.SPECIAL if bot.special_charge >= 210 else Action.HEAVY,
                            )
                        )
                    if abs(bot.x - opponent.x) < 125 and cpu_rng.randrange(90) == 0:
                        held |= Action.DOWN
                held_values[index] = held
                frame = InputFrame.from_held(previous[index], held)
                previous[index] = held
                if index == 0:
                    p1_frame = frame
                else:
                    p2_frame = frame
            game.tick((p1_frame, p2_frame))
            if on_tick:
                on_tick(game.tick_index)
            if game.match.phase is MatchPhase.RESULTS:
                break
        m = game.match
        screen.fill((37, 33, 55))
        if stage is not None:
            screen.blit(stage, (0, 0))
        else:
            pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120))
        if m.phase is MatchPhase.RESULTS:
            if not finisher_frames and m.result is not None and m.result.winner:
                winner, loser = (m.p1, m.p2) if m.result.winner == 1 else (m.p2, m.p1)
                finisher_frames = [
                    pygame.transform.smoothscale(
                        pygame.image.load(path.as_posix()).convert(), (1280, 720)
                    )
                    for path in finisher_frame_paths(winner.fighter_id, loser.fighter_id)
                ]
            if finisher_frames:
                screen.blit(
                    finisher_frames[min(finisher_frame_index, len(finisher_frames) - 1)], (0, 0)
                )
                finisher_frame_index = min(finisher_frame_index + 1, len(finisher_frames) - 1)
                screen.blit(
                    font.render("FINISHER — Space skips — R resets", True, (255, 240, 190)),
                    (465, 680),
                )
                pygame.display.flip()
                clock.tick(10)
                continue
            result_text = "DRAW" if m.result is None or m.result.winner == 0 else (
                "P1 WINS" if m.result.winner == 1 else "P2 WINS"
            )
            screen.blit(font.render(f"{result_text} — R rematch", True, (255, 240, 190)), (450, 350))
            pygame.display.flip()
            clock.tick(60)
            continue
        for f, color in ((m.p1, (196, 75, 67)), (m.p2, (60, 150, 182))):
            fighter_index = 0 if f is m.p1 else 1
            manifest = manifests[f.fighter_id]
            winner = m.result.winner if m.phase is MatchPhase.RESULTS and m.result else None
            clip_name, _ = resolve_clip(
                manifest, f, held_values[fighter_index], winner, fighter_index + 1
            )
            frames = transform_cache.load_clip(pygame, manifest, clip_name, f.facing)
            if frames:
                frame = frames[frame_index(m.tick, manifest.clips[clip_name].fps, len(frames))]
                source_size = (512, 512)
                pivot, diagnostic = resolved_pivot(manifest.pivot, source_size)
                if diagnostic and diagnostic not in transform_cache.diagnostics:
                    transform_cache.diagnostics.append(diagnostic)
                    print(f"{f.fighter_id}: {diagnostic}", file=sys.stderr)
                screen.blit(
                    frame,
                    placement(f.x, f.y, pivot, source_size, 320 / source_size[0]),
                )
            else:
                pygame.draw.rect(screen, color, (f.x - 35, 440, 70, 160), border_radius=18)
        portrait = fighter_sprites.get(m.p1.fighter_id)
        if portrait is not None:
            screen.blit(portrait, (18, 70))
        portrait = fighter_sprites.get(m.p2.fighter_id)
        if portrait is not None:
            screen.blit(
                pygame.transform.flip(portrait, True, False),
                (1182, 70),
            )
        pygame.draw.rect(screen, (80, 20, 25), (40, 35, 500, 24))
        pygame.draw.rect(screen, (65, 180, 90), (40, 35, m.p1.health // 2, 24))
        pygame.draw.rect(screen, (80, 20, 25), (740, 35, 500, 24))
        pygame.draw.rect(screen, (65, 180, 90), (1240 - m.p2.health // 2, 35, m.p2.health // 2, 24))
        pygame.draw.rect(screen, (38, 32, 72), (40, 64, 500, 12))
        pygame.draw.rect(screen, (238, 191, 53), (40, 64, 500 * m.p1.special_charge // 210, 12))
        pygame.draw.rect(screen, (38, 32, 72), (740, 64, 500, 12))
        pygame.draw.rect(
            screen,
            (238, 191, 53),
            (1240 - 500 * m.p2.special_charge // 210, 64, 500 * m.p2.special_charge // 210, 12),
        )
        seconds = (m.round_ticks + 59) // 60
        screen.blit(font.render(f"{seconds:02d}", True, (255, 240, 190)), (612, 32))
        screen.blit(font.render("SPECIAL", True, (255, 230, 120)), (40, 80))
        screen.blit(font.render("SPECIAL", True, (255, 230, 120)), (1160, 80))
        for f in (m.p1, m.p2):
            if f.blocking:
                pygame.draw.circle(screen, (115, 210, 255), (f.x, 462), 76, 4)
        controls = (
            "P1 A/D/S + F/G/H/J    CPU"
            if cpu
            else "P1 A/D/S + F/G/H/J    P2 arrows + keypad 1/2/3/0"
        )
        screen.blit(
            font.render(
                f"{controls}    S/down blocks    R reset    Esc quit", True, (245, 245, 245)
            ),
            (230, 680),
        )
        pygame.display.flip()
    if pygame.mixer.get_init() is not None:
        pygame.mixer.music.stop()
    pygame.quit()
    return 0

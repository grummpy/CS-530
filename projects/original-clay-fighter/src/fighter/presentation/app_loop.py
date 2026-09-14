"""Pygame presentation shell backed by semantic input and deterministic simulation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fighter.content.roster import display_name
from fighter.platform.clock import FixedStepClock
from fighter.platform.input import InputRouter, SemanticAction
from fighter.platform.settings import load, save
from fighter.presentation.app_loop_assets import MatchAssets, draw_match, load_match_assets
from fighter.presentation.assets import SELECTABLE_STAGES
from fighter.presentation.audio import AudioLevels, MixerAudioService
from fighter.presentation.effects import ClayEffectPool
from fighter.presentation.events import PresentationDispatcher
from fighter.presentation.finishers import FinisherPlayback
from fighter.presentation.shell import Shell
from fighter.resource_paths import resource_path
from fighter.sim.cpu import CpuController
from fighter.sim.enums import MatchPhase
from fighter.sim.events import PresentationEvent
from fighter.sim.kernel import SessionKernel


def _event_token(pygame: Any, event: Any) -> tuple[str, str, bool, int | None] | None:
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        return "key", f"key:{event.key}", event.type == pygame.KEYDOWN, None
    if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
        return (
            "button",
            f"button:{event.button}",
            event.type == pygame.JOYBUTTONDOWN,
            event.instance_id,
        )
    if event.type == pygame.JOYHATMOTION:
        direction = {(0, 1): "up", (0, -1): "down", (-1, 0): "left", (1, 0): "right"}.get(
            event.value
        )
        return (
            ("hat", f"hat:{direction}", bool(direction), event.instance_id) if direction else None
        )
    return None


def _draw_menu(
    pygame: Any,
    screen: Any,
    font: Any,
    shell: Shell,
    title: str,
    entries: list[str],
    detail: str,
    high_contrast: bool,
) -> None:
    screen.fill((18, 18, 26))
    big = pygame.font.Font(None, 62)
    screen.blit(big.render(title, True, (255, 230, 120)), (80, 70))
    screen.blit(font.render(detail, True, (240, 240, 240)), (80, 135))
    for index, entry in enumerate(entries):
        rect = pygame.Rect(120, 205 + index * 56, 740, 44)
        selected = index == shell.focus
        pygame.draw.rect(
            screen,
            (255, 255, 255)
            if high_contrast and selected
            else (96, 186, 225)
            if selected
            else (48, 48, 66),
            rect,
            width=4 if selected else 0,
            border_radius=6,
        )
        color = (10, 10, 10) if high_contrast and selected else (255, 255, 255)
        screen.blit(
            font.render(f"{'▶ ' if selected else '  '}{entry}", True, color), (138, rect.y + 11)
        )


def _load_title_background(pygame: Any) -> Any | None:
    """Load the approved title key art once and preserve a plain fallback."""
    try:
        image = pygame.image.load(
            resource_path("assets/ui/title/title_hero_v1.png").as_posix()
        ).convert()
        return pygame.transform.smoothscale(image, (1280, 720))
    except (OSError, pygame.error):
        return None


def _draw_title(
    pygame: Any,
    screen: Any,
    shell: Shell,
    entries: list[str],
    detail: str,
    high_contrast: bool,
    background: Any | None,
) -> None:
    """Render the cinematic four-fighter front door at the logical resolution."""
    if background is None:
        screen.fill((24, 12, 31))
    else:
        screen.blit(background, (0, 0))
    vignette = pygame.Surface((1280, 720), pygame.SRCALPHA)
    vignette.fill((5, 3, 12, 46))
    pygame.draw.rect(vignette, (8, 4, 18, 155), (0, 0, 1280, 190))
    pygame.draw.rect(vignette, (8, 4, 18, 185), (0, 585, 1280, 135))
    screen.blit(vignette, (0, 0))

    title_font = pygame.font.SysFont("impact", 94)
    subtitle_font = pygame.font.SysFont("arial", 21, bold=True)
    menu_font = pygame.font.SysFont("arial", 24, bold=True)
    title = title_font.render("PAPIER PARADE", True, (255, 206, 54))
    shadow = title_font.render("PAPIER PARADE", True, (45, 4, 36))
    title_x = (1280 - title.get_width()) // 2
    screen.blit(shadow, (title_x + 5, 31))
    screen.blit(title, (title_x, 24))
    tagline = subtitle_font.render("FOUR EGOS ENTER  •  THE CLAY REMEMBERS", True, (255, 245, 224))
    screen.blit(tagline, ((1280 - tagline.get_width()) // 2, 124))

    button_width, gap = 245, 18
    start_x = (1280 - (button_width * len(entries) + gap * (len(entries) - 1))) // 2
    for index, entry in enumerate(entries):
        rect = pygame.Rect(start_x + index * (button_width + gap), 618, button_width, 58)
        selected = index == shell.focus
        fill = (225, 61, 91) if selected else (28, 23, 42)
        border = (255, 224, 104) if selected else (194, 178, 210)
        pygame.draw.rect(screen, (8, 5, 16), rect.move(0, 5), border_radius=12)
        pygame.draw.rect(screen, fill, rect, border_radius=12)
        pygame.draw.rect(screen, border, rect, 3 if selected else 1, border_radius=12)
        label = menu_font.render(entry.upper(), True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=rect.center))
    hint = pygame.font.SysFont("arial", 16).render(detail, True, (225, 216, 232))
    screen.blit(hint, ((1280 - hint.get_width()) // 2, 691))


def _load_selection_art(
    pygame: Any, title_background: Any | None
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Cache fighter key-art crops and arena previews for the selection screen."""
    fighter_crops: dict[str, Any] = {}
    if title_background is not None:
        crop_rects = {
            "rhinestone_angel": (0, 145, 350, 440),
            "mr_president": (325, 150, 300, 435),
            "tech_billionaire": (675, 145, 315, 440),
            "master_chef": (970, 140, 310, 445),
        }
        for fighter_id, rect in crop_rects.items():
            fighter_crops[fighter_id] = title_background.subsurface(rect).copy()
    stage_previews: dict[str, Any] = {}
    stage_files = {
        "roadside_truck_stop": "roadside_truck_stop_concept.png",
        "executive_lawn": "executive_lawn_concept.png",
        "electric_assembly_hall": "electric_assembly_hall_concept.png",
    }
    for stage_id, filename in stage_files.items():
        try:
            image = pygame.image.load(
                resource_path(f"assets/stages/{filename}").as_posix()
            ).convert()
            stage_previews[stage_id] = pygame.transform.smoothscale(image, (376, 212))
        except (OSError, pygame.error):
            continue
    return fighter_crops, stage_previews


def _draw_select(
    pygame: Any,
    screen: Any,
    shell: Shell,
    fighters: tuple[str, ...],
    p1_id: str,
    p2_id: str,
    stage_id: str,
    detail: str,
    high_contrast: bool,
    background: Any | None,
    fighter_crops: dict[str, Any],
    stage_previews: dict[str, Any],
    cpu_difficulty: str,
) -> None:
    """Render fighter and arena choices as a cinematic versus card."""
    if background is None:
        screen.fill((22, 12, 30))
    else:
        screen.blit(background, (0, 0))
    shade = pygame.Surface((1280, 720), pygame.SRCALPHA)
    shade.fill((8, 5, 17, 190))
    screen.blit(shade, (0, 0))

    heading_font = pygame.font.SysFont("impact", 54)
    name_font = pygame.font.SysFont("arial", 25, bold=True)
    small_font = pygame.font.SysFont("arial", 16, bold=True)
    heading = heading_font.render("CHOOSE YOUR CLAY", True, (255, 207, 60))
    screen.blit(heading, heading.get_rect(center=(640, 48)))

    card_specs = (
        (pygame.Rect(42, 100, 350, 420), p1_id, "PLAYER 1", (235, 63, 103), 0),
        (
            pygame.Rect(888, 100, 350, 420),
            p2_id,
            f"CPU • {cpu_difficulty.upper()}",
            (52, 178, 224),
            1,
        ),
    )
    for rect, fighter_id, player_label, accent, focus_index in card_specs:
        selected = shell.focus == focus_index
        pygame.draw.rect(screen, (8, 5, 15), rect.move(7, 8), border_radius=18)
        pygame.draw.rect(screen, (25, 20, 37), rect, border_radius=18)
        art = fighter_crops.get(fighter_id)
        if art is not None:
            screen.blit(
                pygame.transform.smoothscale(art, (rect.width - 12, 326)), (rect.x + 6, rect.y + 6)
            )
        pygame.draw.rect(
            screen, (15, 11, 24, 235), (rect.x + 6, rect.bottom - 88, rect.width - 12, 82)
        )
        pygame.draw.rect(
            screen,
            (255, 231, 112) if selected else accent,
            rect,
            5 if selected else 3,
            border_radius=18,
        )
        screen.blit(small_font.render(player_label, True, accent), (rect.x + 18, rect.bottom - 78))
        name = name_font.render(display_name(fighter_id).upper(), True, (255, 255, 255))
        screen.blit(name, (rect.x + 18, rect.bottom - 52))
        cycle = small_font.render("PRESS ENTER TO CHANGE", True, (220, 210, 228))
        screen.blit(cycle, (rect.right - cycle.get_width() - 16, rect.bottom - 76))

    vs = heading_font.render("VS", True, (255, 82, 99))
    screen.blit(vs, vs.get_rect(center=(640, 245)))
    stage_rect = pygame.Rect(450, 304, 380, 218)
    preview = stage_previews.get(stage_id)
    if preview is not None:
        screen.blit(preview, (stage_rect.x + 2, stage_rect.y + 2))
    else:
        pygame.draw.rect(screen, (34, 29, 45), stage_rect)
    pygame.draw.rect(
        screen,
        (255, 231, 112) if shell.focus == 2 else (153, 130, 180),
        stage_rect,
        5 if shell.focus == 2 else 2,
        border_radius=12,
    )
    stage_label = name_font.render(stage_id.replace("_", " ").upper(), True, (255, 255, 255))
    label_bg = pygame.Surface((stage_rect.width - 4, 42), pygame.SRCALPHA)
    label_bg.fill((8, 5, 15, 220))
    screen.blit(label_bg, (stage_rect.x + 2, stage_rect.bottom - 44))
    screen.blit(stage_label, stage_label.get_rect(center=(640, stage_rect.bottom - 23)))

    roster_y = 545
    for index, fighter_id in enumerate(fighters):
        rect = pygame.Rect(92 + index * 196, roster_y, 180, 48)
        active = fighter_id in (p1_id, p2_id)
        pygame.draw.rect(screen, (87, 46, 104) if active else (28, 23, 42), rect, border_radius=9)
        pygame.draw.rect(
            screen, (255, 210, 94) if active else (111, 99, 127), rect, 2, border_radius=9
        )
        label = small_font.render(display_name(fighter_id), True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=rect.center))

    difficulty_rect = pygame.Rect(802, roster_y, 190, 58)
    pygame.draw.rect(screen, (35, 28, 50), difficulty_rect, border_radius=12)
    pygame.draw.rect(
        screen,
        (255, 231, 112) if shell.focus == 3 else (91, 190, 220),
        difficulty_rect,
        4 if shell.focus == 3 else 2,
        border_radius=12,
    )
    difficulty_label = small_font.render(f"CPU: {cpu_difficulty.upper()}", True, (255, 255, 255))
    screen.blit(difficulty_label, difficulty_label.get_rect(center=difficulty_rect.center))

    fight_rect = pygame.Rect(1008, roster_y, 190, 58)
    fight_selected = shell.focus == 4
    pygame.draw.rect(screen, (8, 5, 15), fight_rect.move(0, 5), border_radius=12)
    pygame.draw.rect(
        screen, (225, 61, 91) if fight_selected else (42, 33, 55), fight_rect, border_radius=12
    )
    pygame.draw.rect(
        screen,
        (255, 231, 112) if fight_selected else (190, 176, 205),
        fight_rect,
        4 if fight_selected else 2,
        border_radius=12,
    )
    fight_label = name_font.render("BEGIN MATCH", True, (255, 255, 255))
    screen.blit(fight_label, fight_label.get_rect(center=fight_rect.center))
    hint_color = (255, 255, 255) if high_contrast else (224, 215, 231)
    hint = pygame.font.SysFont("arial", 16).render(detail, True, hint_color)
    screen.blit(hint, hint.get_rect(center=(640, 682)))


def _mouse_focus(pygame: Any, screen_name: str, position: tuple[int, int]) -> int | None:
    """Map visible menu controls to the same focus/confirm path as a keyboard."""
    if screen_name == "title":
        for index in range(4):
            if pygame.Rect(123 + index * 263, 618, 245, 58).collidepoint(position):
                return index
        return None
    if screen_name == "select":
        regions = (
            pygame.Rect(42, 100, 350, 420),
            pygame.Rect(888, 100, 350, 420),
            pygame.Rect(450, 304, 380, 218),
            pygame.Rect(802, 545, 190, 58),
            pygame.Rect(1008, 545, 190, 58),
        )
        return next(
            (index for index, rect in enumerate(regions) if rect.collidepoint(position)), None
        )
    for index in range(12):
        if pygame.Rect(120, 205 + index * 56, 740, 44).collidepoint(position):
            return index
    return None


def _present_event(
    audio: MixerAudioService, effects: ClayEffectPool, reduced: bool, event: PresentationEvent
) -> None:
    audio.dispatch(event)
    effects.trigger(event, reduced)


def run_windowed_g3(title: str, seed: int, on_tick: Callable[[int], None] | None = None) -> int:
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption(title)
    clock, font = pygame.time.Clock(), pygame.font.Font(None, 28)
    settings, diagnostic = load()
    router = InputRouter(bindings=settings.bindings)
    shell, sim_clock = Shell(), FixedStepClock()
    fighters = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
    p1_id, p2_id, training, game = fighters[0], fighters[1], False, None
    cpu_difficulty, cpu = "Medium", None
    stage_id = "electric_assembly_hall"
    title_background = _load_title_background(pygame)
    fighter_crops, stage_previews = _load_selection_art(pygame, title_background)
    match_assets: MatchAssets | None = None
    audio = MixerAudioService(
        pygame,
        AudioLevels(
            settings.audio.master,
            settings.audio.music,
            settings.audio.sfx,
            settings.audio.voice,
            settings.audio.ui,
            tuple(settings.audio.muted),
        ),
    )
    dispatcher, effects = PresentationDispatcher(), ClayEffectPool()
    running = True
    remapping: tuple[int, SemanticAction] | None = None
    last_actions: tuple[set[SemanticAction], set[SemanticAction]] = (set(), set())
    while running:
        elapsed = clock.tick(240)
        disconnected = False
        mouse_confirm = False
        mouse_back = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                router.lifecycle.connect(joystick.get_instance_id(), joystick.get_name())
            elif event.type == pygame.JOYDEVICEREMOVED:
                disconnected = router.lifecycle.disconnect(event.instance_id) is not None
            elif event.type in (pygame.WINDOWFOCUSLOST, pygame.WINDOWMINIMIZED):
                shell.pause("Focus lost")
                router.clear()
            elif event.type == pygame.JOYHATMOTION:
                for direction in ("up", "down", "left", "right"):
                    router.event("hat", f"hat:{direction}", False, event.instance_id)
                direction = {(0, 1): "up", (0, -1): "down", (-1, 0): "left", (1, 0): "right"}.get(
                    event.value
                )
                if direction:
                    router.event("hat", f"hat:{direction}", True, event.instance_id)
            elif event.type == pygame.MOUSEMOTION and shell.screen != "match":
                hovered = _mouse_focus(pygame, shell.screen, event.pos)
                if hovered is not None:
                    shell.focus = hovered
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if shell.screen == "match":
                        mouse_confirm = True
                    else:
                        hovered = _mouse_focus(pygame, shell.screen, event.pos)
                        if hovered is not None:
                            shell.focus = hovered
                            mouse_confirm = True
                elif event.button == 3:
                    mouse_back = True
            else:
                translated = _event_token(pygame, event)
                if translated:
                    router.event(*translated)
                    if (
                        remapping is not None
                        and translated[0] in {"key", "button"}
                        and translated[2]
                    ):
                        try:
                            router.set_binding(remapping[0], remapping[1], translated[1])
                            diagnostic, remapping = "Binding saved.", None
                            save(settings)
                        except ValueError as error:
                            diagnostic, remapping = f"Remap rejected: {error}", None
        if disconnected and game is not None:
            shell.pause("Controller disconnected")
            router.clear()
        edges = router.shell_edges()
        if mouse_confirm:
            edges.add(SemanticAction.CONFIRM)
        if mouse_back:
            edges.add(SemanticAction.BACK)
        if shell.screen != "match":
            entries = {
                "title": ["Start versus", "Training", "Settings", "Controls"],
                "select": [
                    f"P1: {display_name(p1_id)}",
                    f"P2: {display_name(p2_id)}",
                    f"Stage: {stage_id.replace('_', ' ').title()}",
                    f"CPU difficulty: {cpu_difficulty}",
                    "Begin match",
                ],
                "settings": [
                    f"High contrast: {'on' if settings.accessibility.high_contrast else 'off'}",
                    f"Reduced effects: {'on' if settings.accessibility.reduced_effects else 'off'}",
                    f"Master volume: {settings.audio.master}%",
                    f"Music volume: {settings.audio.music}%",
                    f"SFX volume: {settings.audio.sfx}%",
                    f"Voice volume: {settings.audio.voice}%",
                    f"UI volume: {settings.audio.ui}%",
                    "Assign connected controller to P1",
                    "Assign connected controller to P2",
                    "Remap P1 light",
                ],
                "controls": [
                    "P1: A/D/W/S + J/K/L/I/U",
                    "P2: arrows + keypad 1/2/3/0/5",
                    "Controller: D-pad + buttons 0/1/2/3",
                    "Remap via settings.json",
                ],
                "training": ["Start training", "Move list", "Back"],
                "moves": [
                    "Light / Medium / Heavy / Special",
                    "Throw: map a controller button",
                    "Back",
                ],
            }[shell.screen]
            for action in edges:
                shell.navigate(action, len(entries))
            if SemanticAction.BACK in edges:
                shell.screen, shell.focus = ("title", 0)
            if SemanticAction.CONFIRM in edges:
                if shell.screen == "title":
                    shell.screen, shell.focus = (
                        ("select", 0)
                        if shell.focus == 0
                        else ("training", 0)
                        if shell.focus == 1
                        else ("settings", 0)
                        if shell.focus == 2
                        else ("controls", 0)
                    )
                elif shell.screen == "select":
                    if shell.focus == 0:
                        p1_id = fighters[(fighters.index(p1_id) + 1) % len(fighters)]
                    elif shell.focus == 1:
                        p2_id = fighters[(fighters.index(p2_id) + 1) % len(fighters)]
                    elif shell.focus == 2:
                        stage_id = SELECTABLE_STAGES[
                            (SELECTABLE_STAGES.index(stage_id) + 1) % len(SELECTABLE_STAGES)
                        ]
                    elif shell.focus == 3:
                        levels = ("Easy", "Medium", "Hard")
                        cpu_difficulty = levels[(levels.index(cpu_difficulty) + 1) % len(levels)]
                    else:
                        training, shell.screen = False, "match"
                        game, sim_clock = SessionKernel(seed, p1_id, p2_id), FixedStepClock()
                        game.match.fight_start_ticks = 90
                        cpu = CpuController(cpu_difficulty)
                        match_assets = load_match_assets(pygame, (p1_id, p2_id), stage_id)
                        audio.start_match_music(seed)
                elif shell.screen == "training":
                    if shell.focus == 0:
                        training, shell.screen = True, "match"
                        game, sim_clock = (
                            SessionKernel(seed, p1_id, p2_id, training=1),
                            FixedStepClock(),
                        )
                        match_assets = load_match_assets(pygame, (p1_id, p2_id), stage_id)
                        audio.start_match_music(seed)
                    elif shell.focus == 1:
                        shell.screen, shell.focus = "moves", 0
                    else:
                        shell.screen, shell.focus = "title", 0
                elif shell.screen == "settings":
                    if shell.focus < 2:
                        attr = "high_contrast" if shell.focus == 0 else "reduced_effects"
                        setattr(
                            settings.accessibility, attr, not getattr(settings.accessibility, attr)
                        )
                        save(settings)
                    elif shell.focus in {2, 3, 4, 5, 6}:
                        attr = ("master", "music", "sfx", "voice", "ui")[shell.focus - 2]
                        value = (getattr(settings.audio, attr) + 10) % 110
                        setattr(settings.audio, attr, value)
                        audio.apply_levels(
                            AudioLevels(
                                settings.audio.master,
                                settings.audio.music,
                                settings.audio.sfx,
                                settings.audio.voice,
                                settings.audio.ui,
                                tuple(settings.audio.muted),
                            )
                        )
                        save(settings)
                    else:
                        if shell.focus == 9:
                            remapping = (0, SemanticAction.LIGHT)
                            diagnostic = "Press a keyboard key or controller button for P1 light."
                        else:
                            device = next(iter(router.lifecycle.devices), None)
                            if device is not None:
                                router.lifecycle.assign(device, shell.focus - 7)
            detail = (
                diagnostic or "Arrow/D-pad navigate • Enter/button 0 confirm • Esc/button 1 back"
            )
            if shell.screen == "title":
                _draw_title(
                    pygame,
                    screen,
                    shell,
                    entries,
                    detail,
                    settings.accessibility.high_contrast,
                    title_background,
                )
            elif shell.screen == "select":
                _draw_select(
                    pygame,
                    screen,
                    shell,
                    fighters,
                    p1_id,
                    p2_id,
                    stage_id,
                    detail,
                    settings.accessibility.high_contrast,
                    title_background,
                    fighter_crops,
                    stage_previews,
                    cpu_difficulty,
                )
            else:
                _draw_menu(
                    pygame,
                    screen,
                    font,
                    shell,
                    shell.screen.upper(),
                    entries,
                    detail,
                    settings.accessibility.high_contrast,
                )
        elif game is not None and match_assets is not None:
            if game.match.phase is MatchPhase.RESULTS and SemanticAction.CONFIRM in edges:
                complete = max(game.match.p1_round_wins, game.match.p2_round_wins) >= 2
                if match_assets.finisher is not None:
                    match_assets.finisher.teardown()
                    match_assets.finisher = None
                router.clear()
                if complete:
                    shell.screen, shell.focus = "select", 0
                    audio.stop_match_music()
                    game = None
                    continue
                game.reset()
                game.match.fight_start_ticks = 90
                sim_clock.reset()
                if cpu is not None:
                    cpu.previous = 0
            if SemanticAction.PAUSE in edges or SemanticAction.BACK in edges:
                shell.pause("Paused") if not shell.paused else shell.resume()
                router.clear()
            if SemanticAction.OPEN_MOVE_LIST in edges:
                shell.screen, shell.focus = "moves", 0
                router.clear()
            if SemanticAction.RESET in edges and training:
                if match_assets.finisher is not None:
                    match_assets.finisher.teardown()
                    match_assets.finisher = None
                game.reset()
                sim_clock.reset()
                router.clear()
            if not shell.paused:
                for _ in range(sim_clock.consume_wall_ms(elapsed)):
                    frames = router.frames()
                    last_actions = (router.actions_for(0), router.actions_for(1))
                    if cpu is not None and not training:
                        frames = (frames[0], cpu.frame(game.match))
                    game.tick(frames)
                    result = game.match.result
                    if (
                        result is not None
                        and result.finisher_variant
                        and match_assets.finisher is None
                    ):
                        match_assets.finisher = FinisherPlayback(result.finisher_variant)
                    if (
                        game.match.phase in {MatchPhase.KO_HOLD, MatchPhase.FINISHER_WINDOW}
                        and match_assets.finisher is not None
                    ):
                        match_assets.finisher.preload_one(pygame)
                        match_assets.finisher.preload_one(pygame)
                    dispatcher.dispatch(
                        game.presentation_events(),
                        lambda event: _present_event(
                            audio, effects, settings.accessibility.reduced_effects, event
                        ),
                    )
                    effects.advance()
                    if on_tick:
                        on_tick(game.tick_index)
                    if game.match.phase is MatchPhase.RESULTS:
                        break
            draw_match(
                pygame,
                screen,
                font,
                game,
                last_actions,
                training,
                shell.paused,
                shell.pause_reason,
                settings.accessibility.reduced_effects,
                match_assets,
                stage_id,
                effects,
                None if training else cpu_difficulty,
            )
        pygame.display.flip()
    settings.bindings = router.bindings
    settings.onboarding_complete = True
    save(settings)
    audio.shutdown()
    pygame.quit()
    return 0

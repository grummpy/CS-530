"""Pygame presentation shell backed by semantic input and deterministic simulation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fighter.content.roster import display_name
from fighter.platform.clock import FixedStepClock
from fighter.platform.input import InputRouter, SemanticAction
from fighter.platform.settings import load, save
from fighter.presentation.app_loop_assets import MatchAssets, draw_match, load_match_assets
from fighter.presentation.shell import Shell
from fighter.sim.enums import MatchPhase
from fighter.sim.kernel import SessionKernel


def _event_token(pygame: Any, event: Any) -> tuple[str, str, bool, int | None] | None:
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        return "key", f"key:{event.key}", event.type == pygame.KEYDOWN, None
    if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
        return "button", f"button:{event.button}", event.type == pygame.JOYBUTTONDOWN, event.instance_id
    if event.type == pygame.JOYHATMOTION:
        direction = {(0, 1): "up", (0, -1): "down", (-1, 0): "left", (1, 0): "right"}.get(event.value)
        return ("hat", f"hat:{direction}", bool(direction), event.instance_id) if direction else None
    return None


def _draw_menu(pygame: Any, screen: Any, font: Any, shell: Shell, title: str,
               entries: list[str], detail: str, high_contrast: bool) -> None:
    screen.fill((18, 18, 26))
    big = pygame.font.Font(None, 62)
    screen.blit(big.render(title, True, (255, 230, 120)), (80, 70))
    screen.blit(font.render(detail, True, (240, 240, 240)), (80, 135))
    for index, entry in enumerate(entries):
        rect = pygame.Rect(120, 205 + index * 56, 740, 44)
        selected = index == shell.focus
        pygame.draw.rect(screen, (255, 255, 255) if high_contrast and selected else (96, 186, 225)
                         if selected else (48, 48, 66), rect, width=4 if selected else 0, border_radius=6)
        color = (10, 10, 10) if high_contrast and selected else (255, 255, 255)
        screen.blit(font.render(f"{'▶ ' if selected else '  '}{entry}", True, color), (138, rect.y + 11))


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
    match_assets: MatchAssets | None = None
    running = True
    remapping: tuple[int, SemanticAction] | None = None
    last_actions: tuple[set[SemanticAction], set[SemanticAction]] = (set(), set())
    while running:
        elapsed = clock.tick(240)
        disconnected = False
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
            else:
                translated = _event_token(pygame, event)
                if translated:
                    router.event(*translated)
                    if remapping is not None and translated[0] in {"key", "button"} and translated[2]:
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
        if shell.screen != "match":
            entries = {
                "title": ["Start versus", "Training", "Settings", "Controls"],
                "select": [f"P1: {display_name(p1_id)}", f"P2: {display_name(p2_id)}", "Begin match"],
                "settings": [f"High contrast: {'on' if settings.accessibility.high_contrast else 'off'}",
                             f"Reduced effects: {'on' if settings.accessibility.reduced_effects else 'off'}",
                             "Assign connected controller to P1", "Assign connected controller to P2",
                             "Remap P1 light"],
                "controls": ["P1: A/D/W/S + F/G/H/J/T", "P2: arrows + keypad 1/2/3/0/5",
                             "Controller: D-pad + buttons 0/1/2/3", "Remap via settings.json"],
                "training": ["Start training", "Move list", "Back"],
                "moves": ["Light / Medium / Heavy / Special", "Throw: map a controller button", "Back"],
            }[shell.screen]
            for action in edges:
                shell.navigate(action, len(entries))
            if SemanticAction.BACK in edges:
                shell.screen, shell.focus = ("title", 0)
            if SemanticAction.CONFIRM in edges:
                if shell.screen == "title":
                    shell.screen, shell.focus = (("select", 0) if shell.focus == 0 else
                                                 ("training", 0) if shell.focus == 1 else
                                                 ("settings", 0) if shell.focus == 2 else ("controls", 0))
                elif shell.screen == "select":
                    if shell.focus == 0:
                        p1_id = fighters[(fighters.index(p1_id) + 1) % len(fighters)]
                    elif shell.focus == 1:
                        p2_id = fighters[(fighters.index(p2_id) + 1) % len(fighters)]
                    else:
                        training, shell.screen = False, "match"
                        game, sim_clock = SessionKernel(seed, p1_id, p2_id), FixedStepClock()
                        match_assets = load_match_assets(pygame, (p1_id, p2_id))
                elif shell.screen == "training":
                    if shell.focus == 0:
                        training, shell.screen = True, "match"
                        game, sim_clock = SessionKernel(seed, p1_id, p2_id, training=1), FixedStepClock()
                        match_assets = load_match_assets(pygame, (p1_id, p2_id))
                    elif shell.focus == 1:
                        shell.screen, shell.focus = "moves", 0
                    else:
                        shell.screen, shell.focus = "title", 0
                elif shell.screen == "settings":
                    if shell.focus < 2:
                        attr = "high_contrast" if shell.focus == 0 else "reduced_effects"
                        setattr(settings.accessibility, attr, not getattr(settings.accessibility, attr))
                        save(settings)
                    else:
                        if shell.focus == 4:
                            remapping = (0, SemanticAction.LIGHT)
                            diagnostic = "Press a keyboard key or controller button for P1 light."
                        else:
                            device = next(iter(router.lifecycle.devices), None)
                            if device is not None:
                                router.lifecycle.assign(device, shell.focus - 2)
            _draw_menu(pygame, screen, font, shell, shell.screen.upper(), entries,
                       diagnostic or "Arrow/D-pad navigate • Enter/button 0 confirm • Esc/button 1 back",
                       settings.accessibility.high_contrast)
        elif game is not None and match_assets is not None:
            if SemanticAction.PAUSE in edges or SemanticAction.BACK in edges:
                shell.pause("Paused") if not shell.paused else shell.resume()
                router.clear()
            if SemanticAction.OPEN_MOVE_LIST in edges:
                shell.screen, shell.focus = "moves", 0
                router.clear()
            if SemanticAction.RESET in edges and training:
                game.reset()
                sim_clock.reset()
                router.clear()
            if not shell.paused:
                for _ in range(sim_clock.consume_wall_ms(elapsed)):
                    frames = router.frames()
                    last_actions = (router.actions_for(0), router.actions_for(1))
                    game.tick(frames)
                    if on_tick:
                        on_tick(game.tick_index)
                    if game.match.phase is MatchPhase.RESULTS:
                        break
            draw_match(pygame, screen, font, game, last_actions, training, shell.paused,
                       shell.pause_reason, settings.accessibility.reduced_effects, match_assets)
        pygame.display.flip()
    settings.bindings = router.bindings
    settings.onboarding_complete = True
    save(settings)
    pygame.quit()
    return 0

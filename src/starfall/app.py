"""Pygame presentation layer for the local arcade-fighter engine."""

from __future__ import annotations

import pygame

from .game import FIXED_TIMESTEP, GROUND_Y, WORLD_HEIGHT, WORLD_WIDTH, FighterInput, GameState

BACKGROUND = (16, 20, 39)
STAGE = (37, 50, 80)
GRID = (63, 82, 123)
TEXT = (243, 245, 255)
GOLD = (255, 211, 90)


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    pygame.display.set_caption("Starfall Arena")
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 52)
    ui_font = pygame.font.Font(None, 28)
    game = GameState()
    accumulator = 0.0
    running = True

    while running:
        dt = min(clock.tick(120) / 1000, 0.1)
        accumulator += dt
        p1_edge, p2_edge = _read_events()
        if p1_edge is None:
            running = False
            continue
        keys = pygame.key.get_pressed()
        p1 = FighterInput(
            move=int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
            jump=p1_edge.jump,
            light=p1_edge.light,
            heavy=p1_edge.heavy,
        )
        p2 = FighterInput(
            move=int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]),
            jump=p2_edge.jump,
            light=p2_edge.light,
            heavy=p2_edge.heavy,
        )
        if game.match_over and (p1.light or p2.light):
            game = GameState()
        while accumulator >= FIXED_TIMESTEP:
            game.step(FIXED_TIMESTEP, p1, p2)
            p1 = FighterInput(move=p1.move)
            p2 = FighterInput(move=p2.move)
            accumulator -= FIXED_TIMESTEP
        _draw(screen, game, title_font, ui_font)
        pygame.display.flip()

    pygame.quit()


def _read_events() -> tuple[FighterInput | None, FighterInput]:
    p1 = FighterInput()
    p2 = FighterInput()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, p2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p1 = FighterInput(jump=True)
            elif event.key == pygame.K_f:
                p1 = FighterInput(light=True)
            elif event.key == pygame.K_g:
                p1 = FighterInput(heavy=True)
            elif event.key == pygame.K_UP:
                p2 = FighterInput(jump=True)
            elif event.key == pygame.K_k:
                p2 = FighterInput(light=True)
            elif event.key == pygame.K_l:
                p2 = FighterInput(heavy=True)
    return p1, p2


def _draw(
    screen: pygame.Surface, game: GameState, title_font: pygame.font.Font, ui_font: pygame.font.Font
) -> None:
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, STAGE, (0, GROUND_Y + 2, WORLD_WIDTH, WORLD_HEIGHT - GROUND_Y))
    for x in range(0, WORLD_WIDTH, 48):
        pygame.draw.line(screen, GRID, (x, GROUND_Y), (x, WORLD_HEIGHT), 1)
    pygame.draw.line(screen, GOLD, (0, GROUND_Y), (WORLD_WIDTH, GROUND_Y), 3)

    _health_bar(screen, 24, 24, game.fighters[0].health, game.fighters[0].color, False)
    _health_bar(screen, WORLD_WIDTH - 344, 24, game.fighters[1].health, game.fighters[1].color, True)
    timer = title_font.render(str(int(game.round_timer + 0.99)).zfill(2), True, GOLD)
    screen.blit(timer, timer.get_rect(center=(WORLD_WIDTH // 2, 48)))
    _wins(screen, 250, game.wins[0])
    _wins(screen, WORLD_WIDTH - 250, game.wins[1])

    for fighter in game.fighters:
        _draw_fighter(screen, fighter, ui_font)

    controls = ui_font.render("P1: A/D + W + F/G     P2: arrows + K/L", True, TEXT)
    screen.blit(controls, controls.get_rect(center=(WORLD_WIDTH // 2, WORLD_HEIGHT - 26)))
    if game.round_over or game.match_over:
        banner = pygame.Surface((WORLD_WIDTH, 100), pygame.SRCALPHA)
        banner.fill((0, 0, 0, 180))
        screen.blit(banner, (0, 170))
        message = title_font.render(game.winner_text(), True, GOLD)
        screen.blit(message, message.get_rect(center=(WORLD_WIDTH // 2, 208)))
        if game.match_over:
            restart = ui_font.render("Press F or K to restart", True, TEXT)
            screen.blit(restart, restart.get_rect(center=(WORLD_WIDTH // 2, 244)))


def _health_bar(
    screen: pygame.Surface, x: int, y: int, health: int, color: tuple[int, int, int], mirrored: bool
) -> None:
    width, height = 320, 24
    pygame.draw.rect(screen, (50, 53, 68), (x, y, width, height), border_radius=4)
    remaining = round(width * health / 1000)
    fill_x = x + width - remaining if mirrored else x
    pygame.draw.rect(screen, color, (fill_x, y, remaining, height), border_radius=4)
    pygame.draw.rect(screen, TEXT, (x, y, width, height), 2, border_radius=4)


def _wins(screen: pygame.Surface, x: int, wins: int) -> None:
    for index in range(2):
        color = GOLD if index < wins else (75, 78, 95)
        pygame.draw.circle(screen, color, (x + index * 20, 58), 6)


def _draw_fighter(screen: pygame.Surface, fighter: object, font: pygame.font.Font) -> None:
    x, y = round(fighter.x), round(fighter.y)
    width, height = round(fighter.width), round(fighter.height)
    rect = pygame.Rect(x - width // 2, y - height, width, height)
    pygame.draw.rect(screen, fighter.color, rect, border_radius=8)
    pygame.draw.circle(screen, TEXT, (x + fighter.facing * 11, y - height + 22), 5)
    if fighter.attack_active:
        reach = round(fighter.attack.reach)
        hitbox = pygame.Rect(x, y - height + 18, reach, 44)
        if fighter.facing < 0:
            hitbox.right = x
        pygame.draw.rect(screen, GOLD, hitbox, 2)
    label = font.render(fighter.name, True, TEXT)
    screen.blit(label, label.get_rect(center=(x, y + 16)))

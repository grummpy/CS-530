"""Simple local-versus visual shell with keyboard controls."""
from collections.abc import Callable
from pathlib import Path
from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.presentation.audio import start_match_music


def _load_stage(pygame: object) -> object | None:
    """Load approved arena art once; preserve a playable fallback on failure."""
    path = Path(__file__).resolve().parents[3] / "assets" / "stages" / "roadside_truck_stop_concept.png"
    try:
        return pygame.transform.smoothscale(pygame.image.load(path.as_posix()).convert(), (1280, 720))
    except (OSError, pygame.error):
        return None


def _load_fighter_sprite(pygame: object, fighter_id: str) -> object | None:
    path = Path(__file__).resolve().parents[3] / "assets" / "characters" / fighter_id / "portrait.png"
    try:
        image = pygame.image.load(path.as_posix()).convert_alpha()
        return pygame.transform.smoothscale(image, (210, 320))
    except (OSError, pygame.error):
        return None


def run_windowed_g3(title: str, seed: int, on_tick: Callable[[int], None] | None = None) -> int:
    import pygame
    pygame.init(); screen = pygame.display.set_mode((1280, 720)); pygame.display.set_caption(title); clock = pygame.time.Clock(); font = pygame.font.Font(None, 28)
    stage = _load_stage(pygame)
    start_match_music(pygame, seed)
    game = SessionKernel(seed=seed, p1_id="rhinestone_angel", p2_id="baron_boardroom"); previous = [0, 0]; running = True
    fighter_sprites = {fighter_id: _load_fighter_sprite(pygame, fighter_id) for fighter_id in (game.match.p1.fighter_id, game.match.p2.fighter_id)}
    bindings = ((pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j), (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: game.reset()
        keys = pygame.key.get_pressed(); frames=[]
        for index, group in enumerate(bindings):
            held = (Action.LEFT if keys[group[0]] else 0) | (Action.RIGHT if keys[group[1]] else 0) | (Action.LIGHT if keys[group[4]] else 0) | (Action.MEDIUM if keys[group[5]] else 0) | (Action.HEAVY if keys[group[6]] else 0) | (Action.SPECIAL if keys[group[7]] else 0)
            frames.append(InputFrame.from_held(previous[index], held)); previous[index] = held
        game.tick((frames[0], frames[1])); m=game.match; screen.fill((37, 33, 55))
        if stage is not None: screen.blit(stage, (0, 0))
        else: pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120))
        for f, color in ((m.p1,(196,75,67)), (m.p2,(60,150,182))):
            sprite = fighter_sprites.get(f.fighter_id)
            if sprite is None: pygame.draw.rect(screen, color, (f.x-35,440,70,160), border_radius=18)
            else: screen.blit(sprite, (f.x-105, 280))
        pygame.draw.rect(screen,(80,20,25),(40,35,500,24)); pygame.draw.rect(screen,(65,180,90),(40,35,m.p1.health//2,24)); pygame.draw.rect(screen,(80,20,25),(740,35,500,24)); pygame.draw.rect(screen,(65,180,90),(1240-m.p2.health//2,35,m.p2.health//2,24))
        screen.blit(font.render("P1 A/D + F/G/H/J    P2 arrows + keypad 1/2/3/0    R reset    Esc quit", True, (245,245,245)),(230,680)); pygame.display.flip(); clock.tick(60)
        if on_tick: on_tick(game.tick_index)
    pygame.mixer.music.stop()
    pygame.quit(); return 0

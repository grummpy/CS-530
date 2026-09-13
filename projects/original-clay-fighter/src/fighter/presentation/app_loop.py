"""Simple local-versus visual shell with keyboard controls."""
from collections.abc import Callable
from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel

def run_windowed_g3(title: str, seed: int, on_tick: Callable[[int], None] | None = None) -> int:
    import pygame
    pygame.init(); screen = pygame.display.set_mode((1280, 720)); pygame.display.set_caption(title); clock = pygame.time.Clock(); font = pygame.font.Font(None, 28)
    game = SessionKernel(seed=seed, p1_id="captain_campaign", p2_id="baron_boardroom"); previous = [0, 0]; running = True
    bindings = ((pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f, pygame.K_g, pygame.K_h), (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: game.reset()
        keys = pygame.key.get_pressed(); frames=[]
        for index, group in enumerate(bindings):
            held = (Action.LEFT if keys[group[0]] else 0) | (Action.RIGHT if keys[group[1]] else 0) | (Action.LIGHT if keys[group[4]] else 0) | (Action.MEDIUM if keys[group[5]] else 0) | (Action.HEAVY if keys[group[6]] else 0)
            frames.append(InputFrame.from_held(previous[index], held)); previous[index] = held
        game.tick((frames[0], frames[1])); m=game.match; screen.fill((37, 33, 55))
        pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120));
        for f, color in ((m.p1,(196,75,67)), (m.p2,(60,150,182))): pygame.draw.rect(screen,color,(f.x-35,440,70,160),border_radius=18)
        pygame.draw.rect(screen,(80,20,25),(40,35,500,24)); pygame.draw.rect(screen,(65,180,90),(40,35,m.p1.health//2,24)); pygame.draw.rect(screen,(80,20,25),(740,35,500,24)); pygame.draw.rect(screen,(65,180,90),(1240-m.p2.health//2,35,m.p2.health//2,24))
        screen.blit(font.render("P1 A/D + F/G/H    P2 arrows + keypad 1/2/3    R reset    Esc quit", True, (245,245,245)),(260,680)); pygame.display.flip(); clock.tick(60)
        if on_tick: on_tick(game.tick_index)
    pygame.quit(); return 0

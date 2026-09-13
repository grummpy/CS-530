"""Simple local-versus visual shell with keyboard controls."""
from collections.abc import Callable
import json
from pathlib import Path
from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.presentation.audio import start_match_music
from fighter.presentation.finishers import finisher_frame_paths


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


def _load_fighter_clips(pygame: object, fighter_id: str) -> dict[str, list[object]]:
    root = Path(__file__).resolve().parents[3] / "assets" / "characters" / fighter_id
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        return {name: [pygame.transform.smoothscale(pygame.image.load((root / "sprites" / frame).as_posix()).convert_alpha(), (320, 320)) for frame in clip["frames"]] for name, clip in manifest["clips"].items()}
    except (OSError, ValueError, KeyError, pygame.error):
        return {}


def _active_clip(fighter: object) -> str:
    if fighter.stun_ticks: return "hit"
    if fighter.attack_ticks:
        if fighter.fighter_id == "tech_billionaire":
            if fighter.attack_kind == 4: return "exosuit_call"
            if fighter.armor_ticks: return "armor_kick" if fighter.attack_kind == 3 else "armor_punch"
        return {1: "light", 2: "medium", 3: "heavy", 4: "hostile_takeover" if fighter.fighter_id == "mr_president" else "kitchen_rush" if fighter.fighter_id == "master_chef" else "star_chord"}.get(fighter.attack_kind, "idle")
    if fighter.fighter_id == "tech_billionaire" and fighter.armor_ticks: return "armor_idle"
    return "idle"


def run_windowed_g3(title: str, seed: int, on_tick: Callable[[int], None] | None = None) -> int:
    import pygame
    pygame.init(); screen = pygame.display.set_mode((1280, 720)); pygame.display.set_caption(title); clock = pygame.time.Clock(); font = pygame.font.Font(None, 28)
    stage = _load_stage(pygame)
    start_match_music(pygame, seed)
    game = SessionKernel(seed=seed, p1_id="rhinestone_angel", p2_id="master_chef"); previous = [0, 0]; running = True
    finisher_frames: list[object] = []; finisher_frame_index = 0
    fighter_sprites = {fighter_id: _load_fighter_sprite(pygame, fighter_id) for fighter_id in (game.match.p1.fighter_id, game.match.p2.fighter_id)}
    fighter_clips = {fighter_id: _load_fighter_clips(pygame, fighter_id) for fighter_id in (game.match.p1.fighter_id, game.match.p2.fighter_id)}
    bindings = ((pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j), (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: game.reset(); finisher_frames = []; finisher_frame_index = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finisher_frames: finisher_frame_index = len(finisher_frames) - 1
        keys = pygame.key.get_pressed(); frames=[]
        for index, group in enumerate(bindings):
            held = (Action.LEFT if keys[group[0]] else 0) | (Action.RIGHT if keys[group[1]] else 0) | (Action.LIGHT if keys[group[4]] else 0) | (Action.MEDIUM if keys[group[5]] else 0) | (Action.HEAVY if keys[group[6]] else 0) | (Action.SPECIAL if keys[group[7]] else 0)
            frames.append(InputFrame.from_held(previous[index], held)); previous[index] = held
        game.tick((frames[0], frames[1])); m=game.match; screen.fill((37, 33, 55))
        if stage is not None: screen.blit(stage, (0, 0))
        else: pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120))
        if m.phase == 2:
            if not finisher_frames:
                winner, loser = (m.p1, m.p2) if m.p2.health == 0 else (m.p2, m.p1)
                finisher_frames = [pygame.transform.smoothscale(pygame.image.load(path.as_posix()).convert(), (1280, 720)) for path in finisher_frame_paths(winner.fighter_id, loser.fighter_id)]
            if finisher_frames:
                screen.blit(finisher_frames[min(finisher_frame_index, len(finisher_frames) - 1)], (0, 0)); finisher_frame_index = min(finisher_frame_index + 1, len(finisher_frames) - 1)
                screen.blit(font.render("FINISHER — Space skips — R resets", True, (255, 240, 190)), (465, 680)); pygame.display.flip(); clock.tick(10)
                if on_tick: on_tick(game.tick_index)
                continue
        for f, color in ((m.p1,(196,75,67)), (m.p2,(60,150,182))):
            frames = fighter_clips.get(f.fighter_id, {}).get(_active_clip(f), [])
            if frames:
                frame = frames[(m.tick // 4) % len(frames)]
                screen.blit(pygame.transform.flip(frame, f.facing < 0, False), (f.x - 160, 300))
            else:
                pygame.draw.rect(screen, color, (f.x-35,440,70,160), border_radius=18)
        portrait = fighter_sprites.get(m.p1.fighter_id)
        if portrait is not None:
            screen.blit(pygame.transform.smoothscale(portrait, (80, 120)), (18, 70))
        pygame.draw.rect(screen,(80,20,25),(40,35,500,24)); pygame.draw.rect(screen,(65,180,90),(40,35,m.p1.health//2,24)); pygame.draw.rect(screen,(80,20,25),(740,35,500,24)); pygame.draw.rect(screen,(65,180,90),(1240-m.p2.health//2,35,m.p2.health//2,24))
        screen.blit(font.render("P1 A/D + F/G/H/J    P2 arrows + keypad 1/2/3/0    R reset    Esc quit", True, (245,245,245)),(230,680)); pygame.display.flip(); clock.tick(60)
        if on_tick: on_tick(game.tick_index)
    pygame.mixer.music.stop()
    pygame.quit(); return 0

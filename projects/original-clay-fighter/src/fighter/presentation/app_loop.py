"""Simple local-versus visual shell with keyboard controls."""
from collections.abc import Callable
import json
from pathlib import Path
import random
from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.presentation.audio import start_match_music
from fighter.presentation.finishers import finisher_frame_paths
from fighter.content.roster import display_name


def _load_stage(pygame: object, stage_id: str) -> object | None:
    """Load approved arena art once; preserve a playable fallback on failure."""
    names = {
        "roadside_truck_stop": "roadside_truck_stop_concept.png",
        "executive_lawn": "executive_lawn_concept.png",
        "electric_assembly_hall": "electric_assembly_hall_concept.png",
    }
    path = Path(__file__).resolve().parents[3] / "assets" / "stages" / names[stage_id]
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
    fighters = ("rhinestone_angel", "mr_president", "tech_billionaire", "master_chef")
    slogans = {"rhinestone_angel":"Make every note hurt.", "mr_president":"Deal with it.", "tech_billionaire":"Disrupt the competition.", "master_chef":"Dinner is served."}
    stages = ("roadside_truck_stop", "executive_lawn", "electric_assembly_hall")
    portraits = {fid: _load_fighter_sprite(pygame, fid) for fid in fighters}
    title_clips = {fid: _load_fighter_clips(pygame, fid) for fid in fighters}
    ui_state, p1_id, p2_id, stage_id, cpu = "title", fighters[0], fighters[1], stages[0], True
    while ui_state != "match":
        mouse = pygame.mouse.get_pos(); click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.quit(); return 0
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE): ui_state = "select" if ui_state == "title" else "match"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and ui_state == "select": cpu = not cpu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: click = True
        screen.fill((27, 24, 38)); big = pygame.font.Font(None, 74)
        if ui_state == "title":
            screen.blit(big.render("PAPIER PARADE", True, (255, 208, 77)), (420, 52)); screen.blit(font.render("Clay comedy. Dark splats. Four fighters.", True, (235,235,235)), (447, 122))
            for index, fid in enumerate(fighters):
                x = 110 + index * 285; hovered = pygame.Rect(x, 220, 220, 300).collidepoint(mouse)
                pygame.draw.rect(screen, (92,52,110) if hovered else (48,44,62), (x,220-(12 if hovered else 0),220,300), border_radius=16)
                pose = title_clips[fid].get("heavy", []) if hovered else []
                if pose:
                    screen.blit(pygame.transform.smoothscale(pose[(pygame.time.get_ticks() // 125) % len(pose)], (150, 220)), (x + 35, 245 - (12 if hovered else 0)))
                elif portraits[fid]: screen.blit(pygame.transform.smoothscale(portraits[fid], (150,220)), (x+35,245-(12 if hovered else 0)))
                screen.blit(font.render(display_name(fid), True, (255,255,255)), (x+14,480)); screen.blit(font.render(slogans[fid], True, (255,210,135)), (x+14,510))
            button = pygame.Rect(500,610,280,58); pygame.draw.rect(screen,(185,54,72),button,border_radius=12); screen.blit(font.render("START GAME",True,(255,255,255)),(565,627))
            if click and button.collidepoint(mouse): ui_state="select"
        else:
            screen.blit(big.render("SELECT FIGHTERS + ARENA",True,(255,208,77)),(290,35))
            for index,fid in enumerate(fighters):
                x=90+index*295; card=pygame.Rect(x,150,250,310); pygame.draw.rect(screen,(72,80,112) if fid in (p1_id,p2_id) else (48,44,62),card,border_radius=12)
                if portraits[fid]: screen.blit(pygame.transform.smoothscale(portraits[fid],(130,190)),(x+60,165))
                screen.blit(font.render(display_name(fid),True,(255,255,255)),(x+22,360));screen.blit(font.render(slogans[fid],True,(255,210,135)),(x+22,392))
                if click and card.collidepoint(mouse):
                    if mouse[1] < 305:
                        p1_id = fid
                    else:
                        p2_id = fid
            screen.blit(font.render("Click upper card half: P1. Lower card half: P2. Toggle CPU: C",True,(235,235,235)),(315,490))
            screen.blit(font.render(f"P1: {display_name(p1_id)}     P2: {'CPU' if cpu else display_name(p2_id)}",True,(255,255,255)),(390,525))
            for index,stage in enumerate(stages):
                rect=pygame.Rect(180+index*300,560,250,42);pygame.draw.rect(screen,(70,135,120) if stage==stage_id else (48,44,62),rect,border_radius=8);screen.blit(font.render(stage.replace('_',' ').title(),True,(255,255,255)),(rect.x+12,570))
                if click and rect.collidepoint(mouse): stage_id=stage
            go=pygame.Rect(500,625,280,52);pygame.draw.rect(screen,(185,54,72),go,border_radius=12);screen.blit(font.render("FIGHT!",True,(255,255,255)),(600,640))
            if click and go.collidepoint(mouse): ui_state="match"
        pygame.display.flip(); clock.tick(60)
    if cpu:
        cpu_choices = tuple(fid for fid in fighters if fid != p1_id)
        p2_id = random.Random(seed).choice(cpu_choices)
    stage = _load_stage(pygame, stage_id)
    start_match_music(pygame, seed)
    game = SessionKernel(seed=seed, p1_id=p1_id, p2_id=p2_id); previous = [0, 0]; running = True; cpu_rng = random.Random(seed ^ 0xC1A7)
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
            held = (Action.LEFT if keys[group[0]] else 0) | (Action.RIGHT if keys[group[1]] else 0) | (Action.UP if keys[group[2]] else 0) | (Action.DOWN if keys[group[3]] else 0) | (Action.LIGHT if keys[group[4]] else 0) | (Action.MEDIUM if keys[group[5]] else 0) | (Action.HEAVY if keys[group[6]] else 0) | (Action.SPECIAL if keys[group[7]] else 0)
            if index == 1 and cpu:
                opponent, bot = game.match.p1, game.match.p2
                held = Action.LEFT if bot.x > opponent.x else Action.RIGHT
                if abs(bot.x - opponent.x) < 105 and not bot.attack_ticks and not bot.stun_ticks and cpu_rng.randrange(24) == 0:
                    held |= cpu_rng.choice((Action.LIGHT, Action.MEDIUM, Action.HEAVY, Action.SPECIAL if bot.special_charge >= 210 else Action.HEAVY))
            frames.append(InputFrame.from_held(previous[index], held)); previous[index] = held
        game.tick((frames[0], frames[1])); m=game.match; screen.fill((37, 33, 55))
        if stage is not None: screen.blit(stage, (0, 0))
        else: pygame.draw.rect(screen, (224, 200, 134), (0, 600, 1280, 120))
        if m.phase == 2:
            if not finisher_frames:
                winner, loser = (m.p1, m.p2) if m.p1.health >= m.p2.health else (m.p2, m.p1)
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
        pygame.draw.rect(screen, (38, 32, 72), (40, 64, 500, 12)); pygame.draw.rect(screen, (238, 191, 53), (40, 64, 500 * m.p1.special_charge // 210, 12))
        pygame.draw.rect(screen, (38, 32, 72), (740, 64, 500, 12)); pygame.draw.rect(screen, (238, 191, 53), (1240 - 500 * m.p2.special_charge // 210, 64, 500 * m.p2.special_charge // 210, 12))
        seconds = (m.round_ticks + 59) // 60
        screen.blit(font.render(f"{seconds:02d}", True, (255, 240, 190)), (612, 32)); screen.blit(font.render("SPECIAL", True, (255, 230, 120)), (40, 80)); screen.blit(font.render("SPECIAL", True, (255, 230, 120)), (1160, 80))
        for f in (m.p1, m.p2):
            if f.blocking: pygame.draw.circle(screen, (115, 210, 255), (f.x, 462), 76, 4)
        controls = "P1 A/D/W/S + F/G/H/J    CPU" if cpu else "P1 A/D/W/S + F/G/H/J    P2 arrows + keypad 1/2/3/0"
        screen.blit(font.render(f"{controls}    S/down blocks    R reset    Esc quit", True, (245,245,245)),(230,680)); pygame.display.flip(); clock.tick(60)
        if on_tick: on_tick(game.tick_index)
    pygame.mixer.music.stop()
    pygame.quit(); return 0

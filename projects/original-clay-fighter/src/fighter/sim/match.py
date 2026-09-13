"""Small deterministic combat loop; presentation never mutates this module's state."""

from fighter.sim.bits import Action
from fighter.sim.constants import LEFT_WALL, RIGHT_WALL, WALK_SPEED
from fighter.sim.input_frame import InputFrame
from fighter.sim.state import FighterState, MatchState, initial_match


def new_match(
    seed: int = 1, p1_id: str = "graybox_rival", p2_id: str = "graybox_rival", training: int = 0
) -> MatchState:
    return initial_match(seed, p1_id, p2_id, training)


def reset_round(match: MatchState) -> None:
    fresh = initial_match(match.seed, match.p1.fighter_id, match.p2.fighter_id, match.training)
    match.p1, match.p2, match.tick, match.phase, match.events, match.round_ticks = (
        fresh.p1,
        fresh.p2,
        fresh.tick,
        fresh.phase,
        [],
        fresh.round_ticks,
    )


def _move(f: FighterState, held: int) -> None:
    f.blocking = bool(held & Action.DOWN) and not f.attack_ticks
    if f.stun_ticks or f.attack_ticks:
        return
    direction = (1 if held & Action.RIGHT else 0) - (1 if held & Action.LEFT else 0)
    f.x = max(LEFT_WALL, min(RIGHT_WALL, f.x + direction * WALK_SPEED))


ARMOR_CHARGE_THRESHOLD = 210
ARMOR_DURATION_TICKS = 600


def _start_attack(f: FighterState, pressed: int, events: list[str]) -> None:
    if f.stun_ticks or f.attack_ticks:
        return
    for action, kind, length in (
        (Action.LIGHT, 1, 12),
        (Action.MEDIUM, 2, 18),
        (Action.HEAVY, 3, 25),
        (Action.SPECIAL, 4, 28),
        (Action.THROW, 4, 16),
    ):
        if pressed & action:
            if action == Action.SPECIAL:
                if f.special_charge < ARMOR_CHARGE_THRESHOLD:
                    return
                f.special_charge = 0
                if f.fighter_id == "tech_billionaire":
                    f.armor_charge = 0
                    f.armor_ticks = ARMOR_DURATION_TICKS
                    events.append("armor_mode_on")
            f.attack_kind, f.attack_ticks, f.hit_this_attack = kind, length, False
            return


def _resolve(attacker: FighterState, defender: FighterState, events: list[str]) -> None:
    if not attacker.attack_ticks or attacker.hit_this_attack:
        return
    active = attacker.attack_ticks in {attacker.attack_kind + 5, attacker.attack_kind + 6}
    if active and abs(attacker.x - defender.x) < 112:
        damage = 35 * attacker.attack_kind + (
            3 if attacker.fighter_id == "tech_billionaire" and attacker.armor_ticks else 0
        )
        if defender.blocking:
            damage = max(1, damage // 3)
            events.append("block")
        absorbed = damage
        defender.health = max(0, defender.health - damage)
        if defender.fighter_id == "tech_billionaire":
            defender.armor_charge = min(ARMOR_CHARGE_THRESHOLD, defender.armor_charge + absorbed)
        defender.special_charge = min(ARMOR_CHARGE_THRESHOLD, defender.special_charge + absorbed)
        defender.stun_ticks = 8 + attacker.attack_kind * 3
        attacker.hit_this_attack = True
        events.append("hit")


def tick(match: MatchState, inputs: tuple[InputFrame, InputFrame]) -> None:
    if match.phase != 1:
        return
    match.events.clear()
    for fighter, frame in zip((match.p1, match.p2), inputs, strict=True):
        fighter.facing = 1 if fighter is match.p1 else -1
        _move(fighter, frame.held)
        _start_attack(fighter, frame.pressed, match.events)
    _resolve(match.p1, match.p2, match.events)
    _resolve(match.p2, match.p1, match.events)
    for fighter in (match.p1, match.p2):
        fighter.attack_ticks = max(0, fighter.attack_ticks - 1)
        fighter.stun_ticks = max(0, fighter.stun_ticks - 1)
        if fighter.armor_ticks:
            fighter.armor_ticks -= 1
            if fighter.armor_ticks == 0:
                match.events.append("armor_mode_off")
    if not match.training:
        match.round_ticks = max(0, match.round_ticks - 1)
        if match.p1.health == 0 or match.p2.health == 0 or match.round_ticks == 0:
            match.phase = 2
            match.events.append("ko")
    match.tick += 1

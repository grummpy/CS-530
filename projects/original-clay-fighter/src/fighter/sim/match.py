"""Small deterministic combat loop; presentation never mutates this module's state."""

from fighter.content.loader import FighterDefinition, load_fighter
from fighter.sim.bits import Action
from fighter.sim.boxes import Box
from fighter.sim.constants import LEFT_WALL, RIGHT_WALL, WALK_SPEED
from fighter.sim.input_frame import InputFrame
from fighter.sim.moves import MoveDefinition
from fighter.sim.state import FighterState, MatchState, initial_match


def new_match(
    seed: int = 1, p1_id: str = "graybox_rival", p2_id: str = "graybox_rival", training: int = 0
) -> MatchState:
    return initial_match(seed, p1_id, p2_id, training, load_fighter(p1_id), load_fighter(p2_id))


def reset_round(match: MatchState) -> None:
    fresh = new_match(match.seed, match.p1.fighter_id, match.p2.fighter_id, match.training)
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


def _attack_kind(move_name: str) -> int:
    return {"light": 1, "medium": 2, "heavy": 3}.get(move_name, 4)


def _start_attack(
    f: FighterState, definition: FighterDefinition, pressed: int, events: list[str]
) -> None:
    if f.stun_ticks or f.attack_ticks:
        return
    for action, move_name in (
        (Action.LIGHT, "light"),
        (Action.MEDIUM, "medium"),
        (Action.HEAVY, "heavy"),
        (Action.SPECIAL, definition.profile.special_id),
    ):
        if not (pressed & action) or move_name is None:
            continue
        if action == Action.SPECIAL:
            move = definition.moves.get(move_name)
            charge_requirement = (
                definition.profile.armor_charge_requirement
                if definition.profile.armor_charge_requirement is not None
                else move.meter_cost if move is not None else 0
            )
            if f.special_charge < charge_requirement:
                return
            f.special_charge = 0
            if definition.profile.armor_charge_requirement is not None:
                f.armor_charge = 0
                f.armor_ticks = definition.profile.armor_duration_ticks
                events.append("armor_mode_on")
                return
        move = definition.moves.get(move_name)
        if move is None:
            return
        f.attack_kind = _attack_kind(move_name)
        f.attack_move = move_name
        f.attack_ticks = move.total
        f.hit_this_attack = False
        return


def _active_hitbox(attacker: FighterState, move: MoveDefinition) -> Box | None:
    frame = move.total - attacker.attack_ticks + 1
    for window in move.hitboxes:
        if window.start <= frame <= window.end:
            return window.box.world(attacker.x, 600, attacker.facing)
    return None


def _resolve(
    attacker: FighterState,
    defender: FighterState,
    definition: FighterDefinition,
    defender_definition: FighterDefinition,
    events: list[str],
) -> None:
    if not attacker.attack_ticks or attacker.hit_this_attack:
        return
    move = definition.moves[attacker.attack_move]
    hitbox = _active_hitbox(attacker, move)
    defender_box = defender_definition.hurt_box.world(defender.x, 600, defender.facing)
    if hitbox is not None and hitbox.intersects(defender_box):
        damage = move.damage + (
            definition.profile.armor_damage_bonus if attacker.armor_ticks else 0
        )
        if defender.blocking:
            damage = max(1, damage // 3)
            events.append("block")
        absorbed = damage
        defender.health = max(0, defender.health - damage)
        charge_limit = (
            defender_definition.profile.armor_charge_requirement
            if defender_definition.profile.armor_charge_requirement is not None
            else max((candidate.meter_cost for candidate in defender_definition.moves.values()), default=0)
        )
        if defender_definition.profile.armor_charge_requirement is not None:
            defender.armor_charge = min(charge_limit, defender.armor_charge + absorbed)
        defender.special_charge = min(charge_limit, defender.special_charge + absorbed)
        defender.stun_ticks = move.blockstun if defender.blocking else move.hitstun
        attacker.hit_this_attack = True
        events.append("hit")
def tick(match: MatchState, inputs: tuple[InputFrame, InputFrame]) -> None:
    if match.phase != 1:
        return
    match.events.clear()
    for fighter, frame in zip((match.p1, match.p2), inputs, strict=True):
        fighter.facing = 1 if fighter is match.p1 else -1
        _move(fighter, frame.held)
        _start_attack(fighter, fighter.definition, frame.pressed, match.events)
    p1_definition, p2_definition = match.p1.definition, match.p2.definition
    _resolve(match.p1, match.p2, p1_definition, p2_definition, match.events)
    _resolve(match.p2, match.p1, p2_definition, p1_definition, match.events)
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

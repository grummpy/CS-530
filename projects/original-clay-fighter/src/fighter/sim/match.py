"""Cycle 4 deterministic, integer-only local fight loop.

Per tick order is movement/air physics, wall clamp, symmetric push separation,
position-facing, action starts, simultaneous strike resolution, throws, state
timers, then the single terminal-result classification point.
"""

from __future__ import annotations

from fighter.content.loader import FighterDefinition, load_fighter
from fighter.sim.bits import Action, dir_numpad
from fighter.sim.boxes import Box
from fighter.sim.constants import (
    GRAVITY,
    GROUND_Y,
    LEFT_WALL,
    MAX_FALL,
    RIGHT_WALL,
    RULES,
    WALK_SPEED,
)
from fighter.sim.enums import FighterMode, MatchPhase, ResultReason
from fighter.sim.events import (
    PRESENTATION_EVENT_VERSION,
    PresentationEvent,
    PresentationKind,
    PresentationPayload,
)
from fighter.sim.input_frame import InputFrame
from fighter.sim.moves import HitLevel, MoveDefinition
from fighter.sim.state import FighterState, MatchState, ResultPayload, initial_match

KO_HOLD_TICKS = 30
FINISHER_WINDOW_TICKS = 180


def new_match(
    seed: int = 1, p1_id: str = "graybox_rival", p2_id: str = "graybox_rival", training: int = 0
) -> MatchState:
    return initial_match(seed, p1_id, p2_id, training, load_fighter(p1_id), load_fighter(p2_id))


def reset_round(match: MatchState) -> None:
    score = (match.p1_round_wins, match.p2_round_wins, match.round_number + 1, match.first_to)
    fresh = new_match(match.seed, match.p1.fighter_id, match.p2.fighter_id, match.training)
    (
        match.p1,
        match.p2,
        match.tick,
        match.phase,
        match.events,
        match.round_ticks,
        match.result,
        match.phase_ticks,
    ) = (fresh.p1, fresh.p2, fresh.tick, fresh.phase, [], fresh.round_ticks, None, 0)
    match.presentation_events = []
    match.p1_round_wins, match.p2_round_wins, match.round_number, match.first_to = score


def _push_interval(fighter: FighterState) -> tuple[int, int]:
    box = fighter.definition.push_box
    return fighter.x + box.x, fighter.x + box.x + box.w


def _move_and_jump(fighter: FighterState, held: int, pressed: int) -> None:
    fighter.blocking = False
    locked = {
        FighterMode.ATTACK,
        FighterMode.THROW,
        FighterMode.JUMP_STARTUP,
        FighterMode.HITSTUN,
        FighterMode.BLOCKSTUN,
        FighterMode.KNOCKDOWN_SOFT,
        FighterMode.KNOCKDOWN_HARD,
        FighterMode.WAKEUP,
        FighterMode.KO,
    }
    if fighter.mode in locked:
        return
    if fighter.mode in {FighterMode.ASCENT, FighterMode.DESCENT}:
        direction = (1 if held & Action.RIGHT else 0) - (1 if held & Action.LEFT else 0)
        fighter.x += direction * WALK_SPEED
        return
    if fighter.mode is FighterMode.NEUTRAL and pressed & Action.UP:
        fighter.mode, fighter.state_ticks = FighterMode.JUMP_STARTUP, RULES.jump_startup_ticks
        return
    direction = (1 if held & Action.RIGHT else 0) - (1 if held & Action.LEFT else 0)
    if fighter.airborne:
        fighter.x += direction * WALK_SPEED
        return
    if direction:
        fighter.mode = FighterMode.WALK
        fighter.x += direction * WALK_SPEED
    elif held & Action.DOWN:
        fighter.mode = FighterMode.CROUCH
    else:
        fighter.mode = FighterMode.NEUTRAL


def _clamp_and_separate(p1: FighterState, p2: FighterState) -> None:
    """Clamp first, then split overlap by position, never player iteration."""
    for fighter in (p1, p2):
        left, right = _push_interval(fighter)
        fighter.x += max(LEFT_WALL - left, 0) - max(right - RIGHT_WALL, 0)
    left_fighter, right_fighter = (p1, p2) if p1.x <= p2.x else (p2, p1)
    overlap = _push_interval(left_fighter)[1] - _push_interval(right_fighter)[0]
    if overlap > 0:
        left_limit = left_fighter.x - (LEFT_WALL - left_fighter.definition.push_box.x)
        right_limit = (
            RIGHT_WALL - (right_fighter.definition.push_box.x + right_fighter.definition.push_box.w)
        ) - right_fighter.x
        left_shift = min((overlap + 1) // 2, max(0, left_limit))
        right_shift = min(overlap - left_shift, max(0, right_limit))
        left_shift += overlap - left_shift - right_shift
        left_fighter.x -= left_shift
        right_fighter.x += right_shift


def _facing(p1: FighterState, p2: FighterState) -> None:
    if p1.x != p2.x:
        p1.facing = 1 if p2.x > p1.x else -1
        p2.facing = -p1.facing


def _attack_kind(move_name: str) -> int:
    return {"light": 1, "medium": 2, "heavy": 3}.get(move_name, 4)


def _can_cancel(fighter: FighterState, definition: FighterDefinition, pressed: int) -> str | None:
    if fighter.mode is not FighterMode.ATTACK or not fighter.attack_confirm:
        return None
    source = definition.moves[fighter.attack_move]
    frame = source.total - fighter.attack_ticks + 1
    if (
        not source.cancel_start <= frame <= source.cancel_end
        or fighter.cancel_depth >= RULES.max_cancel_depth
    ):
        return None
    allowed = source.cancel_on_hit if fighter.attack_confirm == "hit" else source.cancel_on_block
    if not allowed:
        return None
    for action, name in (
        (Action.LIGHT, "light"),
        (Action.MEDIUM, "medium"),
        (Action.HEAVY, "heavy"),
        (Action.SPECIAL, definition.profile.special_id),
    ):
        if pressed & action and name in source.cancels and name != source.move_id:
            return name
    return None


def _start_attack(
    fighter: FighterState, definition: FighterDefinition, pressed: int, events: list[str]
) -> None:
    cancel = _can_cancel(fighter, definition, pressed)
    if fighter.mode in {
        FighterMode.JUMP_STARTUP,
        FighterMode.ASCENT,
        FighterMode.DESCENT,
        FighterMode.LANDING,
        FighterMode.HITSTUN,
        FighterMode.BLOCKSTUN,
        FighterMode.KNOCKDOWN_SOFT,
        FighterMode.KNOCKDOWN_HARD,
        FighterMode.WAKEUP,
        FighterMode.KO,
        FighterMode.THROW,
    }:
        return
    if pressed & Action.THROW and fighter.mode not in {FighterMode.ATTACK, FighterMode.THROW}:
        fighter.mode, fighter.attack_move = FighterMode.THROW, "__throw__"
        fighter.attack_ticks, fighter.hit_this_attack, fighter.attack_confirm = (
            RULES.throw_startup + RULES.throw_active + RULES.throw_recovery,
            False,
            "",
        )
        return
    if fighter.mode is FighterMode.ATTACK and cancel is None:
        queued = pressed & int(
            Action.LIGHT | Action.MEDIUM | Action.HEAVY | Action.SPECIAL | Action.THROW
        )
        if queued and fighter.attack_ticks <= 6:
            fighter.buffered_action, fighter.buffer_ticks = queued, 8
        return
    for action, move_name in (
        (Action.LIGHT, "light"),
        (Action.MEDIUM, "medium"),
        (Action.HEAVY, "heavy"),
        (Action.SPECIAL, definition.profile.special_id),
    ):
        if not (pressed & action) or move_name is None:
            continue
        move = definition.moves.get(move_name)
        if move is None:
            return
        if action is Action.SPECIAL and fighter.special_charge < move.meter_cost:
            return
        if action is Action.SPECIAL:
            fighter.special_charge -= move.meter_cost
        fighter.cancel_depth = fighter.cancel_depth + 1 if cancel else 0
        fighter.mode, fighter.attack_kind, fighter.attack_move = (
            FighterMode.ATTACK,
            _attack_kind(move_name),
            move_name,
        )
        fighter.attack_ticks, fighter.hit_this_attack, fighter.attack_confirm = (
            move.total,
            False,
            "",
        )
        return


def _active_hitbox(attacker: FighterState, move: MoveDefinition) -> Box | None:
    frame = move.total - attacker.attack_ticks + 1
    for window in move.hitboxes:
        if window.start <= frame <= window.end:
            return window.box.world(attacker.x, GROUND_Y, attacker.facing)
    return None


def _guarding(defender: FighterState, held: int, level: HitLevel) -> bool:
    if defender.airborne:
        return dir_numpad(held, defender.facing) in {4, 7} and level is not HitLevel.LOW
    direction = dir_numpad(held, defender.facing)
    return direction == 1 if level is HitLevel.LOW else direction in {1, 4}


def _damage(defender: FighterState, amount: int) -> None:
    defender.health = max(0, defender.health - amount)
    defender.special_charge = min(3000, defender.special_charge + amount)


def _present(
    match: MatchState,
    kind: PresentationKind,
    actor: int | None,
    target: int | None,
    fighter: FighterState,
    move: str | None = None,
    strength: int = 0,
    result: ResultReason | None = None,
) -> None:
    """Append an ID-addressable event; this never participates in simulation state."""
    match.presentation_events.append(
        PresentationEvent(
            PRESENTATION_EVENT_VERSION,
            match.next_presentation_event_id,
            match.tick,
            kind,
            actor,
            target,
            (fighter.x, fighter.y),
            PresentationPayload(move, strength, result),
        )
    )
    match.next_presentation_event_id += 1


def _resolve_strike(
    attacker: FighterState,
    defender: FighterState,
    definition: FighterDefinition,
    defender_definition: FighterDefinition,
    defender_input: InputFrame,
    events: list[str],
    match: MatchState,
    actor: int,
    target: int,
) -> None:
    if attacker.mode is not FighterMode.ATTACK or attacker.hit_this_attack:
        return
    move = definition.moves[attacker.attack_move]
    hitbox = _active_hitbox(attacker, move)
    if hitbox is None or not hitbox.intersects(
        defender_definition.hurt_box.world(defender.x, defender.y, defender.facing)
    ):
        return
    guarded = _guarding(defender, defender_input.held, move.hit_level)
    damage = max(1, move.damage * RULES.combo_damage_percent // 100)
    if guarded:
        _damage(defender, max(1, damage // 3))
        defender.mode, defender.stun_ticks, defender.blocking = (
            FighterMode.BLOCKSTUN,
            move.blockstun,
            True,
        )
        attacker.attack_confirm, events[:] = "block", [*events, "block"]
        _present(match, "block", actor, target, defender, move.move_id, damage)
        defender.x += attacker.facing * max(4, attacker.attack_kind * 3)
        match.hitstop_ticks = max(match.hitstop_ticks, 2 + attacker.attack_kind)
    else:
        _damage(defender, damage)
        defender.stun_ticks, defender.combo_count = move.hitstun, defender.combo_count + 1
        if move.launch:
            defender.y, defender.vy, defender.mode = GROUND_Y - 1, -8, FighterMode.ASCENT
        else:
            defender.mode = FighterMode.HITSTUN
        attacker.attack_confirm, events[:] = "hit", [*events, "hit"]
        _present(match, "hit", actor, target, defender, move.move_id, damage)
        defender.x += attacker.facing * (7 + attacker.attack_kind * 5)
        match.hitstop_ticks = max(match.hitstop_ticks, 3 + attacker.attack_kind)
    attacker.hit_this_attack = True


def _throw_active(fighter: FighterState) -> bool:
    frame = (
        RULES.throw_startup + RULES.throw_active + RULES.throw_recovery - fighter.attack_ticks + 1
    )
    return RULES.throw_startup < frame <= RULES.throw_startup + RULES.throw_active


def _resolve_throw(
    attacker: FighterState,
    defender: FighterState,
    defender_input: InputFrame,
    events: list[str],
    match: MatchState,
    actor: int,
    target: int,
) -> None:
    if (
        attacker.mode is not FighterMode.THROW
        or attacker.hit_this_attack
        or not _throw_active(attacker)
    ):
        return
    if defender.airborne or defender.mode in {
        FighterMode.KNOCKDOWN_SOFT,
        FighterMode.KNOCKDOWN_HARD,
        FighterMode.WAKEUP,
        FighterMode.KO,
    }:
        events.append("throw_immune")
    elif abs(attacker.x - defender.x) > RULES.throw_range:
        events.append("throw_whiff")
    elif (
        defender_input.pressed & Action.THROW
        or defender.throw_tech_until >= attacker.throw_tech_until
    ):
        attacker.attack_ticks = defender.attack_ticks = 0
        attacker.mode = defender.mode = FighterMode.NEUTRAL
        events.append("throw_tech")
        _present(match, "throw_tech", actor, target, defender)
    else:
        _damage(defender, RULES.throw_damage)
        defender.mode, defender.state_ticks, defender.combo_count = (
            FighterMode.KNOCKDOWN_SOFT,
            RULES.throw_knockdown_ticks,
            0,
        )
        events.append("throw")
        _present(match, "throw", actor, target, defender, "__throw__", RULES.throw_damage)
    attacker.hit_this_attack = True


def _advance_states(
    fighter: FighterState, events: list[str], match: MatchState, player: int
) -> None:
    if fighter.mode is FighterMode.JUMP_STARTUP:
        fighter.state_ticks -= 1
        if fighter.state_ticks == 0:
            fighter.mode, fighter.vy = FighterMode.ASCENT, -16
    elif fighter.mode in {FighterMode.ASCENT, FighterMode.DESCENT} or fighter.airborne:
        fighter.y += fighter.vy
        fighter.vy = min(MAX_FALL, fighter.vy + GRAVITY)
        fighter.mode = FighterMode.ASCENT if fighter.vy < 0 else FighterMode.DESCENT
        if fighter.y >= GROUND_Y:
            fighter.y, fighter.vy, fighter.mode, fighter.state_ticks = (
                GROUND_Y,
                0,
                FighterMode.LANDING,
                RULES.landing_ticks,
            )
            events.append("land")
            _present(match, "land", player, None, fighter)
    elif fighter.mode in {
        FighterMode.LANDING,
        FighterMode.KNOCKDOWN_SOFT,
        FighterMode.KNOCKDOWN_HARD,
        FighterMode.WAKEUP,
    }:
        fighter.state_ticks -= 1
        if fighter.state_ticks == 0:
            if fighter.mode in {FighterMode.KNOCKDOWN_SOFT, FighterMode.KNOCKDOWN_HARD}:
                fighter.mode, fighter.state_ticks = FighterMode.WAKEUP, RULES.wakeup_ticks
            else:
                fighter.mode = FighterMode.NEUTRAL
    if fighter.attack_ticks:
        fighter.attack_ticks -= 1
        if fighter.attack_ticks == 0 and fighter.mode in {FighterMode.ATTACK, FighterMode.THROW}:
            fighter.mode, fighter.combo_count = FighterMode.NEUTRAL, 0
    if fighter.buffer_ticks:
        fighter.buffer_ticks -= 1
        if fighter.buffer_ticks == 0:
            fighter.buffered_action = 0
    if fighter.stun_ticks:
        fighter.stun_ticks -= 1
        if fighter.stun_ticks == 0 and fighter.mode in {FighterMode.HITSTUN, FighterMode.BLOCKSTUN}:
            fighter.mode, fighter.combo_count = FighterMode.NEUTRAL, 0
    if fighter.armor_ticks:
        fighter.armor_ticks -= 1
        if fighter.armor_ticks == 0:
            events.append("armor_mode_off")


def _classify_terminal(match: MatchState) -> None:
    if match.training or match.result is not None:
        return
    p1, p2 = match.p1, match.p2
    if p1.health == 0 or p2.health == 0:
        reason = ResultReason.DOUBLE_KO if p1.health == p2.health else ResultReason.KO
    elif match.round_ticks == 0:
        reason = ResultReason.TIMEOUT_DRAW if p1.health == p2.health else ResultReason.TIMEOUT_WIN
    else:
        return
    winner = 0 if p1.health == p2.health else 1 if p1.health > p2.health else 2
    if winner == 1:
        match.p1_round_wins += 1
    elif winner == 2:
        match.p2_round_wins += 1
    set_complete = max(match.p1_round_wins, match.p2_round_wins) >= match.first_to
    variant = None
    if reason is ResultReason.KO and winner and set_complete:
        victor, defeated = (p1, p2) if winner == 1 else (p2, p1)
        variant = f"{victor.fighter_id}_vs_{defeated.fighter_id}"
    match.result = ResultPayload(reason, winner, match.tick, p1.health, p2.health, variant)
    match.phase = (
        MatchPhase.KO_HOLD
        if reason in {ResultReason.KO, ResultReason.DOUBLE_KO}
        else MatchPhase.RESULTS
    )
    match.phase_ticks = KO_HOLD_TICKS if match.phase is MatchPhase.KO_HOLD else 0
    p1.mode, p2.mode = (
        FighterMode.KO if p1.health == 0 else p1.mode,
        FighterMode.KO if p2.health == 0 else p2.mode,
    )
    match.events.append(f"result:{reason.name.lower()}")
    if reason in {ResultReason.KO, ResultReason.DOUBLE_KO}:
        ko_target = (
            1 if p1.health == 0 and p2.health else 2 if p2.health == 0 and p1.health else None
        )
        _present(
            match, "ko", winner or None, ko_target, p1 if ko_target == 1 else p2, result=reason
        )
    if match.phase is MatchPhase.RESULTS:
        _present(match, "result", winner or None, None, p1 if winner != 2 else p2, result=reason)


def _advance_terminal(match: MatchState, inputs: tuple[InputFrame, InputFrame]) -> None:
    """Advance presentation-facing terminal phases without mutating result data."""
    if match.phase is MatchPhase.KO_HOLD:
        match.phase_ticks -= 1
        if match.phase_ticks <= 0:
            result = match.result
            assert result is not None
            actor = result.winner or None
            fighter = match.p1 if result.winner != 2 else match.p2
            if result.finisher_variant:
                match.phase, match.phase_ticks = MatchPhase.FINISHER_WINDOW, FINISHER_WINDOW_TICKS
                _present(
                    match,
                    "finisher",
                    actor,
                    None,
                    fighter,
                    move=result.finisher_variant,
                    result=result.reason,
                )
            else:
                match.phase, match.phase_ticks = MatchPhase.RESULTS, 0
                _present(match, "result", actor, None, fighter, result=result.reason)
    elif match.phase is MatchPhase.FINISHER_WINDOW:
        skip = bool((inputs[0].pressed | inputs[1].pressed) & Action.START)
        match.phase_ticks -= 1
        if skip or match.phase_ticks <= 0:
            match.phase, match.phase_ticks = MatchPhase.RESULTS, 0
            result = match.result
            assert result is not None
            fighter = match.p1 if result.winner != 2 else match.p2
            match.events.append("finisher:skip" if skip else "finisher:complete")
            _present(match, "result", result.winner or None, None, fighter, result=result.reason)


def tick(match: MatchState, inputs: tuple[InputFrame, InputFrame]) -> None:
    if match.phase is not MatchPhase.FIGHT:
        match.events.clear()
        match.presentation_events.clear()
        _advance_terminal(match, inputs)
        match.tick += 1
        return
    match.events.clear()
    match.presentation_events.clear()
    if match.fight_start_ticks:
        match.fight_start_ticks -= 1
        match.tick += 1
        return
    if match.hitstop_ticks:
        for fighter, frame in zip((match.p1, match.p2), inputs, strict=True):
            queued = frame.pressed & int(
                Action.LIGHT | Action.MEDIUM | Action.HEAVY | Action.SPECIAL | Action.THROW
            )
            if queued:
                fighter.buffered_action, fighter.buffer_ticks = queued, 10
        match.hitstop_ticks -= 1
        match.tick += 1
        return
    p1_frame, p2_frame = inputs
    buffered_frames = []
    for fighter, frame in ((match.p1, p1_frame), (match.p2, p2_frame)):
        if fighter.buffered_action:
            frame = InputFrame(frame.held, frame.pressed | fighter.buffered_action, frame.released)
            fighter.buffered_action = fighter.buffer_ticks = 0
        buffered_frames.append(frame)
    p1_frame, p2_frame = buffered_frames
    for fighter, frame in ((match.p1, p1_frame), (match.p2, p2_frame)):
        if frame.pressed & Action.THROW:
            fighter.throw_tech_until = match.tick + RULES.throw_startup
    for fighter, frame in ((match.p1, p1_frame), (match.p2, p2_frame)):
        _move_and_jump(fighter, frame.held, frame.pressed)
    _clamp_and_separate(match.p1, match.p2)
    _facing(match.p1, match.p2)
    _start_attack(match.p1, match.p1.definition, p1_frame.pressed, match.events)
    _start_attack(match.p2, match.p2.definition, p2_frame.pressed, match.events)
    _resolve_strike(
        match.p1,
        match.p2,
        match.p1.definition,
        match.p2.definition,
        p2_frame,
        match.events,
        match,
        1,
        2,
    )
    _resolve_strike(
        match.p2,
        match.p1,
        match.p2.definition,
        match.p1.definition,
        p1_frame,
        match.events,
        match,
        2,
        1,
    )
    _resolve_throw(match.p1, match.p2, p2_frame, match.events, match, 1, 2)
    _resolve_throw(match.p2, match.p1, p1_frame, match.events, match, 2, 1)
    for player, fighter in enumerate((match.p1, match.p2), 1):
        _advance_states(fighter, match.events, match, player)
    for fighter in (match.p1, match.p2):
        if fighter.mode is FighterMode.NEUTRAL and fighter.buffered_action:
            queued = fighter.buffered_action
            fighter.buffered_action = fighter.buffer_ticks = 0
            _start_attack(fighter, fighter.definition, queued, match.events)
    if not match.training:
        match.round_ticks = max(0, match.round_ticks - 1)
    _classify_terminal(match)
    match.tick += 1

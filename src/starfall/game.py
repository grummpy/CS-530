"""Deterministic arcade-fighter simulation, independent of Pygame rendering."""

from __future__ import annotations

from dataclasses import dataclass, field

WORLD_WIDTH = 960
WORLD_HEIGHT = 540
GROUND_Y = 445
FIXED_TIMESTEP = 1 / 60


@dataclass(frozen=True)
class FighterInput:
    move: int = 0
    jump: bool = False
    light: bool = False
    heavy: bool = False


@dataclass(frozen=True)
class Attack:
    name: str
    duration: float
    active_start: float
    active_end: float
    damage: int
    reach: float
    height: float
    knockback_x: float
    knockback_y: float


LIGHT = Attack("light", 0.28, 0.08, 0.15, 55, 58, 54, 235, -85)
HEAVY = Attack("heavy", 0.48, 0.17, 0.31, 115, 92, 88, 360, -270)


@dataclass
class Fighter:
    name: str
    x: float
    color: tuple[int, int, int]
    facing: int
    y: float = GROUND_Y
    velocity_x: float = 0
    velocity_y: float = 0
    health: int = 1000
    state: str = "idle"
    state_timer: float = 0
    attack: Attack | None = None
    attack_connected: bool = False
    hitstun: float = 0
    input_buffer: list[tuple[str, float]] = field(default_factory=list)

    width: float = 42
    height: float = 86
    walk_speed: float = 235
    air_speed: float = 180

    @property
    def grounded(self) -> bool:
        return self.y >= GROUND_Y

    @property
    def attack_active(self) -> bool:
        return (
            self.attack is not None
            and self.attack.active_start <= self.state_timer <= self.attack.active_end
        )

    def queue_input(self, controls: FighterInput) -> None:
        for action, pressed in (
            ("jump", controls.jump),
            ("light", controls.light),
            ("heavy", controls.heavy),
        ):
            if pressed:
                self.input_buffer.append((action, 0.14))

    def update(self, dt: float, controls: FighterInput) -> None:
        self._age_input_buffer(dt)
        self.queue_input(controls)
        self.hitstun = max(0, self.hitstun - dt)
        if self.state_timer > 0:
            self.state_timer = max(0, self.state_timer - dt)
            if self.state_timer == 0 and self.state not in {"idle", "walk", "jump"}:
                self.state = "idle" if self.grounded else "jump"
                self.attack = None

        actionable = self.hitstun == 0 and self.attack is None
        if actionable:
            self._start_buffered_action()
        if self.hitstun == 0 and self.attack is None:
            speed = self.walk_speed if self.grounded else self.air_speed
            self.velocity_x = controls.move * speed
            if self.grounded and self.state != "jump":
                self.state = "walk" if controls.move else "idle"

        self.velocity_y += 1_800 * dt
        self.x = min(
            WORLD_WIDTH - self.width / 2,
            max(self.width / 2, self.x + self.velocity_x * dt),
        )
        self.y += self.velocity_y * dt
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.velocity_y = 0
            if self.state == "jump":
                self.state = "idle"

    def receive_hit(self, attack: Attack, attacker_facing: int) -> None:
        self.health = max(0, self.health - attack.damage)
        self.velocity_x = attack.knockback_x * attacker_facing
        self.velocity_y = attack.knockback_y
        self.hitstun = 0.30 if attack is LIGHT else 0.55
        self.state = "hit"
        self.attack = None
        self.state_timer = self.hitstun

    def _age_input_buffer(self, dt: float) -> None:
        self.input_buffer = [
            (action, remaining - dt)
            for action, remaining in self.input_buffer
            if remaining - dt > 0
        ]

    def _start_buffered_action(self) -> None:
        if not self.input_buffer:
            return
        action, _ = self.input_buffer.pop(0)
        if action == "jump" and self.grounded:
            self.velocity_y = -660
            self.state = "jump"
        elif action == "light":
            self._start_attack(LIGHT)
        elif action == "heavy":
            self._start_attack(HEAVY)

    def _start_attack(self, attack: Attack) -> None:
        self.attack = attack
        self.attack_connected = False
        self.state = f"attack_{attack.name}"
        self.state_timer = attack.duration


@dataclass
class GameState:
    """Match controller for two local fighters and first-to-two rounds."""

    fighters: list[Fighter] = field(
        default_factory=lambda: [
            Fighter("Player 1", 270, (78, 186, 255), 1),
            Fighter("Player 2", 690, (255, 94, 130), -1),
        ]
    )
    wins: list[int] = field(default_factory=lambda: [0, 0])
    round_number: int = 1
    round_timer: float = 99
    round_over: bool = False
    match_over: bool = False
    round_end_timer: float = 0

    def step(self, dt: float, player_one: FighterInput, player_two: FighterInput) -> None:
        """Advance the match by a fixed step with edge-triggered attack inputs."""
        if self.match_over:
            return
        dt = min(dt, FIXED_TIMESTEP)
        if self.round_over:
            self.round_end_timer -= dt
            if self.round_end_timer <= 0:
                self._start_next_round()
            return

        self.round_timer = max(0, self.round_timer - dt)
        first, second = self.fighters
        first.update(dt, player_one)
        second.update(dt, player_two)
        self._update_facing()
        self._resolve_attacks(first, second)
        self._resolve_attacks(second, first)
        self._separate_fighters()

        if self.round_timer == 0 or any(fighter.health == 0 for fighter in self.fighters):
            self._finish_round()

    def winner_text(self) -> str:
        if self.match_over:
            winner = self.fighters[0] if self.wins[0] > self.wins[1] else self.fighters[1]
            return f"{winner.name.upper()} WINS THE MATCH"
        if self.round_over:
            if self.fighters[0].health == self.fighters[1].health:
                return "DRAW GAME"
            winner = max(self.fighters, key=lambda fighter: fighter.health)
            return f"{winner.name.upper()} WINS THE ROUND"
        return f"ROUND {self.round_number}"

    def _resolve_attacks(self, attacker: Fighter, defender: Fighter) -> None:
        if (
            attacker.attack is None
            or not attacker.attack_active
            or attacker.attack_connected
            or defender.hitstun > 0
        ):
            return
        horizontal_distance = (defender.x - attacker.x) * attacker.facing
        vertical_distance = abs(defender.y - attacker.y)
        if (
            0 < horizontal_distance <= attacker.attack.reach
            and vertical_distance <= attacker.attack.height
        ):
            defender.receive_hit(attacker.attack, attacker.facing)
            attacker.attack_connected = True

    def _update_facing(self) -> None:
        first, second = self.fighters
        first.facing = 1 if first.x < second.x else -1
        second.facing = -first.facing

    def _separate_fighters(self) -> None:
        first, second = self.fighters
        overlap = (first.width + second.width) / 2 - abs(second.x - first.x)
        if overlap <= 0:
            return
        direction = 1 if second.x >= first.x else -1
        first.x -= overlap / 2 * direction
        second.x += overlap / 2 * direction
        first.x = min(WORLD_WIDTH - first.width / 2, max(first.width / 2, first.x))
        second.x = min(WORLD_WIDTH - second.width / 2, max(second.width / 2, second.x))

    def _finish_round(self) -> None:
        self.round_over = True
        self.round_end_timer = 2.2
        if self.fighters[0].health > self.fighters[1].health:
            self.wins[0] += 1
        elif self.fighters[1].health > self.fighters[0].health:
            self.wins[1] += 1
        self.match_over = max(self.wins) == 2

    def _start_next_round(self) -> None:
        self.round_number += 1
        self.round_timer = 99
        self.round_over = False
        self.fighters = [
            Fighter("Player 1", 270, (78, 186, 255), 1),
            Fighter("Player 2", 690, (255, 94, 130), -1),
        ]

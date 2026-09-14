"""Device-independent semantic input routing; simulation sees only InputFrames."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from fighter.sim.bits import Action
from fighter.sim.input_frame import InputFrame


class SemanticAction(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SPECIAL = "special"
    THROW = "throw"
    CONFIRM = "confirm"
    BACK = "back"
    PAUSE = "pause"
    MENU_UP = "menu_up"
    MENU_DOWN = "menu_down"
    MENU_LEFT = "menu_left"
    MENU_RIGHT = "menu_right"
    OPEN_MOVE_LIST = "open_move_list"
    RESET = "reset"


COMBAT_ACTIONS = frozenset(
    {
        SemanticAction.LEFT,
        SemanticAction.RIGHT,
        SemanticAction.UP,
        SemanticAction.DOWN,
        SemanticAction.LIGHT,
        SemanticAction.MEDIUM,
        SemanticAction.HEAVY,
        SemanticAction.SPECIAL,
        SemanticAction.THROW,
    }
)
SHELL_ACTIONS = frozenset(set(SemanticAction) - set(COMBAT_ACTIONS))
ACTION_BITS = {
    SemanticAction.LEFT: Action.LEFT,
    SemanticAction.RIGHT: Action.RIGHT,
    SemanticAction.UP: Action.UP,
    SemanticAction.DOWN: Action.DOWN,
    SemanticAction.LIGHT: Action.LIGHT,
    SemanticAction.MEDIUM: Action.MEDIUM,
    SemanticAction.HEAVY: Action.HEAVY,
    SemanticAction.SPECIAL: Action.SPECIAL,
    SemanticAction.THROW: Action.THROW,
}
CONTROLLER_DEFAULTS = {
    "hat:left": SemanticAction.LEFT,
    "hat:right": SemanticAction.RIGHT,
    "hat:up": SemanticAction.UP,
    "hat:down": SemanticAction.DOWN,
    "button:0": SemanticAction.LIGHT,
    "button:1": SemanticAction.MEDIUM,
    "button:2": SemanticAction.HEAVY,
    "button:3": SemanticAction.SPECIAL,
    "button:4": SemanticAction.THROW,
    "button:7": SemanticAction.PAUSE,
    "button:9": SemanticAction.CONFIRM,
    "button:8": SemanticAction.BACK,
}


def default_bindings() -> list[dict[str, str]]:
    """Return serializable bindings; key values deliberately use stable pygame key codes."""
    # Familiar keyboard layout: WASD movement with the right hand on J/K/L/I/U.
    p1 = ("97", "100", "119", "115", "106", "107", "108", "105", "117")
    p2 = (
        "1073741904",
        "1073741903",
        "1073741906",
        "1073741905",
        "1073741913",
        "1073741914",
        "1073741915",
        "1073741922",
        "1073741917",
    )
    names = ("left", "right", "up", "down", "light", "medium", "heavy", "special", "throw")
    common = {
        "confirm": "key:13",
        "back": "key:27",
        "pause": "key:112",
        "menu_up": "key:1073741906",
        "menu_down": "key:1073741905",
        "menu_left": "key:1073741904",
        "menu_right": "key:1073741903",
        "open_move_list": "key:9",
        "reset": "key:114",
    }
    return [
        {**{name: f"key:{code}" for name, code in zip(names, p1, strict=True)}, **common},
        {**{name: f"key:{code}" for name, code in zip(names, p2, strict=True)}, **common},
    ]


@dataclass
class Device:
    instance_id: int
    label: str
    player: int | None = None


@dataclass
class DeviceLifecycle:
    """Tracks hot-plug assignment without leaking controller state into the sim."""

    devices: dict[int, Device] = field(default_factory=dict)
    awaiting_reconnect: set[int] = field(default_factory=set)

    def connect(self, instance_id: int, label: str) -> Device:
        device = Device(instance_id, label)
        vacant = next(
            (p for p in sorted(self.awaiting_reconnect) if p not in self.assignments), None
        )
        if vacant is not None:
            device.player = vacant
            self.awaiting_reconnect.remove(vacant)
        self.devices[instance_id] = device
        return device

    @property
    def assignments(self) -> dict[int, int]:
        return {
            device.player: device.instance_id
            for device in self.devices.values()
            if device.player is not None
        }

    def assign(self, instance_id: int, player: int) -> None:
        if player not in (0, 1) or instance_id not in self.devices:
            raise ValueError("invalid player or unavailable controller")
        for device in self.devices.values():
            if device.player == player:
                device.player = None
        self.devices[instance_id].player = player
        self.awaiting_reconnect.discard(player)

    def disconnect(self, instance_id: int) -> int | None:
        device = self.devices.pop(instance_id, None)
        if device is not None and device.player is not None:
            self.awaiting_reconnect.add(device.player)
            return device.player
        return None


@dataclass
class InputRouter:
    bindings: list[dict[str, str]] = field(default_factory=default_bindings)
    lifecycle: DeviceLifecycle = field(default_factory=DeviceLifecycle)
    held: dict[str, set[str]] = field(default_factory=dict)
    previous: list[int] = field(default_factory=lambda: [0, 0])
    previous_shell: set[SemanticAction] = field(default_factory=set)

    def set_binding(self, player: int, action: SemanticAction, token: str) -> None:
        if player not in (0, 1) or action.value not in self.bindings[player]:
            raise ValueError("unknown player or action")
        if not _valid_token(token):
            raise ValueError("invalid binding")
        context = COMBAT_ACTIONS if action in COMBAT_ACTIONS else SHELL_ACTIONS
        for name, existing in self.bindings[player].items():
            if name != action.value and SemanticAction(name) in context and existing == token:
                raise ValueError(f"binding conflicts with {name}")
        self.bindings[player][action.value] = token
        self.clear()

    def event(self, kind: str, token: str, pressed: bool, instance_id: int | None = None) -> None:
        source = "keyboard" if kind == "key" else f"controller:{instance_id}"
        held = self.held.setdefault(source, set())
        if pressed:
            held.add(token)
        else:
            held.discard(token)

    def clear(self) -> None:
        self.held.clear()
        self.previous = [0, 0]
        self.previous_shell.clear()

    def actions_for(self, player: int) -> set[SemanticAction]:
        sources = {"keyboard"}
        controller = self.lifecycle.assignments.get(player)
        if controller is not None:
            sources.add(f"controller:{controller}")
        physical = set().union(*(self.held.get(source, set()) for source in sources))
        actions = {
            SemanticAction(name)
            for name, token in self.bindings[player].items()
            if token in physical
        }
        if controller is not None:
            actions.update(
                action
                for token, action in CONTROLLER_DEFAULTS.items()
                if token in self.held.get(f"controller:{controller}", set())
            )
        return actions

    def frames(self) -> tuple[InputFrame, InputFrame]:
        frames: list[InputFrame] = []
        for player in (0, 1):
            held = 0
            for action in self.actions_for(player) & COMBAT_ACTIONS:
                held |= ACTION_BITS[action]
            frames.append(InputFrame.from_held(self.previous[player], held))
            self.previous[player] = held
        return frames[0], frames[1]

    def shell_edges(self) -> set[SemanticAction]:
        held = set().union(*(self.actions_for(player) & SHELL_ACTIONS for player in (0, 1)))
        edges = held - self.previous_shell
        self.previous_shell = held
        return edges


def _valid_token(token: str) -> bool:
    prefix, separator, value = token.partition(":")
    return (
        prefix in {"key", "button", "hat"}
        and bool(separator)
        and value.isascii()
        and len(value) <= 24
    )

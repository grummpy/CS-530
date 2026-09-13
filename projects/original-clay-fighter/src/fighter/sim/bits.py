"""Action bitfields and facing-relative numpad directions."""
from __future__ import annotations
from enum import IntEnum
class Action(IntEnum):
    LEFT = 1 << 0
    RIGHT = 1 << 1
    UP = 1 << 2
    DOWN = 1 << 3
    LIGHT = 1 << 4
    MEDIUM = 1 << 5
    HEAVY = 1 << 6
    SPECIAL = 1 << 7
    THROW = 1 << 8
    START = 1 << 9
BUTTONS = (Action.LIGHT, Action.MEDIUM, Action.HEAVY, Action.SPECIAL, Action.THROW, Action.START)
def dir_numpad(held: int, facing: int) -> int:
    left = bool(held & Action.LEFT)
    right = bool(held & Action.RIGHT)
    up = bool(held & Action.UP)
    down = bool(held & Action.DOWN)
    if left and right:
        left = right = False
    if up and down:
        up = down = False
    forward = right if facing >= 0 else left
    back = left if facing >= 0 else right
    if up and forward: return 9
    if up and back: return 7
    if down and forward: return 3
    if down and back: return 1
    if up: return 8
    if down: return 2
    if forward: return 6
    if back: return 4
    return 5
def is_back(numpad: int) -> bool:
    return numpad in {1, 4, 7}
def is_down(numpad: int) -> bool:
    return numpad in {1, 2, 3}
def is_forward(numpad: int) -> bool:
    return numpad in {3, 6, 9}
def is_up(numpad: int) -> bool:
    return numpad in {7, 8, 9}

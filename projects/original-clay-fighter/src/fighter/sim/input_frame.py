"""Immutable, per-tick controller state."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class InputFrame:
    held: int = 0
    pressed: int = 0
    released: int = 0

    @classmethod
    def from_held(cls, previous: int, current: int) -> "InputFrame":
        return cls(current, current & ~previous, previous & ~current)

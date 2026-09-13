"""Axis-aligned boxes in integer space."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class Box:
    x: int
    y: int
    w: int
    h: int
    def flipped(self) -> Box:
        return Box(x=-(self.x + self.w), y=self.y, w=self.w, h=self.h)
    def world(self, origin_x: int, origin_y: int, facing: int) -> Box:
        local = self if facing >= 0 else self.flipped()
        return Box(origin_x + local.x, origin_y + local.y, local.w, local.h)
    def intersects(self, other: Box) -> bool:
        return self.x < other.x + other.w and other.x < self.x + self.w and self.y < other.y + other.h and other.y < self.y + self.h
    def to_tuple(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.w, self.h)

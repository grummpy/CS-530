"""Bounded, clay-style presentation effect hooks."""

from __future__ import annotations

from dataclasses import dataclass, field

from fighter.sim.events import PresentationEvent


@dataclass(frozen=True, slots=True)
class ClayEffect:
    kind: str
    position: tuple[int, int]
    ttl: int
    essential: bool


@dataclass(slots=True)
class ClayEffectPool:
    capacity: int = 24
    effects: list[ClayEffect] = field(default_factory=list)

    def trigger(self, event: PresentationEvent, reduced: bool = False) -> None:
        style = {"hit": "impact", "block": "block", "throw": "crumb", "throw_tech": "block",
                 "land": "dust", "ko": "ko", "result": "meter"}.get(event.kind)
        if style is None or (reduced and event.kind in {"land", "result"}):
            return
        effect = ClayEffect(style, event.position, 18 if event.kind == "hit" else 30,
                            event.kind in {"hit", "block", "ko"})
        if len(self.effects) == self.capacity:
            self.effects.pop(0)
        self.effects.append(effect)

    def advance(self) -> None:
        self.effects = [ClayEffect(item.kind, item.position, item.ttl - 1, item.essential)
                        for item in self.effects if item.ttl > 1]

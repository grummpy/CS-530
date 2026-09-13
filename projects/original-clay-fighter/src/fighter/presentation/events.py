"""Exactly-once fan-out of immutable presentation events."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

from fighter.sim.events import PresentationEvent


@dataclass(slots=True)
class PresentationDispatcher:
    _seen: set[int] = field(default_factory=set)

    def dispatch(self, events: Iterable[PresentationEvent], consumer: Callable[[PresentationEvent], None]) -> int:
        delivered = 0
        for event in events:
            if event.event_id in self._seen:
                continue
            self._seen.add(event.event_id)
            consumer(event)
            delivered += 1
        return delivered

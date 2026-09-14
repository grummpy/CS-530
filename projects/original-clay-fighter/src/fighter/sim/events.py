"""Immutable, non-authoritative simulation-to-presentation events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from fighter.sim.enums import ResultReason

PRESENTATION_EVENT_VERSION = 1
PresentationKind = Literal[
    "hit", "block", "throw", "throw_tech", "land", "ko", "finisher", "result"
]


@dataclass(frozen=True, slots=True)
class PresentationPayload:
    """Typed metadata intentionally excluded from authoritative checksums."""

    move: str | None = None
    strength: int = 0
    result: ResultReason | None = None


@dataclass(frozen=True, slots=True)
class PresentationEvent:
    version: int
    event_id: int
    tick: int
    kind: PresentationKind
    actor: int | None
    target: int | None
    position: tuple[int, int]
    payload: PresentationPayload

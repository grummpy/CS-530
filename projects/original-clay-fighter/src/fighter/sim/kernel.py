"""Session facade used by the app and headless replay."""

from __future__ import annotations

from fighter.sim.checksum import checksum_match
from fighter.sim.events import PresentationEvent
from fighter.sim.input_frame import InputFrame
from fighter.sim.match import new_match, reset_round, tick
from fighter.sim.state import MatchState


class SessionKernel:
    def __init__(
        self,
        seed: int = 1,
        p1_id: str = "graybox_rival",
        p2_id: str = "graybox_rival",
        training: int = 0,
    ) -> None:
        if seed < 0:
            raise ValueError("seed must be a non-negative integer")
        self._match = new_match(seed=seed, p1_id=p1_id, p2_id=p2_id, training=training)

    @property
    def match(self) -> MatchState:
        return self._match

    @property
    def seed(self) -> int:
        return self._match.seed

    @property
    def tick_index(self) -> int:
        return self._match.tick

    def tick(self, inputs: tuple[InputFrame, InputFrame] | None = None) -> int:
        pair = inputs if inputs is not None else (InputFrame(), InputFrame())
        tick(self._match, pair)
        return self._match.tick

    def reset(self) -> None:
        reset_round(self._match)

    def snapshot(self) -> dict[str, object]:
        snap = self._match.snapshot()
        snap["tick_index"] = self._match.tick
        return snap

    def checksum(self) -> str:
        return checksum_match(self._match)

    def presentation_events(self) -> tuple[PresentationEvent, ...]:
        """Return this tick's presentation-only events without exposing mutation."""
        return tuple(self._match.presentation_events)

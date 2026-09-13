"""Fixed 60 Hz simulation clock with accumulator and catch-up cap."""
from __future__ import annotations
from fighter import MAX_CATCH_UP_TICKS, TICK_HZ
class FixedStepClock:
    def __init__(self, tick_hz: int = TICK_HZ, max_catch_up: int = MAX_CATCH_UP_TICKS) -> None:
        if tick_hz <= 0:
            raise ValueError("tick_hz must be positive")
        if max_catch_up <= 0:
            raise ValueError("max_catch_up must be positive")
        self.tick_hz = tick_hz
        self.tick_ms = 1000 // tick_hz
        self.max_catch_up = max_catch_up
        self._accumulator_ms = 0
        self.sim_tick = 0
    def reset(self) -> None:
        self._accumulator_ms = 0
        self.sim_tick = 0
    def consume_wall_ms(self, elapsed_ms: int) -> int:
        if elapsed_ms < 0:
            elapsed_ms = 0
        self._accumulator_ms += elapsed_ms
        ticks = 0
        while self._accumulator_ms >= self.tick_ms and ticks < self.max_catch_up:
            self._accumulator_ms -= self.tick_ms
            ticks += 1
        if ticks == self.max_catch_up:
            self._accumulator_ms = 0
        return ticks
    def advance(self, ticks: int) -> int:
        self.sim_tick += ticks
        return self.sim_tick

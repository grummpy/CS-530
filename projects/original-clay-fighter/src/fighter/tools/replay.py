"""Headless replay helper."""

from __future__ import annotations

from fighter.sim.checksum import checksum_match
from fighter.sim.input_frame import InputFrame
from fighter.sim.kernel import SessionKernel
from fighter.sim.match import new_match, tick


def run_replay(ticks: int, seed: int = 1) -> tuple[int, str]:
    kernel = SessionKernel(seed=seed)
    for _ in range(ticks):
        kernel.tick()
    return kernel.tick_index, kernel.checksum()


def run_input_replay(
    frames: list[tuple[InputFrame, InputFrame]], seed: int = 1, hash_every: int = 15
) -> list[tuple[int, str]]:
    match = new_match(seed=seed)
    hashes: list[tuple[int, str]] = []
    for frame in frames:
        tick(match, frame)
        if match.tick % hash_every == 0:
            hashes.append((match.tick, checksum_match(match)))
    if not hashes or hashes[-1][0] != match.tick:
        hashes.append((match.tick, checksum_match(match)))
    return hashes


def held_stream(p1: list[int], p2: list[int] | None = None) -> list[tuple[InputFrame, InputFrame]]:
    other = p2 if p2 is not None else [0] * len(p1)
    if len(other) != len(p1):
        raise ValueError("p1 and p2 streams must be the same length")
    frames: list[tuple[InputFrame, InputFrame]] = []
    prev1 = 0
    prev2 = 0
    for h1, h2 in zip(p1, other, strict=True):
        frames.append((InputFrame.from_held(prev1, h1), InputFrame.from_held(prev2, h2)))
        prev1, prev2 = h1, h2
    return frames

"""Integer LCG. Authoritative random state is a single uint32."""

from __future__ import annotations


def advance(state: int) -> int:
    return (1664525 * (state & 0xFFFFFFFF) + 1013904223) & 0xFFFFFFFF


def roll(state: int, modulo: int) -> tuple[int, int]:
    nxt = advance(state)
    if modulo <= 0:
        return nxt, 0
    return nxt, nxt % modulo

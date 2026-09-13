"""Deterministic no-window smoke checks for the command-line launcher."""

from fighter.tools.replay import run_replay


def run_sample_matrix() -> dict[str, str]:
    """Return stable checksums for a small selection of seeded matches."""
    return {f"seed_{seed}": run_replay(180, seed)[1] for seed in (1, 7, 42)}

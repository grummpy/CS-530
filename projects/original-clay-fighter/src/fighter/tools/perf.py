"""Small deterministic simulation throughput report."""

from time import perf_counter

from fighter.tools.replay import run_replay


def report(ticks: int = 6_000) -> dict[str, int | float]:
    """Measure headless simulation throughput without claiming render performance."""
    started = perf_counter()
    run_replay(ticks, 1)
    elapsed = perf_counter() - started
    return {
        "ticks": ticks,
        "seconds": round(elapsed, 6),
        "ticks_per_second": round(ticks / elapsed, 2) if elapsed else 0.0,
    }

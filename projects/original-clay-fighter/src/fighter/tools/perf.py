"""Raw, machine-readable Cycle 8 measurements (not target-floor certification)."""

import csv
import json
import platform
import resource
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

from fighter.tools.replay import run_replay


def report(ticks: int = 6_000) -> dict[str, Any]:
    """Measure headless simulation throughput without claiming render performance."""
    started = perf_counter()
    run_replay(ticks, 1)
    elapsed = perf_counter() - started
    return {
        "ticks": ticks,
        "seconds": round(elapsed, 6),
        "ticks_per_second": round(ticks / elapsed, 2) if elapsed else 0.0,
    }


def raw_report(ticks: int = 6_000) -> dict[str, Any]:
    """Capture raw timing/RSS/build metadata without claiming render measurements."""
    sample = report(ticks)
    sample.update(
        {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
            "cache_bytes": 0,
            "measurement": "headless simulation only",
        }
    )
    return sample


def write_raw_report(json_path: Path, csv_path: Path, ticks: int = 6_000) -> dict[str, Any]:
    """Write one JSON and CSV sample to caller-selected persistent paths."""
    sample = raw_report(ticks)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(sample, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(sample))
        writer.writeheader()
        writer.writerow(sample)
    return sample

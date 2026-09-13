# Cycle 8 Finisher Lifecycle and Performance Report

## Delivered

- The simulation now owns the deterministic `FIGHT -> KO_HOLD ->
  FINISHER_WINDOW -> RESULTS` terminal lifecycle. Results are immutable,
  including the deterministic selected winner-versus-loser variant. Timeout
  bypasses the finisher and draw/KO retains its declared result.
- `START` from either player deterministically skips the finisher window to
  results. Reset creates a fresh round and presentation IDs remain monotonic.
- Presentation validates a selected 30-frame variant before playback,
  incrementally decodes/scales one frame per simulation update, uses a
  byte-accounted LRU transformed-frame cache capped at 48 MiB, and releases
  match-owned media on teardown.
- Missing, unreadable, decode, transform, or over-budget media emits one
  diagnostic and uses the same readable result-card fallback. It never changes
  simulation-owned results.
- `fighter.tools.perf.write_raw_report` produces persistent JSON and CSV raw
  samples with timing, RSS, cache, Python, platform, and measurement scope.

## Validation actually performed

On 2026-09-13 with `.venv/bin/python` (Python 3.12.14):

```text
.venv/bin/python -m pytest                 49 passed in 0.11s
.venv/bin/python -m ruff check src tests   All checks passed
.venv/bin/python -m mypy src/fighter       Success: no issues found in 37 source files
```

The test suite covers KO/double-KO lifecycle timing, skip and reset semantics,
timeout bypass, all 12 committed variants with 30 frames each, malformed media,
decode failure, one-time fallback diagnostics, byte-bounded LRU eviction,
ten teardown cycles, replay determinism, and JSON/CSV report output.

`CYCLE_8_RAW_MEASUREMENTS_2026-09-13.{json,csv}` are raw headless simulation
measurements, not rendered target-floor performance certification.

## Target-floor gate

The approved planning baseline is Windows 10/11 x64 with the stated
i5-8250U/Ryzen 3 3200U integrated-graphics floor. This validation host was
macOS arm64, so the 30 cold/warm startup, selection/load, KO/skip/rematch,
render frame-time, cache peak, and RSS target-floor gate remains **not
certified**. No Cycle 9 packaging or art work was performed.

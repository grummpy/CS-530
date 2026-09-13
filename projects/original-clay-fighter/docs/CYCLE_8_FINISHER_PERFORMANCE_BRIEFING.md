# Cycle 8 Finisher Lifecycle and Performance Briefing

**Status:** Approval required. This cycle covers lifecycle, media loading,
fallback, cache ownership, and measurement only.

## Decision requested

Approve a target-floor performance pass for existing finisher media. Proposed
planning floor: Windows 10/11 x64, Intel i5-8250U or Ryzen 3 3200U, 8 GB RAM,
UHD 620/Vega 3-class integrated graphics, and 1280x720 at 60 Hz. These values
must be confirmed before implementation.

## Audit

Twelve directed finisher variants (360 PNG frames, 30 per variant at 640x360)
exist, but current results bypass playback. There is no simulation-owned
`KO_HOLD`/`FINISHER_WINDOW`, selected-media preload, skip lifecycle, media
failure fallback, cache budget, or rendered performance evidence. Retaining all
30 display-scaled frames would require roughly 105 MiB; source frames require
about 26 MiB.

## Required contract

`FIGHT -> KO_HOLD -> FINISHER_WINDOW -> RESULTS -> RESET/REMATCH`.

Simulation owns immutable result data and lifecycle timing. Presentation
receives one finisher event, incrementally preloads selected source frames,
uses a byte-accounted rolling transformed-frame window, and tears match-owned
media down on reset/rematch. Missing/corrupt/unreadable media produces one
diagnostic and a deterministic readable result-card fallback without changing
the result.

## WBS and gate evidence

| WBS | Deliverable | Exit evidence |
|---|---|---|
| 8.1 | Lifecycle/result/skip state | KO, draw, timeout, reset, rematch, replay tests. |
| 8.2 | Variant manifest validation/resolver | All 12 variants plus malformed/missing media tests. |
| 8.3 | Incremental preload/readiness flow | Trace proving no decode/scale on KO render path. |
| 8.4 | Byte-accounted rolling cache/teardown | Cap, eviction, 10-rematch leak tests. |
| 8.5 | Deterministic fallback card/diagnostics | Load/decode/transform failure injection tests. |
| 8.6 | Raw measurement harness | JSON/CSV timings, RSS, cache bytes, hardware/build metadata. |
| 8.7 | Target-floor validation | 30 cold/warm startup, load, KO/skip/rematch repetitions. |

## Proposed P95 budgets

| Metric | Target | Hard failure |
|---|---:|---:|
| Gameplay/KO frame time | <=16.7 ms | P99 >33.3 ms |
| Selection to `FIGHT` | <=2.0 s | >3.0 s |
| KO to first finisher/fallback frame | <=100 ms | >250 ms |
| Skip to stable results | <=100 ms | >250 ms |
| Finisher cache peak | <=48 MiB | >64 MiB |
| Process RSS peak | <=350 MiB | >450 MiB |
| Ten-rematch retention | within 10 MiB | monotonic growth |

Approve only after confirming target hardware and these budgets. Cycle 8 does
not authorize packaging or character-art work.

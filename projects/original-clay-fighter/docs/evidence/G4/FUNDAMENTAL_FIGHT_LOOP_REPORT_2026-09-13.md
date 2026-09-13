# Cycle 4 fundamental fight-loop report

**Date:** 2026-09-13  
**Validated tree base:** `f8c61e276f5634f55512882a15b252ab452fd16a`  
**Platform:** macOS; Python 3.12.14; pygame-ce 2.5.8 / SDL 2.32.10.

## Delivered contracts

`sim/match.py` resolves each tick in this fixed order: intended movement and
air physics, wall clamp, symmetric push separation, position-based facing,
actions, simultaneous strikes, throws, timers, then one terminal
classification. `sim/constants.py` is the versioned `cycle4.v1` owner of
global integer rules. Fighter state has named jump, air, landing, throw,
stun, knockdown, wake-up, and KO modes. `ResultPayload` is immutable and is
the only result source consumed by the presentation shell.

Back blocks mids/highs; down-back blocks lows; airborne back blocks non-low
strikes. Throws are separate from hitboxes, miss out of range, ignore
airborne/downed targets, and tech on the buffered throw window. The declared
graybox cancel graph is light → medium → heavy, confirmation-gated, and
depth-limited. The content loader validates optional cancel windows/targets
and rejects self-loops, cycles, and missing targets.

## Acceptance evidence

| Briefing criteria | Evidence |
|---|---|
| C4-AC-01 | `test_identical_input_replay_has_same_digest_at_30_60_and_144_hz` asserts equal tick, checksum, and result across schedules. |
| C4-AC-02–03 | Push/wall/facing and jump/landing state assertions in `tests/test_sim.py`. |
| C4-AC-04 | Parameterized high/mid/low back, down-back, and front guard matrix. |
| C4-AC-05 | Success, range miss, tech, and knockdown result assertions. |
| C4-AC-06–07 | Knockdown state and confirmed-cancel regression assertions; loader rejects malformed cancel graphs. |
| C4-AC-08 | Double KO, timeout win, training exclusion, immutable result assertions. |
| C4-AC-09–10 | Existing unknown-fighter/fallback regressions; scoped typing, lint, headless, smoke, whitespace checks below. |

## Validation results

Both committed Python 3.12 virtual environments were used:

```text
.venv/bin/ruff check src tests                 PASS
.venv/bin/pytest                              PASS (20 passed)
.release-venv/bin/ruff check src tests         PASS
.release-venv/bin/pytest                      PASS (20 passed)
.release-venv/bin/mypy src/fighter/sim src/fighter/content
                                                PASS (15 source files)
.release-venv/bin/python -m fighter --headless --ticks 180 --dump-hash
                                                PASS bad005e9e8277fe57c9ccf44eaa11609e7275c05d9fc5058c55e70a818af4e8b
.release-venv/bin/python -m fighter --smoke   PASS
git diff --check                              PASS
```

Smoke digests: seed 1
`bad005e9e8277fe57c9ccf44eaa11609e7275c05d9fc5058c55e70a818af4e8b`; seed 7
`98878b3b92fcc2964b679a2543cb4f082a71d83f49b2ff7558a0c56067b5536f`; seed 42
`01e4d37e33cc7971c402f0829e7a41ff40fdd3ab31c9105d46dfc9c9f1d6815c`.

Full `mypy` was also run in both environments: it retains the same 39
pre-existing diagnostics in `presentation/audio.py` and
`presentation/app_loop.py` caused by deliberately untyped pygame objects.
The touched simulation/content modules are clean. The simulation imports no
renderer, wall-clock, audio, or file I/O and presentation only consumes its
snapshot/result payload.

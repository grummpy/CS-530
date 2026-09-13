# Cycle 7 Audio and Presentation Evidence

**Scope:** Approved Cycle 7 only. No packaging, finisher-performance, or art work was
performed.

## Delivered contracts

- Version 1 frozen presentation events carry monotonic IDs, simulation tick, kind,
  actor/target, position, and typed move/strength/result payload. They are deliberately
  absent from `MatchState.snapshot()`, preserving authoritative checksum inputs.
- ID-only `PresentationDispatcher` provides exactly-once audio/VFX fan-out through
  pause/re-render/replay.
- `MixerAudioService` centralizes bounded category gains/mutes, cache/channel limits,
  deterministic music selection, shutdown, and persistent diagnosable safe mode.
- Settings schema v2 migrates v0/v1 and persists Master/Music/SFX/Voice/UI values/mutes.
- Bounded `ClayEffectPool` retains impact/block/KO signals under reduced effects.
- Approved stages have tint/HUD-safe-zone profiles and result labels route to KO,
  double-KO, or timeout presentation labels without loading finisher media.

## Validation

Executed with the project Python 3.12 environment:

```console
.venv/bin/python -m pytest
.venv/bin/python -m ruff check src tests
.venv/bin/python -m mypy src
```

Results: **41 passed**, Ruff passed, and strict Mypy passed. Headless replay and smoke
commands also exited successfully. The Cycle 7 suite exercises ordering/same-tick
result/reset/checksum invariance, duplicate dispatch, reduced effects, audio
init/asset/channel safe mode, and settings migration/bounds. No listening claim is made
because no original one-shot assets are supplied.

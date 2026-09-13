# Cycle 1 Baseline Evidence

**Date:** 2026-09-13  
**Scope:** First-build audit, documentation reconciliation, initial release
planning, and prioritization. No gameplay, character-art, or build-system
implementation changes were made in Cycle 1.

## Frozen source baseline

The repository contains a Python/Pygame-ce desktop prototype with:

| Item | Observed baseline |
|---|---:|
| Selectable runtime fighters | 4 |
| Tracked fighter profiles | 11 |
| Playable arena backgrounds | 3 |
| Tracked stage definitions | 6 |
| Blender character masters | 4 |
| Runtime character PNG frames | 122 |
| Finisher sequences | 12 |
| Finisher PNG frames | 360 |
| Finisher MP4 previews | 12 |
| Runtime WAV tracks | 5 |
| Current simulation tests | 4 |

The baseline is a prototype. It is not evidence of a packaged commercial
release, controller compatibility, target-hardware performance, or completed
fighter-specific combat integration.

## Reconciliation completed

- Corrected the runtime-audio record from IMA-ADPCM to 48 kHz stereo signed-16-bit PCM WAV.
- Corrected asset availability records: committed Blender masters, frame
  libraries, finisher PNGs/previews, stages, and music are present.
- Recorded the mismatch between tracked profiles/stage definitions and current
  runtime selectable content as an open Cycle 2 design/content requirement.
- Linked Cycle 1 evidence and requirement status through the traceability
  matrix and updated the project status/risk records.

## Provisional delivery baseline

These are planning values, not final release commitments:

| Decision | Provisional value | Cycle 2 decision required |
|---|---|---|
| First platform | Windows 10/11 x64 desktop | Confirm operating-system version and storefront. |
| Presentation target | 1280x720 baseline, 60 FPS | Confirm resolution options and minimum hardware. |
| Minimum performance measure | 16.7 ms frame budget at 60 FPS | Confirm the reference low-spec PC and 95th-percentile transition budgets. |
| Release authority | Project owner | Confirm approver and external-beta/release decision process. |

## Validation status

`python3 -m pytest -q` could not run because this shell has Python 3.11 with
no installed project test dependency. The project requires Python 3.12+ and no
project virtual environment is present in this workspace. This is recorded as
an open reproducibility gap; no previous test result is reasserted as newly
verified.

## Prioritized Cycle 2 input

1. Approve the functional and nonfunctional requirements baseline.
2. Confirm the provisional Windows/minimum-hardware/release-authority values.
3. Approve interface contracts for fixed-step simulation, input, settings,
   audio events, finisher resources, and packaging.
4. Do not implement Cycle 2 until its briefing is approved.

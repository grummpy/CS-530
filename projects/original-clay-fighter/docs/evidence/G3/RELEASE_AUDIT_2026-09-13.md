# G3 release audit — 2026-09-13

## PAPM checkpoint

**Mission:** deliver a local Python/Pygame-ce fighting-game increment that
launches, loads its committed media, reaches a match, accepts its documented
keyboard controls, plays compatible music, and exits cleanly.

**Primary user:** a local desktop player selecting one of four clay fighters
for a short local or CPU match.

**Acceptance evidence:** static checks, deterministic simulation tests,
Pygame-ce asset load, soundtrack load, and a scripted title-to-match smoke.

## Specialist reconciliation

| Owner | Review lane | Reconciled result |
| --- | --- | --- |
| Jarvis | Runtime, CLI, asset/audio load | Converted unsupported IMA ADPCM music to 48 kHz stereo signed-16-bit PCM. Added missing CLI diagnostic modules and guarded mixer shutdown. |
| Leonardo | Art, assets, renderer | Confirmed all referenced sprite frames, three stage images, and 12 finisher sets load. Added P2 HUD portrait and state-appropriate walk/crouch/block clip selection. |
| Super | Controls, gameplay, match flow | Corrected stale special-meter test, improved CPU spacing/guard behavior, added a result fallback for missing finisher frames, and retained 99-second/block/special coverage. |

## Verification performed

- Created an isolated Python 3.12 virtual environment and installed
  `pygame-ce==2.5.8` plus the project development dependencies.
- `ruff check src tests` passed.
- `pytest` passed: 4 tests.
- `python -m fighter --headless --ticks 180 --dump-hash` completed.
- `--smoke`, `--perf`, and `--export-frames` completed.
- SDL dummy Pygame-ce smoke loaded four portraits, all clip manifests, all
  three stages, 360 finisher frames, and five PCM soundtracks.
- Scripted title → selection → match → clean exit smoke completed under SDL
  dummy video and audio.

## Residual release risks

- A real monitor/audio-device playtest and a packaged-build test have not been
  captured in this repository.
- The finisher frame sequence is decoded at match end and can briefly hitch on
  lower-spec systems.
- Menu navigation and match input are keyboard/mouse only; controller support,
  pause/settings, one-shot combat audio, and configurable bindings remain
  backlog items.
- The authoritative match loop uses a small generic move model; authored
  fighter YAML and detailed hitbox data are not yet individual gameplay tuning.

# G3 UI and HUD system report

## Delivered behavior

- Four-fighter title screen with hover attack-pose animation and slogan text.
- Clickable start, fighter, arena, CPU-toggle, and fight controls.
- Three selectable clay arenas: roadside truck stop, executive lawn, and
  electric assembly hall.
- Local two-player mode and a seeded randomized CPU opponent mode.
- 99-second timer, health bars, block shield feedback, and damage-charged
  special meters.
- Existing clay-splat finisher playback after KO or time expiry.

## Verification

`PYTHONPATH=src python3 -m compileall -q src` completed successfully.

An authoritative simulation check verified the 5,940-tick round duration,
block activation, one-third blocked damage, damage-to-special-meter charging,
and a timer-expiry transition to the finisher phase. `git diff --check` also
completed without whitespace errors.

The automated environment does not provide Pygame, so a rendered window and
mouse-click smoke test requires a local desktop run after dependency setup.

# Best-of-three, CPU, and finisher audit

Date: 2026-09-13

Jarvis, Super, and Leonardo independently audited the match flow, simulation,
input handling, and visual assets. Their release-blocking findings were fixed:

- The match now records round number and round wins and requires two wins.
- Finishers run after the deciding KO and all other rounds reach a navigable
  next-round result.
- Easy, Medium, and Hard deterministic CPU controllers use the normal input seam.
- Finisher frames use the approved character sprites and arena paintings instead
  of geometric puppets.
- Thirty-frame finishers play once at their authored 10 FPS cadence.
- Attack clips begin at their own local animation time and contain startup,
  impact, and recovery poses.
- Fighter pivots use the actual 512-pixel foot baseline.
- Short keyboard taps survive until the next simulation tick.
- Controller D-pad neutral and direction changes release the prior direction.
- Finisher display scaling is cached per displayed frame.

Verification: Ruff passed, 54 Pytest tests passed, all 12 finishers decoded all
360 frames, and the real SDL/Pygame title-to-selection-to-CPU-match flow passed.

## Follow-up gameplay correction — 2026-09-14

- Removed the victory pose that had been included in the repeating idle clip.
- Added a 90-tick READY/FIGHT lock so neither fighter drifts before play begins.
- Added impact freeze, knockback, and a ten-tick attack input buffer, including
  inputs pressed during impact freeze.
- Rebuilt Mr. President versus Rhinestone Angel around the detailed handset,
  jet approach, falling payloads, layered clay fireball, crater, irregular clay
  splatter, and recognizable wing, guitar, boot, and hair debris.
- Removed the large rectangular end banner from that sequence.

## Control, corner, and finisher correction — 2026-09-14

- Player 1 now uses the arrow keys; Z/X/C attack, V activates the special, and B
  throws. Settings version 4 migrates existing launcher installations.
- Wall correction now continues during impact freeze, keeping both hurt boxes
  inside the arena and follow-up attacks in range at either corner.
- Automated corner tests confirm damage connects at the left and right walls.
- Removed the remaining rectangular ending panel from every finisher family and
  visually reviewed a contact sheet containing all 12 final frames.

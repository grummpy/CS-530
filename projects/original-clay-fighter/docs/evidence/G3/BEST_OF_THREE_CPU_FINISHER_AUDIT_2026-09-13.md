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

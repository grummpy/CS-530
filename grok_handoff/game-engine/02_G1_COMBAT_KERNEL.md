# G1: Deterministic Combat Kernel Prompt

```text
Implement G1 only after G0 passes. Build a two-player colored-rectangle combat proof at 1280x720 presentation, using a 60 Hz fixed simulation with an accumulator and a maximum catch-up cap. The simulation must be runnable headlessly.

Create typed, serializable state for MatchState, FighterState, InputFrame, MoveDefinition, Box, GameEvent, and canonical checksum snapshots. Authoritative coordinates, velocity, timers, meter, health, and random state must use integers/fixed point; combat may not depend on render dt, Pygame events, sets/dicts with unspecified iteration, audio, particles, or camera smoothing.

Map player actions to arcade-style actions: LEFT, RIGHT, UP, DOWN, LIGHT, MEDIUM, HEAVY, SPECIAL, THROW, START. Keyboard defaults: P1 A/D/W/S + F/G/H/R/T; P2 arrows + J/K/L/U/I. Support D-pad and analog-stick digitalization with configurable dead zone. Maintain held, pressed, released bits and a 15-tick facing-relative direction buffer. Add simple motion-command parsing.

Implement match and fighter state machines: round intro, neutral, walk, crouch, jump, dash, attack, block, hitstun, blockstun, knockdown, KO, and finisher window. Implement pushboxes, hurtboxes, hitboxes, attack startup/active/recovery, hitstop, damage, block, launch, round reset, and explicit same-tick trade rules. Collision resolution is ordered by attacker slot, move instance, hitbox index, defender slot.

Add debug controls: pause, single simulation tick, slow motion, reset, input history, state/frame labels, and box overlays. Write golden replay and determinism tests for movement, command recognition, hit, block, trade, knockdown, and reset. The same replay must produce identical periodic SHA-256 canonical state hashes in repeated headless runs. Record G1 evidence and stop.
```

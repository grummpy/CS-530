# Cycle 4 Fundamental Fight-Loop Audit

**Date:** 2026-09-13  
**Status:** Approval required; no Cycle 4 implementation is authorized by this document.  
**Decision:** Approve the bounded Cycle 4 rules and verification plan in
[`CYCLE_4_FUNDAMENTAL_FIGHT_LOOP_BRIEFING.md`](CYCLE_4_FUNDAMENTAL_FIGHT_LOOP_BRIEFING.md),
or return it for revision.

## Scope and exclusions

Cycle 4 is limited to authoritative, fixed-tick rules for movement, collision
push, facing, aerial state; directional defense; throws and their counterplay;
knockdown and wake-up; cancels and combos; round timeout/draw; and results
flow. It may add only the input actions, typed content fields, presentation
events, and regression tests necessary for those rules. No work outside this
listed scope is authorized.

## Evidence reviewed

| Source | Verified position | Cycle 4 implication |
|---|---|---|
| `COMMERCIAL_READINESS_AUDIT.md` | Cycle 4 requires state, frame-data, hitbox, trade, guard, throw, and results regression evidence. | This is the required exit-evidence set. |
| `CYCLE_2_REQUIREMENTS_BRIEFING.md` | Simulation must remain 60 Hz, deterministic, integer-only, and isolated from presentation; presentation events must not mutate it. | All new state, input edges, resolution order, and snapshots must obey this boundary. |
| `evidence/G3/CONTENT_AUTHORITATIVE_REPORT_2026-09-13.md` | Four selected fighters compile to immutable typed definitions; authored timing, hitboxes, damage, stun, and special values are live. Nine tests, lint, headless hash, and smoke passed; presentation-layer mypy remains a known limitation. | Extend validated schemas rather than reintroducing combat constants; retain current content rejection behavior. |
| Cycle 3 fixed-step implementation and tests | Windowed execution consumes elapsed time through a capped fixed-step accumulator; its current tests cover 30/60/120 Hz tick count, not replay-checksum equivalence at all required schedules. | Add 30/60/144 Hz *identical-input checksum* evidence before approval. |
| Current match loop | Fighters have one horizontal coordinate, fixed player-slot facing, walk, down-held block, generic hurt box, attack/stun timers, simultaneous hit resolution, a single phase transition at KO/expiry, and presentation-selected finishers. | The existing behavior is insufficient for every Cycle 4 rule area and must not be represented as a complete fight loop. |
| `evidence/G3/FINISHER_SYSTEM_REPORT.md` and `UI_HUD_SYSTEM_REPORT.md` | Results presentation currently selects a finisher after either KO or expiry; the HUD displays a 99-second clock. | Cycle 4 must authoritatively determine KO, timeout winner, draw, and results payload before presentation; finisher playback remains later-cycle presentation work. |

## Current-gap disposition

| Area | Current observed behavior | Gap to close |
|---|---|---|
| Movement, push, facing, aerial | Walk clamps independently to walls; facing is assigned by player slot; no overlap separation, jump, landing, or airborne state exists. | Position-derived facing; deterministic pushbox separation; explicit grounded/jump/air/landing state and boundaries. |
| Directional defense | Holding Down blocks all hittable attacks, regardless of attack direction/height or opponent position. | Back-relative standing/crouching/air guard rules, guardable hit levels, cross-up behavior, and guard failure outcomes. |
| Throws/counterplay | `MoveDefinition` has throw metadata, but live input never starts throws and resolver treats all attacks as ordinary hits. | Throw range/startup/tech window, throw immunity and throw-invulnerability rules, and deterministic success/tech/failure events. |
| Knockdown/wake-up | Damage only applies stun; knockback and launch fields are not consumed. | Knockdown state, forced movement/landing, wake-up timing, controllable/locked states, and defined invulnerability policy. |
| Cancels/combos | Move cancel metadata and meter fields exist but are not used; one-hit-per-attack prevents only repeat hits from that attack. | Hit/block-confirm windows, permitted transitions, combo counter/reset rules, scaling policy, and prevention of invalid self/loop cancels. |
| Round/results | Any zero health or timer expiry enters phase `2`, always emits `ko`, and presentation picks higher health (P1 on equal health). | Enum-backed round/result states; simultaneous KO, timeout winner, true draw, result reason/payload, rematch/reset contract, and one terminal event. |

## Audit conclusion

Cycle 3 has established the necessary deterministic/content-authority
foundation, but it has not delivered the fundamental fighting rules. Authorize
Cycle 4 only against the briefing's contracts, measurable acceptance criteria,
and stop conditions. A passing implementation must demonstrate deterministic
outcomes and reject invalid content; a playable-looking result screen alone is
not acceptable evidence.

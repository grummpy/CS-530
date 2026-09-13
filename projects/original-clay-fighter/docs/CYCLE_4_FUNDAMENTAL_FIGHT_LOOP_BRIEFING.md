# Cycle 4 Fundamental Fight-Loop Briefing

**Status:** Approval required. Implementation begins only after the approval
gate below passes.  
**Prerequisite:** Cycle 3 fixed-step/content-authority work and its evidence.  
**Scope:** The authoritative local fight loop only; all timing below is in
integer simulation ticks at 60 Hz.

## Decision requested

Approve the exact Cycle 4 objectives, rule contracts, acceptance criteria,
dependencies, safety/error handling, WBS, risks, and validation plan. This
approval authorizes a bounded implementation of the fundamental fight loop; it
does not authorize work outside the scope stated above.

## Objectives and required rule contracts

| ID | Objective | Required authoritative behavior |
|---|---|---|
| C4-OBJ-01 | Movement, push, facing, aerial state | Resolve intended horizontal movement, walls, then push separation in a fixed documented order. Fighters cannot overlap, leave stage bounds, or gain side advantage from update order. Facing follows relative positions except during an explicitly locked action. Jump startup, ascent, descent, landing, and grounded recovery are enum-backed states with integer velocity/position and a defined landing transition. |
| C4-OBJ-02 | Directional defense | Resolve guard from direction relative to the opponent: back guards standing mids/highs, down-back guards lows, and the documented air-guard rule applies only while airborne. Front/down-only holds do not guard. Unblockable/throw attacks bypass guard only when their typed rule says so. |
| C4-OBJ-03 | Throws and counterplay | Add a typed throw action and resolver separate from strike hitboxes. A throw has range, startup, active, recovery, damage, and resulting state. Define and test tech input/window, throw immunity, airborne and knockdown exclusions, and the result of whiff, tech, and success. |
| C4-OBJ-04 | Knockdown and wake-up | Consume typed launch/knockback values. Define soft/hard knockdown, airborne hit/landing, wake-up duration, controllable state, and any wake-up invulnerability in data. Knocked-down fighters neither block, attack, move, nor accept throws unless their state explicitly permits it. |
| C4-OBJ-05 | Cancels and combos | Consume typed cancel metadata only in explicit confirm windows. Define legal source/target moves, hit versus block permissions, meter cost, chain-depth limit, combo counter/reset, damage scaling (or an approved explicit no-scaling policy), and launch/ground state continuity. Illegal, mistimed, unaffordable, self-looping, and cyclic cancels fail without state corruption. |
| C4-OBJ-06 | Round timeout, draw, results | Replace numeric phase behavior with named authoritative states sufficient for active round, terminal freeze, results, and reset. At one resolution point, classify KO, double KO, timeout win, timeout draw, or training exclusion; emit one immutable result payload/event. Results and rematch consume that payload and cannot re-decide a winner from presentation state. |

## Acceptance criteria

| ID | Acceptance criterion | Required evidence |
|---|---|---|
| C4-AC-01 | At identical positions/inputs, 30/60/144 Hz render schedules produce the same terminal snapshot checksum, events, result payload, and tick count. | Automated replay corpus and recorded digests. |
| C4-AC-02 | Wall approach, head-on walk, corner push, cross-through attempt, and position swap tests prove bounds, non-overlap, stable position-derived facing, and no player-order bias. | Parameterized simulation tests and state snapshots. |
| C4-AC-03 | Jump startup, ascent, descent, landing, airborne hit, and landing recovery have exact state/tick assertions; no movement or action is accepted where state rules prohibit it. | State-transition test table. |
| C4-AC-04 | Standing-back, crouch-back, front, down, cross-up, high, mid, low, air, unblockable, and guard-break/guard-failure cases resolve to the specified damage/stun/state. | Guard matrix with expected snapshots/events. |
| C4-AC-05 | Throw success, range miss, throw tech at both accepted window edges, late/early tech, airborne target, knockdown target, and throw-immunity cases have deterministic outcomes. | Throw matrix and replay tests. |
| C4-AC-06 | Every knockdown/wake-up variant reaches its defined recovery tick; prohibited actions are rejected; wake-up invulnerability neither leaks nor suppresses permitted hits. | Knockdown/wake-up timing tests. |
| C4-AC-07 | Every declared cancel edge is tested for legal hit/block confirmation and cost. Invalid targets, cyclic/self cancels, missing content, bad windows, and insufficient meter are rejected safely. Combo count, scaling, and reset are asserted. | Content-validation and combo regression tests. |
| C4-AC-08 | KO, simultaneous KO, timeout health win, timeout equal-health draw, damage on final timer tick, rematch, and training mode produce exactly one correct terminal classification/payload and reset cleanly. | Results truth table and replay tests. |
| C4-AC-09 | Existing explicit `graybox_rival` fallback remains selectable; unknown/incomplete content remains rejected; no float, renderer, wall-clock, audio, or file I/O enters simulation. | Content-negative tests, static review, and regression suite. |
| C4-AC-10 | Focused tests pass, full existing test suite passes, Ruff passes, and `git diff --check` passes. Existing strict-mypy presentation diagnostics may not be counted as Cycle 4 failures, but no new diagnostic may be introduced in touched simulation/content modules. | Command output saved under `docs/evidence/G4/`. |

## Dependencies

1. Approved Cycle 3 typed `FighterDefinition`, `MoveDefinition`, box schema,
   fixed-step clock, snapshot, and content-rejection contract.
2. An approved Cycle 4 rule table specifying numeric movement/jump/push
   constants, pushbox/hurtbox dimensions, guardable levels, throw-tech window,
   knockdown/wake timings, cancel graph, combo scaling, and result-state names.
   Values belong in validated data where fighter/move-specific; global rules
   must have one versioned authoritative owner.
3. Input-frame support for the agreed jump/throw/guard semantics, preserving
   press edges once per simulation tick.
4. A deterministic replay/checksum harness capable of capture and comparison
   across 30/60/144 Hz synthetic schedules.
5. Cycle 5 consumes these state and event contracts; no visual dependency may
   block Cycle 4 simulation validation.

## Safety and error conditions

| Condition | Required safe behavior |
|---|---|
| Malformed/missing movement, guard, throw, knockdown, cancel, or result content | Reject match construction with a precise validation error; never silently substitute generic combat values. |
| Out-of-range position, impossible state combination, timer underflow, negative meter/health, or unknown result reason | Fail the test/debug assertion and prevent a checksum from being certified; release-mode handling must reset only through the documented safe match-construction path and record a diagnostic. |
| Simultaneous strikes/throws/KO/expiry | Use a single documented resolution order, independent of player iteration; produce one terminal payload. |
| Catch-up cap/drop-frame condition | Do not invent inputs or advance presentation-owned time in simulation; preserve the fixed-step clock policy and record a diagnostic for performance investigation. |
| Presentation missing/failing after a terminal event | Preserve the authoritative result payload and offer the existing results/rematch fallback; presentation may not alter winner, draw, or state. |
| Content graph cycle or invalid cancel transition | Reject content at load time; never recurse or permit unbounded same-tick transitions. |

## Work breakdown structure

| WBS | Work package | Exit deliverable |
|---|---|---|
| 4.1 | Freeze Cycle 4 rule table, state diagram, terminal-result truth table, resolution order, and numeric ownership. | Approved versioned rules annex. |
| 4.2 | Extend typed, immutable schemas and validators for state rules, pushboxes, defense, throws, knockdown/wake, cancels, combos, and result reasons. | Valid/invalid content fixtures and loader tests. |
| 4.3 | Implement deterministic movement, wall/push resolution, position-derived facing, and aerial state machine. | State transition and symmetry replay tests. |
| 4.4 | Implement directional defense and strike/throw resolution ordering. | Guard and throw matrices. |
| 4.5 | Implement knockdown/wake-up and cancel/combo state transitions. | Timing, content-graph, meter, and combo regressions. |
| 4.6 | Implement authoritative round terminal state, timeout/draw classification, result payload, reset/rematch contract, and presentation event boundary. | Results truth-table regressions. |
| 4.7 | Expand replay corpus; run deterministic cross-refresh, focused/full regression, lint, typing-delta, and diff-whitespace checks. | Commit-pinned `docs/evidence/G4/` report with commands, versions, digests, and failures/disposition. |
| 4.8 | Conduct implementation review against every acceptance criterion and request the approval gate. | Traceability matrix and gate record. |

## Principal risks and controls

| Risk | Impact | Control / decision trigger |
|---|---|---|
| Rule table is incomplete or changes during implementation. | Ambiguous behavior and rework. | Gate 4.1 before coding; changes require versioned approval and affected replay updates. |
| Facing/push or simultaneous resolution is player-order dependent. | Non-determinism and unfair matches. | Symmetry tests with swapped players/positions; fail gate on divergent snapshots. |
| New schema is only partially authoritative. | Generic fallback values negate data validation. | Validate all selected fighter packages; reject missing required fields; test distinct values. |
| Cancel graph creates loops or one tick launches multiple transitions. | Hang, exploits, checksum instability. | Load-time graph validation; per-tick transition cap with asserted violation. |
| Terminal event is inferred by renderer/finisher. | Incorrect timeout/draw and rematch outcomes. | Immutable simulation result payload; presentation-only consumer tests. |
| Existing tests mask cadence defects. | Fixed-step claim is unproven. | Require same-input 30/60/144 Hz checksum corpus, not tick-count tests alone. |
| Strict-mypy baseline is already nonzero. | New regressions could be hidden. | Baseline diagnostics; require zero new diagnostics in touched simulation/content modules. |

## Validation evidence plan

Store a single commit-pinned report at
`docs/evidence/G4/FUNDAMENTAL_FIGHT_LOOP_REPORT_YYYY-MM-DD.md`. It must name
the commit, Python/dependency versions, platform, commands, outcomes, replay
inputs, and checksums. Attach:

1. Cross-refresh replay digests at 30/60/144 Hz for normal movement, corner
push, cross-up/guard, throw/tech, knockdown/wake, cancel/combo, KO, double KO,
timeout win, and timeout draw.
2. The rule/result truth tables and a test-to-acceptance-criterion matrix.
3. Content fixtures proving valid data loads and each required invalid condition
is rejected.
4. Focused and complete test-suite output, Ruff output, touched-module typing
delta, and `git diff --check`.
5. A reviewer statement that simulation remains presentation-independent and
that all terminal outcomes are authored by simulation.

## Explicit approval gate

**Approve Cycle 4 implementation only when all of the following are true:**

1. Product/design owner signs the rule table in dependency 2, including every
   numeric policy and the timeout/draw/result truth table.
2. Engineering accepts the deterministic resolution order, typed-schema
   ownership, state diagram, and error behaviors.
3. QA accepts the acceptance criteria, matrices, replay corpus, and evidence
   destination.
4. Release owner accepts the bounded scope and confirms that a Cycle 4 pass
   and confirms that a Cycle 4 pass is not commercial-release authorization.

**Cycle 4 exits only when C4-AC-01 through C4-AC-10 pass with the required G4
evidence.** Any failed deterministic, safety, content-validation, or terminal
results criterion is a blocking return to its owning WBS item. Approval then
authorizes Cycle 5 fighter/frame/scene work only; it does not waive later
controls, packaging, performance, or release gates.

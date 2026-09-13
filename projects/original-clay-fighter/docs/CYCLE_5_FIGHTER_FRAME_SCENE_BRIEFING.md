# Cycle 5 Fighter, Frame, and Scene Integration Briefing

**Status:** Approval required. Do not implement Cycle 5 until approved.  
**Baseline:** Cycle 4 commit `4448d8d`; 20 tests, Ruff, deterministic replay, and smoke checks passed.  
**Scope:** Integrate existing Blender-made character and scene assets into the authoritative combat and presentation state. No character-art creation or redesign is included.

## Decision requested

Approve a bounded integration pass for the four selectable fighters, 122 runtime
PNG frames, existing manifests, existing special/armor clips, and three
selectable stage backgrounds. This cycle corrects frame timing, pivots, state
mapping, presentation caching, and scene readability without changing the
approved character assets or expanding the shared normal move kit.

## Audit findings

| Priority | Observed gap | Cycle 5 correction |
|---|---|---|
| P0 | The renderer advances all clips at `tick // 4` (15 fps), ignoring declared 8/12 fps manifest values. | Use a manifest-driven tick-to-frame clock that does not affect simulation timing. |
| P0 | Manifest pivots are ignored. Three fighters use `(256, 480)` but Rhinestone Angel declares `(512, 1000)`, outside the 512x512 source frame. | Derive render placement from manifest pivot, scale, and stage ground line; report invalid source pivots explicitly and use a documented fallback only when needed. |
| P0 | Reachable Cycle 4 states have incomplete/incorrect clip mapping: throw, landing, ascent/descent, blockstun, KO, and results have no explicit route; blocking always uses `block_low`. | Add a versioned presentation coverage map from combat state/result/guard level/move to an existing clip or documented fallback. |
| P1 | Fighter identity is visible in special and armor assets, but shared normal mechanics remain intentionally identical. | Preserve shared normal values; demonstrate each existing special/armor state through state/event/frame traces. |
| P1 | Stages are fixed 1280x720 backgrounds; declared stage/asset coverage and fighter/HUD safe areas are not verified. | Validate stage IDs/assets; capture each fighter and reachably mapped state on each stage. |
| P1 | Sprite flips allocate presentation surfaces and finishers pre-scale large sequences. | Cache flipped/scaled character frames. Measure selected-fighter/stage/finisher memory and frame time; finisher loading optimization remains Cycle 8 work. |

## Work breakdown structure

| WBS | Deliverable | Dependencies | Acceptance evidence |
|---|---|---|---|
| 5.1 | Presentation coverage map | Cycle 4 state/result contract and clip manifests | Four-fighter x reachable-state matrix with no unresolved runtime key. |
| 5.2 | Manifest frame clock | 5.1; declared clip FPS | 8/12 fps tick-sequence unit tests and observed frame trace. |
| 5.3 | Pivot-aware placement | 5.1; stage `ground_y` | Per-fighter source pivot, scale, baseline, fallback record, and ground-contact capture. |
| 5.4 | Fighter presentation profile | 5.1-5.3; existing move data | Existing special/armor trace for every selectable fighter. |
| 5.5 | Scene and HUD readability | 5.3; stage assets | State captures for all fighter/stage combinations with unobscured HUD. |
| 5.6 | Measurement and regression evidence | 5.1-5.5 | Commit-pinned report, replay invariance, tests, lint, headless/smoke output. |

## Acceptance criteria

1. Every reachable fighter mode, guard level, result, and existing move resolves a declared clip or explicit approved fallback. Missing assets never produce a crash or a silent substitute.
2. 8 fps and 12 fps clips follow their manifest cadence to within one visual frame over ten seconds. Simulation checksums and move timing remain unchanged.
3. Grounded fighters contact stage ground `y=600` within two rendered pixels. An invalid source pivot is reported and uses a documented fallback rather than being ignored.
4. All four fighters preserve their existing special identities; Tech Billionaire armor states map to the existing armor clips. Shared normal data remains unchanged.
5. Each selected fighter is captured on each playable stage in neutral, attack, guard, airborne, knockdown/wake, and results states. HUD values remain readable and unobscured.
6. Replaying the same input at synthetic 30/60/144 Hz render schedules leaves Cycle 4 authoritative checksums and result payloads unchanged.
7. Cached transforms reduce repeated allocation where measurable. Record ten-minute match peak memory/frame-time observations; do not claim a low-spec finisher budget until Cycle 8.

## Risks and controls

| Risk | Control |
|---|---|
| The Angel source pivot is beyond the source frame and may reveal a source-space inconsistency. | Validate at load time, emit a diagnostic, and record an approved render fallback. |
| Correct manifest cadence may expose visual timing that differs from hit frames. | Keep collision simulation authoritative; test presentation traces and preserve Cycle 4 checksum results. |
| Existing clips do not cover every state. | Require an explicit existing-clip fallback map; do not add art or silently alias a state. |
| Cached textures increase memory. | Bound cache lifetime to selected fighters/stage and record memory measurements. |
| Stage contrast weakens fighter readability. | Capture the matrix at fight distance and document any stage-specific rendering adjustment for later approval. |

## Validation plan

Run manifest and stage validation; unit tests for clip selection, fallback,
timing, pivots, and cache behavior; presentation trace comparisons for
30/60/144 Hz; selected-fighter/stage matrix capture; existing regression tests,
Ruff, scoped typing checks, headless hash, smoke, and `git diff --check`.
The existing full-presentation mypy debt remains separately tracked and may not
hide new diagnostics.

## Approval gate

Authorize implementation only after product accepts the existing-assets-only
scope and fallback policy; engineering accepts the simulation/presentation
boundary and pivot/timing rules; QA accepts the state/stage coverage matrix,
two-pixel ground-contact tolerance, and replay evidence plan. Passing Cycle 5
does not authorize Cycle 6 controls/settings implementation.

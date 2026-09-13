# Papier Parade Commercial-Readiness Audit

**Date:** 2026-09-13  
**Disposition:** Prototype only. Do not authorize commercial release or unbounded content expansion.  
**Approval requested:** Approve Cycle 1, the first-build audit and requirements baseline. No gameplay/source update is authorized by this briefing.

## Top-priority objective

Deliver a commercially releasable local PC fighting game only after the build is demonstrably reliable, accessible, package-tested, and playable on the declared minimum hardware. Preserve this ordering:

1. Platform and distribution readiness.
2. Player trust: controller support, pause/settings, feedback, and predictable match behavior.
3. Deterministic combat correctness and performance.
4. Measured gameplay, art, audio, and release polish.

The immediate five items are mandatory first-review scope: **controller support; pause/settings; one-shot combat sound effects; packaged-build testing; and reducing finisher transition load on slower hardware.** Existing Blender-made character art is the accepted visual baseline. Character-art creation and redesign are not in scope for this audit or its implementation cycles.

## Verified baseline and release blockers

| Priority | Area | Verified finding | Required correction and acceptance evidence |
|---|---|---|---|
| P0 | Packaging | Runtime assets/data are loaded from source-tree-relative paths and are not configured as installed package resources. No packaged artifact is verified. | Package resources with a single resolver; build and clean-install a `onedir` artifact from another working directory; run asset/audio/headless smoke tests. |
| P0 | Fixed-step combat | Windowed play advances one simulation tick per rendered frame; the fixed-step clock is not authoritative. | Drive simulation at 60 Hz through an accumulator. Replays must produce identical checksums under synthetic 30/60/144 Hz render schedules. |
| P0 | Authored combat | Fighter/move/box YAML exists but live combat uses generic hard-coded timing, range, damage, and collision behavior. | Compile validated content into immutable match definitions. Test each move's timing, boxes, results, and special behavior. |
| P0 | Finisher lifecycle | KO transitions are presentation-coupled; media loads/scales after KO with no authoritative finisher window, results, timeout/draw, or reliable cleanup state. | Add enum-backed `KO_HOLD -> FINISHER_WINDOW -> RESULTS/RESET` simulation states; test KO, draw, skip, unavailable media, rematch, and checksum consistency. |
| P1 | Controllers | Combat is keyboard-only; no hot-plug, reconnect, remapping, device-specific prompts, menu navigation, or focus-loss handling. | Implement an action-based input router and two-controller/device test matrix. Disconnect pauses and presents a reconnect path. |
| P1 | Pause/settings | Escape exits; no pause, settings, persisted preferences, focus-loss pause, audio/window options, or accessibility controls. | Add validated, atomic user settings; test pause freeze, settings restore, corrupt-settings recovery, and app-data containment. |
| P1 | Audio | Music loops only; combat events do not trigger one-shot SFX; volume is fixed and device failures are silent. | Add typed presentation events, cached one-shots, mixer/category policy, user controls, and silent-device fallback. Validate one cue per intended event. |
| P1 | Art/frame integration | Some clips declare 8/12 fps but runtime displays at a fixed 15 fps. Core states are single held frames or never selected; sprite pivots/lighting differ. | Honor manifest timing and event metadata; establish pivot, value, lighting, alpha, scale, and animation acceptance checks. |
| P1 | Performance | Finishers synchronously decode and upscale frames at KO; UI and fighter assets are repeatedly scaled. The current headless rate is not rendered performance evidence. | Preload/cache selected content in a loading state; cache transforms; capture frame-time percentiles, memory, and transition time on target minimum hardware. |
| P1 | Type and test quality | Strict mypy currently reports 41 errors; only four simulation tests exist; no CI build gate was found. | Resolve typing or explicitly revise the standard; add CI for lint, typing, content, deterministic replay, wheel install, and SDL-dummy smoke. |
| P2 | Design/playability | Fighters share generic moves; fundamental states and counterplay are incomplete. Mouse-led UI and no training/onboarding prevent meaningful playtest. | Add core state/frame system, differentiated data-driven kits, training mode, move list, and structured matchup testing. |
| P2 | Provenance/readiness docs | Asset, audio codec, finisher, roster, and release records conflict. | Generate a signed inventory with source, hash, version, and release status; reconcile traceability. |

## First-review work packages

The 12 packages catalog design, frames, fight scenes, action, gameplay, controllers, audio/music, meshing, playability, lines/voicing, lighting/modeling, and code/release engineering. They are listed in dependency order; they are not authorization to change the build.

| ID | Work package | Improvement scope | Approval evidence |
|---|---|---|---|
| IMP-01 | Baseline and product decisions | Freeze scope; reconcile asset/roster/documentation conflicts; select first OS, store, audience, ratings posture, minimum hardware, and owner. | Signed inventory, traceability, and risk register. |
| IMP-02 | Fixed simulation and content contracts | Establish 60 Hz windowed simulation, typed schemas, and data-authoritative profiles/moves/boxes. | Cross-refresh deterministic replay corpus; schema/content tests. |
| IMP-03 | Core fighting design | Define push/facing, jump/dash, high/low block, throws/counterplay, knockdown/wake-up, cancels/combos, ties, and result flow. | Frame-data specification, hitbox captures, state-transition tests. |
| IMP-04 | Character differentiation and animation | Replace generic kits and held poses with data-driven roles, readable startup/contact/recovery, state coverage, and manifest-correct FPS. | Per-fighter move sheet, 720p readability review, replay tests. |
| IMP-05 | Controller, UI, and accessibility | Add remappable semantic actions, controller lifecycle, keyboard/controller menus, tutorial/training, focus, pause/settings, contrast, reduced effects. | Two-player controller matrix, settings/persistence tests, accessibility checklist. |
| IMP-06 | Combat feedback, sound, and voice | Implement one-shot hits/blocks/KO/UI cues, mixer groups, visual redundancy, music controls, and character-bark or no-VO decisions. | Cue sheet, provenance, trigger-once tests, listening sessions. |
| IMP-07 | Art, meshing, lighting, and VFX | Implement a common Blender rig/UV/material/export contract; correct pivots; create atlas/event metadata, stage readability, clay-consistent VFX, reduced-flash controls. | Rig/export validation, atlas checks, stage silhouette and flash review. |
| IMP-08 | Finisher lifecycle and performance | Make deterministic results transitions, preload/cache media, graceful media fallback, transformed-asset caching, and low-spec budgets. | 95th-percentile KO transition/frame-time/memory results on the target floor. |
| IMP-09 | Packaging, security, and assurance | Use reproducible package build, resource loading, versioning, dependency/SBOM/license process, CI, content validation, and clean-machine tests. | Signed/hashable artifact, install/launch/exit/uninstall evidence. |
| IMP-10 | External validation and release decision | Conduct structured playtests, balance passes, release-candidate triage, platform/content review, support plan, and launch gate. | Matchup data, defect disposition, release checklist, executive go/no-go. |
| IMP-11 | Stage/fight-scene production | Complete or formally defer declared stages; add parallax, safe foregrounds, ground shadows, camera rules, and non-gameplay hazards only after readability. | Per-stage technical/art review and performance capture. |
| IMP-12 | Rollback readiness (not delivery) | Add canonical byte snapshots, restore/resimulate tests, event de-duplication, and input-history boundaries. No online claim or feature is included. | Local rollback-harness results and architecture decision record. |

## Ten-cycle waterfall program

Each cycle requires the preceding gate to pass. Any failed requirement returns to the owning cycle; no later cycle is assumed complete by artifact presence alone.

| Cycle | Objective and bounded scope | Depends on | Exit evidence | Approval gate |
|---|---|---|---|---|
| 1. First-build audit | Freeze baseline; reconcile documentation, roster/assets, risks, and the five immediate items. Declare supported OS, store, minimum hardware, performance target, and release authority. | Current repository inventory and named decision owner. | Commit-pinned inventory; corrected traceability; initial hardware/device matrix; measured source-build baseline; prioritized closure plan. | Approve requirements/product baseline. |
| 2. Requirements and architecture | Baseline functional/nonfunctional requirements for controls, settings, sound, frame data, performance, packaging, security/privacy, accessibility, and content. Design input, pause/settings, audio-event, finisher-lifecycle, and resource interfaces. | Cycle 1 approval. | Approved SRS/architecture, data schemas, error paths, test plan, and measurable budgets. | Approve implementation baseline. |
| 3. Deterministic combat foundation | Make fixed 60 Hz simulation authoritative; validate content schemas and state snapshots; convert generic combat toward authored data. | Cycle 2 contracts. | 30/60/144 Hz checksum equivalence; schema tests; content inventory; typed-model progress. | Approve combat-core baseline. |
| 4. Fundamental fight loop | Implement/review movement, push/facing, aerial states, defensive rules, throws, knockdown/wake, attacks, cancels, rounds, timeout/draw, and results. | Cycle 3. | State, frame-data, hitbox, trade, guard, throw, and results regression evidence. | Approve complete core rules. |
| 5. Fighter, frame, and scene pass | Integrate differentiated data-driven kits; complete required animations; correct manifest FPS/pivots/lighting; add readable stage/camera/interaction rules. | Cycle 4 and approved visual contract. | Fighter move sheets; in-engine state coverage; 720p readability test; matchup replay corpus. | Approve playable roster alpha. |
| 6. Controls, settings, and onboarding | Add controller hot-plug/remapping, device prompts, focus navigation, pause/focus-loss behavior, persisted settings, training, move list, and accessibility controls. | Cycle 2 interfaces and Cycle 5 UI states. | Keyboard/controller matrix; persistence tests; contrast/focus evidence; first-time-player test. | Approve usability/accessibility baseline. |
| 7. Sound, voice, VFX, and lighting | Add event-driven original one-shots, mixer categories, music/SFX/voice settings, visual feedback, clay-consistent VFX, stage lighting, and voice/bark policy. | Cycles 5-6; cleared media rights. | Cue/event map; trigger-once tests; listening test; VFX/flash review; provenance updates. | Approve presentation baseline. |
| 8. Finishers and low-spec performance | Implement authoritative finisher window/results cleanup, cache/preload strategy, asset budgets, low-spec fallback, and performance instrumentation. | Cycles 3-7. | Minimum-hardware frame-time, memory, load, KO, skip, rematch, and failure-path captures. | Approve release-performance baseline. |
| 9. Package and quality system | Build a reproducible package, resource resolver, CI, static quality, dependency review, SBOM/license process, and clean-machine compatibility tests. | Cycles 1-8; platform decision. | Wheel/package artifact, hashes, clean install/uninstall/launch/exit results, CI report, zero approved release blockers. | Authorize controlled external beta. |
| 10. Beta and commercial decision | Run external playtests, matchup/balance sessions, hardware/controller/audio/accessibility/content review, defect triage, release notes, support plan, and final go/no-go. | Cycles 1-9 all passed. | Test reports, defect disposition, rights/rating/store evidence, signed release checklist, rollback/monitoring plan. | Approve release candidate or return to owning cycle. |

## Commercial benchmark constraints

- **Input:** Action-based controls, two-controller support, keyboard/controller parity, remapping, disconnect pause/reconnect, device-specific prompts, and non-mouse-only menus. This aligns with [Steam Input guidance](https://partner.steamgames.com/doc/features/steam_controller/getting_started_for_devs), [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/allow-controls-to-be-remapped-reconfigured/), and [Xbox Accessibility Guideline 112](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/112).
- **Feedback/accessibility:** Critical states require redundant visual/audio/text cues; provide separate Master/Music/SFX/Voice controls, high-contrast focus and essential UI states, reduced flash/effects controls, and never describe any setting as “epilepsy safe.” Sources: [XAG 103](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103), [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [audio controls guidance](https://gameaccessibilityguidelines.com/provide-separate-volume-controls-or-mutes-for-effects-speech-and-background-music/), and [photosensitivity guidance](https://gameaccessibilityguidelines.com/avoid-flickering-images-and-repetitive-patterns/).
- **Audio:** Configure and test explicit Pygame-ce mixer parameters before initialization; buffer size is a latency/dropout tradeoff. Source: [Pygame-ce mixer documentation](https://pyga.me/docs/ref/mixer.html).
- **Distribution:** Start with a reproducible PyInstaller `onedir` build plus explicit data files; a packaged build—not an editable install—is the release-test subject. Source: [PyInstaller usage](https://pyinstaller.org/en/stable/usage.html).
- **Future online:** Deterministic snapshots, restoration, re-simulation, input history, and presentation-event de-duplication are prerequisites. They do not constitute online/rollback support. Source: [GGPO rollback overview](https://github.com/pond3r/ggpo/blob/master/doc/README.md).
- **Asset baseline:** Preserve per-file asset/music/voice source, version, and export metadata so approved Blender-made character art and its runtime derivatives remain traceable through build and release.

## Approval decision

Approve **Cycle 1 only** to formalize and reconcile the release baseline. It produces requirements, evidence, target hardware/platform choices, and an implementation-ready backlog; it does not alter fight behavior, art, or shipping configuration. Implementation begins only after the Cycle 1 briefing/gate is accepted.

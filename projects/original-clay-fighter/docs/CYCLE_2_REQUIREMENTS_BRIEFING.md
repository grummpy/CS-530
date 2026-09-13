# Cycle 2 Requirements and Architecture Briefing

**Status:** Approval required. Do not implement Cycle 2 until this briefing is approved.  
**Cycle 1 evidence:** [`evidence/CYCLE_1_BASELINE.md`](evidence/CYCLE_1_BASELINE.md)  
**Scope:** Requirements, architecture, ownership, test design, and measurable acceptance baseline only.

## Decision requested

Approve the requirements and architecture baseline for a local Windows desktop
game. This cycle defines implementation contracts for fixed-step simulation,
input/controller behavior, settings, audio, finisher resources, packaging, and
quality assurance. It does not create or redesign character art, add fighters,
implement online play, expand stages, complete balancing, or launch a store
release.

## Provisional delivery target

These planning values require approval before implementation. They are not
claims of verified commercial performance.

| Item | Proposed baseline | Decision needed |
|---|---|---|
| First platform | Windows 10 22H2 / Windows 11, 64-bit | Confirm OS/store target. |
| Presentation | 1280x720 internal/windowed baseline, 60 FPS | Confirm available display modes. |
| Package test subject | PyInstaller `onedir` package outside the source tree | Confirm packaging path. |
| Minimum CPU | 64-bit dual-core, approximately 2.5 GHz class | Name representative test machine. |
| Minimum RAM | 4 GB system RAM | Confirm target floor. |
| Graphics | Integrated GPU capable of SDL/Pygame-ce at the baseline presentation target | Name representative test machine. |
| Storage | 1 GB free, subject to measured package size | Approve after artifact measurement. |
| Input | Keyboard plus two XInput-compatible controllers | Confirm supported controller models. |
| Audio | Stereo output with continued play if no device is available | Approve expected fallback behavior. |

## Requirements baseline

| ID | Requirement | Verification approach | Planned implementation cycle |
|---|---|---|---:|
| FR-SIM-01 | Simulation advances in authoritative 60 Hz fixed ticks independently of render cadence. | Cross-refresh replay checksums. | 3 |
| FR-SIM-02 | The same input stream under 30/60/144 Hz synthetic render schedules produces identical checksums. | Automated deterministic replay suite. | 3 |
| FR-INPUT-01 | Devices map to semantic actions rather than device-specific combat logic. | Unit/integration input tests. | 6 |
| FR-INPUT-02 | Support two controllers, mixed keyboard/controller play, hot-plug, reconnect, and device-appropriate prompts. | Device matrix and human test. | 6 |
| FR-INPUT-03 | Controller disconnect and focus loss pause matches and provide a deterministic resume/reconnect path. | Lifecycle/focus tests. | 6 |
| FR-SET-01 | Pause preserves match state; settings validate, persist atomically, and recover safely from corrupt data. | Persistence/failure-path tests. | 6 |
| FR-SET-02 | Settings include Master/Music/SFX/Voice levels, window mode, remapping, reduced effects, and high-contrast focus support. | UI/accessibility review. | 6 |
| FR-AUDIO-01 | Typed simulation events trigger no more than one intended sound effect per event identity. | Event/deduplication tests and listening test. | 7 |
| FR-FIN-01 | KO uses simulation states `KO_HOLD -> FINISHER_WINDOW -> RESULTS/RESET`. | State/lifecycle/replay tests. | 8 |
| FR-FIN-02 | Selected finisher media preloads or caches before KO; missing media returns safely to results. | Resource/failure-path/performance tests. | 8 |
| FR-PKG-01 | Data and assets resolve through a single source/wheel/frozen-package-aware resolver. | Installed-package smoke test from another directory. | 9 |
| FR-PKG-02 | Build a reproducible Windows `onedir` package with explicit bundled resources. | Clean-machine install/launch/exit/uninstall test. | 9 |
| NFR-PERF-01 | Measure 95th-percentile frame time, memory, startup, match-load, and KO-transition time on the approved minimum device. | Performance capture. | 8-9 |
| NFR-QUAL-01 | CI gates lint, agreed typing standard, content validation, deterministic replay, package install, and SDL-dummy smoke. | CI artifact and logs. | 9 |
| NFR-ACC-01 | Essential UI/match states have redundant visual/text/audio feedback and non-mouse-only control. | Accessibility checklist and player test. | 6-7 |
| NFR-REL-01 | Missing optional media, audio absence, corrupt settings, controller loss, and focus loss do not corrupt match state or player data. | Negative-path regression tests. | 6-9 |

## Architecture contracts

| Boundary | Contract | Non-negotiable rule |
|---|---|---|
| Simulation | `advance(p1_input, p2_input) -> snapshot, presentation_events` | Simulation has no Pygame, renderer, audio, file I/O, wall-clock, or floating-point authoritative-state dependency. |
| Input | `device -> action state -> InputFrame` | Edges are generated once per simulation tick. Device assignment, remapping, prompts, focus, and reconnect remain outside simulation. |
| Settings | Versioned schema with defaults, validation, migration, and atomic load/save in platform user-data storage. | Invalid persisted data falls back safely and records a recoverable diagnostic. |
| Audio | Tick/event-sequenced event IDs and categories feed a mixer/cache policy. | Audio never changes simulation state; replay/resimulation cannot duplicate cues. |
| Finisher resources | Validated manifest identifies variants, duration, skip policy, and resource paths; resource manager reports ready/missing/failed. | Simulation controls lifecycle; presentation controls playback only. |
| Packaging | One resource resolver locates immutable bundled resources in source, wheel, and frozen contexts. | User settings/logs never write inside an installation directory. |

## Cycle 2 WBS

1. Baseline platform, release, device, and performance decisions.
2. Map every requirement to owner, implementation cycle, test method, and evidence path.
3. Approve fixed-step, snapshot/checksum, and presentation-event interface contracts.
4. Approve input actions, controller lifecycle, remapping, and focus behavior.
5. Approve settings persistence, pause behavior, accessibility, and error behavior.
6. Approve audio category/mixer/event contracts.
7. Approve finisher lifecycle, preload/cache, fallback, and cleanup contracts.
8. Approve packaging/resource-resolution and CI/test contracts.
9. Record dependencies, risks, and the Cycle 3 implementation authorization decision.

## Gate criteria

Cycle 2 passes only when:

1. The project owner approves the provisional platform, distribution, input, and minimum-hardware baseline.
2. Numeric performance budgets and a named representative test system are recorded.
3. Each requirement has an owner, planned cycle, verification method, and evidence destination.
4. Engineering accepts all six architecture contracts and their failure behavior.
5. QA/release ownership accepts the device, package, and regression-test plans.
6. The approved scope remains limited to requirements and architecture. No implementation is implied by this approval.

## Recommendation

Approve Cycle 2 as the requirements-and-architecture baseline once the
provisional platform and hardware decisions are accepted. On approval, Cycle 3
will implement and test the deterministic simulation foundation only.

# Cycle 7 Audio and Presentation Briefing

**Status:** Approval required. Cycle 7 is presentation-only and cannot change
authoritative combat state, timing, inputs, checksums, or results.

## Decision requested

Approve event-driven combat/UI feedback: one-shot SFX, mixer/settings
integration, safe audio fallback, bounded clay-consistent VFX, result feedback,
stage readability profiles, and reduced-effects behavior. Packaging,
finisher-load performance, and character-art work remain out of scope.

## Audit baseline

Five PCM music files are present, but windowed play does not call the music
starter. The direct music API has no category gains, mutes, one-shot sounds,
device state, or failure tests. Simulation emits transient string events
(`hit`, `block`, `throw`, `land`, and results), without IDs or payloads, and no
presentation consumer exists. Guard ring is the only visual feedback and is
removed by reduced effects. All stage images validate, but selected-stage flow
and results clip routing are incomplete.

## Required contracts and WBS

| WBS | Contract/deliverable | Acceptance evidence |
|---|---|---|
| 7.1 | Immutable presentation events: version, monotonic ID, tick, kind, actor/target, position, move/strength/result metadata. | Ordering, same-tick, reset/result, and checksum-invariance tests. |
| 7.2 | Exactly-once non-authoritative dispatcher. | Re-render/pause/replay cannot duplicate cue/effect. |
| 7.3 | Central mixer service: Master/Music/SFX/Voice/UI categories, caching, priority, shutdown, no-device mode. | Injected init/load/channel failure matrix; match continues safely. |
| 7.4 | Versioned bounded audio settings and UI. | Migration, persistence, mute/gain live-application tests. |
| 7.5 | Original/placeholder one-shot cue registry and event mapping. | Cue manifest, one-cue-per-event tests, listening capture. |
| 7.6 | Pooled, bounded clay dust/crumb/impact/block/meter/KO feedback. | Hit/block/throw/land/KO/reduced-effects capture matrix. |
| 7.7 | Presentation-only stage tint/contrast-safe zones and result clip route. | Three-stage readability/HUD/fighter captures. |

## Acceptance gate

1. Event IDs are the sole simulation-to-presentation bridge and preserve
deterministic replays.
2. Device, asset, and channel failures enter diagnosable silent mode without
affecting a match.
3. Settings provide bounded Master/Music/SFX/Voice/UI gains and mutes.
4. Reduced effects retain non-color-only hit, block, and KO information.
5. Three-stage feedback/readability captures, automated tests, lint, scoped
typing, headless replay, smoke, and diff validation pass.

## Risks

Deduplicate by event ID to prevent replayed sounds; cap pooled effects and
channels to protect frame time; retain visible feedback in reduced-effects
mode; test category clipping and no-device operation. Cycle 7 completion does
not authorize Cycle 8 finisher-performance work.

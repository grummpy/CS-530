# Status

Cycle 1 commercial-readiness baseline is complete. The playable Pygame-ce
prototype contains four selectable clay fighters, three arena backgrounds,
local/CPU matches, runtime PCM music, HUD health/block/special indicators, and
12 finisher frame sequences.

Cycle 3 deterministic-combat work is complete. The fixed-step clock is
authoritative in the windowed loop, and validated fighter/move/box content
drives existing combat values. See
`evidence/G3/CONTENT_AUTHORITATIVE_REPORT_2026-09-13.md` for the content
contract and validation evidence. Cycle 4 fundamental fight-loop work is
complete against the approved briefing: integer movement/push/facing, jumps,
directional guard, throws, knockdown/wake-up, explicit cancels, and
authoritative result payloads are simulation-owned. See
`evidence/G4/FUNDAMENTAL_FIGHT_LOOP_REPORT_2026-09-13.md` for validation
evidence and the remaining pre-existing presentation typing limitation.

Cycle 5 existing-asset fighter, frame, and scene integration is complete.
Manifest cadence, source-pivot placement with a diagnostic fallback, state and
stage validation, and cached transforms remain presentation-only. See
`evidence/G5/FIGHTER_FRAME_SCENE_REPORT_2026-09-13.md` for commit-pinned
implementation and actual validation results.

Cycle 6 controls, settings, and onboarding is complete. The presentation shell
routes keyboard and Pygame controller input through semantic actions before
creating simulation `InputFrame`s, tracks assignment/hot-plug lifecycle,
pauses safely on focus/device loss, and provides keyboard/controller-operated
title, selection, settings, training, and move-list views. Versioned,
allowlisted settings are written atomically in per-user configuration storage.
See `evidence/G6/CONTROLS_SETTINGS_REPORT_2026-09-13.md`.

Cycle 7 audio and presentation is complete within the approved presentation-only scope.
Immutable event IDs remain checksum-exempt; the dispatcher, failure-safe mixer, audio
settings, cue registry, bounded clay feedback, and stage readability/result routes are
covered by `tests/test_cycle7_presentation.py`. See
`evidence/CYCLE_7_AUDIO_PRESENTATION_REPORT_2026-09-13.md`.

Cycle 8 finisher lifecycle and performance implementation is complete against
the approved provisional target floor/budgets: authoritative KO hold/finisher
window/result transitions, deterministic skip/result data, selected-media
validation, incremental preload, bounded byte-accounted transformed cache,
teardown, deterministic fallback diagnostics, and raw report output are
implemented and validated. Target-floor rendered-performance certification is
still pending on the approved Windows x64 hardware. See
`evidence/CYCLE_8_FINISHER_PERFORMANCE_REPORT_2026-09-13.md`.

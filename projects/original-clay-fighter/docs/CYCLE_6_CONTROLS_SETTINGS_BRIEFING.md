# Cycle 6 Controls, Settings, and Onboarding Briefing

**Status:** Approval required. Do not implement Cycle 6 until approved.  
**Baseline:** Cycle 5 evidence commit `4418a3c`; 26 tests, Ruff, scoped typing,
headless replay, and smoke checks passed.

## Decision requested

Approve a bounded player-operating layer: controller support, semantic actions
and remapping, device lifecycle, keyboard/controller navigation, pause and
focus-loss behavior, persistent settings, training/move-list onboarding, and
focus/contrast/reduced-effects accessibility. This cycle excludes audio,
packaging, finisher-performance, and character-art work.

## Current gaps

- Windowed play directly polls two fixed keyboard layouts; it has no controller
  API, action router, remapping, assignment, hot-plug, reconnect, or
  device-specific prompts.
- Title and selection screens are mouse-led; Enter/Space shortcuts do not form
  a focus-navigation system.
- Escape exits rather than pauses. Focus loss does not preserve input/match
  lifecycle safely.
- No versioned user settings, validated persistence, recovery diagnostics, or
  accessibility preference model exists.
- Training is parsed but not routed to a usable windowed experience; players
  have no reachable input display, reset flow, dummy controls, or move list.

## Work breakdown structure

| WBS | Deliverable | Acceptance evidence |
|---|---|---|
| 6.1 | Device-independent action router | Mapping and per-tick edge tests. |
| 6.2 | Two-player assignment and device lifecycle | Hot-plug/disconnect/reconnect matrix. |
| 6.3 | Keyboard/controller menu focus and prompts | Screen-by-screen navigation capture. |
| 6.4 | Pause and focus-loss behavior | Frozen-state/checksum and recovery tests. |
| 6.5 | Versioned settings persistence | Round-trip, migration, corrupt-file, and atomic-write tests. |
| 6.6 | Training, move list, and first-run onboarding | Scripted first-time-player test. |
| 6.7 | High-contrast focus and reduced-effects preferences | Focus/contrast/reduced-effects review. |

## Required contracts

| Boundary | Contract |
|---|---|
| Input | `physical state/event -> semantic action state -> per-player Action bits -> InputFrame`. Only this final adapter reaches simulation; edges occur once per fixed tick. |
| Shell actions | Add `CONFIRM`, `BACK`, `PAUSE`, `MENU_UP/DOWN/LEFT/RIGHT`, and `OPEN_MOVE_LIST`. Shell actions cannot enter combat action state. |
| Device identity | Track controller instance ID, display label, and player assignment. Loss of an assigned controller pauses the match and marks that player for reconnection. |
| Pause/focus | Pause before more simulation ticks, clear held input, preserve exact match state, and require deliberate resume. |
| Settings | Versioned allowlisted schema with bounded values/bindings, defaults/migrations, atomic temp-sibling replacement, recoverable invalid-data diagnostics, and user-data—not install-directory—storage. |
| Accessibility | One preference model controls high-contrast focus and reduced visual effects. Audio behavior remains out of scope. |

## Acceptance criteria

1. Two supported controllers, keyboard/controller mixed play, and valid remaps
   produce expected semantic-action traces.
2. Assigned-device loss pauses the match; unassigned-device loss does not;
   reconnect/reassignment is tested and cannot alter the paused checksum.
3. Pause, focus loss, minimize/restore, and resume preserve match state and
   cannot create stuck/ghost input.
4. Title, select, settings, pause, training, and move-list UI work entirely
   without a mouse and use visible focus, predictable ordering, and back/return
   behavior.
5. Settings survive restart; malformed JSON, unknown fields, invalid ranges,
   duplicate/conflicting bindings, and interrupted writes recover safely.
6. A first-time player can view controls, select a device, enter training,
   reset, display current inputs, and open the selected fighter's move list.
7. Focus/state is not communicated by color alone; reduced effects suppress
   nonessential visual intensity while preserving gameplay information.
8. Existing deterministic replay, tests, lint, scoped typing, headless smoke,
   and diff validation continue passing.

## Risks and controls

| Risk | Control |
|---|---|
| Controller API/device variance | Test named supported devices and retain a clear generic/unsupported-device fallback. |
| Stuck input after focus/device lifecycle events | Clear physical and semantic held state on pause, loss, disconnect, remap, and reassignment. |
| Unsafe or corrupt preferences | Validate schema/bounds and use atomic writes plus recoverable diagnostics. |
| Unplayable remaps | Reserve essential navigation actions and reject same-context conflicts or require explicit swap. |
| Accessibility regression | Treat focus, contrast, and reduced effects as tested preferences, not visual convention. |

## Approval gate

Approve only after accepting the supported-device/onboarding baseline and the
input, lifecycle, settings, and QA contracts above. Passing Cycle 6 does not
authorize Cycle 7 presentation/audio work.

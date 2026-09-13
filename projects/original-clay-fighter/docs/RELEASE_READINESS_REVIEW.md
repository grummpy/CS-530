# Shelf-readiness review

**Decision: Not releasable.** The project is a G1 combat prototype, not a shelf-ready game. This review applies PAPM program controls and reconciles Jarvis, Leonardo, Super, Sound, Motion, and quality checks.

## Mission and release gate

The release target is a local two-player original-fiction 2D fighter that a player can install, launch, understand, play through a complete match, and exit without broken controls, missing art, absent audio, or stuck states. Passing requires a clean Python 3.12+ installation, a real display/audio run, complete media provenance, and documented acceptance evidence.

| Lane | Current evidence | Gate decision |
|---|---|---|
| PAPM | Scope, risks, and traceability exist. | Blocked by missing production deliverables. |
| Jarvis | Headless deterministic replay and compilation pass. Content import defect was repaired in this review. No packaging, crash, display, device, or audio-device test exists. | Blocked. |
| Super | Local keyboard movement and three attack inputs are implemented; only a minimal KO loop exists. No menus, round flow, blocking, specials, throws, training controls, controller support, save/settings, or playtests. | Blocked. |
| Leonardo | Fighters, stage, HUD, and buttons are procedural rectangles. No sprites, portraits, menus, loading/error imagery, animation, visual QA, or asset masters are committed. | Blocked. |
| Sound | No runtime audio integration, mixer setup, cue sheet, playable WAV files, mix, captions, or volume controls. | Blocked. |
| Motion / finishers | YAML names only; no timeline, state cleanup, skip action, animatic, video, or frame/timecode QA. | Blocked. |
| Quality | Determinism smoke passes. Pytest, Pygame-ce windowed test, controller test, resolution matrix, and packaged build test are unavailable in this environment. | Blocked. |

## Player flow and failure cases

`Launch → title/menu → select fighters/stage → versus match → KO/finisher or rematch → results → quit` is required. The current build starts directly in a match and only supports `Esc` and `R`; it has no UI buttons, focus model, or controller navigation. Missing image/audio files must produce a visible fallback and keep the match playable; no asset system exists yet.

## Critical path to a releasable demo

1. **Runtime foundation:** install and lock Python 3.12/Pygame-ce; add CI, package build, crash logging, real-display/audio smoke, resize/fullscreen/focus-loss recovery, controller reconnect, and a test matrix.
2. **Complete game flow:** build title, fighter/stage select, pause/settings, match rounds, KO/results/rematch, keyboard/controller focus, accessible labels, and every button's enabled/back behavior.
3. **Graphics:** create original editable character masters and exported sprites, animated state clips, stage layers, HUD/menu/button art, loading/error fallbacks, and an asset manifest. Validate alpha, pivots, scaling, contrast, 720p/1080p/1440p, and missing-file behavior in-game.
4. **Sound:** define a cue sheet; create and license/provenance-track UI, movement, hit, KO, ambience, and finisher assets; add mixer categories, volume/mute controls, channel limits, captions/visual alternatives, device fallback, and a no-clipping mix review.
5. **Finishers:** use original, absurd non-graphic transformations. Implement deterministic timeline state, skip/cancel, cleanup, return-to-results, and one short video/animatic per fighter only after acceptance tests. Video is optional for a 2D runtime if in-engine timelines meet the player-facing result; it is mandatory only if marketed as cinematic video.
6. **Content and balance:** author full data-defined move kits and frame data; add blocking, throws, special/super rules, hitbox viewer, training mode, controller mapping, recorded playtests, regression replays, and balance evidence.

## Acceptance evidence before release

Every launch button and menu action must pass mouse, keyboard, and controller tests; every image must be captured at target resolutions and with an intentionally missing asset; every cue must be heard and checked for sync, clipping, looping, device absence, and visual alternative; every finisher must be frame-stepped for start, skip, cleanup, and match recovery. Build a clean distributable, install it on a system without the development environment, and run a complete two-player match.

## Production backlog

P0: release pipeline, menu/input contract, asset and audio manifests, full display/audio/controller test matrix.  
P1: original sprites/UI/stage/animations, mixer and sound library, finisher timeline and six playable finishers.  
P2: optional rendered finisher videos, controller remapping, accessibility polish, balance playtests, performance profiling.

No dates, cost, staffing, or completed media are asserted because the repository contains none of that evidence.

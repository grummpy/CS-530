# Cycle 5 Fighter, Frame, and Scene Report

**Implementation commit:** `a875ea5e5afa21eabb49094380e6ada08beed339`  
**Validation environment:** `.venv` Python 3.12.14, 2026-09-13

## Implemented scope

The presentation layer now loads and validates the committed Blender-frame
manifests and the three approved stage definitions. `presentation.assets`
contains version 1 of the state coverage map. Each Cycle 4 fighter mode,
guard level, attack move, and result selects an existing declared clip or
returns a named fallback. Notable explicit fallbacks are jump startup/descent
to `jump`, landing to `wake`, throws to `heavy`, and KO to `knockdown`.

Clip frame selection derives from the 60 Hz tick number and each clip's
declared 8/12 FPS; it does not write simulation state. Sprite placement uses
the source pivot and the stage's `ground_y=600`. The Angel's invalid
`(512, 1000)` source pivot is diagnosed once at runtime and uses the documented
lower-center `(256, 511)` fallback. Scaled and mirrored clip frames are cached
per fighter/clip/facing.

Tech Billionaire armor maps to `armor_idle`, `armor_punch`, or `armor_kick`;
the activation route remains `exosuit_call`. Other fighters' declared special
clips remain `kitchen_rush`, `hostile_takeover`, and `star_chord`. No art,
controls, audio, finisher behavior, or packaging was changed.

## Actual validation results

| Check | Result |
| --- | --- |
| Focused manifest timing, pivot, mapping, cache, and stage tests | 6 passed |
| Full test suite | 26 passed |
| Ruff (`src`, `tests`) | passed |
| Scoped mypy (`presentation/assets.py`) | passed |
| `python -m fighter headless` | passed |
| `git diff --check` | passed |
| 180-tick seed 1 replay | `bad005e9e8277fe57c9ccf44eaa11609e7275c05d9fc5058c55e70a818af4e8b` |
| 120-tick 30/60/144 Hz schedule | identical `d3f958ea7fa80ca7c994c13ca443a6f175f752030cc2570caa4f410924732819` and no result |

The focused cache test confirms a repeated request returns the same scaled,
flipped frame tuple without additional loads/transforms. The diagnostic policy
and stage contract are verified for all four selectable fighters and all three
approved stages. The existing `perf.report()` measurement recorded 6,000
headless simulation ticks in 0.039068 seconds (153,577.07 ticks/sec); it is
not a render-memory or ten-minute frame-time claim. Finisher optimization
remains deferred to Cycle 8 as scoped.

# Original Satirical Clay Fighter: Executive Plan

## Decision brief

Build a local, 1v1, six-fighter 2D combat prototype that launches and debugs from PyCharm. The recommended first implementation is Python 3.12+ with Pygame-ce. It validates the combat, visual pipeline, and finishers quickly while preserving a clean decision point before production.

The project owner selects the character and parody direction for this private prototype. Every imported or generated asset must retain documented provenance and a review record. Finishers should be theatrical and surreal: clay deformation, confetti, paper, paint, broken props, and absurd reversals rather than realistic injury.

**Prototype success criteria**

- Six differentiated original fighters complete local matches with keyboard and supported controllers.
- Combat is responsive and deterministic at a 60 Hz simulation rate and targets 60 FPS at 1080p on the agreed reference laptop.
- Every fighter uses data-defined moves, hit/hurt/push boxes, frame data, and one short finisher.
- Training/debug mode provides frame stepping, input history, hitbox viewing, reset, and dummy behavior.
- The project launches from a documented PyCharm configuration on a clean supported development machine.
- Each fighter and finisher passes an originality/content review before integration.

**Explicit exclusions for this phase:** online/rollback delivery, campaign/story mode, real-person depictions, monetization, accounts, console certification, and more than six fighters.

## Recommended technical direction

| Option | Recommendation | Rationale |
|---|---|---|
| Pygame-ce + Python | Adopt for prototype | Fast PyCharm iteration, SDL input/audio, transparent fixed-step loop, and minimal framework overhead. |
| Arcade | Evaluate only if effects demand it | OpenGL sprite batching is useful, but it offers little early advantage for two fighters and a small stage. |
| Godot | Primary production candidate | Mature 2D editor, animation, shaders, camera, audio, and export workflow; use GDScript or C#, not Python, for runtime gameplay. |
| Unity | Conditional production candidate | Strong multi-platform tools, Timeline, and input ecosystem, but justified only with existing C# expertise and a platform requirement. |
| Unreal | Do not use for the prototype | High-end cinematics are attractive, but complexity and staffing costs outweigh benefits for this scope. |

Use a hybrid visual pipeline: sculpt original clay-like characters in Blender, rig and animate them, and render sprite sequences for the 2D fight plane. Rendered 2D fighters retain legibility and deterministic collision; optional real-time 3D is limited to stage decoration and finishing-move camera shots. Use a 3/4 orthographic fight camera, warm key/cool rim lighting, visible handcrafted seams and fingerprints, and a shared material palette.

Combat simulation must be independent of Pygame presentation:

```text
physical input -> action bitfields -> fixed 60 Hz simulation -> deterministic events
                                                        |-> rendering/camera/VFX/audio
                                                        |-> replay/checksum/test tools
```

Authoritative simulation uses integer or fixed-point state, fixed tick timers, stable collision ordering, serializable match RNG (or no combat RNG), and no gameplay dependence on wall time, rendering, camera, particles, or audio. Record canonical per-tick inputs and hash canonical state periodically. This gives local replay reliability now and preserves the option to assess rollback networking later.

### Core project layout

```text
pyproject.toml
src/fighter/
  app.py
  platform/pygame_app.py
  sim/{world,fighter,fixed,input_frame,commands,state_machine,move_system,
       hit_system,round_system,finisher_system,events,checksum}.py
  content/{schemas,loader,validators}.py
  presentation/{renderer,sprite_renderer,camera,hud,audio,vfx,debug_overlay}.py
  input/{devices,bindings,sampler}.py
  tools/{hitbox_editor,sprite_sheet_builder,replay_viewer}.py
data/{fighters,moves,stages,input,finishers}/
assets/{characters,stages,audio,vfx}/
tests/{unit,simulation,content,replays}/
.run/{Game,Tests,Headless Replay}.run.xml
```

Each move is versioned content rather than special-case code. It specifies startup/active/recovery frames, collision boxes, impulses, cancel windows, hit/block results, audio/VFX cues, and per-hit identifiers. Simulation order is fixed: recognize inputs; transition state; update movement/facing/pushboxes; generate hitboxes; resolve hits with stable tie-breakers; apply results; advance timers; emit presentation events.

## Historical and current technical research

| Reference | Verified lesson | Project application |
|---|---|---|
| [Marvel vs. Capcom 2 developer interview](https://shmuplations.com/marvelvscapcom2/) | Capcom used 2D fighters with 3D backgrounds for player readability, reduced controls to an ergonomic vocabulary, and constrained systems such as assists/wakeups to prevent degenerate play. | Prioritize visible silhouettes and a compact intentional button layout. Build rules and anti-infinite constraints into data before spectacle. |
| [Soulcalibur developer interview](https://shmuplations.com/soulcalibur/) | Motion capture informed weapons and character concepts; substantial animation rework and bespoke character subsystems increased balancing cost. | Use performance reference only as input to original animation. Require new mechanics to fit shared systems and budget their long-term test cost. |
| [Mortal Kombat (1992) overview](https://en.wikipedia.org/wiki/Mortal_Kombat_(1992_video_game)) | Its digitized-sprite production, compact control scheme, palette reuse, and round-ending finishers established a performance-derived 2D pipeline. | Prefer animated 3D-to-sprite work over live performer capture for an original, manageable clay style. Treat finishers as gated round-end scripts. |
| [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) | Variable render time must not change authoritative game timing. | Simulate fighting rules at a 60 Hz fixed tick with an accumulator; render separately. |
| [GGPO](https://www.ggpo.net/) and [GGPO source](https://github.com/pond3r/ggpo) | Rollback requires save/load state, replayable input, and simulation without rendering. | Build deterministic snapshots, input recordings, hashes, and headless replay tests now; do not promise network play until profiled and funded. |
| [Godot finite-state-machine demo](https://github.com/godotengine/godot-demo-projects/tree/master/2d/finite_state_machine) | State enter/exit/update contracts make transitions and interruptions explicit. | Use hierarchical match and fighter state machines with legal transition/cancel tables. |

### Non-negotiable engineering and content checks

- Input commands operate on 10-15 facing-relative deterministic frames, held/pressed/released bits, not raw keyboard callbacks.
- Keep animation selection separate from gameplay state. Animation callbacks cannot authoritatively activate hitboxes.
- Define trades, throws, armor, invulnerability, projectile clashes, and multi-hit behavior through explicit stable rules.
- Add a hitbox viewer, frame advance, input display, content validator, and golden replay tests before producing a large roster.
- Use original source assets; track Blender masters, export settings, licenses, and source provenance. Do not copy fighters, animation, logos, dialogue, UI, or trade dress from reference games.

## Creative and art plan

### Original fighter roster

| Fighter | Satirical focus | Combat identity | Signature prop and finisher concept |
|---|---|---|---|
| Captain Campaign | Civic spectacle and empty promises | Space control, rallies, temporary barricades | Microphone sceptre; a papier-mache ballot avalanche buries the rival and reveals a dazed thumbs-up. |
| Baron Boardroom | Corporate excess | Armored pressure and money-meter risk/reward | Gold briefcase gauntlets; an absurd invoice folds into a shipping crate around the rival. |
| Doctor Broadcast | Attention-driven wellness media | Traps, counterplay, and status misdirection | Ring light and foam syringe; a commercial break turns the rival into a harmless product cutout. |
| General Gravy | Celebrity cooking spectacle | Heavy swings, heat zones, and slow armored attacks | Ceremonial ladle; an oversized recipe card folds the rival into a comic clay dumpling. |
| General Gadget | Tech solutionism | Drones, prototypes, mobility, and malfunction risk | Mini drone swarm; an autonomous cart delivers a harmless pile of cardboard parts and confetti. |
| Influence Oracle | Attention economy | Range control, follower-meter buffs, and selfie teleports | Selfie staff; a phone UI shrinks the rival into a repeatedly tapped “skip ad” button. |

Every concept must have an asset provenance and content-review entry before integration. Project review occurs at concept, first playable, and pre-release gates.

### Asset and animation budgets

- Master assets: Blender `.blend`, editable texture sources, and 16-bit EXR render passes. Use Git LFS or equivalent for large binaries.
- Runtime: sRGB sprites with premultiplied alpha; initial 2048 x 2048 atlases, scaling to 4096 x 4096 only after memory profiling. Use 8 px extrusion and 4 px packing margins.
- Fighter canvas: 1024 x 1024; ground pivot under the lead foot; nominal body height 760 px.
- Per fighter target: about 260 body frames, 90 facial/hand overlays, 80 effects frames, and 20 portraits/icons. Render at 24 fps and play most combat at intentional 12 fps holds; effects may play at 24 fps.
- Required animation groups: locomotion, blocks, hit reactions, knockdown/recovery, throw, six normals, three command normals, three specials, super, taunt, intro/outro, win/lose, and finisher.
- Each attack has a move sheet containing frame counts, hit/hurt/push boxes, cancel windows, VFX/audio event frames, camera notes, and mirroring exceptions.

Use 5-7 parallax stage layers and no gameplay-important stage collision in the initial slice. UI uses high-contrast molded-plastic panels, readable health/meter bars, optional screen-shake reduction, scalable HUD, volume controls, and remappable actions where feasible.

## WBS and execution plan

| WBS | Deliverable | Exit evidence | Owner |
|---|---|---|---|
| 1.0 | Program foundation and compliance | Charter, RACI, risk/decision log, originality matrix | Producer |
| 2.0 | Combat design | Input map, frame-state rules, move-kit templates, balance principles | Combat designer |
| 2.1 | Combat kernel | Fixed-step loop, input buffer, state machine, collision and hit resolution | Gameplay engineer |
| 2.2 | Match/training systems | HUD, rounds, rematch, pause, dummy tools, debug overlays | Gameplay/UI engineer |
| 2.3 | Toolchain | PyCharm configurations, headless replay runner, content validation | Engineering |
| 3.0 | Character content | Six data-driven kits, animation events, boxes, balance documentation | Design + gameplay |
| 3.1 | Art direction | Clay-style guide, palette/lighting/pivot rules, asset naming | Art director |
| 3.2 | Fighter assets | Models, rigs, sprite atlases, VFX, portraits, finisher props | Tech art + animation |
| 3.3 | Environments | One polished stage and one test stage | Environment art |
| 4.0 | Finisher framework | Timeline/camera/event system with skip and cleanup behavior | Gameplay + tech art |
| 4.1 | Finisher content | One reviewed and tested finisher per fighter | Design + animation |
| 5.0 | Audio | Combat/UI/arena cues, mix groups, accessibility controls | Audio |
| 6.0 | Quality and balance | Automated tests, regression replays, test matrix, balance records | QA + combat design |
| 6.1 | Performance and stability | Frame-time/memory captures, defect triage, controller matrix | Engineering + QA |
| 7.0 | Build/readiness | Setup guide, reproducible build, demo checklist, engine decision package | Producer + engineering |

### Prototype iteration plan

Planning estimate: 12-16 weeks for 4-6 dedicated contributors. This is a prototype estimate, not a commercial-release commitment.

| Iteration | Duration | Objective | Exit gate |
|---|---:|---|---|
| 0: Discovery | 2 weeks | Approve product pillars, content boundaries, combat spec, toolchain spike, and source-control rules. | G0: scope and originality process approved. |
| 1: Combat proof | 3 weeks | Two graybox fighters, fixed 60 Hz loop, input buffering, boxes, camera, basic HUD. | G1: responsive local match and initial performance baseline. |
| 2: Pipeline proof | 3 weeks | One complete original fighter, Blender-to-sprite pipeline, one stage, debug tools, finisher framework. | G2: measured production cost and no code rewrite needed for content. |
| 3: Roster alpha | 3-4 weeks | Six fighters, initial VFX/audio, one finisher each, end-to-end local versus. | G3: complete roster is playable and test plan is active. |
| 4: Polish and balance | 2-3 weeks | External playtests, accessibility baseline, performance fixes, regression coverage. | G4: acceptance criteria met and no blocker defect. |
| 5: Prototype exit | 1 week | Demo package, measured metrics, risks, staffing/cost range, engine recommendation. | G5: fund production, change engine, or stop. |

Critical path: combat rules -> deterministic simulation -> shared fighter state/move data -> asset pipeline -> six-fighter integration -> finisher reliability -> balance/stability -> exit review.

## Risks and decision gates

| ID | Risk | Mitigation | Owner |
|---|---|---|---|
| R-01 | Character designs become identifiable as real people. | Distance test and legal/content review at three gates; redesign on failure. | Producer + reviewer |
| R-02 | Pygame cannot meet production needs. | Keep content/contracts engine-agnostic; run Godot/Unity evaluation before G5. | Technical lead |
| R-03 | Clay art costs too much per fighter. | Measure hours for one complete fighter and reuse rigs, materials, VFX, and move templates. | Art director |
| R-04 | Finishers soft-lock match state or disrupt readability. | Shared deterministic timeline, automated cleanup tests, skip behavior, camera review. | Gameplay lead |
| R-05 | Combat is unresponsive or unbalanced. | Fixed tick, frame tools, weekly playtests, golden replays, documented balance changes. | Combat designer |
| R-06 | Controller behavior differs by operating system. | Test an explicit supported device/OS matrix and reconnect behavior before roster alpha. | Engineering |
| R-07 | Content conflicts with intended ratings or distribution. | Establish rating target early; use stylized non-gratuitous effects and review each finisher. | Producer |
| R-08 | Per-character exceptions fragment the codebase. | Require data-driven moves and a technical approval for any new subsystem. | Technical lead |

## Immediate action order

1. Establish the Python environment and PyCharm run, test, and headless-replay configurations.
2. Build two colored-box fighters with fixed ticks, action-bit input, pushboxes, hit/hurt boxes, frame debug, and golden replay coverage.
3. Complete one original fighter and one stage through the Blender-to-sprite import pipeline, including a reusable finisher timeline.
4. Measure performance and asset effort, conduct G1/G2 reviews, and decide whether Pygame remains appropriate through roster alpha.
5. Scale only shared content contracts to all six fighters; no character-specific match-loop branches.
6. Perform playtests, content reviews, and G4/G5 engine/readiness decisions using measured evidence.

# Pygame and 2D game development

Use this reference for every Python/Pygame game, Pygame code review, 2D prototype, educational game, or desktop 2D application built on the Pygame event/rendering stack.

## Establish the runtime

Inspect the repository before choosing APIs. Record the Python version, operating systems, installed distribution and version, display backend, target resolution, packaging method, and input devices. `pygame` and `pygame-ce` both expose the `pygame` import name; do not install, mix, or migrate between them implicitly. Follow the project lockfile and verify behavior against documentation matching the installed distribution.

Use an isolated virtual environment and a reproducible dependency file or lockfile. Resolve assets from a stable application/resource root rather than the process working directory so development and packaged builds behave consistently.

## Architecture

For anything beyond a tiny example, separate:

- application startup, configuration, and shutdown;
- the event loop and input mapping;
- fixed simulation updates and variable-rate rendering;
- scene/state transitions such as boot, menu, play, pause, results, and settings;
- entities/components or domain objects;
- rendering, camera, UI, audio, assets, persistence, and debug tooling.

Keep gameplay rules testable without opening a window or requiring audio. Pass services or state explicitly instead of hiding all behavior in module globals. Use Pygame `Sprite` and `Group` where their lightweight image/rect/update/draw contract helps; they are optional, not a required architecture.

## Main loop and timing

Pump the event queue every frame and handle `QUIT`, focus changes, resizing, and device changes deliberately. Distinguish edge-triggered actions from held input: events are suitable for presses/releases and text entry, while current key/controller state suits continuous movement.

Use `pygame.time.Clock` for frame pacing and elapsed time. For physics, combat, timers, replay, or deterministic behavior, prefer a fixed simulation step with an accumulator and a cap on catch-up work. Render independently where useful. Never make motion depend on an assumed frame count unless the design intentionally uses fixed ticks.

Express velocity and acceleration in units per second. Clamp or subdivide large elapsed times after pauses or stalls so objects do not tunnel or timers skip uncontrollably.

## Display and coordinates

Choose a logical game resolution separately from the actual window when pixel consistency or multi-resolution support matters. Render to a logical `Surface`, then scale or letterbox to the window with an explicit integer-scaling policy for pixel art. Translate mouse/touch coordinates back into logical space and reject letterbox regions correctly.

Maintain clear coordinate spaces: world, camera/view, screen, UI, tile, and physics. Centralize conversions. Use `Vector2` or floating-point world positions for smooth movement, while deriving `Rect` positions for rendering and broad-phase collision; repeated integer-only motion can lose subpixel movement.

Convert loaded opaque images with `convert()` and alpha images with `convert_alpha()` after the display is initialized. Cache loaded and transformed assets. Do not reload files, fonts, rescale images, rotate source surfaces repeatedly, or recreate masks in the hot loop without measured justification.

## Sprites, animation, and rendering

Represent animation with named clips containing frames, durations, looping behavior, and events. Advance by elapsed simulation time, preserve the entity anchor when frames change size, and define what happens when a non-looping clip completes.

Keep update order intentional: input → decisions/AI → movement/physics → collision resolution → consequences → animation/camera → render. Use layers or explicit draw order for predictable composition. Clear the full frame by default; use dirty rectangles only after profiling shows that partial redraw helps the actual target.

For large maps, draw only visible tiles and entities. Pre-render stable chunks or layers when beneficial, but invalidate caches correctly when the world changes.

## Collision and movement

Choose the cheapest collision model that matches gameplay:

- `Rect` overlap for broad phase, arcade hitboxes, and most tile movement;
- circles or custom geometric tests when shape semantics require them;
- `Mask` overlap only for cases where pixel-level silhouettes materially improve play.

Separate visual bounds, hurtboxes, hitboxes, interaction zones, and terrain collision. Resolve movement one axis at a time for simple axis-aligned tile collision, or use swept/substepped methods for fast objects. Define slopes, one-way platforms, moving platforms, ladders, knockback, and corner tolerance explicitly rather than letting incidental rectangle behavior decide them.

If mask collision is used, cache masks and recreate them when the underlying sprite image changes. Never create a mask inside every pairwise collision test. Use spatial partitioning, tile neighborhoods, or another broad phase before expensive checks when entity counts grow.

## Camera, tilemaps, and UI

Camera behavior is gameplay. Specify target, dead zone, look-ahead, bounds, smoothing, shake composition, zoom, and snap rules. Avoid smoothing formulas that change feel with frame rate.

For tilemaps, define tile size, map orientation, layers, object metadata, collision data, asset paths, and coordinate convention. Validate missing tiles and malformed custom properties. Keep render layers distinct from collision/navigation data.

Build UI with its own layout and focus/navigation model. Support keyboard, mouse, and controller where claimed. Test text scaling, long strings, resolution changes, focus visibility, remapping, pause behavior, and readable contrast. Do not tie UI hit detection to unscaled window coordinates when rendering through a logical surface.

## Audio and input

Initialize or preconfigure the mixer before loading sound when latency and format matter. Use `Sound` objects for short effects and the music stream for long tracks. Assign channels or groups for priorities, concurrency limits, ducking, and volume categories. Handle missing audio hardware gracefully when the game should still run.

Map physical controls to game actions. Store remappable bindings separately from gameplay code. Handle controller connection/disconnection, duplicate devices, dead zones, analog normalization, and focus loss. Do not assume one controller or one keyboard layout.

## Saving, testing, and debugging

Version save data and write it atomically using a temporary file plus replacement. Store user data in a platform-appropriate writable location, never beside packaged read-only assets. Validate ranges and missing fields; do not unpickle untrusted save data.

Test pure gameplay logic with ordinary Python tests. For Pygame-dependent tests, use controlled fixtures and a headless video/audio configuration when supported, then separately smoke-test a real window and packaged build. Seed randomness for repeatable simulations. Add debug overlays for FPS/frame time, collision shapes, entity counts, camera bounds, coordinates, and current scene.

Profile before optimizing. Measure update and render phases separately, inspect entity-pair growth, cache conversions and transforms, avoid per-frame allocations in demonstrated hot paths, and test the packaged build on the slowest supported hardware.

## Packaging and delivery

Keep resource discovery compatible with the chosen packager. Include fonts, sounds, images, maps, licenses, and platform runtime dependencies explicitly. Build from a clean checkout, launch on a machine without the development environment, test save locations and upgrades, and scan the artifact for accidentally bundled source data or secrets.

For browser/WASM targets, verify the selected Pygame distribution and packager support, restructure blocking loops for the web runtime when required, and test browser audio, storage, input, and asset-loading constraints. Do not claim web compatibility from desktop execution.

## Acceptance evidence

At minimum, run syntax/import checks, automated tests, the real game loop, and a clean packaged-build smoke test when packaging is in scope. Report controls, Python/Pygame versions, supported platforms actually tested, frame target, logical/window resolution, save path, build command, and known limitations.

## Authoritative sources

- Pygame repository, examples, and tests: https://github.com/pygame/pygame
- Pygame documentation: https://www.pygame.org/docs/
- Sprite and collision reference: https://www.pygame.org/docs/ref/sprite.html
- Mask reference: https://www.pygame.org/docs/ref/mask.html
- Pygame Community Edition documentation when that distribution is selected: https://pyga.me/docs/

Check the installed version before relying on development-branch documentation or newer APIs.

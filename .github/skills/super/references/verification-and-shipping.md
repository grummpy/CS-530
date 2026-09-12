# Verification and shipping

Use this reference for profiling, test strategy, multiplayer, saves, packaging, or release readiness.

## Evidence ladder

Name the strongest evidence actually obtained:

1. Static inspection or compilation.
2. Automated unit or engine test.
3. Editor play mode or simulation.
4. Development build on the target device.
5. Representative playtest or network session.
6. Release configuration on supported hardware.

Never collapse these levels into “tested.” State the engine version, build configuration, device, scenario, duration, and result when they matter.

## Performance

- Define the frame-time budget from the target refresh rate: approximately 33.3 ms at 30 Hz, 16.7 ms at 60 Hz, and 8.3 ms at 120 Hz.
- Measure CPU, GPU, memory, allocations, loading, streaming, and frame-time percentiles on target hardware. Average FPS alone can hide stalls.
- Reproduce a representative scene before profiling. Compare captures before and after a change and account for profiler overhead.
- In Unreal, use Unreal Insights and relevant stat commands; use a frame debugger such as RenderDoc for draw-level faults. In Godot or Unity, use their engine profilers before external profilers.

## Gameplay and persistence

- Convert mechanics into observable tests: input → state transition → feedback → outcome.
- Test keyboard/mouse and each supported controller, remapping, focus loss, pause, resolution/aspect changes, localization expansion, and accessibility settings.
- Version save data. Test new save, round trip, corrupted or truncated input, missing optional fields, and migration from the oldest promised compatible release.
- Separate deterministic simulation tests from presentation. Seed randomness when repeatability is required.

## Multiplayer

- Document authority, ownership, replication frequency, prediction, reconciliation, and trust boundaries for each important action.
- Exercise latency, jitter, loss, reconnects, host departure, duplicate requests, ordering, and incompatible client versions.
- Never infer internet-scale readiness from multiple local editor windows. Use packaged clients and a real server path before claiming multiplayer verification.

## Release gate

A releasable candidate should have a reproducible clean build, known dependency and asset licenses, no embedded secrets, bounded logs and telemetry, recoverable saves, crash reporting appropriate to the project, verified controls, and a smoke test on every claimed platform. Store certification and console testing require the relevant current platform documentation and authorized SDK access.

## Authoritative starting points

- Unreal profiling overview: https://dev.epicgames.com/documentation/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine
- Godot performance guidance: https://github.com/godotengine/godot-docs/blob/master/tutorials/performance/general_optimization.rst
- Unity verified repositories and testable samples: https://github.com/Unity-Technologies

Consult current engine documentation before giving version-specific commands.

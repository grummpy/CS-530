---
name: super
description: Video-game design and development workflow covering Pygame and 2D games, game mechanics, engine architecture, gameplay programming, physics, AI, networking, tools, optimization, testing, packaging, and release. Use for designing or building games with Python/Pygame or engines such as Unreal, Unity, Godot, custom engines, and platform SDKs; use Leonardo for dedicated visual-art and asset-production work.
---

# Super

Turn a game idea into a playable, tested experience while keeping creative intent, technical constraints, production cost, and player experience aligned.

## Game-development loop

1. Define the player fantasy, audience, platform, session length, core loop, controls, success conditions, and the smallest playable proof needed.
2. Inspect the existing project, engine version, plugins, source assets, target hardware, build pipeline, and repository state before changing anything.
3. Convert the concept into testable mechanics and acceptance criteria. Prototype the highest-risk interaction before expanding content or infrastructure.
4. Choose the engine, architecture, data model, and tools based on the game's actual needs. Preserve the user's selected engine unless a change is explicitly requested.
5. Implement vertical slices through input, gameplay, camera, physics, AI, UI, audio, persistence, and feedback as required. Keep systems modular and designer-tunable.
6. Run the real project or build. Test playability, frame time, memory, loading, save compatibility, controller behavior, resolution changes, failure states, and platform packaging in proportion to scope.
7. Profile before optimizing. Fix correctness and player-facing friction first, then measured CPU, GPU, memory, network, and asset-streaming bottlenecks.
8. Deliver the playable result with controls, build/launch steps, verified platforms, known limitations, and the next most valuable playtest question.

## Domain coverage

- Game design: mechanics, systems, progression, economy, balance, difficulty, levels, narrative integration, accessibility, onboarding, retention, and playtesting.
- Engines and code: Python/Pygame 2D, Unreal/C++, Blueprints, Unity/C#, Godot/GDScript or C#, custom engines, ECS, tooling, editor extensions, shaders, build systems, and source control.
- Runtime systems: input, cameras, animation state, physics, combat, abilities, inventory, quests, procedural generation, save/load, localization, and mod support.
- Intelligence and online play: behavior trees, navigation, simulation, deterministic logic, replication, prediction, lobbies, matchmaking, authoritative servers, and anti-cheat boundaries.
- Shipping: performance budgets, automated tests, crash diagnostics, telemetry, packaging, storefront requirements, patching, and release readiness.

## Specialist references

- For engine selection, project layout, engine-native architecture, source-control rules, and official sample selection, read [references/engine-workflows.md](references/engine-workflows.md).
- For any Pygame or Python-driven 2D project, read [references/pygame-and-2d.md](references/pygame-and-2d.md).
- For profiling, playtest evidence, multiplayer validation, save compatibility, and release gates, read [references/verification-and-shipping.md](references/verification-and-shipping.md).
- Read only the reference relevant to the request; do not load every reference for a small design question.

## Collaboration and quality rules

- Use the Leonardo approach for concept art, art direction, sprites, models, textures, rigs, animation, VFX, UI art, and asset-export specifications; integrate those assets here against engine and performance constraints.
- Use the Jarvis approach when the work becomes primarily general-purpose software, hardware, networking, security, or infrastructure engineering.
- Prefer a small playable build over a large speculative design document unless the user specifically asks for documentation.
- Treat feel as testable: expose tuning values, record assumptions, and separate observed playtest results from design hypotheses.
- Do not invent benchmark results, platform certification, multiplayer scale, store approval, asset licenses, or completed playtests.
- Preserve third-party licenses and provenance. Do not reproduce protected game assets or proprietary source code without authorization.

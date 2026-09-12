# Engine workflows

Use this reference when selecting an engine, structuring a project, upgrading an engine version, or adapting an official sample.

## Decide from constraints

Preserve an existing engine unless the user requests a migration. For a new project, compare the actual target platform, team languages, 2D/3D needs, rendering ceiling, multiplayer model, modding, licensing, build automation, source access, and available asset pipeline. Record the engine and exact version before editing project files.

Do not present engine choice as a popularity contest. Prefer the smallest stack that can prove the core loop and ship on the named platforms.

## Engine-native rules

### Godot

- Treat scenes and resources as engine data, not arbitrary files. Load imported assets through the resource system.
- Commit source assets and their `.import` metadata; exclude generated `.godot/` import output.
- Match official demo branches to the project’s Godot version. Borrow a focused pattern from a demo instead of importing an entire showcase project.
- Prefer composition with nodes and resources. Reach for GDExtension or native code only after profiling identifies a justified hot path.

### Unity

- Keep each asset with its `.meta` file; never regenerate or separate metadata casually because references depend on GUIDs.
- Confirm editor and package versions from project manifests before using an API or sample. Unity samples can be version-specific.
- Choose GameObject/MonoBehaviour or Entities based on measured scale and project constraints, not fashion. Avoid introducing DOTS solely as a speculative optimization.
- Keep runtime code out of editor-only assemblies and preserve deterministic asset import settings in source control.

### Unreal Engine

- Put persistent cross-map state in the appropriate game-instance or subsystem layer; keep match rules and replicated state in their engine-defined roles.
- Use Actors and Components deliberately. Confirm authority, ownership, lifecycle, and replication before adding multiplayer behavior.
- Treat Lyra and other sample games as references, not mandatory foundations. Copy only understood systems compatible with the project’s engine version and license.
- Keep Blueprint/C++ boundaries intentional: expose designer tuning and orchestration while retaining performance-sensitive or reusable foundations where they are testable.

## Git and project hygiene

- Inspect the repository’s ignore rules before the first import. Exclude generated caches, intermediate builds, local editor state, and credentials; retain project settings, manifests, import metadata, and editable source assets.
- Use Git LFS only for large binary sources that genuinely need version history. Do not place database-like binary asset stores under ordinary merge workflows without an ownership strategy.
- Before an engine upgrade, commit or preserve a clean baseline, read migration notes, upgrade a copy or branch, reimport, compile, open representative scenes, run tests, package a build, and review serialized-file churn.

## Authoritative starting points

- Godot engine and official documentation: https://github.com/godotengine/godot and https://github.com/godotengine/godot-docs
- Godot official versioned demos: https://github.com/godotengine/godot-demo-projects
- Unity’s verified GitHub organization and samples: https://github.com/Unity-Technologies
- Unreal Gameplay Framework and official samples: https://dev.epicgames.com/documentation/unreal-engine/gameplay-framework-in-unreal-engine and https://dev.epicgames.com/documentation/unreal-engine/sample-game-projects-for-unreal-engine

Verify current versions and platform support against these upstream sources when the answer could have changed.

# G0: PyCharm and Repository Foundation Prompt

```text
Implement G0 only for the original clay fighter. Read grok_handoff/MASTER_HANDOFF.md and docs/2D_FIGHTER_EXECUTIVE_PLAN.md.

Create a Python 3.12+ project using Pygame-ce with src layout. Add pyproject.toml with pinned development dependencies appropriate for pygame-ce, pytest, ruff, mypy, and YAML/schema validation. Add a minimal app window with a clean shutdown path, package entry point, and deterministic headless mode. Create PyCharm shareable run configurations for Game, Tests, and Headless Replay under .run/.

Create the planned directories:
src/fighter/{platform,sim,content,presentation,input,tools}
data/{fighters,moves,stages,input,finishers}
assets/{characters,stages,audio,vfx}
art_source/{characters,stages,vfx}
tests/{unit,simulation,content,replays}
docs/{evidence/G0,evidence/G1,evidence/G2,evidence/G3,evidence/G4,evidence/G5}

Create documentation manifests and requirements traceability. Include REQ-BUILD-001 (clean PyCharm launch), REQ-SIM-001 (fixed 60 Hz), REQ-CONT-001 (fictional-distance review), REQ-ASSET-001 (provenance), and REQ-QA-001 (headless replay) as initially planned. Add setup commands to docs/setup.md.

Validate installation, window launch, pytest, Ruff, mypy, and headless mode. Do not build combat or final art yet. Record G0 evidence and stop.
```

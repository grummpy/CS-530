# Requirements traceability

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| REQ-BUILD-001 | Python package launches headless. | `python -m fighter --headless --dump-hash --ticks 180` | Pass |
| REQ-COMBAT-001 | Fixed-tick, integer-only combat state. | `sim/state.py`, `sim/match.py`, deterministic replay digest | Pass |
| REQ-COMBAT-002 | Two local keyboard players can move and attack. | `presentation/app_loop.py` | Implemented; runtime smoke pending Pygame-ce |
| REQ-ROSTER-001 | Six original fictional fighter profiles exist. | `data/fighters/*.yaml` | Pass |
| REQ-CONTENT-001 | No real-person or third-party-game content. | `docs/originality_matrix.md` | Pass by source review |
| REQ-ASSET-001 | Blender sprites and cinematic exports available. | Asset inventory | Deferred: source assets were not supplied |

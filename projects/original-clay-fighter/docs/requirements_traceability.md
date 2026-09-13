# Requirements traceability

| ID | Requirement | Evidence | Status |
|---|---|---|---|
| REQ-BUILD-001 | Python package launches headless. | `python -m fighter --headless --dump-hash --ticks 180` | Pass |
| REQ-COMBAT-001 | Fixed-tick, integer-only combat state. | `sim/state.py`, `sim/match.py`, deterministic replay digest | Pass |
| REQ-COMBAT-002 | Two local keyboard players can move and attack. | `presentation/app_loop.py` | Implemented; runtime smoke pending Pygame-ce |
| REQ-ROSTER-001 | Fighter profiles and asset manifests resolve through the content loader. | `data/fighters/*.yaml` | Pass |
| REQ-CONTENT-001 | Character asset provenance and approved visual bibles are recorded. | `docs/asset_provenance.md` | Baseline recorded; per-file manifest deferred to Cycle 2 |
| REQ-ASSET-001 | Blender sprites and cinematic exports available. | Cycle 1 tracked inventory | Pass: four Blender masters, runtime frame libraries, 12 MP4 previews, and 360 finisher PNG frames are tracked |
| REQ-C1-001 | Baseline inventory identifies current roster, stages, media, tests, and release gaps. | `docs/evidence/CYCLE_1_BASELINE.md` | Pass |
| REQ-C1-002 | Documentation records actual audio codec and available media. | `docs/audio_cue_sheet.md`, `docs/asset_provenance.md` | Pass |
| REQ-C1-003 | Delivery platform, hardware floor, and release authority are stated for planning. | `docs/evidence/CYCLE_1_BASELINE.md` | Provisional; requires Cycle 2 approval |
| REQ-C1-004 | Immediate work is prioritized without authorizing implementation. | `docs/COMMERCIAL_READINESS_AUDIT.md` | Pass |

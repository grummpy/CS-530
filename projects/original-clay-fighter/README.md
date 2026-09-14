# Papier Parade (Original Clay Fighter)

Local, two-player 2D clay-style fighting-game prototype.
Python 3.12+ and Pygame-ce. Designed to run and debug from PyCharm.

Character and media provenance is tracked in project documentation. The project
owner selects the character and parody direction for this private prototype.

## Current gate

The playable combat foundation is being completed in this repository. See
[`docs/STATUS.md`](docs/STATUS.md) for verified gate evidence and known limits.

## Quick start

See [docs/setup.md](docs/setup.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m fighter
pytest
```

## Release verification

Package resources are installed beneath `fighter.resources`; the runtime never
depends on repository-relative `assets/` or `data/` paths. Create reproducible
artifacts and provenance with:

```bash
python -m pip install --require-hashes -r requirements/dev.lock
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) python scripts/build_release.py
python scripts/verify_artifacts.py
```

`artifacts/` contains `SHA256SUMS`, build metadata, and a CycloneDX SBOM.
The `Package quality` workflow performs the same checks plus a clean wheel
install, SDL-dummy smoke test, uninstall, and remnant-import check.

## Release-candidate process

The current release-candidate disposition, evidence checklist, external beta
forms, balance matrix, defect triage, support, and rollback procedure are in
[`docs/CYCLE_10_RELEASE_CANDIDATE_READINESS.md`](docs/CYCLE_10_RELEASE_CANDIDATE_READINESS.md).
The current status is no-go pending external Windows target-floor
installed-package smoke and human external playtest evidence.

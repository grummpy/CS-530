# Setup

## Prerequisites

- Python 3.12 or newer
- Git
- PyCharm Professional or Community (optional but targeted)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --require-hashes -r requirements/dev.lock
pip install -e . --no-deps
```

## Run

- Game: `python -m fighter`
- Headless Replay: `python -m fighter --headless --dump-hash --ticks 180`
- Tests: `pytest`

## Package and dependency quality

Release builds use the committed hash-locked requirement files. Build a wheel
and sdist with `SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) python
scripts/build_release.py`, then run
`python scripts/verify_artifacts.py`. This writes artifact SHA-256 checksums,
build metadata, and a CycloneDX SBOM under `artifacts/`. Install the wheel in a
fresh virtual environment with the runtime lock before approving a release.

## Controls and settings

All windowed input travels through semantic actions before the fixed-tick
simulation adapter. Keyboard defaults are P1 arrow keys for movement, `Z/X/C`
for light/medium/heavy attacks, `V` for special, and `B` for throw. P2 uses
`W/A/S/D` and `J/K/L/I/U`; a connected controller uses D-pad, buttons
`0–4` for combat, and buttons `7/8/9` for pause/back/confirm. Menus support
arrows or D-pad with Enter/controller confirm. Settings are stored outside the
installation in the user configuration directory and can be changed from the
Settings menu, including a capture-based P1-light remap. Every menu button also
supports mouse hover and left-click activation; right-click performs Back.
Versus mode uses a CPU opponent. Choose Easy, Medium, or Hard on the fighter
selection screen. A match is first to two round wins; click or press Enter on a
round result to continue.

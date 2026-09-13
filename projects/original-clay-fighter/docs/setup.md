# Setup

## Prerequisites

- Python 3.12 or newer
- Git
- PyCharm Professional or Community (optional but targeted)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

- Game: `python -m fighter`
- Headless Replay: `python -m fighter --headless --dump-hash --ticks 180`
- Tests: `pytest`

## Controls and settings

All windowed input travels through semantic actions before the fixed-tick
simulation adapter. Keyboard defaults are P1 `A/D/W/S`, `F/G/H/J/T` and P2
arrows plus keypad `1/2/3/0/5`; a connected controller uses D-pad, buttons
`0–4` for combat, and buttons `7/8/9` for pause/back/confirm. Menus support
arrows or D-pad with Enter/controller confirm. Settings are stored outside the
installation in the user configuration directory and can be changed from the
Settings menu, including a capture-based P1-light remap.

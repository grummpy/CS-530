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

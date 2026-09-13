# Papier Parade (Original Clay Fighter)

Local, two-player, original-fiction 2D clay-style fighting-game prototype.
Python 3.12+ and Pygame-ce. Designed to run and debug from PyCharm.

This is original satirical fiction. It does not depict or imitate real people,
companies, political groups, copyrighted fighters, game assets, logos, voices,
quotes, or trade dress.

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

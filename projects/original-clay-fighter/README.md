# Papier Parade (Original Clay Fighter)

Local, two-player, original-fiction 2D clay-style fighting-game prototype.
Python 3.12+ and Pygame-ce. Designed to run and debug from PyCharm.

This is original satirical fiction. It does not depict or imitate real people,
companies, political groups, copyrighted fighters, game assets, logos, voices,
quotes, or trade dress.

## Current gate

**G5 — Measured sandbox perf.** Sim 50.8 µs/tick; dummy 1080p flip ~1.5 ms.
Physical 1080p panel FPS is not claimed. See docs/engine_recommendation.md.

Post-G5: local login screen, placeholder WAV foley, Blender atlas contract,
pooled VFX, distinct silhouettes. Physical 1080p panel still unmeasured.

Full history lives locally at commit `d59b5b2`. Shell `git push` from the sandbox
cannot send username/password. Push from a machine logged in as `grummpy`.

## Quick start

See [docs/setup.md](docs/setup.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m fighter
pytest
```

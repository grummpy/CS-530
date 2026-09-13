# G3 content-authority report — 2026-09-13

## Delivered

Combat initialization now compiles the four playable fighter profiles, move
files, and box files into frozen typed definitions. The simulation uses those
definitions for move duration, active frames, hitboxes, damage, hitstun,
special charge requirements, and Tech Billionaire Armor Mode values. The
generic graybox kit remains available only when `graybox_rival` is explicitly
selected; unknown or incomplete fighter packages are rejected.

The common normal values were recorded in the existing four authored move
files to replace their former match-loop constants. This is data integration,
not a Cycle 4 kit or mechanic expansion.

## Validation

Run in the committed `.release-venv` on 2026-09-13:

| Command | Result |
| --- | --- |
| `.release-venv/bin/python -m pytest` | Pass — 9 tests |
| `.release-venv/bin/ruff check src tests` | Pass |
| `.venv/bin/python -m mypy src` | Project limitation — fails with 39 strict-typing diagnostics in the Pygame presentation layer; the changed content/simulation surfaces pass targeted mypy |
| `.release-venv/bin/python -m fighter --headless --ticks 180 --dump-hash` | Pass — `635f443e8e000e6ac7fa036511b6b2abfaa5f688ee972b8bf422f7aa53788d6d` |
| `.release-venv/bin/python -m fighter --smoke` | Pass — deterministic hashes for seeds 1, 7, and 42 |

Focused tests cover immutable/rejected content selection, authored special
startup/active-frame timing, hitbox range, and authored special damage. No
character art was changed.

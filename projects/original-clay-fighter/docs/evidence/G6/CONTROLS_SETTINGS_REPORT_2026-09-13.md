# Cycle 6 Controls, Settings, and Onboarding Report

## Delivered

- Semantic keyboard/controller action routing is isolated in
  `fighter.platform.input`; only its per-tick `InputFrame` adapter reaches the
  deterministic kernel.
- Controller identity, assignment, safe assigned-device disconnect pause, and
  reconnect assignment are presentation lifecycle state.
- Focus loss/minimize, manual pause, resume, reset, menu navigation, training
  input display, and move list remain outside the simulation boundary.
- Settings use a versioned allowlist, bounded physical tokens, same-context
  conflict rejection, default recovery diagnostics, and temporary sibling
  replacement in user configuration storage (`XDG_CONFIG_HOME`/`APPDATA` or
  `~/.config`), never the install tree.
- High-contrast focus and reduced effects are controlled by one accessibility
  preferences model.

## Scope held

No Cycle 7 audio work, Cycle 8 finisher-performance work, Cycle 9 packaging
work, or character-art work was added. Cycle 5 assets remain untouched.

## Validation

Run with the project Python 3.12 `.venv`:

```text
.venv/bin/python -m pytest
.venv/bin/python -m ruff check src tests
.venv/bin/python -m mypy src/fighter
.venv/bin/python -m fighter --headless --dump-hash --ticks 180
```

Actual results:

```text
36 passed in 0.11s
All checks passed!
```

The project-wide type command still reports the pre-existing
`presentation/audio.py` `object`-annotation errors documented by Cycle 5;
Cycle 6's new modules pass scoped strict typing:

```text
Success: no issues found in 5 source files
```

The headless replay remained deterministic:

```text
bad005e9e8277fe57c9ccf44eaa11609e7275c05d9fc5058c55e70a818af4e8b
```

The three-seed smoke matrix completed with hashes `bad005e9…`, `98878b3b…`,
and `01e4d37e…`.

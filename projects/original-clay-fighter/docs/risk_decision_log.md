# Risk and decision log

| ID | Decision / risk | Disposition |
|---|---|---|
| D-01 | Keep Python/Pygame-ce for the prototype. | Retained; it has the smallest integration cost for the current local slice. |
| R-01 | Missing committed presentation/audio masters. | Open; replace procedural placeholders only with original, documented assets. |
| R-02 | Windowed test cannot run in the current Python 3.11 environment without Pygame-ce. | Open; run `pip install -e '.[dev]'` on Python 3.12+ before release. |
| R-03 | Full frame data, blocking, special moves, finishers, controller mapping, and balance are not complete. | Open; required before G3/G4 claims. |

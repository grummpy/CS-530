# Risk and decision log

| ID | Decision / risk | Disposition |
|---|---|---|
| D-01 | Keep Python/Pygame-ce for the prototype. | Retained; it has the smallest integration cost for the current local slice. |
| R-01 | Missing committed presentation/audio masters. | Open; replace procedural placeholders only with original, documented assets. |
| R-02 | Windowed test cannot run in the current Python 3.11 environment without Pygame-ce. | Open; run `pip install -e '.[dev]'` on Python 3.12+ before release. |
| R-03 | Full frame data, blocking, special moves, finishers, controller mapping, and balance are not complete. | Open; required before G3/G4 claims. |
| D-02 | Cycle 1 scope is baseline reconciliation, verification planning, and requirements preparation only. | Approved and complete; Cycle 2 implementation remains blocked pending approval. |
| D-03 | Planning release target is Windows 10/11 x64 desktop at 1280x720, 60 FPS. | Provisional; sponsor must approve the store and minimum hardware in Cycle 2. |
| R-04 | Source-build validation cannot be reproduced in this workspace because Python 3.12 project dependencies are unavailable. | Open; reproduce in a clean Python 3.12 environment before any gate claim. |
| R-05 | Packaged-build, controller, audio-device, and low-spec finisher-transition evidence is absent. | Open; Cycle 2 must define measurable requirements and Cycle 6-9 must implement and verify them. |

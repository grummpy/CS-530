# Release readiness review

## Current increment

The playable Pygame-ce build contains four original clay-style fighters, three
arena backgrounds, title and selection screens, local or CPU opponents, music,
HUD meters, blocking, special moves, and 12 winner-versus-opponent finisher
frame sequences. The presentation uses deliberately exaggerated clay comedy
and non-realistic splat effects.

## Evidence

The release environment is Python 3.12 with Pygame-ce 2.5.8. The project was
installed from a clean virtual environment. `pytest`, `ruff check`, `mypy`,
headless replay, CLI smoke, CLI performance, SDL dummy video/audio asset-load,
and a scripted title-to-match Pygame smoke are the required verification set.
Music is stored as 48 kHz, stereo, signed-16-bit PCM WAV because Pygame-ce does
not support the previously supplied ADPCM WAV format.

## Known limitations

This is a desktop prototype, not a packaged store release. It has keyboard
controls only, no settings/pause/menu focus system, no remapping, and no
separate one-shot combat sound effects. Windowed gameplay is designed at
1280x720. The finisher still loads its frame sequence when a match ends, which
can cause a brief transition delay on slower machines.

## Next release gate

Add fixed-step rendering decoupling, keyboard/controller menu navigation,
pause/settings, one-shot impact/audio cues, a packaged-build smoke test, and
recorded desktop playtest evidence.

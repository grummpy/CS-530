# Match soundtrack cue sheet

All runtime tracks are 48 kHz stereo signed-16-bit PCM WAV files. The game chooses a deterministic track from the match seed at match start, loops it at 55% music volume, and silently continues when audio initialization or loading fails.

| Cue ID | Runtime file | Trigger | Duration | Mix / acceptance state |
|---|---|---|---:|---|
| MUS-001 | `battle_of_the_kitchen.wav` | Match start | 2:32 | PCM format recorded; in-game listening pending. |
| MUS-002 | `mark_zuckerberg_in_battle.wav` | Match start | 2:04 | PCM format recorded; in-game listening pending. |
| MUS-003 | `neon_warrior.wav` | Match start | 3:13 | PCM format recorded; in-game listening pending. |
| MUS-004 | `make_america_great_again.wav` | Match start | 1:43 | PCM format recorded; in-game listening pending. |
| MUS-005 | `hoosiers_stand_together.wav` | Match start | 1:35 | PCM format recorded; in-game listening pending. |

Before release, audition each track in the Pygame-ce target build for clipping, loop transition, codec support, and volume balance. Add a menu selector and music mute/volume controls before claiming player music selection.

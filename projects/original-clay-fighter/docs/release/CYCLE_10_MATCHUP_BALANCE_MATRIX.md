# Cycle 10 matchup and balance test matrix

**Status:** execution pending. This is a test plan, not a balance result.
**Candidate:** 0.1.0 installed wheel identified on each run sheet.

The current values in [`../balance_change_log.md`](../balance_change_log.md)
are implementation defaults, not playtest-validated balance. Do not change
combat values while executing this matrix; file findings through triage.

## Required matrix

Run each directed matchup twice: once with the row fighter as Player 1 and
once as Player 2. Use the row fighter's default stage for the first run and a
different available stage for the second. Use a human-vs-human session when
possible; otherwise mark CPU-assisted runs as supplemental and do not use them
alone for release balance approval.

| Row fighter \ Opponent | Master Chef | The Tech Billionaire | Rhinestone Angel | Mr. President |
| --- | ---: | ---: | ---: | ---: |
| Master Chef | Training/control | MC vs TB ×2 | MC vs RA ×2 | MC vs MP ×2 |
| The Tech Billionaire | TB vs MC ×2 | Training/control | TB vs RA ×2 | TB vs MP ×2 |
| Rhinestone Angel | RA vs MC ×2 | RA vs TB ×2 | Training/control | RA vs MP ×2 |
| Mr. President | MP vs MC ×2 | MP vs TB ×2 | MP vs RA ×2 | Training/control |

This produces 24 directed competitive runs. Add one mirror/control match per
fighter (four total) to distinguish player-skill variance from character
asymmetry. Repeat any run interrupted by a defect, retaining both the
interrupted record and defect ID.

## Per-run data form

```text
Run ID: __________  Session/tester IDs: __________  Candidate SHA-256: ______
Row fighter/side: __________  Opponent/side: __________  Stage: ____________
Input devices: __________  Human-vs-human? [ ] Y [ ] N  CPU supplemental? [ ] Y [ ] N
Winner: __________  Rounds played: __________  Approximate match duration: __
Decisive moves/states observed (including block, throw, special, armor, KO):
_____________________________________________________________________________
Could either player consistently answer the decisive tactic? ________________
Perceived fairness (1 very unfair — 5 even): P1 ___ P2 ___
Readability/control/finisher concerns: _____________________________________
Defect ID(s), video/log link(s), and retest need: __________________________
Facilitator synthesis: _____________________________________________________
```

## Review criteria

Flag a matchup for investigation when two or more independent human sessions
identify the same repeatable, low-counterplay tactic; when a fighter's
decisive advantage persists after side rotation; or when a controls,
readability, or stability defect determines an outcome. A win-rate difference
alone is not a balance conclusion at this sample size.

The balance lead must summarize sample counts, human/CPU separation, repeated
tactics, confounding defects, and disposition. Any proposed tuning requires a
new candidate and re-execution of affected rows.

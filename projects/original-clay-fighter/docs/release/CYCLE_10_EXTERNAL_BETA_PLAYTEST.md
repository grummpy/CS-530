# Cycle 10 external beta playtest plan, forms, and templates

**Status:** planned; no external sessions have been performed or inferred.
**Scope:** usability, stability, match flow, controller/keyboard behavior,
finisher comprehension, and perceived matchup fairness of the installed
0.1.0 candidate. This plan is not evidence of completed playtesting.

## Plan

| Item | Plan |
| --- | --- |
| Candidate | Record wheel filename, SHA-256, build metadata revision, and install command before every session. |
| Cohort | At least 8 external adult testers: at least 4 keyboard-first and 4 controller-first; include novice and fighting-game-experienced players. Obtain consent before recording feedback. |
| Environments | Capture OS/version, CPU/GPU/RAM, display resolution, input device, audio-device state, and whether the session uses the approved Windows target-floor hardware. Do not collect serial numbers or account names. |
| Sessions | One 30–45 minute orientation/play session per tester, then one 15-minute focused retest if a release-blocking issue is corrected. Use local two-player and CPU modes where available. |
| Core route | Launch installed package; title/menu navigation; settings; selection; one keyboard match; one controller match if available; pause/focus loss/reconnect where available; KO/finisher/skip/results/rematch; clean exit and relaunch. |
| Balance route | Run the [matchup matrix](CYCLE_10_MATCHUP_BALANCE_MATRIX.md), rotating side/order and stage. Record wins, round duration, decisive mechanics, and perceived fairness without changing game values. |
| Evidence | Assign anonymized tester IDs (for example, `BETA-01`); retain completed forms, logs, screenshots/video only with consent, and defect IDs. |
| Stop rule | Stop a session on crash, data-loss concern, repeated input loss, seizure/motion-sickness concern, or tester withdrawal. Preserve evidence, thank the tester, and triage before resuming. |

## Facilitator script

> You are testing a pre-release local fighting-game prototype. Please describe
> what you expect and what surprises you. Do not share passwords or private
> information. You may stop at any time. We are testing the game, not you.
> Please report crashes, controls problems, unclear screens, and moments that
> feel unfair; do not try to work around a crash repeatedly.

Do not coach combat decisions unless the tester asks for control help. Record
observations separately from the tester's words. Do not promise a fix or a
release date.

## Tester consent and environment form

```text
Session ID: __________  Date/time (with zone): __________
I agree to provide voluntary pre-release feedback. I may stop at any time.
Feedback recording permitted? [ ] notes only [ ] screenshots [ ] video/audio
Tester initials or anonymous ID: __________

Candidate wheel filename/SHA-256: ___________________________________________
Build metadata source revision: _____________________________________________
OS/version: __________________ CPU: __________________ RAM: _________________
GPU: __________________ Display resolution/refresh: _________________________
Input tested: [ ] keyboard  [ ] controller (type only): _____________________
Audio device state: [ ] available [ ] unavailable  Target-floor device? [ ] Y [ ] N
Install completed: [ ] Y [ ] N  Launch completed: [ ] Y [ ] N
```

## Session observation and tester feedback form

```text
Session ID: __________  Facilitator: __________  Start/end: ________________

Route results (Pass / Fail / Not tested; link defects):
Title/menu ____  Settings ____  Keyboard match ____  Controller match ____
Pause/focus/device recovery ____  KO/finisher/skip ____  Results/rematch ____
Exit/relaunch ____  Crash observed? ____  Defect IDs: _______________________

Tester statements (quote or concise paraphrase):
1. What was clear or enjoyable? ____________________________________________
2. What was confusing or difficult? ________________________________________
3. Did either fighter or move feel unfair? Describe matchup/side/stage: _____
4. Were controls, readability, audio, or effects uncomfortable? ____________
5. Would you play another match? Why/why not? ______________________________

Facilitator observations (facts only): ______________________________________
Consent to retain submitted feedback: [ ] Y [ ] N
```

## Invitation and follow-up templates

**Invitation**

> You are invited to a voluntary 30–45 minute private beta session for
> *Papier Parade*, a local 2D fighting-game prototype. We will ask you to use
> a pre-release installed package and give candid feedback. Participation is
> optional; you may stop at any time. We collect only an anonymous tester ID,
> broad device details, and feedback you choose to provide. Reply with your
> availability and whether you prefer keyboard or controller.

**Issue acknowledgement**

> Thank you for reporting `DEFECT-ID`. We recorded the candidate hash,
> environment, and reproduction details. The report is under triage; this
> acknowledgement does not promise a fix or release date. Please do not
> repeatedly retry a crash or share private data in follow-up.

**Completion thank-you**

> Thank you for the beta session. Your feedback is recorded under `BETA-ID`
> and will be reviewed with other anonymous results. No further action is
> needed unless the playtest lead requests a focused retest and you opt in.

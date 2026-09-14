# Cycle 10 final go/no-go decision record

**Record date:** 2026-09-13
**Candidate:** `original-clay-fighter` 0.1.0
**Candidate metadata:** source revision
`980f4cbcdb7e5b2a5c61cc761c5523863b1a1911`; see
[`artifacts/build-metadata.json`](../../artifacts/build-metadata.json).
**Decision:** **NO-GO**

## Evidence reviewed

| Evidence | Finding |
| --- | --- |
| Cycle 8 finisher/performance report | Local macOS/Python 3.12 automated qualification completed; raw measurements are headless only. |
| Cycle 9 packaging/quality report | Local reproducibility, package lifecycle, lint, typing, and 52-test evidence retained. |
| Artifact metadata and checksums | 0.1.0 wheel and sdist metadata/SHA-256 values are retained. |
| Cycle 10 readiness checklist | Release process, beta forms, balance matrix, triage, support, and rollback procedures are now defined. |

## Open blockers

1. **Windows target-floor installed-package smoke is external pending evidence.**
   No retained run proves the installed package on the planned Windows 10/11
   x64 i5-8250U/Ryzen 3 3200U, 8 GB RAM, UHD 620/Vega 3-class target.
2. **Human external playtests are external pending evidence.** No completed
   external beta sessions substantiate usability, controller/keyboard behavior,
   stability, finisher readability, or gameplay perception.
3. **Matchup/balance matrix is unexecuted.** Current combat values remain
   implementation defaults rather than externally observed balance evidence.

No test result, external session, target-floor result, defect count, or
approval is claimed by this record beyond the retained Cycle 8/9 evidence.

## Decision rationale

The local automated/package evidence is necessary but does not establish
target-floor installed-package behavior or real-player readiness. The missing
external evidence is release-critical; therefore artifact distribution outside
controlled internal evaluation is not authorized.

## Conditions to reconsider

The decision authority may reconsider only after RC-05 through RC-09 in the
[readiness checklist](../CYCLE_10_RELEASE_CANDIDATE_READINESS.md) have
evidence links and pass dispositions, all blocker/critical defects are closed,
and the exact approved artifact hashes are recorded below.

```text
Decision authority: ____________________  Date/time: ____________________
Approved candidate filename(s)/SHA-256: __________________________________
Windows target-floor evidence link: _______________________________________
External beta summary link: ______________________________________________
Balance synthesis link: __________________________________________________
Open accepted risks/support wording: ______________________________________
Go / No-go (circle one): ____________________
Rollback contact and controlled distribution channel: ______________________
```

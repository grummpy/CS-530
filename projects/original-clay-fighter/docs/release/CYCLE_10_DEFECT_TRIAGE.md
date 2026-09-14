# Cycle 10 defect triage criteria

**Status:** active for candidate evaluation. Severity is based on the observed
installed candidate, not assumptions about source behavior.

## Intake minimum

Every report must contain: defect ID; reporter/session ID; candidate wheel
hash and source revision; OS/environment; input device; exact route and
expected/actual behavior; reproducibility; artifacts/logs if consented; and
the reporter's contact only if they opted in. Remove secrets and unnecessary
personal data before retention.

## Severity and release disposition

| Severity | Criteria | Candidate disposition |
| --- | --- | --- |
| Blocker | Cannot install/launch; crash/hang/data corruption; persistent loss of player input; release artifact integrity/provenance failure; severe safety/accessibility concern; or an issue that prevents the core match route for most users. | Immediate no-go; stop affected testing; fix and requalify. |
| Critical | Repeatable failure of a major route (selection, match, results/rematch, settings), major incorrect match result, frequent loss of controls/audio, or exploit that consistently determines outcomes with no reasonable counterplay. | No-go until resolved or decision authority records an exceptional, time-bounded risk acceptance. |
| Major | Material degradation with a reliable workaround: broken optional controller path, significant readability defect, finisher failure with usable fallback, or repeatable matchup concern needing investigation. | Must be dispositioned; unresolved items require documented acceptance and support wording. |
| Minor | Cosmetic, copy, isolated audio/visual, or low-impact usability issue with no meaningful route impairment. | Track for follow-up; does not block by itself. |
| Observation | Preference, enhancement, or insufficiently reproducible report. | Log for analysis; do not treat as a defect until corroborated. |

## Triage workflow and service targets

1. Acknowledge every external report within two business days using the beta
   acknowledgement template.
2. De-duplicate, sanitize, and classify within two business days of intake.
3. Attempt reproduction on the exact installed artifact; record `reproduced`,
   `not reproduced`, or `insufficient evidence`.
4. Assign owner, severity, affected route, and disposition: `fix`,
   `retest`, `accepted risk`, `deferred`, or `not a defect`.
5. Escalate blocker/critical findings to the decision authority immediately.
6. A fix requires a new candidate hash, targeted retest, and re-evaluation of
   affected release-checklist rows.

## Defect record template

```text
ID: DEF-____  Opened: ____  Reporter/session: ____  Owner: ____
Candidate filename/SHA-256/revision: _______________________________________
Environment and input: ______________________________________________________
Route, steps, expected, actual: ____________________________________________
Reproducibility/rate: _______________________________________________________
Evidence links and consent restrictions: ____________________________________
Severity: [ ] Blocker [ ] Critical [ ] Major [ ] Minor [ ] Observation
Reproduction: [ ] reproduced [ ] not reproduced [ ] insufficient evidence
Disposition: [ ] fix [ ] retest [ ] accepted risk [ ] deferred [ ] not defect
Decision/rationale, retest candidate, and closure evidence: ________________
```

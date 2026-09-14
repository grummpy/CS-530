# Cycle 10 release notes, support, and rollback plan

**Status:** draft operational material; it does not announce a release.
**Release condition:** the [Cycle 10 readiness checklist](../CYCLE_10_RELEASE_CANDIDATE_READINESS.md)
must be approved first.

## Draft release notes — 0.1.0

> **Papier Parade 0.1.0 (release candidate)**
>
> This local two-player clay-style fighting-game prototype includes four
> selectable fighters, three arena backgrounds, local or CPU opponents,
> keyboard/controller input, settings and onboarding screens, music and
> presentation feedback, and winner-versus-opponent finisher sequences.
>
> **Known limitations:** desktop prototype; no store-release approval yet;
> windowed gameplay targets 1280×720; the finisher transition may be slower on
> low-spec machines; external Windows target-floor and external human-playtest
> evidence are still pending. Do not describe this candidate as release-ready
> until the final decision record is go.

Replace “release candidate” only after a go decision, and include the exact
artifact names, version, SHA-256 values, support contact, and confirmed known
issues in the published notes.

## Support plan

| Need | Initial handling | Escalation |
| --- | --- | --- |
| Install/launch | Request candidate hash, OS version, and sanitized launch output; compare the hash to approved metadata. | Blocker if a supported environment cannot install/launch. |
| Controls/audio/display | Collect input-device type, settings route, and concise reproduction steps; never request account credentials or whole home-directory archives. | Major/critical based on route loss and workaround. |
| Gameplay/balance | Record matchup, side, stage, input, tactic, and fairness observation using the matrix form. | Balance lead after triage. |
| Crash/hang | Ask the player to stop retrying, preserve sanitized error output, and provide candidate/environment details. | Immediate blocker/critical assessment. |

The release owner owns first response and the triage lead owns classification.
Publish only a support contact/channel approved by the project owner. Retain
only the minimum information required to reproduce and resolve a report.

## Rollback plan

1. **Trigger:** any blocker; a confirmed critical affecting core play; checksum
   mismatch; or decision-authority instruction.
2. **Contain:** stop distribution, unpublish/withdraw the affected candidate
   from the controlled channel, and mark the release status withdrawn. Do not
   delete retained evidence or overwrite the published hash record.
3. **Communicate:** post a concise notice naming the affected version/hash,
   impact, immediate user action (stop using/revert if applicable), support
   contact, and next update time. Do not speculate on cause.
4. **Recover:** identify a previously qualified artifact only if its hashes
   and evidence remain valid; otherwise issue no replacement until a corrected
   candidate is rebuilt and requalified.
5. **Close:** attach the incident/defect record, withdrawal time, affected
   channels, corrected artifact hash, retest evidence, and decision-authority
   approval to the final decision record.

Because no external release channel or previously approved public artifact is
recorded, the default rollback action today is **do not distribute the
candidate**.

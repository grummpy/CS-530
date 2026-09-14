# Cycle 10 release-candidate readiness checklist

**Record date:** 2026-09-13
**Candidate:** `original-clay-fighter` 0.1.0
**Decision authority:** project owner
**Current disposition:** **NO-GO — evidence collection continues.**

This is a documentation and operational-readiness cycle. It authorizes neither
game-code nor art changes. It reconciles the Cycle 8 and Cycle 9 retained
evidence and defines the evidence required before a release candidate can be
approved for external distribution.

## Baseline reconciled

| Area | Retained evidence | Status |
| --- | --- | --- |
| Finisher lifecycle and fallback | [Cycle 8 report](evidence/CYCLE_8_FINISHER_PERFORMANCE_REPORT_2026-09-13.md): 49 tests, lint, and typing passed on macOS arm64/Python 3.12.14. | Qualified locally |
| Package quality | [Cycle 9 report](evidence/CYCLE_9_PACKAGING_QUALITY_REPORT_2026-09-13.md): reproducible wheel/sdist, package checks, SBOM, 52 tests, lint, and typing passed locally. | Qualified locally |
| Candidate provenance | [`artifacts/build-metadata.json`](../artifacts/build-metadata.json) records 0.1.0, source revision `980f4cbcdb7e5b2a5c61cc761c5523863b1a1911`, hashes, and artifact sizes. | Available |
| Target-floor installed package | No retained Windows target-floor run exists. | **External pending evidence** |
| External gameplay usability/balance | No human external playtest sessions or signed feedback are retained. | **External pending evidence** |

Cycle 8 raw measurements are explicitly headless simulation measurements on
macOS, not rendered target-floor certification. Cycle 9 Linux CI/local package
checks do not replace the Windows target-floor gate.

## Release-candidate checklist

The decision authority must date, link, and initial every row. A blocker makes
the decision no-go; a conditional item requires an explicitly accepted risk.

| ID | Check | Acceptance evidence | Owner | State |
| --- | --- | --- | --- | --- |
| RC-01 | Freeze exact source revision and version. | Git revision, clean-tree confirmation, 0.1.0 version, and candidate identifier recorded. | Release owner | Ready to perform |
| RC-02 | Rebuild and verify candidate. | `build_release.py`, `verify_artifacts.py`, fresh artifact hashes, metadata, and SBOM attached. | Release owner | Ready to perform |
| RC-03 | Re-run automated qualification. | Python 3.12 CI/local logs for Ruff, strict mypy, pytest, installed-wheel lifecycle, headless, and SDL-dummy smoke. | Release owner | Ready to perform |
| RC-04 | Validate artifact integrity. | Published wheel/sdist checksums match the approved metadata and SBOM names/version. | Release owner | Ready to perform |
| RC-05 | Perform installed-package smoke on target floor. | Completed Windows 10/11 x64 i5-8250U or Ryzen 3 3200U, 8 GB RAM, UHD 620/Vega 3-class run sheet, logs, and results. | External Windows tester | **External pending evidence — blocker** |
| RC-06 | Collect external beta playtests. | Completed, consented sessions and defect reports using the [beta plan](release/CYCLE_10_EXTERNAL_BETA_PLAYTEST.md). | Playtest lead | **External pending evidence — blocker** |
| RC-07 | Complete matchup/balance matrix. | Logged samples, reviewer synthesis, and disposition for every required pairing in the [matrix](release/CYCLE_10_MATCHUP_BALANCE_MATRIX.md). | Balance lead | **External pending evidence — blocker** |
| RC-08 | Triage all reported defects. | Every issue classified and dispositioned using the [triage criteria](release/CYCLE_10_DEFECT_TRIAGE.md); no open blocker/critical issue. | Triage lead | Pending RC-05/06/07 |
| RC-09 | Review player-facing communications. | Release notes, support intake, known-issues list, and rollback owner approved per the [release plan](release/CYCLE_10_RELEASE_SUPPORT_ROLLBACK.md). | Release owner | Ready to perform |
| RC-10 | Make and record final decision. | [Decision record](release/CYCLE_10_GO_NO_GO_DECISION.md) signed with evidence links, exceptions, and release/rollback contacts. | Decision authority | No-go |

## Candidate handling rules

1. Treat the candidate as private until RC-01 through RC-10 are complete.
2. Test from a clean installed wheel, never a repository checkout.
3. Preserve raw test logs, screenshots/video where permitted, environment
   details, artifact hash, and tester/session identifier in the release record.
4. Do not collect passwords, account tokens, precise address, or unnecessary
   personal data from beta participants.
5. A candidate rebuild, version change, dependency-lock change, or content
   change invalidates the affected evidence and requires requalification.

## Exit criterion

The project owner may change this record to go only after the three external
pending-evidence blockers are closed, no blocker/critical defect remains, and
the final decision record names the exact artifact hashes approved for release.

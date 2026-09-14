# Cycle 9 Packaging and Quality Briefing

**Status:** Approval required. Current disposition: no-go for distributable package approval.

Cycle 8 validated runtime quality, but no wheel/sdist, package-resource strategy,
CI workflow, clean installed-package test, dependency lock/SBOM, or
version/artifact provenance exists.

| WBS | Deliverable | Required evidence |
|---|---|---|
| 9.1 | Resource-safe wheel/sdist | Isolated installed CLI loads data/assets outside repository paths. |
| 9.2 | CI gate | Python 3.12 build, Ruff, strict mypy, pytest, resource validation, retained reports. |
| 9.3 | Lifecycle qualification | Fresh install, headless and SDL-dummy smoke, clean exit/uninstall/remnant check. |
| 9.4 | Supply-chain controls | Hash-locked dependencies, SBOM, dependency/license inventory. |
| 9.5 | Release artifacts | Single-source version, tag/version check, checksums, build metadata, wheel/sdist/SBOM. |

**Risks:** packaged resource failure and absent CI are high-risk release blockers;
dependency variance, duplicate versions, and unqualified Windows target-floor
hardware remain open.

Approve Cycle 9 only when its scope is limited to package/build/quality systems.
Completion requires CI-generated evidence for every WBS item, a clean installed
package lifecycle, retained artifact contents/checksums/SBOM, and Windows
target-floor package-smoke evidence.

# Cycle 9 packaging and quality report — 2026-09-13

## Implemented scope

- Runtime resources resolve from the installed `fighter.resources` package.
- Builds produce a wheel and sdist with data and media included.
- The release builder normalizes sdist archive metadata using
  `SOURCE_DATE_EPOCH`, permitting byte-for-byte repeatable artifacts.
- `scripts/verify_artifacts.py` validates package contents and writes
  SHA-256 checksums, versioned metadata, and a CycloneDX SBOM.
- `requirements/*.lock` pins dependencies and hashes. The Python 3.12 CI
  workflow runs Ruff, strict mypy, pytest, artifact validation, and a clean
  installed-wheel lifecycle including headless and SDL-dummy smoke checks.

## Local Python 3.12 evidence

Two clean builds with the same source epoch were byte-identical for both
artifacts. The retained build checksums were:

| Artifact | SHA-256 |
| --- | --- |
| Wheel | `4089a2aa27237955ebad8f7a6b41c945fa3244ffce330042b24cb3fd275ecafe` |
| sdist | `39e8bd4925935a2db76a9725839eb9295304a623f55e49f8091eecc79a691616` |

Ruff passed, strict mypy reported no issues, and pytest passed all 52 tests.
A fresh runtime-lock install successfully ran the headless CLI, SDL-dummy
smoke matrix, and installed resource checks; after uninstall, `import fighter`
failed as required.

## Residual release gate

The required Windows target-floor installed-package smoke evidence is not
available from this macOS validation host. The CI workflow provides the
repeatable Linux package qualification; retain an equivalent Windows run
before distributable-package approval.

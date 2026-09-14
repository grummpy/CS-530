"""Verify release artifacts and write reproducible release provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from fighter import __version__


def _sha256(path: Path) -> str:
    return hashlib.file_digest(path.open("rb"), "sha256").hexdigest()


def _members(path: Path) -> set[str]:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            return set(archive.namelist())
    with tarfile.open(path) as archive:
        return {member.name for member in archive.getmembers()}


def _require_members(path: Path) -> None:
    members = _members(path)
    required = (
        "fighter/resource_paths.py",
        "fighter/resources/data/fighters/master_chef.yaml",
        "fighter/resources/assets/characters/master_chef/manifest.json",
    )
    for member in required:
        if not any(name.endswith(member) for name in members):
            raise SystemExit(f"{path}: missing required package resource {member}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--output", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    artifacts = sorted(args.dist.glob(f"original_clay_fighter-{__version__}*"))
    wheel = next((path for path in artifacts if path.suffix == ".whl"), None)
    sdist = next((path for path in artifacts if path.suffix == ".gz"), None)
    if wheel is None or sdist is None:
        raise SystemExit("expected exactly one version-matched wheel and sdist")
    if os.environ.get("GITHUB_REF_TYPE") == "tag" and os.environ.get("GITHUB_REF_NAME") != f"v{__version__}":
        raise SystemExit(f"release tag must be v{__version__}")
    for artifact in (wheel, sdist):
        _require_members(artifact)

    args.output.mkdir(parents=True, exist_ok=True)
    distributions = json.loads(
        subprocess.check_output([sys.executable, "-m", "pip", "inspect"], text=True)
    )["installed"]
    components = [
        {
            "type": "library",
            "name": item["metadata"]["name"],
            "version": item["metadata"]["version"],
            "licenses": [{"license": {"name": item["metadata"].get("license", "UNKNOWN")}}],
        }
        for item in distributions
    ]
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:original-clay-fighter-{__version__}",
        "version": 1,
        "metadata": {"component": {"type": "application", "name": "original-clay-fighter", "version": __version__}},
        "components": sorted(components, key=lambda component: component["name"].lower()),
    }
    (args.output / "sbom.cdx.json").write_text(json.dumps(sbom, indent=2) + "\n", encoding="utf-8")
    metadata = {
        "package": "original-clay-fighter",
        "version": __version__,
        "python": sys.version,
        "source_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "generated_at": datetime.now(UTC).isoformat(),
        "artifacts": [{"name": path.name, "sha256": _sha256(path), "bytes": path.stat().st_size} for path in artifacts],
    }
    (args.output / "build-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (args.output / "SHA256SUMS").write_text(
        "".join(f"{item['sha256']}  {item['name']}\n" for item in metadata["artifacts"]),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

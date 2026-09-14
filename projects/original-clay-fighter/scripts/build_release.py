"""Build release artifacts and normalize sdist archive metadata."""

from __future__ import annotations

import gzip
import os
import subprocess
import sys
import tarfile
from pathlib import Path


def normalize_sdist(path: Path, epoch: int) -> None:
    normalized = path.with_suffix(".normalized")
    with (
        tarfile.open(path, "r:gz") as source,
        normalized.open("wb") as output,
        gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=epoch) as compressed,
        tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as target,
    ):
        for member in source.getmembers():
            member.mtime = epoch
            member.uid = member.gid = 0
            member.uname = member.gname = ""
            member.pax_headers = {}
            target.addfile(member, source.extractfile(member) if member.isfile() else None)
    normalized.replace(path)


def main() -> int:
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", "0"))
    subprocess.run([sys.executable, "-m", "build", "--no-isolation"], check=True)
    for sdist in Path("dist").glob("*.tar.gz"):
        normalize_sdist(sdist, epoch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

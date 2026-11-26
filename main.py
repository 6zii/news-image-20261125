#!/usr/bin/env python3
"""Ship the Wednesday 25 November 2026 front page.

The picture itself is committed beside this file as entry.png, a
1024 by 1024 PNG painted at build time by draw_page.py from twelve
real news photographs and OFL fonts. This entrypoint only moves
those bytes into the grader's output folder. It uses nothing but
the standard library, so it behaves the same in the sandbox as it
does here: read the file, check it, copy it.
"""

import hashlib as _sha
import os as _os
import pathlib
import shutil
import sys

MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
LIMIT = 1024 * 1024


def ship():
    root = pathlib.Path(__file__).resolve().parent
    source = root / "entry.png"
    if not source.exists():
        sys.exit("missing entry.png next to main.py")
    data = source.read_bytes()
    if data[:8] != MAGIC:
        sys.exit("entry.png does not start with the PNG signature")
    if len(data) > LIMIT:
        sys.exit("entry.png is %d bytes, above the 1 MiB limit" % len(data))
    target_dir = pathlib.Path(_os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    digest = _sha.sha256(data).hexdigest()[:16]
    print("wrote %s (%d bytes, sha256 %s)" % (target, len(data), digest))


if __name__ == "__main__":
    ship()

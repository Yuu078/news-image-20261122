#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Copies the pre-rendered poster (entry.png, built by render_atlas.py in this
repository) to the output directory as entry.png. Deterministic: the same
bytes are written on every run.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    got = os.path.getsize(dst)
    want = os.path.getsize(src)
    if got != want:
        print("size mismatch after copy", file=sys.stderr)
        sys.exit(1)
    print("wrote", dst, got, "bytes")


if __name__ == "__main__":
    sys.exit(main())

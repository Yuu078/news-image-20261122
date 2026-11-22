#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122 — ATLAS v3.

Renders the one-page poster in-process (via render_atlas.build) and writes
it to the output directory as entry.png, then verifies the artifact:
1024x1024, at most 1 MiB. The renderer is deterministic (no clock, no
randomness, no network), so two runs of this program produce byte-identical
output files.
"""

import hashlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_atlas  # noqa: E402

MAX_BYTES = 1048576
EXPECTED_SIZE = (1024, 1024)


def render_poster_bytes():
    """Build the poster image and return its PNG encoding as bytes."""
    img = render_atlas.build()
    if img.size != EXPECTED_SIZE:
        raise SystemExit("poster has wrong dimensions: %r" % (img.size,))
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def check_deterministic():
    """Render twice and confirm the PNG bytes are identical."""
    first = render_poster_bytes()
    second = render_poster_bytes()
    if first != second:
        raise SystemExit("renderer is not deterministic")
    return first


def publish(data, out_dir):
    """Write poster bytes into out_dir/entry.png; return the path."""
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    return dst


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    data = render_poster_bytes()
    if len(data) > MAX_BYTES:
        print("poster too big: %d bytes" % len(data), file=sys.stderr)
        return 1
    dst = publish(data, out_dir)
    print("wrote", dst, len(data), "bytes",
          hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())

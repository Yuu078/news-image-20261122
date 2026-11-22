#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122 - ATLAS v4.

Pipeline stages:
  1. render  - build the poster twice via render_atlas_v4.build and demand
               byte-identical PNG output (the renderer is deterministic:
               no clock, no randomness, no network).
  2. verify  - parse the PNG header by hand and enforce the kit gates:
               exactly 1024x1024 and at most 1 MiB.
  3. emit    - write entry.png to MAKEFUN_OUTPUT_DIR when set, otherwise
               next to this script, and report size + sha256.
"""

import hashlib
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_atlas_v4  # noqa: E402

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
REQUIRED_DIMENSIONS = (1024, 1024)
BYTE_LIMIT = 1024 * 1024


def stage_render():
    """Return the poster's PNG bytes, proving determinism on the way."""
    def encode():
        buf = io.BytesIO()
        render_atlas_v4.build().save(buf, format="PNG", optimize=True)
        return buf.getvalue()

    first, second = encode(), encode()
    if first != second:
        raise SystemExit("rendering is not deterministic")
    return first


def stage_verify(png_bytes):
    """Enforce the kit gates straight from the PNG byte stream."""
    if not png_bytes.startswith(PNG_SIGNATURE):
        raise SystemExit("artifact is not a PNG file")
    ihdr = png_bytes[16:24]  # width + height, big-endian, inside IHDR
    dimensions = struct.unpack(">II", ihdr)
    if dimensions != REQUIRED_DIMENSIONS:
        raise SystemExit("wrong dimensions: %r" % (dimensions,))
    if len(png_bytes) > BYTE_LIMIT:
        raise SystemExit("artifact too big: %d bytes" % len(png_bytes))
    return dimensions


def stage_emit(png_bytes):
    """Write entry.png to the output directory; return its path."""
    out_dir = os.environ.get(
        "MAKEFUN_OUTPUT_DIR",
        os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(png_bytes)
    return path


def run():
    png_bytes = stage_render()
    dimensions = stage_verify(png_bytes)
    path = stage_emit(png_bytes)
    digest = hashlib.sha256(png_bytes).hexdigest()
    print("entry.png -> %s" % path)
    print("dimensions %dx%d | %d bytes | sha256 %s"
          % (dimensions[0], dimensions[1], len(png_bytes), digest))
    return 0


if __name__ == "__main__":
    sys.exit(run())

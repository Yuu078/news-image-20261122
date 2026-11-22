#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122 - ATLAS v5.

A PosterJob renders the poster twice through render_atlas_v5, refuses
to ship unless both renders agree byte for byte, inspects the artifact
with Pillow itself (format, dimensions, byte budget), then delivers it
as entry.png into MAKEFUN_OUTPUT_DIR (default: this script's folder).
"""

import hashlib
import io
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image  # noqa: E402

import render_atlas_v5  # noqa: E402

EXPECTED_SIZE = (1024, 1024)
BYTE_BUDGET = 1024 * 1024  # 1 MiB kit gate


class PosterJob:
    """One deterministic build of the Morning Atlas poster."""

    def __init__(self):
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
        self.target = (Path(out_dir) if out_dir
                       else Path(__file__).resolve().parent) / "entry.png"

    @staticmethod
    def _encode():
        buf = io.BytesIO()
        render_atlas_v5.poster().save(buf, format="PNG", optimize=True)
        return buf.getvalue()

    def render_reproducibly(self):
        """Render twice; the kit demands identical bytes on re-runs."""
        first = self._encode()
        second = self._encode()
        if first != second:
            raise SystemExit("poster render is not reproducible")
        return first

    @staticmethod
    def inspect(png_bytes):
        """Verify the artifact against the kit gates via Pillow."""
        with Image.open(io.BytesIO(png_bytes)) as probe:
            if probe.format != "PNG":
                raise SystemExit("artifact format is %r, not PNG"
                                 % (probe.format,))
            if probe.size != EXPECTED_SIZE:
                raise SystemExit("artifact size is %r, expected %r"
                                 % (probe.size, EXPECTED_SIZE))
        if len(png_bytes) > BYTE_BUDGET:
            raise SystemExit("artifact is %d bytes, budget is %d"
                             % (len(png_bytes), BYTE_BUDGET))

    def deliver(self, png_bytes):
        self.target.parent.mkdir(parents=True, exist_ok=True)
        self.target.write_bytes(png_bytes)
        return self.target

    def run(self):
        png_bytes = self.render_reproducibly()
        self.inspect(png_bytes)
        path = self.deliver(png_bytes)
        digest = hashlib.sha256(png_bytes).hexdigest()
        print("delivered %s" % path)
        print("1024x1024 PNG | %.1f KiB | sha256 %s"
              % (len(png_bytes) / 1024.0, digest))
        return 0


def main():
    return PosterJob().run()


if __name__ == "__main__":
    sys.exit(main())

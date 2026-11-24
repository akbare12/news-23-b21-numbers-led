#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with a read-only /bot (this repository) and a
writable /output, so the program must never write next to itself: the only
output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png
"""
import hashlib
import os
import shutil
import struct
import sys


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("FAIL: output is not a PNG", file=sys.stderr)
        return 1
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        print(f"FAIL: expected 1024x1024, got {w}x{h}", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print(f"FAIL: output {len(data)} bytes exceeds 1 MiB", file=sys.stderr)
        return 1
    src_sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
    dst_sha = hashlib.sha256(data).hexdigest()
    if src_sha != dst_sha:
        print("FAIL: sha256 mismatch", file=sys.stderr)
        return 1
    print(f"OK: wrote {dst} ({len(data)} bytes, sha256 {dst_sha[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

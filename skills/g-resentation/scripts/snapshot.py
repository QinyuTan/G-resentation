#!/usr/bin/env python3
"""Snapshot brief.md, outline.md and out/ into versions/vNN-<label>/."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# Windows 控制台默认不是 UTF-8，中文输出会抛 UnicodeEncodeError
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")



def next_index(versions: Path) -> int:
    nums = [int(m.group(1)) for p in versions.iterdir() if p.is_dir() and (m := re.match(r"v(\d+)", p.name))]
    return max(nums, default=0) + 1


def main() -> int:
    ap = argparse.ArgumentParser(description="留一版")
    ap.add_argument("deck_dir", help="deck 文件夹")
    ap.add_argument("label", help="短标签，例如 outline、final、fix-layout")
    args = ap.parse_args()

    deck = Path(args.deck_dir).resolve()
    versions = deck / "versions"
    versions.mkdir(parents=True, exist_ok=True)

    label = re.sub(r"[^a-z0-9\-]+", "-", args.label.lower()).strip("-") or "snap"
    target = versions / f"v{next_index(versions):02d}-{label}"
    target.mkdir(parents=True)

    copied = []
    for name in ("brief.md", "outline.md"):
        src = deck / name
        if src.is_file():
            shutil.copy2(src, target / name)
            copied.append(name)
    out_dir = deck / "out"
    if out_dir.is_dir():
        shutil.copytree(out_dir, target / "out")
        copied.append("out/")

    if not copied:
        target.rmdir()
        print("error: 没有可存的 brief.md / outline.md / out/", file=sys.stderr)
        return 2

    print(f"[OK] {target}")
    print(f"     存入：{', '.join(copied)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

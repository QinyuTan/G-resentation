#!/usr/bin/env python3
"""Create a deck folder with brief.md and outline.md from the skill's templates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Windows 控制台默认不是 UTF-8，中文输出会抛 UnicodeEncodeError
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"


def main() -> int:
    ap = argparse.ArgumentParser(description="新建一份 PPT 项目文件夹")
    ap.add_argument("slug", help="项目短名，全小写英文与连字符，例如 q4-review")
    ap.add_argument("--root", default=".", help="项目根目录，默认当前目录")
    ap.add_argument("--title", default="", help="这份材料的标题")
    ap.add_argument("--small", action="store_true", help="小事档：不建 assets/ 和 versions/")
    ap.add_argument("--force", action="store_true", help="目录已存在时覆盖 brief.md 与 outline.md")
    args = ap.parse_args()

    slug = args.slug.strip()
    if not slug or "/" in slug or "\\" in slug:
        print(f"error: slug 不合法：{slug!r}", file=sys.stderr)
        return 2

    deck = Path(args.root).resolve() / "decks" / slug
    if deck.exists() and not args.force:
        print(f"error: {deck} 已存在，换个 slug 或加 --force", file=sys.stderr)
        return 2

    deck.mkdir(parents=True, exist_ok=True)
    if args.small:
        (deck / "out").mkdir(exist_ok=True)
    else:
        for sub in ("assets/sources", "assets/media", "out", "versions"):
            (deck / sub).mkdir(parents=True, exist_ok=True)

    title = args.title.strip() or slug
    brief_src = ASSETS / "brief-template.md"
    outline_src = ASSETS / "outline-template.md"
    for src in (brief_src, outline_src):
        if not src.is_file():
            print(f"error: 模板缺失：{src}", file=sys.stderr)
            return 2

    brief_dst = deck / "brief.md"
    outline_dst = deck / "outline.md"
    if brief_dst.exists() and not args.force:
        print(f"skip: {brief_dst} 已存在")
    else:
        text = brief_src.read_text(encoding="utf-8")
        brief_dst.write_text(f"# 需求说明：{title}\n\n{text}", encoding="utf-8")
    if outline_dst.exists() and not args.force:
        print(f"skip: {outline_dst} 已存在")
    else:
        text = outline_src.read_text(encoding="utf-8").replace("- **标题**：", f"- **标题**：{title}")
        outline_dst.write_text(text, encoding="utf-8")

    print(f"[OK] {deck}")
    print("下一步：填 brief.md → 写 outline.md → 跑 check_outline.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

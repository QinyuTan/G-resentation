#!/usr/bin/env python3
"""Validate outline.md: page numbering, required fields, and drift against the frozen baseline."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PAGE_RE = re.compile(r"^##\s+P(\d+)\b(.*)$")
FIELDS = [
    "想表达的意思",
    "屏幕文字",
    "数据与来源",
    "图片素材",
    "建议布局",
    "演讲备注",
]
ENTRY_RE = re.compile(r"^\s*(\d+)\.\s*\*\*(.+?)\*\*")


def strip_fences(lines: list[str]) -> list[str]:
    """Drop fenced code blocks so template examples are not parsed as pages."""
    out: list[str] = []
    fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return out


def parse(path: Path) -> tuple[dict, list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = strip_fences(text.splitlines())
    header: dict[str, str] = {}
    for line in lines:
        m = re.match(r"^-\s*\*\*(.+?)\*\*[：:]\s*(.*)$", line.strip())
        if m and not PAGE_RE.match(line):
            header.setdefault(m.group(1), m.group(2).strip())

    pages: list[dict] = []
    current = None
    for line in lines:
        pm = PAGE_RE.match(line.strip())
        if pm:
            current = {"id": f"P{int(pm.group(1)):02d}", "num": int(pm.group(1)), "title": pm.group(2).strip(), "fields": {}}
            pages.append(current)
            continue
        if current is not None:
            fm = ENTRY_RE.match(line)
            if fm:
                current["fields"][fm.group(2).strip()] = fm.group(1).strip()
    return {"header": header, "pages": pages}, text.splitlines()


def main() -> int:
    ap = argparse.ArgumentParser(description="检查逐页稿编号与字段")
    ap.add_argument("deck_dir", help="deck 文件夹，例如 decks/q4-review")
    ap.add_argument("--baseline", help="冻结基线 outline.md，默认自动找 versions/v01-outline/outline.md")
    args = ap.parse_args()

    deck = Path(args.deck_dir).resolve()
    outline = deck / "outline.md"
    if not outline.is_file():
        print(f"error: 找不到 {outline}", file=sys.stderr)
        print("下一步：先建一份材料，再回来检查", file=sys.stderr)
        print(f'  python3 "{Path(__file__).resolve().parent / "new_deck.py"}" {deck.name} --root "{deck.parent}"', file=sys.stderr)
        return 2

    doc, raw = parse(outline)
    pages = doc["pages"]
    problems: list[str] = []

    if not pages:
        problems.append("没有解析到任何页面：每页应为 `## P01 标题`，编号从 P01 起连续排")
    else:
        nums = [p["num"] for p in pages]
        if nums != list(range(1, len(nums) + 1)):
            problems.append(f"页码不连续或乱序：{[f'P{n:02d}' for n in nums]}")
        for p in pages:
            if not p["title"]:
                problems.append(f"{p['id']} 缺标题")
            for f in FIELDS:
                if f not in p["fields"]:
                    problems.append(f"{p['id']} 缺字段：{f}")

    status = doc["header"].get("状态", "")
    baseline = Path(args.baseline) if args.baseline else deck / "versions" / "v01-outline" / "outline.md"
    if baseline.is_file():
        base_ids = [p["id"] for p in parse(baseline)[0]["pages"]]
        now_ids = [p["id"] for p in pages]
        if base_ids and base_ids != now_ids:
            problems.append(
                "页码与冻结基线不一致（增删页需用户点头，并记录原编号对应关系）：\n"
                f"  冻结：{base_ids}\n  现在：{now_ids}"
            )
    elif status.startswith("已冻结"):
        problems.append("状态已是冻结，但缺少 versions/v01-outline/outline.md 基线，先留版再继续")

    if problems:
        print("发现问题：")
        for item in problems:
            print(f"  - {item}")
        if any("基线" in p for p in problems):
            print(f'\n下一步：python3 "{Path(__file__).resolve().parent / "snapshot.py"}" "{deck}" outline')
        return 1

    print(f"[OK] {len(pages)} 页，编号连续，六个字段齐全；状态：{status or '未标注'}")
    for p in pages:
        print(f"  {p['id']} {p['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

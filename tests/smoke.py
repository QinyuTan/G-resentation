#!/usr/bin/env python3
"""End-to-end smoke test: build a deck, prove the freeze gate blocks, unblock it, re-check.

Runs the same three scripts a user would. Exits non-zero on any unexpected result.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "g-resentation"
SCRIPTS = SKILL / "scripts"

FIXTURE = """
## P01 冒烟测试页

1. **想表达的意思**：验证脚本可用
2. **屏幕文字**：冒烟测试
3. **数据与来源**：无
4. **图片素材**：待补充
5. **建议布局**：居中
6. **演讲备注**：无
"""


def run(script: str, *args: str) -> int:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
    ).returncode


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        if run("new_deck.py", "smoke", "--root", tmp) != 0:
            print("FAIL: new_deck 没能建出项目")
            return 1

        deck = Path(tmp) / "decks" / "smoke"
        outline = deck / "outline.md"
        text = outline.read_text(encoding="utf-8")
        text = text.replace("- **状态**：草稿", "- **状态**：已冻结")
        text = text.split("---")[0] + FIXTURE
        outline.write_text(text, encoding="utf-8")

        if run("check_outline.py", str(deck)) != 1:
            print("FAIL: 标了冻结却没有基线，机检应该拦下来")
            return 1

        if run("snapshot.py", str(deck), "outline") != 0:
            print("FAIL: snapshot 没能留版")
            return 1

        if run("check_outline.py", str(deck)) != 0:
            print("FAIL: 留版之后机检应该通过")
            return 1

    print("PASS: 建项目 → 冻结拦截 → 留版 → 复检，四个环节都符合预期")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

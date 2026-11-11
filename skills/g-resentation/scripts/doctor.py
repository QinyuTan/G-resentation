#!/usr/bin/env python3
"""First-run self check for G-resentation.

Prints a readable status table and one next command. Optional tools missing is a
warning, never a blocker: the skill still works without them.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Windows 控制台默认不是 UTF-8，中文输出会抛 UnicodeEncodeError
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL_DIR / "scripts"
ASSETS = SKILL_DIR / "assets"

OPTIONAL = [
    ("frontend-slides", "npx skills add vercel-labs/agent-skills", "HTML 演示"),
    ("guizang-ppt-skill", "在技能市场搜 guizang-ppt 安装", "HTML 演示的风格包"),
    ("ppt-master", "npx skills add hugohe3/ppt-master", "可编辑 PPTX"),
    ("imagegen", "在技能市场搜 imagegen 安装", "整页出图"),
]

rows: list[tuple[str, str, str]] = []  # (level, item, detail)
fatal = 0
warn = 0


def add(level: str, item: str, detail: str) -> None:
    global fatal, warn
    rows.append((level, item, detail))
    if level == "FAIL":
        fatal += 1
    elif level == "WARN":
        warn += 1


def check_python() -> None:
    v = sys.version_info
    if v >= (3, 10):
        add("OK", "Python", f"{sys.executable}  {v.major}.{v.minor}.{v.micro}")
    else:
        add("FAIL", "Python", f"需要 3.10 以上，当前 {v.major}.{v.minor}。装一个新版本后再跑")


def check_templates() -> None:
    missing = [p.name for p in (ASSETS / "brief-template.md", ASSETS / "outline-template.md") if not p.is_file()]
    if missing:
        add("FAIL", "模板文件", f"缺少 {', '.join(missing)}；技能包不完整，重新装一次")
    else:
        add("OK", "模板文件", "brief-template.md / outline-template.md 都在")


def check_scripts() -> None:
    broken = []
    for name in ("new_deck.py", "check_outline.py", "snapshot.py"):
        path = SCRIPTS / name
        if not path.is_file():
            broken.append(f"{name} 缺失")
            continue
        try:
            r = subprocess.run([sys.executable, str(path), "--help"], capture_output=True, timeout=30)
            if r.returncode not in (0, 2):
                broken.append(f"{name} 启动失败")
        except Exception:
            broken.append(f"{name} 启动失败")
    if broken:
        add("FAIL", "脚本", "；".join(broken))
    else:
        add("OK", "脚本", "new_deck / check_outline / snapshot 都能启动")


def skill_roots() -> list[Path]:
    roots = []
    env = os.environ.get("SKILLS_HOME")
    if env:
        roots.append(Path(env))
    home = Path.home()
    roots += [home / ".agents" / "skills", home / ".chengxiaobang" / "skills"]
    roots += [Path.cwd() / "skills", Path.cwd() / ".agents" / "skills"]
    seen, out = set(), []
    for r in roots:
        try:
            key = r.resolve()
        except Exception:
            continue
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def find_skill(name: str) -> str | None:
    for root in skill_roots():
        cand = root / name
        if (cand / "SKILL.md").is_file():
            return str(cand)
    return None


def check_optional() -> None:
    for name, install, purpose in OPTIONAL:
        hit = find_skill(name)
        if hit:
            add("OK", f"可选 · {name}", f"{purpose}  已安装")
        else:
            add("WARN", f"可选 · {name}", f"{purpose}  未安装，需要时执行：{install}")


def check_ppt_master_deps() -> None:
    if not find_skill("ppt-master"):
        return
    missing = [m for m in ("pptx", "yaml", "pathops", "uharfbuzz") if importlib.util.find_spec(m) is None]
    if missing:
        add("WARN", "ppt-master 依赖", f"当前 Python 缺 {', '.join(missing)}；走 PPTX 路线前执行：pip install -r <PPT_MASTER_DIR>/requirements.txt")
    else:
        add("OK", "ppt-master 依赖", "python-pptx / PyYAML / skia-pathops / uharfbuzz 都能导入")


def check_writable() -> None:
    try:
        with tempfile.NamedTemporaryFile(dir=Path.cwd(), prefix=".g-resentation-", suffix=".tmp", delete=True):
            pass
        add("OK", "当前目录", f"{Path.cwd()} 可写，项目会建在这里的 decks/ 下")
    except Exception as e:
        add("FAIL", "当前目录", f"不可写（{e.__class__.__name__}）；换一个有权限的目录再跑")


def disp_width(text: str) -> int:
    """Terminal display width: CJK and fullwidth characters take two cells."""
    w = 0
    for ch in text:
        code = ord(ch)
        wide = (
            0x1100 <= code <= 0x115F
            or 0x2E80 <= code <= 0xA4CF
            or 0xAC00 <= code <= 0xD7A3
            or 0xF900 <= code <= 0xFAFF
            or 0xFE30 <= code <= 0xFE6F
            or 0xFF00 <= code <= 0xFF60
            or 0xFFE0 <= code <= 0xFFE6
        )
        w += 2 if wide else 1
    return w


def pad(text: str, width: int) -> str:
    return text + " " * max(1, width - disp_width(text))


def print_report() -> None:
    width = max(disp_width(r[1]) for r in rows) + 3
    line = "=" * (width + 62)
    print("G-resentation 自检\n" + line)
    for level, item, detail in rows:
        print(f"[{level:<4}] {pad(item, width)}{detail}")
    print(line)
    ok = sum(1 for r in rows if r[0] == "OK")
    print(f"{ok} 项正常 · {warn} 项警告 · {fatal} 项失败\n")

    if fatal:
        print("先修失败项，再往下走。")
        return

    if warn:
        print("警告不影响现在开始；用到对应路线时再补装就行。\n")

    py = "python3" if shutil.which("python3") else "python"
    print("下一步：建第一份材料")
    print(f'  {py} "{SCRIPTS / "new_deck.py"}" my-first-deck --title "我的第一份材料"')
    print("  然后按 QUICKSTART.md 第 2–5 步走，五分钟能看到三页样稿。")


def main() -> int:
    check_python()
    check_templates()
    check_scripts()
    check_optional()
    check_ppt_master_deps()
    check_writable()
    print_report()
    return 2 if fatal else 0


if __name__ == "__main__":
    raise SystemExit(main())

# 参与

这个项目最缺的不是代码，是**真实使用记录**。如果你用它做过一份真材料，比提十个功能都有用。

## 报问题

开 issue 时带上三件事，能省一轮来回：

1. 你当时在做什么（给谁看、什么场合、几页）
2. 走到哪一步卡住了（判档／问需求／逐页稿／选路线／制作／验收）
3. 期望发生什么，实际发生了什么

如果和脚本有关，贴完整命令和输出。

## 改代码

- 脚本只用 Python 标准库，不引入依赖；`python3.10+` 能在 macOS / Linux / Windows 上跑通
- 改完跑一遍本地检查：`python skills/g-resentation/scripts/doctor.py`，再跑 `check_outline.py skills/g-resentation/examples/minimal`
- CI 会验证完整往返：建项目 → 冻结前拦截 → 留版 → 复检通过。别把这条路径改坏
- 文档和代码一起改。改了流程却没改 `SKILL.md` 或 `QUICKSTART.md`，别人会按旧路走

## 改流程

流程上的改动比代码改动重要，提 PR 前先说清一件事：**你是碰到了哪种真实的失败，才要加这一步？** 没有失败案例支撑的步骤，通常是过度设计。

## 同步安装版

如果你本地装了这份技能（`~/.agents/skills/g-resentation`），改完仓库里的副本后同步过去：

```bash
cp -r skills/g-resentation/* ~/.agents/skills/g-resentation/
```

两边不一致时，以上面的仓库版本为准。

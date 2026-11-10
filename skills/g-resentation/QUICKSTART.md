# 五分钟跑通

先看这一段，决定要不要往下走：本技能不画页面，它负责在动手之前把需求问清楚、把页码锁死、把活交给合适的工具、最后验收。装好之后，说一句"我要做一份 XX"就会自动接上。

下面五步都在命令行里。`<SKILL_DIR>` 换成这个技能所在的目录；PowerShell 里把 `"$S/xxx.py"` 写成 `"$S\xxx.py"`。

## 第 0 步 · 自检（30 秒）

```bash
python3 "<SKILL_DIR>/scripts/doctor.py"
```

会看到一张表：

```
[OK  ] Python         D:\...\python.exe  3.12.13
[OK  ] 模板文件       brief-template.md / outline-template.md 都在
[OK  ] 脚本           new_deck / check_outline / snapshot 都能启动
[WARN] 可选 · ppt-master  可编辑 PPTX  未安装，需要时执行：npx skills add hugohe3/ppt-master
...
下一步：建第一份材料
```

`WARN` 不用管，它只表示某条路线暂时走不了。出现 `FAIL` 才需要先修——表里会直接写修法。

## 第 1 步 · 建项目（10 秒）

```bash
S="<SKILL_DIR>/scripts"
python3 "$S/new_deck.py" my-first-deck --title "我的第一份材料"
```

看到 `[OK] .../decks/my-first-deck` 就成功了。目录里多了两份空表：`brief.md` 和 `outline.md`。

内部例会这类"做错了下周还能改"的活，加 `--small`，少建两个目录：

```bash
python3 "$S/new_deck.py" weekly --small --title "周会同步"
```

## 第 2 步 · 填需求（3 分钟）

打开 `decks/my-first-deck/brief.md`，按提示填。最小版本填这六行就够：

```
给谁看：销售负责人
什么场合：部门月度例会，投屏
要他们做什么：认同诊断方向，同意做一个季度试点
看完记住一句话：下滑不是因为报价，而是交付后 90 天没人管
讲多久、几页：15 分钟，5 页
必须出现的内容：流失结构、流失前信号、试点方案
```

不想自己写也可以直接对 AI 说："我要做一份给销售负责人看的续约复盘，例会讲 15 分钟。"它会按大事小事分档来问你，一次问一个。

## 第 3 步 · 出逐页稿（1 分钟）

让 AI 用 `references/prompts.md` 里的 **P1** 写逐页稿，产出落进 `outline.md`。每页七项：标题、想表达的意思、屏幕文字、数据与来源、图片素材、建议布局、演讲备注。

写完跑一次机检：

```bash
python3 "$S/check_outline.py" decks/my-first-deck
```

期望看到：

```
[OK] 5 页，编号连续，六个字段齐全；状态：草稿
  P01 ...
```

报错就按它指出的页码去改，常见两种：页码跳号、某页少了字段。

## 第 4 步 · 冻结（10 秒）

确认内容没问题，把 `outline.md` 顶部的状态改成 `已冻结`，然后存基线：

```bash
python3 "$S/snapshot.py" decks/my-first-deck outline
```

再跑一次 `check_outline.py`，这次要看到 `状态：已冻结` 且退出码为 0。从此页码不许动，增删页必须你点头——后面说"改 P03"永远指得准。

## 第 5 步 · 出三页样稿（看你的路线）

挑最难的三页：封面、信息最多的一页、图表或流程最复杂的一页。

- **HTML 演示**：用 `references/prompts.md` 的 **P3**，配 `frontend-slides` 或 `guizang-ppt`，没装就手写单文件 HTML
- **出图片**：用 **P4**，三张原始分辨率的 PNG
- **可编辑 PPTX**：用 **P6**，配 `ppt-master`

方向确认后再放量，每十页一批。收尾按 `references/checklist.md` 四类验收。

---

## 想先看一份填好的

`examples/minimal/` 里有一份完整示例（五页，通用题材，不含任何真实信息）。直接跑：

```bash
python3 "<SKILL_DIR>/scripts/check_outline.py" "<SKILL_DIR>/examples/minimal"
```

## 卡住了看这里

| 你看到的 | 意思 | 怎么办 |
|---|---|---|
| `python3: command not found` | 没有 Python 或不在 PATH | 换 `python` 或 `py -3`；Windows 上可能是应用商店占位程序，用 `python3 -V` 确认 |
| `error: ... 已存在，换个 slug 或加 --force` | 同名文件夹已存在 | 换名字，或确认要覆盖时加 `--force` |
| `没有解析到任何页面` | 逐页稿还没写，或标题不是 `## P01` 格式 | 照模板写第一页，编号从 P01 起 |
| `状态已是冻结，但缺少基线` | 改了状态没留版 | 跑一次 `snapshot.py <deck> outline` |
| `页码与冻结基线不一致` | 页数被改过 | 先确认是谁改的；增删页需要你同意，同意就重新留版 |
| `ModuleNotFoundError: yaml` | 走 PPTX 路线但 Python 缺依赖 | 在同一个解释器里 `pip install -r <PPT_MASTER_DIR>/requirements.txt` |

## 它不做的事

已经有逐页大纲只求排版、只要美化、只改一页、只转格式——这些直接交给制作工具，不用走这套流程。

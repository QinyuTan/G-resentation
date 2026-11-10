# G-resentation

**做砸的 PPT，问题通常不在排版，在于没人问清楚这份东西给谁看、听完要他们做什么。**

G-resentation 在你的 AI 动手之前先拦住它，把需求问到说不出含糊话，再把页码锁死、把活分给合适的工具、最后按清单验收。名字来自 grill me in presentation。

它不是又一个"输入主题、输出幻灯片"的生成器。它管的是从空白到交得出手之间那段最容易返工的路。

## 它解决的问题

一句话丢给 AI："帮我做个 PPT。"你会拿到四十页，结构是新闻稿式的，每一页都在介绍，没有一页在说服。改到第三版，已经不像你要的东西了。

这不是模型笨。是你没说给谁看、什么场合、听完要他们干什么，AI 只能按平均水平补。补出来的东西，谁也不得罪，也就谁也不打动。

G-resentation 的做法很朴素：**先问，再锁，后做，最后验。**

## 五个停顿

| 停顿 | 你做什么 | 它做什么 |
|---|---|---|
| 判档 | 说一句"这是对外评审"或"内部周会" | 按"错了能不能改回来"分大小活，一句话告知，你可以改判 |
| 问需求 | 回答 8–12 个问题，或者填一张表 | 小事给表，大事一次一问：内容三件事、受众四个维度、交付形态 |
| 定结构 | 看逐页稿，改想要的页 | 每页七项写死（观点、文字、数据来源、素材、布局、备注），编号 P01 起 |
| 看样稿 | 看三页真产物 | 只做最难的三页：封面、信息最多、图表最复杂。网页给能翻的 HTML，图给原始分辨率 PNG，PPTX 给能打开的文件 |
| 验收 | 最后通读一遍 | 内容、画面、操作、备用稿四类逐项过，网页版真开浏览器跑 |

中间只报进度，不逐页请示。一个五十页的活停五十次，三天后你就烦了，最后还是全丢给 AI。

## 两件别人没做的事

**页码冻结。** 逐页稿确认后立刻存基线，P01 就是第一页，增删页必须你点头。附带的脚本会拿当前稿和基线比对——偷偷加一页，当场抓出来。这样"改 P07"永远指得准。

**只认真产物。** 样稿阶段不接受截图。截图看不出缩放溢出、看不出动画卡顿、看不出字被挡住。要么给能打开的文件，要么别说做完了。

## 安装

需要 Python 3.10+。技能本身零依赖，只用标准库。

```bash
git clone https://github.com/QinyuTan/G-resentation.git
cp -r G-resentation/skills/g-resentation ~/.agents/skills/
```

其他 agent 平台的技能目录见各自的文档；`SKILL.md` 的位置就是技能目录。

四个制作工具是可选的，按你选的路线装，缺了就自动降级：

| 工具 | 用途 | 没装怎么办 |
|---|---|---|
| [frontend-slides](https://github.com/) | HTML 演示 | 手写单文件 HTML |
| guizang-ppt | HTML 演示的另一种风格 | 用 frontend-slides 顶上 |
| [ppt-master](https://github.com/hugohe3/ppt-master) | 可编辑 PPTX | 退到 HTML 或出图 |
| imagegen | 整页出图 | HTML 截图导 PNG |

## 五分钟上手

```bash
# 1. 自检，告诉你缺什么、下一步敲什么
python3 skills/g-resentation/scripts/doctor.py

# 2. 建一份材料
python3 skills/g-resentation/scripts/new_deck.py my-deck --title "我的第一份材料"

# 3. 填需求，然后出逐页稿、跑机检
python3 skills/g-resentation/scripts/check_outline.py decks/my-deck

# 4. 确认后冻结，存基线
python3 skills/g-resentation/scripts/snapshot.py decks/my-deck outline

# 5. 出三页样稿，方向对了再放量
```

详细步骤、每步的预期输出、六种常见报错怎么修，见 [QUICKSTART.md](skills/g-resentation/QUICKSTART.md)。

想先看一份填好的：`skills/g-resentation/examples/minimal/`，五页通用题材，可以直接跑机检。

## 里面有什么

```
skills/g-resentation/
├── SKILL.md              主线七步、边界、硬规则
├── QUICKSTART.md         五分钟五步 + 卡点表
├── references/
│   ├── step0.md          分档判据、表格字段、受众四维、逐页稿格式
│   ├── prompts.md        七条按步骤编号的提示词（P1–P7）
│   ├── paths.md          三条路的判据、各路线调用要点
│   └── checklist.md      四类验收、留版时机、交付说明
├── assets/               需求说明与逐页稿空表
├── examples/minimal/     填好的五页示例
└── scripts/
    ├── doctor.py         首次使用自检
    ├── new_deck.py       建项目夹
    ├── check_outline.py  页码连号、字段完整性、与冻结基线比对
    └── snapshot.py       留版
```

## 它不做的事

- 已有逐页大纲只求排版、只要美化、只改一页、只转格式——直接交给制作工具，不用走这套流程
- 不替你做设计判断：风格由制作环节决定，有参考图就给参考图
- 不替你编内容：资料冲突或缺失时它会停下来问，不会猜一个数字填上去
- 不打包任何第三方工具

## 现状

v0.1.0。流程、脚本、提示词都跑通过一份十四页的客户材料（那份材料不在仓库里）。真正的限制是：只有一份真实材料验证过，场景还窄。用着不对劲的地方，欢迎开 issue 说清楚你当时在做什么。

## License

MIT，见 [LICENSE](LICENSE)。

---

## English

**Most bad decks don't fail on layout. They fail because nobody asked who the deck is for and what the audience should do afterwards.**

G-resentation (from *grill me in presentation*) stops your agent before it starts generating. It interviews you until the brief is unambiguous, freezes the page numbers, routes the build to the right tool, and checks the result against a fixed list.

Not another topic-to-slides generator. It owns the part between a blank page and something you can hand to a client.

**Five stops:** classify the job by "can a mistake be undone" → gather requirements (one question at a time, four audience dimensions) → lock a seven-field per-page outline with frozen IDs → build the three hardest pages as real artifacts (openable HTML, full-resolution PNG, working PPTX — never screenshots) → run a four-category acceptance pass.

**Two things others skip:** page IDs are frozen with a stored baseline, so "edit P07" always points at P07 and an added page is caught automatically; and samples must be real products, not screenshots.

**Requirements:** Python 3.10+. Zero runtime dependencies. Three build tools are optional; the flow degrades gracefully without them.

Read [QUICKSTART.md](skills/g-resentation/QUICKSTART.md) — five steps, five minutes.

MIT licensed.

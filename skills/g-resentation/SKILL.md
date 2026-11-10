---
name: g-resentation
display-name: G-resentation
description: 把"要做一份 PPT"变成一条从提问到交付的完整生产流程——grill 出需求与受众、锁死页码、选制作路线、三页样稿、分批产出、验收留版。用户要做演示文稿、幻灯片、汇报材料、deck，或说"做PPT""整理逐页稿""走一遍PPT流程"时使用。只要求把已有大纲直接排版成文件的，交给 frontend-slides、guizang-ppt 或 ppt-master，不要用本技能。
---

# G-resentation

把"要做一份 PPT"变成一条从提问到交付的完整生产流程。名字来自 grill me in presentation：先把你问到说不出含糊话，再动手。

本技能只做编排：问清需求、定结构、选路线、把活交给合适的制作技能、最后验收。它不自己画页面。

第一次用先跑 `python3 "<SKILL_DIR>/scripts/doctor.py"`，它会告诉你缺什么、下一步敲什么；完整上手路径见 `QUICKSTART.md`。

## 边界

- 用：内容还没定稿，要从零做一份演示材料。
- 不用：已有逐页大纲只想排版，或只要美化、改单页、转格式——直接调制作技能。
- 触发优先级：本技能先选路线，再调制作技能。制作技能自己也会宣称能"生成演示文稿"，别让它跳过第 0 步。

## 项目结构

一份活一个文件夹 `decks/<slug>/`，文件名固定，后续每一步只认文件名：

```
decks/<slug>/
├── brief.md      需求说明（第 0 步产出）
├── outline.md    逐页稿（P01、P02…）
├── assets/
│   ├── sources/  核对事实用的原始资料
│   └── media/    真正上页的图、Logo、截图
├── out/          成品
└── versions/     留版
```

小事可以不建 `assets/` 和 `versions/`。

## 脚本

三个脚本只做确定性的事，不代替判断。只用标准库，任何 3.10+ 的 Python 都能跑，不需要额外装包。

`<SKILL_DIR>` 是本技能所在目录的绝对路径，执行前自己替换；下面的命令在 macOS / Linux / Git Bash 通用，PowerShell 把 `"$S/xxx.py"` 写成 `"$S\xxx.py"` 即可。

```bash
S="<SKILL_DIR>/scripts"

python3 "$S/new_deck.py" q4-review --title "Q4 复盘"      # 建项目夹与两份空表
python3 "$S/new_deck.py" weekly-sync --small              # 小事档
python3 "$S/check_outline.py" decks/q4-review             # 页码连号、六字段、与冻结基线比对
python3 "$S/snapshot.py" decks/q4-review outline          # 留版，自动递增 v01、v02…
```

Windows 上 `python3` 可能是应用商店的占位程序，先跑一次 `python3 -V` 确认；不行就换 `python` 或 `py -3`。所有脚本都接受任意一个能用的解释器。

`check_outline.py` 退出码非 0 就先修，别往下走。冻结后再跑一次，它会把与 `versions/v01-outline/` 的页码差异列出来，这正是"改 P07 只认编号"的兜底。

## 外部依赖（可选，按需自装）

本技能只是编排层，不打包任何制作工具。下面四个按你选的路线需要，缺了就走降级：

| 依赖 | 哪条路线用 | 没装怎么办 |
|---|---|---|
| `frontend-slides` | HTML 演示 | 自己写单文件 HTML，或改用下面两条路线 |
| `guizang-ppt-skill` | HTML 演示的另一种风格 | 用 `frontend-slides` 顶 |
| `ppt-master` | 可编辑 PPTX | 退到 HTML 或出图，页面上注明"未生成 PPTX" |
| `imagegen` | 整页出图 | 用 HTML 截图导出 PNG 代替 |

装法都是 `npx skills add <owner/repo>`，具体看各自仓库。缺依赖时如实告诉用户缺哪一条、影响什么，不要假装能出。

`ppt-master` 有一组非标准库依赖（python-pptx、PyYAML、skia-pathops、uharfbuzz 等）。别写死别人的解释器路径，先探测：

```bash
PY=$(command -v python3 || command -v python)
"$PY" -c "import pptx, yaml, pathops, uharfbuzz" 2>/dev/null \
  || echo "缺少依赖：让用户在该 Python 环境里 pip install -r <PPT_MASTER_DIR>/requirements.txt"
```

通过后再跑它的完整性校验 `"$PY" "<PPT_MASTER_DIR>/scripts/attribution_guard.py"`，非零就停，不修不绕过。

## 素材与事实

讲"当下"的内容，不要凭记忆写。装了 `aihot` 技能就用它取最新动态，它是只读公开 API，不需要 Key：

```bash
curl -sL "https://aihot.virxact.com/api/v1/items?mode=selected&window=7d&q=<关键词>&limit=10"
curl -sL "https://aihot.virxact.com/api/v1/hot-topics"
```

- `mode=selected` 是精选池；带 `q` 查询返回空时再用 `mode=all` 试一次，并注明"未进入精选"。
- 抓到的原始响应存进 `assets/sources/`，供后面核对，不进交付文件。
- **页脚只标第三方原始出处**（发布方、报告名、日期），不要整段转述资讯站的摘要，也不要把它的链接当引用。
- 它允许个人与非商业使用；面向客户的商业交付、对外收费或批量再分发，要先按它的条款取得授权，别默认可以用。
- 没装这个技能、或者取数失败，就退到公开搜索或让用户提供资料，并说明数据截至什么时候。

## 流程

### 1. 判档

判据只有一条：**这活做错了能不能改回来。**

对外客户、正式评审、要存档或传播、跨部门交付 → 大活；内部周会、熟人小范围、随时能重做 → 小事。

判完用一句话告知："这活我按大活处理"或"小事，填个表就行"，用户可以改判，然后往下走。

### 2. 问需求（gate）

- 小事：把 `assets/brief-template.md` 给用户填。缺项就按缺口问，不要替他猜。
- 大活：一次问一个问题，先内容、再受众四维、最后形态。问法和话术见 `references/step0.md`。

不管哪档，问完先用三句话复述："这份是给谁看、要他们做什么、看完记住什么。"用户确认后才写 `brief.md`。

### 3. 逐页稿（gate）

按 `references/step0.md` 的七字段写 `outline.md`，每页一个编号，P01 起顺序排。标题写在编号那一行，其余六项往下排。写的时候用 `references/prompts.md` 的 **P1 逐页稿**，把里面 `［ ］` 全部换成 `brief.md` 的真实内容。写完跑 `check_outline.py`，编号不连续、标题或字段缺失都算没写完。

确认后**冻结**：立刻 `snapshot.py <deck> outline` 存基线，页数和编号此后不得改动。增删页必须用户点头，任何重排都要报告"原 P07 → 现 P05"。后面所有"改第几页"只认编号。

### 4. 选路线 + 三页样稿（gate）

先猜后确认：根据 brief 推断一条路，说明理由让用户否决，不要直接问"你要哪种"。判据和调用方式见 `references/paths.md`。

样张必须挑最难的三页：封面、信息最多的一页、图表或流程最复杂的一页。给真产物（能翻的 HTML、能看的 PNG、能打开的 PPTX），不给截图。方向确认才放量。三条路线的 prompt（P3 / P4 / P6）都自带这一步的样稿要求，不用另写。

### 5. 制作

按路线调用对应技能，并拉起对应 prompt：

| 路线 | 用的 prompt | 技能 |
|---|---|---|
| 网页演示 | P3 | `frontend-slides` 或 `guizang-ppt-skill` |
| 出图片 | P4，必要时接 P5 | `imagegen`；P5 走 `ppt-master` |
| 可编辑 PPTX | P6 | `ppt-master` |

有参考图或对视觉要求高，先在 prompt 前加 **P2 拆解风格**；没有参考图就跳过，风格跟着制作技能的默认走。

所有 prompt 里的 `［ ］` 用 `brief.md` 的真实内容替换，留一个都不许发出去。

每十页一批，出完报一句"P11–P20 好了"，不打断节奏，只在某页确实做不出来时停下来问。

`ppt-master` 用之前先确认解释器能导入它要的包，导不进去就让用户自己装它的 `requirements.txt`，不要写死别人的虚拟环境路径：

```bash
PY=$(command -v python3 || command -v python)
"$PY" -c "import pptx, yaml, pathops, uharfbuzz" || echo "缺依赖，见上方外部依赖一节"
```

### 6. 验收 + 留版

按 `references/checklist.md` 四类逐项过。网页版必须用内置浏览器真开一遍，翻页、缩放、断网都要试。哪项不过就用 **P7 单页改稿**，带页编号和截图，一次只改一页；多页同类问题统一说明范围后整份复检。

交付前 `snapshot.py <deck> final` 存一版。

### 7. 交付说明

一句话说清：从哪个文件打开、需要什么运行条件、还有哪些已知限制。

## 硬规则

- 每个检查点只问具体问题（"这三页的方向对不对，哪里不对"），不问"您看怎么样"。
- 不补造事实、数字、案例。资料冲突或缺失时停下来问，不猜。
- 一项要求做不到就明说限制和替代方案，不悄悄降级。
- 同一个问题两轮没改善，先查原因，不继续重复生成。
- 全流程只在样稿和终检停两次；中间不逐页确认。

# 配图怎么改

README 里的图不是 P 出来的，是这个目录下的 HTML 排版后截的图。要改文案、换页面、调版式，改这里再重新渲染就行。

## 文件

| 文件 | 产出 |
|---|---|
| `hero.html` | `../hero-zh.png`、`../hero-en.png`（能力展示：六页代表作 + 数字） |
| `flow.html` | `../flow-zh.png`、`../flow-en.png`（七步流程与三处检查点） |
| `compare.html` | `../compare-zh.png`、`../compare-en.png`（同题对照） |
| `typical-page.html` | `../deck/typical.png`（不加约束时的默认输出形态，对照图左半边） |

中英两版共用一个文件，靠 `?lang=en` 切换，文案在文件末尾的 `L` 对象里。

## 重新渲染

```bash
npm i playwright
npx playwright install chromium

# 六张拼图 + 默认输出样例
node render-figures.js

# 拼图里用到的演示页面缩略图（需要先把 deck 生出来）
node render-deck.js /path/to/deck/index.html ../deck
```

渲染固定以 2 倍像素密度输出：1280 画布得到 2560 宽的 PNG，高分屏和放大看都不糊。别用 1 倍截图替代，字会发虚。

演示页面那一组默认取第 1、3、6、9、11、12、14 页，改 `render-deck.js` 顶部的 `TARGETS` 即可。

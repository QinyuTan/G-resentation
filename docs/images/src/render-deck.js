// 重截演示页面本身（拼图里的缩略图），以 2 倍像素密度
// 用法：node render-deck.js <deck 的 index.html 路径> [输出目录]
const { chromium } = require("playwright");
const { pathToFileURL } = require("url");
const path = require("path");

const deckPath = process.argv[2];
const outDir = process.argv[3] || path.resolve(__dirname, "..", "deck");
if (!deckPath) {
  console.error("用法：node render-deck.js <deck/index.html> [outDir]");
  process.exit(2);
}

const TARGETS = [1, 3, 6, 9, 11, 12, 14];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(pathToFileURL(path.resolve(deckPath)).href, { waitUntil: "load" });
  await page.waitForTimeout(800);

  // 截图前藏掉翻页控件、进度条，并跳过入场动画
  await page.evaluate(() => {
    for (const id of ["controls", "hint", "progress"]) {
      const el = document.getElementById(id);
      if (el) el.style.display = "none";
    }
    const style = document.createElement("style");
    style.textContent = ".reveal{opacity:1!important;transform:none!important;transition:none!important}";
    document.head.appendChild(style);
  });

  let current = 1;
  for (const target of TARGETS) {
    while (current < target) {
      await page.keyboard.press("ArrowRight");
      await page.waitForTimeout(120);
      current++;
    }
    await page.waitForTimeout(350);
    const name = `p${String(target).padStart(2, "0")}.png`;
    await page.screenshot({ path: path.join(outDir, name) });
    console.log(name, "shot");
  }

  await browser.close();
})();

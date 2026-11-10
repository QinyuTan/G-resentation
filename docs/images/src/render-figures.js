// 重新渲染 README 配图：以 2 倍像素密度截取 docs/images/src 下的版式页
// 用法：npm i playwright && npx playwright install chromium && node render-figures.js
const { chromium } = require("playwright");
const { pathToFileURL } = require("url");
const path = require("path");

const SRC = __dirname;
const OUT = path.resolve(__dirname, "..");

const jobs = [
  { file: "typical-page.html", out: "deck/typical.png", width: 1280, height: 720, query: "" },
  { file: "hero.html", out: "hero-zh.png", width: 1280, height: 720, query: "" },
  { file: "hero.html", out: "hero-en.png", width: 1280, height: 720, query: "?lang=en" },
  { file: "flow.html", out: "flow-zh.png", width: 1280, height: 620, query: "" },
  { file: "flow.html", out: "flow-en.png", width: 1280, height: 620, query: "?lang=en" },
  { file: "compare.html", out: "compare-zh.png", width: 1280, height: 720, query: "" },
  { file: "compare.html", out: "compare-en.png", width: 1280, height: 720, query: "?lang=en" },
  { file: "samples.html", out: "samples-zh.png", width: 1280, height: 720, query: "" },
  { file: "samples.html", out: "samples-en.png", width: 1280, height: 720, query: "?lang=en" },
];

(async () => {
  const browser = await chromium.launch();
  for (const job of jobs) {
    const ctx = await browser.newContext({
      viewport: { width: job.width, height: job.height },
      deviceScaleFactor: 2,
    });
    const page = await ctx.newPage();
    const url = pathToFileURL(path.join(SRC, job.file)).href + job.query;
    await page.goto(url, { waitUntil: "load" });
    await page.waitForTimeout(1200);
    await page.screenshot({ path: path.join(OUT, job.out) });
    console.log(`${job.out}  @2x`);
    await ctx.close();
  }
  await browser.close();
})();

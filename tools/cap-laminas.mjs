import { chromium } from "playwright";
import path from "node:path";
const PORT = process.env.IDIE_PORT || 5174;
const slugs = process.argv.slice(3);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 1.5 });
for (const s of slugs) {
  await p.goto(`http://localhost:${PORT}/src/slides/clase-05/${s}.html`, { waitUntil: "networkidle" });
  await p.waitForTimeout(700);
  await p.screenshot({ path: path.join(process.argv[2], `${s}.png`) });
}
await b.close();
console.log("listo");

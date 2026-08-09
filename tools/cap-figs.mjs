import { chromium } from "playwright";
import { readFileSync, readdirSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
const DIR = "public/figures", OUT = "/tmp/s5cap";
mkdirSync(OUT, { recursive: true });
const CSS = `:root{--fig-ink:#111;--fig-muted:#7a8291;--fig-grid:#ccc;--fig-surface:#f2f2f2;
--fig-paper:#fdfdfd;--fig-accent:#c8102e;--fig-navy:#2f6fba;--fig-ok:#1a7f4b;--fig-warn:#a86a00;
--fig-ramp-1:#7ba4d6;--fig-ramp-2:#3a72b8;--fig-ramp-3:#14396c}
body{margin:0;background:#fff;font-family:'IBM Plex Mono',monospace}
figure{margin:0;padding:14px 18px;border-bottom:1px solid #ddd}
figcaption{font-size:13px;color:#c8102e;margin-bottom:6px}
svg{width:940px;height:auto;display:block}`;
const patron = process.argv[2] || "s5-";
const files = readdirSync(DIR).filter((f) => f.startsWith(patron) && f.endsWith(".svg")).sort();
const html = `<style>${CSS}</style>` + files.map((f) =>
  `<figure><figcaption>${f}</figcaption>${readFileSync(path.join(DIR, f), "utf8")}</figure>`).join("");
writeFileSync("/tmp/s5cap/hoja.html", html);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1000, height: 900 }, deviceScaleFactor: 2 });
await p.goto("file:///tmp/s5cap/hoja.html");
const figs = await p.$$("figure");
for (let i = 0; i < figs.length; i++) {
  await figs[i].screenshot({ path: path.join(OUT, files[i].replace(".svg", ".png")) });
}
await b.close();
console.log(`${files.length} figuras capturadas en ${OUT}`);

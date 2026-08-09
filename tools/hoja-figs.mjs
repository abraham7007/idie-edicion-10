import { chromium } from "playwright";
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
const DIR = "public/figures";
const CSS = `:root{--fig-ink:#111;--fig-muted:#7a8291;--fig-grid:#ccc;--fig-surface:#f2f2f2;
--fig-paper:#fdfdfd;--fig-accent:#c8102e;--fig-navy:#2f6fba;--fig-ok:#1a7f4b;--fig-warn:#a86a00;
--fig-ramp-1:#7ba4d6;--fig-ramp-2:#3a72b8;--fig-ramp-3:#14396c}
body{margin:0;background:#fff;font-family:'IBM Plex Mono',monospace;width:1500px}
figure{margin:0;padding:8px 12px;border-bottom:1px solid #ddd}
figcaption{font-size:12px;color:#c8102e}
svg{width:720px;height:auto;display:block}`;
const nombres = process.argv.slice(3);
const files = nombres.map((n) => `${n}.svg`);
const html = `<style>${CSS}</style>` + files.map((f) =>
  `<figure><figcaption>${f}</figcaption>${readFileSync(path.join(DIR, f), "utf8")}</figure>`).join("");
writeFileSync("/tmp/hoja.html", html);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 780, height: 900 }, deviceScaleFactor: 1.5 });
await p.goto("file:///tmp/hoja.html");
await p.screenshot({ path: process.argv[2], fullPage: true });
await b.close();
console.log("hoja:", process.argv[2]);

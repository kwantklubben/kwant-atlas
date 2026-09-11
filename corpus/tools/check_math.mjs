// corpus/tools/check_math.mjs — gate: every math span must render under the site's KaTeX.
//
// Background: display equations only render when both `$$` delimiters sit on their
// own lines. A single-line `$$a=b$$` silently renders INLINE, and a `$` inside math
// (e.g. `\approx\$96.5`) makes remark-math end the span early, leaving a dangling
// backslash that KaTeX rejects — which the reader sees as raw red error text.
//
// Usage:  node corpus/tools/check_math.mjs [--quiet]
// Exit 0 = clean, 1 = spans failed to render.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import katex from "katex";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CONTENT = path.resolve(HERE, "../../content");
const quiet = process.argv.includes("--quiet");

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name === "_legacy") continue; // retired notes are not published
      walk(p, out);
    } else if (e.name.endsWith(".md")) out.push(p);
  }
  return out;
}

// fence contents are code, never math
function maskFences(text) {
  let inFence = false;
  return text
    .split("\n")
    .map((l) => {
      if (l.trimStart().startsWith("```")) return ((inFence = !inFence), "");
      return inFence ? "" : l;
    })
    .join("\n");
}

const problems = [];
let checked = 0;

for (const file of walk(CONTENT)) {
  const text = maskFences(fs.readFileSync(file, "utf8"));
  const rel = path.relative(CONTENT, file).replace(/\\/g, "/");
  const lineOf = (i) => text.slice(0, i).split("\n").length;

  const spans = [];
  let m;
  const displayRe = /\$\$([\s\S]*?)\$\$/g;
  while ((m = displayRe.exec(text))) spans.push([m.index, m[1], true]);
  const rest = text.replace(/\$\$[\s\S]*?\$\$/g, (s) => " ".repeat(s.length));
  const inlineRe = /(?<![\\$])\$([^$\n]+?)\$/g;
  while ((m = inlineRe.exec(rest))) spans.push([m.index, m[1], false]);

  for (const [idx, body, display] of spans) {
    const src = body.trim();
    if (!src) continue;
    checked++;
    try {
      katex.renderToString(src, { displayMode: display, throwOnError: true, strict: false });
    } catch (e) {
      problems.push({
        loc: `${rel}:${lineOf(idx)}`,
        display,
        msg: String(e.message).replace(/\s+/g, " ").slice(0, 90),
        src: src.replace(/\s+/g, " ").slice(0, 90),
      });
    }
  }
}

if (problems.length === 0) {
  console.log(`check_math: OK — ${checked} math spans all render`);
  process.exit(0);
}

console.log(`check_math: ${problems.length} of ${checked} math spans FAIL to render\n`);
const byMsg = {};
for (const p of problems) (byMsg[p.msg] ||= []).push(p);
for (const [msg, items] of Object.entries(byMsg).sort((a, b) => b[1].length - a[1].length)) {
  console.log(`[${items.length}] ${msg}`);
  if (!quiet) for (const it of items.slice(0, 8)) console.log(`     ${it.loc}  ${it.display ? "display" : "inline "}  ${JSON.stringify(it.src)}`);
  if (!quiet && items.length > 8) console.log(`     ... +${items.length - 8} more`);
}
process.exit(1);

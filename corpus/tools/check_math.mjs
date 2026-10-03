// corpus/tools/check_math.mjs — gate: every math span must render under the site's KaTeX.
//
// Parses each page with the same stack the site uses (remark-parse + remark-gfm +
// remark-math), so it sees math exactly where the site does. The previous version
// found `$…$` with regexes and therefore missed the failures that matter most:
//
//   * a `|` inside math in a TABLE row: GFM splits the cell there first, so the
//     formula is cut in two and both halves print as raw LaTeX;
//   * a currency `$` next to math, which pairs with the wrong delimiter;
//   * `\\` in a display block outside an environment (aligned, cases, …): KaTeX
//     renders it as NOTHING, silently joining the lines;
//   * a non-ASCII character KaTeX cannot typeset (€, µ, §): rendered as a blank;
//   * `\\` in inline math: double-escaped LaTeX. `\\%` even comments out the rest.
//
// Reported per source line. Usage:  node corpus/tools/check_math.mjs [--quiet]
// Exit 0 = clean, 1 = something will render wrong.

import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import katex from "katex"
import { unified } from "unified"
import remarkParse from "remark-parse"
import remarkGfm from "remark-gfm"
import remarkMath from "remark-math"
import { visit } from "unist-util-visit"

const HERE = path.dirname(fileURLToPath(import.meta.url))
const CONTENT = path.resolve(HERE, "../../content")
const quiet = process.argv.includes("--quiet")

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name)
    if (e.isDirectory()) {
      if (e.name === "_legacy") continue // retired notes are not published
      walk(p, out)
    } else if (e.name.endsWith(".md")) out.push(p)
  }
  return out
}

const parser = unified().use(remarkParse).use(remarkGfm).use(remarkMath)

// LaTeX left in ordinary text means a math span was broken apart before KaTeX
// saw it. A `$` directly followed by a backslash command, or a bare \frac-style
// command, never occurs in prose.
const STRAY =
  /\$\\[A-Za-z]|\\(?:frac|sum|int|mathbb|mathbf|mathcal|sqrt|sigma|alpha|beta|lambda|varepsilon|partial|left|right|text|hat|bar|tfrac|dfrac)\b/

const problems = []
let checked = 0

for (const file of walk(CONTENT)) {
  const text = fs
    .readFileSync(file, "utf8")
    .replace(/^---\n[\s\S]*?\n---\n/, (fm) => fm.replace(/[^\n]/g, " ")) // blank the frontmatter but keep line numbers
  const rel = path.relative(CONTENT, file).replace(/\\/g, "/")
  const tree = parser.parse(text)

  visit(tree, (node, _i, parent) => {
    const line = node.position?.start.line ?? 0
    const where = `${rel}:${line}`
    if (node.type === "math" || node.type === "inlineMath") {
      const display = node.type === "math"
      const src = node.value.trim()
      if (!src) return
      checked++
      const warnings = []
      try {
        katex.renderToString(src, {
          displayMode: display,
          throwOnError: true,
          strict: (code, msg) => (warnings.push(`${code}: ${msg}`), "ignore"),
        })
      } catch (e) {
        warnings.push(String(e.message))
      }
      // `\\` in INLINE math outside an environment is a line break KaTeX drops,
      // and `\\%` is worse: a break followed by a comment that silently deletes
      // the rest of the formula. Both come from double-escaping, never intent.
      if (!display && /(?<!\\)\\\\/.test(src) && !/\\begin\{/.test(src))
        warnings.push("double backslash in inline math (double-escaped LaTeX?)")
      for (const w of new Set(warnings.map((w) => w.replace(/ at position.*$/s, "")))) {
        problems.push({
          where,
          kind: w
            .replace(/ at position.*$/s, "")
            .replace(/\s+/g, " ")
            .slice(0, 100),
          src: src.replace(/\s+/g, " ").slice(0, 100),
        })
      }
    } else if (node.type === "text" && parent?.type !== "inlineCode" && STRAY.test(node.value)) {
      problems.push({
        where,
        kind: "LaTeX printed as text (math span broken: `|` in a table, or a stray `$`)",
        src: node.value.replace(/\s+/g, " ").slice(0, 100),
      })
    }
  })
}

if (problems.length === 0) {
  console.log(`check_math: OK — ${checked} math spans all render`)
  process.exit(0)
}

console.log(`check_math: ${problems.length} problem(s) in ${checked} math spans\n`)
const byKind = {}
for (const p of problems) (byKind[p.kind] ||= []).push(p)
for (const [kind, items] of Object.entries(byKind).sort((a, b) => b[1].length - a[1].length)) {
  console.log(`[${items.length}] ${kind}`)
  const shown = quiet ? 0 : 50
  for (const it of items.slice(0, shown)) console.log(`     ${it.where}  ${JSON.stringify(it.src)}`)
  if (items.length > shown) console.log(`     ... +${items.length - shown} more`)
}
process.exit(1)

# Kwant-Atlas — Build Method & Template (reusable per-pillar workflow)

> The repeatable method for turning sources into Atlas content. Use this for every pillar / foundations / fundamentals area. Keep it updated as we refine the pattern.

---

## 1. The end-to-end pipeline (per domain)

1. **Corpus research** — identify canonical books + papers, beginner→expert. → `corpus/<domain>.md`
2. **Titles & acquisition** — classify each: 1 HAVE / 2 FREE(download) / 3 SOURCE(paid). → `corpus/titles/<domain>.TITLES.md`
3. **Acquire** — download free items (done); user provides paid items.
4. **Verified deep-read** (for full books / dense sources) — render pages → read text + vision → produce corrected per-chapter knowledge file. → `verified/`
5. **Author** — write topic folders (hub + sub-pages) from verified material, matching the template.
6. **Lockstep maintenance** — update visualizer, diagnostic matrix, pillar hub, README.
7. **Build & verify** — `npx quartz build`, check for broken links, spot-check formulas vs verified source.

---

## 2. The verified deep-read pipeline (how we read a new book)

- `pdftotext` → text dump. For math-dense books, `pdftoppm` → page PNGs for vision reads.
- One subagent per chapter-group: read text (+ vision on formula pages), cross-check every formula against the source, flag/correct errors, write a corrected per-chapter `.md`.
- **Output = authoritative math** for building notes. Never copy formulas from raw text dumps into the Atlas without this cross-check.

---

## 3. The canonical note template (match this byte-for-byte)

Every topic/foundation note:

```
---
title: "…"
tags:
  - <namespace-first-tag>
  - <lowercase-hyphen-tags>
---

**Basic Prerequisites:** [[full/slug|Alias]] (keyword list).

---

### 1. Intuition & Practical Objective
### 2. Mathematical Ground Truth & Derivations
### 3. Computational Implementation   (Python fenced block + print verification)
### 4. Failure Modes & First-Principles Breakdowns   (numbered)
### 5. Canonical Literature & Study References
### 6. Connected Graph Bridges
```

**Wikilinks:** full slug `|` alias, e.g. `[[pillars/03-derivative-pricing/black-scholes-merton-and-feynman-kac|Black-Scholes]]`. In tables use escaped `\|`.
**First tag = namespace:** `pillar-quant-research`, `pillar-algorithmic-hft`, `pillar-derivative-pricing`, `pillar-quant-risk`, `pillar-portfolio-opt`, `pillar-market-making`, `pillar-ml-altdata`, `pillar-quant-dev`, `foundations`, `fundamentals-accounting`.
**Citations:** papers `Author, First & Author, First: *Title*, Journal Vol(Issue), pages (year).` Books `Author(s): *Title*, Publisher, Chapter N (Topic).`

---

## 4. Folder-per-topic structure (the locked model)

```
pillars/03-derivative-pricing/
├── index.md                          # pillar hub
└── <topic-folder>/
    ├── index.md                      # topic hub: overview, lookup tables, links to sub-pages
    ├── 01-introduction.md            # from zero
    ├── 02-math-foundations.md        # derivations
    ├── 03-advanced-models.md         # advanced sections
    └── ...                           # worked math/code examples as needed
```

Topic hub is the entry + source of truth; sub-pages carry depth; a learner follows the hub top-down, an expert jumps via the index.

---

## 5. Lockstep maintenance (MANDATORY)

- **`content/visualizer.html`** — hardcoded `nodes`/`links` arrays. Each new node needs `{id, title, group, path, math, code, intuition, failure}` + graph edges. Without this, new pages are invisible in the D3 graph.
- **`content/index.md`** — diagnostic matrix rows for new failure-mode-heavy topics.
- Pillar **`index.md`** hubs — add new topic folders.
- **`README.md`** — canonical literature + new areas.

---

## 6. Execution model (parallel subagents)

- **Authoring agents** write only their own new `.md` files under a specified path, and report the exact wikilink slugs + node JSON they need registered.
- **One central pass** does all visualizer/index/README edits (avoids merge conflicts).
- Work in **waves** (see Implementation Plan) and run on a **branch** → verify → merge → delete branch.

---

## 7. Quality gates before considering a pillar "done"

- `npx quartz build` completes with no broken wikilinks.
- Every new note has all 6 sections, correct first-tag namespace, no dead links.
- 3–5 formulas per new page spot-checked against its verified source.
- Visualizer shows all new nodes; diagnostic matrix updated.

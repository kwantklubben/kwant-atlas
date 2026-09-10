# Kwant-Atlas — Project State & File Map (handoff 2026-09-09)

> Everything that exists, where it lives, and what's done. Updated as work progresses — keep this current.

---

## 1. Repo & locations

| Path | What it is |
|---|---|
| `~/local-repos/kwant-atlas/` | The public Kwant-Atlas repo (Quartz v4 site, atlas.kwantklubben.com) |
| `.../content/` | The Atlas content: `pillars/01..08/`, `foundations/`, `index.md`, `visualizer.html`, `Inbox.md` |
| `.../corpus/` | Researched source wishlists + titles + handoff |
| `.../corpus/titles/` | Compact acquisition lists (1 HAVE / 2 FREE / 3 SOURCE) per domain |
| `.../corpus/handoff/` | **This handoff package** |
| `~/kwant-atlas-sources/free/<domain>/` | **Downloaded free sources** (252 items, ~363 MB) — outside the public repo |
| `~/GoogleDrive/Investing/_kwant-atlas-extraction/verified/` | 43 **math-verified** per-chapter deep-reads of the 11 textbooks |

---

## 2. What's DONE

### Sources & corpus
- ✅ Deep-read & **math-verified** all 11 textbooks (Shreve I+II, Björk, Hull, Brigo-Mercurio, Glasserman, Tsay, ESL, Hasbrouck, Foucault-Pagano-Roell, Bernstein calculus) — 43 verified per-chapter files.
- ✅ Researched full **corpus wishlists** for all 8 pillars + foundations + fundamentals/accounting (`corpus/*.md`, ~600 verified entries).
- ✅ Built **titles files** with 1/2/3 status per domain (`corpus/titles/`).
- ✅ **Downloaded 252 free sources** to `~/kwant-atlas-sources/free/` (canonical papers + free math books + official specs).
- ✅ Consolidated `MASTER-CORPUS-AND-ACQUISITION.md` (cross-domain priority list).

### Design
- ✅ Aligned on Atlas vision + folder-per-topic content model (see `01-VISION-AND-STRUCTURE.md`).
- ✅ Implemented the **verified deep-read pipeline** (render pages → vision/text read → corrected per-chapter knowledge files) — this is the reusable method for reading new sources.

---

## 3. What's NEXT (the plan)

1. **User delivers the 304 missing paid sources** → drop into a staging folder / Google Drive.
2. **Verify + deep-read the new paid sources** (Pillar 3 set first) using the established pipeline.
3. **Build Pillar 3 to full depth** (folder-per-topic) as the flagship model.
4. **Review together**, then scale the pattern to other pillars + foundations + fundamentals.

## 3b. BUILD PROGRESS (updated 2026-09-10)

**Pillar 3 (flagship) — in progress.**
- ✅ **Deep-read & verified** the 5 priority gap books: Gatheral (Volatility Surface), Bergomi (Stochastic Volatility Modeling), Duffy (Finite Difference Methods), Haug (Option Pricing Formulas, lookup), Gregory (xVA Challenge). → `corpus/verified/` (now 53 verified files total).
- ✅ **Built the first topic-folder** as the flagship pattern: `content/pillars/03-derivative-pricing/black-scholes-merton/` (index lookup-hub + 6 sub-pages, committed `73a996b`). All formulas verified, Python runnable.
- **User review (2026-09-10):** structure approved ("to the point, not too verbose, good structure"). **Coherence + depth-thoroughness review deferred** until more topics are fleshed out — the plan is to build several topic-folders, THEN assess whether the whole hangs together and whether hard areas are deep enough.
- **In progress / next:** ~~build the next Pillar-3 topic-folders~~ **DONE — Pillar 3 complete.** All 11 topic-folders built and committed: options-fundamentals-and-markets, no-arbitrage-and-binomial, black-scholes-merton, volatility-surfaces-and-smiles, advanced-volatility-heston-sabr, american-options-and-optimal-stopping, numerical-methods, exotic-and-path-dependent-options, interest-rate-and-term-structure, counterparty-risk-and-xva, calibration-and-market-practice. Each = index lookup-hub + 6 sub-pages, math verified vs corpus, Python runnable. **77 pages / ~871 KB total.**
- **Audit (2026-09-10):** full 4-agent audit of Pillar 3 run (completeness, depth/template, coherence/linking, math/code) → reports in `corpus/audit/`. Result: coherent + deep, but initially missing 3 topics and had 1 math error. All fixed: 3 missing topic-folders built; put-call parity error + LSM code bug + broken wikilink fixed; lockstep pass done (pillar index rewritten, visualizer 11 nodes, diagnostic matrix, README, flat notes → `_legacy/`, 152 dangling wikilinks redirected, quartz build clean). Greeks unique content folded into bsm/04.
- **Next:** scale the folder-per-topic pattern to another area. **Foundations — DONE.** All 9 topic-folders built + lockstep pass committed: linear-algebra-and-matrices, calculus-and-optimization, probability-and-measure-theory, stochastic-calculus, statistics-and-inference, econometrics-and-timeseries, bayesian-statistics, numerical-methods, ergodicity-and-statistical-mechanics. 63 pages. Flat notes migrated to `_legacy/`. Build clean (207 files).
- **Next target:** **Fundamentals & Accounting** (the cross-cutting area with zero original coverage — the user's priority). Rich corpus + sources available (Penman, Damodaran, Graham-Dodd epub, Piotroski/Sloan/FF papers). Then the remaining pillars (1, 2, 4-8) which have corpus + free/paid sources ready.
- **Deferred (after pattern approval):** lockstep maintenance (visualizer.html nodes, index.md diagnostic matrix, pillar index, README). — **DONE for Pillar 3.**

---

## 4. Files to update before building content

- `content/index.md` — home hub + diagnostic matrix (hand-maintained; must be edited with new content).
- `content/visualizer.html` — D3 graph nodes/links are **hardcoded**; every new topic needs a node entry (id, group, path, skill scores, failure blurb) + edges.
- Pillar `index.md` hubs — add new topic folders to "Core Topics" lists.
- `README.md` — canonical literature list + new areas.

---

## 5. IMPORTANT — current content/ vs the plan (the migration gap)

**The current `content/` is the OLD DRAFT, NOT the target structure. Do not assume the plan is partly built.**

- As of handoff, `content/` has **65 `.md` files**: 8 pillar dirs each with **one hub + 6 flat topic notes** (the original draft's "6-topics-per-pillar cap"), plus 6 foundations notes, home hub, Inbox, visualizer.html.
- The **folder-per-topic** structure (topic = folder with index.md hub + sub-pages carrying intro→advanced depth) does **NOT exist yet** anywhere. It is a design decision, not a built reality.
- So the build is essentially a **migration + major expansion**: transform each pillar from flat notes into deep topic-folders. The existing 6 notes per pillar are a *starting skeleton* (good intuition/failure-mode seeds) — not finished depth.
- The 6-topics-per-pillar cap is likely to be revisited; some topics may split or merge under the new model.

**The magnitude:** a single pillar to near-Wall-Street depth = thousands of lines across its topic folders, with worked math + code per topic. This is a long, multi-session effort per pillar. Plan work in **defensible chunks** (start with Pillar 3 as the flagship), not one giant all-at-once push.

---

## 6. Consistency invariants (don't break these)

- **Verified files win** over raw text dumps for formulas.
- New notes must match the existing 6-section template & citation style (see `03-BUILD-METHOD`).
- Visualizer + diagnostic matrix updated **in lockstep** with new content, or new pages are invisible.

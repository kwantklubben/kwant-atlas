# Kwant-Atlas — Execution Reality & Scale (handoff 2026-09-09)

> This file exists because the scope is genuinely large. The Atlas, executed well, is one of the best learning-and-truth resources in quant finance — but it is a **long, multi-session, multi-thousand-line effort per pillar**. Reading this sets realistic expectations and the correct working method, so we build deep and correct instead of wide and shallow.

---

## 1. The honest scope

- **Current state:** `content/` is the old draft — 8 pillars × (hub + 6 flat notes) + 6 foundations = 65 files. It is a *skeleton*, not the finished map.
- **Target state:** folder-per-topic, each pillar a **mini-course** (intro → near-Wall-Street) with worked math and code across its topic folders.
- **Magnitude:** a single pillar to full depth is **thousands of lines**. All 8 pillars + foundations + fundamentals is realistically a **many-session, many-month** effort. It will never be "finished" in one pass — and that's fine. The goal is correct, deep, cumulative progress, pillar by pillar.

**We are NOT trying to do everything at once.** We are proving the pattern on Pillar 3, reviewing it with the user, then scaling.

---

## 2. The working method (how to build deep, not shallow)

1. **One pillar at a time.** Start with **Pillar 3 (Derivative Pricing)** — the flagship. Do it to full depth, review, then move on. Never interleave pillars.
2. **One topic-folder at a time.** Within a pillar, build each topic folder completely (hub + all sub-pages) before starting the next.
3. **Sources first, author second.** For each topic, work from the **verified deep-reads** (`corpus/verified/`) and the corpus (`corpus/*.md`, `corpus/titles/`). Verified files are authoritative for formulas — never copy from raw text dumps.
4. **Correctness over volume.** A topic page that is mathematically correct, with a working code block, is worth more than ten pages of plausible but unverified prose. Verify every formula against a source. Spot-check 3–5 formulas per page.
5. **Worked code is mandatory.** Every topic needs at least one real, runnable Python example that demonstrably works (the current template requires a print-verification). This is what makes the Atlas useful to implementers and trustworthy to learners.
6. **Work in defensible chunks.** Each session (or subagent) completes one topic folder or one coherent slice. Commit, verify, and report — don't leave half-finished sprawl.

---

## 3. How to parallelize (use subagents correctly)

- **Subagents are for bounded, well-specified chunks** — e.g. "build the `greeks-and-dynamic-hedging` topic folder from these verified files, matching this exact template." Give each the template, the source files, the target path, and the required frontmatter/tags.
- **Authoring agents write only their own new `.md` files** and report the wikilink slugs + node JSON they need registered.
- **ONE central pass** does the lockstep maintenance (visualizer.html, index.md diagnostic matrix, pillar hub, README) to avoid merge conflicts.
- **Do not** fan out 10 agents to "build Pillar 3" vaguely. Fan out per topic-folder with precise specs, then consolidate.

---

## 4. Depth bar — what "full depth" actually means per topic

A topic folder is "done" when a member can:
- **Beginner:** enter with no prior knowledge and get intuition + prerequisites, then follow the math from the start.
- **Intermediate:** find the formulas, derivations, and working code to implement it.
- **Expert/frontier:** reach the advanced sections, failure modes, and canonical literature for the deep end.

**Per-topic minimums:**
- Intuition section that actually explains *why* (not just *what*).
- Math ground truth with real derivations (LaTeX).
- At least one working, runnable Python implementation with a verification printout.
- Enumerated failure modes tied to first principles.
- Canonical literature (chapter-scoped book refs + papers) in the Atlas citation style.
- Connected graph bridges to related topics/foundations.
- Lookup tables/indexes in the hub so an expert can jump straight to a result.

**Per-pillar:** all its topic folders done to the above bar = a coherent mini-course.

---

## 5. Guard against the failure modes of huge builds

- **Shallow sprawl:** lots of files, none deep. → Enforce the per-topic minimums above before marking a folder done.
- **Formula rot:** plausible-but-wrong math from raw text. → Verified sources only; spot-check.
- **Broken links / invisible nodes:** new pages exist but the graph and diagnostic matrix weren't updated. → Lockstep maintenance is mandatory, not optional.
- **Subagent drift:** an agent goes off-spec. → Give precise specs; steer early from transcripts; consolidate centrally.
- **Burnout / no progress:** trying to do too much. → One pillar, one topic-folder at a time; commit and report each chunk.

---

## 6. Reminder of why this matters

Executed well, the Atlas is a genuine source of learning and truth for quantitative finance — the club's best resource, and potentially a public good for anyone learning quant. It is worth doing slowly and correctly. Depth and correctness are the product; speed is not.

---

## 7. First concrete milestone

**Pillar 3, topic by topic, to the depth bar above, using the delivered paid sources (deep-read) + the free sources + verified books already in hand.** When the user reviews it and the pattern is right, replicate across the other pillars.

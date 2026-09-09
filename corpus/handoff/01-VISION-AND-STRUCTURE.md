# Kwant-Atlas — Vision & Structure (locked 2026-09-09)

> This file records the decisions and the *reasoning* we aligned on, so future sessions (and new club contributors) share one picture. This is the source of truth for what the Atlas IS and WHY it's built this way. If something here seems wrong, change it deliberately and update this doc.

---

## 1. What the Atlas is — the "marriage" of three equal jobs

A **first-principles knowledge graph of quantitative finance for the club**, built so people of very different backgrounds (CS, math, econ — and no background) can enter any topic from zero. It is deliberately built to **marry three equally-important jobs** — none can be dropped:

**Job 1 — Find + understand quickly (the lookup table).**
The best lookup guide in the club: it condenses the important books and many fields into one clear, correct, findable spot. A member can find any topic and understand it fast, because the Atlas distills outputs from many important books and areas into one well-organized place.

**Job 2 — Follow a path and build (the study guide).**
From bare bones, a member can traverse the knowledge in a sensible order and build a real quant project, discovering related areas as their interest grows. If you're new to the club, whatever your education, you can approach from zero and follow the structure to build.

**Job 3 — Debug from first principles (the diagnostic).**
When you're actually building and something breaks, walk symptom → first-principles root cause → fix, through the same knowledge.

**Why they must be married (not separate artifacts):**
- A **graph** gives a great overview but is not useful when actually studying or diagnosing an issue.
- **Study paths** alone don't let you jump straight to an answer when you're stuck.
- A **lookup** alone doesn't teach you to build or to understand deeply.
The Atlas must do all three from the *same source of truth*. This "marriage" is the core of the vision — it is why the project exists.

---

## 2. The audience arc — three stages, all served by one content model

We explicitly aligned that the Atlas must serve members at different stages simultaneously. People join with very different backgrounds and at different points:

- **Beginners** — from any background (CS, math, economics, or none), who approach each topic from zero. The Atlas must let them in at the start.
- **Intermediates** — implementing quant projects, who need working, correct methods and code.
- **Experts / those reaching the frontier** — who need depth approaching (near) Wall-Street implementation and the advanced literature.

The content model serves all three at once:
- **Intuition first** → so beginners understand *why*, not just *what*.
- **Mathematical ground truth** → the derivations and first principles.
- **Working code** → so implementers can actually build.
- **Advanced sections** → for those pushing toward the frontier.

A member should be able to go from "I've never priced an option" to "I understand HJM's no-arbitrage condition" — and beyond — with every topic traced back to its mathematical foundation rather than presented as disconnected recipes.

---

## 3. Content model (locked — the structure that follows from the above)

Because of the audience arc and the depth requirement, we explicitly chose **folder-per-topic** over one giant page (a single page cannot carry intro→advanced with worked examples and stay navigable):

- **Every topic is a folder** with:
  - an **`index.md` hub** — overview, clean lookup (tables/indexes), and links into its sub-pages. The entry point and single source of truth for that topic.
  - **sub-pages** carrying the depth. This is the topic's *own internal structure*, NOT a detached "graded lesson track."
- **Depth standard:** every topic takes a member **from introduction to (near) Wall-Street implementation** — worked math and code. Realistically each pillar becomes a multi-thousand-line mini-course across its topic folders.
- **No artificial level tags / no forced graded tracks.** Depth is added via subsections and sub-sub-sections within the topic's pages. (We considered separate graded lesson tracks and rejected them as too much complexity.)
- **Navigation primacy: strong lists and indexes**, not the graph. "Nothing beats strong lists and indexes." The graph is an overview assist only.
- **One source of truth, community-maintained.** Public repo; members clone and submit PRs as needed.

---

## 4. The three layers

1. **The 8 operational pillars** — the domains you'd work in:
   P1 Quantitative Research · P2 Algorithmic & HFT · P3 Derivative Pricing · P4 Quantitative Risk · P5 Portfolio Optimization · P6 Market Making · P7 ML & Alt Data · P8 Quantitative Development
2. **A shared Foundations toolbox** — the math underneath all pillars (linear algebra, calculus/optimization, probability/measure, stochastic calculus, econometrics/time-series, numerics, Bayesian, info theory, discrete math).
3. **A cross-cutting Fundamentals & Accounting area** — company fundamentals/equity analysis underpin many projects; the Atlas had ZERO coverage here and adding it was an explicit priority.

---

## 5. The diagnostic matrix ("Why is my strategy failing?")

A signature UX mapping observed symptoms → first-principles root cause → remedy note (e.g. "3.5 Sharpe in backtest, instantly loses money live" → backtest overfitting → DSR remedy). This is how Job 3 (debugging) is operationalized.

---

## 6. Existing repo state (as of handoff)

- **`content/`**: 8 pillar dirs (each currently a hub + 6 topic notes), 6 foundations notes, home hub, Inbox, `visualizer.html` (D3 graph, **hardcoded node/link data — must be edited in lockstep with new content**), `index.md` (includes the diagnostic matrix, hand-maintained).
- Current notes use a strict 6-section template (see Build Method doc).
- **`corpus/`**: researched source wishlists per pillar/foundations/fundamentals + titles files + this handoff.
- **Sources on disk:** `~/kwant-atlas-sources/free/<domain>/` (free items downloaded). Verified book deep-reads in `~/local-repos/kwant-atlas/corpus/verified/` (43 files) and also in the Google Drive extraction folder.

---

## 7. Open items / to confirm next session

- **Pillar 3 is the flagship** (Option A): build it to full depth first as the model, review together, then scale the pattern to the other pillars.
- **Branch workflow:** work on a branch, verify, merge to main, delete orphan branches.
- The 6-topics-per-pillar cap of the current draft is likely to be revisited now that topics become folders (some may split/merge).
- Scope is huge (8 pillars + foundations + fundamentals to near-Wall-Street depth) — a long multi-session build. Never "finished" in one pass; iterate pillar by pillar.

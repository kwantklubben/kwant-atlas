# Learner / Newbie Perspective Audit — Does the From-Zero Arc Close?

**Repo:** `/home/alfred/local-repos/kwant-atlas`
**Perspective:** a motivated CS undergrad with **zero finance background**, trying to go from nothing → the intro material → actually building something, **without skipping a beat** (no unexplained jumps, no undefined vocabulary, no "it is obvious that…").
**Scope:** the learner-facing arc — home page → area hubs → `01-from-zero-intuition` pages → the built examples — for the three design jobs (find/understand, follow-and-build, debug-from-first-principles) and the three-rung audience arc (beginner → intermediate → expert).
**Date of audit:** 2026-09-10
**Method:** manual traversal of four real entry paths (files read line-by-line), plus programmatic scans:
- every `**Basic Prerequisites:**` line in the live corpus (`content/`, `_legacy` excluded) → dependency graph;
- full wikilink resolvability scan (8,230 links);
- extraction + execution of the Python block on every page cited here.

---

## 0. Verdict

**FAILS the "from zero" claim; PASSES as a reference.**

The Atlas is genuinely strong on the two jobs a *reference* has to do — it is fast to look things up in, and every code block I executed ran and reproduced its printed output exactly. That is rare and valuable.

But the **from-bare-bones arc does not close**. The core defect is systematic, not local:

> **The `01-from-zero-intuition` pages are titled "from zero" but are *written to a learner who already holds the prerequisite foundation*.** They open with the right rhetorical move ("start with the dumbest question") and then, within a screen, use the specialised vocabulary the prerequisite names — Itô's lemma, a martingale, `I(1)`, a quantile — as if it were already understood. The check that exposes this: **18 of the 96 `01-from-zero*` pages declare a foundation prerequisite that the Atlas's own beginner path never assigns**, and across the whole live corpus **166 of the 698 pages that declare prerequisites** depend on one of those unassigned foundations (econometrics, stochastic calculus, statistics). The page's own header is honest; the *route* that leads to it is not.

Compounding it, **no reading path in the Atlas routes through the Foundations toolbox.** Every pillar has a "Reading Path (Zero to X)", every one of those paths sticks to its own pillar's folders, and Foundations is only ever surfaced as a passive "Connected Graph Bridge" link at the bottom of a page. So the sequence the Atlas signposts is `Pillar hub → 01-from-zero → 02 → …`, while the sequence the content actually requires is `Foundations (unstated subset) → Pillar hub → 01-from-zero → …`. The gap between those two sequences is where the beginner gets stuck.

Two of the four traversed paths break at the *first* substantive step (Pillar 3 and Pillar 4); the third (build a momentum backtest) breaks at the premise (you are handed a prerequisite you were never routed to, and there is no real-data on-ramp). Details below.

---

## 1. Traversal summaries

### Path A — "I want to understand what an option is and price one"

**Route taken** (the route the Atlas itself signposts, from `content/pillars/03-derivative-pricing/index.md` §"Reading Path (Zero to Expert)", *Start* stage):
`options-fundamentals-and-markets/index` → `01-what-is-a-derivative` → `02-options-mechanics-and-payoffs` → `03-markets-and-products` → `04-no-arbitrage-and-bounds` → `no-arbitrage-and-binomial/index` → `01-from-zero` → `02` → `03` → `black-scholes-merton/01-from-zero-intuition` → `02` → `03-the-pricing-formulas`.

**Where it breaks.**

- **The entry is fine.** `options-fundamentals-and-markets/index.md:12` genuinely declares "None. This is the entry point to Pillar 3", and its `01-what-is-a-derivative.md:11` says "None — high-school algebra only." `01` reads from zero (forward vs option, carry vs forecast, payoff algebra) and its code runs. This is the model every other from-zero page should follow.

- **Break A1 — the signposted path omits the foundation it needs.** The pillar-3 `Start` stage names exactly *Options → No-Arbitrage → BSM* (`pillars/03-derivative-pricing/index.md`, "Reading Path", bullet 1) with no mention of the toolbox. But `no-arbitrage-and-binomial/01-from-zero.md:11` requires *Probability & Measure Theory*, and `black-scholes-merton/01-from-zero-intuition.md:9` requires *Stochastic Calculus & Itô's Lemma*. Following the pillar's own path, the learner walks into two gates that the path never warned about.

- **Break A2 — the BSM "from zero" page is not from zero.** `black-scholes-merton/01-from-zero-intuition.md:9` is explicit that the prerequisite is stochastic calculus, yet the page leans on exactly that vocabulary immediately: `:13` uses $dS=\mu S\,dt+\sigma S\,dW$ and "delta-share position", `:20` uses "risk-neutral measure … discounted prices are martingales … a change of measure (Girsanov)", `:26`–`:30` derive via Itô's lemma. For a zero-background learner this is the first *real* wall: the page that promises the aha of option pricing opens by assuming the machinery that produces the aha.

- **Break A3 — "price one" with code is reachable but not signposted to the beginner.** The single most valuable beginner artifact in the pillar is the runnable CRR tree engine at `no-arbitrage-and-binomial/index.md` §3 (stdlib only; I ran it — `n=5/25/100/1000 → 4.6277/4.4265/4.4544/4.4496`, converging to the BSM put 4.4494 as printed). But the hub's "Absolute beginner" route (`index.md:123`) sends the reader to `01-from-zero` (one-period replication) only, and the tree engine sits in the *hub prose*, so a learner following the arc never lands on the one runnable "price an option" program.

- **Naming-convention break (minor).** `options-fundamentals-and-markets/` is the only derivative folder whose first sub-page is **not** `01-from-zero-intuition` (`ls` shows `01-what-is-a-derivative.md …`). Every sibling folder uses `01-from-zero-intuition.md` (or `01-from-zero.md`). The hub's own route and the sibling cross-links happen to point at the real name, so nothing 404s today — but the moment any author writes the cross-folder link by analogy (`…/options-fundamentals-and-markets/01-from-zero-intuition`) it will dangle. The pattern is also inconsistent between folders: `no-arbitrage-and-binomial/01-from-zero.md` and `numerical-methods/01-from-zero.md` vs `01-from-zero-intuition.md` everywhere else.

**Net:** the learner *can* price an option — but only by stepping off the signposted path to read a foundation the path did not name, and only by finding the tree engine in hub prose rather than in the beginner route.

---

### Path B — "I want to build a simple momentum backtest"

**Route taken** (from `content/pillars/01-quantitative-research/index.md` §"Reading Path (Zero to Alpha)", *Start* stage, then the momentum folder):
`statistical-arbitrage-and-pairs/index` → `01-from-zero-intuition` → `fundamental-multi-factor-models` → `momentum/index` → `01-from-zero-intuition` → `02-cross-sectional-momentum` → `03-time-series-momentum` → `04` → `05` → `06`, then (Intermediate stage) `backtesting-hygiene/index`.

**Where it breaks.**

- **Break B1 — the arc's very first page ("from nothing") is gated on an unassigned foundation.** The pillar-1 `Start` stage is labelled "**from nothing** → alpha basics" and begins with `statistical-arbitrage-and-pairs/01-from-zero-intuition.md` — whose `:10` requires *Econometrics & Time Series (stationarity and unit roots)*. `momentum/01-from-zero-intuition.md:10` requires the same. Foundations' own hub (`foundations/index.md`, "Reading Path") tells the **absolute beginner** to read *1 Linear Algebra → 2 Calculus → 3 Probability* only, and files Econometrics under "Quant-interested (building)". So the learner who follows both hubs' advice in good faith arrives at Pillar 1 holding the three foundations he was told to get, and is missing the one the first page needs. This is the single most consequential arc break in the Atlas: **econometrics, stochastic calculus, and statistics are load-bearing across the corpus but appear on no beginner route anywhere.**

- **Break B2 — "no prior knowledge needed" is not true of the vocabulary.** `momentum/01-from-zero-intuition.md:16` claims no prior knowledge needed, but `:18` deploys "efficient market", "martingale", "serial correlation"; `:42` "band-passed"; `:46`–`:48` "dollar-neutral", "unit-gross", "100% gross leverage" — none defined on first use. "decile" appears only inside the code/output (`:88`–`:101`) undefined. A finance-naïve reader gets the *shape* of the argument but not the words.

- **Break B3 — there is no momentum *backtest* to build, only signal statistics.** `momentum/02-cross-sectional-momentum.md` and `03-time-series-momentum.md` produce Sharpe/spread numbers on **synthetic** return series (stdlib `random`), which is why they run cleanly with no data dependencies. But nothing in the folder is a backtest a learner can run end-to-end on real prices; transaction costs surface only as a caveat (`03:115`) pointing at Hygiene; and no page in Pillar 1 shows loading a single real price series. The design intent's job #2 — "traverse knowledge in a sane order **and build a real quant project**" — has no on-ramp in the pillar a newcomer would naturally pick for it.

- **Break B4 — the guardrail for a backtest is in the wrong stage.** A first backtest *is* an overfitting exercise, so `backtesting-hygiene` is needed from step one, but the pillar path files it under "Intermediate", after statarb/multi-factor/momentum. It is reachable via failure-mode prose (`momentum/02…:120`, `05…:99`), not via the route.

**Net:** the learner can *compute* momentum spreads, and every block runs, but "build a simple momentum backtest" has no end-to-end, real-data, cost-aware artifact to follow, and its prerequisite foundation is unassigned.

---

### Path C — "I want to understand risk / VaR"

**Route taken** (from `content/pillars/04-quantitative-risk/index.md` §"Reading Path (Zero to Risk-Governed)", *Start* stage):
`risk-factor-sensitivities/index` → `var-and-expected-shortfall/index` → `01-from-zero-intuition` → `parametric-historical-and-monte-carlo-var`.

**Where it breaks.**

- **Break C1 — the chosen entry point forward-references *another pillar*.** `risk-factor-sensitivities/index.md:12` (Basic Prerequisites) requires **`pillars/03-derivative-pricing/…/04-greeks-and-hedging` (Pillar 3 · The Greeks & Dynamic Hedging)**. A learner who chose the *risk* arc first is told, at the front door, to go read the *derivatives* pillar. Worse, the folder contradicts itself: `risk-factor-sensitivities/01-from-zero-intuition.md:10` says the prerequisite is "only the idea of a partial derivative" and "No options knowledge required." Hub and its own from-zero page disagree about whether Pillar 3 is needed. (In fairness the hub's `:1` framing — "Pillar 3 *derives* the Greeks, Pillar 4 *uses* them" — is pedagogically sound; the defect is that the *start of the arc* is where the cross-pillar debt is called in, rather than `02-delta-gamma-vega`.)

- **Break C2 — the VaR from-zero page is good but still gated.** `var-and-expected-shortfall/01-from-zero-intuition.md:10` requires *Probability & Measure Theory* ("a CDF and a quantile are all you need"), then `:22`/`:32`–`:35` use "quantile", "CDF", "loss distribution", "conditional expectation" as known. The page and its code are excellent (I ran it: `one bond 95% VaR=0.0 ES=80.00`, `two bonds 95% VaR=100.0 ES=103.20`, MC `95% VaR=400.0 ES=535.8` — exactly as printed), but the prerequisite is again not on any beginner route.

- **Break C3 — the follow-on page adds a second unassigned foundation.** `parametric-historical-and-monte-carlo-var/01-from-zero-intuition` requires *Statistics & Inference* — a different foundation from the one the VaR page named, also unassigned by the pillar path.

- **Break C4 — nothing connects the risk arc to a portfolio or real data.** Every example in the folder is a synthetic PMF or an MC over abstract bonds; there is no "here is a portfolio, here is its returns, compute VaR" bridge, which is what "understand risk/VaR" actually means to a builder.

**Net:** the intuition pages are among the best in the corpus, but the arc starts with a cross-pillar forward reference and rests on two unassigned foundations.

---

## 2. Stuck-points table

Severity: **H** = blocks the learner outright; **M** = forces a detour / muddles understanding; **L** = friction.

| # | Page (file:line) | What the learner hits | Proposed fix |
|---|---|---|---|
| 1 | `pillars/01-quantitative-research/index.md` §Reading Path (*Start*) + `statistical-arbitrage-and-pairs/01-from-zero-intuition.md:10` | "from nothing" path's first page requires **Econometrics & Time Series**, which the beginner foundations route never assigns. **H** | Add a "Before this pillar (foundations)" line to every pillar's Reading Path naming the exact foundation folders; for Pillar 1: `econometrics-and-timeseries` + `probability-and-measure-theory`. |
| 2 | `foundations/index.md` §"Reading Path" | Beginner route = LA → Calc → Prob only; files **Econometrics / Stochastic Calculus / Statistics** under later audiences, yet 45 from-zero pages require them. **H** | Rewrite the beginner route as a **consumption-order contract**: "Beginner core (read before any pillar): 3 Probability → 9 … " and list, per pillar, which foundations it consumes. |
| 3 | `pillars/03-derivative-pricing/black-scholes-merton/01-from-zero-intuition.md:9` (+ `pillars/03-derivative-pricing/index.md` §Reading Path) | A page titled "from zero" requires **Stochastic Calculus**; the pillar's Start path never mentions it; page uses Itô/Girsanov/martingale from `:13`. **H** | Insert a synthesis step in the pillar path: "Options → No-Arbitrage → *[foundations/stochastic-calculus]* → BSM", and rename BSM `01` to `01-intuition-given-stochastic-calculus` or add a one-paragraph "what you need first and why" block at the top. |
| 4 | `pillars/03-derivative-pricing/no-arbitrage-and-binomial/01-from-zero.md:11` | Same pattern: requires **Probability & Measure Theory**, absent from the pillar path. **H** | Same as #3 — name the foundation in the path, or make the page truly standalone (it nearly is; the one-period replication needs almost no measure theory). |
| 5 | `pillars/04-quantitative-risk/risk-factor-sensitivities/index.md:12` vs `…/01-from-zero-intuition.md:10` | Hub requires **Pillar 3 (Greeks)**; the from-zero page says "No options knowledge required." Direct contradiction; the risk arc opens with a cross-pillar debt. **H** | Move the Pillar-3 dependency to `02-delta-gamma-vega.md`'s prerequisites; make the hub's start-page prereq match the from-zero page ("multivariable calculus only"). |
| 6 | `pillars/04-quantitative-risk/index.md` §Reading Path (*Start*) | Start stage begins with Risk-Factor Sensitivities but never names *Probability* / *Statistics* foundations its pages require. **M** | Add the "Before this pillar" foundations line (same fix as #1). |
| 7 | `pillars/01-quantitative-research/momentum/01-from-zero-intuition.md:16,18,42,46–48` | Claims "no prior knowledge needed" but uses *efficient market, martingale, serial correlation, band-passed, dollar-neutral, gross leverage* undefined; "decile" only in code (`:88`). **M** | Add a 5-term mini-glossary at first use (or a hoverable glossary page); define "decile" before the code. |
| 8 | `pillars/01-quantitative-research/statistical-arbitrage-and-pairs/01-from-zero-intuition.md:23,43,109` | Uses `I(1)`/unit root/cointegration/ADF with the header's `:10` prerequisite pointing off-route; "beta"/"hedge ratio" appear (`:19`) before the hub's Dictionary of "beta". **M** | Add the on-page one-line definitions at first use; link the foundation page inline at the first mention of *stationarity*. |
| 9 | `pillars/03-derivative-pricing/options-fundamentals-and-markets/` (folder naming) | Only derivative folder whose first sub-page is not `01-from-zero-intuition`; siblings mix `01-from-zero.md` and `01-from-zero-intuition.md`. **L** | Standardise on `01-from-zero-intuition.md` (or document the exception) so analogy-built links resolve. |
| 10 | `pillars/03-derivative-pricing/no-arbitrage-and-binomial/index.md:123` (beginner route) | The one runnable "price an option" program (CRR tree engine, `:56`–`:90`) is in hub prose; the beginner route sends the reader elsewhere. **M** | Add the tree engine to the "Absolute beginner" bullet, or promote it to a tiny `03b-run-it.md`. |
| 11 | Pillar 1 whole folder (all `01…06`) | No end-to-end, real-data, cost-aware backtest to build; all examples are synthetic. **H** (against design job #2) | Add a "your first backtest" capstone page (load one CSV/price series → signal → positions → costs → PnL → deflated Sharpe), or link Pillar 8 `event-driven-backtesting-engines` from the momentum failure modes as the build target. |
| 12 | `pillars/01-quantitative-research/index.md` §Reading Path | `backtesting-hygiene` filed as "Intermediate", after the folders a new builder starts with. **M** | Move a short "backtest hygiene happens *before* you build" pointer into the Start stage. |
| 13 | `pillars/08-quantitative-development/index.md` §Reading Path (*Start* step 1) + `python-quant-stack/index.md:12` | Pillar 8's "from nothing" step 1 (`python-quant-stack`) requires **Pillar 1** (Quantitative Research) and **Numerical Methods** — a forward cross-pillar dependency at the pillar's own start. **M** | Either soften the prereq to "basic Python" (the from-zero page `01-from-zero-intuition.md:9` already says "none beyond basic Python"), or say so in the path. |
| 14 | `content/index.md:14–17,155–167` | Home page gives no "start here / how to read this Atlas" block; Foundations introduced last and phrased as optional ("Before diving into complex models, anchor…"). **H** (onboarding) | Add a top "New here? Start with X → then pick a pillar" panel with the beginner route; label the Foundations block "read this first if you're new". |
| 15 | `foundations/index.md` (end) | No exit ramp: after the toolbox the learner is not told which pillar to enter or that a pillar's from-zero pages link back here. **M** | Add "Now go to: Pillar 1 for alpha, Pillar 3 for derivatives, Pillar 4 for risk" with the entry page for each. |
| 16 | Corpus-wide: 8 prose `[[…]]` math intervals | `[[t_{i,0},t_{i,1}]]` (`purged-cross-validation…/01:44`, `…/03:29,43`, `…/index:32`) and `x[[0,2,4]]` (`python-quant-stack/02:24,44`) sit in prose/math, not code, and will be parsed as wikilinks → broken-link rendering. **L** | Escape or re-typeset the interval notation (`[\![` or `$[\,t_{i,0},t_{i,1}\,]$`). |

---

## 3. Prerequisite-graph problems

### 3.1 Forward references (a page requires something the path has not yet taught)

| Referencing page | Requires | Why it breaks the arc |
|---|---|---|
| `pillars/04-quantitative-risk/risk-factor-sensitivities/index.md:12` | Pillar 3 `black-scholes-merton/04-greeks-and-hedging` | Entry point of the *risk* pillar demands the *derivatives* pillar. |
| `pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index.md:12` | Pillar 3 (options) | Merton structural model = equity as a call; unavoidable, but the pillar path does not sequence Pillar 3 before it. |
| `pillars/04-quantitative-risk/counterparty-risk-and-xva/index.md:12` | Pillar 3 + Pillar 4 | Deep-pillar page; acceptable *if* the path names the ordering — it does not. |
| `pillars/08-quantitative-development/python-quant-stack/index.md:12` | Pillar 1 Quant Research | Pillar 8's declared "from nothing" step 1 depends on Pillar 1. |
| `pillars/08-quantitative-development/event-driven-backtesting-engines/index.md:12` | Pillar 1 + Pillar 2 | Backtesting engine requires alpha + execution knowledge; path does not say so. |
| `pillars/07-machine-learning-altdata/purged-cross-validation-…/index.md:12`, `regime-classification-hmm-and-gmm/index.md:12`, `ml-for-portfolio/index.md:12` | Pillar 1 / Pillar 5 | ML pillar depends on alpha + portfolio pillars; path does not name them. |

All of the above are *legitimate* dependencies a graduate curriculum would have — but the Atlas presents each pillar's reading path as self-contained ("Follow them in the order below"), so the cross-pillar debts are invisible until the learner hits them.

### 3.2 Unassigned / orphaned prerequisites (the systemic defect)

Programmatic scan of `**Basic Prerequisites:**` across the live corpus:
- **96** pages are named `01-from-zero*` (the entries the arc tells you to start with).
- **18** of them declare a foundation **outside** the beginner route (`linear-algebra`, `calculus`, `probability`) — i.e. ~19% of the pages whose entire job is to start from zero.
- Widened to **all** pages, **166 of 698** pages that declare prerequisites pull in one of these off-route foundations.

Breakdown (counts are `01-from-zero*` pages first; total live pages in parentheses):

| Foundation | `01-from-zero*` pages gated | All pages declaring it | Where the beginner route places it |
|---|---|---|---|
| `econometrics-and-timeseries` | 6 | 54 | "Quant-interested (building)" — **after** the beginner stage |
| `stochastic-calculus` | 5 | 35 | "Quant-interested (building)" |
| `statistics-and-inference` | 6 | 51 | "Statistically deep / ML" |
| `ergodicity-and-statistical-mechanics` | 1 | 10 | listed last |
| `bayesian-statistics` | 0 | 13 | listed last |
| `numerical-methods` | 0 | 15 | "Implementation-focused" |

The 18 gated `01-from-zero*` pages are the concrete arc-breakers:
`statistical-arbitrage-and-pairs/01`, `momentum/01`, `event-studies/01`, `regime-detection/01`, `garch-and-volatility-modeling/01` (→ econometrics); `black-scholes-merton/01`, `american-options-and-optimal-stopping/01`, `exotic-and-path-dependent-options/01`, `interest-rate-and-term-structure/01`, `counterparty-risk-and-xva/01` (→ stochastic calculus); `parametric-historical-and-monte-carlo-var/01`, `model-risk-and-validation/01`, `financial-ml-pitfalls-and-low-snr/01`, `tree-and-boosting-methods/01`, `ml-for-portfolio/01`, `alternative-data-pipelines-and-evaluation/01` (→ statistics); `kelly-criterion-and-bet-sizing/01` (→ ergodicity); `spread-decomposition-and-roll-model/01` (→ econometrics).

**Consequence:** the asset that the Atlas advertises most loudly — the shared First-Principles Toolbox (`content/index.md:157`, "anchor your intuition in the rigorous mathematical foundations…") — is structurally **disconnected from the arcs it underwrites.** It is linked only through per-page "Connected Graph Bridges" (bottom-of-page footer links), never through a reading path. Nothing tells the beginner "before Pillar 1, read Econometrics; before BSM, read Stochastic Calculus."

### 3.3 Link integrity

- **Dead links: confined to `_legacy/`.** ~30 dangling references live entirely in `_legacy/` folders (`foundations/stochastic-calculus-and-ito`, `pillars/03-derivative-pricing/implied-volatility-surface-and-smiles`, etc.). These folders are archival and excluded from the live graph, so they do not strand a learner — but they should be pruned or redirected so a curious learner who lands in `_legacy/` isn't lost.
- **Live pages: 0 dangling *navigation* links.** Every hub/sub-page wikilink in the live corpus resolves. This is a real strength — the lookup job (#1) is sound.
- **8 prose `[[…]]` intervals** (see stuck-point #16) will be mis-parsed as wikilinks by Quartz — a rendering defect, not a navigation dead-end.

---

## 4. Onboarding assessment

**Home page (`content/index.md`) — weak for a newcomer.**
- No "start here", "how to use this Atlas", or "reading order for newcomers" anywhere in the file. `:14–17` jumps straight from a welcome sentence into the 8-pillar taxonomy.
- The 8 pillars are presented as a **numbered menu**, which reads like a sequence but is not one (`:20`, `:67`–`:15x`). A newcomer cannot tell whether to start at Pillar 1, at Foundations, or at Fundamentals.
- **Foundations are introduced last and phrased as optional** (`:157`: "Before diving into complex models, anchor your intuition…"). For a zero-background learner this is the *first* thing that should be flagged as required, not a closing footnote.
- **Fundamentals & Accounting is handled well** (`:177`–`:186`): explicit "recommended learning order" and a hub link. The asymmetry is telling — the area the Atlas thought about a newcomer for got an order; the Foundations toolbox did not.
- The interactive graph (`:209`) and the diagnostic matrix (`:190`–`:203`) are excellent for jobs #1 and #3, and useless to a beginner choosing a first step (the matrix is framed for "why is *my strategy* failing" — presupposes a strategy).

**Area hubs — good individually, incoherent collectively.**
- Every pillar hub has a genuinely good staged "Reading Path (Zero to X)" (Pillars 3, 4, 5, 6, 7, 8 all read as thoughtful). Within a pillar, the arc is sane and the sub-page order (01→06) matches the stated climb.
- But **each hub's path is written as if its pillar were the whole world.** None opens with "Foundations you need first," none names a second pillar it depends on, and the fixed 6-slot template (`01-from-zero-intuition … 06-advanced-extensions`) is applied even when a page's prerequisites contradict the slot label (a "from-zero" slot requiring stochastic calculus — §3.2).
- **`foundations/index.md` has a reading path but no exit ramp**; **`fundamentals-accounting/index.md` has both a reading path and an exit ramp** (its "Where This Area Connects" links out). Copy the fundamentals pattern into foundations and the pillars.
- **No glossary / no "vocabulary you'll meet" index**, so undefined-first-use jargon (stuck-points #7, #8) has nowhere to be looked up.

**Net onboarding verdict:** a newcomer knows *what exists* (the map is excellent) but not *what order to read it in* or *that Foundations is a prerequisite rather than an appendix*.

---

## 5. Verdict + top 10 fixes

**Verdict.** As a **lookup guide** and **debugging aid**, the Atlas is close to best-in-class: 8,230 wikilinks with zero dangling navigation links, uniform templates, and code that actually executes and reproduces its printed numbers. As a **follow-a-path-and-build** guide for a true zero-background learner, the arc does **not** close: the `01-from-zero-intuition` pages are written to a reader who already holds an unstated foundation, the reading paths never route through the Foundations toolbox (18 of 96 from-zero pages need a foundation the beginner route never assigns), and the build endgame (real data, costs, an end-to-end backtest) has no on-ramp in the pillar a beginner would pick. **The design intent's "no skipped beat" is not met.**

### Top 10 fixes (highest leverage first)

1. **Give every pillar Reading Path a "Before this pillar (foundations): X, Y" line**, listing the exact foundation folders its from-zero pages require. *(Fixes stuck-points #1, #4, #6, #12, and §3.2 wholesale.)*
2. **Rewrite `foundations/index.md`'s beginner route as a consumption-order contract** — "read Probability, then (for Pillar 1) Econometrics, (for Pillar 3) Stochastic Calculus…" — and add an exit ramp ("now enter Pillar X at page Y").
3. **Add a "New here? Start here" panel to `content/index.md`** with one concrete beginner route (Foundations core → one pillar), and relabel the Foundations section as required reading, not an appendix.
4. **Fix the Pillar-4 entry-point contradiction**: `risk-factor-sensitivities` hub vs its from-zero page disagree about whether Pillar 3 is required — align them and move the Greeks dependency to `02-delta-gamma-vega`.
5. **Gate BSM (and the other 8 stochastic-calculus from-zero pages) honestly**: either insert the foundation into the signposted path or add a "what you must know first, and why" header block, and stop advertising them as "from zero" without qualification.
6. **Build one end-to-end real-data capstone** (e.g. "your first momentum backtest": load prices → signal → positions → costs → PnL → deflated Sharpe) and link it from the Pillar-1 Start stage.
7. **Move `backtesting-hygiene` into the Pillar-1 Start stage** (a first backtest is an overfitting exercise; the guardrail belongs before the build, not after).
8. **Add a 5–10 term mini-glossary** (or per-page first-use definitions) for the jargon the from-zero pages assume: efficient market, martingale, dollar-neutral, gross leverage, decile, I(1), quantile, CDF.
9. **Standardise the from-zero filename** to `01-from-zero-intuition.md` across all folders (fix `options-fundamentals-and-markets` and the two `01-from-zero.md` outliers) so analogy-authored links resolve.
10. **Prune/redirect the `_legacy/` dead links and escape the 8 prose `[[…]]` math intervals** — housekeeping that removes the only genuinely broken links and a class of rendering defects.

---

### Appendix — evidence commands

```bash
# dependency graph of every Basic Prerequisites line (live corpus, _legacy excluded)
python3 /tmp/prereq.py            # -> 96 01-from-zero* pages; 18 gated on off-route foundations; 166/698 pages corpus-wide

# full wikilink resolvability (8,230 links); live pages: 0 dangling nav links, 8 prose intervals + _legacy dead links
python3 /tmp/linkcheck.py

# execute the Python block on each cited page and diff against the printed output
python3 /tmp/runblk.py <page.md> ...
```

Pages whose code was executed and verified against their printed output during this audit:
`options-fundamentals-and-markets/01-what-is-a-derivative.md`, `no-arbitrage-and-binomial/01-from-zero.md`, `no-arbitrage-and-binomial/index.md` (CRR engine), `black-scholes-merton/01-from-zero-intuition.md`, `statistical-arbitrage-and-pairs/01-from-zero-intuition.md`, `momentum/01-from-zero-intuition.md`, `momentum/02-cross-sectional-momentum.md`, `var-and-expected-shortfall/01-from-zero-intuition.md`, `risk-factor-sensitivities/01-from-zero-intuition.md`.

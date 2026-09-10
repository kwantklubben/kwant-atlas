# Pillar 3 — Depth & Template-Adherence Audit

**Scope:** 8 topic-folders under `content/pillars/03-derivative-pricing/`, each = `index.md` + `01`–`06` sub-pages = **56 files**.
**Reference pattern:** `black-scholes-merton/` (flagship).
**Auditor method:** read every file; template checked programmatically (frontmatter, tag order, prerequisites line, section presence/order, Python fences, output blocks); depth assessed against the beginner→intermediate→expert (Wall-Street) arc; two numeric claims re-executed.

---

## 1. Locked-template adherence — checklist

Template requirements per note: (a) YAML frontmatter with **quoted** `title`; (b) `tags:` list whose **first** tag is `pillar-derivative-pricing`; (c) a `**Basic Prerequisites:** [[full/slug|Alias]]` line; (d) exactly the six sections in order — `### 1. Intuition & Practical Objective` → `### 2. Mathematical Ground Truth & Derivations` → `### 3. Computational Implementation` (Python fence **with** print-verification output) → `### 4. Failure Modes & First-Principles Breakdowns` (numbered) → `### 5. Canonical Literature & Study References` → `### 6. Connected Graph Bridges`.

### Pass/fail counts

| Folder | Files | Frontmatter | Quoted title | First tag correct | Prereq line w/ wikilink | All 6 sections in order | Python + output | **Full pass** |
|---|---|---|---|---|---|---|---|---|
| black-scholes-merton | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| volatility-surfaces-and-smiles | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 6/7 | **6/7** |
| advanced-volatility-heston-sabr | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| no-arbitrage-and-binomial | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| numerical-methods | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| exotic-and-path-dependent-options | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 6/7 | 7/7 | **6/7** |
| interest-rate-and-term-structure | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| counterparty-risk-and-xva | 7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | **7/7** |
| **TOTAL** | **56** | **56/56** | **56/56** | **56/56** | **56/56** | **55/56** | **55/56** | **54/56** |

### Deviations (exactly 2, both cosmetic, both in `index.md` files)

1. **`volatility-surfaces-and-smiles/index.md` — §3 has a Python fence but no printed-output block.** The §2 lookup table's "Verified check" column carries the numbers (e.g. skew slice recovered exactly 28/24/20/17/15%, Dupire `0.042695`), and sub-pages 01–06 all carry full output blocks, so the *evidence* exists — but the hub page itself breaks the "(Python fenced block with print-verification output)" letter of the template. The BSM and numerical-methods hubs do include an output block illustration.
2. **`exotic-and-path-dependent-options/index.md` — §2 heading mislabeled.** It reads `### 2. Mathematical Ground Truth & Lookup` instead of `### 2. Mathematical Ground Truth & Derivations`. Content and table are present and strong; only the heading string deviates from the locked template. (This is the sole reason its Section-presence column is 6/7.)

No other structural deviation. Every page — including every `06-advanced-extensions.md` and every `index.md` — has the quoted-title frontmatter, the `pillar-derivative-pricing` first tag, a real `[[full/slug|Alias]]` prerequisites line, LaTeX in §2, numbered failure modes in §4, and at least one runnable stdlib-only Python block with a fenced output block.

**Template verdict: PASS (54/56 strict; 56/56 on all load-bearing requirements). Two one-line fixes close the gap.**

---

## 2. Depth per folder (shallow / adequate / deep)

Size metrics (all 7 files) are a proxy; content was read to confirm.

| Folder | Lines | Words | Py blocks | Depth rating |
|---|---|---|---|---|
| black-scholes-merton | 897 | 6,958 | 9 | **Deep (reference)** |
| volatility-surfaces-and-smiles | 946 | 8,432 | 7 | **Deep** |
| advanced-volatility-heston-sabr | 1,467 | 15,123 | 7 | **Deep (deepest)** |
| no-arbitrage-and-binomial | 1,012 | 8,769 | 10 | **Deep** |
| numerical-methods | 1,679 | 13,877 | 9 | **Deep** |
| exotic-and-path-dependent-options | 987 | 7,923 | 9 | **Deep (one numeric bug)** |
| interest-rate-and-term-structure | 978 | 7,964 | 7 | **Adequate→Deep** |
| counterparty-risk-and-xva | 969 | 9,258 | 9 | **Adequate→Deep** |

### black-scholes-merton — Deep (the reference) ✅
The hub is a genuine *formula lookup*: an 11-row quick-reference table (generalized call/put, parity, all Greeks, gamma–theta trade) with a **"Verified check" column** carrying Haug-verified digits, plus the critical per-1-vol-point / per-day scaling caveat. §3 is a stdlib-only engine (`math.erf`) that reproduces every quoted number, with an output block. Sub-pages walk derivation → closed forms → Greeks → failure modes → extensions. This is the pattern the other seven are copied from, and the copy is faithful.

### volatility-surfaces-and-smiles — Deep ✅
Hub has a 12-row lookup (Dupire local vol both forms, SVI, variance swap, SSR `R_T`, Heston short-dated skew, jump compensator, rough-vol). Math density in §2 is high (60 LaTeX expressions on `04-advanced-dynamics.md`). The standout is **intellectual honesty**: it flags that Gatheral's printed ATM term-structure formula (3.18) returns the long-run mean `0.0354`, not the instantaneous `0.0174`, with the numerical proof. Only blemish: hub §3 lacks an output block (above).

### advanced-volatility-heston-sabr — Deep (deepest) ✅
Largest folder (15.1k words). `02-the-heston-model` (65 LaTeX), `03-sabr-and-asymptotics` (69), `04-stochastic-vol-dynamics` (95), `05-failure-modes` (61). Covers characteristic function, Feller condition, Hagan asymptotics, Bergomi forward-variance, SABR calibration. This is true expert/frontier material — genuinely "Wall-Street-adjacent".

### no-arbitrage-and-binomial — Deep ✅
10 Python blocks — the most of any folder. Starts from the one-period replication system `Δ=(f_u−f_d)/(S_0(u−d))`, the `d < 1+r < u` bracket, risk-neutral weights, then CRR convergence and the Fundamental Theorems of Asset Pricing. Strong intuition ("two instruments, two states ⇒ square system") and clean derivations. Serves all three tiers.

### numerical-methods — Deep ✅
Second-largest (13.9k). Hub has **12 lookup tables** (three families, θ-scheme table, von-Neumann symbols, "which scheme for which problem"). §3 is exemplary: **three engines on one contract** (CRR, Crank–Nicolson, Monte Carlo) all landing on the same number, with a discrepancy noted to 4 decimals. `06-advanced-extensions` (381 lines) is a minor masterpiece — American (PSOR/CRR/LSM with the correct *sign* of each estimator's bias), ADI vs explicit instability (`1.73×10^33` blow-up), randomised-Halton QMC with an honest counter-example (unrandomised Halton off by `−0.1174`). Not "sketched" — fully worked.

### exotic-and-path-dependent-options — Deep, with one numeric bug ⚠️
Hub lookup has ~15 exotic families (barriers Reiner–Rubinstein, BGK discrete-barrier correction, lookbacks, Asians, compound/chooser, Margrabe, quanto, Kirk) with verified check values. Good scaling caveats. **Two issues:**
- **(structure)** hub §2 heading mislabeled (template deviation #2 above).
- **(content)** `06-advanced-extensions.md` §3 "Tool 2" prints **`LSM American put = 6.2518`** and then states it is the *low-biased* estimate, while the page's **own binomial benchmark is `6.0902`** (lower). A low-biased estimator cannot exceed the benchmark by 0.16 — the page's text contradicts its own numbers. Re-executing the exact pasted code reproduces `6.2518`, so the bug is in the LSM discounting logic (ITM non-exercised paths are not discounted each step), not a transcription slip. This should be fixed: it teaches an incorrect lesson about LSM bias direction. (The *other* LSM in `numerical-methods/06` is correct — `4.6765` sits below its `4.6921` benchmark with the premium explained.)

### interest-rate-and-term-structure — Adequate→Deep
7 Python blocks, all with output. Solid: `01` builds the "why" from ZCBs and the log-slope identities; `02` bootstrapping; `03` short-rate models (Vasicek MC `0.807521` vs closed form `0.807678`); `04` numéraire/HJM/LMM. Math density is lower than the vol/BSM folders (mostly 20–47 LaTeX in §2) but the coverage of the fixed-income canon (Björk, Brigo–Mercurio, Shreve I) is correct and the arc is intact. Slightly less "frontier" depth than heston/numerical, but nothing skimmed.

### counterparty-risk-and-xva — Adequate→Deep
Professional and practically oriented. Hub has **13 lookup tables**. Covers exposure mechanics (EFV/PFE/EPE/ENE and the `EPE+ENE=EFV` identity), CVA/DVA, FVA/MVA, then capital (BA-CVA diversification flooring at ρ=50%, SA-CVA), wrong-way risk, and the xVA desk P&L explain. The real-world content is strong. **Caveat:** §2 math is thinner here (9–30 LaTeX on pages 04/05 vs 60–95 on the vol folders) — appropriate to a field that is less formula-dense than stochastic vol, but it is the least "derivation-heavy" folder. Depth is in breadth and practice rather than in worked proofs.

---

## 3. Audience arc (beginner / intermediate / expert)

All **8 `index.md` hubs contain a `**Recommended reading route (audience arc):**` block** explicitly labelling:
- **Absolute beginner** → `01-from-zero*` ("no prior knowledge needed");
- **Formulas + code (undergrad/job-seeking)** → `02`→`03`(→`04`);
- **Robustness (practitioner/graduate)** → `05 Failure Modes` → `06 Advanced Extensions`.

This is uniform across all eight folders — a strong consistency win. The `01` pages genuinely start from "the dumbest question" (e.g. "why does an option have a price at all?", "why is there a term structure?") and build intuition before any formula; the `02–04` pages are formula+code; `05–06` carry the expert failure modes and frontier extensions. **All three tiers are served in every folder.**

---

## 4. Consistency across the 8 folders

- **Voice & voice-format:** Highly consistent. Same section skeletons, same `**Basic Prerequisites:**` convention, same "Hub signposts — the folder's failure-mode analysis lives in …" pattern on hub §4, same stdlib-only (`math`/`cmath`, no numpy/scipy) Python convention with fenced output, same LaTeX notation discipline.
- **Hub quality:** every hub has a Quick-Reference lookup table and a reading-route block. Table counts: numerical-methods 12, counterparty 13, the rest 3 each in the hub (deeper tables live on sub-pages).
- **Thinnest / most off-pattern:** `counterparty-risk-and-xva` and `interest-rate-and-term-structure` are the lightest on §2 math density. Neither reads as "unfinished", but they are the two folders where a Wall-Street expert would want more worked derivations. `exotic-and-path-dependent-options` is the only folder with a *content* defect (the LSM number).
- **Bonus files (outside the 8 folders but in the pillar):** 7 flat root notes (`black-scholes-merton-and-feynman-kac.md`, `the-greeks-and-dynamic-hedging.md`, `implied-volatility-surface-and-smiles.md`, etc.) plus the pillar-level `index.md` (a 47-line Mermaid pipeline overview). The flat notes are shorter (~100–120 lines) but carry the same frontmatter/tag/prereq pattern, and the folder hubs link to them as "sibling topic / related flat notes". They are consistent, not off-pattern.

---

## 5. Overall verdict

**Template adherence: PASS.** 56/56 files satisfy the load-bearing requirements (quoted-title frontmatter, `pillar-derivative-pricing` first tag, `[[full/slug|Alias]]` prerequisites, all six sections in order, LaTeX §2, numbered §4, Python+output). 54/56 strict. The 2 deviations are one missing output block (`volatility-surfaces-and-smiles/index.md`) and one mislabeled heading (`exotic-and-path-dependent-options/index.md`) — both one-line fixes.

**Depth: sufficient for the three-job mission (find-fast, follow-and-build, debug).** The "find fast" job is served by the hub lookup tables with verified-check columns; "follow-and-build" by the stdlib-only, output-verified Python on every page; "debug" by the failure-mode sections that name the exact symptom (CFL blow-ups, CN ringing, ADI on cross-derivatives, wrong cost-of-carry `b`, discrete-vs-continuous monitoring, DVA-in-capital, diffusion-only WWR). The hardest areas — Heston/SABR characteristic functions, α-hypergeometric asymptotics, LSM/duality, ADI/Yanenko splitting, BA-CVA/SA-CVA capital, wrong-way risk — are genuinely worked, not skimmed.

**Required fixes (3, all minor):**
1. `volatility-surfaces-and-smiles/index.md` — add a fenced output block under the §3 Python fence.
2. `exotic-and-path-dependent-options/index.md` — rename §2 heading to `… & Derivations`.
3. `exotic-and-path-dependent-options/06-advanced-extensions.md` — fix the LSM discounting bug and correct the `6.2518` / low-bias narrative (it currently prints a value *above* its own benchmark while claiming low bias).

**Optional depth upgrade:** strengthen §2 formal-derivation density in `counterparty-risk-and-xva` and `interest-rate-and-term-structure` to match the vol/BSM folders — these are the only two that lag the flagship on math.

# Audit: pillars/08-quantitative-development/event-driven-backtesting-engines/

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-11
**Target (exact path):** `content/pillars/08-quantitative-development/event-driven-backtesting-engines/`
**Files checked:** 7 (index.md + 6 sub-pages). `_legacy` ignored.
**Python blocks run:** 7 (one per file). All ran clean (rc=0).
**Verdict:** FAIL — 4 defects (code reproduces exactly; 2 math/claim defects, 2 coherence/claim-accuracy defects).

---

## Summary of findings

| # | Severity | File:line | Type | Stated | Correct |
|---|----------|-----------|------|--------|---------|
| 1 | MED-HIGH (math/semantics) | 03-the-event-loop.md:135 | Self-contradictory scaling claim | "the shortfall grows roughly like $\sqrt{\text{delay}}$ … rising from 18.81 bps (delay 1) to 25.13 bps (delay 100)" | 18.81→25.13 over a 100× delay is a **1.34×** rise; $\sqrt{}$ scaling predicts **10×**. Claim contradicted by its own numbers (and by the hub's shortfall column, which rises 37.5× over the same interval). The cited "300-path simulation of the momentum strategy in 04" does not exist (04 runs 400 paths and computes no shortfall). |
| 2 | MED (math/symbol) | 01-from-zero-intuition.md:47 | Double-counts the spread | $P_{\text{fill}}=S^{\text{ask}}_{t+\tau}(1+s)$, "with $s$ the spread-half you cross" | An ask already crosses the half-spread (05:35 defines $P_{\text{cross}}=P_{\text{mid}}+\tfrac12\text{spread}$). Writing $S^{\text{ask}}\cdot(1+s)$ pays 1.5× the half-spread. Correct: $P_{\text{fill}}=S^{\text{ask}}_{t+\tau}$ **or** $S^{\text{mid}}_{t+\tau}(1+s)$. |
| 3 | MED (claim accuracy) | 02-architecture.md:161 | Unsupported / contradicted by own trace | "Without subtracting in-flight orders from the target, the Portfolio would re-submit the same 100-share order on every bar … manufacturing a $10\times$ position" | Re-running this exact engine with the `work` term removed yields **final position = 100** (the SELL is skipped: `d = target − pos = 0`), not a 10× position. Strategy only emits on change, so no per-bar re-submission occurs either. |
| 4 | LOW (coherence) | index.md:51 | Order-of-magnitude mismatch | "the naive vectorized Sharpe is inflated by roughly **an order of magnitude** over what the same signal achieves under honest fills" | Same page (index.md:61) states the gap is **$116\times$** (precise: 126.7×), i.e. two orders of magnitude. |

**Not counted (observations):**
- 05:49 — closed form $\frac{E^{\text{surv}}}{E^{\text{true}}}=(1+d\ell)^Y = 1.276$ predicts +27.6% while the §3 experiment reports **+29.2%**. The formula is explicitly labelled "roughly", and the experiment is seeded; the true ratio is $(1+\mu_s)/(1+\mu_f)\approx(1.08)/(1.026)$. Acceptable as a heuristic, but the closed form does not equal the quoted measurement.
- index.md:61 / 04:186 quote "$116\times$"; computed from the displayed rounded values (3.50/0.03 = 116.7). The precise script output is naive 3.5043 vs event 0.02766 ⇒ **126.7×**. Rounding artefact, not a defect.
- 03:135 says the cited run is "300-path"; 04's script uses 400 paths. Mismatch noted with defect #1.

---

## 1. Spelling / typos in prose

**No typos found.** Full token sweep of all seven files (code fences, `$…$` math, and wikilink targets stripped) produced 1754 distinct word forms, every one a valid English word (British spellings — *centred, favourable, popularised, realisations, artefact, rumour, catalogue* — are used consistently throughout). No doubled words, no misspellings. Proper nouns all correct: *Hilpisch*, *Halls-Moore*, *López de Prado*, *Almgren & Chriss*, *Tóth*, *NautilusTrader*, *Backtrader*, *VectorBT*, *QuantStart*, *Cerebro*, *yhilpisch/py4at*.

---

## 2. MATH — verification of every boxed/claimed formula

### VERIFIED CORRECT
- **index:40** next-event advance $t_{k+1}=\min\{t(e)\}$; documented pop order `MARKET, ORDER, FILL, MARKET, MARKET` — reproduced exactly by the index code. ✓
- **index:41 / 02:37** total order $e_1\prec e_2\iff(t_1,p_1,s_1)<_{\text{lex}}(t_2,p_2,s_2)$. ✓
- **index:43 / 03:40** latency decomposition $\tau=\tau_{\text{struct}}+\tau_{\text{wire}}+\tau_{\text{queue}}$, $\tau_{\text{struct}}=1$. ✓
- **index:44** passive fill condition $\exists t\ge t_s+\tau:\text{ask}(t)\le L$. ✓
- **index:45 / 03:116 / 05:39** shortfall $\text{IS}=10^4\operatorname{sgn}(P_{\text{fill}}-P_{\text{dec}})/P_{\text{dec}}$; table 1.99 / 20.92 / 47.81 / 74.70 bps — all four recomputed exactly (100.42→1.9920, 100.61→20.916, 100.88→47.809, 101.15→74.701). ✓
- **index:46 / 03:54** $\mathbb{E}|\Delta S|=\sigma S\sqrt{2\tau/\pi}$; $\sigma{=}.2,S{=}100,\tau{=}1/252\Rightarrow1.00524$ (stated 1.0052); MC 1.0066 ⇒ 0.135% agreement (stated 0.14%). ✓
- **index:47 / 05:43** $q_{\text{fill}}=\min(q_{\text{target}},\rho V_{\text{bar}})$; 50,000 into $\rho V_{\text{bar}}{=}1{,}000\Rightarrow50$ bars. ✓
- **index:48** $B=\lceil q/(\rho V_{\text{bar}})\rceil$; 50 bars = 5.0 days @10 bars/day. ✓
- **index:49 / 04:55** $\widehat{SR}=\sqrt{A}\,\hat\mu/\hat\sigma$. ✓
- **index:57-59 / 04:167-171** headline table +889.41% / 3.50, +46.40% / 0.55, +0.92% / 0.03 — reproduced **exactly** by 04's script. ✓
- **index:61** "$116\times$" — internally consistent with 04:186 (rounded; see observation). ✓
- **index:144 / 05:31** random-walk naive +3.435 vs honest +0.028 — reproduced exactly by 01's script. ✓
- **02:43** priority lattice MARKET(0)≺SIGNAL(1)≺ORDER(2)≺FILL(3). ✓
- **02:49** loop invariant. ✓
- **03:28,34** next-event advance; $E=B+n_s+n_o+n_f$, $O(E\log N)$. ✓
- **03:44,48** $t_{\text{fill}}=\min\{t\ge t_{\text{act}}\}$, $t_{\text{fill}}\ge t_s+1$. ✓
- **03:60** determinism $\partial\text{trace}/\partial\text{wall-clock}=0$. ✓
- **03:149** order-lifecycle FSM (PENDING_NEW→OPEN→PARTIALLY_FILLED→FILLED; OPEN→CANCELLED/EXPIRED). ✓
- **04:31,41,47,55** vectorized product form; state recursion $\sigma_{t_{k+1}}=\mathcal F(\sigma_{t_k},e^*)$; three-engine decomposition; Sharpe identity. ✓
- **04:49** look-ahead worth 3.50→0.55, execution fictions 0.55→0.03. ✓
- **05:35** $P_{\text{mid}}=P$, $P_{\text{cross}}=P+\tfrac12\text{spread}$, $P_{\text{slip}}=P+\tfrac12\text{spread}+\delta$. ✓
- **05:125** ~2 bps × 252 = ~5%/yr. ✓
- **06:28** tail ratio $\tau_{p99.9}/\tau_{p50}$; "convex in delay" with $\sigma S\sqrt\tau$. ✓
- **06:34** square-root law $\Delta P/P=Y\sigma\sqrt{Q/V}$; cost $Q\cdot\Delta P\propto Q^{3/2}$ convex (doubling ⇒ 2.83×). ✓
- **06:40** $\Pr(\text{fill})=1-\sum_{k=0}^{\lceil q/s\rceil-1}(\lambda\tau)^k e^{-\lambda\tau}/k!$ — correct and reproduced exactly (0/250/500/1000/2000/4000 ⇒ 1.000/0.997/0.971/0.542/0.003/0.000). ✓
- **06:46** $\text{run}=\Phi(\text{data},\text{seed},\theta)$. ✓

### ERRORS
1. **03-the-event-loop.md:135** — *"the shortfall grows roughly like $\sqrt{\text{delay}}$ … rising from 18.81 bps (delay 1) to 25.13 bps (delay 100)"*. A $\sqrt{}$ law over a 100× delay is a **10×** rise; the quoted numbers give **1.34×** (25.13/18.81). The hub's own shortfall column rises 37.5× over the same interval, so no page supports the claim. The cited experiment ("A full 300-path simulation of the momentum strategy in 04") is not in 04 (400 paths, no shortfall metric). Either the scaling sentence or the two bps figures must be corrected; as written they are mutually inconsistent and unreproducible.
2. **01-from-zero-intuition.md:47** — *"$P_{\text{fill}}=S^{\text{ask}}_{t+\tau}(1+s)$ … where … $s$ is the spread-half you cross"*. Filling at the ask **already** crosses the half-spread (05:35: $P_{\text{cross}}=P_{\text{mid}}+\tfrac12\text{spread}$). Multiplying the ask by $(1+s)$ pays $P_{\text{mid}}(1+\tfrac32\text{spread})$. Correct form: $P_{\text{fill}}=S^{\text{ask}}_{t+\tau}$ with $s$ dropped, **or** $P_{\text{fill}}=S^{\text{mid}}_{t+\tau}(1+s)$ with the superscript changed to mid.

---

## 3. CODE — execution results

**Python blocks run: 7 / 7.** Every block executed (`python3`, stdlib only) with rc=0.

| File | Block | Result |
|------|-------|--------|
| index.md | event-queue trace + shortfall + heap/list bench | **EXACT** on trace and shortfall (4/4 bps). Bench heap=41.3 ms, list=83.9 ms, ratio **2.03×** vs fence 2.07× — wall-clock, within declared ±20%. |
| 01 | random-walk look-ahead demo (300 paths) | **EXACT** — naive +3.435, honest +0.028 (byte-for-byte). |
| 02 | 5-component mini-engine trace | **EXACT** — full 8-line log, `final position = 100 cash = 89,948.00`. |
| 03 | tie-break trace + bench + shortfall | **EXACT** on trace (`['MARKET0','ORDER','FILL','MARKET1','MARKET2']`) and shortfall. Bench heap=41.0 ms, list=87.0 ms, ratio **2.12×** vs fence 2.07× — wall-clock, OK. |
| 04 | 3-engine comparison (400 paths × 1500 bars) | **EXACT** — 889.41% / 3.50, 46.40% / 0.55, 0.92% / 0.03 (precise 3.5043 / 0.5486 / 0.02766). |
| 05 | fill cost + capacity + survivorship | **EXACT** — 0.00/1.00/2.00 bps; 50 bars; +19.7% vs +54.8%, +29.2% inflation. |
| 06 | latency tail + Poisson fill prob | **EXACT** — table and all six queue probabilities reproduced. |

**Benchmark classification.** Only two values are machine-dependent: the heap-vs-sorted-list wall-clock timings and their ratio in **index** (fence 2.07×→run 2.03×) and **03** (fence 2.07×→run 2.12×). Both are explicitly labelled wall-clock with a stated ±20% swing; the durable claim (heap $O(\log N)$ vs sorted-list $O(N)$ insert/pop, ratio ≈2×) holds on this machine. **Not defects.**

**All deterministic blocks reproduce byte-for-byte**, including the three-engine 400-path Sharpe table (defect #3 concerns a prose claim *about* a variant of the 02 engine, not the fence output — I re-ran the engine with the netting removed to test it).

---

## 4. COHERENCE

1. **Hub ↔ 01 prereq:** ✓ index.md:12 correctly scopes folder-level prerequisites to pages 02–06 and notes page 01 states its own smaller entry requirements; 01:11 indeed declares "None". 02:11 → 01; 03:12 → 02; 04:11 → 03+02; 05:12 → 04+hygiene; 06:12 → 05+03. Chain is consistent.
2. **Jargon:** event queue, priority lattice, loop invariant, next-event time advance, activation time, shortfall, participation cap, mark-to-market, event sourcing, square-root impact law, lognormal/Poisson — all used precisely and defined on first use. ✓
3. **Wikilinks:** all **23** distinct out-link targets resolve to existing files (checked against the content tree). ✓
4. **Structure:** index hub + exactly 6 sub-pages, `index.md` is the section hub, sub-page cross-links (Back/Continue/Sibling) all present. ✓
5. **ERROR (02:161):** the trace-point-3 claim of a "10× position" from missing in-flight netting is contradicted by the page's own engine — see defect #3. The genuine failure of missing netting (skipped SELL → position left open) is *the opposite* of the described symptom.
6. **ERROR (index:51):** "roughly an order of magnitude" vs the 116× (precise 127×) figure on the same page — see defect #4.
7. **Cross-page number consistency:** otherwise good — 3.50/0.55/0.03, 3.435/0.028, 50,000→50 bars, +29.2%, 1.3×/12.0×, and the shortfall column all agree between hub and sub-pages.

---

## Recommendation
- **03:135** — drop the $\sqrt{\text{delay}}$ characterisation or replace it with the actual scaling; and either supply the missing shortfall simulation or remove the "18.81 → 25.13 bps / 300-path" sentence (it conflicts with the hub's own shortfall table and with 04's 400-path script).
- **01:47** — remove the redundant $(1+s)$ (or change $S^{\text{ask}}$ → $S^{\text{mid}}$) so the spread is crossed exactly once, matching 05:35.
- **02:161** — restate trace point 3 to the failure the engine actually exhibits (missing netting drops the flattening SELL and mis-states inventory), and drop the unsupported "10× / every naive engine" absolute.
- **index:51** — align "roughly an order of magnitude" with the "$116\times$" (≈two orders) stated at index:61 and 04:186.

The event-loop ordering, event-time vs wall-clock advance, latency accounting, fill-capacity arithmetic, mark-to-market, determinism, and shortfall arithmetic are all correct and reproduced by execution; the defects are confined to two prose claims, one boxed-formula symbol, and one cross-page magnitude inconsistency.

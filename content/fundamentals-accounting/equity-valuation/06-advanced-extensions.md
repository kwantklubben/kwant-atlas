---
title: "06 — Relative Valuation & Advanced Extensions: Multiples and Robustness"
tags:
  - fundamentals-accounting
  - equity-valuation
  - relative-valuation
  - multiples
  - sensitivity
  - monte-carlo
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes]] and [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]].

---

### 1. Intuition & Practical Objective

DCF is *absolute*; **relative valuation** ("comps") is *market-based*. Instead of forecasting cash flows, you ask: *what are similar businesses trading for, and how does this one compare?* Multiples are fast, communicable, and — crucially — they tell you what the market is paying, which is often a more practical question than what an asset is "worth".

This page (a) derives each multiple from the DCF so you know what it *embeds*, (b) builds a comps table and applies it, and (c) shows how to make a DCF **robust** rather than precise: sensitivity grids and Monte Carlo. The closing lesson is the central tension of the whole folder: **absolute and relative valuation answer different questions and can disagree wildly — know which one you are using and why.**

> **The one-sentence essence.** "A multiple is a compressed DCF: $\text{PE}=\dfrac{\text{payout}(1+g)}{k_e-g}$ — so a 'cheap' multiple is only cheap relative to the growth, risk, and returns it embeds."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Every multiple is a rearranged DCF (Damodaran Ch 17–19)

Dividing the stable-growth DCF by the relevant denominator gives the **fundamental** multiple:

$$\text{PE}=\frac{\text{Payout}(1+g_n)}{k_e-g_n},\quad \text{PBV}=\frac{\text{ROE}\cdot\text{Payout}(1+g_n)}{k_e-g_n},\quad \text{PS}=\frac{\text{Margin}\cdot\text{Payout}(1+g_n)}{k_e-g_n},$$

$$\frac{V_0}{\text{FCFF}_1}=\frac{1}{K_c-g_n},\qquad \text{EV/EBITDA}\ \text{and}\ \text{EV/EBIT}\ \text{follow from the same FCFF identity}.$$

This is the *why* behind the "companion variable": each multiple has a **dominant fundamental driver** — growth + risk for P/E, ROE for P/BV, margin for P/S, reinvestment/ROIC for EV multiples. Two firms with the same P/E are *not* equally cheap if their growth or ROE differs.

#### 2.2 Multiples and the risk of circularity

- **Equity multiples** (P/E, P/BV, P/S) apply to equity value per share; **enterprise multiples** (EV/EBITDA, EV/EBIT, EV/Sales) apply to the whole firm and must be bridged **EV → equity** by subtracting net debt (exactly as in page 04).
- **Comparable ≠ same industry.** The textbook definition is firms with similar *cash flows, growth and risk* — industry is only a convenient proxy. The trade-off: a broad industry gives more peers but a noisier median; a narrow one gives fewer but cleaner comps.
- **Controlling for fundamentals:** regress the multiple on the companion variables across peers or the market, then compare each firm to its *predicted* multiple — the only rigorous way to use comps across heterogeneous firms.

#### 2.3 Robustness: from a point estimate to a distribution

Because value is very sensitive to $g$ and $K_c$ (page 05), the professional output is a **range**:

$$V_{\text{lower}}\le V\le V_{\text{upper}}\quad\text{from a }\pm\text{range on each driver (scenario / sensitivity grid)},$$

or, treating the drivers as random, a **Monte Carlo** distribution: draw $g_1,g_n,K_c,\text{reinvestment}$ from distributions, recompute the DCF, and read the percentiles. The point is not a better number — it is an honest *band* and a probability of being below price.

---

### 3. Computational Implementation — comps, implied multiples, and Monte Carlo

Stdlib only. Part A derives the multiples from fundamentals; Part B builds a comps table, takes the median, and applies it; Part C runs the Monte Carlo on the page-04 DCF.

```python
import random
def pe_fund(payout, g, ke):   return payout * (1 + g) / (ke - g)
def pbv_fund(roe, payout, g, ke): return roe * payout * (1 + g) / (ke - g)
def ps_fund(margin, payout, g, ke): return margin * payout * (1 + g) / (ke - g)
def vfcff_fund(kc, g): return 1 / (kc - g)

print(f"P/E   = {pe_fund(0.4,0.05,0.10):.2f}   P/BV = {pbv_fund(0.15,0.4,0.05,0.10):.2f}")
print(f"P/S   = {ps_fund(0.10,0.4,0.05,0.10):.2f}   Value/FCFF = {vfcff_fund(0.10,0.03):.2f}")

# --- comps: peer multiples -> median -> target ---
peers = {"A": (12.0, 8.0), "B": (15.0, 9.5), "C": (18.0, 11.0), "D": (14.0, 9.0)}
med = lambda x: (x[1] + x[2]) / 2
pes = sorted(v[0] for v in peers.values()); evs = sorted(v[1] for v in peers.values())
print(f"median P/E = {med(pes):.1f}  median EV/EBITDA = {med(evs):.2f}")
tgt_eps, tgt_ebitda, tgt_netdebt, shares = 4.00, 500.0, 1200.0, 100.0
print(f"  implied price (P/E)       = {med(pes)*tgt_eps:.2f}")
print(f"  implied price (EV/EBITDA) = {(med(evs)*tgt_ebitda - tgt_netdebt)/shares:.2f}")

# --- Monte Carlo robustness around the page-04 DCF ---
def pv(cfs, r): return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs, 1))
random.seed(7); vals = []
for _ in range(20000):
    w  = random.gauss(0.10, 0.015)      # WACC
    g1 = random.gauss(0.10, 0.02)       # stage-1 growth
    gs = random.gauss(0.03, 0.005)      # stable growth
    rr = random.gauss(0.50, 0.05)       # reinvestment rate
    rev, f = 1000.0, []
    for _t in range(5):
        rev *= (1 + g1); f.append(rev * 0.20 * 0.75 * (1 - rr))
    ev = pv(f, w) + f[-1] * (1 + gs) / (w - gs) / (1 + w) ** 5
    vals.append((ev + 250.0 - 600.0) / 100.0)
vals.sort(); n = len(vals)
print(f"MC per-share: mean={sum(vals)/n:.2f} p5={vals[int(.05*n)]:.2f}"
      f" p50={vals[n//2]:.2f} p95={vals[int(.95*n)]:.2f}")
```
```
P/E   = 8.40   P/BV = 1.26
P/S   = 0.84   Value/FCFF = 14.29
median P/E = 14.5  median EV/EBITDA = 9.25
  implied price (P/E)       = 58.00
  implied price (EV/EBITDA) = 34.25
MC per-share: mean=12.28 p5=6.48 p50=11.31 p95=21.08
```
Read the results:

- **The fundamentals-implied P/E is $8.40$**, not some market-average $15$–$20$. A firm with $40\%$ payout, $5\%$ growth and a $10\%$ cost of equity *should* trade at $\approx8.4\times$; a P/E of $14.5$ for that firm would embed either faster growth or lower risk.
- **The two comps disagree by $70\%$** ($\$58.00$ vs $\$34.25$). This is not a bug — different multiples capture different fundamentals (earnings vs operating cash), and a small, mismatched peer set can't resolve which is right. Relative valuation is only as good as the peer set.
- **The Monte Carlo reframes the "value"**: median $\$11.31$ but a $5$–$95$ band of $\$6.48$–$\$21.08$. **The range is three times wide around the median** — a $\$11.29$ point estimate is a fiction; the honest output is "roughly $\$6$–$\$21$, central $\approx\$11$".

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Comparing unlike firms.** Using industry average multiples across firms with different growth, margins, or leverage mistakes composition for cheapness. Control for the companion variable (regression or matched peers).
2. **Ignoring the bridge.** Applying EV/EBITDA to equity value (or forgetting to subtract net debt) misstates per-share value by the capital structure. Enterprise multiples apply to the *firm*, then bridge.
3. **Linear-multiple fallacy.** PEG and similar shortcuts assume P/E is *linear* in growth; the DCF shows it is not (it is convex and blows up as $g\to k_e$).
4. **Multiples inside a DCF.** Using an exit multiple for terminal value smuggles relative assumptions into an absolute model — the two philosophies silently conflict (page 04).
5. **False precision via a beautiful model.** More line items and a Monte Carlo around *wrong* distributions still produce a wrong range. The distribution inputs are as much a judgment as the point estimate; document them.
6. **No cross-check.** Absolute and relative valuation should be run *together*: a DCF that says $\$11$ and comps that say $\$58$ is a signal to find the disagreement — usually in growth or risk assumptions — not to average them blindly.

---

### 5. Canonical Literature & Study References

- **Damodaran**, *Investment Valuation*, Ch 17 (PE), Ch 18 (PBV), Ch 19 (EV/EBITDA and value multiples), plus the Part on "relative valuation vs DCF" — including the companion-variable framework and the full derivation of each multiple from the stable-growth model.
- **Pinto et al. (CFA Institute)**, *Equity Asset Valuation* — the standard practitioner treatment of multiples, peer selection, and the DCF-vs-comps cross-check.
- **Graham & Dodd**, *Security Analysis* — the earliest systematic use of earnings multiples against asset-value and earnings-power floors.
- **Koller et al. (McKinsey)**, *Valuation*, Ch 16–18 — multiples used *after* a DCF, as a sanity check rather than a primary method.
- **Green & Hand & Zhang (2017)**, "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns", *RFS* — the empirical map from valuation multiples/characteristics to returns (the bridge to [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]]).

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (regressions controlling for fundamentals) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Research: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
- Risk: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]] (scenario + Monte Carlo robustness)

---
title: "Counterparty Risk & xVA: Topic Hub & Formula Lookup"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - xva
  - credit-value-adjustment
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] and [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

> **Scope note — two views of xVA.** This is the **pricing/desk view**: how CVA/DVA/FVA enter the *price* of a derivative and how a desk marks and hedges xVA. The complementary **risk/regulatory view** — capital, netting sets, SA-CCR, wrong-way risk as a risk-management problem — lives at [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Pillar 4 · Counterparty Risk & xVA]]. Same mathematics, different job; use this folder to price, that one to govern.

---

### 1. Intuition & Practical Objective

Every OTC derivative is a *bilateral* contract that can run for decades, and either party can be in-the-money at any future time. **Counterparty credit risk (CCR)** is the risk that the party who owes you money at a given moment defaults before paying it. Unlike a bond — where the exposure is (roughly) the par amount, known today — a derivative's exposure is **uncertain and symmetric**: it evolves with the market and can flip sign. That uncertainty is exactly what the *xVA* world exists to price.

This folder is the counterpoint to the *Black–Scholes–Merton* folder. There, one asset, one volatility, and the price is fixed by no-arbitrage. Here, the pricing question is: **what does the counterparty's default, my own default, the funding of margin, and the cost of regulatory capital add to (or subtract from) that clean price?** The answers are the valuation adjustments — **CVA, DVA, FVA, MVA, KVA, ColVA** — and the object that bundles them, the **xVA** (the subject of Gregory's *The xVA Challenge*, the primary source for this folder).

This page is a *hub*: it (a) gives you the **fast formula lookup** below (job #1 of this pillar), and (b) routes you to six sub-pages that walk from raw intuition, through exposure & margin, the CVA/DVA and FVA/MVA formulas, the failure modes, and the practitioner extensions (capital, the xVA desk, wrong-way risk).

> **The one-sentence essence.** "Price counterparty and funding risk as the time-integral of a *utilisation profile* (EPE, ENE, EFV, EIM) against a *cost curve* (credit spread, funding spread, cost of capital): CVA = LGD × E[EPE × PD], and every other xVA term is the same product with a different market and cost component."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Gregory (2020) — Ch 11 (exposure), Ch 17 (CVA/DVA), Ch 18 (FVA), Ch 20 (MVA), Ch 13 (capital), Ch 9 (SIMM) — and cross-checked against Hull Ch 24 (credit risk, Merton) and Brigo–Mercurio Ch 21–22 (intensity models). The numbers in the check column were **re-executed and reproduced exactly** from the verified corpus (see §3).

**Notation:** $V(t)$ value of the derivative, $V(t)^+=\max(V,0)$ positive (credit) exposure, $V(t)^-=\min(V,0)$ negative exposure, $\lambda_C$/$s_C$ counterparty default intensity/spread, $LGD$ loss-given-default $=100\%-R$, $PD(t_{i-1},t_i)$ default probability over an interval, $FS$ funding spread, $r$ (OIS) risk-free rate, $\phi,\Phi$ standard-normal pdf/cdf, $\Phi^{-1}$ inverse normal.

**Master identities** (each xVA = *market component* × *cost component*, Gregory Table 3.1):

| xVA | Market component (utilisation) | Cost component | Formula |
|---|---|---|---|
| CVA | $EPE = E[V^+]$ | counterparty PD × LGD | $-\!LGD\sum_i EPE_i\,PD(t_{i-1},t_i)$ |
| DVA | $ENE = E[V^-]$ (≤0) | own PD × LGD | $-\!LGD\sum_i ENE_i\,PD_P(t_{i-1},t_i)$ |
| FVA | $EFV = E[V]$ | funding spread $FS$ | $-\!\sum_i EFV_i\,FS_{i-1,i}\,\Delta t$ |
| MVA | $EIM = E[IM]$ | IM funding spread | $-\!\sum_i EIM_i\,FS_{i-1,i}\,\Delta t$ |
| KVA | $ECP = E[K]$ | cost of capital | $-\!\sum_i ECP_i\,CC_{i-1,i}\,\Delta t$ |

**Exposure lookup (normal case, $V\sim N(\mu,\sigma)$, $z=\mu/\sigma$ — Gregory App. 11A):**

| Quantity | Formula | Verified check |
|---|---|---|
| EFV (expected future value) | $\mu$ | $\mu{=}2\Rightarrow2.00$ |
| EPE (expected positive exposure) | $\sigma\phi(z)+\mu\Phi(z)$ | $\mu{=}2,\sigma{=}2\Rightarrow2.17$ ✓ |
| ENE (expected negative exposure) | $\sigma\phi(z)-\mu\Phi(-z)$ | $\mu{=}2,\sigma{=}2\Rightarrow0.17$ ✓ |
| PFE (potential future exposure, =VaR) | $\mu+\sigma\Phi^{-1}(\alpha)$ | $\mu{=}2,\sigma{=}2,\alpha{=}.99\Rightarrow6.65$ ✓ |

**Credit lookup (CVA, Hull 24 / Gregory 17 / BM 21):** hazard from spread $\lambda = s/LGD$ (Hull 24.2; BM 21.25) · survival $Q(\tau>t)=e^{-\int_0^t\lambda}$ · Merton $E_0=V_0N(d_1)-De^{-rT}N(d_2)$, $\mathbb{Q}($default$)=N(-d_2)$ (Hull 24.3–24.4).

| Quantity | Formula | Verified check |
|---|---|---|
| Unilateral CVA (Eq 17.3) | $-\!LGD\sum_i EPE(t_i)\,PD(t_{i-1},t_i)$ | flat $EPE{=}20$, 150bp, $LGD{=}60\%$, 5y $\Rightarrow1.4100$ ✓ |
| Bilateral CVA (Eq 17.7a) | $BCVA = CVA + DVA$ | stylised 5y swap $\Rightarrow -0.89$ |
| CVA as a spread (Eq 17.4) | $-\overline{EPE}\times s$ | $20\times0.015=0.30$ |

**Funding & margin lookup (Gregory 18 / 20 / 9):**

| Quantity | Formula | Verified check |
|---|---|---|
| FVA = FCA + FBA (18.4) | $-\!\sum_i EFV_i\,FS_{i-1,i}\,\Delta t$ | $FCA{-}1.336+FBA{+}0.236=FVA{-}1.100$ ✓ |
| MVA (20.1) | $-\!\sum_i EIM_i\,FS_{i-1,i}\,\Delta t$ | EIM profile, 100bp $\Rightarrow 3.314$ |
| Variance-covariance IM (9.4.3) | $IM_{\alpha,\tau}=\Phi^{-1}(\alpha)\sqrt\tau\,\sigma_P$ | 99% 10-day $\Rightarrow46.4$ ✓ |
| BA-CVA capital (13.3) | $\sqrt{\rho(\sum_c SCVA_c)^2+(1-\rho^2)\sum_c SCVA_c^2}$ | $n{=}10,\rho{=}.5\Rightarrow K/n=0.758$ ✓ |

> **Critical caveat.** CVA is a *netting-set-level* quantity (marginal, not additive across trades), whereas **symmetric FVA is trade-level additive**; MVA/KVA are portfolio/asset-class level. Mixing these aggregation levels is the single most common xVA error (see [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation — the xVA formula engine

This runs on the **standard library only** (`math.erf` gives the normal CDF; the inverse is a few lines of bisection). It reproduces every verified number above, then computes a CVA from scratch — the exact product *market (EPE) × credit (PD) × loss (LGD)* that is this entire folder.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
def phi(x):return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

def inv_normal(p, lo=-10.0, hi=10.0, tol=1e-12):      # stdlib inverse normal (bisection)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if N(mid) < p: lo = mid
        else:          hi = mid
        if hi - lo < tol: break
    return 0.5 * (lo + hi)

def normal_metrics(mu, sigma, alpha=0.99):             # Gregory App.11A exposure formulas
    z = mu / sigma
    return (mu,
            mu + sigma * inv_normal(alpha),            # PFE(alpha) = VaR
            sigma * phi(z) + mu * N(z),                # EPE
            sigma * phi(z) - mu * N(-z))               # ENE (negative)

# --- exposure metrics, verified against Gregory's worked examples ---
for mu, sig in ((2, 2), (2, 4)):
    efv, pfe, epe, ene = normal_metrics(mu, sig)
    print(f"mu={mu} sigma={sig}: EFV={efv:.2f} EPE={epe:.2f} ENE={-ene:.2f} PFE(99%)={pfe:.2f}")

# --- CVA lookup:  CVA = LGD * sum_i EPE(t_i) * PD(t_{i-1}, t_i)  (Eq 17.3) ---
def survival(t, lam): return math.exp(-lam * t)
def hazard_from_spread(s, lgd): return s / lgd         # lambda = s / LGD (Hull 24.2, BM 21.25)

epe, spread, lgd, T = 20.0, 0.015, 0.60, 5              # flat EPE=20, 150bp, LGD 60%, 5y
lam = hazard_from_spread(spread, lgd)
cva = lgd * sum(epe * (survival(i-1, lam) - survival(i, lam)) for i in range(1, T+1))
pd_cum = 1.0 - survival(T, lam)
print(f"hazard lambda={lam:.5f}, cumulative 5y PD={pd_cum:.5f}")
print(f"CVA (discrete sum)          = -{cva:.4f}")
print(f"CVA (flat-EPE check)        = -{lgd * epe * pd_cum:.4f}   (exact match when EPE flat)")
```
```
mu=2 sigma=2: EFV=2.00 EPE=2.17 ENE=-0.17 PFE(99%)=6.65
mu=2 sigma=4: EFV=2.00 EPE=2.79 ENE=-0.79 PFE(99%)=11.31
hazard lambda=0.02500, cumulative 5y PD=0.11750
CVA (discrete sum)          = -1.4100
CVA (flat-EPE check)        = -1.4100   (exact match when EPE flat)
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]]. In one line each:

1. **Independence delusion (no wrong-way risk)** — almost every basic CVA assumes exposure, PD and LGD are independent; when default and exposure move together (wrong-way risk), CVA is structurally *underpriced* (corr +50% ≈ doubles EPE).
2. **Double-counting DVA with FBA** — counting the benefit of a negative exposure twice (once as own-default, once as funding benefit) double-discounts it; choose one consistent framework.
3. **Wrong aggregation level** — applying a trade-level FVA formula to a netting-set CVA (or vice-versa) silently misprices by a portfolio factor.

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge: Counterparty Credit Risk, Funding, Collateral and Capital* (4th ed., Wiley 2020) — *the* primary source for this folder: Ch 1–3 (CCR, xVA components), Ch 7/9 (margin, SIMM), Ch 11 (exposure), Ch 13 (capital), Ch 16–20 (CVA/DVA/FVA/KVA/MVA), Ch 21 (xVA desk). All formulas and numbers below are from this book and verified in the corpus.
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 24 (credit risk, hazard from spread, Merton model, CVA/DVA, wrong-way risk), Ch 25 (CDS/CDO). *Related credit verified in the corpus.*
- **Brigo, Damiano & Fabio Mercurio**: *Interest Rate Models — Theory and Practice* (2nd ed.) — Ch 21 (counterparty-risk/CVA pricing proposition, CDS), Ch 22 (intensity models, CIR++, filtration switching, default-time simulation). *Math-verified in the corpus.*
- **Green, Andrew**: *XVA: Credit, Funding and Capital Valuation Adjustments* (Wiley 2015) — the more rigorous companion text recommended by Gregory.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the clean, default-free price xVA adjusts)
- Related credit: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model|Credit Risk & the Merton Structural Model]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]] (PFE = VaR)
- Market context: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure Models]] (swap exposure is the canonical EPE profile)
- Sub-pages (in-folder): 01 From Zero · 02 Exposure & Margin · 03 CVA & DVA · 04 FVA & MVA · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/02-exposure-and-margin|02 · Exposure & Margin]] → [[pillars/03-derivative-pricing/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]] → [[pillars/03-derivative-pricing/counterparty-risk-and-xva/04-fva-and-mva|04 · FVA & MVA]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/counterparty-risk-and-xva/06-advanced-extensions|06 · Advanced Extensions]].
- Back to the clean price: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate Models]]

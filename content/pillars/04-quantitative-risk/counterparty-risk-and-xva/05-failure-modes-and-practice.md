---
title: "4.7.5 Failure Modes & Practice"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - wrong-way-risk
  - jump-to-default
  - failure-modes
  - model-risk
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/counterparty-risk-and-xva/02-exposure-and-ee-epe-pfe|02 · Exposure & EE/EPE/PFE]] and [[pillars/04-quantitative-risk/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]].

---

### 1. Intuition & Practical Objective

Every CVA formula in this folder rests on one hidden assumption: that **exposure, default probability and LGD are independent**. Real counterparties break that assumption. This page names the ways the standard model fails, so a practitioner knows *which* number to distrust and *how much* it moves.

The failures, in one line each:

1. **Wrong-way risk (WWR)** — exposure is *high* exactly when the counterparty is *likely to default*. The independence assumption is false, and CVA is understated.
2. **Exposure misestimation** — EPE is a model output; understate volatility, correlations, or path dependence and CVA falls proportionally.
3. **Jump-to-default (JTD)** — credit deteriorates not continuously but in *jumps*; a jump defeats collateral, defeats Greek hedging, and dominates the tail.
4. **Collateral false comfort** — margin works beautifully against *continuous* moves and is nearly useless against a correlated *jump*.

> **The headline number.** Take the ATM forward (150bp spread, LGD 60%) whose independent CVA is **−1.05**. Add a *mild* positive dependence between exposure and default intensity, and CVA rises to **−2.54** (2.4×) and then **−3.69**. The same trade, a different assumption about correlation — and correlation is precisely the parameter you cannot estimate reliably.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 General vs specific wrong-way risk

Gregory (Table 17.7) splits WWR into two kinds:

- **General WWR** — *macro-driven*: exposure and credit quality co-move with the economy (e.g. a sovereign paying local currency on an FX swap). Detectable historically, priceable.
- **Specific WWR** — *structural, trade-specific*: the derivative *itself* ties your exposure to the counterparty's fate (e.g. buying protection on a name from a counterparty that *is* that name). Hard to detect, dangerous with naive correlations — **to be avoided, not modelled**.

#### 2.2 Quantifying WWR: conditional EPE

The independent CVA formula uses $\text{EPE}(t,t_i)$, the *unconditional* expected exposure. WWR replaces it with the exposure **conditional on default at that date**:

$$
\text{CVA}^{\text{WWR}}=-\text{LGD}\sum_i \text{EPE}\!\left(t,t_i \mid t_i=\tau_C\right)\text{PD}(t_{i-1},t_i).
$$

A single dependence parameter drives a conditional-EPE formula (Gregory Appendix 17F): at a correlation of $+50\%$ the conditional EPE roughly **doubles**; at $-50\%$ it at least **halves**. The critical and counter-intuitive result: **WWR increases as counterparty credit quality improves** — the default of a strong name is a bigger shock, so a portfolio of *AAA* counterparties can carry the largest relative WWR.

#### 2.3 Jump-to-default

Strong empirical support for jumps (Gregory §17.6.4): implied quanto jumps in CDS markets of **83% for AAA** and **27% for BBB** sovereigns (Levy–Levin 1999); euro-crisis EUR/USD jumps of 9–25% for Greece/Italy/Spain/Germany; Chung–Gregory (2019) financials 13.5%, non-financials 8%, sovereign 38.4%. Pure intensity models **cannot** reproduce this (Ehlers–Schönbucher 2006) — the exposure must be allowed to *gap*, not just diffuse, on the default event.

**Jump-to-default P&L** for a hedged book (Gregory Eq 21.2):
$$
\text{JTD P\&L}=-\underbrace{\text{current exposure}\times\text{LGD}}_{\text{loss on default}}+\underbrace{\text{CDS notional}\times\text{CDS LGD}}_{\text{hedge payoff}}-\underbrace{\text{current CVA contribution}}_{}.
$$
A CDS hedge of the *wrong maturity* leaves JTD risk; buying short-dated protection is the (rarely available) fix.

#### 2.4 Why collateral fails against WWR

Collateral is a *timing* hedge. If exposure approaches its peak **gradually**, margin can be posted along the way and protects you. If exposure **jumps** — as it does on a correlated default — the margin posted before the jump is based on the *pre-jump* value and is grossly insufficient. Pykhtin–Sokol (2013) show that with jumps and elevated post-default volatility, WWR erodes the collateral benefit, and it matters most for the **systemic** banks that post the most margin (Gregory §17.6.6).

---

### 3. Computational Implementation — wrong-way risk, jumps, misestimation

A path-wise Monte Carlo over the ATM forward where the default intensity is tied to the current exposure, $\lambda_i=\lambda_0\,(1+\text{wwr}\cdot V_i/\text{scale})$ — chosen so the *average* hazard is unchanged (isolating the dependence, not just a higher PD). We also measure the jump case and the misestimation case. Standard library only.

```python
import math, random

def mc_cva(S0, T, r, sig, spread, LGD, wwr=0.0, jump=0.0, nsteps=20, npaths=100000, seed=7):
    """CVA by path-wise MC. Default intensity lambda_i = lambda0*(1 + wwr*V_i/scale),
       optionally with an adverse jump of size `jump` in exposure at the default date."""
    K = S0*math.exp(r*T); random.seed(seed); dt = T/nsteps
    lam0 = spread/LGD; scale = S0*sig*math.sqrt(T)
    tot = 0.0; expo_sum = 0.0; def_sum = 0.0; n_def = 0
    for _ in range(npaths):
        S = S0; alive = True
        for i in range(1, nsteps+1):
            t = i*dt
            S *= math.exp((r-0.5*sig**2)*dt + sig*math.sqrt(dt)*random.gauss(0,1))
            V = S - K*math.exp(-r*(T-t))
            lam = max(1e-9, lam0*(1.0 + wwr*V/scale))
            if alive and random.random() < 1.0-math.exp(-lam*dt):
                loss = max(V*(1.0+jump), 0.0)
                tot += math.exp(-r*t)*loss; n_def += 1
                expo_sum += V; def_sum += 1.0
                alive = False
    return -LGD*tot/npaths, n_def/npaths, (expo_sum/max(def_sum,1))

S0, T, r, sig, LGD = 100.0, 5.0, 0.03, 0.25, 0.60
print("CVA vs strength of exposure / default-intensity dependence (150bp, LGD 60%):")
for wwr in (-1.0, 0.0, 1.0, 2.0):
    c, pd, mE = mc_cva(S0, T, r, sig, 0.0150, LGD, wwr=wwr)
    print(f"  wwr={wwr:+.1f}: CVA = {c:8.4f}   cumulative PD={pd:.4f}   E[exposure|default]={mE:7.3f}")
print("wrong-way jump in exposure at default (wwr=0):")
for j in (0.0, 0.15, 0.30, 0.50):
    c,_,_ = mc_cva(S0, T, r, sig, 0.0150, LGD, jump=j)
    print(f"  jump={j:.0%}: CVA = {c:8.4f}")
print("exposure-model (vol) misestimation, true sigma = 25%:")
for sm in (0.15, 0.20, 0.25, 0.35):
    c,_,_ = mc_cva(S0, T, r, sm, 0.0150, LGD)
    print(f"  model sigma={sm:.0%}: CVA = {c:8.4f}")
```
```
CVA vs strength of exposure / default-intensity dependence (150bp, LGD 60%):
  wwr=-1.0: CVA =  -0.1933   cumulative PD=0.1250   E[exposure|default]=-24.053
  wwr=+0.0: CVA =  -1.0512   cumulative PD=0.1185   E[exposure|default]= -0.216
  wwr=+1.0: CVA =  -2.5448   cumulative PD=0.1164   E[exposure|default]= 35.219
  wwr=+2.0: CVA =  -3.6941   cumulative PD=0.1293   E[exposure|default]= 51.170
wrong-way jump in exposure at default (wwr=0):
  jump=0%: CVA =  -1.0512
  jump=15%: CVA =  -1.2089
  jump=30%: CVA =  -1.3666
  jump=50%: CVA =  -1.5769
exposure-model (vol) misestimation, true sigma = 25%:
  model sigma=15%: CVA =  -0.6358
  model sigma=20%: CVA =  -0.8447
  model sigma=25%: CVA =  -1.0512
  model sigma=35%: CVA =  -1.4554
```
Read the three blocks:

- **WWR.** The cumulative PD is held nearly constant across rows (~12%), so the change is *pure dependence*: at `wwr = 0` the E[exposure | default] is ≈ 0 (independence, CVA −1.05); at `wwr = +1` the conditional exposure is **+35** and CVA more than doubles to **−2.54**. Negative dependence (right-way risk) shrinks CVA to **−0.19**.
- **Jump.** A 30% adverse jump on the default date raises CVA by **30%** (−1.05 → −1.37); a 50% jump by **50%**. Jumps are a first-order effect, not a correction.
- **Misestimation.** A model that uses $\sigma=15\%$ on a true $\sigma=25\%$ world reports CVA **40% too low** (−0.64 vs −1.05) — and a *conservative* $\sigma=35\%$ overstates it by 38%. The error is roughly linear in volatility.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Wrong-way risk is unhedgeable in the tail.** No single-name hedge removes a *correlated* default: the CDS protection pays precisely when the exposure jumps above its hedged level. Prefer to **avoid** specific WWR structurally (exclude legally connected trades from the netting set; SA-CCR sets EAD = 100% of value with LGD = 100% in these cases).
2. **Correlation is not independence.** Zero correlation is *not* the same as independence ($Y=X^2$ has zero correlation but total dependence). Reporting a zero WWR parameter as "no WWR" is a category error (Gregory §17.6.2).
3. **Jump-to-default defeats the Greeks.** A delta/CS01 hedge is calibrated to *diffusive* moves; the default event is a jump in a different risk factor. It must be managed with explicit **JTD limits**, not delta (Gregory §21.2.5).
4. **Collateral is a timing hedge, not a default hedge.** Against a gradual exposure, margin protects; against a correlated jump it does not. Assuming collateral eliminates WWR is the most expensive mistake on this page (Pykhtin–Sokol 2013).
5. **Exposure model risk.** Vols, correlations, grid resolution and path-dependence modelling all feed EPE, and errors are roughly proportional. A conservative exposure model is cheaper than an understated CVA.
6. **Data is uninformative.** Credit-quality/exposure co-movement is rare and regime-dependent; historical correlation estimates are noisy and backward-looking. This is why WWR is often addressed by *structure* (avoidance, limits, conservative add-ons) rather than by a correlation parameter.

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge* (5th ed., 2025) — §17.6 (WWR: general vs specific, quantification, intensity vs structural, jump approaches, collateral, CCPs), §13.4.7 (regulatory WWR), §21.2.5 (jump-to-default risk). *Deep-read and numerically re-verified in the corpus.*
- **Pykhtin & Sokol** (2013): *Modelling Wrong-Way Risk and Credit Valuation Adjustment* — the reference treatment of jumps and the erosion of collateral benefit.
- **Levy & Levin** (1999) / **Chung & Gregory** (2019): empirical implied sovereign-jump magnitudes (the evidence base for §2.3).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 24 §24.7 (wrong-way / right-way risk); **Hull & White** (2011): a parametric PD–exposure link calibrated by what-if analysis.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/04-collateral-netting-and-sa-ccr|04 · Collateral, Netting & SA-CCR]]
- Forward: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/06-advanced-extensions|06 · Advanced Extensions (FVA/MVA, WWR modelling)]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] (jump/tail modelling) · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]]

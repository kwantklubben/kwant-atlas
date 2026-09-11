---
title: "03 — Climate Scenarios & Stress Testing: NGFS, CBES, PACTA & Scenario VaR/ES"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - climate-stress-testing
  - ngfs-scenarios
  - scenario-analysis
  - pacta
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · Physical & Transition Risk]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (the quantile integral definition of ES is used verbatim).

---

### 1. Intuition & Practical Objective

Because climate risk has no stationary history, the entire supervisory apparatus converged on one instrument: **the scenario**. A climate stress test does not estimate a probability; it asks *"if the world takes this policy path, what is the portfolio loss?"* — and then asks that question several times, for paths chosen to span the *space of decisions* rather than the space of samples.

Three families define the practice:

- **NGFS scenarios** (Network for Greening the Financial System, produced with an academic consortium including the Potsdam Institute). NGFS sorts scenarios into **orderly** (policies introduced early and gradually tightened — e.g. *Net Zero 2050*), **disorderly** (delayed or divergent policy — e.g. *Delayed Transition*, *Divergent Net Zero*) and **hot house world** (insufficient global effort — e.g. *Current Policies*, *Nationally Determined Contributions*). The organising insight is that **transition and physical risk trade off along the scenario axis**: act early and you pay transition cost; act late and you pay physical damage *plus* a sharper transition cost.
- **The Bank of England's CBES** (Climate Biennial Exploratory Scenario, 2021, results 2022) applies that logic to the UK's largest banks and insurers under three scenarios — **early action**, **late action** and **no additional action** — and is the template for supervisory climate stress testing.
- **PACTA** (Paris Agreement Capital Transition Assessment, originally 2° Investing Initiative, stewardship moved to RMI in 2022) is a *forward-looking alignment* method rather than a loss simulation: it compares a portfolio's sector/technology **production exposure** against the sectoral pathways needed for a temperature target, using companies' five-year production plans.

The practical objective of this page is to assemble those narratives into a **proper risk measure**: a bottom-up scenario P&L engine, the scenario distribution's VaR and ES, and the honest statement of what a finite scenario set can and cannot resolve.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The scenario measure

A scenario set is a finite probability space $(\Omega_s,\mathcal F_s,\mathbb Q)$ with $\Omega_s=\{1,\dots,N\}$, $\mathbb Q(\{k\})=q_k>0$, $\sum_k q_k=1$. Each scenario $k$ carries a shock triple $(\Delta p_k,\Delta T_k,m_k)$ — carbon price, warming, market return — and each holding $i$ has exposures $(b^c_i,b^p_i,\beta_i)$. The portfolio scenario return is the bottom-up identity

$$
\boxed{\ R_k=\sum_i w_i\left(b^c_i\frac{\Delta p_k}{100}+b^p_i\,\Delta T_k+\beta_i\,m_k\right),\qquad L_k=-R_k\ }
$$

The loss distribution is then the discrete law $\mathbb Q\circ L^{-1}$, and the measures are the *same* functionals used for market risk — the discretisation changes, not the mathematics:

$$
\mathrm{VaR}_\alpha(L)=\inf\{l:\mathbb Q(L>l)\le1-\alpha\},\qquad
\mathrm{ES}_\alpha(L)=\frac{1}{1-\alpha}\int_\alpha^1\mathrm{VaR}_u(L)\,du .
$$

For a discrete law the quantile integral must be computed on the *probability-mass grid* (the boundary correction that the VaR folder warns about), i.e. $\mathrm{ES}_\alpha=\frac{1}{1-\alpha}\sum_k L_k\,\big[\text{mass of }L_k\text{ beyond }\alpha\big]$.

#### 2.2 The resolution limit of a finite scenario set

Let $p_{\max}=\max_k q_k$ be the largest scenario weight and $L_{\max}$ the worst loss. The quantile is identified by the scenarios for $\alpha\le 1-p_{\max}$, but for
$$
\alpha>1-p_{\max}:\qquad \mathrm{VaR}_\alpha(L)=L_{\max}
$$
because the mass strictly beyond every interior scenario point already exceeds $1-\alpha$. In the code below $p_{\max}=0.20$, so **every confidence level above $80\%$ collapses onto the worst scenario** — $\mathrm{VaR}_{80\%}=20.64\%$ (interior) but $\mathrm{VaR}_{90\%}=\mathrm{ES}_{90\%}=28.02\%=L_{\max}$. A scenario stress test inherits a **hard ceiling on the confidence level it can express**, and a risk report quoting a $99\%$ climate VaR from six scenarios is quoting its worst narrative with a probability label attached.

#### 2.3 Re-introducing the tail: the transition-jump mixture

Return-based risk and scenario risk are reconciled by a **mixture**: most days are ordinary, and with probability $q$ the transition narrative lands as a jump,

$$
L=(1-\textstyle\sum q_j)\,\mathcal N(0,\sigma^2)+\sum_j q_j\,\delta_{J_j},
$$

i.e. an $\varepsilon$-contamination model. Its closed-form ES is a mass-weighted average of the components' tail integrals, so a jump that barely moves the $99\%$ *quantile* moves the $99\%$ *average* substantially — the same asymmetry, and the same tail-blindness lesson, as the VaR folder ([[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|VaR/ES · 05 · §3]]). That asymmetry is the theoretical reason supervisors moved market-risk capital onto **Expected Shortfall at $97.5\%$** under FRTB (BCBS, 2019): a measure that prices the size of the shock, not just its frequency.

---

### 3. Computational Implementation — scenario losses, scenario VaR/ES and a jump overlay

Panel (A) runs the bottom-up scenario engine over six NGFS-style archetypes, forms the scenario law and computes VaR/ES on it. Panel (B) adds a rare disorderly-transition jump to a daily book and measures how differently VaR and ES respond. Standard library only. Scenario magnitudes are **stylised**, chosen to demonstrate the mechanics — they are not NGFS model outputs.

```python
# c4_stress.py — scenario loss engine + transition-jump ES overlay (page 03 §3)
import math, random

book = [   # name, weight, carbon-price beta (dlnV per +$100/t), physical beta (dlnV per +1C), market beta
    ("Coal utility", 0.10, -0.35, -0.02, 0.8),
    ("Oil major",    0.15, -0.18, -0.03, 0.9),
    ("Cement",       0.05, -0.22, -0.02, 1.0),
    ("Renewables",   0.20, +0.30, -0.05, 1.1),
    ("Real estate",  0.25, -0.05, -0.12, 0.7),
    ("Tech",         0.25,  0.00, -0.01, 1.2),
]
scen = [   # NGFS-style archetypes; magnitudes are illustrative, not NGFS model output
    ("Net Zero 2050      (orderly)",    0.20, 150.0, 1.6,  0.02),
    ("Below 2C / Low Dem.(orderly)",    0.15, 110.0, 1.9,  0.01),
    ("Divergent Net Zero (disorderly)", 0.15, 250.0, 1.7, -0.06),
    ("Delayed transition (disorderly)", 0.20, 350.0, 1.9, -0.10),
    ("NDCs               (hot house)",  0.15,  60.0, 2.7, -0.02),
    ("Current policies   (hot house)",  0.15,  30.0, 3.2,  0.00),
]
print("(A) scenario-conditioned portfolio loss (% of value)")
pmf = {}
for nm, wt, dp, dT, mkt in scen:
    r = sum(w * (bc * (dp / 100.0) + bp * dT + bm * mkt) for _, w, bc, bp, bm in book)
    l = -r
    pmf[round(l, 10)] = pmf.get(round(l, 10), 0.0) + wt
    print(f"    {nm:35s}: {100*l:+7.2f}%")


def var_pmf(pmf, a):
    c = 0.0
    for x in sorted(pmf):
        c += pmf[x]
        if c >= a - 1e-12:
            return x
    return max(pmf)


def es_pmf(pmf, a):
    c = 0.0
    t = 0.0
    for x in sorted(pmf):
        hi = c + pmf[x]
        lo = max(c, a)
        if hi > lo:
            t += x * (hi - lo)
        c = hi
    return t / (1.0 - a)


for a in (0.80, 0.90):
    print(f"    scenario VaR_{a:.0%} = {100*var_pmf(pmf, a):+7.2f}%   ES_{a:.0%} = {100*es_pmf(pmf, a):+7.2f}%")

# (B) a rare disorderly-transition jump inside a daily book
random.seed(42)
N, sig, p_jump, jump = 400_000, 0.0115, 0.005, -0.06
plain, mixed = [], []
for _ in range(N):
    u = random.random(); e = random.gauss(0.0, sig)
    plain.append(-e)                                       # loss = -return
    mixed.append(-(jump if u < p_jump else e))


def var_es(sorted_losses, a):
    n = len(sorted_losses)
    v = sorted_losses[min(n - 1, int(a * n))]
    k = max(1, int((1.0 - a) * n))
    return v, sum(sorted_losses[-k:]) / k


v0, e0 = var_es(sorted(plain), 0.99)
v1, e1 = var_es(sorted(mixed), 0.99)
print("(B) one-day book, 99%, with a 0.5%/day x -6% transition jump")
print(f"    market-only      : VaR = {100*v0:5.3f}%   ES = {100*e0:5.3f}%")
print(f"    with the jump    : VaR = {100*v1:5.3f}%   ES = {100*e1:5.3f}%")
print(f"    change           : VaR {100*(v1/v0-1):+5.1f}%   ES {100*(e1/e0-1):+5.1f}%")
```
```
(A) scenario-conditioned portfolio loss (% of value)
    Net Zero 2050      (orderly)       :   +9.90%
    Below 2C / Low Dem.(orderly)       :  +11.34%
    Divergent Net Zero (disorderly)    :  +20.64%
    Delayed transition (disorderly)    :  +28.02%
    NDCs               (hot house)     :  +16.95%
    Current policies   (hot house)     :  +16.77%
    scenario VaR_80% =  +20.64%   ES_80% =  +28.02%
    scenario VaR_90% =  +28.02%   ES_90% =  +28.02%
(B) one-day book, 99%, with a 0.5%/day x -6% transition jump
    market-only      : VaR = 2.672%   ES = 3.066%
    with the jump    : VaR = 2.947%   ES = 4.607%
    change           : VaR +10.3%   ES +50.3%
```

**Read panel (A) against §2.2.** $\mathrm{VaR}_{80\%}=20.64\%$ is an interior scenario (Divergent Net Zero); $\mathrm{VaR}_{90\%}$ has already collapsed onto $L_{\max}=28.02\%$ (Delayed Transition), exactly the ceiling $\alpha\le1-p_{\max}=0.80$ predicts. **Six scenarios can express a risk appetite up to $80\%$ confidence — no further.** The scenario with the *largest* loss is not the hot-house scenario: a $+3.2^\circ$C world loses $16.77\%$, while a *disorderly* $+1.9^\circ$C world loses $28.02\%$, because the transition shock is concentrated in the decade you hold the assets. That inversion is why the NGFS vocabulary puts "disorderly" beside "hot house world" rather than treating transition risk as the lesser problem.

**Read panel (B) as the tail-blindness lesson.** A $0.5\%$/day chance of a $-6\%$ repricing lifts the $99\%$ VaR by $10.3\%$ — but the $99\%$ **ES by $50.3\%$**, because ES prices the size of the jump and VaR largely only notices that a jump exists ([[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR/ES hub]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Narrative-to-number translation.** Every scenario must become a vector of (\$/t, °C, market) shocks; that translation is economist judgement, not data, and it dominates the answer. Document it.
2. **No probabilities, or false ones.** NGFS scenarios are *not* equiprobable or probability-weighted; if you attach weights (as §3 does, for exposition), you have made a forecast, and the VaR/ES numbers inherit it. State it explicitly or report the loss vector instead of a quantile.
3. **The confidence ceiling.** A finite scenario set pins down $\mathrm{VaR}_\alpha$ only for $\alpha\le1-p_{\max}$ (§2.2). Reporting "99% climate VaR" from six scenarios is the worst narrative wearing a probability label. Report the scenario loss vector and the ceiling.
4. **Incoherent horizons.** A carbon price is a multi-decade path; a market shock is a quarter; combining them into one "scenario return" without a horizon convention makes losses non-comparable across scenarios ([[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · §3]] panel A).
5. **Bottom-up vs aggregate.** Supervisory exercises build losses bottom-up (exposure → shock → loss) precisely because aggregate top-down elasticities hide the composition of the book; a top-down carbon elasticity is a *portfolio summary*, not an exposure, and it cannot see a single stranded asset.
6. **Coverage gaps.** Non-financial corporates, real estate, and counterparty credit lines are commonly modelled coarsely; a portfolio's measured climate risk is bounded by its *least* well-modelled sleeve ([[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]).
7. **No well-defined scenario-weighted ES.** ES on a scenario measure is only coherent if the scenario weights are a genuine probability measure and the loss grid is fine enough that the boundary correction is immaterial; with six atoms, the "ES" of §3 *is* the worst scenario. Say so, and pair it with the jump-mixture view of §2.3 for a tail that is not an artefact of the grid.

---

### 5. Canonical Literature & Study References

- **NGFS**, *Climate Scenarios for Central Banks and Supervisors* (Network for Greening the Financial System; phases I–V) and the NGFS Scenarios Portal — the orderly / disorderly / hot-house-world families. *[REG] primary scenario source.*
- **Bank of England**, *Key Elements of the 2021 Biennial Exploratory Scenario: Financial Risks from Climate Change* (2021) and *Results of the 2021 Climate Biennial Exploratory Scenario* (2022) — early action / late action / no additional action. *[REG]*
- **BCBS**, *Climate-related Financial Risks — Measurement Methodologies* (2021) and *Principles for the Effective Management and Supervision of Climate-related Financial Risks* (2022) — the supervisory framework. *[REG]*
- **ECB**, *ECB Economy-wide Climate Stress Test* (2021) and *2022 Climate Risk Stress Test* (methodology, 2022); **EBA**, *2023 EU-wide Climate Risk Stress Test* — the EU supervisory implementations.
- **PACTA / RMI**, *Paris Agreement Capital Transition Assessment* — forward-looking, production-plan-based portfolio alignment against sectoral pathways.
- **BCBS**, *Minimum Capital Requirements for Market Risk* (2019, d457) — the ES@$97.5\%$ standard that motivates §2.3's tail sensitivity.
- **Rockafellar, R.T. & Uryasev, S.**, *Optimization of Conditional Value-at-Risk*, *Journal of Risk* 2(3):21–41 (2000) — the convex representation that makes scenario-based ES optimisable.
- **TCFD**, *Recommendations* (2017) and *The Use of Scenario Analysis in Disclosure of Climate-related Risks and Opportunities* (Technical Supplement, 2017).

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · Physical & Transition Risk]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/climate-and-esg-risk/04-esg-scores-and-the-carbon-premium|04 · ESG Scores & the Carbon Premium]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Sibling: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (reverse stress testing and scenario construction) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (coherence, the quantile integral) · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] (scenario model risk)
- Forward (portfolio): [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]] (scenario sets as ambiguity sets)

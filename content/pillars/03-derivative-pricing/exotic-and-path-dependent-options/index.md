---
title: "3.7 Exotic & Path-Dependent Options"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - path-dependent-options
  - monte-carlo
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A *vanilla* European option's payoff depends only on the **terminal** stock price $S_T$. An **exotic / path-dependent** option's payoff depends on *more* of the history: the path's **maximum** (lookbacks), its **average** (Asians), whether it **touched a level** (barriers), a **binary event** (digitals), or a **second asset / currency** (exchange, quanto, basket). This is the first big divide in real structuring desks: the moment the payoff references $S_T$ *plus* any other feature of the path or another asset, three things change at once — (1) the closed form (if one exists) gets far more complicated, (2) the natural pricing tool becomes **Monte Carlo over the path**, and (3) the model risk shifts from *volatility* to *correlation and the exact specification of path-monitoring*.

This folder is the lookup hub for the exotic & path-dependent family. It (a) gives the **fast formula lookup** below (job #1 of this pillar), and (b) routes you to six sub-pages: raw intuition, barriers & digitals, lookbacks & Asians, compound/chooser/quanto/exchange, failure modes, and advanced extensions (discrete monitoring & MC for path-dependence).

> **The one-sentence essence.** "An exotic's price is the discounted risk-neutral expectation of a *path-functional* payoff — and the moment the payoff is not a function of $S_T$ alone, you either find a specialized closed form (reflection principle, moment matching) or you simulate the whole path and average."

---

### 2. Mathematical Ground Truth & Lookup

All formulas below are transcribed from Haug (2006) and cross-checked against Shreve Vol II Ch 6–7, Hull Ch 26, and Glasserman Ch 1–3/7–8. Numbers in the check column were **re-executed and reproduced exactly** in this build (see §3).

**Notation:** $S$ spot, $X$ strike, $T$ time to expiry, $r$ risk-free, $b$ cost-of-carry ($b=r-q$ index, $b=0$ futures, $b=r-r_f$ FX), $\sigma$ vol, $N(\cdot)$ normal CDF, $M(a,b;\rho)$ bivariate normal CDF, $H$ barrier, $K$ rebate/digital payout, $\phi=+1$ call/$-1$ put, $\eta=+1$ down/$-1$ up.

| Family | Key formula | Verified check |
|---|---|---|
| **Barrier** (Reiner–Rubinstein $A\dots F$) | $A{-}C{+}F$ (down-and-out call), combination table §2.1 (barriers & digitals) | $c_{do}(H{=}95,\sigma{=}.25)=6.7924$; $c_{ui}(H{=}105)=8.4482$ |
| **In–out parity** | $c_{di}+c_{do}=c_{\text{vanilla}}$ (rebate $K{=}0$) | $3.3368+4.5126=7.8494$ ✓ |
| **Discrete-barrier correction** (Broadie–Glasserman–Kou) | $H_D=H\,e^{\pm\beta\sigma\sqrt{\Delta t}}$, $\beta=0.5826$ | $H_D{=}94.027\Rightarrow$ price $5.9831\approx$ MC $6.0473$ |
| **Cash-or-nothing** | $c=K e^{-rT}N(d)$, $p=K e^{-rT}N(-d)$ | put $=2.6710$ |
| **Asset-or-nothing** | $c=S e^{(b-r)T}N(d)$, $p=S e^{(b-r)T}N(-d)$ | put $=20.2069$ |
| **Floating-strike lookback call** (4.39) | $S e^{(b-r)T}N(a_1)-S_{min}e^{-rT}N(a_2)+\dots$ | $=25.3534$ (book 25.3533) |
| **Geometric Asian** (4.91) | BSM with $\sigma_A=\sigma/\sqrt3$, $b_A=\tfrac12(b-\sigma^2/6)$ | put $=4.6922$ |
| **Arithmetic Asian** (Turnbull–Wakeman) | moment-match $M_1,M_2\to$ BSM form | no closed form; MC $=1.9812$ |
| **Put-on-call compound** (4.29) | bivariate-normal combo + critical $I$ | $=21.1964$, $I{=}538.3165$ |
| **Simple chooser** (4.26) | $c(S,X,T_2)+e^{(b-r)(T_2-t_1)}p(S,Xe^{-b(T_2-t_1)},t_1)$ | $=6.1071$ |
| **Complex chooser** (4.27) | 4-term bivariate-normal combo, critical $I$ | $=6.0508$, $I{=}51.1158$ (Haug 4.27) |
| **Margrabe exchange** (5.7) | $Q_1S_1e^{(b_1-r)T}N(d_1)-Q_2S_2e^{(b_2-r)T}N(d_2)$ | $=1.5260$ |
| **Quanto** (5.39) | $E_p\big[S^*e^{(r_f-r-q-\rho\sigma_S\sigma_E)T}N(d_1)-X^*e^{-rT}N(d_2)\big]$ | call $=5.3280$ |
| **Foreign-equity struck domestic** (5.35) | $\sigma_{ES}=\sqrt{\sigma_S^2+\sigma_E^2+2\rho\sigma_E\sigma_S}$ | call $=8.3056$ |
| **Kirk spread** (5.17) | two-leg BSM with $F=\frac{S_2e^{(b_2-r)T}}{S_2e^{(b_2-r)T}+Xe^{-rT}}$ | call $=2.1670$ |

> **Scaling caveats.** (1) Most exotics collapse to a **BSM-type call/put with adjusted drift/vol** (Asians, quantos, exchange) — always reduce to that first. (2) The lookback and barrier closed forms require the **reflection principle**; a naive "positive-part of the reflected vanilla" misprices the sign of the image term (the verified lookback value needs the `+` sign in the square bracket — flip it and you get $21.35$, not $25.35$). (3) Formulas flagged `[R]` in the source (partial-time lookbacks, double barriers, soft barriers, Curran) are **reconstructed pointers, not verified** — do not quote their digits.

---

### 3. Computational Implementation — the formula engine

Stdlib only (`math.erf` gives the exact normal CDF). The block below is the shared engine; each sub-page embeds a runnable slice that reproduces the numbers above.

```python
import math
from math import log, exp, sqrt, pi

def N(x):   return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
def phi(x): return exp(-0.5 * x * x) / sqrt(2.0 * pi)

def bsm(S, X, T, r, b, sigma, kind):
    """Generalized BSM (cost-of-carry b). kind 'c'/'p'. b=r stock, r-q index,
       0 futures, r-rf FX. Used as the engine for Asian/quanto/exchange exotics."""
    if T <= 0: return max(S - X, 0.0) if kind == 'c' else max(X - S, 0.0)
    d1 = (log(S / X) + (b + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if kind == 'c': return S * exp((b - r) * T) * N(d1) - X * exp(-r * T) * N(d2)
    return X * exp(-r * T) * N(-d2) - S * exp((b - r) * T) * N(-d1)

# Geometric Asian put: BSM with sigma/sqrt(3), b/2 - sigma^2/12  (Haug 4.91)
S, X, T, r, b, sig = 80.0, 85.0, 0.25, 0.05, 0.08, 0.20
sigA = sig / sqrt(3.0);  bA = 0.5 * (b - sig * sig / 6.0)
p = bsm(S, X, T, r, bA, sigA, 'p')
print(f"geometric Asian put = {p:.4f}   (Haug-verified: 4.6922)")
```
```
geometric Asian put = 4.6922   (Haug-verified: 4.6922)
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — full analysis in [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Discrete vs continuous monitoring** — a barrier can be crossed *between* monitoring dates; pricing a discrete barrier with the continuous closed form systematically overvalues knock-outs (the Broadie–Glasserman–Kou shift fixes it).
2. **The correlation trap** — quantos, baskets and spread options live or die on $\rho$; a wrong correlation misprices the convexity terms ($\sigma_2^2T$, $\rho\sigma_1\sigma_2$) that the closed forms carry.
3. **Monte Carlo bias for path-functionals** — pathwise Greeks **fail** for digitals and barriers (the payoff is discontinuous), and MC convergence is $O(n^{-1/2})$ in the number of paths but *slow in the number of monitoring steps* — the two are often conflated.

---

### 5. Canonical Literature & Study References

- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) — Ch 4 §4.12–4.20 (single-asset exotics: chooser, compound, lookback, barrier, binary, Asian), Ch 5 (two-asset: exchange, quanto, spread, basket), Ch 12–13 (basket vol, bivariate normal primitives). *Primary lookup; all quoted digits numerically verified.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance II* — Ch 6 (Feynman–Kac, Asian-option PDE) and Ch 7 (exotics: joint density of max & terminal, knock-out barrier PDE, lookback dimension reduction, Večeř change-of-numeraire). *Math-verified deep-read.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 26 (the 15-family exotic catalog: gap, compound, barrier, binary, lookback, Asian, exchange, rainbow). Ch 27 (MC & trees for path-dependent products, LSM).
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* — Ch 1 (estimator, $O(n^{-1/2})$), Ch 3 (exact GBM path simulation; path-dependent payoffs), Ch 7 (pathwise vs likelihood-ratio Greeks — the failure modes), Ch 8 (American by simulation: LSM, duality).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]] (the vanilla anchor all exotics reduce to)
- Sibling topics: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
- Sub-pages (in-folder): 01 From Zero · 02 Barriers & Digitals · 03 Lookbacks & Asians · 04 Compound/Chooser/Quanto/Exchange · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/02-barriers-and-digitals|02 · Barriers & Digitals]] → [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|03 · Lookbacks & Asians]] → [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange|04 · Compound/Chooser/Quanto/Exchange]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/06-advanced-extensions|06 · Advanced Extensions]].
- Forward: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (model risk for the closed forms) · [[foundations/calculus-and-optimization/index|Multivariable Calculus]]

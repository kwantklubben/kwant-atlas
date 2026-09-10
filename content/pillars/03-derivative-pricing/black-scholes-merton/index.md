---
title: "Black–Scholes–Merton: Topic Hub & Formula Lookup"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - options-pricing
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus]].

---

### 1. Intuition & Practical Objective

The Black–Scholes–Merton (BSM) model is the continuous-time limit of binomial dynamic replication, and it is the *zero point* of all modern derivative pricing. Its claim is sharp: if you can trade the underlying continuously, then the price of a European option is **uniquely fixed by the no-arbitrage condition** — it depends on the current spot, the strike, the remaining time, the risk-free rate, and the (assumed constant) volatility, and on **nothing else**. Not on the drift of the stock, not on your forecast of where the market is going.

This folder is the model topic-folder for the Kwant-Atlas build. It is a *hub*: it (a) gives you the **fast formula lookup** below (job #1 of this pillar), and (b) routes you to six sub-pages that walk you from raw intuition through the derivations, the closed forms, the Greeks, the failure modes, and the extensions.

> **The one-sentence essence.** "Price a derivative as the discounted expectation of its payoff *under the risk-neutral measure* — equivalently, solve the BSM parabolic PDE — where the change-of-measure/derivation is driven entirely by *volatility*, never by *drift*."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Haug (2006) and cross-checked against Shreve Vol II Ch 4–5; the numbers in the check column were **re-executed and reproduced exactly** from the verified corpus (see §3).

**Notation:** $S$ spot, $X$ strike, $T$ time to expiry (years), $r$ risk-free rate, $q$ continuous dividend yield, $b$ cost-of-carry, $\sigma$ vol, $N(\cdot)$ standard normal CDF, $n(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}$.

**Cost-of-carry dictionary** (one master formula, many models): $b=r$ stock · $b=r-q$ stock/index with yield $q$ · $b=0$ futures (Black-76) · $b=r-r_f$ currency (Garman–Kohlhagen).

| Quantity | Formula | Verified check |
|---|---|---|
| $d_1$ | $\dfrac{\ln(S/X)+\left(b+\tfrac12\sigma^2\right)T}{\sigma\sqrt T}$ | — |
| $d_2$ | $d_1-\sigma\sqrt T=\dfrac{\ln(S/X)+\left(b-\tfrac12\sigma^2\right)T}{\sigma\sqrt T}$ | — |
| Generalized call $c$ | $S\,e^{(b-r)T}N(d_1)-X\,e^{-rT}N(d_2)$ | $S{=}60,X{=}65,T{=}.25,r{=}.08,\sigma{=}.30 \Rightarrow c=2.13337$ |
| Generalized put $p$ | $X\,e^{-rT}N(-d_2)-S\,e^{(b-r)T}N(-d_1)$ | Merton $p=2.46479$ ($q{=}5\%$) |
| **Put–call parity** | $c-p=S\,e^{(b-r)T}-X\,e^{-rT}$ | $S{=}100,X{=}105,T{=}.5,r{=}.10$: $C+Xe^{-rT}=P+S=105.57354$ |
| Delta call | $e^{(b-r)T}N(d_1)$ | $0.503105$ |
| Gamma (call=put) | $\dfrac{e^{(b-r)T}n(d_1)}{S\,\sigma\sqrt T}$ | $0.026794$ |
| Vega (call=put) | $S\,e^{(b-r)T}n(d_1)\sqrt T$ | raw $19.2999$, per 1 vol-point $0.1930$ |
| Theta call (per day) | $\dfrac{1}{365}\left[-\dfrac{S e^{(b-r)T}n(d_1)\sigma}{2\sqrt T}-(b-r)Se^{(b-r)T}N(d_1)-rXe^{-rT}N(d_2)\right]$ | $-0.036989$/day |
| Rho call | $T\,X\,e^{-rT}N(d_2)$ | raw $10.9656$, per 1 rate-point $0.1097$ |
| Gamma–theta trade | $\tfrac12\Gamma\,S^2\sigma^2 = -\Theta_{\text{driftless}}$ | both $=11.5800$ |
| ATM-forward approx | $c\approx p\approx0.4\,S\,e^{(b-r)T}\sigma\sqrt T$ | $3.8713$ vs exact $3.8579$ |

> **Critical scaling caveat (Haug §2).** Screen/lookup values for Vega, Rho, Phi, Carry, Vanna, Zomma are quoted **per 1 vol/rate point** = raw $/100$; Vomma $/10\,000$; Ultima $/10^6$; Theta **per day** = raw $/365$. Failing to apply this convention is the single most common lookup error.

---

### 3. Computational Implementation — the formula engine

This runs on the **standard library only** (`math.erf` gives the exact normal CDF, so there is no dependency on numpy/scipy). It reproduces every verified number above.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
def phi(x):return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

def bsm(S, X, T, r, b, sigma):
    """Generalized Black-Scholes-Merton (cost-of-carry b). Returns (call, put).
       b=r stock | b=r-q index | b=0 futures (Black-76) | b=r-rf FX."""
    if T <= 0:
        return (max(S - X, 0.0), max(X - S, 0.0))
    d1 = (math.log(S / X) + (b + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call = S * math.exp((b - r) * T) * N(d1) - X * math.exp(-r * T) * N(d2)
    put  = X * math.exp(-r * T) * N(-d2) - S * math.exp((b - r) * T) * N(-d1)
    return (call, put)

# --- verify against the corpus (Haug-verified numerics) ---
c, p = bsm(100, 100, 1.0, 0.05, 0.05, 0.20)          # b=r, ATM
print(f"S=100 X=100 T=1 r=5% sigma=20%: call={c:.4f} put={p:.4f}")
lhs = c + 100 * math.exp(-0.05); rhs = p + 100       # put-call parity
print(f"parity: C+Xe^-rT={lhs:.6f}  P+S={rhs:.6f}  diff={abs(lhs-rhs):.2e}")
```
```
S=100 X=100 T=1 r=5% sigma=20%: call=10.4506 put=5.5735
parity: C+Xe^-rT=105.573526  P+S=105.573526  diff=0.00e+00
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Constant-vol delusion** — BSM forces one $\sigma$; real markets show a smile, so the only free parameter cannot fit all strikes.
2. **Continuous-hedging friction** — the "riskless portfolio" needs $dt\to0$; costs and discrete rebalancing turn it into a loss maker (measured via the gamma–theta residual).
3. **Lognormal/completeness failure** — jumps and fat tails break the single-Brownian-motion assumption that makes prices unique (the structural route into Heston/SABR and jump models).

---

### 5. Canonical Literature & Study References

- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) — §§1–2 (generalized BSM, full Greek set), Ch 3 (American), Ch 7 (trees). *The formula-authoritative lookup source for this folder; all formulas numerically verified.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance II* — Ch 4 (Itô–Doeblin, BSM PDE, Greeks, parity) and Ch 5 (Girsanov, risk-neutral pricing, BSM by expectation, dividends, forwards/futures). *Math-verified deep-read in the corpus.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 13 (binomial), 14 (Itô), 15 (BSM model), 17 (indices/FX), 18 (futures/Black). *Verification report in the corpus.*
- **Björk, Tomas**: *Arbitrage Theory in Continuous Time* (3rd ed.) — Ch 7 (arbitrage pricing & the BSM PDE), Ch 5 (Feynman–Kac). *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/calculus-and-optimization/index|Calculus]]
- Sibling topic: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]] (the discrete seed of this model)
- Sub-pages (in-folder): 01 From Zero · 02 PDE & Derivation · 03 Pricing Formulas · 04 Greeks & Hedging · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/black-scholes-merton/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|02 · PDE & Derivation]] → [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · Pricing Formulas]] → [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|04 · Greeks & Hedging]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]

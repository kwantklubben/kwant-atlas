---
title: "01 — Risk Parity & ERC from Zero: Intuition & the Why"
tags:
  - pillar-portfolio-optimization
  - risk-parity-and-equal-risk-contribution
  - intuition
  - diversification
---

**Basic Prerequisites:** none — this page needs no prior finance theory. [[foundations/linear-algebra-and-matrices/index|Linear algebra]] and [[foundations/calculus-and-optimization/index|basic calculus]] help later.

---

### 1. Intuition & Practical Objective

This page builds the *why* of risk parity with **no prior knowledge of portfolio theory needed**. The objective is one idea: **diversification that counts dollars is not diversification that counts risk, and the fix is to allocate risk, not capital.**

Start with the dumbest question: *is a 60/40 stock/bond portfolio "balanced"?* A typical equity index has an annualized volatility near 15%; a long government-bond index near 5%. One dollar of stock produces about *three times* the wiggle of one dollar of bonds. So in a portfolio that is 60% stocks and 40% bonds, the stocks supply roughly $0.60\times3=1.8$ units of wiggle and the bonds $0.40\times1=0.6$, meaning **stocks dominate the portfolio's ups and downs.** When a big loss hits, ~9 in 10 dollars of that loss look just like a stock-market loss. Qian (2005) states it as a table of eggs: with $15\%$ stock vol and $5\%$ bond vol, a "60/40" portfolio holds the equivalent of **58 eggs, of which 54 (≈93%) come from the stock basket** — at most *six* of the "diversification" eggs are actually doing any diversification.

Three steps, three "aha"s:

1. **Risk is what actually hurts you, dollars are not.** A portfolio can look diversified by capital but be a single bet by risk. The amount of risk an asset *contributes* is the product of how much you hold and how much that holding moves the *whole portfolio* — not how volatile the asset is in isolation.
2. **Equal capital ≠ equal risk; equal risk ≠ equal capital.** Because most investors are more familiar with equal *dollars* ($1/N$, or 60/40), the discipline of *risk* allocation feels inverted: the safest asset class usually ends up with a *larger* capital weight, not a smaller one.
3. **Risk-balancing is not return-free.** To match a target *return* you get from a stock-heavy portfolio, a risk-balanced portfolio must **leverage** its low-risk legs. That single sentence carries both the promise and the danger of the whole strategy — the danger lives on [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]].

A clean numerical example to carry through the folder. Take just two assets — say a broad equity index with $\sigma_E=15.1\%$ and a bond index with $\sigma_B=4.6\%$, correlation $\rho=0.2$ (exactly Qian's illustrative numbers). A "balanced" 60/40 portfolio gives **over 92% of its risk to the equities**. To instead split the risk 50/50, the weights must be **≈23% equities / ≈77% bonds** — genuinely "inverted" relative to the 60/40 intuition. (Both numbers are reproduced by the code below and again in [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/02-risk-contributions|02 · Risk Contributions]].)

> **The one-sentence essence.** "Risk parity answers the question a 60/40 investor never asked: two thousand eggs are not diversified if 1,800 of them sit in one basket — split the *risk*, then decide how much risk you want with leverage."

---

### 2. Mathematical Ground Truth & Derivations

The only math this page needs is the definition that makes "contribution to risk" precise. Later pages derive it carefully; here is the shape.

Let $w=(w_1,\dots,w_N)$ be the weights (fractions of capital, summing to 1) and $\Sigma$ the covariance matrix of the assets' returns ($\Sigma_{ii}=\sigma_i^2$, $\Sigma_{ij}=\rho_{ij}\sigma_i\sigma_j$). The portfolio's volatility is

$$\sigma(w)=\sqrt{w^\top\Sigma w}.$$

Because $\sigma$ is **homogeneous of degree 1** — scaling every weight by $\lambda$ scales the volatility by $\lambda$: $\sigma(\lambda w)=\lambda\,\sigma(w)$ — Euler's homogeneous-function theorem guarantees the total risk splits exactly into $N$ per-asset pieces:

$$\sigma(w)=\sum_{i=1}^{N} \underbrace{w_i\,\frac{(\Sigma w)_i}{\sigma(w)}}_{=:\;RC_i}.$$

Each $RC_i$ is the **risk contribution of asset $i$** — the slice of total volatility attributable to that position. This decomposition is *not* an approximation and *does not* require any assumption about returns: it is a property of the quadratic form. **Risk parity / ERC** simply asks for the weights that make all the $RC_i$ equal:

$$RC_1=RC_2=\cdots=RC_N=\frac{\sigma(w)}{N}.$$

Everything else in the folder — the closed forms, the convex programs, the failure modes — hangs off these two sentences.

---

### 3. Computational Implementation — the two-asset picture, verified

The 60/40 → ~90% equity risk, and the ≈23/77 parity portfolio, computed in stdlib. Note how the equal-risk weights are *inverted* (more bonds than stocks).

```python
import math

vol_e, vol_b, rho = 0.151, 0.046, 0.20          # Qian (2005) stock/bond inputs
S = [[vol_e*vol_e, rho*vol_e*vol_b],
     [rho*vol_e*vol_b, vol_b*vol_b]]

def risk_share(w, S):
    Sw = [S[0][0]*w[0]+S[0][1]*w[1], S[1][0]*w[0]+S[1][1]*w[1]]
    sig = math.sqrt(w[0]*Sw[0] + w[1]*Sw[1])
    return sig, w[0]*Sw[0]/sig/sig          # sigma and equity %. (RC/vol) share

sig, eq = risk_share([0.60, 0.40], S)
print(f"60/40 portfolio: sigma={sig:.4f}, equity risk share={eq*100:.1f}%")

# parity weights: inverse-vol (two assets, any rho => equal RC)
wE = (1.0/vol_e)/(1.0/vol_e + 1.0/vol_b)
wB = (1.0/vol_b)/(1.0/vol_e + 1.0/vol_b)
sig, eq = risk_share([wE, wB], S)
print(f"parity: wE={wE:.4f} wB={wB:.4f}  sigma={sig:.4f}, equity share={eq*100:.1f}%")
```
```
60/40 portfolio: sigma=0.0960, equity risk share=92.7%
parity: wE=0.2335 wB=0.7665  sigma=0.0546, equity share=50.0%
```

The lesson is on the left column of the weights: **60/40 gives the equity leg ~93% of the portfolio's risk, and to give it its fair 50% share of risk you must flip the dollars to ~23/77.** Same risk appetite, radically different portfolio — one of the two numbers (92.7%) is what a "diversified" investor actually holds today; the other (50/50 risk) is the risk-parity promise.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "costless leverage" assumption (from the start).** The claim that you can fix risk balance and simply "lever the safe leg back up" assumes borrowing at or near the risk-free rate is freely available. It is not always: margin constraints, funding spreads and forced de-leveraging events change the answer (the core of [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/06-advanced-extensions|06 · Leverage Aversion]]).
2. **Equal risk is not automatically better.** Asness et al. (2012) are blunt: equalizing risk is only optimal if you believe you are *not* paid enough in expected return to accept the concentrated risk. Parity is a statement about expected returns, not just about diversification — a point the marketing of risk-parity funds often omits.
3. **The 60/40 math depends on the correlation.** The "90% equity risk" figure assumes low stock–bond correlation. If equities and bonds start to move together, the same 60/40 portfolio becomes *even more* equity-like in a crash — and the parity allocation's leverage becomes dangerous (see [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Qian, Edward**: *Risk Parity Portfolios: Efficient Portfolios Through True Diversification*, PanAgora (2005) — the 60/40-is-~90%-equity-eggs argument; parity weights ≈23/77; parity's mean-variance optimality under equal Sharpe ratios.
- **Maillard, Roncalli & Teïletche**: *The Properties of Equally Weighted Risk Contribution Portfolios*, JPM 36(4) (2010) — the formal place of this two-asset intuition in the general ERC theory.
- **Asness, Frazzini & Pedersen**: *Leverage Aversion and Risk Parity*, FAJ 68(1) (2012) — the honest framing: risk balance is a view on expected returns + a willingness to use leverage.

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/calculus-and-optimization/index|Calculus]]
- Continue: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/02-risk-contributions|02 · Risk Contributions]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Index Hub]]
- Sibling: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean-Variance & Markowitz]]
---
title: "01 — Modern Portfolio Theory from Zero: Return, Risk & Diversification"
tags:
  - pillar-portfolio-optimization
  - modern-portfolio-theory-and-mean-variance
  - intuition
  - diversification
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (vectors, dot products will be enough).

---

### 1. Intuition & Practical Objective

This page builds the *why* of Modern Portfolio Theory with **no prior portfolio knowledge needed**. The objective is one idea: **an asset should never be judged in isolation — its value to a portfolio is entirely determined by how it *covaries* with everything else you hold.** That single shift (asset-by-asset → covariance-aware) is the entire conceptual revolution of Markowitz (1952).

Before Markowitz, investors picked the "best" asset: highest yield, fastest growth. Markowitz replaced *picking* with *averaging*, and proved a stunning fact: **combining risky assets can produce a portfolio *less* risky than any of them individually, at the same or better expected return.** The mechanism is the correlation between assets, and the measure of its payoff is the portfolio-variance formula. Three "aha"s:

1. **A portfolio's risk is not the weighted average of its parts.** It is a *quadratic* blend that includes the cross-terms (covariances). If two assets don't move together, each wobbles while the other stays put, so the portfolio wobbles less.
2. **Diversification is not a strategy, it's arithmetic.** The variance formula below *forces* the reduction. The only "free lunch" in financial economics is the one the quadratic form hands to you.
3. **The lower the correlation, the bigger the gift.** At $\rho=-1$ perfect negative correlation, you can drive variance to zero; at $\rho=+1$ diversification gives nothing. The correlation, not the individual volatilities, decides.

---

### 2. Mathematical Ground Truth & Derivations

**Portfolio of two assets.** Holding weight $w$ in asset 1 and $1-w$ in asset 2, with individual variances $\sigma_1^2,\sigma_2^2$ and correlation $\rho$:
$$\sigma_p^{\,2}=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\rho\,\sigma_1\sigma_2,$$
so the portfolio *volatility* is $\sigma_p=\sqrt{\sigma_p^2}$. The cross-term $2w(1-w)\rho\sigma_1\sigma_2$ is the entire plot: if $\rho<1$, the sum of the two positive "own" terms is partially cancelled, and $\sigma_p < w\sigma_1+(1-w)\sigma_2$ (the weighted-average *volatility*). Note the risk is quadratic in $w$; that convexity is what makes a *minimization* well-posed.

**The minimum-variance weight.** Setting $d\sigma_p^2/dw=0$ gives the weight that makes the portfolio as quiet as possible:
$$w^\*=\frac{\sigma_2^2-\rho\,\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\,\sigma_1\sigma_2}.$$
When the two assets have equal volatility and $\rho\ne1$, $w^\*=1/2$ — equal weight is *exactly* the minimum-variance portfolio, purely by symmetry. When their volatilities differ, you tilt toward the quieter asset; and if $\rho$ is high enough the formula can exceed $1$ or go negative, meaning the minimum-variance portfolio *shorts* one asset (a corner you can't reach long-only).

**The separable, general case ($N$ assets).** With weights $w\in\mathbb{R}^N$, expected returns $\mu$, and covariance $\Sigma$,
$$R_p=w^T\mu,\qquad \sigma_p^2=w^T\Sigma w,$$
with the budget constraint $w^T\mathbf{1}=1$. The two-asset insight generalizes: the cross-covariances in $\Sigma$ (off-diagonal entries) are what diversification harvests. The full machinery is built out on [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · The Efficient Frontier]].

---

### 3. Computational Implementation — diversification in numbers

The two-asset variance formula, stdlib only. Watch the correlation slash the portfolio volatility, and watch the minimum-variance weight tilt as $\rho$ changes.

```python
import math
def port_vol(s1, s2, rho, w):
    """Portfolio volatility for weights (w, 1-w) on two assets."""
    v = w*w*s1*s1 + (1-w)*(1-w)*s2*s2 + 2*w*(1-w)*rho*s1*s2
    return math.sqrt(v)

print("Equal-vol pair (0.30, 0.30), w=0.5 portfolio volatility vs rho:")
for rho in (0.0, 0.3, -0.7):
    print(f"  rho={rho:+.1f}: vol = {port_vol(0.30,0.30,rho,0.5):.4f} "
          f"(vs 0.3000 for either asset alone)")

print("\nUnequal-vol pair (0.25, 0.40): min-variance weight  w*=(s2^2-rho s1 s2)/denom")
for rho in (0.0, 0.3, 0.8):
    w = (0.40**2 - rho*0.25*0.40) / (0.25**2 + 0.40**2 - 2*rho*0.25*0.40)
    print(f"  rho={rho:.1f}: w*_quiet={w:.3f}  vol@w*={port_vol(0.25,0.40,rho,w):.4f} "
          f"  vol@0.5={port_vol(0.25,0.40,rho,0.5):.4f}")
```
```
Equal-vol pair (0.30, 0.30), w=0.5 portfolio volatility vs rho:
  rho=+0.0: vol = 0.2121 (vs 0.3000 for either asset alone)
  rho=+0.3: vol = 0.2419 (vs 0.3000 for either asset alone)
  rho=-0.7: vol = 0.1162 (vs 0.3000 for either asset alone)

Unequal-vol pair (0.25, 0.40): min-variance weight  w*=(s2^2-rho s1 s2)/denom
  rho=0.0: w*_quiet=0.719  vol@w*=0.2120   vol@0.5=0.2358
  rho=0.3: w*_quiet=0.800  vol@w*=0.2366   vol@0.5=0.2658
  rho=0.8: w*_quiet=1.280  vol@w*=0.2400   vol@0.5=0.3092
```

Read the rows: even at *zero* correlation, two assets of volatility 0.30 blend to 0.2121 — a **29% volatility cut with no expected-return cost at all**. At $\rho=-0.7$ it falls to 0.1162. And in the unequal-vol case, when $\rho=0.8$ the minimum-variance weight comes out **1.28**, i.e. the quiet portfolio would *short* the louder asset — the seed of why long-only constraints matter ([[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Constraints]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Correlation vs. causality confusion.** Diversification harvests *historical* correlation; if correlations rise to 1 in a crisis (the "correlation breakdown"), the free lunch disappears exactly when you need it. The formula is an identity given $\rho$, not a guarantee about $\rho$.
2. **The "$N \to \infty$" myth.** More assets help only because they add *independent* variance sources; buying 100 clones of the same factor adds nothing. What matters is the number of *independent* risk factors, not the number of names.
3. **Volatility is not the only risk.** Markowitz captures variance; it says nothing about skew, jumps, or tail dependence. Diversification that reduces variance can still leave correlated tail risk in place (bridge to the extreme-value/fat-tails material in [[pillars/04-quantitative-risk/index|Quantitative Risk]]).
4. **The minimum-variance weight is an optimizer too.** As soon as you minimize, you inherit input sensitivity — $w^\*$ depends on the *estimated* $\sigma_1,\sigma_2,\rho$, and near $\rho\to1$ the denominator $\to0$ and $w^\*$ becomes violently unstable. The fragility of every "optimal" weight is the theme of [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Markowitz, Harry**: *Portfolio Selection*, Journal of Finance 7(1):77–91 (1952) — the founding E-V rule and the diversification math this page walks through.
- **Elton, Gruber, Brown & Goetzmann**: *Modern Portfolio Theory and Investment Analysis*, Wiley — the textbook treatment of the two-asset and multi-asset cases.
- **Hastie, Tibshirani & Friedman (ESL)**, Ch 3–4 — the same $\Sigma$, ridge-type shrinkage intuition that shows up again in covariance estimation ([[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · The Efficient Frontier]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/03-tangency-and-capm|03 · Tangency & CAPM]]
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/probability-and-measure-theory/index|Probability]]
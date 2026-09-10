---
title: "04 — The Value–Momentum Interaction"
tags:
  - pillar-quant-research
  - momentum
  - value
  - factor-interaction
  - diversification
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (correlation, variance) and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]].

---

### 1. Intuition & Practical Objective

Value and momentum are the two best-documented return premia in finance — and they are **negatively correlated**. Value buys cheap, beaten-down assets; momentum buys recent winners. When one is working, the other tends to be struggling: after a long value drawdown the winners momentum wants are exactly the "expensive" names value wants to short, and vice-versa. This negative correlation is the single most useful *practical* fact in the momentum literature: **combining them is not a compromise, it is a hedge.**

Asness, Moskowitz & Pedersen (2013) document the premia in **eight markets** — US, UK, Europe, and Japan individual stocks plus global equity-index, bond, currency, and commodity futures. Key verified results:

- A momentum and a value premium in *every* market.
- Correlation between value and momentum residual returns is **strongly negative: $\approx-0.60$ across stock markets** (Japan $-0.64$), **$\approx-0.49$ within non-stock asset classes**.
- The equal-weighted $50/50$ combination $r^{\text{COMBO}}=0.5\,r^{\text{VALUE}}+0.5\,r^{\text{MOM}}$ **outperforms either strategy alone in every market**, and across all asset classes produces an annualized Sharpe near **1.45**.
- Momentum is *insignificant alone* in Japan, yet the value–momentum combination there still improves the efficient frontier — the negative correlation does the work even where momentum alone "fails."

---

### 2. Mathematical Ground Truth & Derivations

**Combination variance.** Let value and momentum have monthly means $\mu_V,\mu_M$, vols $\sigma_V,\sigma_M$, and correlation $\rho=\operatorname{corr}(r_V,r_M)$. The equal-weight combination $r_C=\tfrac12 r_V+\tfrac12 r_M$ has
$$\mu_C=\tfrac12\mu_V+\tfrac12\mu_M, \qquad \sigma_C^2=\tfrac14\sigma_V^2+\tfrac14\sigma_M^2+2\cdot\tfrac14\,\rho\,\sigma_V\sigma_M.$$
With $\rho<0$ the covariance term is *negative*, shrinking $\sigma_C$ below either leg while keeping $\mu_C$ as the average of two positive means. The Sharpe of the combination, $\text{SR}_C=\mu_C/\sigma_C$, can exceed both $\text{SR}_V$ and $\text{SR}_M$ — the hallmark of a genuine diversifier.

**Why is $\rho$ negative?** Intuitively, both strategies are *reversion bets on mispricing* but on opposite timing: value assumes price over-reacts to bad news and will revert (buy the fallen), momentum assumes price under-reacts to good news and will continue (buy the risers). They are the two halves of the behavioral "over-/underreaction" tension (Daniel, Hirshleifer & Subrahmanyam 1998; Barberis, Shleifer & Vishny 1998). Empirically the negative correlation is robust across markets and asset classes (AMP 2013).

**Optimal weights.** The unconstrained tangency weights for the two-asset portfolio are $\mathbf{w}^*\propto\Sigma^{-1}\boldsymbol\mu$, which put meaningful weight on both legs precisely because $\rho<0$ raises the diversification benefit. Equal-weighting ($0.5/0.5$) is the robust, simple rule that captures most of this.

---

### 3. Computational Implementation — why the 50/50 works

Standard library only. Generates two positively-expected-return, negatively-correlated return streams (momentum and value), computes the $50/50$ combination, and verifies **the combination Sharpe exceeds each leg** and the **combination variance identity** holds exactly.

```python
import random, math
random.seed(5)

T, mu_m, sd_m, mu_v, sd_v = 240, 0.015, 0.045, 0.010, 0.035
rho = -0.60                                              # corr(value, momentum)
z  = [[random.gauss(0.0,1.0) for _ in range(T)] for _ in range(2)]
mom = [mu_m + sd_m*z[0][t]                       for t in range(T)]
val = [mu_v + sd_v*(rho*z[0][t] + math.sqrt(1-rho*rho)*z[1][t]) for t in range(T)]

def stats(s):
    m = sum(s)/len(s); sd = (sum((x-m)**2 for x in s)/len(s))**0.5
    return m, sd, m/sd
def corr(a,b):
    ma, mb = sum(a)/len(a), sum(b)/len(b)
    n = sum((a[t]-ma)*(b[t]-mb) for t in range(T))
    d = math.sqrt(sum((a[t]-ma)**2 for t in range(T))*sum((b[t]-mb)**2 for t in range(T)))
    return n/d

combo = [0.5*mom[t] + 0.5*val[t] for t in range(T)]
mm, sm, srm = stats(mom);  mv, sv, srv = stats(val);  mc, sc, src = stats(combo)
print(f"momentum : SR {srm:+.3f} (mean/mo {mm*100:+.2f}%, vol/mo {sm*100:.2f}%)")
print(f"value    : SR {srv:+.3f} (mean/mo {mv*100:+.2f}%, vol/mo {sv*100:.2f}%)")
print(f"50/50    : SR {src:+.3f} (mean/mo {mc*100:+.2f}%, vol/mo {sc*100:.2f}%)")
print(f"corr(value,momentum) = {corr(val,mom):+.3f}  (target {rho:.2f})")
sigma2_theory = 0.25*sm**2 + 0.25*sv**2 + 2*0.25*corr(val,mom)*sm*sv
print(f"combo var: empirical {sc**2:.6f}  analytic {sigma2_theory:.6f}  (diff {abs(sc**2-sigma2_theory):.1e})")
det = sm**2*sv**2*(1-corr(val,mom)**2)
w_m = (sv**2*mm - corr(val,mom)*sm*sv*mv)/det
w_v = (sm**2*mv - corr(val,mom)*sm*sv*mm)/det
w_m, w_v = w_m/(w_m+w_v), w_v/(w_m+w_v)
print(f"tangency weights: w_momentum {w_m:.3f}  w_value {w_v:.3f}")
```
```
momentum : SR +0.283 (mean/mo +1.38%, vol/mo 4.87%)
value    : SR +0.344 (mean/mo +1.16%, vol/mo 3.37%)
50/50    : SR +0.670 (mean/mo +1.27%, vol/mo 1.89%)
corr(value,momentum) = -0.631  (target -0.60)
combo var: empirical 0.000359  analytic 0.000359  (diff 0.0e+00)
tangency weights: w_momentum 0.398  w_value 0.602
```

The combination's Sharpe ($+0.67$) **more than doubles** the better single-leg ($+0.34$): the negative correlation roughly halves the combo's volatility (1.89% vs the 3.4–4.9% legs) while keeping the mean near the average. The variance identity is reproduced exactly.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Correlation is state-dependent.** Value–momentum correlation is *not* constant: it is most negative precisely when it matters (after market declines, when momentum crashes and value rebounds). A naive assumption of constant $\rho$ overstates the steady-state diversification benefit.
2. **"Add value to anything" is a myth.** The benefit is specific to the *negative* correlation. Pairing momentum with a positively-correlated momentum-like factor (e.g. two trend signals on the same universe) does nothing for diversification and can concentrate crash risk.
3. **Japan's lesson.** Momentum *alone* is weak/insignificant in Japan, yet the combination still helps — but only because the negative correlation is present. The empirical rule is "combine for correlation reasons," not "combine because each premium always works."
4. **Re-balancing and crowding.** A 50/50 that is never rebalanced drifts into the higher-return leg over time; and both legs being crowded compress the premia the combination was built to harvest (see [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]] on crowding).

---

### 5. Canonical Literature & Study References

- **Asness, Moskowitz & Pedersen (2013)**, *Value and Momentum Everywhere*, J. Finance 68(3) — premia in eight markets, negative correlation ($-0.60$ stocks, $-0.49$ other), 50/50 combination Sharpe near 1.45. *Verified corpus refs/15.*
- **Asness, Frazzini, Israel & Moskowitz (2014)**, *Fact, Fiction, and Momentum Investing* — combining momentum with negatively-correlated styles like value as the practical hedge. *Verified corpus refs/18.*
- **Fama & French (1993, 1996)** — the value (HML) factor and why momentum is the anomaly value models cannot explain.
- **Daniel, Hirshleifer & Subrahmanyam (1998)** and **Barberis, Shleifer & Vishny (1998)** — the over/under-reaction behavioral foundations of value and momentum.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (correlation, variance) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]]
- Continue: [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/momentum/06-advanced-extensions|06 · Advanced Extensions]]
- Factor view: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (value HML + momentum UMD)
- Portfolio construction: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean-Variance (combo weights)]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]]

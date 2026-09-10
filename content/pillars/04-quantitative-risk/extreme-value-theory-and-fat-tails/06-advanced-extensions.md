---
title: "06 — Advanced Extensions: Filtered EVT, Multivariate EVT & Copulas"
tags:
  - pillar-quantitative-risk
  - extreme-value-theory
  - filtered-evt
  - multivariate-evt
  - copulas
  - garch
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/04-peaks-over-threshold|04 · Peaks Over Threshold]] and [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

The two real-world defects of textbook EVT — **(a)** extreme returns are dependent/regime-driven, and **(b)** risk is a *portfolio* problem in many dimensions — motivate the extensions on this page. The objective is the **launchpad**: show the two extensions that matter most in practice, **filtered (conditional) EVT** and **multivariate EVT via copulas**, and hand off the deeper machinery to the corpus monographs.

> **Why these two?** Filtered EVT fixes the i.i.d. violation of the POT method in one step: fit a volatility model, standardize the residuals, apply EVT to the (near-i.i.d.) residual tail, and scale back by current volatility. This is the McNeil–Frey (2000) method, and it beat conditional normality and unconditional EVT in their backtests. Multivariate EVT matters because a bank's risk is a *book* of correlated positions, and Gaussian-copula dependence understates the joint probability that *several* positions crash together — the exact failure behind 2008.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Filtered / conditional EVT (McNeil & Frey 2000)

Model returns as a heteroscedastic process
$$X_t=\mu+\sigma_t Z_t,\qquad Z_t \text{ i.i.d. heavy-tailed},$$
where $\sigma_t$ follows GARCH(1,1) $\sigma_t^2=\omega+\alpha X_{t-1}^2+\beta\sigma_{t-1}^2$ (Tsay Ch 3). The two-step method:
1. **Filter:** estimate $\hat\mu,\hat\sigma_t$ (GARCH or EWMA), form standardized residuals $\hat Z_t=(X_t-\hat\mu)/\hat\sigma_t$.
2. **Tail:** fit a GPD to the residual tail and estimate the residual quantile $\hat z_q$ (the EVT machinery of [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/04-peaks-over-threshold|04 · POT]]).
3. **Rescale:** one-day conditional VaR $=\hat\mu_{t+1}+\hat\sigma_{t+1}\hat z_q$; conditional ES $=\hat\mu_{t+1}+\hat\sigma_{t+1}\,\mathbb{E}[Z\mid Z>\hat z_q]$, with $\mathbb{E}[Z\mid Z>z_q]=\frac{z_q+\hat\beta}{1-\hat\xi}$ (McNeil & Frey eq. 14).

**Why it works.** Standardized residuals are far closer to i.i.d. than raw returns, so the EVT limit theorem and the excesses-independence assumption hold (Embrechts–Klüppelberg–Mikosch Ch 5; McNeil & Frey §2.2 cite the AR(1) example where residual-based Hill estimates are far more stable than raw-data Hill). McNeil & Frey's backtests (S&P, DAX, BMW, $/$£, Gold): conditional EVT was correct in 11/15 cases and *never* rejected, while conditional normal failed 11 times and unconditional EVT misread stress periods.

#### 2.2 Multivariate EVT & copulas

Univariate EVT answers "how bad can one risk get?" Portfolio risk asks "how likely do *several* risks get bad *together*?" The dependence structure is captured by a **copula** — a function $C:[0,1]^d\to[0,1]$ with uniform margins that couples them. Sklar's theorem: any joint CDF $F$ with margins $F_i$ writes as $F(x_1,\dots,x_d)=C(F_1(x_1),\dots,F_d(x_d))$.

The relevant quantity for joint extremes is the **upper tail dependence coefficient**
$$\lambda_u=\lim_{q\to1}\mathbb{P}\big(U_1>q\mid U_2>q\big),$$
the probability that one variable is extreme given another is. Key facts:
- **Gaussian copula:** $\lambda_u=0$ for $\rho<1$ — extremes are *asymptotically independent* even for strong correlation. This is the theoretical reason a Gaussian-copula risk model says "two assets never crash together" and why it failed in 2008.
- **$t$-copula (with low dof):** $\lambda_u>0$ — it has genuine tail dependence, which is why it's preferred for portfolio tail risk.
- **Archimedean copulas (Clayton, Gumbel):** explicit tail dependence, used in credit (the one-factor models behind CreditMetrics/Vasicek, [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]]).

Multivariate EVT generalizes the univariate limit: the joint tail converges to a multivariate GEV/Pareto whose dependence is summarized by a **stable tail dependence function** or **Pickands dependence function** (de Haan Ch 6–7; McNeil–Frey–Embrechts Ch 7). The practical message: *fit univariate EVT tails on each margin, choose a copula with the right tail-dependence sign, and glue them together* — never assume independence or Gaussianity in the joint tail.

---

### 3. Computational Implementation — the Gaussian copula understates joint extremes

Direct, stdlib demonstration of §2.2: sample the bivariate Gaussian copula at two correlations and measure the joint probability that both ranks exceed 95%, and the conditional probability one is extreme given the other. (In the doc we read the copula's own ranks; any fat-tailed margins can be attached.)

```python
import math, random

def gauss_copula_sample(rho):
    """One draw from the bivariate Gaussian copula with correlation rho.
    Returns the two uniform ranks (feed any margins to get a joint distribution)."""
    u1 = random.gauss(0,1); u2 = random.gauss(0,1)
    v1 = u1
    v2 = rho*u1 + math.sqrt(1-rho*rho)*u2            # correlation via linear combination
    p1 = 0.5*(1.0 + math.erf(v1/math.sqrt(2.0)))     # standard normal CDF
    p2 = 0.5*(1.0 + math.erf(v2/math.sqrt(2.0)))
    return p1, p2

def tail_probs(rho, n=20000, thr=0.95):
    pairs = [gauss_copula_sample(rho) for _ in range(n)]
    both  = sum(1 for (a,b) in pairs if a>thr and b>thr) / n
    given = sum(1 for (a,b) in pairs if a>thr)
    cond  = sum(1 for (a,b) in pairs if a>thr and b>thr) / max(given,1)
    return both, cond

random.seed(3)
b, c = tail_probs(0.7); b0, c0 = tail_probs(0.0)
print(f"Gaussian copula, n=20000, threshold 95%:")
print(f"  rho=0.7 : P(both>95%)={b:.4f}   P(p2>95% | p1>95%)={c:.3f}")
print(f"  rho=0.0 : P(both>95%)={b0:.4f}   P(p2>95% | p1>95%)={c0:.3f}")
print(f"  (independent would give {0.05*0.05:.4f} and {0.05:.3f})")
```
```
Gaussian copula, n=20000, threshold 95%:
  rho=0.7 : P(both>95%)=0.0194   P(p2>95% | p1>95%)=0.390
  rho=0.0 : P(both>95%)=0.0023   P(p2>95% | p1>95%)=0.046
  (independent would give 0.0025 and 0.050)
```
At the 95% level the high-correlation copula shows *subasymptotic* tail dependence ($0.39$ conditional vs $0.05$ independent). But here is the trap the theory warns about: this conditional probability **decays to zero as the threshold $\to1$** for the Gaussian copula — it is asymptotically tail-independent. A risk model using it will report "joint crashes are impossible" exactly at the extreme level where a bank must not hear that. This is why the $t$-copula (positive $\lambda_u$) and EVT-based tail dependence replace it for portfolio tail risk.

**Filtered EVT in one line** (the McNeil–Frey method, implementation and numbers in [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/05-failure-modes-and-practice|05 · Failure Modes, Experiment 2]]): GARCH/EWMA-filter the returns, fit the GPD to the residual tail, rescale the residual quantile by current volatility — reproducing McNeil & Frey's finding that conditional EVT VaR (0.710) beats conditional normal (0.532) on heavy-tailed GARCH data.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Gaussian-copula tail blindness.** For any $\rho<1$ the Gaussian copula is asymptotically tail-independent ($\lambda_u=0$) — it *guarantees* "no joint crashes" in the extreme tail. If your model uses it, the fat left tail of a portfolio is systematically understated. Use a $t$-copula or EVT dependence for tail risk.
2. **Copula + marginal mismatch.** A copula carries *no* information about the margins — you must model the heavy-tailed margins separately (univariate EVT), or the joint tail is wrong even with a "correct" copula.
3. **Filtering model risk.** The GARCH/EWMA filter must be right; a misspecified volatility model contaminates the residuals and hence the EVT tail. Validate the residuals are near-i.i.d. (ACF of squares) before fitting.
4. **Estimation stability in multivariate EVT.** Multivariate dependence functions and the associated parameters are even harder to estimate than univariate $\xi$ — small samples and high dimensions make them fragile (de Haan Ch 6–7). Report sensitivity, especially for $\lambda_u$.
5. **Regime shifts in $\xi$ and dependence.** Both the tail index and the dependence can change across calm/crisis regimes; a single static copula or tail index mixes regimes (see [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **McNeil & Frey (2000)**, *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series*, JEF 7:271–300 — the filtered/conditional EVT method, ES eq. (14), backtests. *Read in corpus.*
- **de Haan & Ferreira (2006)**, Ch 6–7 — multivariate EVT, stable tail dependence / Pickands dependence functions. *Math-verified in corpus.*
- **McNeil, Frey & Embrechts (2015)**, Ch 7 (EVT) and Ch 8 (copulas, tail dependence). *In library.*
- **Embrechts, Klüppelberg & Mikosch (1997)** — Ch 5 (dependence, extremal index) and Ch 6 (multivariate EVT). The reference monograph.
- **Tsay, *Analysis of Financial Time Series*** — Ch 3 (GARCH, the filter side). *Ch 4–6 verified in corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Index Hub]]
- Portfolio risk: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]
- Credit (fat-tailed joint default): [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus]] (GARCH dynamics) · [[foundations/probability-and-measure-theory/index|Probability Theory]] (copulas)

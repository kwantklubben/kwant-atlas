---
title: "4.3.2 Stylized Facts of Fat-Tailed Financial Returns"
tags:
  - pillar-quantitative-risk
  - extreme-value-theory
  - fat-tails
  - stylized-facts
  - volatility-clustering
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory]].

---

### 1. Intuition & Practical Objective

Before any extreme-value model, we need the *empirical ground truth*: **what do real financial returns actually look like in the tails?** This page collects the well-established stylized facts - heavy tails, volatility clustering, non-normality of kurtosis - and shows them with reproducible simulation so the numbers are concrete. The practical objective: a risk model that does not reproduce these facts is wrong in the tail by construction, and EVT is built to match exactly these observed regularities.

The four facts that matter for this pillar:

1. **Returns are heavy-tailed (leptokurtic).** Excess kurtosis is large and positive; the survival function is closer to a power law than to a Gaussian. Empirically the tail index sits near $\alpha\approx3$–$4$.
2. **Volatility clusters.** Large changes tend to be followed by large changes, of either sign (ARCH/GARCH). Returns themselves are nearly serially uncorrelated, but *squared* returns are strongly autocorrelated.
3. **Kurtosis is unstable / often infinite.** Because $\alpha$ is near 3–4, the 4th moment is borderline or nonexistent - so sample kurtosis does not converge to a stable number. This is a *feature* of fat tails, not a data problem.
4. **Extreme events arrive in clusters, not independently.** The i.i.d. assumption of textbook EVT fails in the presence of clustering - a key driver of the GARCH-filtered methods in [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/06-advanced-extensions|06 · Advanced Extensions]].

---

### 2. Mathematical Ground Truth & Derivations

**Heavy tails as power laws.** A distribution is in the Fréchet domain of attraction (tail index $\alpha=1/\xi$) iff its survival function is regularly varying (de Haan Thm 1.2.1; Gnedenko 1943):
$$
1-F(x)=x^{-\alpha}L(x),\qquad x\to\infty,
$$
where $L$ is *slowly varying* ($L(tx)/L(t)\to 1$). For a Student-t with $\nu$ dof, $\alpha=\nu$ exactly, and (McNeil & Frey 2000, eq. 12):
$$
1-F_\nu(x)\sim \frac{\nu^{\nu/2-1}}{B(1/2,\nu/2)}\,x^{-\nu}\qquad\Big(=\frac{\Gamma((\nu+1)/2)\,\nu^{\nu/2-1}}{\sqrt{\pi}\,\Gamma(\nu/2)}\,x^{-\nu}\Big),\qquad x\to\infty.
$$
Consequences: the $m$-th moment exists only if $m<\alpha$. For $\alpha=3$ the 4th moment (kurtosis) does **not exist**; for $\alpha=2$ even the variance doesn't.

**Kurtosis and the mean-excess function.** The classic diagnostics:
- Sample kurtosis $\hat\kappa=\frac{1}{n}\sum(x_i-\bar x)^4/\big(\frac{1}{n}\sum(x_i-\bar x)^2\big)^2$ - finite only if the 4th moment exists.
- The **mean excess function** $e(u)=\mathbb{E}[X-u\mid X>u]$. For a GPD tail, $e(u)=\dfrac{\beta+\xi u}{1-\xi}$ - a straight line in $u$ with slope $\xi/(1-\xi)>0$ when $\xi>0$. An upward-sloping empirical mean-excess plot is the standard visual sign of a heavy tail (McNeil 1997 §4.1).

**Volatility clustering in one equation.** The GARCH(1,1) model (Bollerslev 1986; Tsay Ch 3) is the canonical generator:
$$
\sigma_t^2=\omega+\alpha\,X_{t-1}^2+\beta\,\sigma_{t-1}^2,\qquad X_t=\sigma_t Z_t,
$$
with $Z_t$ heavy-tailed innovations. It reproduces all four facts: heavy-tailed marginals (from $Z_t$), volatility clustering (from the $\sigma_t^2$ recursion), and near-zero autocorrelation of returns with strong autocorrelation of squares.

---

### 3. Computational Implementation - reproducing the stylized facts

Simulate three return series - i.i.d. normal, i.i.d. t₄, and GARCH(1,1) with t₄ innovations - and measure kurtosis, tail exceedance frequencies, and squared-return autocorrelation. Stdlib only.




Read the table top to bottom: kurtosis explodes (t₄'s 4th moment is *infinite*, so the sample number is unstable - that is the point); 5-sigma events that are impossible under a normal occur ~170× per 100k in heavy-tailed series; and GARCH reproduces the *signature* fact - squared-return autocorrelation of $+0.36$ while raw-return autocorrelation is ~0. That $+0.36$ in $r_t^2$ is volatility clustering, the empirical reason the i.i.d. assumption fails in the tail ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using sample kurtosis as a stable diagnostic.** When the true $\alpha\lesssim4$, the 4th moment doesn't exist, so sample kurtosis is an unstable random variable - the $54.8$ vs $546.3$ above are *not* converging to a "true" value. Estimate the *tail index* $\alpha$ directly (Hill estimator, [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/03-extreme-value-theory|03 · EVT]]) instead.
2. **Testing "normality" on the whole distribution.** The fat tail is a *tail* phenomenon; the center of returns is often near-normal. Global normality tests reject, but the useful question is only the tail index.
3. **Ignoring clustering when using i.i.d. EVT.** Real extreme losses arrive in clusters (a crash is several bad days in a row), so the "i.i.d. excesses" assumption of textbook POT is violated - the count of exceedances is wrong and the effective sample is smaller than $N_u$.

---

### 5. References

- **Tsay, Ruey S.**, *Analysis of Financial Time Series* (3rd ed., Wiley)
- **McNeil & Frey (2000)**, *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series*, JEF 7:271–300
- **McNeil (1997)**, *Estimating the Tails of Loss Severity Distributions Using EVT*, ASTIN 27:117–137
- **Embrechts, Klüppelberg & Mikosch (1997)**

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/03-extreme-value-theory|03 · Extreme Value Theory]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/04-peaks-over-threshold|04 · Peaks Over Threshold]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] (GARCH machinery) · [[foundations/probability-and-measure-theory/index|Probability Theory]]

---
title: "4.3.4 Peaks-Over-Threshold"
tags:
  - pillar-quantitative-risk
  - extreme-value-theory
  - peaks-over-threshold
  - generalized-pareto
  - var
  - expected-shortfall
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/03-extreme-value-theory|03 · Extreme Value Theory]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]].

---

### 1. Intuition & Practical Objective

Block-maxima (GEV) is statistically wasteful: it discards all but one observation per block. **Peaks-Over-Threshold (POT)** keeps *every* observation above a high threshold $u$ and models the *exceedances*. The objective of this page - the practical core of the folder - is to (a) state the threshold-excess limit theorem, (b) define the **Generalized Pareto Distribution (GPD)**, and (c) derive and implement the **EVT VaR and Expected Shortfall** formulas that turn a GPD tail fit into risk numbers.

The one-sentence claim (McNeil 1997; McNeil & Frey 2000): for a wide class of distributions, **losses that exceed a high enough threshold are Generalized Pareto**, so you can fit a two-parameter GPD to the tail, invert it, and get closed-form high-quantile VaR/ES that beat both historical simulation and the normal assumption at extreme levels. This is the method of choice for insurance loss severity (McNeil 1997), operational risk, and filtered financial returns (McNeil & Frey 2000).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Pickands–Balkema–de Haan threshold-excess theorem

Let $X\sim F$, $u$ a high threshold below the right endpoint $x_0$, and define the **excess distribution**
$$
F_u(y)=\mathbb{P}\big(X-u\le y\mid X>u\big)=\frac{F(u+y)-F(u)}{1-F(u)},\qquad 0\le y<x_0-u.
$$

**Theorem (Balkema & de Haan 1974; Pickands 1975).** For $F\in\text{MDA}(G_\xi)$,
$$
\lim_{u\to x_0}\ \sup_{0<y<x_0-u}\Big|F_u(y)-G_{\xi,\beta(u)}(y)\Big|=0,
$$
i.e. the excesses over a high threshold converge to a **GPD** with scale $\beta(u)$ and shape $\xi$ equal to the GEV shape (McNeil 1997 §3.4; de Haan). The GPD:
$$
G_{\xi,\beta}(y)=\begin{cases}1-\big(1+\xi y/\beta\big)^{-1/\xi},&\xi\neq0,\\[4pt] 1-e^{-y/\beta},&\xi=0,\end{cases}\qquad y\ge0,\quad 1+\xi y/\beta>0.
$$
The shape $\xi$ is *the* tail parameter (same $\xi$ as GEV); $\beta>0$ is scale. Mean excess: $e(u)=\mathbb{E}[X-u\mid X>u]=\dfrac{\beta+\xi u}{1-\xi}$ (linear in $u$ when $\xi\neq0$ - the mean-excess-plot diagnostic).

#### 2.2 Fitting the GPD and the tail estimator (McNeil & Frey 2000, eq. 8)

Let $N_u$ be the number of exceedances of $u$ out of $n$. Estimate $\widehat F_u$ by the fitted GPD and $1-F(u)$ empirically by $N_u/n$:
$$
\widehat F(x)=1-\frac{N_u}{n}\Big(1+\hat\xi\frac{x-u}{\hat\beta}\Big)^{-1/\hat\xi},\qquad x>u,
$$
using maximum likelihood for $(\hat\xi,\hat\beta)$ (McNeil 1997 §3.6 - regular, asymptotically normal for $\xi>-1/2$).

#### 2.3 EVT quantile (VaR) and Expected Shortfall (McNeil & Frey 2000, eq. 10 & §4.1)

Inverting the tail estimator for $q>1-N_u/n$:
$$
\boxed{\ \widehat{x}_q=u+\frac{\hat\beta}{\hat\xi}\Big[\Big(\frac{n}{N_u}(1-q)\Big)^{-\hat\xi}-1\Big]\ }
$$
This is the **EVT VaR** at confidence $q$. The expected shortfall follows from the GPD mean-excess identity (McNeil & Frey eq. 14: $E[W-w\mid W>w]=\frac{\hat\beta+\hat\xi w}{1-\hat\xi}$):
$$
\boxed{\ \widehat{\text{ES}}_q=\frac{\widehat{x}_q+\hat\beta-\hat\xi u}{1-\hat\xi}\ }
$$
Interpretation: ES is VaR plus the average excess beyond it, scaled by the GPD shape. For $\xi>0$ the ES/VaR ratio exceeds 1 and *grows* into the tail - the two measures diverge exactly in the fat-tailed regime where VaR's subadditivity and information failures matter most ([[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]]).

#### 2.4 Threshold selection (McNeil 1997 §4.4; McNeil & Frey §2.3)

The threshold $u$ (equivalently $k=N_u$) is *the* free choice. Too low $u$ ⇒ non-tail data bias the GPD fit (the limit theorem applies only above a high threshold). Too high $u$ ⇒ $N_u$ tiny and variance explodes. Guidance:
- **Mean-excess plot:** choose $u$ above which the sample mean-excess function is approximately linear (Danish data: straightens above $u\approx10$, McNeil 1997 §4.1).
- **Stability of $\hat\xi$:** plot $\hat\xi$ against $u$; pick the region where it's flat. McNeil & Frey's simulation (n=1000, t₄) finds the GPD estimator's MSE is **robust** for $k\gtrsim50$ and its optimum near $k\approx100$ - much more forgiving than Hill.
- Tradeoff: e.g. Danish fire losses, $u=10$ (109 exceedances, $\hat\xi=0.497$) vs $u=20$ (36 exceedances, $\hat\xi=0.684$) - both "reasonable," different answers, wider spread at more distant quantiles (McNeil 1997 Table 1).

---

### 3. Computational Implementation - GPD fit + EVT VaR/ES vs empirical

Fit a GPD to the tail excesses of heavy-tailed losses by maximum likelihood (stdlib profile likelihood), then compare EVT VaR/ES to the empirical values at extreme quantiles. Stdlib only.



The fitted shape $\hat\xi=0.360$ recovers the true $1/3$ well. Read the comparison honestly: at $q=0.995$ and $q=0.999$ the EVT VaR/ES track the empirical values closely; at $q=0.9999$ - a one-in-ten-thousand event, of which the sample holds ~2 observations - the empirical VaR ($0.3645$) is dominated by the single second-largest loss and overshoots, while EVT smooths it to $0.3029$. **EVT is model-based interpolation in the tail**: the fitted GPD shape stabilizes the extreme quantile against the noise of a handful of observations, rather than letting one sample point be the answer.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Threshold choice (bias–variance).** The entire method hangs on $u$. Too low ⇒ GPD limit theorem doesn't apply (bias); too high ⇒ few exceedances (variance). McNeil 1997 §4.4 shows the 0.9999-quantile estimate of the Danish data swings with threshold far more than the 0.995 - **distant-quantile estimation is inherently threshold-sensitive**.
2. **Small-sample extrapolation.** Estimating a quantile beyond the data (e.g. the 0.9999th from ~2000 losses) is extrapolation, not measurement. McNeil 1997: the 0.9999-quantile "entails extrapolation of the model beyond the data." Report it as a model output with wide uncertainty, not a fact.
3. **Independence of excesses.** The theory needs i.i.d. exceedances. Real losses cluster (volatility clustering, contagion), inflating the effective $N_u$ and narrowing apparent confidence intervals. Fix: filter volatility first ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Tail-index convention.** "Tail index" means $\alpha=1/\xi$ to Hill/EKM, but $\xi$ to de Haan. $\hat\xi=0.36\equiv\hat\alpha\approx2.8$ - same number, two labels.
5. **$\xi$ near/below $-\tfrac12$.** MLE regularity (asymptotic normality) fails for $\xi<-1/2$; and for $\xi\ge1$ the GPD mean (hence ES) is infinite - the risk measure stops being finite, which is itself information about how heavy the tail is.

---

### 5. References

- **McNeil, Alexander J.**, *Estimating the Tails of Loss Severity Distributions Using Extreme Value Theory*, ASTIN Bulletin 27(1):117–137 (1997)
- **McNeil, Alexander J. & Rüdiger Frey**, *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series*, Journal of Empirical Finance 7(3–4):271–300 (2000)
- **Pickands, James III (1975)**; **Balkema & de Haan (1974)**
- **de Haan & Ferreira (2006)**
- **McNeil, Frey & Embrechts (2015)**

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/03-extreme-value-theory|03 · Extreme Value Theory]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/06-advanced-extensions|06 · Advanced Extensions]]
- Measures: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (what EVT VaR/ES feed into) · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] (the methods EVT improves on)

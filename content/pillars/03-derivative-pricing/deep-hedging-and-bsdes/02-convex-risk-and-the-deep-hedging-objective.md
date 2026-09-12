---
title: "3.14.2 Convex Risk Measures & the Deep-Hedging Objective"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - convex-risk-measures
  - cvar
  - entropic-risk
  - exponential-utility
  - hedging
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/01-from-zero-intuition|01 · From Zero]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]].

---

### 1. Intuition & Practical Objective

Page 01 established that an incomplete market leaves a residual. This page answers the only remaining question: **what do you do with it?** The answer is to *rank* residual distributions, and the ranking device is a convex risk measure. Three objects dominate practice, and they are not interchangeable:

| risk measure | what it penalises | where it comes from | computable? |
|---|---|---|---|
| **variance** $\mathrm{Var}$ | both tails, equally | Föllmer–Sondermann projection, Markowitz | yes - closed form (a regression) |
| **CVaR**$_\alpha$ | the worst $(1-\alpha)$ tail only | Rockafellar–Uryasev, Basel/ES regulation | yes - a convex program, but no PDE |
| **entropic** $\rho_\gamma$ | *all* moments (exponential tilting) | exponential utility, indifference pricing | yes - **a quadratic BSDE** |

The last row is the hinge of the whole folder: *one* of these preferences is analytically tractable, and it is the one that generates a backward SDE - which is why pages 03–04 exist. The one-sentence essence:

> **Convex risk measures are the preference ordering that replaces no-arbitrage in an incomplete market; the entropic measure is the unique one of the family with a closed-form *dynamic* (BSDE) representation, and the mean–variance hedge is its small-risk-aversion limit - so the entire BSDE/Deep-BSDE machinery is the "utility" special case of deep hedging, while CVaR and general convex measures remain purely numerical.**

Three things to internalise:

1. **The risk measure is the objective, not a tuning knob.** §3 shows the *same data, same payoff, same instrument set*, giving optimal hedge ratios $0.56$, $0.59$, $0.66$ under variance, CVaR$_{97.5\%}$ and entropic risk. Nothing else changed.
2. **Entropic risk *is* exponential-utility indifference pricing.** With $U(x)=-e^{-\gamma x}$ the certainty-equivalent is exactly $\rho_\gamma$; the indifference price of a liability $H$ is $\rho_\gamma(H)=\frac1\gamma\ln\mathbb E[e^{\gamma H}]$. That is the bridge to the BSDE of §03 and to every nonlinear pricing result in the literature.
3. **Convexity is what makes learning legitimate.** $\delta\mapsto L_T^\delta$ is affine and $\rho$ is convex, so the deep-hedging objective is convex in the strategy - no spurious local minima from the economics. What *is* non-convex is the *parametrisation* (a neural network), which is why the optimisation is a machine-learning problem at all.

The practical objective: be able to write down and distinguish the three risk measures, know their robust (dual) representations, know the exact entropic/indifference-pricing correspondence, and know that the choice of measure - not the optimiser - determines the hedge.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The axiomatic frame

A *convex risk measure* on a space of bounded random variables is a map $\rho:\mathcal X\to\mathbb R$ with

$$
\text{(monotone) } X\le Y\Rightarrow\rho(X)\le\rho(Y);\quad
\text{(cash-additive) } \rho(X+c)=\rho(X)+c;\quad
\text{(convex) } \rho(\lambda X+(1-\lambda)Y)\le\lambda\rho(X)+(1-\lambda)\rho(Y).
$$

Cash-additivity makes $\rho(X)$ read as "the capital that must be added to $X$ to make it acceptable", which is exactly the desk meaning: the premium. Adding sub-additivity ($\rho(X+Y)\le\rho(X)+\rho(Y)$) upgrades *convex* to *coherent* (Artzner–Delbaen–Eber–Heath 1999) - the CVaR/ES family qualifies, the entropic family does not (it is convex but not coherent; it is *not* positively homogeneous).

The universal dual object is the **robust representation**

$$
\boxed{\ \rho(X)=\sup_{\mathbb Q\in\mathcal Q}\Big(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q)\Big)\ }
$$

with $\mathcal Q$ a set of probability measures and $\alpha$ a penalty function (Föllmer–Schied). This is what turns "minimise a convex risk measure" into "minimise a worst case over a family of models" - the source of the distributionally-robust hedging of [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06]].

#### 2.2 The three workhorse measures

**(i) Variance (quadratic).** $\rho(X)=\mathrm{Var}(X)=\mathbb E[(X-\mathbb E X)^2]$. It is *not* monotone (it ignores the mean), so in deep hedging it is used in the mean-demeaned form $\rho(R(\delta))$ with $R=\delta\Delta S-H$ - the residual already absorbs the mean. The optimal hedge is the regression

$$
\delta^\star=\frac{\mathrm{Cov}(\Delta S,H)}{\mathrm{Var}(\Delta S)} .
$$

**(ii) CVaR (expected shortfall).** With confidence $\alpha$,

$$
\boxed{\ \mathrm{CVaR}_\alpha(X)=\inf_{t\in\mathbb R}\Big\{t+\frac{1}{1-\alpha}\mathbb E\big[(X-t)^+\big]\Big\}=\frac{1}{1-\alpha}\int_\alpha^1\mathrm{VaR}_u(X)\,du=\mathbb E\big[-X\,\big|\,-X\ge\mathrm{VaR}_\alpha\big]\ }
$$

(Rockafellar–Uryasev 2000). It is coherent, and its robust representation uses the *absolutely continuous* set

$$
\mathcal Q_{\mathrm{CVaR}}=\Big\{\mathbb Q\ll\mathbb P:\ \frac{d\mathbb Q}{d\mathbb P}\le\frac{1}{1-\alpha}\Big\},\qquad \rho(X)=\sup_{\mathbb Q\in\mathcal Q_{\mathrm{CVaR}}}\mathbb E_{\mathbb Q}[-X].
$$

For $X\sim N(0,1)$ there is a closed form: $\mathrm{CVaR}_\alpha(X)=\varphi(z_\alpha)/(1-\alpha)$ with $z_\alpha=\Phi^{-1}(\alpha)$ - the check used in §3.

**(iii) Entropic risk.** For $\gamma>0$,

$$
\boxed{\ \rho_\gamma(X)=\frac1\gamma\ln\mathbb E\big[e^{\gamma X}\big]\ }
$$

which is monotone, cash-additive and convex, with $X\sim N(m,s^2)\Rightarrow\rho_\gamma(X)=m+\tfrac{\gamma}{2}s^2$ **exactly**. Its robust representation is the "reverse" one over *all* measures,

$$
\rho_\gamma(X)=\sup_{\mathbb Q\ll\mathbb P}\Big(\mathbb E_{\mathbb Q}[-X]-\tfrac1\gamma H(\mathbb Q\|\mathbb P)\Big),\qquad H=\text{relative entropy},
$$

which is the Girsanov log-density in the diffusion case - the exact reason it produces a *BSDE with a quadratic driver* (§03).

#### 2.3 Entropic risk = exponential-utility indifference pricing

Let $U(x)=-e^{-\gamma x}$ (CARA) and consider a seller of a liability $H$. The *indifference price* $p$ is the cash making her indifferent between selling (and hedging optimally) and not:

$$
\sup_\delta\mathbb E\big[U\big(p+X_T^\delta-H\big)\big]=\sup_\delta\mathbb E\big[U\big(X_T^\delta\big)\big].
$$

In the zero-hedge / complete-market case this collapses to

$$
-e^{-\gamma p}\mathbb E\big[e^{\gamma H}\big]=-1\quad\Longrightarrow\quad
\boxed{\ p^{\mathrm{ind}}=\frac1\gamma\ln\mathbb E\big[e^{\gamma H}\big]=\rho_\gamma(H)\ } .
$$

**The indifference price *is* the entropic risk measure of the liability.** This identity is the entire justification for calling the risk-measure-minimising hedge "utility-based", and it is what makes the entropic case solvable by a BSDE rather than by brute-force learning.

#### 2.4 The mean–variance limit (the bridge back to page 01)

Expand the entropic transform in small risk aversion:

$$
\ln\mathbb E[e^{-\gamma\xi}]=-\gamma\mathbb E[\xi]+\frac{\gamma^2}{2}\mathrm{Var}(\xi)+O(\gamma^3)
\quad\Longrightarrow\quad
\boxed{\ Y_0=-\frac1\gamma\ln\mathbb E[e^{-\gamma\xi}]=\mathbb E[\xi]-\frac{\gamma}{2}\mathrm{Var}(\xi)+O(\gamma^2)\ } .
$$

So **quadratic (variance-optimal) hedging is the $\gamma\to0$ limit of the entropic/BSDE problem**. This is why the Föllmer–Sondermann projection of page 01 is not a *different* theory from the BSDE one - it is its first-order approximation, and the two agree exactly in the limit. For a Gaussian terminal it is exact: $\xi\sim N(m,s^2)\Rightarrow Y_0=m-\tfrac{\gamma}{2}s^2$ (§03 check C confirms this numerically).

#### 2.5 Transaction-cost-aware objectives

Costs enter the objective, not the model: with proportional cost $\kappa$ on traded notional, the static one-period problem becomes

$$
\min_{c,\delta}\ \mathrm{Var}\big(c+\delta\Delta S-H\big)+\underbrace{\kappa\,|\delta|\,S_0}_{\text{cost}} ,
$$

whose solution is $\delta^\star(\kappa)=\big(\mathrm{Cov}(\Delta S,H)-\tfrac{\kappa S_0}{2}\big)/\mathrm{Var}(\Delta S)$ - the hedge **shrinks** linearly in $\kappa$. Multi-period, the cost term is $\kappa\sum_i|\delta_{t_i}-\delta_{t_{i-1}}|S_{t_i}$: a *path* functional, so the objective is no longer a function of a single number and the deep-hedging formulation becomes unavoidable. §05 quantifies both effects (the optimum frequency, and Leland's asymptotic correction in §06).

---

### 3. Computational Implementation - the risk measure picks the hedge

We (a) verify the closed forms of CVaR and entropic risk on a standard-normal sample, and (b) minimise three *different* convex risk measures over the one-period hedge ratio applied to a **jump-diffusion** residual, showing that the optimal hedge is a function of the preference, not of the data.




**Reading the output.**

- **(a) The closed forms are reproduced.** CVaR: the empirical values $1.7589/2.0686/2.3450/2.6711$ sit $0.2$–$0.3\%$ above the exact $\varphi(z_\alpha)/(1-\alpha)=1.7550/2.0627/2.3378/2.6652$ - the residual is the *discreteness of the empirical quantile* ($k=(1-\alpha)n$ atoms in the tail), which biases the estimate slightly upward. Entropic: $0.2511/0.5006/1.0034$ against $\gamma/2=0.25/0.5/1.0$, i.e. within one or two Monte-Carlo standard errors ($0.0024$–$0.0098$). Both families are correct to sampling precision, and the standard errors are reported so that "within tolerance" is a *measured* statement, not a claim.
- **(b) The preference, not the data, chooses the hedge.** All three columns are computed from **the same 60 000 residual paths**: variance is minimised at $\delta=0.56$, CVaR$_{97.5\%}$ at $0.59$, entropic ($\gamma=1$) at $0.66$. Moving from the variance hedge to the CVaR hedge *costs* $1.26\%$ of variance and *buys* $1.62\%$ of CVaR; the entropic hedge sacrifices $12\%$ of variance. There is no "correct" answer here - there is only the stated preference, and the spread between the three answers (a $18\%$ range in the hedge ratio, $0.56\to0.66$) is the *size of the modelling decision* a desk makes when it names its risk measure.
- **The jump does the work.** With a symmetric residual all three measures would coincide at the same $\delta$ (the residual is a linear function of $\delta$, and for a symmetric payoff the optima nearly agree). The downward $5\%$ jump makes the loss distribution *skewed*, and it is exactly the asymmetric measures (CVaR, entropic) that then demand a *larger* hedge. This is the same leverage/skew mechanism as [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|stochastic volatility]], now applied to the *hedge* rather than the price.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Choosing the risk measure to make the hedge cheap.** Because the objective *is* the preference, a desk can loosen $\alpha$ (CVaR) or lower $\gamma$ (entropic) until the "optimal" hedge is the one it wanted. The mitigation is governance, not mathematics: the risk measure belongs to the risk function, not the trading desk. Compare [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]].
2. **Using variance as if it were a risk measure.** Variance is not monotone: adding a deterministic loss leaves it unchanged, and it penalises upside and downside identically. For a *short* option book, upside and downside are not symmetric and variance systematically under-hedges the left tail. It survives in practice only as the small-risk-aversion limit (§2.4) and because it has a closed form.
3. **Confusing CVaR's two definitions.** $\mathbb E[-X\mid -X\ge\mathrm{VaR}_\alpha]$ and $\inf_t\{t+\frac{1}{1-\alpha}\mathbb E[(X-t)^+]\}$ agree for continuous distributions but **differ for atoms**. Simulated P&Ls are *always* discrete, so the two estimators differ at the $O(1/n)$ level. State which one you implement (the infimum form is the convex program used in learning; the conditional-mean form is the reporting number). Here §3 reports the conditional-mean form after demeaning.
4. **Forgetting that cash-additivity requires the premium to be exogenous.** If $p$ is optimised jointly with $\delta$ under a non-mean-centred $\rho$ (e.g. raw CVaR), the objective is unbounded below in $p$ and the "optimum" is $-\infty$. The standard fix - used in §3 - is to *demean the residual*, i.e. optimise the shape of the risk and let cash handle the level.
5. **Reading the entropic $\gamma$ as a market parameter.** $\gamma$ is a *preference* (risk aversion), not a calibrated quantity, and it cannot be inferred from option prices. Calibrating $\gamma$ to make deep hedging reproduce a market price is circular: it fits the preference to a quantity that does not observe it.
6. **Assuming the robust representation is innocent.** $\rho(X)=\sup_{\mathbb Q\in\mathcal Q}(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q))$ turns a risk-measure minimisation into a *min–max* problem, and the inner adversary has to be represented too (a second network, or an explicit finite set of measures as in §06). Deep hedging with CVaR is therefore an *adversarial* learning problem, with all the stability issues that implies ([[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading|RL for Trading]]).
7. **Treating transaction costs as a "small adjustment".** In the one-period problem the shift is $O(\kappa S_0/\mathrm{Var}(\Delta S))$ (tiny for small $\kappa$), which is why a single-period cost adjustment looks negligible. Multi-period, the cost is summed over the *path* and dominates the $\sqrt{\Delta t}$ gain from finer rebalancing (§05, §06). Never import the one-period intuition into the multi-period problem.
8. **Ignoring that the objective is $L^2$-convex but the *parametrisation* is not.** Convexity of the economics guarantees a unique optimum *in strategy space*; it says nothing about the loss surface in *weight space* once the strategy is a neural network. Multiple weight configurations represent (nearly) the same strategy and can have very different apparent loss (§05, training instability).

---

### 5. References

- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291
- **Artzner, P., Delbaen, F., Eber, J.-M., Heath, D.** (1999), *Coherent measures of risk*, Mathematical Finance 9(3), 203–228
- **Rockafellar, R.T. & Uryasev, S.** (2000), *Optimization of conditional value-at-risk*, Journal of Risk 2, 21–41
- **Föllmer, H. & Sondermann, D.** (1986), *Hedging of non-redundant contingent claims*; **Schweizer, M.** (2001), *A guided tour through quadratic hedging approaches*
- **Musiela, M. & Zariphopoulou, T.** (2004), *A valuation algorithm for indifference prices in incomplete markets*, Finance & Stochastics 8, 399–414
- **Almgren, R. & Chriss, N.** (2001), *Optimal execution of portfolio transactions*, Journal of Risk 3, 5–39
- **Hull, J.**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]]
- Forward: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] (why entropic risk is a quadratic BSDE) · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Risk measures in the risk pillar: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|VaR/ES · 04 Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|VaR/ES · 05 Failure Modes]]
- Cost side: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs|Constraints & Transaction Costs]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|P5 · 03 Transaction-Cost Models]] · [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|MM · 03 Temporary vs Permanent Impact]]
- Utility/hedging classics: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|VS · 05 Failure Modes]]
- Robustness: [[pillars/05-portfolio-optimization/robust-optimization|Robust Optimization]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]]

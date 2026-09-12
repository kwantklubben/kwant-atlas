---
title: "4.8.1 Model Risk from Zero"
tags:
  - pillar-quantitative-risk
  - model-risk-and-validation
  - intuition
  - model-risk
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (quantiles, likelihood) and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (the number whose *model* risk this folder is about).

---

### 1. Intuition & Practical Objective

This page builds the *why* of model risk with **no prior risk-management knowledge needed**. The objective is one idea: **a model is a toy, not the world; the risk you carry is not the model's error in the abstract but the model's error *multiplied by your decision's sensitivity to it*.**

Start with the dumbest honest question: *if I have a risk model, what can go wrong?* The tempting answer is "the model could be inaccurate." That is true and useless. The useful answer decomposes the worry into things you can *measure*:

1. **The output is a point, the truth is unknown.** A $99\%$ VaR of \$10M is not a fact; it is one number produced by choosing a distribution, a window, an estimator. Change any one and the number moves. **That movement is the model risk.**
2. **Models are what you build when you cannot see the future.** Derman's observation: in physics the variables (mass, time) exist whether or not humans do; in finance the variables (expected return, volatility) are *human expectations* - hidden variables inferred, not observed. You are always extrapolating from a proxy.
3. **The failure is not symmetric with useful effort.** Most modelling effort goes into precision (more factors, faster calibration); most model risk sits in *assumption* error (wrong functional form, wrong window, wrong dependence). Precise answers to the wrong question are the signature of a model-risk event.

Three steps:

1. **Same data, different defensible models, materially different numbers.** Feed one realistic (fat-tailed) sample to three textbook-defensible VaR estimators - parametric-normal, historical, and peaks-over-threshold EVT - and watch the $99.9\%$ number differ by up to $40\%$. Nobody made a mistake. That gap *is* model risk.
2. **Model risk lives in the tail.** The three estimators agree closely at the $95\%$ quantile and diverge wildly at $99.9\%$, because that is where no estimator has data and every estimator substitutes an *assumption* for evidence.
3. **Managing model risk is not "getting the right model"; it is bounding the decision's exposure to being wrong** - a validation process, an error budget, a conservative add-on, and an organisational authority to say "do not use this".

---

### 2. Mathematical Ground Truth & Derivations

**A model, formally.** A valuation/risk model is a map $V_\theta$ from inputs $X$ and parameters $\theta$ (estimated from data or implied) to an output (price, VaR, capital). The **true** quantity is $V^\star(X)$. The **model error** is
$$
\Delta V \;=\; V_\theta(X)-V^\star(X).
$$
Model risk is the *distribution* of $\Delta V$ induced by uncertainty in (i) the functional form $V_\bullet$, (ii) the parameters $\theta$, (iii) the implementation, and (iv) the use. SR-11-7's two causes map onto this directly: fundamental error (i–iii) and misuse (iv).

**Quantile model risk.** For a loss $L$ with CDF $F$, the $\alpha$-quantile (VaR) is $q_\alpha=F^{-1}(\alpha)$. Two models $F_A,F_B$ give $\mathrm{VaR}^{A}_\alpha,\mathrm{VaR}^{B}_\alpha$. The **relative model risk** is
$$
\mathrm{MR}_\alpha=\frac{\big|\mathrm{VaR}^{A}_\alpha-\mathrm{VaR}^{B}_\alpha\big|}{\mathrm{VaR}^{A}_\alpha}.
$$
Because the density $f$ thins in the tail, $\mathrm{MR}_\alpha$ **grows with $\alpha$** - the same two models can agree to $1\%$ at the median and disagree by $50\%$ at $99.9\%$. Formally, if the two models differ by a slowly-varying ratio $\rho$ in the tail (a differing tail index $\xi_A\ne\xi_B$), then $q^A_\alpha/q^B_\alpha\sim(\dots)\alpha^{\xi_B-\xi_A}$: the discrepancy is **power-law amplified** in $\alpha$. Tail indices are exactly what data-poor quantiles estimate worst - hence the amplification.

**The peaks-over-threshold (POT) estimator** used below (Pickands–Balkema–de Haan): above a high threshold $u$ the excess distribution is approximately Generalized Pareto, $Y=L-u\mid L>u\sim\mathrm{GPD}(\xi,\beta)$. With $N_u$ exceedances in $N$ observations, the quantile is
$$
\widehat{\mathrm{VaR}}_\alpha \;=\; u+\frac{\widehat\beta}{\widehat\xi}\Big[\Big(\tfrac{N}{N_u}(1-\alpha)\Big)^{-\widehat\xi}-1\Big],
$$
and a method-of-moments fit gives $\widehat\xi=\tfrac12\big(1-\bar y^2/s^2\big)$, $\widehat\beta=\tfrac12\bar y\big(\bar y^2/s^2+1\big)$ from the exceedance mean $\bar y$ and variance $s^2$. The normal estimator, by contrast, is $\widehat{\mathrm{VaR}}_\alpha=\hat\mu+\hat\sigma z_\alpha$ - a *single* assumption about the tail shape.

---

### 3. Computational Implementation - one sample, three models

We draw $N=2000$ i.i.d. returns from a **Student-$t$ with $\nu=5$ degrees of freedom, scaled to unit variance** (a standard fat-tailed proxy; $\sqrt{(\nu-2)/\nu}=\sqrt{3/5}$). We then estimate the $99\%$, $99.5\%$ and $99.9\%$ VaR three ways: parametric-normal, historical (empirical quantile), and POT-GPD. Stdlib only, seeded, deterministic.




The move from $99\%$ to $99.9\%$ is the whole lesson in one line: **the spread across three standard, defensible models grows from $7.6\%$ to $40.8\%$ purely as you ask the question where there is no data.** At $99.9\%$ with $N=2000$, the historical estimate is essentially the single worst or second-worst observation - a sample of size one dressed as a quantile - while the normal estimator substitutes a thin-tailed assumption that the data reject. All three are "correct" implementations of different models. The gap is model risk.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Mistaking precision for accuracy.** A model that reproduces its own inputs to six decimals feels trustworthy and says nothing about $\Delta V$. The $40.8\%$ spread above exists between *correctly coded* estimators.
2. **The tail is an assumption, not an observation.** Past the largest few observations, every quantile estimator is extrapolation; the choice of extrapolation rule (normal tail vs GPD tail vs empirical) dominates. Denying this is the first failure; recognising it is the start of this folder.
3. **Model independence is assumed, not tested.** Two "independent" validators who share the same data, codebase and training will share the same blind spot and certify the same error - the illusion of diversity (develop this in [[pillars/04-quantitative-risk/model-risk-and-validation/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **The decision, not the number, is what is at risk.** A $40\%$ VaR error matters only through leverage, limits and capital it drives. Always convert model error into the *decision* it changes - that is the error budget of [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|02 · Sources of Model Risk]].

---

### 5. Canonical Literature & Study References

- **Derman, E.**, *Model Risk*, Goldman Sachs QSR Notes (1996) - "Models translate opinions into values", "Uncertainty is fundamental", "A model is only a model…". *Read in full from the corpus PDF.*
- **Federal Reserve / OCC**, *SR 11-7* (2011) - the definition of model risk and the two causes. *Read in full from the corpus PDF.*
- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015), Ch 2 (risk measures) and Ch 7 (EVT: POT/GPD quantile). The spine reference for the POT estimator used above.
- **Embrechts, Klüppelberg & Mikosch**, *Modelling Extremal Events* (1997) - the EVT monograph behind the tail-discrepancy power law.

---

### 6. Connected Graph Bridges

- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Continue: [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|02 · Sources of Model Risk]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] (the POT machinery in full)

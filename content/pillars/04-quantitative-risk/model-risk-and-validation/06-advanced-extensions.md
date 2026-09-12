---
title: "4.8.6 Advanced Extensions"
tags:
  - pillar-quantitative-risk
  - model-risk-and-validation
  - model-uncertainty
  - bayesian-model-averaging
  - relative-entropy
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/model-risk-and-validation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[foundations/bayesian-statistics/index|Bayesian Statistics]] (posterior weighting, information criteria).

---

### 1. Intuition & Practical Objective

The earlier pages *reduce* model risk (validate, benchmark, budget). This page **quantifies and prices** it. Three constructs turn "we might be wrong" into a number that sits next to the value:

1. **Bayesian model averaging (BMA).** Instead of picking *the* model, carry all of them weighted by their evidence, and read the spread as the model-selection uncertainty.
2. **Relative entropy (KL divergence).** Measure *how far* one model is from another in information terms - a principled scalar for "how much do these models disagree?", with an operational reading as an entropy budget.
3. **Entropy-robust bounds.** Given only "the true model is within an entropy budget $\varepsilon$ of our reference model", compute the *worst-case* (robust) value and hence a defensible model-risk add-on.

The objective: replace a single point estimate with a **range** whose width is the model uncertainty, and whose construction is defensible to a validator. This is the quantitative half of the framework - it is what Morini calls *valuing* model risk rather than merely flagging it.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Bayesian model averaging.** With candidate models $\mathcal M_i$, Bayesian posterior weights are $w_i=\mathbb P(\mathcal M_i\mid\mathcal D)\propto \mathbb P(\mathcal D\mid\mathcal M_i)\,\mathbb P(\mathcal M_i)$. A practical, BIC-based approximation (ESL eq. 7.35) is
$$
w_i=\frac{e^{-\frac12\Delta\mathrm{BIC}_i}}{\sum_j e^{-\frac12\Delta\mathrm{BIC}_j}},\qquad \Delta\mathrm{BIC}_i=\mathrm{BIC}_i-\min_j\mathrm{BIC}_j,
$$
and the BMA estimate and its model-selection variance are
$$
\bar V=\sum_i w_iV_i,\qquad \sigma_{\text{model}}^2=\sum_i w_i\,(V_i-\bar V)^2.
$$
$\sigma_{\text{model}}$ is the model risk *made explicit*: it is large precisely when the models disagree, and it shrinks automatically when the evidence concentrates.

**2.2 Relative entropy (KL divergence).** The information distance from model $Q$ to model $P$ is
$$
D_{\mathrm{KL}}(P\|Q)=\int p(x)\ln\frac{p(x)}{q(x)}\,dx\ \ge 0,
$$
finite and closed-form for Gaussians:
$$
D_{\mathrm{KL}}\!\big(\mathcal N(\mu_P,\sigma_P)\|\mathcal N(\mu_Q,\sigma_Q)\big)=\ln\frac{\sigma_Q}{\sigma_P}+\frac{\sigma_P^2+(\mu_P-\mu_Q)^2}{2\sigma_Q^2}-\frac12 .
$$
It is **asymmetric** (it is not a metric) and *quadratic* in the mean gap but only logarithmically sensitive to scale differences - matching the intuition that a small shift in the mean of a forecast is worse than a small shift in its width.

**2.3 Entropy-robust value bounds.** Let $X$ be a payoff and $P$ the reference (pricing) measure. Define the ambiguity set $\mathcal U_\varepsilon=\{Q\ \text{model}: D_{\mathrm{KL}}(Q\|P)\le\varepsilon\}$. The worst-case value is a *dual* object whose second-order expansion is
$$
\sup_{Q\in\mathcal U_\varepsilon}\mathbb E_Q[X]\;=\;\mathbb E_P[X]+\sqrt{2\varepsilon\,\operatorname{Var}_P(X)}\;+\;\mathcal O(\varepsilon),
$$
obtained by exponential tilting $dQ/dP\propto e^{\theta X}$ with $\theta=\theta(\varepsilon)$ set by the entropy budget. The right-hand side is the **model-risk add-on**: a non-negative premium that vanishes as $\varepsilon\to0$, grows with the payoff's dispersion, and is *robust* - it does not require knowing which alternative model is true, only how far any alternative is allowed to be. Cont's program (model uncertainty and the pricing of derivatives) is the systematic version of this.

**2.4 Reading the three together.** BMA gives a *weighted ensemble* (prediction), KL gives a *distance* (diagnostic), and the robust bound gives a *worst case* (capital). A complete advanced model-risk report states all three: the central estimate, the inter-model disagreement, and the entropy-budgeted bound.

---

### 3. Computational Implementation

Stdlib only. (A) BMA weights and spread for three option models; (B) KL between Gaussian model views; (C) the entropy-robust bound for a call payoff.




Reading it: the three models span $10.45\to11.40$, a $\pm5\%$ range; BIC weighting pulls the BMA to $10.6179$ with a **model-selection sd of $0.2903$** (about $2.8\%$ of value). The KL divergences quantify *how far* the alternative views are: shifting the mean by $0.05$ and widening by $10\%$ costs only $0.0096$ nats, whereas a $0.20$ shift and $40\%$ widening costs $0.102$ nats - an order of magnitude more. The robust bounds then turn the entropy budget into a price: with the payoff variance from the reference model, allowing $\varepsilon=0.001$ nats of model deviation adds $+ $ \$0.655 to the value, \varepsilon=0.01$ adds $+ $ $\$2.071, and \varepsilon=0.05$ adds $+ $ $\$4.632 - **a monotone, defensible model-risk add-on**. (The base uses a Monte Carlo reference expectation \approx10.4733$; the small gap from the analytic $10.4506$ is simulation noise.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **BMA near-degeneracy.** If one model's BIC dominates, its weight $\to1$ and the ensemble silently reverts to the single model - model risk looks small while it is merely *undetected*. Always report the weight vector, not just the BMA price.
2. **Priors as hidden assumptions.** BMA weights depend on model priors $\mathbb P(\mathcal M_i)$; a "flat" prior over *many variants of one model* over-weights that family. The prior is a model choice with its own model risk.
3. **Wrong divergence.** KL is asymmetric and infinite when $Q$ has support where $P$ does not (a mis-specified tail can make $D_{\mathrm{KL}}=\infty$); Jensen–Shannon or Hellinger are the symmetric alternatives. Reporting "distance" without stating the direction is a category error.
4. **Trusting $\varepsilon$.** The entropy budget is *itself* a judgement; a robust bound with a small $\varepsilon$ is only as good as the argument that the truth lies within it. Make $\varepsilon$ exogenous (regulatory, or derived from estimation-error size), not chosen to produce a comfortable number.
5. **Second-order bound misused.** $\sqrt{2\varepsilon\operatorname{Var}_P(X)}$ is the leading term; for large $\varepsilon$ or heavy tails the exact dual (exponential tilt) differs - use the closed-form tilt when $\varepsilon$ is not small.
6. **Robustness without governance.** A bound is only useful once it feeds a limit, a capital add-on or a use-restriction - otherwise it is an elegant number with no owner ([[pillars/04-quantitative-risk/model-risk-and-validation/04-model-risk-management|04 · §2.3]]).

---

### 5. References

- **Hastie, Tibshirani & Friedman**, *ESL* 2nd ed. (2009)
- **Cont, R.**, *Model Uncertainty and Its Impact on the Pricing of Derivative Instruments*, *Mathematical Finance* 16(3):519–547 (2006)
- **Morini, M.**, *Understanding and Managing Model Risk* (2011)
- **Acerbi, C.**, *Spectral Measures of Risk* (2002) and **Artzner et al.** (1999)
- **Glasserman, P. & Xu, X.**, *Robust Risk Measurement and Model Risk*, *Quantitative Finance* 14(1):29–58 (2014)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/model-risk-and-validation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/model-risk-and-validation/04-model-risk-management|04 · Model-Risk Management]]
- Base: [[foundations/bayesian-statistics/index|Bayesian Statistics]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Coherent Risk Measures]]
- Forward: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Index Hub]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] (ensembles, stacking, low-SNR uncertainty)

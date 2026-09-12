---
title: "3.13.5 Failure Modes & Practice"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - failure-modes
  - calibration
  - gauge-freedom
  - model-risk
  - usable-models
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/03-the-particle-method|03 · The Particle Method]] and [[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04 · The Fokker–Planck / McKean–Vlasov Route]].

---

### 1. Intuition & Practical Objective

Everything up to here was mathematics; this page is about what goes wrong when LSV is put on a desk. Five symptom classes, each traceable to a first principle:

1. **The proxy bias.** $\mathbb E[v_t|S_t=S]\ne\mathbb E[v_t]$. Using the forward-variance curve as the conditional variance is the single most common implementation error, and - as §03 showed - it can make the calibrated model *worse* than the un-levered one.
2. **Estimator noise.** $m(t,S)$ is estimated from a finite sample, and the error propagates as $\delta\ln\sigma=-\tfrac12\delta\ln m$. In the wings, where the bins are thin, this becomes a *systematic-looking* wing distortion.
3. **The gauge.** The LSV parameterisation is redundant: $\zeta^u\to\varphi^u\zeta^u$ with $\sigma\to\sigma/\sqrt{\varphi^u}$ leaves the spot process invariant. Two implementations can report different leverage surfaces and identical prices.
4. **"Usable" versus "not a model".** Bergomi's admissibility condition - the pricing function must be insensitive to the SV state variables for fixed hedge instruments - is *not* automatic. A forward-variance-driven LSV is admissible; a Heston-driven LSV generally is not, and its hedged P&L leaks spurious terms.
5. **Model risk dwarfs parameter risk.** Because vanillas see only the product $\sigma^2m$, agreement on prices says nothing about agreement on dynamics. Two models that fit today's surface can disagree on forward skew by whole vol points ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston · 05]]).

The practical objective: know the size of the proxy error and of the binning error, know how to fix the gauge, know how to test admissibility, and be able to state where an LSV model's *unobservable* content lives.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The proxy bias, quantified

Define the proxy $\hat m(t,S)=\xi_0^t=\mathbb E[v_t]$ and the truth $m(t,S)=\mathbb E[v_t|S_t=S]$. Then

$$
\frac{m}{\xi_0^t}-1=\text{relative error in the model's local standard deviation},\qquad \frac{\sigma_{proxy}}{\sigma_{true}}-1=\sqrt{\frac{\xi_0^t}{m}}-1=\text{relative error in the leverage}.
$$

Because local variance $=\sigma^2m$, substituting the proxy for $m$ leaves the local variance multiplied by $m/\xi_0^t$ - *not* unity. The proxy is exact only when $v_t$ is independent of $S_t$ (the LV limit, or $\rho=0$ with a deterministic driver).

**How big is it?** It depends on $\rho$ and on the variance-of-variance. Two reference numbers:

- **No correlation at all** (§3 below, two-state toy): $m/\xi_0^t-1=+79.6\%$ in the wings and $-40.0\%$ at the money. The conditional variance is a *strike-dependent* object even when the spot and the vol are independent, because at the money the region where $S_t\approx S_0$ mixes both vol states while the wings are dominated by one of them.
- **Fitted index parameters, real correlation** (§03, Heston-LSV at $t=1$): $m(1,S)/\xi_0^1$ runs from $5.63$ in the crash wing ($m=0.17249$ vs $\xi_0^1=0.03062$) to $0.32$ in the upside wing ($0.00975$). And the proxy does not merely bias the result: it produced a smile of $24.4\%/13.6\%$ across the wings against a flat-$20\%$ target - *worse* than the un-levered Heston ($20.8\%/11.0\%$).

That last fact is worth stating plainly: **an LSV implementation that uses the forward-variance proxy can produce a more skewed smile than the model it was supposed to bend.**

#### 2.2 Error propagation for the estimator

From $\sigma^2=\sigma^2_{loc}/m$, log-differentiate:

$$
\boxed{\;\delta\ln\sigma=\tfrac12\left(\delta\ln\sigma^2_{loc}-\delta\ln m\right)\;}
$$

So a $1\%$ error in $m$ is a $0.5\%$ error in $\sigma$. In the particle method the estimator is a bin mean, so

$$
\mathrm{SE}\big(\hat m\big)\simeq\sqrt{\frac{\mathrm{Var}(v_t\,|\,S_t)}{n_{bin}}},
$$

with the conditional variance estimated inside the bin. Note the $n_{bin}$: doubling the accuracy in the wings requires *four times* the paths *per bin*, and the bins that matter most (the far wings, which set the wing skew) are exactly the ones with the fewest paths. This is the dimensional curse of the particle method: the number of bins grows with the richness of the leverage surface one wants to represent, while the paths are spread over the whole spot range.

#### 2.3 Gauge freedom (the LSV redundancy)

Consider a forward-variance driver $\zeta^u_t$ and the LSV spot process

$$
dS_t=(r-q)S_tdt+\sigma(t,S_t)\sqrt{\zeta_t^t}\,S_tdW^S_t.
$$

Apply the transformation

$$
\zeta^u\to\varphi^u\zeta^u\quad(\varphi^u>0\ \text{constant in }u),\qquad \sigma(u,S)\to\frac{\sigma(u,S)}{\sqrt{\varphi^u}}.
$$

The instantaneous variance is $\sigma(t,S_t)^2\zeta_t^t\to(\sigma^2/\varphi^t)(\varphi^t\zeta_t^t)=\sigma(t,S_t)^2\zeta_t^t$: **invariant**. Hence the spot process, and every vanilla price, is unchanged - the transformation is a **gauge redundancy**. Its consequence is that the leverage function is only defined up to this family: the "level" of $\sigma$ has no invariant meaning, only the product $\sigma^2\zeta$ does. Fixing the gauge (e.g. requiring $\zeta^u_0$ to equal the market variance-swap curve) is a *modelling convention*, not a derivation.

#### 2.4 The admissibility condition ("usable" LSV)

Fix the hedge instruments: the spot and a set of vanilla option prices $\{O_i\}$. A pricing function $P$ is **usable** if the P&L of a delta- and vega-hedged position, expanded to second order in the instrument variations and first order in $\delta t$, reads as a pure gamma/theta carry plus a hedge covariance term - with no residual dependence on the *model-specific* state variables. With $x=(S,\{O_i\},\{\lambda_k\})$, $\lambda_k$ the SV state variables, the condition is

$$
\boxed{\;\frac{\partial P}{\partial \lambda_k}\bigg|_{S,\{O_i\}}=0\quad\forall k\;}
$$

If it fails, the hedged P&L contains terms like $\tfrac12\frac{\partial^2P}{\partial\lambda_k\partial\lambda_l}(\delta\lambda_k\delta\lambda_l-\hat a_{kl}\delta t)$ and $\frac{\partial P}{\partial\lambda_k}\delta\lambda_k$ that "have no financial significance" and cannot be hedged away, since hedge instrument prices do not depend on $\lambda_k$. Bergomi's verdict is blunt: **"most local-stochastic volatility models are not usable models."**

Which side of the line does LSV fall on?

- **Forward-variance-driven LSV: admissible.** The rescaling $\zeta^u\to\varphi^u\zeta^u$, $\sigma\to\sigma/\sqrt{\varphi^u}$ (the gauge of §2.3) leaves the spot process invariant, so $\partial P/\partial\zeta^u\equiv0$ and the condition holds. This is a *structural* property of the lognormal forward-variance driver, and it is why LSV-with-a-variance-curve is the production construction.
- **Heston-driven LSV: generally not admissible.** $P$ depends on the Heston state variable $V$, and the leakage is of order $\mathrm{Var}(v_T)\,\partial^2P/\partial V^2$ - small for vanilla-like payoffs, large for strongly vega-convex ones.

The practical reading: choosing the *driver* is not only a dynamics choice, it is an **admissibility** choice. An admissible driver (forward variance) costs you a measure of realism in the spot/vol correlation; an inadmissible driver (Heston) costs you a well-defined hedge P&L.

#### 2.5 Where the unobservable content lives

Split the model's content into three buckets:

| bucket | pinned by | example |
|---|---|---|
| vanillas | the target surface | the *product* $\sigma^2m$ |
| the driver | the modelling choice + variance-swap / vol-of-vol instruments | forward skew, SSR, $\nu_T(t)$ |
| the gauge | nothing | the level of $\sigma$ |

Everything that exotic products price lives in the second bucket, and the second bucket is *not fitted to vanillas*. This is the LSV restatement of the folder's central warning: **the static fit is a constraint, not a test.**

---

### 3. Computational Implementation - proxy bias, error propagation, gauge and binning noise

We quantify the four failure modes: the proxy bias and the leverage error it induces (exact, two-state toy), the error-propagation law, the gauge invariance, and the binning standard error with an independent Monte-Carlo check of the CIR variance used in it. Stdlib only.




**Reading the output.**

- **(1) The proxy bias is large even without correlation.** $m/\xi_0^t-1$ is $+79.6\%$ in the wings and $-40.0\%$ at the money; the induced leverage error is $-25.4\%$ and $+29.1\%$ respectively. The pattern is structural, not statistical: at the money the density at $X_t\approx0$ mixes both volatility states (weighting the *narrow* state more heavily, which pushes $m$ down), while the wings are dominated by the single wide state (pushing $m$ up). In the toy the effect is symmetric; with $\rho\ne0$ it becomes asymmetric and much larger (§03's $5.6\times/0.32\times$).
- **(2) The propagation law is linear in the logs.** $\delta\ln\sigma=-\tfrac12\delta\ln m$: a $-20\%$ error in $m$ is a $+10\%$ error in $\sigma$, and - because the *product* $\sigma^2m$ is what prices vanillas - the local variance is wrong by $-20\%$. Note the asymmetry of the practical reading: a binning *underestimate* of $m$ inflates the leverage, and the two errors partially cancel in the local variance only if you know which one you made. You do not.
- **(3) The gauge is exact.** The transformation $\zeta^u\to\varphi^u\zeta^u$, $\sigma\to\sigma/\sqrt{\varphi^u}$ leaves $\sigma^2\zeta^t$ invariant to machine precision for $\varphi=0.25,2,4$. This is the redundancy that makes "the leverage level" meaningless and, in the forward-variance case, makes the model *admissible* (§2.4).
- **(4) Binning noise is a real budget item.** The CIR variance formula is confirmed independently by Monte Carlo ($\mathrm{Var}(v_1)=0.001467$ analytic against $0.001471$ simulated with $20000$ Milstein paths). The resulting standard errors: with $500$ paths per bin the conditional-variance error is $5.7\%$ and the local-vol error $0.57$ vol points; you need $\approx10^4$ paths per bin to bring it to $0.13$ vol points. Over a $20$-bin leverage grid that is $2\times10^5$ paths *per iteration*, times $3$–$10$ iterations, times the number of maturities being calibrated. **This is the real cost of the particle method.**
- **A caveat on the SE numbers.** The formula uses the *unconditional* $\mathrm{Var}(v_1)$ as an upper bound for $\mathrm{Var}(v_1|S_1)$; the true conditional variance is smaller in most bins, so the table is conservative. Counteracting that, bins are not independent, the estimates are correlated across neighbouring bins through the shared paths, and the $500$-paths figures are below the practical cutoff - which is why the fill-from-neighbour rule of §03 matters.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using $\xi_0^t$ (or the variance-swap curve) for $m(t,S)$.** The error is O(100%) in the wings even with zero correlation, and it can make the smile *worse* than the un-levered model. It is the defining implementation error of this topic.
2. **Reporting a leverage surface without its gauge.** Different gauges give different $\sigma$ and identical prices. Any comparison of leverage functions across implementations must first fix the gauge (conventionally, $\zeta_0^u$ from the variance-swap market).
3. **Skipping the admissibility test.** Before deploying an LSV model, check $\partial P/\partial\lambda_k|_{S,\{O_i\}}=0$ for the model's SV state variables on the actual product's pricing function. Failing it means the hedged P&L has unhedgeable, financially meaningless terms - the model is a non-model.
4. **Believing more leverage resolution is free.** Every extra bin in $(t,S)$ costs paths: the SE of $m$ scales as $1/\sqrt{n_{bin}}$. Wing bins are the thinnest and the most leveraged, which is the worst possible combination.
5. **Treating the converged leverage as an estimable market quantity.** It is a decomposition of a fitted surface, conditioned on the driver and the gauge. Reporting it as "the market's spot-vol response" is a category error.
6. **Confusing leverage-looking-good with hedge-looking-good.** A model can reproduce the surface to bid–ask and still have the wrong minimum-variance delta, because the delta depends on $\partial\mathbb E[\sigma_{imp}]/\partial S$ - i.e. on the leverage and on $\rho$ - not on the price level. Fit is not hedging.
7. **Arguing parameters when the disagreement is the driver.** Because vanillas constrain only $\sigma^2m$, two desks can disagree on forward-start or cliquet prices *and both be right about vanillas*. Establish agreement on the driver and the admissibility class before arguing about calibration residuals.
8. **Forgetting the vol-of-vol (and variance) risk premium is priced.** $m$ calibrated to vanillas is a $\mathbb Q$ object that embeds a premium; using it as a forecast of realized conditional variance confuses measures ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|Heston · 04]]).
9. **Assuming the McKean–Vlasov iteration always converges.** It is a nonlinear fixed point; extreme smiles, very high vol-of-vol, or a badly resolved wing can stall it. Monitor the residual surface *and* the iteration-to-iteration change in $\sigma$, not just the final fit.

---

### 5. Canonical Literature & Study References

- **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107 - the particle method, the proxy-versus-conditional distinction, and the stability questions. **Guyon, J. & Henry-Labordère, P.** (2013), *Nonlinear Option Pricing* (Chapman & Hall/CRC) - the McKean–Vlasov framework and its well-posedness.
- **Bergomi, L.**, *Local-stochastic volatility: models and non-models*, Risk - the admissibility condition $\partial P/\partial\lambda_k|_{S,\{O_i\}}=0$, the gauge transformation $\zeta^u\to\varphi^u\zeta^u$ with $\sigma\to\sigma/\sqrt{\varphi^u}$ that makes the forward-variance LSV admissible, and the delta discussion. **Bergomi, L.**, *Stochastic Volatility Modeling* (CRC, 2016) - Ch 1 (usable models, P&L attribution), Ch 12 §12.2.2 (*"most local-stochastic volatility models are not usable models"*), Ch 7 (forward-variance drivers and exact simulation). *Math-verified in the corpus.*
- **Hagan, P. S., Kumar, D., Lesniewski, A. & Woodward, D.** (2002), *Managing smile risk*, Wilmott 84–108 - the SABR driver and the LSV-LMM construction; **Ren, Y., Madan, D. & Qian, M. Q.** (2007), *Calibrating and pricing with embedded local volatility models*, Risk **20**(9) - the rates-desk form of LSV, and a case where the gauge is fixed by market convention (the LMM volatility structure).
- **Gatheral, J.**, *The Volatility Surface*, Ch 7 §7.8 (shape is model-generic - the reason fit is not validation) and Ch 8 (digitals and cliquets, where the dynamics show up in the price). **Hull, J. C.**, *Options, Futures, and Other Derivatives*, Ch 20 §20.5 (minimum-variance delta $\Delta_{MV}=\Delta_{BSM}+\mathcal V_{BSM}\partial\mathbb E[\sigma_{imp}]/\partial S$). *Verification report in the corpus.*
- **Andersen, L.** (2008), *Simple and efficient simulation of the Heston stochastic volatility model*; **Lord, Koekkoek & van Dijk** (2010); **Broadie & Kaya** (2006) - the schemes and the exact transitions that keep the binning input clean. **Jourdain, B. & Sbai, M.** (2015) and **Abergel & Tachet** (2010) - calibration stability and well-posedness for LSV.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/03-the-particle-method|03 · The Particle Method]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04 · The Fokker–Planck / McKean–Vlasov Route]]
- Forward: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston & SABR · 05 Failure Modes & Practice]] (Feller vs Milstein, calibration flatness, digital skews) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|Heston & SABR · 04 SV Dynamics]] (SSR, vol-of-vol term structure - the unobservables LSV inherits) · [[pillars/03-derivative-pricing/calibration-and-market-practice|Calibration & Market Practice]] (regularisation, parameter stability, model-risk governance) · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (conditional-mean estimation and its standard errors)

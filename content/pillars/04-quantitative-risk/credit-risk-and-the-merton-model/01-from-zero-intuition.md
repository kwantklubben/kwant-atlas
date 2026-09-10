---
title: "01 — Credit Risk from Zero: Default as an Option on Firm Assets"
tags:
  - pillar-quantitative-risk
  - credit-risk-and-the-merton-model
  - intuition
  - limited-liability
  - default
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (CDFs, expectation) and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black-Scholes-Merton]] (a call \(=\max(S-K,0)\) can be priced from no-arbitrage alone).

---

### 1. Intuition & Practical Objective

This page builds the *why* of credit-risk modelling with **no prior credit knowledge needed**. The objective is one idea, and it is the founding idea of the entire field:

> **Limited liability means the shareholders of a levered firm hold a call option on the firm's assets.** The strike is the debt's face value; the "underlying" is the value of the firm; the expiration is the debt's maturity.

Start with the dumbest question: *why does a bond ever default?* A firm's assets are worth something stochastic, $V$. It owes its creditors a fixed amount $D$ at maturity. If $V_T>D$, the owners pay the debt and keep $V_T-D$. If $V_T\le D$, the owners are *not obligated* to contribute the shortfall — limited liability lets them walk away and hand the firm to the bondholders. So the shareholders' payoff is

$$E_T=\max(V_T-D,\,0),$$

which is exactly the payoff of a European **call option** with underlying $V$, strike $D$, maturing at $T$. The debt's payoff is its complement, $\min(V_T,D)$ — the residual claim.

Three "aha"s:

1. **Default is a rational exercise decision, not an accident.** The shareholders default precisely when exercising would be a bad trade: when the call is out of the money. Default probability is therefore an **exercise probability** — and BSM tells us the risk-neutral exercise probability is $N(-d_2)$.

2. **Everything about a firm's credit quality lives in two unobservable numbers: asset value $V$ and asset volatility $\sigma_V$.** Equity's *price* and *volatility* are observable and are functions of $(V,\sigma_V)$, so in principle we can invert them. That inversion is the whole empirical content — and the whole fragility — of the model.

3. **A credit spread is put premium.** Since $V=E+F$ and $F=\min(V,D)=D-K$ plus a put (put–call parity), a risky bond is a riskless bond *minus a put* on the firm's assets. The bondholders are effectively short a put written to the shareholders. The credit spread is what it costs to be short that put.

---

### 2. Mathematical Ground Truth & Derivations

**The payoff split.** At maturity the total firm value divides without loss,

$$V_T \;=\; E_T + F_T,\qquad E_T=\max(V_T-D,0),\qquad F_T=\min(V_T,D).$$

**Equity is a call; debt is riskless-minus-put.** Using put–call parity for a call with underlying $V$ and strike $D$,
$$E \;=\; V\,N(d_1)-D e^{-rT}N(d_2),$$
so the debt value is
$$F \;=\; V-E \;=\; \underbrace{D\,e^{-rT}}_{\text{risk-free bond}} \;-\; \underbrace{\Big[D\,e^{-rT}N(-d_2)-V\,N(-d_1)\Big]}_{\text{put written to shareholders}}.$$

**The risk-neutral default probability.** In the risk-neutral world $V_T$ is lognormal with drift $r$ and volatility $\sigma_V$, so
$$\mathbb{Q}(V_T<D)=\mathbb{Q}\!\left(\ln\frac{V_T}{V}<\ln\frac{D}{V}\right)=N(-d_2),\qquad d_2=\frac{\ln(V/D)+(r-\tfrac12\sigma_V^2)T}{\sigma_V\sqrt T}.$$
This is the exact statement: **the risk-neutral probability of default is the Black-Scholes risk-neutral exercise probability.** (Section 03 separates this from the *real-world* PD, which uses the physical drift $\mu$.)

**Where the model lives.** Merton (1974) derives this directly from his eq. (10) — the PDE satisfied by $f(V,t)$, the equity value — and notes (his words) that it is "identical to the equations for a European call option on a non-dividend-paying common stock where firm value corresponds to stock price and $B$ corresponds to the exercise price."

---

### 3. Computational Implementation — the payoff split and the kinked claim

The simplest possible demonstration: enumerate terminal firm values and show that equity is a call payoff and debt is the risk-free payoff minus a put. Stdlib only.

```python
D = 100.0                      # face value of the (zero-coupon) debt
print("V_T   equity=E_T   debt=min(V_T,D)   total")
for VT in (60.0, 80.0, 100.0, 120.0, 150.0):
    e = max(VT - D, 0.0)       # call payoff  (limited liability)
    d = min(VT, D)             # bondholders get the rest
    print(f"{VT:5.0f}  {e:9.1f}  {d:14.1f}  {e+d:6.1f}")
```
```
V_T   equity=E_T   debt=min(V_T,D)   total
   60        0.0            60.0    60.0
   80        0.0            80.0    80.0
  100        0.0           100.0   100.0
  120       20.0           100.0   120.0
  150       50.0           100.0   150.0
```
Read the table: below $V_T=100$ the equity is **flat at zero** (the call is out of the money — shareholders walk away) while the debt absorbs the entire shortfall. Above $V_T=100$ the equity rises **one-for-one** and the debt is capped. Equity is a **convex, kinked** claim — exactly a call. The flat-at-zero region *is* default.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "it defaults when it runs out of cash" trap.** Merton's default is a *maturity-event* driven by the *asset value* crossing the debt face — not a liquidity event. A firm can default with cash on hand (strategic default) or survive with negative equity (rolling debt). The model captures only the terminal claim structure.
2. **Asset value is a fictional, unobservable variable.** Nobody observes "$V$". The model's inputs are equity price and equity vol; the firm's asset value and vol are *inferred*, and the inference is ill-conditioned (see [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **One zero-coupon bond is a caricature.** Real firms have layered, coupon-paying, callable, covenant-laden debt. Merton's own paper extends to coupon and callable bonds (§VI), but the clean "default only at $T$" result is the vanilla case.

---

### 5. Canonical Literature & Study References

- **Merton, Robert C.** — *On the Pricing of Corporate Debt: The Risk Structure of Interest Rates*, *Journal of Finance* 29(2):449–470 (1974). Read §III (equity as a call, eqs. 10–11) and §IV (comparative statics, eq. 15). *The primary source for this page; formula-verified in the corpus.*
- **Bluhm, Overbeck & Wagner** — *Introduction to Credit Risk Modeling*, 2nd ed. (2010) — §1.2.3 (asset-value models: the default point and the induced bivariate asset-value distribution). *Corpus digest available.*
- **Hull** — *Options, Futures, and Other Derivatives*, Ch 24: the equity-as-call identity as an *application* of the option-pricing machinery you already know.

---

### 6. Connected Graph Bridges

- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black-Scholes-Merton]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/02-the-merton-structural-model|02 · The Merton Structural Model]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (what to do with the loss distribution this option payoff generates)

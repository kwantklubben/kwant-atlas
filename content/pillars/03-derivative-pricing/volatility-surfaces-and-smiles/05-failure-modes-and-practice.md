---
title: "3.4.5 Failure Modes & Real-World Practice"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - failure-modes
  - arbitrage
  - forward-skew
  - model-risk
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|04 · Advanced Dynamics]].

---

### 1. Intuition & Practical Objective

The surface is a *fitted* object, and fitting is where the money leaks. This page names the failures precisely, in the order a practitioner meets them:

1. **Interpolation arbitrage** - a smooth fit that is not arbitrage-free (negative densities, decreasing total variance).
2. **Forward-skew flattening** - the local-vol model matches today's vanillas but moves wrongly for path-dependent products.
3. **Model risk dominating parameter risk** - the spread *between* models is larger than the spread from mis-setting a parameter inside one model.

The objective is not cynicism; it is the discipline of knowing exactly which assumption to distrust, and measuring the residual in money terms. The recurring lesson from Gatheral ch 8–10 and Bergomi ch 2–3: **stress the modeling assumptions themselves, not just the parameters.**

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Static arbitrage conditions

A call surface $C(K,T)$ is arbitrage-free iff (Bergomi §2.2):

- **Butterfly/vertical:** $\dfrac{\partial^2C}{\partial K^2}=e^{-rT}\phi(K,T)\ge0$ - equivalently every butterfly spread has non-negative value.
- **Calendar/convex order:** for $T_1\le T_2$ and fixed moneyness $k=K/F_T$,
$$
e^{qT_1}C(kF_{T_1},T_1)\le e^{qT_2}C(kF_{T_2},T_2)\iff T_1\hat\sigma_{kT_1}^2\le T_2\hat\sigma_{kT_2}^2,
$$
  i.e. **total implied variance is non-decreasing in maturity at fixed moneyness** (Bergomi eq 2.9/2.14/2.15). Violating it is a calendar-spread free lunch.

In the $(y,T)$ coordinates used for interpolation, the conditions become simply: $f(t,y)=(t-t_0)\hat\sigma^2$ must satisfy $f_{i+1}(y)\ge f_i(y)$ (profiles must not cross), and affine interpolation in $T$ between slices preserves convex order (Bergomi eq 2.20).

#### 2.2 Local-vol dynamics failure - the arithmetic

The local-vol forward skew is (Bergomi eq 2.91/2.92)
$$
\mathcal S_\theta(\tau)=\mathcal S_{\tau+\theta}-\frac{\tau}{\theta}\!\left(\frac1\theta\int_\tau^{\tau+\theta}\mathcal S_t\,dt-\mathcal S_{\tau+\theta}\right),\qquad \mathcal S_\theta(\tau)\propto\left(\frac{\theta}{\tau}\right)^{\gamma}\mathcal S_\theta.
$$
For a *decreasing* skew term structure the bracket is **positive** (the running average exceeds the endpoint), so the leading minus makes $\mathcal S_\theta(\tau)<\mathcal S_{\tau+\theta}$: **every future skew is weaker than today's, and dies out like $(\theta/\tau)^\gamma$.** A forward-start option (cliquet) is an option on precisely this forward skew, so LV underprices it. And because LV also *cannot* lock the forward vol-of-vol (it changes with recalibration), the exotic's P&L is large and unpredictable.

The vol-of-vol mismatch is equally structural: LV implies $\mathrm{vol}(\hat\sigma_{F_TT})=\big(\mathcal S_T+\frac1T\int_0^T\mathcal S_t\,dt\big)\frac{\hat\sigma_{F_00}}{\hat\sigma_{F_TT}}\to2\mathcal S_T$ as $T\to0$ (Bergomi eq 2.83–2.85), while a *time-homogeneous* SV model has time-independent vol-of-vol - they cannot agree (Bergomi §2.5).

#### 2.3 The size of the errors (from the corpus)

- **Digitals:** dropping the skew term misprices a 1-year ATM digital by $\sim12\%$ of notional (Gatheral §8.4).
- **Cliquets:** a 5-year 6% digital cliquet can be mispriced by up to $5.76\%$ of notional (Bergomi/Gatheral ch 8/10); a locally-capped-globally-floored cliquet differed 3.53% (Heston) vs 2.55% (LV) - a 2.94% upfront gap (Gatheral §10.1), a large multiple of the provider's margin.
- **Barriers:** LV vs SV price gaps can *exceed the bid-offer* (Gatheral ch 9); a one-touch is worth two European binaries (reflection, zero log-drift) but the ratio is highly model-dependent.

---

### 3. Computational Implementation - arbitrage detection & forward-skew flattening

We (i) exhibit a butterfly arbitrage from an *invalid* SVI slice (negative Breeden–Litzenberger density) against a valid one, (ii) show a calendar-arbitrage violation numerically, and (iii) quantify the LV forward-skew flattening of §2.2. Stdlib only.




The bad slice produces a **negative risk-neutral density** ($-6.92$ at $k=-0.04$) - a butterfly free lunch that a naive spline would happily generate. The good slice's total variance is increasing ($0.0400>0.0200$); the bad one's is not, so it admits a calendar arbitrage. And the LV forward skew is **$0.586\times$ today's** - the measured flattening that underlies every forward-skew mispricing above.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Interpolation arbitrage (statics).** Unconstrained polynomials/splines fit the quotes but violate $\partial_K^2C\ge0$ or $\partial_Tw\ge0$. **Fix:** parametrize $w(k,T)$ directly with arbitrage-aware objects (SVI with calendar constraints, affine-in-$T$ profiles).
2. **LV's flat forward skew (dynamics).** Demonstrated: future skew $=0.586\times$ today's. Digitally-capped cliquets, barriers, digitals all misprice; LV sellers of forward-skew risk "win the deal and lose money" (Gatheral ch 10).
3. **Recalibration risk.** LV has no lockable forward vol-of-vol; forward skews/vol-of-vols move with each recalibration ⇒ large unpriced carry P&L when residual gammas are sizeable (Bergomi §2.6).
4. **Model risk > parameter risk.** The spread between *models* (LV vs SV vs SVJ) can be several % of notional on cliquets/barriers - far wider than the spread from getting a parameter wrong inside one model. Napoleon-style products hinge on volatility convexity that LV underprices (Gatheral §10.3). **Manage by pricing under several models, not by tuning one.**
5. **Delta convention risk.** Without a stated sticky rule, "the delta" is undefined; BS delta ≠ minimum-variance delta (Hull §20.5). Hedging with the wrong convention is a systematic bleed.
6. **Extrapolation & wing risk.** VS vols and low-strike vols are dominated by the smile *outside* the traded strikes; a wrong wing extrapolation silently reprices the whole book (Bergomi §5.2). Enforce consistency with liquid VS quotes.

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 7 §7.8 (shape is model-generic), Ch 8 (dynamics, digitals & digital cliquets, the 12%-of-notional digital error), Ch 9 (barriers & quasistatic hedging), Ch 10 (exotic cliquets: LCFG 3.53% vs 2.55%). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 2 §2.2 (no-arbitrage & convex order 2.9/2.14/2.20), §2.5–2.6 (SSR, forward skew, vol-of-vol mismatch), Ch 3 §3.1.7 (model-independent bounds). *Math-verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 20 §20.5–20.8 (minimum-variance delta, model role, single-large-jump frown).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|04 · Advanced Dynamics]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]

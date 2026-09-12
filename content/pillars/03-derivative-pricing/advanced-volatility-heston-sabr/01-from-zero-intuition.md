---
title: "3.5.1 Advanced Volatility from Zero"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - intuition
  - stochastic-volatility
  - smile
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (or none - this page is written to stand alone).

---

### 1. Intuition & Practical Objective

In Black–Scholes the volatility is a number you look up. That is not a simplification you can get away with, because the market *tells* you it is false: invert the Black–Scholes formula on every listed option and you get a surface, not a number. The only honest reading of that surface is that **the variance of the underlying is itself random**.

This page builds the *why* with no prior stochastic-volatility background. The objective is one idea: **a stochastic-volatility model fixes the smile because it makes the risk-neutral distribution a mixture - and a mixture is exactly what produces fat tails, a smile, and a skew.** Everything in the rest of this folder is a choice about *which* process drives that mixture.

Three "aha"s:

1. **Fat tails come from mixing.** If the variance $v$ were known, $\ln S_T$ would be normal. Let $v$ be random with distribution $\pi(v)$. Then the density of $\ln S_T$ is the *mixture* $\int \mathcal N(x;\,\cdot,v)\,\pi(v)\,dv$ - a scale mixture of normals. Its kurtosis exceeds $3$ whenever $\pi$ is non-degenerate. The smile is not an anomaly to be explained away; it is the *generic* consequence of random variance.

2. **The skew needs correlation, not just randomness.** A *symmetric* variance mixture produces a symmetric U-shaped **smile** (both tails fat - this is what FX options look like). Equity options show a downward **skew**: the left tail is fatter than the right. For that you need the two Brownian motions to be correlated: $\langle d\ln S,dv\rangle=\rho\eta v\,dt$ with $\rho<0$. Prices fall *because* volatility rises - the **leverage effect**. One parameter, $\rho$, turns a smile into a skew.

3. **Variance's own "volatility" is the missing knob.** Black–Scholes has one number; an SV model has a *distribution* of variance. Its dispersion, the **vol-of-vol** $\eta$, sets the *curvature* of the smile (how much the wings lift). This is why $\eta$ is the parameter that matters for exotic products: it controls convexity in vol, which is precisely what cliquets and forward-skew products pay for.

The practical objective: understand that a stochastic-volatility model is a *distributional* device, and that its parameters are not "a better volatility" - they are the shape of the variance distribution and its coupling to the spot.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Mixture of lognormals, in one line

Take $X_T=\ln(S_T/F_T)$. With random variance $v$ (independent of the Brownian motion driving $S$),

$$
p(x)=\int_0^\infty \mathcal N\!\Big(x\,;\,-\tfrac12 Tv,\;Tv\Big)\,\pi(v)\,dv,\qquad \mathcal N(x;m,s^2)=\frac{1}{s\sqrt{2\pi}}e^{-\frac{(x-m)^2}{2s^2}}.
$$

Its cumulants are the *cumulants of the variance-average*, and the third cumulant (skewness) is exactly zero unless $v$ is correlated with $S$ - the mathematical statement of aha #2. The variance-mixture route is the classic "Taylor/SV" explanation of the smile (Hull ch 20 §20.3 gives the leverage + volatility-feedback + crashophobia trio for equities).

#### 2.2 Why a single $\sigma$ cannot reproduce a mixture's prices

Black–Scholes assigns one density. The mixture assigns another. If the two disagree in the wings, **no choice of $\sigma$ can repair it**: the model has one degree of freedom and the mismatch is a *function* of $K$. Concretely, with a two-point variance mixture,

$$
C(K,T)=p\,\text{BSM}(F,K,T,\sigma_1)+(1-p)\,\text{BSM}(F,K,T,\sigma_2),
$$

which is an exact closed form (no simulation needed) - the cleanest possible demonstration. Its ATM implied vol is *below* $\sqrt{\mathbb{E}[v]}$ (Jensen: option prices are convex in vol), and its wings rise.

#### 2.3 The Heston programme, previewed

Heston replaces "distributed variance" by a concrete, tractable process:

$$
dS_t=\sqrt{v_t}\,S_t\,dZ_1,\qquad dv_t=-\lambda(v_t-\bar v)\,dt+\eta\sqrt{v_t}\,dZ_2,\qquad dZ_1dZ_2=\rho\,dt .
$$

Failure to produce a smile is *not* an option here: the variance mixture induced by the CIR process $v_t$ **is** the smile generator. The four parameters have one job each - $\bar v$ sets the level, $\lambda$ the term structure, $\eta$ the curvature, $\rho$ the skew (§02–§04). The rest of this folder is spent making that precise, computing it, and finding where it breaks.

---

### 3. Computational Implementation - a two-state mixture *is* a smile

We price a two-state variance mixture in closed form and invert the Black–Scholes formula strike-by-strike. No simulation, no free parameters to fit: the smile appears because the density is a mixture. Stdlib only.




Three facts to read off the table:

1. **The implied vol is not constant.** It runs $24.97\%$ at $K{=}70$ down to $19.98\%$ ATM and back up to $23.60\%$ at $K{=}130$ - a **smile**, produced by nothing but the randomness of the variance.
2. **ATM implied vol $\ne\sqrt{\mathbb E[v]}$.** $19.98\%$ against $22.36\%$. Option prices are convex in $\sigma$; mixing two pure-volatility worlds and then quoting the price back in *one* volatility systematically under-states the dispersion. This gap is the reason variance swaps and ATMF implied vols are *different market parameters*.
3. **The mixture is symmetric** - *both* wings lift. To tilt it down (equity skew) you must **correlate** the variance with the spot return. That single observation is why every equity SV model carries a $\rho\in[-1,0)$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"A mixture is a model."** A two-point mixture reproduces a smile but has **no dynamics**: it says nothing about how the variance moves, so it cannot price a forward-start option, a cliquet, or a variance swap. Statics ≠ dynamics - the recurring theme of this folder ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]]).
2. **Confusing implied vol with expected vol.** As the table shows, $\sigma_{BS}^{ATM}=19.98\%$ while $\sqrt{\mathbb E[v]}=22.36\%$. Convexity (Jensen) means implied variance is *not* the expected variance, and the two series (implied ATMF vs variance-swap) are distinct market quotes (Bergomi ch 5).
3. **Forgetting that the risk-neutral mixture is not the real-world one.** Everything above lives under $\mathbb Q$. The market's $\pi^{\mathbb Q}(v)$ carries a **variance risk premium** and is not the histogram of realized variance. Calibrating dynamics to historical time series is a category error (Hull ch 23 is about $\mathbb P$, not $\mathbb Q$).
4. **Assuming more parameters ⇒ better.** The smile's *shape* is nearly model-generic (Gatheral §7.8): once a model has fat tails via a variance mixture and a negative $\rho$, it will fit today's slice. What differs is the *dynamics*, which today's slice cannot see. Fitting harder is not the answer; testing dynamics is.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 20 §20.3–20.8 (why smiles exist: leverage, volatility feedback, crashophobia; FX smile vs equity skew; surface as an interpolation tool; single-large-jump "frown") and Ch 23 §23.1–23.6 (EWMA/GARCH volatility term structure eq. 23.14 - the $\mathbb P$-measure cousin of the SV term structure). *Verification report in the corpus.*
- **Gatheral**, *The Volatility Surface*, Ch 1 (empirical motivation: volatility clustering, fat tails, and the SDEs 1.1–1.2 that follow), Ch 7 §7.8 (shape is model-generic). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 1 (what a "usable" model is; the Black–Scholes equation as an accounting device) and Ch 5 Appendix B (the Gram–Charlier/$\kappa_3$ perturbation that makes the mixed-density intuition precise). *Math-verified.*
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1.1–1.9 (generalized BSM, put–call parity, symmetries) and §2.9 (vega - the map that makes vol-inversion well posed). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · 03 Pricing Formulas]]
- Continue: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/01-from-zero-intuition|VS · 01 From Zero]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR (flat note)]]

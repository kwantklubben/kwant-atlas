---
title: "3.7.4 Compound, Chooser, Quanto, Exchange & Spread Options"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - compound-options
  - chooser
  - quanto
  - margrabe
  - spread-options
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]].

---

### 1. Intuition & Practical Objective

These exotics extend BSM along two new axes:

- **Time** - **compound** (option on an option) and **chooser** (call-or-put later) add a *decision date* $t_1$ before the underlying's expiry.
- **A second asset / currency** - **exchange (Margrabe)**, **spread (Kirk)**, **quanto** and **foreign-equity** options trade one asset against another or translate across currencies.

The practical objective: the **bivariate normal CDF $M(a,b;\rho)$** is the new mathematical primitive (chooser/compound are four-term combinations; two-asset options carry the correlation $\rho$ explicitly). Every closed form here is "BSM in one or two dimensions, with a critical price level $I$ (or a correlation-adjusted volatility) solved for." Verified anchors: compound put-on-call $=21.1964$, simple chooser $=6.1071$, complex chooser $=6.0507$, Margrabe $=1.5260$, quanto $=5.3280$, foreign-equity $=8.3056$, Kirk spread $=2.1670$, complex chooser $I=51.1158,\ w=6.0508$ (Haug 4.27).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The bivariate normal primitive

$$
M(a,b;\rho)=\mathbb{P}(X\le a,\,Y\le b),\qquad (X,Y)\sim N\!\Big(0,\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}\Big)=\int_{-\infty}^{a}\varphi(x)\,N\!\Big(\frac{b-\rho x}{\sqrt{1-\rho^2}}\Big)\,dx.
$$

This one-dimensional integral form is exactly how it is computed here (adaptive Simpson) - no external library needed. Haug recommends the Genz algorithm for production accuracy (§13.3.1); the integral form reproduces all anchors to 3–4 dp.

#### 2.2 Compound options (Haug §4.13) - a call on a call/put

For a **put-on-call** (eq 4.29, verified): the critical level $I$ solves $c_{BSM}(I,X_1,T_2-t_1)=X_2$ (the spot at which the underlying call is worth the compound strike $X_2$), and

$$
p_{call}=X_1 e^{-rT_2}M(z_2,-y_2;-\rho)-S e^{(b-r)T_2}M(z_1,-y_1;-\rho)+X_2 e^{-r t_1}N(-y_2),
$$

with $z_1,z_2$ (function of $X_1$, $T_2$), $y_1,y_2$ (function of $I$, $t_1$), $\rho=\sqrt{t_1/T_2}$. Compound-option **put–call parity** (Haug eqs 4.32–4.33): $c_{call}+X_2 e^{-r t_1}=p_{call}+c_{BSM}(S,X_1,T_2)$.

#### 2.3 Choosers (Haug §4.12)

**Simple chooser** - at $t_1$ you pick a call *or* put (both strike $X$, expiry $T_2$). Cleanest verified form is the **decomposition** (the literal transcription's last-term exponent is ambiguous in the source; the decomposition reproduces the book's $6.1071$):

$$
\text{chooser}=c(S,X,T_2)+e^{(b-r)(T_2-t_1)}\,p\big(S,\;X e^{-b(T_2-t_1)},\;t_1\big).
$$

**Complex chooser** - at $t_1$ you choose between a call $(X_c,T_c)$ and a put $(X_p,T_p)$; four bivariate-normal terms with correlations $\rho_1=\sqrt{t_1/T_c}$, $\rho_2=\sqrt{t_1/T_p}$, and a critical level $I$ solving $c_{BSM}(I,X_c,T_c-t_1)=p_{BSM}(I,X_p,T_p-t_1)$.

#### 2.4 Exchange (Margrabe, Haug §5.7) and spread (Kirk §5.8)

**Margrabe** - the option to exchange asset 2 for asset 1: $C=Q_1S_1e^{(b_1-r)T}N(d_1)-Q_2S_2e^{(b_2-r)T}N(d_2)$ with the *net* volatility $\sigma=\sqrt{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}$ and $d_1=[\ln(Q_1S_1/Q_2S_2)+(b_1-b_2+\tfrac12\sigma^2)T]/(\sigma\sqrt T)$. Note: **no $X$** - the exchange option needs only two assets and the correlation. This is why a quanto / spread reduces to it.

**Kirk spread** - payoff $(S_1-S_2-X)^+$ approximated by treating $S_2e^{(b_2-r)T}+Xe^{-rT}$ as a single "asset" with weight $F=S_2e^{(b_2-r)T}/(S_2e^{(b_2-r)T}+Xe^{-rT})$ and vol $\sigma=\sqrt{\sigma_1^2+(F\sigma_2)^2-2\rho\sigma_1F\sigma_2}$.

#### 2.5 Quanto & foreign-equity (Haug §5.16)

**Quanto** (fixed-rate foreign equity, Derman–Karasinski–Wecker / Reiner): payoff in domestic currency of a foreign asset, struck at a fixed exchange rate $E_p$:

$$
c=E_p\Big[S^*\,e^{(r_f-r-q-\rho\sigma_S\sigma_E)T}N(d_1)-X^*\,e^{-rT}N(d_2)\Big],\qquad d_1=\frac{\ln(S^*/X^*)+(r_f-q-\rho\sigma_S\sigma_E+\tfrac12\sigma_S^2)T}{\sigma_S\sqrt T}.
$$

The term $-\rho\sigma_S\sigma_E$ is the **quanto adjustment** - it shifts the foreign drift by the covariance of the asset with the FX rate. **Foreign equity struck in domestic currency** (Reiner) instead uses the *combined* vol $\sigma_{ES}=\sqrt{\sigma_S^2+\sigma_E^2+2\rho\sigma_E\sigma_S}$ with $d_1=[\ln(ES^*/X)+(r-q+\tfrac12\sigma_{ES}^2)T]/(\sigma_{ES}\sqrt T)$ and $c=ES^*e^{-qT}N(d_1)-Xe^{-rT}N(d_2)$.

---

### 3. Computational Implementation - the bivariate engine

Stdlib only. $M(a,b;\rho)$ via the one-dimensional integral form; compound/chooser/Margrabe/quanto all reproduced.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Correlation is the hidden input.** Margrabe, quanto and spread all carry $\rho$; the closed forms *look* like BSM but the effective volatility is correlation-dependent ($\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2$). A wrong $\rho$ misprices the whole contract - and correlations are notoriously unstable (see [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]).
2. **Quanto adjustment sign.** The drift shift is $-\rho\sigma_S\sigma_E$ in the quanto (domestic payoff at fixed FX); confuse it with the foreign-equity case ($+\rho$ in the combined vol) and you flip the sign of the entire covariance correction.
3. **Critical-level root finding.** Compound and complex choosers need $I$ solved from a BSM equality; a sloppy root finder (or using the wrong side of the equation) invalidates every bivariate term. The $I$ here is verified ($538.3165$, $51.1158$) - but re-solve it, don't hardcode.
4. **$M(a,b;\rho)$ is the real cost.** These closed forms hide a bivariate-normal evaluation; a naive/incorrect bivariate routine silently corrupts all four terms. Use the integral form or Genz, and validate against a known anchor before production.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.12 (choosers, eqs 4.26–4.27), §4.13 (compound, eqs 4.28–4.34), Ch 5 (Margrabe 5.7, Kirk 5.17–5.18, quanto 5.35–5.42), §13.3 (bivariate normal primitives).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 26 (compound §26.7, chooser, Margrabe §26.14, quanto).
- **Shreve**, *Stochastic Calculus for Finance II*, §5.6 (change of numeraire - the rigorous basis of quanto adjustments, via the covariance term in the drift).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §1.2 (change of numeraire; Margrabe as the worked example).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/03-lookbacks-and-asians|03 · Lookbacks & Asians]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (the correlation/vol input)

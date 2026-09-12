---
title: "3.5.4 Stochastic-Vol Dynamics"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - vol-of-vol
  - bergomi-guyon
  - skew-stickiness
  - forward-variance
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]] and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03 · SABR & Asymptotics]].

---

### 1. Intuition & Practical Objective

Here is the uncomfortable theorem of this whole pillar (Gatheral §7.8): **all stochastic-volatility-with-jumps models generate essentially the same surface shape.** Any of them, with appropriate parameters, will fit today's vanilla smile. So the static fit cannot select a model; it is a *constraint*, not a *test*. This page is about what actually does select one: the **dynamics**.

Two questions, answerable by two different objects:

| question | object | what it measures |
|---|---|---|
| **Statics** - what is today's shape? | skew level $\partial_k\sigma^2_{BS}\big|_0=\frac{\rho\eta}{2}\beta(v_0)$ (+ jumps) | the spot/vol covariance, *model-independently* |
| **Dynamics** - how does the surface move? | **skew stickiness ratio** $R_T$ and the **vol-of-vol term structure** $\nu_T(t)$ | how implied vol co-moves with spot, and how vol-of-vol decays with maturity |

Everything in this folder that a *practitioner* cares about lives in the second row. Three concrete claims drive the page:

1. **Heston is structurally Type I.** Its ATMF skew decays as $1/T$ and its skew stickiness ratio tends to $1$. Equivalently, its skew is hard-wired inversely proportional to the vol level, $\mathcal S_T\propto1/\hat\sigma_{F_TT}$ - which reality does not show (Bergomi §6). Real markets are Type II with $\mathcal S_T\propto T^{-1/2}$.
2. **Heston's vol-of-vol term structure is a fixed one-time-scale shape**, $\propto(1-e^{-k(T-t)})/(k(T-t))$, which cannot match the empirical power law $\nu_T\propto T^{-0.4}$ over a wide maturity range. Forward-variance (Bergomi) models with a couple of OU factors can - that is their entire reason for existing.
3. **The Bergomi–Guyon expansion makes the smile *computable* in terms of three dimensionless numbers.** To second order in vol-of-vol, *any* SV model's smile is $\hat\sigma(K,T)=\hat\sigma_{F_TT}+S_Tk+\frac{C_T}{2}k^2$, with the coefficients given by $C^{x\xi},C^{\xi\xi},D$ - integrals of the spot/vol and vol/vol covariance functions. Same recipe, any model.

The practical objective: know that vanilla smiles barely constrain the exotic book, know which dynamic quantity to measure to discriminate, and know the two settings (vol-of-vol *level* and *term structure*) that decide the price of forward-skew products.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Heston as a one-factor forward-variance model (Bergomi ch 6)

Bergomi rewrites Heston in terms of the **variance curve** $\xi_t^T=\mathbb E_t[v_T]$:

$$
\xi_t^T=\bar v+e^{-\lambda(T-t)}(v_t-\bar v),\qquad \hat\sigma_T^2(t)=\bar v+\frac{1-e^{-\lambda(T-t)}}{\lambda(T-t)}(v_t-\bar v),
$$

and as a forward-variance SDE $d\xi_t^T=\eta e^{-\lambda(T-t)}\sqrt{\xi_t^t}\,dZ_t$ - **driftless**, which is why variance-swap implied vols stay fixed under perturbations. The price of this elegance is a hard constraint on the initial curve,

$$
\frac{d\xi_0^T}{dT}=-\lambda(\xi_0^T-\bar v)\qquad(\text{6.2}),
$$

so **Heston cannot fit a general variance-swap term structure and an ATM term structure simultaneously** - the curve has one free parameter ($\bar v$) and one exponent ($\lambda$). Its vol-of-vol term structure for a flat VS curve is fixed (6.9):

$$
\mathrm{vol}(\hat\sigma_T)\propto\frac{1-e^{-\lambda(T-t)}}{\lambda(T-t)}\ \text{(short }T: \to1;\ \text{long }T:\propto1/(T-t)).
$$

Heston's **ATMF skew** at order one in $\eta$ (6.17b, flat curve 6.20):

$$
\mathcal S_T=\frac{1}{\hat\sigma_T^3T^2}\frac{\rho\eta}{2}\int_0^T V_\tau\,\frac{1-e^{-\lambda(T-\tau)}}{\lambda}d\tau\ \ \xrightarrow{\ \text{flat}\ }\ \ \frac{\rho\eta}{2\sqrt{\bar v}}\frac{\lambda T+e^{-\lambda T}-1}{(\lambda T)^2},
$$

with the two exact limits

$$
\mathcal S_T\to\frac{\rho\eta}{4\sqrt{\bar v}}\ (T\to0)\qquad\text{and}\qquad\mathcal S_T\to\frac{\rho\eta}{2\sqrt{\bar v}}\frac{1}{\lambda T}\ (T\to\infty).
$$

The $1/T$ long-maturity decay is Heston's signature - and the reason it is a **Type I** model.

#### 2.2 Skew stickiness and the Type I / Type II classification (Bergomi ch 9)

The skew stickiness ratio measures the co-movement of implied vol with spot, normalised by the skew,

$$
R_T=\frac{1}{\mathcal S_T}\frac{\mathbb E\big[d\ln S\;d\hat\sigma_{F_T(S)T}\big]}{\mathbb E\big[(d\ln S)^2\big]}
$$

($R_T=1$ sticky-strike, $R_T=0$ sticky-delta). At lowest non-trivial order, for a time-homogeneous model with covariance kernel $\mu$ on a flat curve,

$$
R_T=\frac{\int_0^T\mu(t)dt}{\int_0^T(1-t/T)\mu(t)dt}.
$$

For monotone-decaying $\mu$ this yields the **model-independent range**

$$
\boxed{\;R_T\in[1,2]\;}\qquad\text{with}\qquad R_0=2\ \text{(the same short-end limit as local volatility).}
$$

Classifying models by the decay exponent $\mu(t)\propto t^{-\gamma}$:

$$
\text{Type I }(\gamma>1):\ \mathcal S_T\propto\frac1T,\ R_\infty=1;\qquad \text{Type II }(\gamma<1):\ \mathcal S_T\propto T^{-\gamma},\ R_\infty=2-\gamma;\qquad \mathcal S_T\propto T^{-(2-R_\infty)} .
$$

Heston ($\mu$ exponential) is **Type I**, $R_T\to1$; local volatility gives $R_T\to(2-\gamma)/(1-\gamma)$ (e.g. $3$ for $\gamma=\tfrac12$) - i.e. LV and SV start at the same $R_0=2$ and go in **opposite directions**. The data say Type II ($\gamma\approx\tfrac12$, $R_\infty\approx1.5$), so **neither** pure LV nor Heston is right, and the two-factor model is built to be Type II over a practical range:

$$
\mathcal S_T=\frac{\omega}{2}\sum_iw_i\rho_{iS}\frac{k_iT-1+e^{-k_iT}}{(k_iT)^2},\qquad R_T=\frac{\sum_iw_i\rho_{iS}(1-e^{-k_iT})/(k_iT)}{\sum_iw_i\rho_{iS}(k_iT-(1-e^{-k_iT}))/(k_iT)^2}\ \text{(9.16a,b)}.
$$

**Pricing consequence (Bergomi §9):** for a long spot/vol cross-gamma book, *local volatility* is the conservative (higher-$R$) choice; for a short cross-gamma book, *SV* is. Same smile, opposite prices - that is the whole point of this chapter.

#### 2.3 The Bergomi–Guyon expansion (Bergomi ch 8)

Write the pricing equation as $\partial_tP+H_tP=0$ with $H_t=H_t^0+\varepsilon W_t^1+\varepsilon^2W_t^2$, where $\varepsilon$ scales the vol-of-vol ($\mu\to\varepsilon\mu$, $\nu\to\varepsilon^2\nu$, then $\varepsilon=1$). Because forward variances are **driftless**, VS implied vols are *unchanged* by $\varepsilon$ - so the expansion perturbs the smile without shifting the level. The price expansion is (8.18)

$$
P=\Big[1+\varepsilon\frac{C_0^{x\xi}}{2}(\partial_x^3-\partial_x^2)+\varepsilon^2\Big(\frac{C_0^{\xi\xi}}{8}(\partial_x^2-\partial_x)^2+\frac{(C_0^{x\xi})^2}{8}(\partial_x^3-\partial_x)^2+\frac{D_0}{2}(\partial_x^3-\partial_x)^2\Big)\Big]P_0,
$$

with the **three dimensionless model-dependent constants**

$$
C_t^{x\xi}=\!\int_t^T\!\!d\tau\!\int_\tau^T\!\!du\,\mu(\tau,u)=\!\int_t^T\!(T-\tau)\big\langle d\ln S_\tau\,d\hat\sigma_T^2(\tau)\big\rangle,
$$

$$
C_t^{\xi\xi}=\!\int_t^T\!\!d\tau\!\int_\tau^T\!\!du\!\int_\tau^T\!\!du'\,\nu(\tau,u,u')=\!\int_t^T\!(T-\tau)^2\big\langle d\hat\sigma_T^2(\tau)\,d\hat\sigma_T^2(\tau)\big\rangle,
$$

$$
D_t=\!\int_t^T\!\!d\tau\!\int_\tau^T\!\!du\,\mu(\tau,u)\frac{\delta C_\tau^{x\xi}}{\delta\xi^u},
$$

so the whole smile at order 2 is a function of $(C^{x\xi},C^{\xi\xi},D)$ - the *skew* functional, the *vol-of-vol* functional, and the *term-structure* functional. The implied-vol expansion (8.20–8.21) is

$$
\hat\sigma(K,T)=\hat\sigma_{F_TT}+S_T\ln(K/F_T)+\frac{C_T}{2}\ln^2(K/F_T)+O(\varepsilon^3),
$$

$$
S_T=\hat\sigma_T\frac{\varepsilon\,C^{x\xi}}{2Q^2}\Big\{1+O(\varepsilon)\Big\},\qquad Q=\hat\sigma_T^2T,\qquad \hat\sigma_{F_TT}=\hat\sigma_T+\frac{Q}{2}S_T .
$$

**The order-1 skew is *exactly* the local-volatility formula (2.89).** With $\mu$ the instantaneous spot/VS-vol covariance,

$$
S_T=\frac{1}{2\hat\sigma_T^3T}\int_0^T\frac{T-\tau}{T}\big\langle d\ln S_\tau\,d\hat\sigma_T^2(\tau)\big\rangle_0d\tau,
$$

i.e. **the ATMF skew is the (weighted) average of the instantaneous spot/vol covariance over the residual maturity** - a statement first derived for local volatility and now shown to be *model-independent at order 1*. That is the cleanest form of the "skew is the covariance of spot with implied vol" mantra.

Short-maturity limit ($T\to0$, order 2, $\mu_0\equiv\mu(0,0,\xi_0^0)$, $\nu_0\equiv\nu(0,0,0,\xi_0^0)$):

$$
C^{x\xi}=\frac{T^2\mu_0}{2},\quad C^{\xi\xi}=\frac{T^3\nu_0}{3},\quad D=\frac{T^3\mu_0\,d\mu_0/d\xi_0^0}{6},\qquad S_0=\frac{\mu_0}{4(\xi_0^0)^{3/2}},\quad S_0=\frac{1}{2\hat\sigma_0^2}\frac{\langle d\ln S\,d\hat\sigma_0\rangle}{dt},
$$

which reproduces (8.39)–(8.44): SABR $S_0=\rho\nu/2$, Heston $S_0=\rho\eta/(4\sqrt{V_0})$, vanishing correlation $S_0=0$ (all verified in [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03 · SABR & Asymptotics]]).

**Order-2 consequences worth remembering:** at order 2 the skew is *exactly quadratic in log-moneyness* (hence "curvature" is meaningful only there); the truncated density can go negative at extreme strikes (use only near the money); and the triple $(C^{x\xi},C^{\xi\xi},D)$ is **not enough to pin the dynamics** - the SSR needs $\mu$ itself.

#### 2.4 The gamma representation, and what the skew *hedges*

With $\omega_t=\hat\sigma_T^2(t)$ and $Q=e^{-rt}P_{BS}$,

$$
P=P_{BS}(0,S_0,\hat\sigma_T^2(0))+\mathbb E\Big[\int_0^Te^{-rt}\Big(\frac{\partial^2P_{BS}}{\partial S\partial\hat\sigma_T^2}dS_t\,d\hat\sigma_T^2(t)+\frac12\frac{\partial^2P_{BS}}{\partial(\hat\sigma_T^2)^2}d\hat\sigma_T^2(t)d\hat\sigma_T^2(t)\Big)\Big],
$$

whose order-1 truncation shows the **materialising payoff for the spot/vol cross-gamma is $\ln^2(S_T/S_0)$** - a log-contract-like position with (signed) replication density $\rho(K)=\frac{2}{K}(1-\ln(K/S_0))$ (positive for $K\ll S_0$). This makes the implied integrated spot/vol covariance a **model-free read-off** from the market price of $\ln^2$, and it is the theoretical basis of the synthetic-skew trade (Bergomi §9.10: cross-gamma/theta P&L $=S\hat\sigma_0^2\frac{d^2\Pi}{dSd\hat\sigma_0}(R_T^{r,\text{short}}-2)\delta t$).

#### 2.5 Forward-variance models: the fix (Bergomi ch 7)

Model $(S_t,\{\xi_t^T\})$ directly, with the pricing equation (7.4)

$$
\frac{\partial P}{\partial t}+(r-q)S\frac{\partial P}{\partial S}+\frac{\xi_t^t}{2}S^2\frac{\partial^2P}{\partial S^2}+\frac12\iint\nu\,\frac{\delta^2P}{\delta\xi^u\delta\xi^{u'}}+\int\mu\,S\frac{\delta^2P}{\partial S\,\delta\xi^u}=rP,
$$

subject to the **cardinal rule** that the break-even spot vol equals the instantaneous VS vol, $\sigma(t,S,\xi)^2=\xi_t^t$ (no free theta). A **Markov representation** exists if and only if $\omega(u)=\omega e^{-ku}$, i.e. forward variances are driven by OU processes:

$$
\xi_t^T=\xi_0^T\exp\Big(\omega e^{-k(T-t)}X_t-\frac{\omega^2}{2}e^{-2k(T-t)}\mathbb E[X_t^2]\Big),\qquad dX_t=-kX_tdt+dW_t,
$$

which is **exactly simulable**. The two-factor workhorse (7.28–7.39) generalises this with two well-separated time scales and gives the vol-of-vol term structure

$$
\nu_T(t)=\nu\alpha_\theta\sqrt{\textstyle\sum_{ij}w_iw_j\rho_{ij}I(k_i(T-t))I(k_j(T-t))},\qquad I(x)=\frac{1-e^{-x}}{x},
$$

against the empirical **power-law benchmark** (7.40)

$$
\nu_T(t)=\sigma_0\Big(\frac{\tau_0}{T-t}\Big)^{\alpha},\qquad \alpha\approx0.4,\ \tau_0=3\text{m}.
$$

This is the desk-grade answer to LV's missing forward skew: a model that fits the VS term structure *by construction* and controls the vol-of-vol term structure with one or two extra factors. Note also the structural difference from Heston: $\xi_t^T$ is **lognormal** (so short vol is lognormal, not normal - the empirically preferred $\beta(v)\sim\sqrt v$ scaling).

---

### 3. Computational Implementation - Heston's forward-variance facts, the skew limits, and the vol-of-vol term structure

We (i) verify Heston's VS-vol curve (6.4) and its short-maturity limit, (ii) verify the ATMF skew formula (6.20) against **both** of its exact limits, (iii) confirm the short-dated variance skew $\rho\eta/2$ *from the characteristic-function pricer* (an independent route to §03's asymptotics), and (iv) compare the vol-of-vol term structures of Heston (6.9), the two-factor model (7.39) and the empirical power law (7.40). Stdlib only.




**What the output establishes.**

- **The Heston forward-variance curve and its limit.** $\hat\sigma_T$ runs $13.410\%\to18.634\%$ as $T$ goes $0.05\to20$ yr, and the short-maturity limit is exactly $\sqrt{v_0}=13.1909\%$. Note $\hat\sigma_T$ **converges to $\sqrt{\bar v}$** for large $T$ - Heston's forward-variance curve is a one-parameter exponential, which is why it cannot fit a rich VS term structure.
- **The ATMF skew formula (6.20) is right, in both limits.** At $T{=}0.01$ the formula gives $-0.367480$ against its exact short-maturity limit $-0.369105$ ($0.4\%$ off, and the gap shrinks as $T\to0$); at $T{=}50$ it gives $-0.010972$ against the $1/T$ limit $-0.011140$ ($1.5\%$ off, again shrinking). Both asymptotics are reproduced.
- **The short-dated variance skew is $-\rho\eta/2$ to three digits from a completely independent route.** The characteristic-function pricer - no asymptotics anywhere - gives $-0.138331$/$-0.138404$ at $T{=}0.005$–$0.01$ versus the analytic $-\rho\eta/2=-0.138894$. (At $T{=}0.002$ with $h=2\times10^{-4}$ the finite-difference window is no longer small compared with $\sigma_{BS}\sqrt T$, so the value drifts to $-0.120$ - a *discretisation* artefact of the test, not of the model.) This is the strongest single validation in the folder: the Gatheral (7.3) asymptote, the Bergomi (6.18b) limit and the exact Fourier price all agree.
- **The vol-of-vol term structure test - Heston fails, the two-factor model passes.** Normalising all three shapes at $T{=}0.25$: the two-factor model tracks the empirical power law within about $8\%$ over $0.1$–$5$ years ($0.916$–$1.000$), while Heston is $24\%$ low at 3 months ($0.763$), $13\%$ high at 1–2 years, and $41\%$ low at 5 years ($0.587$). Since $\nu_T(t)$ sets the price of anything depending on future vol-of-vol (VS options, forward-vol products), this is a *pricing* failure, not a cosmetic one.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Selecting a model by its static fit.** Vanilla smiles barely constrain forward-skew-dependent products: Bergomi's model-independent bounds leave a 95/105 forward call spread anywhere in $[1.6\%,7.7\%]$ from a flat 20% smile, narrowing only when *congruent* payoffs are added (Bergomi §3.1.7). Fitting today's surface is not model validation.
2. **Ignoring the direction of the SSR.** LV and SV have the *same* $R_0=2$ and then diverge (LV up to $\approx3$, SV down into $[1,2]$). A trader on the wrong side of $R_T$ has the wrong sign for the cross-gamma/theta P&L - the realised-SSR backtest (Euro Stoxx 50, 2007–2012) found $\approx1.6$ realised against an implied $2$, a real materialisable P&L (Bergomi §9.10).
3. **Market SSR can go negative, and it is not a model failure.** Realised SSR was sharply negative in the Nikkei in 2012, traced to dealer autocall-vega hedging (Bergomi §9.11). Diagnosing this as a calibration error and "fixing" the model makes things worse.
4. **Treating vol-of-vol as a single number.** $\nu_T(t)$ is a *term structure*; Heston hard-wires it (6.9) and the mismatch is $2\times$ at 3 months and $1.7\times$ at 5 years against the benchmark. Any product whose vega is concentrated in the vol-of-vol (VS swaptions, forward-vol claims) is mispriced outright.
5. **Using the order-2 expansion where it is not valid.** The truncated density can go negative at extreme strikes; the implied variance is at most affine in $|k|$ (Lee). The Bergomi–Guyon expansion is a *near-the-money* tool. Exponential resummation (ch 8 App. C) improves tails but does not make it global.
6. **Forgetting that vol-of-vol is what the vol-of-vol *risk premium* prices.** $\nu_T$ calibrated to vanillas is a $\mathbb Q$ quantity incorporating a premium; using it as a forecast of realized vol-of-vol confuses measures (Bergomi ch 5).
7. **Believing the two-factor model is "the" model.** The two-factor fit to the benchmark (7.40) above is good but not exact; extra factors buy flexibility at the cost of unidentifiable parameters - and the *variance curve* ($\xi_0^T$) must be treated as an input from the VS market, not as a calibration output.

---

### 5. Canonical Literature & Study References

- **Bergomi**, *Stochastic Volatility Modeling* - **Ch 6** (Heston in the forward-variance framework: 6.1–6.5, drift of $V_t$ as the short-end curve slope, 6.6–6.9 vol-of-vol, 6.16–6.20 skew and its limits, and the four structural criticisms), **Ch 7** (forward-variance models: pricing equation 7.4, break-even covariances 7.2, Markov representation 7.9–7.10 and 7.13, $N$-factor 7.11–7.27, two-factor 7.28–7.39, benchmark 7.40, VIX/realized-variance §7.6–7.7), **Ch 8** (**Bergomi–Guyon**: 8.3–8.12 the expansion machinery, 8.13–8.17 the three constants, 8.18 the price expansion, 8.20–8.21 implied vols, 8.22–8.26 the order-1 skew and the LV identity, 8.29–8.33 gamma representation and $\ln^2$ payoff, 8.35–8.44 short-maturity limits and the SABR/Heston specialisations), **Ch 9** (SSR: 9.1–9.9 definitions and $R_T\in[1,2]$, 9.11–9.16 Type I/II and the two-factor forms, 9.22–9.31 realised SSR and the skew trade), **Ch 10** (what causes equity smiles: Student-$t$ one-day distribution, the $1/T$ contribution of the one-day smile, jumps as a stress-reserve policy). *The primary modern treatment, math-verified in the corpus.*
- **Gatheral**, *The Volatility Surface*, Ch 3 (gamma-weighted implied variance 3.1–3.11, Heston local variance 3.15, ATM term structure 3.18) and Ch 8 (skew level-independence §8.1, LV forward skew §8.2, stochastic implied vol §8.3, digitals and cliquets §8.4). *Math-verified.*
- **Bergomi & Guyon** (2012), *Stochastic volatility's orderly smiles*, Risk 25(5) - the published form of ch 8; **Durrleman** (2005) on extracting variance dynamics from the implied-vol surface; **Lewis** (2000) on the small-vol-of-vol expansion that proves (7.11) exact to $O(\eta)$.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 20 (smile dynamics, volatility term structure, minimum-variance delta $\Delta_{MV}=\Delta_{BSM}+\mathcal V_{BSM}\partial\mathbb E[\sigma_{imp}]/\partial S$ - the practical face of the SSR) and Ch 23 (GARCH variance term structure eq. 23.14, the $\mathbb P$-measure analogue of $\xi_0^T$). *Verification report in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03 · SABR & Asymptotics]]
- Forward: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|VS · 04 Advanced Dynamics]] (SSR and the LV/Heston skew, from the surface side) · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] (cross-gamma/theta) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (estimating $\nu_T$ and the SSR from data)

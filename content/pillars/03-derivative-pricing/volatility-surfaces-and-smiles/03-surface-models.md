---
title: "3.4.3 Surface Models"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - svi
  - variance-swap
  - sticky-rules
  - arbitrage-free
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|02 · Implied vs Local Vol]].

---

### 1. Intuition & Practical Objective

You now know the surface is the market's price object and that it uniquely pins a local-vol diffusion. The next practical problem is **representation**: how do you store, interpolate, extrapolate and *risk-manage* a surface without introducing arbitrage, and how do you extract the tradable quantities - the **forward variances** and **variance-swap vol** - that live inside it?

Three building blocks:

1. **A parametric, arbitrage-free slice: SVI.** Gatheral's "stochastic-volatility-inspired" parametrization fits a whole maturity slice with five numbers and is built to avoid butterfly/calendar arbitrage (Gatheral eq 3.20).
2. **Sticky rules.** When the spot moves, *what stays fixed* - the fixed-strike vols (sticky-strike) or the smile translated with the spot (sticky-delta)? This single assumption changes every delta you hedge with (Bergomi §2.5; Hull §20.5 minimum-variance delta).
3. **Forward variance / variance swaps.** The tradable object that makes the surface's dynamics concrete: a variance swap's fair vol is almost exactly the log-contract implied vol, computable as a *weighted integral of the smile* (Bergomi ch 5; Gatheral §4.21/5.17).

> **One-line essence.** "A surface model is a set of parameters + arbitrage bounds + a rule for how the surface moves; SVI supplies the parameters and bounds, the sticky rules supply the motion, and forward variance supplies the hedging instrument."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 SVI (Gatheral 2004, eq 3.20)

For a single maturity, with $k=\ln(K/F)$ log-strike,
$$
\boxed{\;w(k)=\sigma_{BS}^2(k)\,T=a+b\!\left[\rho\,(k-m)+\sqrt{(k-m)^2+s^2}\right]\;}
$$
with parameters $a,b,\rho,s,m$ ($b\ge0$, $|\rho|<1$, $s>0$). As $|k|\to\infty$ the slice is asymptotically linear in $|k|$ with slopes $b(1\pm\rho)$ - matching **Roger Lee's** regularity bound (implied variance grows at most linearly in $|k|$, with the gradients tied to the maximal finite moments of $S_T$; Gatheral §7.7, model-independent). The **ATM variance skew** is
$$
\left.\frac{\partial w}{\partial k}\right|_{k=0}=b\!\left(\rho+\frac{-m}{\sqrt{m^2+s^2}}\right)\xrightarrow[m=0]{}b\rho.
$$
The ATM **level** is $w(0)=a+b(\rho(-m)+\sqrt{m^2+s^2})$.

#### 2.2 Sticky rules and the minimum-variance delta

Two benchmark behaviors of the surface as $S$ moves:

- **Sticky-strike:** $\partial\sigma_{BS}/\partial S=0$ - each fixed strike keeps its vol; the ATM point slides *along* the smile. Delta = BS delta.
- **Sticky-delta (sticky-moneyness):** $\sigma_{BS}=f(\ln(K/S))$ - the smile translates with the spot; each fixed log-moneyness keeps its vol.

The **skew stickiness ratio** $R_T$ interpolates them,
$$
R_T=\frac{1}{\mathcal S_T}\frac{d\hat\sigma_{F_TT}}{d\ln S_0},\qquad R_T=1:\ \text{sticky-strike},\quad R_T=0:\ \text{sticky-delta}
$$
(Bergomi eq 2.61–2.62). The practical consequence is Hull's **minimum-variance delta**: because vol moves with the spot,
$$
\Delta_{MV}=\Delta_{BSM}+V_{BSM}\,\frac{\partial\,\mathbb{E}[\sigma_{imp}]}{\partial S}<\Delta_{BSM},
$$
i.e. the naive BS delta *over-hedges* a short option position when the skew is downward-sloping (Hull §20.5).

#### 2.3 Term structure and total variance (calendar no-arbitrage)

The surface's maturity axis obeys the **convex-order condition** - total implied variance must increase with maturity at fixed moneyness (Bergomi eq 2.14/2.15):
$$
T_1\le T_2\ \Longrightarrow\ T_1\hat\sigma^2(k,T_1)\le T_2\hat\sigma^2(k,T_2)\quad\text{for all fixed }k.
$$
Equivalently, in $(y,T)$ coordinates the *total-variance profiles must not cross*. Slices are interpolated in $T$ by a monotone spline on $w$ (Gatheral uses Stineman monotonic).

#### 2.4 Variance swaps, log contracts and forward variance

A variance swap pays realized variance; its fair strike is replicated by a **log contract** $f(S)=-2\ln S$. The weight $\rho(K)\propto1/K^2$ is exactly the density whose vega is spot-independent ($\rho(K)K\phi(S/K)$ constant; Bergomi eq 3.5). In any *diffusive* model calibrated to the smile,
$$
\hat\sigma_{VS,T}=\hat\sigma_T\qquad\text{(log-contract and VS implied vols coincide)}
$$
(Bergomi eq 5.13/5.14). The practical evaluation is a **weighted integral of the smile** (Gatheral/Chriss–Morokoff; Bergomi eq 4.21/5.17):
$$
\boxed{\;\hat\sigma_{VS,T}^2=\int_{-\infty}^{\infty}\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\,\sigma_{BS}^2\!\big(K(y),T\big),\qquad y(K)=\frac{\ln(K/F_T)}{\sigma_{KT}\sqrt T}-\frac{\sigma_{KT}\sqrt T}{2}\;}
$$
For a **flat** smile this is *exactly* $\sigma_0^2$; for a skewed/convex smile the VS vol exceeds the ATM vol - a **skew/convexity premium**. Only in non-diffusive (jump/Lévy) models does $\hat\sigma_{VS,T}\ne\hat\sigma_T$; the gap measures implied short-return skewness, $\hat\sigma_{VS,T}^2-\hat\sigma_T^2\simeq-\tfrac13\lambda\langle J^3\rangle$ (Bergomi eq 5.28/5.29).

**Forward variance** is the tradable state variable:
$$
\xi_t^T=\frac{d}{dT}\big[(T-t)\hat\sigma_{VS,T}^2(t)\big],\qquad d\xi_t^T=\lambda_t^T\,dW_t^T\quad(\text{driftless}),
$$
with the universal constraint $\xi_t^t=\sigma_t^2$: **the short end of the forward-variance curve is the instantaneous variance** (Bergomi eq 5.6, 4.30). This is the foundation of forward-variance / Bergomi models (page 06).

---

### 3. Computational Implementation - SVI, the VS integral, and the density

We evaluate an SVI slice, compute its ATM skew, extract the **variance-swap implied variance** via the log-contract integral (checking the flat-smile identity), and test the slice for **butterfly arbitrage** through the Breeden–Litzenberger density. Stdlib only.




Three verifications land at once: the **flat-smile identity** returns exactly $0.04=\sigma_0^2$; the SVI slice's **butterfly density is everywhere positive** ($\min=0.0178>0$), so it is static-arbitrage free; and the **VS vol ($24.09\%$) exceeds the ATM vol ($18.71\%$)** because the skewed/convex smile forces the log-contract to weight the fat left wing.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Parametric fit without arbitrage constraints.** You can always fit five SVI numbers to one slice, but a family of slices fitted independently will violate calendar no-arbitrage. Fit all expirations **simultaneously** with a monotone total-variance interpolant in $T$ (Gatheral §3, ch 3).
2. **The wrong sticky rule → the wrong delta.** Using BS delta while the market is sticky-delta mis-hedges by the vega×skew term (Hull minimum-variance delta). The choice is *not* cosmetic; it is a statement about the surface's motion, and it is directly measurable via $R_T$.
3. **VS vol ≠ ATM vol is not "noise".** It is the convexity premium; treating the ATM implied vol as the variance-swap strike underprices the swap. Conversely, the residual gap $\hat\sigma_{VS,T}-\hat\sigma_T$ in a diffusive world should be ~$0$ - if your calibration produces a large non-zero gap, your surface extrapolation (not the market) is at fault.
4. **Extrapolation drives the VS integral.** The log-contract integral $\int dy\,e^{-y^2/2}\sigma^2_{K(y)}$ is *very* sensitive to the smile outside traded strikes (Bergomi §5.2). Practitioners invert the other way: use liquid VS quotes to pin the low-strike implied vols (Gatheral ch 3; Bergomi §5.5).
5. **Term-structure kink at dividends.** Total-variance continuity across dividend dates requires the Bos–Vandermark effective-dividend adjustment of $y$ (Bergomi eq 2.23/2.26); ignoring it creates spurious local-vol spikes.

---

### 5. References

- **Gatheral**, *The Volatility Surface*
- **Bergomi**, *Stochastic Volatility Modeling*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Lee, Roger**: *The Moment Formula for Implied Volatility at Extreme Strikes* (2004)

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|02 · Implied vs Local Vol]]
- Forward: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|04 · Advanced Dynamics]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]]

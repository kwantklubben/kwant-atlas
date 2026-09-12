---
title: "3.9.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - multi-curve
  - smile
  - local-volatility
  - stochastic-volatility
  - sabr
  - calibration
  - uncertain-parameter
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]].

---

### 1. Intuition & Practical Objective

This page is the **launchpad** for everything beyond the vanilla single-curve, flat-volatility world. The three directions, in one line each:

1. **The smile in rates (BM Ch9–12).** LFM's lognormal vol is a property of the *rate*, not the strike - so one $v(T)$ cannot match two market caplet strikes. Fix: local-volatility, stochastic-volatility, or uncertain-parameter models that reproduce the strike-dependent implied-vol surface.
2. **Multi-curve / basis risk.** Post-2008 the discount curve (OIS) and the forward curve (LIBOR) diverged; single-curve pricing misvalues swaps, and the LFM's forwards must be consistent with the discount curve.
3. **Calibration (BM Ch7).** Fitting LFM/SVM/UPM parameters to caps + swaptions is the practical art - two-step (vols→caps, correlation→swaptions) or full joint optimization.

> **Why these?** These are exactly the steps where a working model meets the market. The vanilla LFM prices ATM caplets/swaptions correctly by construction; the residual - the smile, the basis, the correlation - is what an extensions page must put on a sound footing.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The smile in the LFM (BM Ch9)

A `T2`-caplet resetting at `T1` pays $\tau(F(T_1;T_1,T_2)-K)^+$ and prices as $P(0,T_2)\tau\,\mathbb{E}^{\mathbb{Q}^{T_2}}[(F-K)^+]$. Under the LFM, $F$ is lognormal, so $v_2(T_1)=\sqrt{\int_0^{T_1}\sigma_2^2\,dt}$ gives Black's formula. **Because LFM volatility is a property of the rate, not the strike, one $v$ cannot match two strikes** - the market caplet prices imply a strike-dependent $v^{MKT}(T_1,K)$, whose curve is the **volatility smile** (minimum near ATM underlying; **skew** = low strikes priced at higher vol, BM §9.1).

The implied density is recovered by **Breeden–Litzenberger** (BM eq. 9.4):

$$
\frac{\partial^2}{\partial K^2}Cpl^{MKT}(0,T_1,T_2,K)=P(0,T_2)\,\tau\, p_2(K),
$$

so the smile *is* a statement about a non-lognormal implied density. Six families can reproduce it (BM §9.2): local-volatility (LVM), stochastic-volatility (SVM), jump-diffusion (JDM), market models of implied vol (MMIV), Lévy-driven (LDM), and **uncertain-parameter models (UPM)**. Only LVM/SVM/UPM are treated in the book for tractability.

#### 2.2 Local-volatility & shifted-lognormal (BM Ch10)

- **Shifted lognormal** $F_j=X_j+\alpha$, $dF_j=\beta(t)(F_j-\alpha)dW$: caplet closed form $Cpl=\tau N\,P(t,T_j)\,Bl(K-\alpha,F_j(t)-\alpha,U)$ - produces only *skews* (BM eq. 10.6).
- **Lognormal-mixture (LM)** local vol $\sigma^2(t,y)=\sum_i\Lambda_i v_i^2/y^2$: caplet is a convex combination of Black prices $\sum_i\lambda_i Bl(K,F_j(0),V_i)$ with the implied-vol **minimum exactly at the ATM strike and zero ATM slope** (BM Prop 10.4.1, eqs 10.27–10.34).
- **CEV** $dF_j=\sigma_j(t)F_j^\gamma dW$, $0<\gamma<1$: absorbing boundary at 0 for $\gamma<1/2$; non-central-$\chi^2$ caplet; LCEV fixes absorption (BM eqs 10.7–10.11).

#### 2.3 Stochastic-volatility & SABR (BM Ch11)

General SVM: $dF_j=a_j\phi(F_j)V^{\gamma}dZ_j$, $dV=a_V dt+b_V dW$. **Zero rate-vol correlation ⇒ smile-shaped vols (min at ATM); a skew needs (i) non-zero correlation, (ii) displaced diffusion, or (iii) non-linear $\phi$** (BM Ch11 opening). Heston-type (Wu–Zhang) uses correlated square-root vol priced by characteristic function + Fourier inversion. **SABR (HKLW 2002)**: $dF=VF^{\beta}dZ$, $dV=\varepsilon V\,dW$ - models a *single* forward asset (per swaption), with the Hagan implied-vol approximation separating **beta skew $\propto-\frac12(1-\beta)$** and **vanna skew $\propto\frac12\rho\lambda$** (BM eqs 11.33–11.35).

#### 2.4 Uncertain-parameter models (BM Ch12)

UPM = volatility is a random *variable*, not a diffusion: $dF_t=\sigma F_t\,dZ_t$ with $\sigma$ drawn $\sigma_1..\sigma_N$ w.p. $\lambda_1..\lambda_N$ just after time 0. The caplet is a **mixture of adjusted Black prices** (BM eq. 12.7):

$$
Cpl=\sum_i\lambda_i\,Bl\big(K+\alpha_j^i,\ F_j(0)+\alpha_j^i,\ V_j^i\big),
$$

producing a smile with minimum at $F_0$; a shift $\alpha$ adds skew. The swaption is likewise a mixture under the annuity measure (BM eq. 12.8).

#### 2.5 Multi-curve & calibration (BM Ch1, Ch7)

**Multi-curve:** post-2008, discount at OIS but quote forwards off LIBOR; the two curves are separate. The swap rate and caplet formulas above must use the *forward curve consistent with the discount curve* - the single-curve relation $1+\tau L=P(t,T)/P(t,S)$ is replaced by a spread between curves.

**Calibration (BM Ch7):** fit LFM vols to caps (fix average vols) and swaptions (fix correlation/terminal structure). **Cascade calibration (CCA)** recovers piecewise-constant vols one swaption at a time walking the swaption matrix; **RCCAEI** adds endogenous interpolation to remove negative/complex artifacts. Two-stage (vol→caps, correlation→swaptions) or joint optimization are the practical routes; instantaneous correlations are treated as exogenous during cascade fitting.

---

### 3. Computational Implementation - smile machinery in numbers

Stdlib only: (1) a UPM/lognormal-mixture caplet reproducing a smile with minimum at ATM, (2) shifted lognormal skew, (3) the SABR implied-vol approximation showing beta/vanna skew.



The UPM mixture produces a textbook **smile**: implied vol dips to its minimum at the ATM strike $F_0=4.04\%$ and rises away from it - the exact signature BM Ch10 (LM) proves analytically. SABR with $\rho<0$ gives a downward skew through ATM with curvature from $\nu$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The under-determined extraction problem.** Breeden–Litzenberger gives the implied density only up to the *interpolation scheme* on prices (BM §9.1). Two interpolations of the same quoted strikes give different smiles. The model does not "know" the true density.
2. **LVM decorrelation caveat (BM §10.5.1).** In *any* LVM the instantaneous corr $\text{corr}(dF,d\nu^2)=+1$ (vol is a function of $F$), yet the terminal corr with time-averaged squared vol is exactly 0 - an UVM projection artifact (BM §12.1.1). Do not read a local-vol model's "correlation" as a stochastic-vol one.
3. **SABR is not an LFM extension (BM Remark 11.4.1).** It models a *single* forward asset; a genuine multi-rate LIBOR smile needs LVM/SVM/UPM with the full measure/correlation structure.
4. **Over-parameterization.** Lognormal-mixture/LMDM/HSDM have many free parameters (BM Ch10 §10.9: LM=5, LMDM=4, HSDM=5); joint UPM calibration can reach 243 free parameters (BM §12.9). Watch for instability and non-uniqueness.
5. **UPM forward vols flatten.** After the volatility "draw," future implied vols lose the initial smile (BM §12 drawback); empirically mitigated by shifts, but a real limit for forward-start products.

---

### 5. Canonical Literature & Study References

- **Brigo–Mercurio**, *Interest Rate Models*, Ch 9 (smile in LFM: Breeden–Litzenberger, six-family taxonomy), Ch 10 (LVM: shifted-lognormal, CEV, lognormal-mixture, LMDM, HSDM, Dupire-à-la), Ch 11 (SVM: AB-R, Wu–Zhang Heston, Piterbarg, SABR, Joshi-Rebonato), Ch 12 (UPM: SLMUP, mixture-of-Black caplet/swaption 12.7/12.8, calibration), Ch 7 (cascade/RCCAEI calibration). *Primary verified source.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 29 (SABR, shifted lognormal, Bachelier for negative rates, SOFR backward-looking).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 34 (BGM) - the single-asset vs multi-rate distinction.
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 27 (LMM) and Ch 28 (positive-interest / potential models) - for completeness of the positive-rate landscape.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Forward topic-folder pages: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]

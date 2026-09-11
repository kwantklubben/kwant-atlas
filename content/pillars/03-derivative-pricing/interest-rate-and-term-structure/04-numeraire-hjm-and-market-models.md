---
title: "04 — Numeraire Change, the HJM Framework & Market Models (LFM/LMM, BGM)"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - numeraire
  - forward-measure
  - hjm
  - libor-market-model
  - bgm
  - black-76
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page is the mathematical *engine room* of interest-rate modelling: the two tools that make rate derivatives tractable. The practical objective: understand why forward-LIBOR products are priced by **Black's formula under the forward measure**, and why swaptions need the **annuity measure**, all via a single device — the **change of numeraire**.

Two structural ideas, both with no constant-$r$ analogue:

1. **A numeraire is just a unit of account you choose to make the payoff simple.** Under the risk-neutral measure $\mathbb{Q}$ (numeraire = bank account $B$), a $T$-payoff needs the messy $\mathbb{E}[e^{-\int_0^T r} \cdot]$ integral. Switch to the **$T$-forward measure** $\mathbb{Q}^T$ (numeraire = the $T$-bond $P(t,T)$) and the same claim prices as $P(t,T)\,\mathbb{E}^{\mathbb{Q}^T}[\text{payoff}]$ — no discount integral, and *any forward rate spanning to $T$ is a martingale* under $\mathbb{Q}^T$. That martingale property is what makes Black's lognormal formula exact.

2. **Model the object you price, not a hidden state.** Short-rate models specify $r$ and derive the curve. **HJM** instead specifies the *whole forward curve* $df(t,T)=\alpha(t,T)dt+\sigma(t,T)dW$ — which fits today's curve *by construction* — and the no-arbitrage **drift condition** then fixes $\alpha$ from $\sigma$ alone. But lognormal *instantaneous* forwards explode (see §2.3). The fix is the **LIBOR market model (LFM/LMM = BGM)**: model each *simple* forward LIBOR $F_k$ as lognormal under its own measure, giving exact Black caplets and avoiding the explosion.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Change of numeraire & the forward measure (BM Ch2; Björk Ch26; Shreve Ch33)

A numeraire is any strictly positive asset. **Fact One (BM Ch2):** price/numeraire is a martingale under that numeraire's measure; **Fact Two:** the risk-neutral price is invariant under change of numeraire. The Radon–Nikodym derivative between bank-account ($\mathbb{Q}$) and forward ($\mathbb{Q}^T$) measures is

$$
\frac{d\mathbb{Q}^T}{d\mathbb{Q}}=\frac{P(T,T)/B(T)}{P(0,T)/B(0)}=\frac{1}{B(T)P(0,T)}.
$$

Pricing a $T$-payoff $X$:

$$
\Pi_t(X)=B(t)\mathbb{E}^{\mathbb{Q}}\!\left[\frac{X}{B(T)}\right]=P(t,T)\,\mathbb{E}^{\mathbb{Q}^T}\left[X\right].
$$

The **Girsanov kernel between two numeraires is their volatility difference**: for numeraires $S_0,S_1$ the kernel is $\varphi^1_0(t)=\sigma_1(t)-\sigma_0(t)$ (Björk eq. 26.20). Crucially, the instantaneous forward $f(t,T)$ is a $\mathbb{Q}^T$-martingale, and the forward LIBOR $L(t;T,S)$ is a $\mathbb{Q}^S$-martingale (numeraire $P(t,S)$) — different maturity indices (Björk Lemma 26.10; BM Prop 2.5.1).

**Forward vs futures (Björk Ch29 correction):** forward price $f(t;T,Y)=\mathbb{E}^{\mathbb{Q}^T}[Y]$; futures price $F(t;T,Y)=\mathbb{E}^{\mathbb{Q}}[Y]$; they are equal *iff* the short rate is deterministic.

#### 2.2 HJM framework (BM Ch5; Björk Ch25; Shreve Ch28/34; Hull Ch33)

Model the forward curve directly:

$$
df(t,T)=\alpha(t,T)dt+\sigma(t,T)dW(t),\qquad f(0,T)=f^{M}(0,T).
$$

No-arbitrage forces the **drift condition** (Björk Prop 25.2):

$$
\alpha(t,T)=\sigma(t,T)\int_t^T\sigma(t,s)ds .
$$

The drift is *completely determined by volatility* — no freedom remains. With this, the bond satisfies $dP=rP\,dt-\sigma^*(t,T)P\,dW$ with accumulated vol $\sigma^*(t,T)=\int_t^T\sigma(t,s)ds$. **Musiela parametrization** ($x=T-t$, $r(t,x)=f(t,t+x)$) turns this into an infinite-dimensional SDE (Björk §25.3). One-factor HJM with mean-reverting vol $\sigma e^{-a(T-t)}$ **is** the Hull–White model (BM Ch5 headline).

#### 2.3 Why lognormal *instantaneous* forwards explode (Shreve Ch34; Björk Ch27)

Take $\sigma(t,T)=\sigma f(t,T)$. Then $\sigma^*(t,T)=\sigma\int_t^T f(t,u)du$ and the HJM drift is $\alpha=\sigma^2 f\int f \sim f^2$. The deterministic toy $f'=f^2$, $f(0)=c$, solves $f(t)=c/(1-ct)$ and **blows up at $t=1/c$** — HJM show the stochastic analogue does the same. Hence: model lognormal *simple* (LIBOR) rates instead.

#### 2.4 LIBOR market model / BGM (BM Ch6; Björk Ch27; Shreve Ch34; Hull Ch33)

Forward LIBOR $F_k(t)=L(t;T_{k-1},T_k)$ is a **martingale under its own forward measure** $\mathbb{Q}^{T_k}$. The LFM postulates

$$
dF_k(t)=\sigma_k(t)F_k(t)\,dZ_k(t)\quad\text{under }\mathbb{Q}^{T_k}.
$$

The **caplet** is then priced *exactly* by Black's formula (BM Prop 6.4.1; Björk Def 27.2):

$$
Cpl_i(t)=P(t,T_i)\,\tau_i\Big[F_i(t)N(d_1)-K N(d_2)\Big],\quad d_1=\frac{\ln(F_i/K)+\tfrac12 v_i^2}{v_i},\quad v_i^2=\int_t^{T_{i-1}}\sigma_i^2(s)\,ds\ \text{(vol accumulated to the reset }T_{i-1}\text{)}.
$$

Under a *single* common measure (e.g. terminal/spot-LIBOR $\mathbb{Q}^d$), the rates carry **drift terms** summing over other rates (BM Prop 6.3.3):

$$
dF_k=\sigma_kF_k\Big[\sum_{j=\beta}^{k}\frac{\rho_{kj}\tau_j\sigma_jF_j}{1+\tau_jF_j}\Big]dt+\sigma_kF_k\,dZ^d_k .
$$

The forward **swap rate** $R_{\alpha,\beta}$ is a martingale under the **annuity (swap) measure** $\mathbb{Q}^{\alpha,\beta}$ (numeraire $C_{\alpha,\beta}(t)=\sum\tau_iP(t,T_i)$), giving the **Black swaption** formula (BM Prop 6.7.1):

$$
PS^{Black}(0)=C_{\alpha,\beta}(0)\Big[R(0)N(d_1)-K N(d_2)\Big].
$$

---

### 3. Computational Implementation — Black caplets, the martingale, and swaptions

Stdlib only: price a caplet by Black, verify forward-LIBOR is driftless (a martingale) under its own measure, and price a swaption under the annuity measure.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
P0 = lambda T: math.exp(-0.04*T)               # flat 4% discount curve

def caplet_black(F,K,v,T_i,tau):
    d1=(math.log(F/K)+0.5*v*v*T_i)/(v*math.sqrt(T_i)); d2=d1-v*math.sqrt(T_i)
    return P0(T_i)*tau*(F*N(d1)-K*N(d2))

# 3y caplet: forward over [2,2.5], strike 4%, vol 20%
F=(P0(2.0)/P0(2.5)-1.0)/0.5; K=0.04; v=0.20; tau=0.5
print(f"3y caplet Black price = {caplet_black(F,K,v,2.5,tau):.6f}")

# LFM martingale: under Q^{T_i}, dF = sigma F dW -> E[F(T_i)] = F(0)
def mc_fwd(F0,v,tau_opt,n):
    random.seed(4); tot=0.0
    for _ in range(n):
        W=random.gauss(0,1)
        tot+=F0*math.exp(-0.5*v*v*tau_opt+v*math.sqrt(tau_opt)*W)
    return tot/n
Em=mc_fwd(F,v,2.0,200000)
print(f"LFM martingale: E^{{Ti}}[F(T_i)] = {Em:.6f}  vs F(0)={F:.6f}")

# Black swaption under annuity measure
def black_swaption(swaprate,K,v,tau,A):
    d1=(math.log(swaprate/K)+0.5*v*v*tau)/(v*math.sqrt(tau)); d2=d1-v*math.sqrt(tau)
    return A*(swaprate*N(d1)-K*N(d2))
A=sum(0.5*P0(0.5*i) for i in range(1,11))      # 5y semi-annual annuity PV
print(f"5y-into-5y ATM payer swaption (v=15%, annuity={A:.3f}) = {black_swaption(0.04,0.04,0.15,5.0,A):.6f}")

# forward vs futures
print(f"forward price S0/B(0,1) = {100/P0(1.0):.4f};  futures E^Q[S(1)] = {100*math.exp(0.04):.4f} (equal when r deterministic)")
```
```
3y caplet Black price = 0.002377
LFM martingale: E^{Ti}[F(T_i)] = 0.040420  vs F(0)=0.040403
5y-into-5y ATM payer swaption (v=15%, annuity=4.487) = 0.023902
forward price S0/B(0,1) = 104.0811;  futures E^Q[S(1)] = 104.0811 (equal when r deterministic)
```
The forward LIBOR is driftless under its own measure (MC returns $F(0)$ to $10^{-4}$) — *that* is why the Black caplet is exact, not an approximation. The swaption uses the annuity numeraire, not the bank account.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Modelling lognormal instantaneous forwards** — the HJM explosion of §2.3. This is *the* structural reason market models exist; do not "fix" it by fiat.
2. **Wrong numeraire for the product.** Caplets need the $T$-forward measure; swaptions need the annuity measure; spot-LIBOR products need $\mathbb{Q}^d$. Pricing a caplet with a constant-discount shortcut, or a swaption with the bank account, is a first-principles error (BM Ch6 §6.2 rigorously avoids any "deterministic discount" approximation).
3. **LFM vs LSM distributional incompatibility.** A swap rate built from lognormal forwards is *not* exactly lognormal under the annuity measure (BM §6.8) — "mostly theoretical" in practice (Brace-Dun-Barton), but real when vols are high.
4. **Forward ≠ futures with stochastic rates.** The futures price is a $\mathbb{Q}$-martingale; the forward is $\mathbb{Q}^T$. Conflating them (Björk Ch29 corrected error) misses the convexity/marking-to-market adjustment.

---

### 5. Canonical Literature & Study References

- **Brigo–Mercurio**, *Interest Rate Models*, Ch 2 (numeraire change: drift-shift 2.12, forward measure 2.20, Prop 2.5.1/2.5.2), Ch 5 (HJM drift condition 5.2, HJM↔HW equivalence, Musiela), Ch 6 (LFM/LSM: Prop 6.3.1–6.3.3, caplet=Black Prop 6.4.1, swaption Prop 6.7.1), Ch 7 (calibration). *Primary verified source.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 25 (HJM, drift condition Prop 25.2, Musiela 25.20), Ch 26 (change of numeraire ★, GER Prop 26.11, caps §26.8), Ch 27 (LMM/LSM, Black caplet Def 27.2, terminal measure 27.30, swaption Def 27.13), Ch 29 (forwards vs futures correction).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 33 (change of numeraire, T-forward measure, Merton formula) and Ch 34 (BGM: forward-LIBOR dynamics 5.3/5.4, Black caplet 9.2, forward swap rate).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 33 (HJM drift 33.5, LMM forward-rate vol 33.10–33.11).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]

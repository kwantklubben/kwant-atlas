---
title: "02 — The BSM PDE, Its Derivation & the Feynman-Kac Bridge"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - pde
  - feynman-kac
  - girsanov
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Two pictures produce the *same* price: the **PDE picture** (a parabolic partial differential equation with boundary conditions, solved analytically for European options) and the **expectation picture** (a discounted conditional expectation under the risk-neutral measure $\mathbb{Q}$). The **Feynman–Kac theorem** is the bridge that declares these two pictures *identical*. The practical objective: once you see the bridge, every option becomes the same kind of object — "integrate the payoff against a probability density under $\mathbb{Q}$" — and the PDE is just that integral written in differential form.

This page gives the **full, honest derivation** of the BSM PDE (delta-neutral replication) plus the **risk-neutral/expectation derivation** (Girsanov change of measure), and then shows they coincide via Feynman–Kac. This is the mathematical spine of the whole topic-folder.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Route A — Delta-Neutral Replicating Portfolio (PDE)

Underlying follows GBM under physical measure $\mathbb{P}$:

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t .$$

Let $V(t,S)$ be the derivative price. By Itô–Doeblin (Shreve II Thm 4.4.6; Hull eq. 14.12):

$$dV = \left(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}+\frac12\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt + \sigma S\frac{\partial V}{\partial S}\,dW .$$

Form $\Pi=V-\Delta S$, the hedged portfolio. Substituting and choosing $\Delta=\partial V/\partial S$ kills the $dW$ term:

$$d\Pi = \left(\frac{\partial V}{\partial t}+\frac12\sigma^2S^2\frac{\partial^2 V}{\partial S^2}\right)dt .$$

A riskless portfolio must earn the risk-free rate (Shreve II §4.5; Björk Prop 7.6 — "only one short rate on an arbitrage-free market"): $d\Pi = r(V-\Delta S)dt$. Equating and rearranging gives the **BSM PDE**:

$$\boxed{\;\frac{\partial V}{\partial t}+rS\frac{\partial V}{\partial S}+\frac12\sigma^2S^2\frac{\partial^2 V}{\partial S^2}-rV=0\;}\qquad (0\le t<T,\; S\ge0).$$

**Terminal & boundary conditions** (Shreve II 4.5.14):
- Terminal payoff: $V(T,S)=\max(S-K,0)$ (call), $\max(K-S,0)$ (put).
- Boundary: $V(t,0)=0$ for a call (a worthless stock, worthless option).
- Growth: $V(t,S)\sim S-e^{-r(T-t)}K$ as $S\to\infty$.

The drift $\mu$ is absent — **volatility (not drift) is the pricing parameter** (Shreve II §4.5).

#### 2.2 Route B — Risk-Neutral Expectation (Girsanov / Martingale)

Shreve II Ch 5 and Björk Ch 7. Define the money-market account $D(t)=e^{-\int_0^t R\,ds}$ and the **market price of risk** $\Theta(t)=(\alpha(t)-R(t))/\sigma(t)$. Girsanov's theorem (Shreve II Thm 5.2.3) builds the equivalent measure $\mathbb{Q}$ via the Radon–Nikodym derivative

$$Z(t)=\exp\!\Big\{-\!\int_0^t\Theta(u)\,dW(u)-\tfrac12\!\int_0^t\Theta^2(u)\,du\Big\},$$

under which $\widetilde W(t)=W(t)+\int_0^t\Theta(u)du$ is a Brownian motion. Under $\mathbb{Q}$ the stock becomes

$$dS = R\,S\,dt+\sigma S\,d\widetilde W,$$

and the **discounted stock $D(t)S(t)$ is a $\mathbb{Q}$-martingale**. The risk-neutral pricing formula (Shreve II 5.2.30/31) is then

$$V(t)=\widetilde{\mathbb{E}}\!\left[e^{-\int_t^T R(u)du}\,V(T)\,\Big|\,F(t)\right].$$

For constant $r,\sigma$ and payoff $(S_T-K)^+$, this expectation has a closed form — the BSM formula (next page). Crucially, the change of measure changes the **mean rate** ($\alpha\to r$) but **not the volatility or the paths**.

#### 2.3 The Feynman–Kac Bridge (Björk Props 5.5/5.6; Shreve II §4.5)

**Theorem.** If $F(t,x)$ solves the parabolic PDE
$$F_t+\mu F_x+\tfrac12\sigma^2F_{xx}-rF=0,\qquad F(T,x)=\Phi(x),$$
for the SDE $dX=\mu\,dt+\sigma\,dW$, then
$$F(t,x)=e^{-r(T-t)}\,\mathbb{E}_{t,x}\!\left[\Phi(X_T)\right].$$

Applying it to the BSM PDE ($\mu=r$, the $\mathbb{Q}$-drift) says exactly: *the PDE solution equals the discounted risk-neutral expectation of the payoff.* The two routes in §2.1 and §2.2 are the same number by construction.

---

### 3. Computational Implementation — verifying the bridge by Monte Carlo

Direct proof of §2.3: simulate the risk-neutral dynamics (drift $r$, not $\mu$) and compare the discounted average payoff to the closed-form BSM price. Stdlib only.

```python
import math, random

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bsm_call(S, X, T, r, sigma):                       # closed form, b=r
    d1 = (math.log(S/X) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    return S*N(d1) - X*math.exp(-r*T)*N(d2)

def mc_risk_neutral_call(S, X, T, r, sigma, npaths):
    """Discounted expected payoff under Q:  V = e^{-rT} E^Q[(S_T-K)^+]."""
    tot = 0.0
    for _ in range(npaths):
        W = random.gauss(0.0, 1.0)
        ST = S*math.exp((r - 0.5*sigma**2)*T + sigma*math.sqrt(T)*W)  # drift = r
        tot += max(ST - X, 0.0)
    return math.exp(-r*T) * tot / npaths

random.seed(7)
S, X, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.20
print(f"closed-form BSM call   = {bsm_call(S,X,T,r,sigma):.4f}")
for n in (1000, 100000):
    print(f"risk-neutral MC (n={n:6d}) = {mc_risk_neutral_call(S,X,T,r,sigma,n):.4f}")
```
```
closed-form BSM call   = 10.4506
risk-neutral MC (n=  1000) = 10.6402
risk-neutral MC (n=100000) = 10.4839
```
The MC expectation converges to the PDE solution — the Feynman–Kac bridge, verified numerically. (Remaining gap at $n{=}10^5$ is $O(1/\sqrt{n})$ sampling error, exactly as Glasserman Ch 1 predicts.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Girsanov requires an integrability condition.** The theorem needs $\widetilde{\mathbb{E}}\!\int_0^T\Theta^2(u)du<\infty$ (equivalently a Novikov-type condition) for $Z$ to be a genuine martingale — this was a flagged omission in early extractions (Shreve II 5.2.13). Without it the change of measure is formal only.
2. **Martingale Representation (MRT) needs the right filtration.** Replicating an $F(T)$-claim requires $F$ to be generated by the Brownian motion (Shreve II Thm 5.3.1). Extra randomness (jumps, an untraded source) breaks completeness — the deep root of the failure modes in [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]].
3. **The delta-neutral "riskless portfolio" is riskless only if rebalancing is continuous.** The PDE is derived for $dt\to0$. In discrete time there is hedging error proportional to gamma and squared returns — the gamma–theta residual ([[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|04 · Greeks]]).
4. **$\frac12\sigma^2$ is not optional.** Itô's lemma uses $dW^2=dt$; forgetting the half-variance term breaks the martingale property and the pricing formula.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 4 (BSM PDE, solution, Greeks, forward, parity) and Ch 5 (Girsanov 5.2.3, risk-neutral pricing 5.2.30, BSM by RN expectation 5.2.5, MRT 5.3.1, FTA 5.4.7/5.4.9). *Math-verified in the corpus.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 5 (Feynman–Kac Props 5.5/5.6) and Ch 7 (arbitrage pricing, BSM PDE Thm 7.7, risk-neutral valuation Thm 7.8). *Math-verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 15 (BSM PDE eq. 15.16, risk-neutral rationale) and Ch 14 (Itô's lemma).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · Pricing Formulas]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]

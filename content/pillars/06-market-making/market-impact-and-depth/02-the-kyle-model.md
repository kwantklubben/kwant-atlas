---
title: "02 — The Kyle (1985) Model: Linear Impact, Lambda & Depth"
tags:
  - pillar-market-making
  - market-impact
  - kyle-lambda
  - depth
  - adverse-selection
  - equilibrium
---

**Basic Prerequisites:** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (informed vs uninformed) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (bivariate normal, projection theorem).

---

### 1. Intuition & Practical Objective

Kyle (1985) answered a question Glosten–Milgrom left open. In a sequential-trade market, the spread is set by a competitive market maker's **zero-profit condition** — but the *informed trader* there is a robot who always trades in the right direction and never optimises. Kyle asked the harder question: what happens when the informed trader is **strategic** — when he knows that a big, aggressive order reveals his information and therefore chooses to *hide* it inside the noise flow?

The answer produced the single most-used object in microstructure: **Kyle's $\lambda$**, the linear price impact. The model is one auction — three agents, one price — and yet it pins down:

- why **price impact is linear** in order flow (at least at the margin),
- why **market depth equals $1/\lambda$**,
- why **exactly half of the private information is impounded** into the price,
- and why **more noise trading makes the market more liquid, while more information makes it less liquid**.

**The economic engine.** The insider faces a trade-off: trade small and the price barely moves (good) but you make little money (bad); trade large and the price moves against you (bad) but you capture more of the mispricing (good). Meanwhile the market makers are Bayesians: a large net buy makes them suspect the value is high. In equilibrium the insider's optimal aggressiveness and the market makers' optimal response are mutually consistent, and the implied price function is **linear**. The constant of proportionality is $\lambda$.

> **The one-sentence essence.** "A competitive market maker sets the price at the expected value given the order flow; a strategic insider trades just aggressively enough that his order flow is uninformative beyond what he intends; the equilibrium price response is linear, $P=p_0+\lambda y$, with $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ and market depth $1/\lambda$."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Setup (single auction)

- **Value:** $v\sim\mathcal N(p_0,\Sigma_0)$ — the terminal value, unknown; prior mean $p_0$, variance $\Sigma_0$.
- **Informed trader:** knows $v$ exactly, submits a market order $x(v)$.
- **Noise ("liquidity") traders:** submit $u\sim\mathcal N(0,\sigma_u^2)$, independent of $v$ and of $x$. This flow is the insider's camouflage.
- **Market makers:** observe the **total order flow** $y=x+u$ (but not its decomposition), act competitively and risk-neutrally, and set the price equal to the expected value:
$$P=\mathbb E[v\mid y].$$

#### 2.2 Solve by conjecture

Suppose the price rule and insider strategy are linear:

$$P=\mu+\lambda y,\qquad x=\alpha+\beta v .$$

**Insider's problem.** Given the price rule, the insider's expected profit conditional on $v$ is
$$\mathbb E[\pi\mid v]=\mathbb E\big[(v-P)x\mid v\big]=(v-\mu-\lambda x)\,x .$$
This is a concave quadratic in $x$; the first-order condition $v-\mu-2\lambda x=0$ gives
$$x=\frac{v-\mu}{2\lambda}\;\Longrightarrow\;\boxed{\ \beta=\frac{1}{2\lambda},\qquad \alpha=-\frac{\mu}{2\lambda}\ }.$$

**Market efficiency.** By the projection theorem for the bivariate normal $(v,y)$,
$$P=\mathbb E[v\mid y]=p_0+\frac{\mathrm{Cov}(v,y)}{\mathrm{Var}(y)}\big(y-\mathbb E[y]\big).$$
Now $y=x+u=\alpha+\beta v+u$, so
$$\mathrm{Cov}(v,y)=\beta\Sigma_0,\qquad \mathrm{Var}(y)=\beta^2\Sigma_0+\sigma_u^2,\qquad \mathbb E[y]=\alpha+\beta p_0 .$$
Hence $\lambda=\dfrac{\beta\Sigma_0}{\beta^2\Sigma_0+\sigma_u^2}$ and $\mu=p_0-\lambda\mathbb E[y]$.

**Closing the system.** Substitute $\beta=1/(2\lambda)$ into the $\lambda$ expression:
$$\lambda=\frac{\beta\Sigma_0}{\beta^2\Sigma_0+\sigma_u^2}\Big|_{\lambda=1/(2\beta)}\;\Longrightarrow\;\beta^2\Sigma_0+\sigma_u^2=2\beta^2\Sigma_0\;\Longrightarrow\;\beta^2=\frac{\sigma_u^2}{\Sigma_0}.$$
Taking the positive root:

$$\boxed{\ \beta=\sqrt{\frac{\sigma_u^2}{\Sigma_0}},\qquad \lambda=\frac{1}{2\beta}=\frac12\sqrt{\frac{\Sigma_0}{\sigma_u^2}},\qquad \mu=p_0,\qquad \alpha=-\tfrac12 p_0\ }$$

(the second-order condition $\lambda>0$ rules out the negative root). **Market depth** is

$$\boxed{\ \frac{1}{\lambda}=2\sqrt{\frac{\sigma_u^2}{\Sigma_0}}\ }$$

— the signed order flow needed to move the price by one dollar. Larger noise flow $\sigma_u^2$ and smaller information $\Sigma_0$ both make the market deeper.

#### 2.3 What the equilibrium implies

- **Information revelation.** $\mathrm{Var}[v\mid y]=\Sigma_0-\dfrac{(\beta\Sigma_0)^2}{\beta^2\Sigma_0+\sigma_u^2}=\Sigma_0-\dfrac{\beta^2\Sigma_0^2}{2\sigma_u^2}=\Sigma_0-\dfrac{\Sigma_0}{2}=\dfrac{\Sigma_0}{2}.$
  **Exactly half of the insider's private information is incorporated into the price, no matter how much noise there is.** This is a sharp, testable fingerprint of the model.
- **Insider profit** (conditional on $v$, using $x=(v-p_0)/2\lambda$):
$$\mathbb E[\pi\mid v]=(v-p_0)x-\lambda x^2=\frac{(v-p_0)^2}{2\lambda}-\frac{(v-p_0)^2}{4\lambda}=\boxed{\frac{(v-p_0)^2}{2}\sqrt{\frac{\sigma_u^2}{\Sigma_0}}},$$
increasing in the squared mispricing and in *noise* variance (more camouflage). Averaging over $v$: $\mathbb E[\pi]=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$. *(This is Hasbrouck Ch 7 eq. 7.5; the conditional-vs-unconditional distinction is the correction flagged in the verified corpus — for a **fixed** $v$ the profit actually *decreases* in $\Sigma_0$.)*
- **Noise independence.** $\mathrm{Var}[P]=\lambda^2(\beta^2\Sigma_0+\sigma_u^2)=\lambda^2\cdot 2\sigma_u^2$, and the price innovations are driven by order flow, not by $\sigma_u^2$ directly: **the volatility of the price is unaffected by the level of noise trading** (Kyle, §2).

#### 2.4 Multi-period and the continuous limit

Repeat the auction $N$ times with the insider splitting his order ("slicing and dicing"). With $v$ fixed and prior variance $\Sigma_n=\mathrm{Var}[v\mid p_n]$:
$$\Delta x_n=\beta_n\,(v-p_{n-1})\,\Delta t,\qquad p_n=p_{n-1}+\lambda_n\,(\Delta x_n+\Delta u_n),\qquad \lambda_n=\frac12\sqrt{\frac{\Sigma_n}{\Delta t\,\sigma_u^2}}.$$
The insider trades so that **total order flow is serially uncorrelated** (a martingale), and $\Sigma_n$ shrinks predictably. As the time between auctions $\to0$ the sequential equilibrium converges to the **continuous auction equilibrium** $dP_t=\lambda\,dY_t$ with $\lambda$ constant — the origin of the "$\Delta P=\lambda\cdot\text{order flow}$" rule used everywhere on this folder. (Huberman–Stanzl 2004: only *linear* price schedules are manipulation-free, which is why the linear model survives.)

---

### 3. Computational Implementation — simulate and recover $\lambda$

Simulate the equilibrium, then **estimate $\lambda$ from order flow by OLS** (as a market maker would), and check the half-information and profit predictions. Stdlib only; the recovery is exact up to sampling noise.

```python
import math, random

def kyle_sim(p0=100.0, Sigma0=4.0, sig_u2=1.0, n=300000, seed=11):
    """Single-auction Kyle equilibrium.
       v ~ N(p0,Sigma0); x = beta(v-p0); u ~ N(0,sig_u2); y = x+u;
       P = p0 + lambda*y,  lambda = 0.5*sqrt(Sigma0/sig_u2)."""
    lam  = 0.5 * math.sqrt(Sigma0 / sig_u2)      # price impact ($ per share of flow)
    beta = math.sqrt(sig_u2 / Sigma0)            # insider aggressiveness
    random.seed(seed); sv, su = math.sqrt(Sigma0), math.sqrt(sig_u2)
    syy = svy = prof = 0.0
    for _ in range(n):
        v = p0 + sv*random.gauss(0, 1)
        u = su*random.gauss(0, 1)
        x = beta*(v-p0); y = x+u; P = p0 + lam*y
        prof += (v-P)*x
        svy += (v-p0)*y; syy += y*y
    slope = svy/syy                              # OLS of (v-p0) on order flow y
    resid = Sigma0 - slope*slope*(syy/n)         # Var[v|y] empirically
    return lam, beta, slope, resid, prof/n

lam, beta, slope, resid, prof = kyle_sim()
print("Kyle single-auction equilibrium: p0=100, Sigma0=4, sigma_u^2=1")
print(f"  lambda (theory)        = {lam:.4f}   [0.5*sqrt(Sigma0/sigma_u^2)]")
print(f"  beta   (theory)        = {beta:.4f}   [sqrt(sigma_u^2/Sigma0)]")
print(f"  lambda (recovered,OLS) = {slope:.4f}   <- impact estimated from flow")
print(f"  Var[v|y] (empirical)   = {resid:.4f}   [theory Sigma0/2 = 2.0000]")
print(f"  insider profit         = {prof:.4f}   [theory 0.5*sqrt(sigma_u^2*Sigma0) = 1.0000]")
print(f"  market depth  1/lambda = {1/lam:.4f}")
```

```
Kyle single-auction equilibrium: p0=100, Sigma0=4, sigma_u^2=1
  lambda (theory)        = 1.0000   [0.5*sqrt(Sigma0/sigma_u^2)]
  beta   (theory)        = 0.5000   [sqrt(sigma_u^2/Sigma0)]
  lambda (recovered,OLS) = 0.9998   <- impact estimated from flow
  Var[v|y] (empirical)   = 1.9982   [theory Sigma0/2 = 2.0000]
  insider profit         = 0.9969   [theory 0.5*sqrt(sigma_u^2*Sigma0) = 1.0000]
  market depth  1/lambda = 1.0000
```

Every equilibrium prediction is recovered from the simulation: $\lambda$ from a regression of value on flow, the halving of variance, and the insider's profit. **The market maker never sees $v$ — but the regression of $v$ on $y$ hands him exactly the price rule the model says he should use.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The linear-price-rule assumption is fragile.** Linearity comes from **normality** (the projection theorem). With fat-tailed values or non-Gaussian noise the linear equilibrium may not exist or may not be unique; the "$\lambda$" you estimate empirically is then a local slope, not a structural constant.
2. **Competition and risk neutrality.** Market makers are assumed perfectly competitive and risk-neutral, so price $=\mathbb E[v\mid y]$ exactly (zero expected profit). A real book has finite depth, inventory costs ([[pillars/06-market-making/inventory-management-and-quote-skewing|inventory skewing]]) and a spread — the Kyle $\lambda$ is the *adverse-selection* component, not the whole cost.
3. **Single informed trader.** The model assumes one strategic insider. With multiple informed traders (or a partially informed one), the equilibrium $\lambda$ changes and information is impounded faster — the empirically relevant case.
4. **The insider is assumed to know $v$ exactly and have infinite horizon.** Real informed traders have noisy signals and must trade before their information decays; this is why the *continuous* equilibrium and its no-dynamic-arbitrage constraints (page 06) matter.
5. **$\lambda$ is not constant in reality.** Empirically impact is concave (square-root) at larger sizes and $\lambda$ drifts with intraday depth. Kyle's $\lambda$ is the correct *local linearisation*, and the square-root law is its concavity at scale (page 04).
6. **Half-information is a knife-edge.** $\mathrm{Var}[v\mid p]=\Sigma_0/2$ depends on the joint normality and the single-auction timing. In multi-period versions the fraction impounded per round is $\Sigma_n-\Sigma_{n+1}$ and is *not* a constant half.

---

### 5. Canonical Literature & Study References

- **Kyle, A. S. (1985)**, *Continuous auctions and insider trading*, Econometrica 53(6), 1315–1335. *Theorem 1 (single auction): $\beta=(\sigma_u^2/\Sigma_0)^{1/2}$, $\lambda=\tfrac12(\Sigma_0/\sigma_u^2)^{1/2}$; §2 "Properties": $1/\lambda$ = depth, $\mathrm{Var}[v\mid p]=\Sigma_0/2$, profit. Primary PDF in corpus (`40_Kyle_1985_...`).*
- **Hasbrouck, J. (2007)**, *Empirical Market Microstructure*, Ch 7 *Strategic Trade Models*. *Cleanest textbook exposition of the equilibrium, eqs 7.1–7.5; verified in corpus (`hasbrouck_ch6-10.md`, Ch 7 section).*
- **Huberman, G. & Stanzl, W. (2004)**, *Price manipulation and quasi-arbitrage*, Econometrica 72(4). *Only linear price schedules are manipulation-free — the no-arbitrage anchor for Kyle's linear rule.*
- **Glosten, L. R. & Milgrom, P. R. (1985)**, *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*, JFE 14(1). *The sequential-trade counterpart (non-strategic insider).*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-impact-and-depth/01-from-zero-intuition|01 · From Zero]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]]
- Forward: [[pillars/06-market-making/market-impact-and-depth/03-temporary-vs-permanent-impact|03 · Temporary vs Permanent]] · [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]] · [[pillars/06-market-making/market-impact-and-depth/index|Index Hub]]
- Related: [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] (the $\lambda$-and-$c$ decomposition of the spread) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (where the book's depth is actually observed)

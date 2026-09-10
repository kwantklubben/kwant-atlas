---
title: "01 — Black-Scholes-Merton from Zero: Intuition & the Why"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - intuition
  - replication
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of Black-Scholes-Merton with **no prior derivatives knowledge needed**. The objective is one idea: **an option can be exactly replicated by a continuously-rebalanced portfolio of the underlying stock and the risk-free bond, and therefore its price is forced by the no-arbitrage principle — it cannot be anything else.**

Start with the dumbest question: *why does an option have a price at all?* A stock has a price because it pays future cash flows. An option is just a *contract* — a bet written as $\max(S_T-K,0)$ for a call. Its value comes from a different mechanism: you can **manufacture** that payoff by trading. If the manufacturing cost is knowable, then the option must trade at that cost, or someone can lock in a risk-free profit by selling the option and manufacturing the payoff cheaply (or vice-versa).

Three steps, three "aha"s:

1. **The stock's expected drift is irrelevant.** The stock moves as $dS=\mu S\,dt+\sigma S\,dW$. The *probability* of ending in the money depends on $\mu$. But because we replicate by holding a delta-share position, the option's *price* cancels $\mu$ entirely. You never need to forecast the direction — you only need the *size of the wiggles* $\sigma$.

2. **Volatility, not drift, is the pricing parameter.** If two stocks have the same volatility but different expected returns, options on them must have the *same* price. Only $\sigma$ matters. This feels absurd at first and is exactly right: the hedge removes the return, leaving only the uncertainty that volatility quantifies.

3. **Risk-neutral expectation is a bookkeeping trick, not a belief.** The "risk-neutral measure" $\mathbb{Q}$ does not say the market is risk-neutral. It is the measure under which *discounted prices are martingales*, and its only job is to make the drift equal $r$ so that pricing becomes "discount the expected payoff." It is a change of measure (Girsanov), not a change of opinion.

---

### 2. Mathematical Ground Truth & Derivations

**The replication story in three pictures.**

**One-step binomial (the discrete seed).** Suppose the stock is $S_0$ and, over one period, moves to either $S_0u$ (up) or $S_0d$ (down). Buy $\Delta$ shares and finance with the bond. Choose $\Delta$ so the portfolio's payoff matches the option in both states:

$$\Delta = \frac{f_u-f_d}{S_0u-S_0d},$$

where $f_u,f_d$ are the option payoffs in the up/down states. The option price is the (discounted) cost of this replicating portfolio. Letting the number of steps $\to\infty$ and the step size $\to0$ (Cox–Ross–Rubinstein) converges *exactly* to the BSM closed form.

**Continuous limit.** In continuous time the underlying obeys geometric Brownian motion

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t.$$

By Itô's lemma the option $V(t,S)$ moves as

$$dV = \Big(\frac{\partial V}{\partial t}+\mu S\frac{\partial V}{\partial S}+\tfrac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}\Big)dt + \sigma S\frac{\partial V}{\partial S}\,dW.$$

Hold $\Pi=V-\Delta S$. Pick $\Delta=\partial V/\partial S$ to kill the $dW$ term — the portfolio becomes **riskless**, so it must earn $r$ (else arbitrage):

$$\frac{\partial V}{\partial t}+\tfrac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}=r\Big(V-S\frac{\partial V}{\partial S}\Big)
\;\Longrightarrow\;
\frac{\partial V}{\partial t}+rS\frac{\partial V}{\partial S}+\tfrac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}-rV=0.$$

This is the BSM PDE (Hull eq. 15.16; Shreve II 4.5.14; Björk Thm 7.7). **Notice: $\mu$ is gone.** That is the entire point of the model.

---

### 3. Computational Implementation — the binomial tree *converges* to BSM

This is the single most convincing way to *see* the theory: build the CRR tree (Haug §4.1, hull Ch 13), price a European put, and watch it converge to the closed form. Stdlib only.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bsm_put(S, X, T, r, sigma):                       # closed form, b=r
    d1 = (math.log(S/X) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    return X*math.exp(-r*T)*N(-d2) - S*N(-d1)

def crr_euro_put(S, X, T, r, sigma, n):               # CRR binomial, backward induction
    dt = T/n; u = math.exp(sigma*math.sqrt(dt)); d = 1.0/u
    p  = (math.exp(r*dt) - d) / (u - d)               # risk-neutral prob (b=r)
    val = [max(X - S*u**(n-i)*d**i, 0.0) for i in range(n+1)]   # terminal payoff
    for j in range(n-1, -1, -1):
        val = [math.exp(-r*dt)*(p*val[i] + (1-p)*val[i+1]) for i in range(j+1)]
    return val[0]

S, X, T, r, sigma = 100.0, 95.0, 0.5, 0.08, 0.30
exact = bsm_put(S, X, T, r, sigma)
print(f"BSM closed-form put = {exact:.4f}   (Haug-verified: 4.4494)")
for n in (5, 25, 100, 1000):
    v = crr_euro_put(S, X, T, r, sigma, n)
    print(f"  CRR tree n={n:5d}: {v:.4f}   error={abs(v-exact):.4f}")
```
```
BSM closed-form put = 4.4494   (Haug-verified: 4.4494)
  CRR tree n=    5: 4.6277   error=0.1783
  CRR tree n=   25: 4.4265   error=0.0229
  CRR tree n=  100: 4.4544   error=0.0050
  CRR tree n= 1000: 4.4496   error=0.0003
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "it's just expected discounted payoff" trap.** Under the *physical* measure $\mathbb{P}$, $\mathbb{E}^{\mathbb{P}}[e^{-rT}\max(S_T-K,0)]$ is *not* the correct price — it depends on $\mu$. Only under $\mathbb{Q}$ (drift $=r$) does it price correctly. The beginner error is to discount under the wrong measure.
2. **Replication is not prediction.** The hedge removes drift, but only if you can trade continuously. If you cannot (costs, gaps, jumps), $\mu$-independence breaks down — that is the seed of every failure mode in [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]].
3. **The $\frac12\sigma^2$ correction surprises beginners.** $\ln S_T$ has drift $\mu-\tfrac12\sigma^2$, not $\mu$. Itô's lemma inserts the half-variance term because $dW^2=dt$ has nonzero quadratic variation. Missing it misprices everything.

---

### 5. Canonical Literature & Study References

- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 2 (binomial: replicating weights, risk-neutral valuation, Prop 2.9–2.11) — the cleanest discrete seed.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13 (binomial trees & convergence) and Ch 15 (the model, risk-neutral rationale).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.1 (CRR tree, verified 4.4494→4.4496).

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial-trees|No-Arbitrage & Binomial Trees]]
- Continue: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|02 · PDE & Derivation]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]

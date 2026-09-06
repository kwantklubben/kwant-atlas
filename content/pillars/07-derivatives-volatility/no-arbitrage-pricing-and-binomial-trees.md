---
title: "No-Arbitrage Pricing & Binomial Trees"
tags: [derivatives, binomial-trees, crr, put-call-parity]
---

# No-Arbitrage Pricing & Binomial Trees

Before continuous stochastic calculus, derivatives pricing can be completely understood through discrete no-arbitrage mechanics.

## 1. Put-Call Parity
Consider two portfolios at time $t$:
- Portfolio A: One European call option $C_t$ + Cash $K e^{-r(T-t)}$.
- Portfolio B: One European put option $P_t$ + One share of stock $S_t$.

At expiration $T$:
- If $S_T > K$: Portfolio A is $(S_T - K) + K = S_T$. Portfolio B is $0 + S_T = S_T$.
- If $S_T \le K$: Portfolio A is $0 + K = K$. Portfolio B is $(K - S_T) + S_T = K$.

Both portfolios have **identically identical payoffs** in all states of the world. By the Law of One Price:
$$C_t + K e^{-r(T-t)} = P_t + S_t$$

---

## 2. Cox-Ross-Rubinstein (CRR) Binomial Tree
Let stock $S$ move over time step $\Delta t$ to either $u S$ with probability $p$ or $d S$ with probability $1 - p$.
To match continuous-time volatility $\sigma$:
$$u = e^{\sigma \sqrt{\Delta t}}, \quad d = \frac{1}{u} = e^{-\sigma \sqrt{\Delta t}}$$

### Risk-Neutral Probability
Construct a replicating portfolio of $\Delta$ shares and bank loan $B$. Setting the portfolio value equal to the option payoff at both up and down nodes reveals that the option price is the discounted expected value under the **unique risk-neutral probability $q$**:
$$q = \frac{e^{r \Delta t} - d}{u - d}$$
$$V_0 = e^{-r \Delta t} [q V_u + (1 - q) V_d]$$

### American Options & Early Exercise
Binomial trees solve American option pricing via backward induction by comparing continuation value to immediate exercise value at each node:
$$V_{\text{node}} = \max\left( \text{Payoff}(S), \, e^{-r \Delta t} [q V_u + (1 - q) V_d] \right)$$

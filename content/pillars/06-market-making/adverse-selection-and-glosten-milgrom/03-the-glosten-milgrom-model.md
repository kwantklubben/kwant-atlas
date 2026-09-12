---
title: "6.4.3 The Glosten–Milgrom Sequential-Trade Model"
tags:
  - pillar-market-making
  - glosten-milgrom
  - bayesian-updating
  - market-maker
  - bid-ask-spread
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/index|Bayesian Statistics]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/02-informed-vs-uninformed|02 · Informed vs Uninformed]].

---

### 1. Intuition & Practical Objective

Glosten–Milgrom (1985) built the smallest market where the spread is *endogenous*: one risky asset worth either $V_L$ or $V_H$; a risk-neutral, **competitive** market maker; and a random stream of traders who are either informed (know the state) or uninformed (trade noise). The maker's only tool is a price rule. The model's striking conclusions, all verified against Hasbrouck Ch 5 and Foucault Ch 3:

1. **The spread exists *purely* because of potential informed trading.** With zero informed traders ($\pi=0$) the spread collapses to zero even though the maker still does all the mechanics.
2. **Quotes are "regret-free" conditional means.** The maker sets ask = expected value *given a buy just hit it* and bid = expected value *given a sell just hit it*. Because a buy is mildly informative, the maker marks the ask *up* and the bid *down* - and the gap between the two is the spread.
3. **Transaction prices are a martingale** with respect to the maker's information: prices adapt as fast as the maker learns, so the trade-price series cannot be predicted. Yet the observable tick-by-tick moves *convey* information - that is price discovery.

The practical objective: implement the market maker's inference + quoting policy, run it, and watch the belief and the spread evolve through hundreds of trades - a faithful, working rendition of the primary paper.

---

### 2. Mathematical Ground Truth & Derivations

Let $V\in\{V_L,V_H\}$, prior $\theta_{t-1}=\mathbb{P}(V=V_H)$, and $\pi$ = probability a given trader is informed. Uninformed buy/sell with probability $\tfrac12$; informed buy if $V=V_H$, sell if $V=V_L$.

**Arrival law of a Buy order:**

$$
\mathbb{P}(B\mid V_H)=\pi+(1-\pi)\tfrac12=\tfrac{1+\pi}{2},\qquad
\mathbb{P}(B\mid V_L)=(1-\pi)\tfrac12=\tfrac{1-\pi}{2}.
$$

**Bayes update** (Hasbrouck eq. 5.1/5.5; Foucault eq. 3.16–3.17):

$$
\theta_{t}^{+}=\frac{\tfrac{1+\pi}{2}\,\theta_{t-1}}{\tfrac{1+\pi}{2}\theta_{t-1}+\tfrac{1-\pi}{2}(1-\theta_{t-1})},\qquad
\theta_{t}^{-}=\frac{\tfrac{1-\pi}{2}\,\theta_{t-1}}{\tfrac{1-\pi}{2}\theta_{t-1}+\tfrac{1+\pi}{2}(1-\theta_{t-1})}.
$$

**Zero-profit (competitive, regret-free) quotes** (Hasbrouck eq. 5.2/5.6; Foucault eq. 3.5/3.7):

$$
A_{t}=\mathbb{E}[V\mid B_t]=V_L+\theta_{t}^{+}(V_H-V_L),\qquad
B_{t}=\mathbb{E}[V\mid S_t]=V_L+\theta_{t}^{-}(V_H-V_L).
$$

**Vanishing spread as learning converges.** With $\theta_0=\tfrac12$ and a value dispersion of $V_H-V_L=2$:

$$
S_t=A_t-B_t=\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi\theta_{t-1}+\tfrac{1-\pi}{2}}(2)+\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi(1-\theta_{t-1})+\tfrac{1-\pi}{2}}(2),
$$

which at $\theta_{t-1}=\tfrac12$ gives the celebrated **first-trade spread**

$$
\boxed{\;S_{\theta=\tfrac12}=\pi(V_H-V_L)\;}.
$$

The spread is widest at maximal uncertainty ($\theta=\tfrac12$), shrinks toward $0$ as $\theta\to1$ or $0$ (the maker learns the value), and is **zero for all $\theta$ when $\pi=0$** - adverse selection alone generates the entire spread. Hasbrouck's equivalent formula (with $\delta=\mathbb{P}(V=V_L)$) is $A-B=\dfrac{4(1-\delta)\delta\mu(V_H-V_L)}{1-(1-2\delta)^2\mu^2}$, identical at $\delta=\tfrac12$ to $\pi(V_H-V_L)$.

**Net wealth-transfer identity** (Hasbrouck eq. 5.4): expected gains from uninformed exactly balance expected losses to informed,

$$
(A-\mathbb{E}[V\mid U,B])\Pr(U\mid B)=-(A-\mathbb{E}[V\mid I,B])\Pr(I\mid B).
$$

---

### 3. Computational Implementation - the sequential Bayesian market maker (stdlib only)

Simulate the maker learning. With true value $V=V_H=12$, $\pi=0.25$: the maker starts at $\theta=0.5$, quotes ask $11.25$/bid $10.75$, and after thousands of informed-biased buys drives $\theta\to1$ and the spread to $0$. **Ran and verified.**





The output is exactly the model's three claims: (1) spread grows linearly in $\pi$ (and is $0$ at $\pi=0$), (2) the quoted values track $\theta$, and (3) over time the competing maker learns the truth - price converges to $V_H$ and the spread vanishes. This is **price discovery**: transaction prices are martingales for the maker, yet they converge to the true value.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Missing why the spread is asymmetric.** In general $\theta\neq\tfrac12$, so $A$ and $B$ are *not* symmetric about the unconditional mean. Quoting mid $=\mathbb{E}[V]$ is wrong once flow is one-sided - the mid should equal $\mu_t=\theta_tV_H+(1-\theta_t)V_L$ only when $\theta=\tfrac12$ (Hasbrouck Ch 5; Foucault Ch 3).
2. **Forgetting the quotes are conditional, not point estimates.** $A=\mathbb{E}[V\mid B_t]$ is an expected value given a *specific* order. A maker who treats the ask as "value + constant fee" has thrown away the information content of the order that just filled them.
3. **The martingale does not mean "no information."** Transaction prices being a martingale w.r.t. the maker's info does **not** imply trades are uninformative - it is precisely because they are informative that the maker marks them into the quotes. Conflating the two is the classic misread of GM.

---

### 5. Canonical Literature & Study References

- **Glosten & Milgrom (1985)**, JFE 14(1), 71–100 - the anchor paper; the model, the regret-free/martingale results, the serial-correlation-of-spread analysis.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 5 §5.2 (eqs 5.1–5.7; spread formula; wealth-transfer identity; extensions) and §5.3 (market dynamics; martingale; spread decline). **Math-verified.**
- **Foucault, Pagano & Röell (2013)**, *Market Liquidity*, Ch 3 §3.4 (eqs 3.6–3.28; spread $\pi(v_H-v_L)$; belief updates; convergence). **Math-verified.**
- **Bagehot (1971)** (= Walter Bagehot pseudonym), *The only game in town*, Financial Analysts Journal 27(2), 12–14 - the essay that first framed adverse selection as the reason dealers must charge a spread.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/02-informed-vs-uninformed|02 · Informed vs Uninformed]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]] (add order-processing & inventory on top of this information spread)
- Sibling: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov Optimal Quoting]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
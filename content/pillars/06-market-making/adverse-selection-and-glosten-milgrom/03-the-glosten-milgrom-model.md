---
title: "03 — The Glosten–Milgrom Sequential-Trade Model: the Bayesian Market Maker"
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
2. **Quotes are "regret-free" conditional means.** The maker sets ask = expected value *given a buy just hit it* and bid = expected value *given a sell just hit it*. Because a buy is mildly informative, the maker marks the ask *up* and the bid *down* — and the gap between the two is the spread.
3. **Transaction prices are a martingale** with respect to the maker's information: prices adapt as fast as the maker learns, so the trade-price series cannot be predicted. Yet the observable tick-by-tick moves *convey* information — that is price discovery.

The practical objective: implement the market maker's inference + quoting policy, run it, and watch the belief and the spread evolve through hundreds of trades — a faithful, working rendition of the primary paper.

---

### 2. Mathematical Ground Truth & Derivations

Let $V\in\{V_L,V_H\}$, prior $\theta_{t-1}=\mathbb{P}(V=V_H)$, and $\pi$ = probability a given trader is informed. Uninformed buy/sell with probability $\tfrac12$; informed buy if $V=V_H$, sell if $V=V_L$.

**Arrival law of a Buy order:**

$$\mathbb{P}(B\mid V_H)=\pi+(1-\pi)\tfrac12=\tfrac{1+\pi}{2},\qquad
\mathbb{P}(B\mid V_L)=(1-\pi)\tfrac12=\tfrac{1-\pi}{2}.$$

**Bayes update** (Hasbrouck eq. 5.1/5.5; Foucault eq. 3.16–3.17):

$$\theta_{t}^{+}=\frac{\tfrac{1+\pi}{2}\,\theta_{t-1}}{\tfrac{1+\pi}{2}\theta_{t-1}+\tfrac{1-\pi}{2}(1-\theta_{t-1})},\qquad
\theta_{t}^{-}=\frac{\tfrac{1-\pi}{2}\,\theta_{t-1}}{\tfrac{1-\pi}{2}\theta_{t-1}+\tfrac{1+\pi}{2}(1-\theta_{t-1})}.$$

**Zero-profit (competitive, regret-free) quotes** (Hasbrouck eq. 5.2/5.6; Foucault eq. 3.5/3.7):

$$A_{t}=\mathbb{E}[V\mid B_t]=V_L+\theta_{t}^{+}(V_H-V_L),\qquad
B_{t}=\mathbb{E}[V\mid S_t]=V_L+\theta_{t}^{-}(V_H-V_L).$$

**Vanishing spread as learning converges.** With $\theta_0=\tfrac12$ and a value dispersion of $V_H-V_L=2$:

$$S_t=A_t-B_t=\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi\theta_{t-1}+\tfrac{1-\pi}{2}}(2)+\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi(1-\theta_{t-1})+\tfrac{1-\pi}{2}}(2),$$

which at $\theta_{t-1}=\tfrac12$ gives the celebrated **first-trade spread**

$$\boxed{\;S_{\theta=\tfrac12}=\pi(V_H-V_L)\;}.$$

The spread is widest at maximal uncertainty ($\theta=\tfrac12$), shrinks toward $0$ as $\theta\to1$ or $0$ (the maker learns the value), and is **zero for all $\theta$ when $\pi=0$** — adverse selection alone generates the entire spread. Hasbrouck's equivalent formula (with $\delta=\mathbb{P}(V=V_L)$) is $A-B=\dfrac{4(1-\delta)\delta\mu(V_H-V_L)}{1-(1-2\delta)^2\mu^2}$, identical at $\delta=\tfrac12$ to $\pi(V_H-V_L)$.

**Net wealth-transfer identity** (Hasbrouck eq. 5.4): expected gains from uninformed exactly balance expected losses to informed,

$$(A-\mathbb{E}[V\mid U,B])\Pr(U\mid B)=-(A-\mathbb{E}[V\mid I,B])\Pr(I\mid B).$$

---

### 3. Computational Implementation — the sequential Bayesian market maker (stdlib only)

Simulate the maker learning. With true value $V=V_H=12$, $\pi=0.25$: the maker starts at $\theta=0.5$, quotes ask $11.25$/bid $10.75$, and after thousands of informed-biased buys drives $\theta\to1$ and the spread to $0$. **Ran and verified.**

```python
import random

def gm_quotes(prior_high, mu, v_low=10.0, v_high=12.0):
    """Zero-profit GM quotes. Returns (ask, bid, theta_after_buy, theta_after_sell)."""
    pbH, pbL = (1 + mu) / 2, (1 - mu) / 2          # P(Buy|V_H), P(Buy|V_L)
    psH, psL = (1 - mu) / 2, (1 + mu) / 2          # P(Sell|V_H), P(Sell|V_L)
    th_buy  = pbH * prior_high / (pbH * prior_high + pbL * (1 - prior_high))
    th_sell = psH * prior_high / (psH * prior_high + psL * (1 - prior_high))
    ask = v_low + th_buy  * (v_high - v_low)
    bid = v_low + th_sell * (v_high - v_low)
    return ask, bid, th_buy, th_sell

print("Opening quotes at theta=1/2 (competitive spread should equal pi*(V_H-V_L)=2*pi, V_H-V_L=2):")
for mu in (0.0, 0.1, 0.25, 0.5, 0.9):
    a, b, _, _ = gm_quotes(0.5, mu)
    print(f"  pi={mu:.2f}: ask={a:.4f}  bid={b:.4f}  spread={a-b:.4f}     2*pi={2*mu:.2f}")

def simulate_gm(mu, v_low, v_high, n, seed=3):
    random.seed(seed)
    true_v = v_high; theta = 0.5; final = None
    for _ in range(n):
        a, b, thb, ths = gm_quotes(theta, mu, v_low, v_high)
        if random.random() < mu:      # informed -> trade toward true value
            side = +1 if true_v == v_high else -1
        else:                         # uninformed -> coin flip
            side = +1 if random.random() < 0.5 else -1
        theta = thb if side == +1 else ths
        final = (a, b)
    return theta, final

print("\nSequential discovery, true V=12, pi=0.25:")
th, (a, b) = simulate_gm(0.25, 10.0, 12.0, 3000)
print(f"  after 3000 trades: posterior theta={th:.4f}  final ask={a:.4f} bid={b:.4f} spread={a-b:.4f}")
print("  (theta -> 1 and spread -> 0: the maker has learned the true high value V_H=12)")
```

```text
Opening quotes at theta=1/2 (competitive spread should equal pi*(V_H-V_L)=2*pi, V_H-V_L=2):
  pi=0.00: ask=11.0000  bid=11.0000  spread=0.0000     2*pi=0.00
  pi=0.10: ask=11.1000  bid=10.9000  spread=0.2000     2*pi=0.20
  pi=0.25: ask=11.2500  bid=10.7500  spread=0.5000     2*pi=0.50
  pi=0.50: ask=11.5000  bid=10.5000  spread=1.0000     2*pi=1.00
  pi=0.90: ask=11.9000  bid=10.1000  spread=1.8000     2*pi=1.80

Sequential discovery, true V=12, pi=0.25:
  after 3000 trades: posterior theta=1.0000  final ask=12.0000 bid=12.0000 spread=0.0000
  (theta -> 1 and spread -> 0: the maker has learned the true high value V_H=12)
```

The output is exactly the model's three claims: (1) spread grows linearly in $\pi$ (and is $0$ at $\pi=0$), (2) the quoted values track $\theta$, and (3) over time the competing maker learns the truth — price converges to $V_H$ and the spread vanishes. This is **price discovery**: transaction prices are martingales for the maker, yet they converge to the true value.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Missing why the spread is asymmetric.** In general $\theta\neq\tfrac12$, so $A$ and $B$ are *not* symmetric about the unconditional mean. Quoting mid $=\mathbb{E}[V]$ is wrong once flow is one-sided — the mid should equal $\mu_t=\theta_tV_H+(1-\theta_t)V_L$ only when $\theta=\tfrac12$ (Hasbrouck Ch 5; Foucault Ch 3).
2. **Forgetting the quotes are conditional, not point estimates.** $A=\mathbb{E}[V\mid B_t]$ is an expected value given a *specific* order. A maker who treats the ask as "value + constant fee" has thrown away the information content of the order that just filled them.
3. **The martingale does not mean "no information."** Transaction prices being a martingale w.r.t. the maker's info does **not** imply trades are uninformative — it is precisely because they are informative that the maker marks them into the quotes. Conflating the two is the classic misread of GM.

---

### 5. Canonical Literature & Study References

- **Glosten & Milgrom (1985)**, JFE 14(1), 71–100 — the anchor paper; the model, the regret-free/martingale results, the serial-correlation-of-spread analysis.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 5 §5.2 (eqs 5.1–5.7; spread formula; wealth-transfer identity; extensions) and §5.3 (market dynamics; martingale; spread decline). **Math-verified.**
- **Foucault, Pagano & Röell (2013)**, *Market Liquidity*, Ch 3 §3.4 (eqs 3.6–3.28; spread $\pi(v_H-v_L)$; belief updates; convergence). **Math-verified.**
- **Bagehot (1971)** (= Walter Bagehot pseudonym), *The only game in town*, Financial Analysts Journal 27(2), 12–14 — the essay that first framed adverse selection as the reason dealers must charge a spread.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/02-informed-vs-uninformed|02 · Informed vs Uninformed]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]] (add order-processing & inventory on top of this information spread)
- Sibling: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov Optimal Quoting]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
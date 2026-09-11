---
title: "6.4.2 Informed vs Uninformed Traders"
tags:
  - pillar-market-making
  - informed-trading
  - noise-traders
  - toxic-flow
  - bayesian-inference
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/index|Bayesian Statistics]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Every trade is an unresolved mystery: is this buyer *informed* (they know the price is going up) or *uninformed* (they just need to sell for cash)? The two types are observationally tangled — both hit your ask. This page is about **type detection**: how to use the *pattern* of order flow to update your belief that you are trading against someone who knows something.

The objective: build the inference machinery that the market maker uses every round. It has three ingredients:

1. **The informed trader is directionally committed.** They trade only in the direction of their (private) information. Uninformed traders' directions are coin flips. So a *concentrated run* of one-sided buys is statistically much more likely to be informed-driven than a balanced mix.
2. **The prior matters.** If you believe insiders are rare ($\pi$ small), a single buy is weak evidence; a *streak* of buys is strong. The Bayesian posterior compresses all of this into one number: $\theta_t=\mathbb{P}(V=V_H\mid \text{orders seen so far})$.
3. **Not every buy is toxic.** $\mathbb{P}(\text{informed}\mid \text{buy})$ is generally *larger* than $\pi$ — a buy is a mild signal — but it is only overwhelming for large $\pi$ or long streaks. This quantification is the core of "toxicity."

> **The tester's habit.** Whenever you see flow, first ask *what would posterior $\theta$ be if this trader were uninformed?* — the answer is "noisy around $\theta_{t-1}$." Informed traders push $\theta$ in a *consistent* direction. Deviation from the noise benchmark is the signal.

---

### 2. Mathematical Ground Truth & Derivations

In the GM economy, informed traders buy with probability $1$ when $V=V_H$ and sell with probability $1$ when $V=V_L$; uninformed buy or sell with probability $\tfrac12$. The condition matters: an informed trader buys only in the high state, so

$$
\mathbb{P}(B\mid I)=\mathbb{P}(V_H\mid I)=\theta_{t-1},\qquad \mathbb{P}(B\mid U)=\tfrac12,\qquad \mathbb{P}(B)=\pi\,\theta_{t-1}+(1-\pi)\tfrac12 .
$$

(Equivalently, conditioned on the *state*, $\mathbb{P}(B\mid V_H)=\pi+(1-\pi)\tfrac12=\tfrac{1+\pi}{2}$ — the arrival law used on [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The Glosten–Milgrom Model]]. Conditioning on $I$ instead would give $\mathbb{P}(B\mid I)=1$, which is only correct in the degenerate $\theta=1$ case.)

**Probability that a buy came from an informed trader** (Bayes):

$$
\mathbb{P}(I\mid B)=\frac{\mathbb{P}(B\mid I)\,\pi}{\mathbb{P}(B)}=\frac{\pi\,\theta_{t-1}}{\pi\theta_{t-1}+\tfrac{1-\pi}{2}}=\boxed{\;\frac{2\pi\,\theta_{t-1}}{2\pi\,\theta_{t-1}+1-\pi}\;},
$$

which equals $\pi$ at the symmetric prior $\theta_{t-1}=\tfrac12$ and exceeds it only when $\theta_{t-1}>\tfrac12$. That is the right reading of the model: **at a symmetric prior a buy tells you about $V$, not about whether the trader was informed** ($\mathbb{P}(V_H\mid B)>\theta_{t-1}$ while $\mathbb{P}(I\mid B)=\pi$). The informed-ness becomes visible in the *streak*: after a run of buys the conditional $\theta$ rises, and a further buy is then genuinely more likely to be informed flow. At $\pi=0.1$ and $\theta=\tfrac12$: $\mathbb{P}(I\mid B)=0.100$; at $\theta=0.9$ it is $0.167$.

**Posterior belief that value is high** after observing a buy at prior $\theta_{t-1}$ (the GM update, repeated here explicitly):

$$
\theta_t=\mathbb{P}(V_H\mid B_t)
=\frac{\tfrac{1+\pi}{2}\,\theta_{t-1}}{\tfrac{1+\pi}{2}\theta_{t-1}+\tfrac{1-\pi}{2}(1-\theta_{t-1})}.
$$

For a *run* of $n$ buys the update compounds. A sequence of buys moves $\theta\to1$ (value-revealed as high), a sequence of sells moves it to $0$. The interesting, non-obvious content: the *speed* of learning is driven by $\pi$. Larger $\pi$ ⇒ each buy is more likely informed ⇒ posterior moves faster (Foucault Ch 3; Hasbrouck Ch 5).

---

### 3. Computational Implementation — type detection and streak diagnostics (stdlib only)

```python
def p_informed_given_buy(mu, theta):
    """P(informed | buy) with prior theta = P(V_H), informed fraction mu.
    An informed trader buys only in state V_H, so P(buy|I) = theta."""
    return 2.0 * mu * theta / (2.0 * mu * theta + 1.0 - mu)

def posterior_high(prior, mu, n_buys, n_sells):
    """Bayesian GM posterior after n_buys buys and n_sells sells, starting at prior theta."""
    th = prior
    for _ in range(n_buys):
        pbH, pbL = (1 + mu) / 2, (1 - mu) / 2
        th = pbH * th / (pbH * th + pbL * (1 - th))
    for _ in range(n_sells):
        psH, psL = (1 - mu) / 2, (1 + mu) / 2
        th = psH * th / (psH * th + psL * (1 - th))
    return th

print("--- P(informed | a Buy): function of informed fraction pi and prior theta ---")
print("    (= pi at theta=1/2: at a symmetric prior a buy informs you about V, not about I)")
for mu in (0.10, 0.25, 0.50):
    row = "  ".join(f"theta={t:.1f}: {p_informed_given_buy(mu, t):.4f}" for t in (0.20, 0.50, 0.90))
    print(f"  pi={mu:.2f}:  {row}")

print("\n--- a 1-buy vs a 10-buy streak: how fast the maker learns (pi = 0.10) ---")
print(f"  theta=0.50, after  1 buy : {posterior_high(0.5, 0.10, 1, 0):.4f}")
print(f"  theta=0.50, after  5 buys: {posterior_high(0.5, 0.10, 5, 0):.4f}")
print(f"  theta=0.50, after 10 buys: {posterior_high(0.5, 0.10, 10, 0):.4f}")
print(f"  theta=0.50, 1 buy then 5 sells (buy was noise/bi-directional): {posterior_high(0.5, 0.10, 1, 5):.4f}")
```

```text
--- P(informed | a Buy): function of informed fraction pi and prior theta ---
    (= pi at theta=1/2: at a symmetric prior a buy informs you about V, not about I)
  pi=0.10:  theta=0.2: 0.0426  theta=0.5: 0.1000  theta=0.9: 0.1667
  pi=0.25:  theta=0.2: 0.1176  theta=0.5: 0.2500  theta=0.9: 0.3750
  pi=0.50:  theta=0.2: 0.2857  theta=0.5: 0.5000  theta=0.9: 0.6429

--- a 1-buy vs a 10-buy streak: how fast the maker learns (pi = 0.10) ---
  theta=0.50, after  1 buy : 0.5500
  theta=0.50, after  5 buys: 0.7317
  theta=0.50, after 10 buys: 0.8815
  theta=0.50, 1 buy then 5 sells (buy was noise/bi-directional): 0.3095
```

Read the numbers as a toxicity screen: at $\pi=0.10$ a single buy barely moves the posterior ($0.50\to0.55$), but **ten consecutive buys push it to $0.88$** — you should now be quoting a heavily skewed book, not symmetric. Conversely a buy followed by five sells *over*-shoots the posterior *below* 0.5 ($\to0.31$) — classic back-and-forth noise. Directional persistence, not any single order, is what identifies information. This is the seed of order-flow-imbalance (OFI) and Volume-Synchronized probability of **toxicity** measures.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating each order as independent noise.** The toxic agent trades in one direction persistently. Averaging over "order flow is balanced" hides the local one-sidedness that is exactly the signal. Use run-lengths / imbalance windows, not per-order classification.
2. **Ignoring the base rate.** If insiders are genuinely rare ($\pi=0.01$), even a buy streak is weak. Over-flagging noise as toxicity gets you killed on opportunity cost; under-flagging gets you killed by the informed. The posterior quantifies the trade.
3. **Believing the market maker "can't see" the signal.** The *maker's* belief $\pi$ is what matters — $\pi$ is the maker's belief about informed probability, which updates with experience (Hasbrouck Ch 5: "the stock doesn't know that you own it"). A stale $\pi$ makes detection lag reality. The GM dynamics describe beliefs, not the true composition of traders.

---

### 5. Canonical Literature & Study References

- **Glosten & Milgrom (1985)**, JFE 14 (sequential Bayes; belief dynamics; martingale transaction prices).
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 5 §5.6 (price impact as signal extraction) and Ch 6 (PIN — the likelihood-based measure of informed-trading probability).
- **Easley, Kiefer & O'Hara (1997)**, *The information content of the trading process*, JFE 44 — the POISSON model of informed/uninformed arrivals behind PIN.
- **Foucault, Pagano & Röell (2013)**, *Market Liquidity*, Ch 3 §3.5 (price discovery $\mu_t=\theta_tV_H+(1-\theta_t)V_L$; convergence speed in $\pi$).

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/01-from-zero-intuition|01 · From Zero]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Index Hub]]
- Forward: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]] (the full quoting solver)
- Sibling: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/limit-order-book-mechanics|Order Flow & OFI]]
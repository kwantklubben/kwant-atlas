---
title: "6.4.5 Failure Modes & Real-World Practice"
tags:
  - pillar-market-making
  - failure-modes
  - winner-curse
  - spread-widening
  - toxic-flow
---

**Basic Prerequisites:** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]].

---

### 1. Intuition & Practical Objective

The GM/adverse-selection theory is mathematically clean and empirically dangerous in five specific ways. This page names them precisely so a market maker or student knows *which* assumption is biting and *how* it shows up in P&L. The objective is not cynicism — it is the discipline of knowing where the model is an approximation so the residual risk can be priced and cut.

The five failures, in one line each:

1. **The winner's curse.** You get filled *because* the order was adverse — every fill is a message that you are on the wrong side.
2. **Underestimated $\pi$ (informed fraction).** Quote a spread thinner than poison and you lose on *both* sides — the toxic one directly, and the healthy one you no longer cover.
3. **Spread widening as protection.** The GM logic predicts spreads expand as uncertainty grows (announcements, opens) — a maker who doesn't widen in time is a gift to insiders.
4. **Toxicity ≠ volatility.** Price *movement* is not the same as price *information*; flow that moves the efficient price permanently is the poison, and it needs a separate detector (VPIN etc.) — see [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]].
5. **Belief vs reality.** $\pi$ is the maker's *belief* about informed probability. It lags and can be wrong — and the model's machinery is exactly as good as that belief (Hasbrouck Ch 5: "the stock doesn't know that you own it").

---

### 2. Mathematical Ground Truth & Derivations

**The winner's curse quantified.** A competitive maker's *break-even* half-spread equals the adverse-selection half-spread. From the GM model at $\theta=\tfrac12$ the full spread is $\pi(V_H-V_L)$, hence the **break-even half-spread is $h^{\star}=\pi\,\frac{V_H-V_L}{2}$**. A maker who quotes a half-spread $h$ while the *true* informed fraction is $\pi$ earns

$$
\mathbb{E}[\text{P\&L per trade}]=h-\pi\tfrac{V_H-V_L}{2}\;\Longrightarrow\;\text{loss if } h<\pi\tfrac{V_H-V_L}{2}.
$$

With $V_H-V_L=2$ (a $\pm1$ move about the mid) this collapses to $\mathbb{E}[\text{P\&L}]=h-\pi$. **Underestimating $\pi$ by $0.2$ means giving up $0.2$ per share on every trade, permanently.** Because informed flow is one-sided, underestimating $\pi$ compounds: the maker keeps *seeing* adverse fills and (in the naive model) keeps quoting, so losses transfer linearly with trade count.

**The spread-widening rule.** At belief $\theta$, the ask-side adverse half-spread is (Foucault eq. 3.15)

$$
s_a^t=\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi\theta_{t-1}+(1-\pi)\tfrac12}\,(V_H-V_L),
$$

which is **maximized at $\theta=\tfrac12$** and vanishes toward $0/1$. So uncertainty *in the maker's belief* directly inflates the required spread — the mechanism behind pre-announcement and post-open widening. A maker quoting a flat spread through rising $\pi$ or rising uncertainty is systematically mispricing information.

---

### 3. Computational Implementation — the winner's curse in numbers (stdlib only)

Simulate the P&L of a maker who quotes a *fixed* half-spread $h$ against a stream whose true informed fraction is $\pi=0.30$ (break-even $h=0.30$): one maker quotes correctly, one underestimates ($h=0.10$), and one over-covers ($h=0.50$).

```python
import random

def maker_pl(n, true_mu, half_spread, seed=11, v_high=1.0, v_low=-1.0):
    random.seed(seed)
    pl = 0.0; mid = 0.0
    for _ in range(n):
        if random.random() < true_mu:                 # informed: trades toward the value
            value = v_high if random.random() < 0.5 else v_low
            if value > 0:  pl += (mid + half_spread) - value    # sell at ask, value -> +1
            else:          pl += value - (mid - half_spread)   # buy at bid,  value -> -1
        else:                                         # uninformed: donates the half-spread
            pl += half_spread
    return pl / n

print("true informed fraction pi = 0.30  (break-even half-spread = pi*(V_H-V_L)/2 = 0.30)")
for h, tag in ((0.30, "correct GM half-spread      (break-even)"),
               (0.10, "underestimated pi (h too thin) -> LOSES"),
               (0.50, "over-covered pi              (wins, but is quoted past)")):
    print(f"  h={h:.2f}  {tag}:  mean P&L/trade = {maker_pl(50000, 0.30, h):+.4f}")
```

```text
true informed fraction pi = 0.30  (break-even half-spread = pi*(V_H-V_L)/2 = 0.30)
  h=0.30  correct GM half-spread      (break-even):  mean P&L/trade = -0.0030
  h=0.10  underestimated pi (h too thin) -> LOSES:  mean P&L/trade = -0.2030
  h=0.50  over-covered pi              (wins, but is quoted past):  mean P&L/trade = +0.1970
```

The three solid numbers: correct $h$ is break-even ($\approx0$), the underestimating maker bleeds $-0.203$/trade (≈ $h-\pi=0.10-0.30=-0.20$), and the over-priced maker earns $+0.197$ but will be undercut by any competitor quoting the correct $h=0.30$. **This is the winner's curse in one experiment: the fill itself is the signal, and a spread thinner than the information cost is a guaranteed slow loss.** The free correction is to widen as $\pi$ and uncertainty rise — exactly what GM prescribes via the belief-dependent half-spread.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **The winner's curse is structural, not bad luck.** Every fill is conditional on you being *willing* to trade — and the informed side is the one that exploits that willingness. In GM terms the quotes are regret-free precisely so that no fill is, on average, a gift; a maker who deviates from the conditional-mean quotes invites exactly the adverse fills the model prices out.
2. **Underestimated informed fraction.** Too-thin spread $\Rightarrow$ linear, one-sided loss (the $-0.20$/trade above). Death by a thousand adverse fills. The theoretical ceiling is tightness; the practical ceiling is $\pi$ — and $\pi$ is a *belief*, so it must be re-estimated (see PIN/toxicity, bridges).
3. **Flat spreads through rising uncertainty.** The required half-spread rises with uncertainty/$\pi$; a flat quote through announcements, halts reopens, or earnings is a standing invitation to insiders. Widen (and thin back) in step with the belief $\theta$.
4. **Equating volatility with information.** A volatile-but-uninformed stock and a quiet-but-informed stock have entirely different spread requirements. Toxicity is the *permanent* price impact of the flow, not its variance — measure the permanent mark, not the bounce ([[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]], and [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]]).
5. **Belief lag.** $\pi$ and $\theta$ are beliefs, and beliefs update with experience. A maker who never updates (keeps $\pi$ from last year) quotes stale spreads into a market that has changed composition.

---

### 5. Canonical Literature & Study References

- **Glosten & Milgrom (1985)**, JFE 14 — the regret-free/zero-profit quote that prices the winner's curse (spread $=\pi(V_H-V_L)$ at $\theta=\tfrac12$).
- **Copeland & Galai (1983)**, J. Finance 38 — the "short a put and a call" view: the dealer's adverse-selection losses are option-like payoffs whose value rises with information uncertainty — i.e. why the spread must widen with uncertainty.
- **Hasbrouck (2007)**, Ch 5 (market-maker P&L/zero-profit; belief dynamics) and Ch 6 (PIN as the empirical estimate of the informed-arrival probability $\pi$).
- **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25 — the practical detector of toxic (permanent-impact) flow feeding directly off this model family. *(Primary PDF: `33Easley2012_flow_toxicity_and_liquidity_in`.pdf in corpus.)*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Index Hub]]
- Forward: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]
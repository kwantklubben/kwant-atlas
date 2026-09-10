---
title: "01 — Adverse Selection from Zero: Why the Spread Exists at All"
tags:
  - pillar-market-making
  - adverse-selection
  - intuition
  - bid-ask-spread
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of the bid-ask spread with **no prior microstructure knowledge needed**. The objective is one unshakeable idea: **even with zero exchange fees, zero inventory-carrying costs, and zero dealer monopoly power, a bid-ask spread must still exist — because the market maker risks trading against someone who knows more than they do.**

Start with the dumbest question: *why is a stock's ask higher than its bid?* Three candidate answers — (a) to pay exchange fees, (b) to compensate the maker for holding inventory overnight, (c) to exploit customers. All three fail to explain the spread in a liquid, near-frictionless, competitive market. The answer GM (1985) nailed is (d): **the maker's counterparty might be better informed than the maker.** When that happens the maker is systematically on the *wrong* side — buying right before a fall, selling right before a rise. The spread is collected from uninformed traders to pay for those unavoidable informed losses.

Three intuitions in increasing sophistication:

1. **The mid-price-only dealer goes bankrupt.** Quote a single price and buy/sell at it. Informed traders hurt you every single time; uninformed traders just shuffle cash around at no profit to you. Your P&L is pure negative — the liquidity you "facilitate" is a net transfer *out* of your books to the informed.
2. **The spread is a toll, not a fee.** It bounces you *out* of what the information costs. Thinner than the information cost and the maker loses; thicker and a competitor quotes past you. Competition pins the spread down to exactly the adverse-selection cost.
3. **The mid is not "the price."** The *efficient* price — what the maker believes the asset is worth given everything observed — is a *conditional* mean that moves with order flow. The quoted bid/ask straddle it asymmetrically (see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]]).

---

### 2. Mathematical Ground Truth & Derivations

Set up a one-round adverse-selection game. There is a single "true" but as-yet-unrevealed terminal value; it is $+1$ above the initial mid $m=100$ with probability $\tfrac12$ and $-1$ below it with probability $\tfrac12$. A trader arrives:

- **Informed** (prob $\pi$): knows the sign of the move and always trades in its direction (buys if up, sells if down).
- **Uninformed** (prob $1-\pi$): buys or sells with equal probability for liquidity; carries no information.

Suppose the dealer trades at the **mid** with no spread. If the informed trader buys (value about to be $101$), the dealer sells at $100$ and immediately loses $1$ per share; symmetric loss on informed sells. Uninformed trades transact at fair value and break the dealer even. So the **expected loss per trade at zero spread is $\pi$** (per unit of the move): the dealer who quotes no spread loses money in direct proportion to the informed fraction. Let the half-spread be $h$, i.e. ask $=100+h$, bid $=100-h$. Then:

- informed buy: dealer sells at $100+h$ but the share is worth $101$ → P&L $= h-1$;
- informed sell: dealer buys at $100-h$ but the share is worth $99$ → P&L $= h-1$;
- uninformed (either direction): dealer banks the half-spread $h$.

Expected P&L per trade:

$$\mathbb{E}[\text{P&L}]= \pi(h-1)+(1-\pi)h = h-\pi .$$

**Zero-expected-profit quote:** set $\mathbb{E}[\text{P&L}]=0\Longrightarrow \boxed{\,h^{\star}=\pi\,}$ — the required half-spread equals the informed probability. This is the *discrete, no-friction* seed of the Glosten–Milgrom result. The full symmetric GM formula $A-B=\pi(V_H-V_L)$ (with $V_H-V_L=2$) is exactly this "$h^\star=\pi$" written against the value dispersion.

---

### 3. Computational Implementation — the dealer who quotes the mid loses; the GM-dealer breaks even

Stdlib only. We simulate thousands of trades against a dealer who (a) quotes no spread (mid only) and (b) quotes the break-even half-spread $h=\pi$ of GM.

```python
import random

def dealer_pl(n, mu, half_spread, seed=7):
    random.seed(seed)
    pl = 0.0
    for _ in range(n):
        move = 1.0 if random.random() < 0.5 else -1.0   # true value will move +1 or -1
        informed = random.random() < mu
        mid = 100.0
        if informed:
            if move == 1.0:      # informed buys -> dealer sells at ask, value -> 101
                pl += (mid + half_spread) - (mid + move)
            else:                # informed sells -> dealer buys at bid, value -> 99
                pl += (mid + move) - (mid - half_spread)
        else:                    # uninformed: pay the half-spread either way, no information
            pl += half_spread
    return pl / n

print("mu = 0.30  (break-even half-spread per GM = mu = 0.30)")
for h, tag in ((0.0, "zero spread (mid only)      -> guaranteed loss"),
               (0.3, "half-spread = mu (GM quote) -> break-even / zero-profit")):
    print(f"  h={h:.2f}  {tag}:  mean P&L per trade = {dealer_pl(20000, 0.30, h):+.4f}")
```

```text
mu = 0.30  (break-even half-spread per GM = mu = 0.30)
  h=0.00  zero spread (mid only)      -> guaranteed loss:  mean P&L per trade = -0.3009
  h=0.30  half-spread = mu (GM quote) -> break-even / zero-profit:  mean P&L per trade = -0.0009
```

Two solid numbers from the run: quoting the **mid** costs the dealer $0.301$ per trade (matches $-\pi=-0.30$ to Monte-Carlo error), and quoting the **GM half-spread** brings P&L to $\approx 0$ (the noise band around the theoretical $0$). The spread is not a fee for services rendered — it is *insurance against information*.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "markets are efficient so orders carry no news" trap.** Roll's model and naive quoting assume trades are uninformative. GM's whole point is they are not — the moment you quote the mid you assume $\pi=0$ and bleed. This is why normal-distribution, frictionless "mid execution" cost models misprice liquidity for illiquid/information-heavy names (see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|05 · Failure Modes]]).
2. **Confusing the *spread* with the *price.*** The midpoint is *not* the efficient price except at maximal uncertainty. A dealer who thinks the mid is "fair value" is pricing the asset as if orders were noise, i.e. exactly the assumption that makes them a target.
3. **The half-spread is not a free parameter.** It is pinned by the *informed* fraction, not by what the dealer *wants* to earn. Competing makers who can quote the same value dispersion at the same information risk will undercut any thicker spread.

---

### 5. Canonical Literature & Study References

- **Glosten & Milgrom (1985)**, *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*, JFE 14(1), 71–100 — the sequential-trade model whose symmetric spread is $A-B=\pi(V_H-V_L)$.
- **Copeland & Galai (1983)**, *Information effects on the bid-ask spread*, J. Finance 38(5), 1457–1469 — the "dealer is short a put and a call" option framing of the same idea.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 5 — the verified statement of the GM model (δ/µ notation, eq. 5.1–5.7, spread formula, wealth-transfer identity).

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/bayesian-statistics/index|Bayesian Statistics]]
- Continue: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/02-informed-vs-uninformed|02 · Informed vs Uninformed]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Index Hub]]
- Sibling: [[pillars/06-market-making/limit-order-book-mechanics-and-l3|Limit Order Book Mechanics]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow]]
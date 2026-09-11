---
title: "6.9.5 Failure Modes & Practice"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - failure-modes
  - rebate-distortion
  - inventory-risk
---

**Basic Prerequisites:** [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]] and [[pillars/06-market-making/market-maker-economics-and-rebates/04-competition-and-the-race-to-zero|04 · Competition & the Race to Zero]].

---

### 1. Intuition & Practical Objective

Every market-making desk in the world is a version of the same bet: **capture the spread faster than you get picked off and before your inventory kills you.** The economics is clean paper; the P&L is decided by five specific ways the paper breaks. This page names them for a desk manager and a student alike, so that each failure is recognisable *before* it shows up as a drawdown.

The five ways a market-making desk dies:

1. **Rebate-driven distortion** — you keep quoting to earn the rebate after your true edge has gone negative; the subsidy *masks* the loss.
2. **Competition eroding the edge** — $N\to N^\star$ compresses your per-share profit toward zero; the survivor is whoever has the lowest fixed cost.
3. **Inventory blowups** — one-sided (informed) flow turns inventory into a trending, levered position that breaches financing limits.
4. **Adverse selection mis-estimated** — the maker quotes to the wrong $\lambda$ and the winner's curse compounds.
5. **Fixed-cost escalation** — message-rate data fees and latency spend grow while fills-per-quote fall, moving $N^\star$ against you.

> **The one-sentence essence.** "A rebate can keep a losing maker quoting, a thicket of competitors can erode a winning one to zero, and a one-sided fill burst can turn a hedged book into an unhedged bet — in that order of subtlety."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Rebate-driven distortion: the rebate *buys tolerance for toxicity*

Use the Glosten–Milgrom per-trade result (see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|GM — 05]]): with $V_H-V_L=2$ (a $\pm1$ move about the mid), the expected adverse-selection cost per trade is $\pi$, the informed fraction. Adding the rebate, the maker's per-trade P&L is
$$
\mathbb{E}[\pi_{\text{trade}}] = h + r - \pi.
$$
Break-even informs the **toxicity tolerance**:
$$
\boxed{\;\pi^{\star} = h + r.\;}
$$
A rebate of $r$ raises the toxicity the maker can survive by exactly $r$:
$$
\Delta\pi^{\star} = r.
$$

**This is the failure.** The rebate does not make a bad market good; it makes a bad maker *survive longer* in a market he should leave. A maker who *should* exit at $\pi>\pi^\star$ instead keeps quoting, bleeding $r$ per trade less than he otherwise would — the loss is *masked*, not removed. Regulators reading "rebates improve liquidity" must ask whether the additional liquidity is good or merely *persistent*.

#### 2.2 Inventory blowups: the random walk with a levered boundary

Inventory $q_t$ accumulates fill-by-fill. Under balanced flow it is a **zero-drift random walk**: $\mathbb{E}[q_t]=0$, $\text{sd}(q_t)\propto\sqrt{t}$. Under *informed* one-sided flow it acquires a **drift**: $q_t \approx (2p-1)\,t$ where $p$ is the buy-probability. The maker's loss from carrying inventory scales with the **variance** of the terminal mark,
$$
\text{inventory P\&L} \;\sim\; -\tfrac12\,\gamma_{\text{risk}}\,\sigma^2 q^2,
$$
which is **quadratic in $q$** (the Avellaneda–Stoikov penalty). A blowup is therefore a *self-accelerating* process: the more one-sided the flow, the larger $|q|$, the larger the required reserve, the more leverage — until a financing or risk-limit boundary is breached. Hasbrouck (2007) Ch 11 notes the ruin channel is precisely this **levered inventory + credit withdrawal** (Brunnermeier–Pedersen 2005), not the spread.

#### 2.3 Edge erosion and cost escalation

From Page 04, $\pi_N = eQ/N - C$. Two degradations act simultaneously:

- $N$ rises (more competitors enter), dividing $Q$.
- $C$ rises (message-rate data fees, latency hardware), so each entrant needs more edge to justify staying.

Combined, the *survivable* edge rises while the *achievable* edge falls — the two curves cross, and that crossing is the exit of the marginal desk.

---

### 3. Computational Implementation — the failure modes in numbers

Standard library only. Part 1 shows the rebate raising the toxicity tolerance and **masking** a genuine loss. Part 2 shows inventory under balanced vs. toxic flow.

```python
# ---- Part 1: the rebate raises toxicity tolerance (and masks a losing desk) ----
h = 0.010                     # half-spread, V_H - V_L = 2 so AS cost per trade = pi
pi_true = 0.014               # true informed fraction of the flow
print(f"true toxicity pi = {pi_true:.4f}")
for r in (0.000, 0.002, 0.004):
    pi_star = h + r                                   # break-even toxicity
    pl      = h + r - pi_true                         # realised P&L per trade
    tag = "LOSES" if pl < 0 else ("break-even" if abs(pl) < 1e-12 else "wins")
    print(f"  rebate {r:.3f} -> tolerance pi* = {pi_star:.4f}   "
          f"P&L/trade = {pl:+.4f}  [{tag}]")

# ---- Part 2: inventory random walk — balanced vs one-sided (toxic) flow ----
import random

def inventory_path(n, p_buy, seed=7):
    random.seed(seed)
    inv = 0; peak = 0; terminal = 0
    for _ in range(n):
        inv += 1 if random.random() < p_buy else -1
        peak = max(peak, abs(inv)); terminal = inv
    return terminal, peak

print("\ninventory after 10,000 fills:")
for p, label in ((0.50, "balanced flow"), (0.65, "toxic one-sided flow")):
    term, peak = inventory_path(10000, p, seed=7)
    print(f"  {label:22s} p_buy={p:.2f}  terminal q={term:6d}  peak |q|={peak:6d}")
```

```text
true toxicity pi = 0.0140
  rebate 0.000 -> tolerance pi* = 0.0100   P&L/trade = -0.0040  [LOSES]
  rebate 0.002 -> tolerance pi* = 0.0120   P&L/trade = -0.0020  [LOSES]
  rebate 0.004 -> tolerance pi* = 0.0140   P&L/trade = +0.0000  [break-even]

inventory after 10,000 fills:
  balanced flow          p_buy=0.50  terminal q=    60  peak |q|=   150
  toxic one-sided flow   p_buy=0.65  terminal q=  3002  peak |q|=  3002
```

**Three solid results.**

- The rebate raises the toxicity the desk tolerates **one-for-one** with $r$: $\pi^\star = 0.0100 \to 0.0120 \to 0.0140$. At $r=0.004$ the desk *looks* break-even — but it is quoting into a market it cannot beat; the rebate has converted a $-0.004$/trade loss into a $0.000$ line. **The subsidy masked the failure; it did not fix it.**
- Inventory under balanced flow stays **bounded** ($|q|\le150$ over $10{,}000$ fills, growing like $\sqrt{t}$), while a shift to $p=0.65$ produces a **terminal inventory of $3002$** — a **20×** larger position at the risk limit, purely from flow composition, not from the spread.
- Because the inventory penalty goes as $q^2$, the toxic case's risk charge is roughly $20^2=400$× the balanced case's. This is a *leverage* failure, and it is the one that ends desks.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The rebate masks, it does not cure.** $r$ shifts the break-even toxicity $\pi^\star=h+r$ rightward. A desk that survives on the rebate is a desk that has been *made persistent*, not *made good*. Cutting the rebate reveals the loss instantly (the $+0.0000\to-0.0040$ jump above).
2. **Inventory blowups are flow-composition events, not price events.** The $3002$-share toxic-book inventory above was generated with the *same* price process as the balanced case; only the fill *direction bias* changed. Risk systems that monitor volatility but not **order-flow imbalance** (see [[pillars/06-market-making/limit-order-book-mechanics|Order Flow Imbalance]]) are blind to the actual trigger.
3. **Quadratic inventory risk is invisible in linear TCA.** A per-share inventory cost of $0.001$ looks harmless; the true $\tfrac12\gamma\sigma^2q^2$ charge is what breaches limits. Always reconcile the linearised $c_{\text{inv}}$ against the convex penalty at the 99th percentile of $|q|$.
4. **Edge erosion is silent and continuous.** No single day shows a collapse; $e\to0$ over months as entrants arrive and costs rise. The desk discovers it only when the quarterly rebate-tier true-up reveals it was paying to trade.
5. **Adverse selection clustering.** Informed flow arrives in bursts, so $\lambda$ is *autocorrelated*, not i.i.d. A maker who sizes reserve against the *average* $\lambda$ will have exactly the wrong amount of capital precisely when it is needed (VPIN, [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow]]).

---

### 5. Canonical Literature & Study References

- **Glosten & Milgrom (1985)**, JFE 14 — the $\pi$ toxicity structure behind $\pi^\star = h+r$.
- **Hasbrouck (2007)**, Ch 11 (inventory/ruin and the levered-inventory channel; Brunnermeier–Pedersen 2005 reference) and Ch 5 (the winner's curse). *Verified in corpus.*
- **Menkveld (2013)**, JFM 16(4) — inventory costs as a first-order term in a real HFT maker's P&L.
- **Malinova & Park (2015)**, JF 70(2) — empirical evidence that maker rebates change *behaviour* (order aggressiveness, adverse-selection costs) without necessarily changing cum-fee costs.
- **Brunnermeier & Pedersen (2009)**, *Market liquidity and funding liquidity*, RFS 22(6) — the leverage/funding channel of inventory blowups.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-maker-economics-and-rebates/04-competition-and-the-race-to-zero|04 · Competition & the Race to Zero]]
- Forward: [[pillars/06-market-making/market-maker-economics-and-rebates/06-advanced-extensions|06 · Advanced Extensions]]
- Siblings: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|GM — 05 · Failure Modes]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]
- Hub: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Index Hub]]

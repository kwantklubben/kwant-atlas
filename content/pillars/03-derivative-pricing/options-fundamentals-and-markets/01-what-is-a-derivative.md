---
title: "01 — What Is a Derivative? From Zero"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - intuition
  - forwards
  - no-prior-knowledge
---

**Basic Prerequisites:** None — high-school algebra only. This is the most accessible page in Pillar 3.

---

### 1. Intuition & Practical Objective

This page answers one question with **no derivatives knowledge assumed**: *what actually is a derivative, and why does it have a price?* The objective is the mental picture — a derivative is a **contract that pays a specified function of some other price**, and the only reason its price is knowable is that you can **manufacture that function yourself** out of traded assets.

Start from the dumbest possible question. A stock has a price because it is a claim on future cash flows. A *derivative* has no cash flows of its own — a forward contract on gold literally promises "at time $T$ I pay you $S_T-K$ and nothing happens until then." So why isn't it worth zero? Because buying the contract and then holding the right inventory is the **same thing** as buying the inventory now. If you want the gold today, you can buy it outright for $S_0$; if you instead buy a forward and put $S_0$ in the bank, you get the gold at $T$ for a *known* cost. The two routes must cost the same, or money is free. That is the entire field in one paragraph.

**The three shapes, in words:**

1. **Forward / futures — a *symmetric* promise.** Both sides are obliged to trade at $K$. Long receives $S_T-K$, short receives $K-S_T$. One wins exactly what the other loses. It costs nothing to enter, because an at-market forward has zero expected value *and* zero initial cash flow.
2. **Option — an *asymmetric* right.** The buyer *may* trade at $K$; the seller *must* if asked. Because the buyer's downside is truncated at (premium), and the seller bears the tail, the buyer pays an **up-front premium**. This asymmetry is the entire reason option pricing is hard and forward pricing is easy.
3. **Swap — a *strip* of forwards.** Two parties exchange a fixed cash flow for a floating one, period after period. Nothing new is needed to value it; it is just many forwards glued together.

> **The one-sentence essence.** "A derivative is a contract; its price is the cost of the cheapest portfolio of traded assets that pays exactly the same thing — and because that cost does not depend on anyone's forecast, the derivative trades at it."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Forward payoffs (Hull Ch 1.3)

Entering a forward costs nothing, so its **payoff *is* its profit and loss**:

$$\text{long forward: }S_T-K,\qquad \text{short forward: }K-S_T.$$

Compare with an option, where the buyer pays a premium $c$ up front:

$$\text{long call net P\&L: }\max(S_T-K,0)-c .$$

The $\max(\cdot,0)$ is the **kink** that makes options non-linear. A forward payoff is a straight line through zero; a call payoff is flat at zero and then a $45°$ line. Everything interesting follows from that kink.

#### 2.2 Why the forward price is $S_0e^{rT}$ (Hull eq. 5.1)

Suppose a non-dividend stock trades at $S_0$, the risk-free rate is $r$, and the forward delivers in $T$ years. Consider two strategies:

- **Cash-and-carry:** borrow $S_0$, buy the stock, hold it, sell it forward at $F_0$.
- **Do nothing (and settle the forward at market).**

The cash-and-carry strategy costs $0$ today and pays $S_T-F_0$ at time $T$ after repaying $S_0e^{rT}$. For no arbitrage the terminal payoff must be zero:

$$\boxed{\,F_0=S_0e^{rT}\,}\qquad\text{(no income; Hull eq. 5.1)}.$$

So the forward price is *not a forecast* — it is the **cost of carrying** the asset to $T$. If it trades anywhere else, the difference is a free lunch (the reverse cash-and-carry, or a short sale for the other direction).

#### 2.3 The value of a forward *after* it is struck (Hull eq. 5.4/5.5)

Once the market moves, an old forward becomes an asset or a liability. The standard argument: contract to buy at $K$ today is equivalent to entering a *new* forward at $F_0$ **plus** the certainty of receiving $F_0-K$, so

$$f=(F_0-K)e^{-rT}\;=\;S_0-Ke^{-rT}\quad\text{(no income)}.$$

This is the whole use of forwards in hedging: the contract's mark-to-market is the present value of the price move, *not* the price move itself. (For a **futures** contract the same total accrues, but it arrives in **daily instalments** — Hull Ch 2 — because futures are marked to market every day.)

#### 2.4 The asymmetry that creates the option premium

$$
\begin{aligned}
\text{forward long: } & S_T-K &&\text{(can go arbitrarily negative)}\\
\text{call long: } & \max(S_T-K,0)-c &&\text{(floor at } -c)\\
\text{put long: } & \max(K-S_T,0)-c &&\text{(floor at } -c)
\end{aligned}
$$

Truncating the loss transfers the left tail from buyer to seller. That transfer has value, and that value **is** the option price. Put–call parity (§ next folder page) will make this razor-sharp: a call plus a discounted strike is *identical* to a put plus the stock, so the two premiums are linked by the same no-arbitrage force that gave $F_0=S_0e^{rT}$.

---

### 3. Computational Implementation — payoffs are the whole story

Standard library only. This runs the three ideas above: the symmetric forward payoff, the fair forward price, the marked-to-market value of an old forward, and the truncated option payoff.

```python
import math
K = 63.0
print("Forward (entered at K=63, cost 0 -> payoff IS the P&L):  Hull Ch1 Sec 1.3")
for ST in (55.0, 63.0, 71.0):
    print(f"  S_T={ST:5.1f}:  long = S_T-K = {ST-K:+6.2f}   short = K-S_T = {K-ST:+6.2f}")
S0, r, T = 60.0, 0.05, 1.0
print(f"  no-arbitrage forward price F0 = S0 e^(rT) = {S0*math.exp(r*T):.4f}   [Hull eq 5.1; Ch1 preview ~$63]")
S1, T1 = 66.0, 0.5
print(f"  value of that long forward later (S={S1}, 0.5y left): f = S - K e^-rT = {S1 - K*math.exp(-r*T1):.4f}   [Hull eq 5.5]")
print("Option (right, not obligation; premium up front):")
prem = 3.0
for ST in (55.0, 66.0, 71.0):
    print(f"  S_T={ST:5.1f}:  long call (X=66) net P&L = max(S_T-X,0) - prem = {max(ST-66.0,0.0)-prem:+6.2f}")
```
```
Forward (entered at K=63, cost 0 -> payoff IS the P&L):  Hull Ch1 Sec 1.3
  S_T= 55.0:  long = S_T-K =  -8.00   short = K-S_T =  +8.00
  S_T= 63.0:  long = S_T-K =  +0.00   short = K-S_T =  +0.00
  S_T= 71.0:  long = S_T-K =  +8.00   short = K-S_T =  -8.00
  no-arbitrage forward price F0 = S0 e^(rT) = 63.0763   [Hull eq 5.1; Ch1 preview ~$63]
  value of that long forward later (S=66.0, 0.5y left): f = S - K e^-rT = 4.5555   [Hull eq 5.5]
Option (right, not obligation; premium up front):
  S_T= 55.0:  long call (X=66) net P&L = max(S_T-X,0) - prem =  -3.00
  S_T= 66.0:  long call (X=66) net P&L = max(S_T-X,0) - prem =  -3.00
  S_T= 71.0:  long call (X=66) net P&L = max(S_T-X,0) - prem =  +2.00
```
Read the last three lines: the **forward** loses $8$ when $S_T=55$; the **call** loses only the $3$ premium. That truncation is what the buyer pays for. Notice also that the forward's fair price $63.0763$ comes *entirely* from the carry cost $S_0e^{rT}$, with no view on gold at all.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"A derivative is a bet on direction."** A forward is *not* a view — it is a contract priced off the carry, and its value is a present value. Two traders with opposite forecasts agree on $F_0$. If you find yourself pricing a forward with a forecast, stop.
2. **Treating the payoff as the value.** A forward entered *at* $K=F_0$ has zero value, but a forward struck at $K\ne F_0$ has value $(F_0-K)e^{-rT}$. Discounting the payoff is mandatory; the "payoff = P&L" shortcut applies only because entry cost is zero and settlement is at $T$.
3. **Forgetting the daily settlement.** For a *futures* contract the same total gain accrues, but in daily cash flows — and those flows earn or cost interest. This is why futures and forward prices differ when rates are stochastic (Hull §5.8, and the convexity adjustment in Hull Ch 6).
4. **Assuming option and forward obligations are symmetric.** A short *option* has unbounded loss potential; a short *forward*'s loss is linear in $S_T$. The margin and risk treatment of the two is fundamentally different (Hull Ch 2 vs Ch 10.7).
5. **Ignoring income.** A dividend-paying stock or an index changes the forward to $F_0=S_0e^{(r-q)T}$; a foreign currency to $S_0e^{(r-r_f)T}$. Using $S_0e^{rT}$ for all of them is the single most common beginner error and the first item on the failure checklist in [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 1 §1.1–1.4 (forward payoff $S_T-K$, call/put rights, trader taxonomy) and Ch 5 §5.1–5.7 (cash-and-carry, $F_0=S_0e^{rT}$, forward value $f=(F_0-K)e^{-rT}$). *Verification report in the corpus.*
- **Shreve**, *Stochastic Calculus for Finance I*, §1.1 (the discrete version of exactly this replication argument: $d<1+r<u$, delta, risk-neutral $\tilde p$). *Math-verified.*
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1.1–1.2 (the cost-of-carry dictionary and the generalized formula this forward price feeds into).

---

### 6. Connected Graph Bridges

- Next: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/02-options-mechanics-and-payoffs|02 · Options Mechanics & Payoffs]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Index Hub]]
- Forward topic-page: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]] (the discrete seed of this replication idea)
- Sibling topic-folders: [[pillars/03-derivative-pricing/black-scholes-merton|Black-Scholes-Merton]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure|Interest Rate & Term Structure]] (forwards on rates, FRAs and swaps)

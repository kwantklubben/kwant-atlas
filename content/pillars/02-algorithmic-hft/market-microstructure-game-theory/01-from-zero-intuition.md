---
title: "01 - From Zero: Markets Are Games Between Makers, Informed and Noise"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - game-theory
  - adverse-selection
  - intuition
  - spread
---

**Basic Prerequisites:** None. (For the market-making view of the same game, [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]].)

---

### 1. Intuition & Practical Objective

Watch a single trade for ten seconds. A market maker has a two-sided quote posted: **bid 99.80 / ask 100.20**. Someone lifts the offer. The maker has just sold at 100.20 a share that — unknown to the maker — is worth 101.00. Was the buyer a pension fund rebalancing, or someone who knows something? The maker **cannot tell**. That single fact of ignorance is the entire origin of the bid–ask spread, and it is a *game*, not an accounting identity.

There are exactly three kinds of players, and their interests are opposed:

1. **The informed trader.** Knows (or has an edge on) the value. Wants to trade as much as possible *before* the price adjusts. If she buys when the value is high, the maker loses.
2. **The noise trader.** Trades for reasons unrelated to value — cash flow, index rebalancing, a tax bill. Loses on average; this is the maker's revenue.
3. **The market maker.** Quotes *conditionally*. She cannot ask "are you informed?", so she prices the average of who *does* trade at each side. **The ask is the expected value conditional on someone choosing to buy. The bid is the expected value conditional on someone choosing to sell.** The gap is the toll that makes her whole.

Read that last sentence again, because it inverts the usual framing. Most people think of the spread as a *cost* that theory then has to justify. Game-theoretic microstructure says the spread **is** the equilibrium price of a specific adverse-selection exposure — it is set by the composition of the flow, and if the composition changes, the spread changes with it.

The practical objective of this page is to build three intuitions with no prior mathematics:

- **Adverse selection is a tax on being uninformed on the other side.** The more probable it is that your counterparty knows something, the wider the price you must be offered.
- **A maker who ignores it does not "do slightly worse" — she bleeds at a known, computable rate.** Quoting the mid at $\pi=0.20$ loses **\$0.200 per share, every trade, forever** (§3).
- **The spread is state-dependent.** It depends on what the maker currently believes. Near maximum uncertainty it is widest; when the maker is nearly certain of the value it collapses toward zero. A *constant* spread cannot be an equilibrium.

> **The one-sentence essence.** "The maker sets the ask to the expected value given that someone bought and the bid to the expected value given that someone sold, so the spread is the market-clearing price of the maker's ignorance — and it widens and narrows with the flow."

---

### 2. Mathematical Ground Truth & Derivations

We need the smallest model that contains the game. Two possible values, one type of informed trader, one type of noise trader.

**Setup.** $V\in\{V_L,V_H\}$ with $V_L<V_H$; the maker's prior is $\theta=\mathbb{P}(V=V_H)$. A trader arrives. With probability $\pi$ it is an **informed** trader who buys iff $V=V_H$ and sells iff $V=V_L$. With probability $1-\pi$ it is a **noise** trader who buys or sells with probability $\tfrac12$ each, independent of $V$. Therefore the *buy-arrival laws* are

$$
\mathbb{P}(B\mid V_H)=\pi\cdot 1+(1-\pi)\cdot\tfrac12=\frac{1+\pi}{2},\qquad \mathbb{P}(B\mid V_L)=\pi\cdot 0+(1-\pi)\cdot\tfrac12=\frac{1-\pi}{2}.
$$

**The maker's problem.** She posts quotes before seeing the trader. By Bayes' rule the break-even (zero-expected-profit) quotes are conditional expectations:

$$
A=\mathbb{E}[V\mid B]=\frac{V_H(1+\pi)\theta+V_L(1-\pi)(1-\theta)}{(1+\pi)\theta+(1-\pi)(1-\theta)},\qquad B=\mathbb{E}[V\mid S]=\frac{V_H(1-\pi)\theta+V_L(1+\pi)(1-\theta)}{(1-\pi)\theta+(1+\pi)(1-\theta)}.
$$

At $\theta=\tfrac12$ each denominator is 1 and the spread collapses to the textbook form

$$
\boxed{\;A-B=\pi\,(V_H-V_L)\;}
$$

so the spread is **linear in the informed share and in the value range** — no fudge factors, no inventory, no fixed-cost story. It is purely the price of ignorance.

**Why a mid-quoting maker loses.** Put $p_0=\tfrac12(V_H+V_L)$. A maker who quotes $p_0$ on both sides sells on buy-arrivals and buys on sell-arrivals, earning
$$
\mathbb{E}[\text{P\&L}\mid B]=p_0-A,\qquad \mathbb{E}[\text{P\&L}\mid S]=B-p_0,
$$
and since buy- and sell-arrivals each occur with probability $\tfrac12$,
$$
\mathbb{E}[\text{P\&L}]=\tfrac12\big[(p_0-A)+(B-p_0)\big]=\tfrac12\big[B-A\big]=-\tfrac12\,\pi(V_H-V_L).
$$
**A mid-quoting maker loses exactly half the equilibrium spread per trade.** Verified numerically below at every $\pi$.

**Why the quotes must be state-dependent.** $A$ and $B$ depend on $\theta$, and $\theta$ changes after every trade. The spread is *widest at maximum uncertainty and vanishes at the extremes* — because near $\theta\to1$ both sides of the book converge on $V_H$ and there is nothing left to be selected on. A constant spread equal to the average of $A(\theta)-B(\theta)$ is therefore **wrong on every single trade**, even though it is right on average.

**The martingale property (the punchline).** Because $A$ and $B$ are conditional expectations,
$$
\mathbb{E}[P_{t+1}\mid\mathcal{F}_t]=\mathbb{P}(B\mid\mathcal{F}_t)\,A_t+\mathbb{P}(S\mid\mathcal{F}_t)\,B_t=P_t.
$$
**The quoted price is a martingale.** Prices are unpredictable *by construction* — not as an empirical accident, but because the maker's quotes are Bayesian. This is the single most important structural consequence of putting the game first, and it is what every "impact" and "alpha" conversation downstream is really arguing about.

---

### 3. Computational Implementation — the adverse-selection game in numbers

Stdlib only. The table gives the full game for a range of informed shares: the equilibrium quotes, the spread, the loss a mid-quoting maker suffers, the posterior after a buy, and the toxicity of a fill. All numbers re-executed.

```python
import math
VH, VL, p0 = 101.0, 99.0, 100.0
print("A market maker against informed + noise traders (VH=101, VL=99, prior theta=1/2)")
print(f"{'pi':>5} {'ask':>8} {'bid':>8} {'GM spread':>10} {'pnl @mid':>9} {'theta+':>7} {'P(inf|buy)':>11}")
for pi in (0.0, 0.05, 0.10, 0.20, 0.40, 0.50):
    A = 0.5*(VH*(1+pi)+VL*(1-pi)); B = 0.5*(VH*(1-pi)+VL*(1+pi))
    nA = (1+pi)*0.5 + (1-pi)*0.5
    pnl_mid = 0.5*((p0-A) + (B-p0))          # quote the mid on both sides
    print(f"{pi:5.2f} {A:8.3f} {B:8.3f} {A-B:10.3f} {pnl_mid:9.3f} {(1+pi)*0.5/nA:7.4f} {2*pi*0.5/nA:11.4f}")
print(f"spread = pi*(VH-VL) at theta=1/2;  pi=0.2 -> {0.2*(VH-VL):.3f}")
print("A maker that quotes the mid loses exactly half the GM spread on every trade.")
```
```
A market maker against informed + noise traders (VH=101, VL=99, prior theta=1/2)
   pi      ask      bid  GM spread  pnl @mid  theta+  P(inf|buy)
 0.00  100.000  100.000      0.000     0.000  0.5000      0.0000
 0.05  100.050   99.950      0.100    -0.050  0.5250      0.0500
 0.10  100.100   99.900      0.200    -0.100  0.5500      0.1000
 0.20  100.200   99.800      0.400    -0.200  0.6000      0.2000
 0.40  100.400   99.600      0.800    -0.400  0.7000      0.4000
 0.50  100.500   99.500      1.000    -0.500  0.7500      0.5000
spread = pi*(VH-VL) at theta=1/2;  pi=0.2 -> 0.400
A maker that quotes the mid loses exactly half the GM spread on every trade.
```

Read the columns together. The spread is **exactly** $\pi(V_H-V_L)$ ($0.400$ at $\pi=0.20$). The mid-quoter's loss is **exactly** $-\tfrac12$ of it ($-0.200$). `theta+` is the posterior the maker holds after being bought from ($0.6000$ from a $0.5000$ prior) — the mechanical reason the *next* trade is quoted off a different spread. And `P(inf|buy)` is the answer to the question every execution trader actually cares about: **given that I just traded, what was the chance I was picked off?** At maximum uncertainty it equals the informed share $\pi$; away from $\theta=\tfrac12$ it does not (see page 05).

Notice what is *absent*: no inventory cost, no order-processing cost, no fixed fee. The spread here is 100% adverse selection, and it already reproduces the qualitative behaviour of real quotes.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The spread compensates inventory risk."** Half right and dangerously half wrong. This model has **no inventory** at all and still produces a spread. Inventory is a second, additive source; conflating them makes you miscalibrate both. See [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]] for the pure-inventory half.
2. **"π is a constant I can look up."** $\pi$ is not observable; it is estimated, and it drifts with news, time of day and volatility. Because the equilibrium spread is *linear* in $\pi$, a 2x error in $\pi$ is a 2x error in the fair spread — and the maker's P&L error is first-order, not second-order.
3. **The two-point value is a fiction.** Real values are continuous, so there is no $V_H-V_L$ to plug in. The continuous-value generalisation (Kyle, page 02) replaces $\pi(V_H-V_L)$ with $\lambda\cdot(\text{order flow})$, and the spread with a linear price rule — a different object with the same economics.
4. **One trade at a time is a fiction too.** Real markets have simultaneous, competing liquidity. Competitive entry of makers drives the spread to the zero-profit level *only if* entry is free — with finite maker capital the equilibrium spread can sit above it. That is a genuinely different game with a different answer.
5. **The martingale conclusion is a *modelling* statement, not a forecasting one.** $P_t$ is a martingale *in the maker's information set*. To a trader with better information, or to a trader who can see the order book, it is emphatically not.

---

### 5. Canonical Literature & Study References

- **Glosten, Lawrence R.; Milgrom, Paul R.** — "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders," *Journal of Financial Economics* 14(1), 71–100 (1985). *The origin of everything on this page; the zero-profit conditional-expectation quotes are theirs.*
- **Copeland, Thomas E.; Galai, Dan** — "Information effects on the bid-ask spread," *Journal of Finance* 38(5), 1457–1469 (1983). *The contemporaneous, independent derivation of the same adverse-selection spread.*
- **Kyle, Albert S.** — "Continuous auctions and insider trading," *Econometrica* 53(6), 1315–1335 (1985). *The continuous-value counterpart; see page 02.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 5. *The textbook development of the Bayesian specialist; corpus verification `hasbrouck_ch1-5.md`.*
- **Foucault, Thierry; Pagano, Marco; Röell, Ailsa** — *Market Liquidity: Theory, Evidence, and Policy* (2013), Ch 3. *Corpus verification `foucault_ch1-3.md`; the cleanest treatment of "who loses and who gains".*

---

### 6. Connected Graph Bridges

- The game in full: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & the Glosten–Milgrom Model]] (the sequential-trade recursion in depth)
- The continuous-value version: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/02-the-kyle-model-and-back-limit|02 - Kyle & the Back Limit]]
- The Bayesian machinery: [[foundations/bayesian-statistics/index|Bayesian Statistics]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Where the spread goes: [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] (estimating $\pi$)
- Continue: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/03-glosten-milgrom-sequential-trade|03 - Glosten–Milgrom]]

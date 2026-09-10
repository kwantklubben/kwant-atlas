---
title: "06 - Advanced Extensions: The HFT Strategy Taxonomy, Latency and Market Design"
tags:
  - pillar-algorithmic-hft
  - hft
  - latency
  - market-design
  - regulation
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 - Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The order types and mechanics of the previous pages are the *alphabet*; this page is the *grammar* of what is written with it — the taxonomy of high-frequency strategies, the economics of the latency race, and the market-design and regulatory responses. The three questions:

1. **What are the HFT strategies?** Nearly all reduce to a small set: **market making** (earn the spread and rebates), **arbitrage** (latency, cross-venue, index/ETF, and statistical), and **order-anticipation / liquidity detection** (infer and front-run a predictable flow).
2. **Why is there a latency arms race?** Because in a *continuous* market, the first firm to react to a stale quote captures a riskless edge; the race is a *rent-dissipation* contest whose cost is pure social waste once it exceeds the value of the edge (Biais–Foucault–Moinas).
3. **What are the design and regulatory responses?** Speed bumps, batch auctions, order-protection and best-execution rules, and trading-obligation/market-access regimes — each an attempt to keep the race from consuming the market's value.

> **The one-sentence essence.** "HFT is a taxonomy of *ways to be first* — make, arbitrage, anticipate — and market design is the debate over whether being first should pay at all (hence speed bumps and batch auctions)."

---

### 2. Mathematical Ground Truth & Derivations

**The latency race as a winner-take-most contest.** Let the faster firm's edge be $\Delta$ (its latency advantage) and let reaction times be exponentially distributed with scale $\tau$. The probability the faster firm wins the stale-quote race is

$$P(\text{win})=\Pr[T_\text{slow}-T_\text{fast}>\Delta]\approx e^{-\Delta/\tau}.$$

With value captured per win $V$ and $N$ race events, the faster firm's daily rent is

$$R(\Delta)=N\,V\,e^{-\Delta/\tau}.$$

**Key implications:** (i) the *slower* firm's profit is $N\,V\,(1-e^{-\Delta/\tau})$ and it is **negative** once adverse selection dominates — speed is defensive as much as offensive; (ii) $R$ is concave in $\Delta$, so the race's marginal returns vanish yet the spending continues — the classic arms-race signature; (iii) in equilibrium the *social* return to speed can be near zero (the losers just stopped losing), which is the Biais–Foucault–Moinas inefficiency.

**Frequent batch auctions remove the race (Budish–Cramton–Shim).** If all orders arriving in a window $[t,t+\delta]$ are cleared together at a single uniform price with ties broken by *size*, then reaction speed within the window is worthless:

$$\mathbb{E}[\text{speed rent}]=0\quad\text{for any }\Delta<\delta,$$

because whoever arrives marginally earlier in the window loses ties to the larger order and crosses at the same price. This is the formal market-design counterpoint to continuous matching — the modern, high-frequency version of the call auction from [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]].

**Market-maker net economics.** A passive market maker's per-share profit decomposes as

$$\text{net}=\underbrace{r_m}_{\text{rebate}}+\underbrace{S_r}_{\text{realized spread}}-\underbrace{\text{AS}}_{\text{adverse selection}},$$

so a higher rebate is not "free money" — it is compensation that must cover the adverse-selection term (Hasbrouck Ch 5; the Glosten–Milgrom spread).

**The regulatory frame.** Regulation acts directly on the mechanics of this folder: **order-protection / trade-through rules** (Reg NMS Rule 611 in the US, shaping SOR and the NBBO), **best-execution and algorithmic-trading rules** (MiFID II, notably RTS 6 obligations on testing, kill-switches, and market-making schemes), **market-access controls** (SEC Rule 15c3-5), **execution-quality disclosure** (Rule 605/606), and **dark-pool** reporting. None of these changes the mechanics; all of them change what an engine is *allowed* to do with them.

---

### 3. Computational Implementation — latency rent and the batch-auction counterfactual

Quantify the sniping profit as a function of latency advantage, show the batch auction zeros it, and decompose the market-maker PnL. Standard library only; **re-executed and reproduced**.

```python
# 06 - HFT taxonomy: latency race, sniping profit, batch auction
import math
tau = 50.0
edge_per_win = 0.08        # $/share captured from a stale quote
shares = 100000            # shares lifted per event
events = 2000              # race events per day
for d in (0, 10, 50, 200):
    p = math.exp(-d / tau)
    daily = p * edge_per_win * shares * events
    print(f"latency advantage {d:>3} us : P(win)={p:5.3f}  sniping profit/day = ${daily:,.0f}")

print("\nfrequent batch auction: every order in the interval clears together,")
print("no first-mover race -> latency advantage is worthless (sniping profit = $0).")

rebate = 0.0020; spread_capture = 0.0050; adverse = 0.0015   # $/share
net = rebate + spread_capture - adverse
print(f"\nmarket-maker net = rebate {rebate:.4f} + spread {spread_capture:.4f} "
      f"- adverse {adverse:.4f} = {net:.4f} $/share")
```
```
latency advantage   0 us : P(win)=1.000  sniping profit/day = $16,000,000
latency advantage  10 us : P(win)=0.819  sniping profit/day = $13,099,692
latency advantage  50 us : P(win)=0.368  sniping profit/day = $5,886,071
latency advantage 200 us : P(win)=0.018  sniping profit/day = $293,050

frequent batch auction: every order in the interval clears together,
no first-mover race -> latency advantage is worthless (sniping profit = $0).

market-maker net = rebate 0.0020 + spread 0.0050 - adverse 0.0015 = 0.0055 $/share
```

**Read the numbers.** The winning probability decays exponentially ($e^{-\Delta/50}$), so a **10 µs** edge keeps **82%** of the $16M/day pot while a **200 µs** edge keeps only **1.8%** — and crucially, the *slower* firm's 18% share at 10 µs is its **losses**, not its profits. The concavity is exactly the arms-race signature: the first 10 µs of speed buy ~$3M/day of rent; the next 190 µs buy a further ~$12.8M more but at vastly higher engineering cost. Batch clearing **zeros** the entire $\Delta$-dependence. Finally, the market maker's **5.5 cents/share** net is *conditional on the adverse-selection term being small* — raise adverse selection above rebate $+$ spread and the strategy is a guaranteed loser.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing the rebate with the edge.** A maker-taker rebate is *compensation for quoting*, not profit; it is paid out of the adverse-selection and inventory losses the maker takes. A strategy that nets positive only because of rebates is short volatility in disguise.
2. **Assuming the latency race is winnable.** $R(\Delta)\propto e^{-\Delta/\tau}$ means a firm one order of magnitude slower than its peers is not "a bit behind" — it is *the liquidity the fast firms trade against*. The viable choices are to compete at the frontier or to *not post defensible quotes*; a middling latency is the worst of both.
3. **Regulatory constraints are part of the strategy space.** Order-protection, best-execution, kill-switch, and market-access rules change which strategies are legal, not just which are fast. A latency-arbitrage design that ignores Rule 611 / MiFID II obligations can be both unprofitable and non-compliant.
4. **Batch auctions are a design trade, not a free lunch.** They remove the speed race but impose latency, price uncertainty within the window, and their own tie-breaking incentives. No mechanism dominates; the choice is a policy question, which is why it remains contested.

---

### 5. Canonical Literature & Study References

- **Budish, Cramton & Shim** — "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response," *QJE* 130(4), 2015. *The batch-auction counterfactual and the latency-race critique.*
- **Biais, Foucault & Moinas** — "Equilibrium fast trading," *JFE* 116(2), 2015. *When private speed investment is socially wasteful.*
- **Hasbrouck & Saar** — "Low-latency trading," *JFM* 16(4), 2013. *Order lifetimes and cancel rates that define the latency-sensitive trader.*
- **Menkveld** — "High-frequency trading and the new market makers," *JFM* 16(4), 2013. *HFT as the new cross-venue market makers.*
- **Cartea, Jaimungal & Penalva** — *Algorithmic and High-Frequency Trading* (2015). *The mathematical spine: market making and latency under stochastic control.*
- **MacKenzie, Donald** — *Trading at the Speed of Light* (2021). *The socio-technical account of colocation, microwave links, and the race to the matching engine.*
- **Regulatory primary sources:** SEC Reg NMS (Rule 611 order protection; Rules 605/606 disclosure; Rule 15c3-5 market access); MiFID II / **RTS 6** (algorithmic-trading obligations); exchange colocation and timestamp specifications. *Treat these as primary documentation, not secondary commentary.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Index Hub]]
- Systems tier: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]
- Queue & fill: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Market-maker economics: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]
- Design counterpoint: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]]

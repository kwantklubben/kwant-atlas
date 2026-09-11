---
title: "04 — MEV, Sandwiching & Cross-Venue Arbitrage: Adverse Selection in DeFi"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - mev
  - sandwiching
  - adverse-selection
  - arbitrage
---

**Basic Prerequisites:** [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02 · The Constant-Product AMM]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]].

---

### 1. Intuition & Practical Objective

The AMM is a passive market maker, and passivity is an invitation. Because every quote is a standing commitment that cannot be cancelled, the AMM is exposed to **maximal extractable value (MEV)** — the value an adversarial block producer or trader can capture by ordering, inserting, or censoring transactions. The two canonical attacks, **sandwiching** and **liquidation sniping**, are both *adverse selection against the LP* in the exact sense of [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]]: an informed trader extracts the stale-quote spread.

The practical objective: model a **sandwich attack** trade-by-trade, show who pays (the LP via divergence loss and the victim via slippage), and map the whole economy onto the toxic-order-flow framing of [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]. Then add the two market-level forces every crypto maker lives with: **cross-venue arbitrage** (which keeps AMM prices honest and is itself an adverse-selection cost) and **gas / priority-fee economics** (which decides whether any of this extraction is even profitable).

The three ideas:

1. **MEV is adverse selection with the informer inside the settlement layer.** A sandwich attacker doesn't know more about fundamentals — he knows the *future order flow* (your pending swap) and the *settlement order* (he can place his tx ahead of and behind yours). That is pure pick-off risk for the LP.
2. **The LP always loses, the victim pays, the attacker profits.** Divergence loss is the LP's share of the loss; the victim's extra slippage is the attacker's revenue; the difference is the attacker's own price impact.
3. **Arbitrage is the AMM's price-discovery mechanism and its tax.** The same trade that corrects the pool to the fair price is the trade that imposes divergence loss — there is no AMM without the arbitrageur, and no LP without the tax.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Sandwich mechanics

A victim submits a swap to buy $X$ (spend $\Delta y$ of $Y$). The attacker inserts two transactions around it: first a *front-run* swap that buys $X$ (pushing the AMM price up), then the victim's trade executes at that worse price, then a *back-run* swap that sells the attacker's $X$ back. Because the victim's swap moved price further, the attacker's round-trip earns a profit, and the LP absorbs the extra divergence loss.

The pool math (from [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]]): swapping $\Delta y$ of $Y$ in returns

$$
\Delta x = x - \frac{xy}{y+\Delta y} = \frac{x\,\Delta y}{y+\Delta y}
$$

of $X$ out. The price the victim pays is $\Delta y/\Delta x$, strictly worse than the pre-swap marginal $p=y/x$ — and worse still when the attacker's front-run has already raised $p$. The sandwich is profitable iff the attacker's back-run proceeds exceed his front-run cost plus gas.

#### 2.2 MEV as adverse selection, quantified

In the Glosten–Milgrom / VPIN language of this pillar, the AMM LP quotes a standing (stale) price, and the sandwich attacker is the informed trader who trades against it. The LP's realized adverse-selection cost is exactly the **divergence loss** the arbitrage/attack trades impose; the victim's slippage is the attack's revenue; the residual is the attacker's profit. Higher volatility (more divergence loss per move), deeper victim flows (more slippage), and tighter fee tiers (cheaper to attack) all *raise* the attack's profitability and hence the LP's expected toxic-flow cost — the crypto echo of VPIN-gated quoting in [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow]].

#### 2.3 Cross-venue arbitrage, bridge and funding risk

The AMM's price is only "fair" because **arbitrageurs link it to the CEX price**. Two frictions make that link risky rather than free:

- **Bridge / peg risk.** Cross-chain and wrapped assets trade at a discount to the native asset when the bridge is perceived as risky (hack, withdrawal delay, depeg). An arbitrageur moving value across a bridge takes **bridge risk** (the wrapped token may not convert 1:1), so the AMM price on a risky bridge can diverge from the CEX price — divergence loss without an arbitrageur willing to close it.
- **Funding-rate risk.** In perpetuals markets, the funding rate is the periodic transfer between longs and shorts; the delta-neutral arbitrage that keeps perp and spot prices aligned pays/collects funding as a running cost. A "market-neutral" LP that hedges spot inventory with perps carries funding exposure — a cash-flow risk on top of the divergence loss.

#### 2.4 Gas and priority-fee economics

Ethereum-style settlement uses a **priority fee** (tip above the base fee, EIP-1559): inclusion and ordering are auctioned by tip, so the sandwich attacker bids a higher tip to front-run, and the victim bids to defend. The attack is viable only if

$$
\text{extracted value} - \text{gas costs} - \text{priority fees} > 0 .
$$

Gas is a *fixed* cost per action, so it is a **deflationary tax on small-scale market making**: rebalancing a concentrated position ([[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03]]), migrating liquidity, and posting/removing orders all cost gas, which a low-margin maker may not recover. MEV also creates the fee-tier threshold of [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05]]: a pool is attackable whenever the extractable value exceeds the swap fee it would have to pay, which is why the deepest pools are exactly the ones arbitrageurs target.

---

### 3. Computational Implementation — the sandwich attack, trade by trade

We simulate a sandwich on an ETH/USDC pool step by step, exactly as a bot would, and read off who wins and who pays.

```python
import math

def swap_y_in(dy, x, y):    # dy USDC in -> ETH out
    ny = y+dy; nx = (x*y)/ny
    return x-nx, nx, ny
def swap_x_in(dx, x, y):    # dx ETH in -> USDC out
    nx = x+dx; ny = (x*y)/nx
    return y-ny, nx, ny

x, y = 100.0, 300000.0                      # pool: 100 ETH, 300,000 USDC (p = 3000)
v_alone, _, _ = swap_y_in(30000.0, x, y)    # victim trades with no attacker present
print(f"victim alone: buys {v_alone:.4f} ETH, realized {30000/v_alone:.1f} USDC/ETH")

x, y = 100.0, 300000.0
att,  xa, ya = swap_y_in(15000.0, x, y)     # attacker front-runs: buys ETH
vict, xb, yb = swap_y_in(30000.0, xa, ya)   # victim executes at the worse price
out,  xc, yc = swap_x_in(att, xb, yb)        # attacker back-runs: sells ETH
print(f"attacker buys {att:.4f} ETH  (pool price now {ya/xa:.1f})")
print(f"victim buys {vict:.4f} ETH  realized {30000/vict:.1f}  (vs {30000/v_alone:.1f} alone)")
print(f"attacker sells {att:.4f} ETH back for {out:.1f} USDC  ->  profit {out-15000:.1f} USDC")
print(f"victim ETH shortfall vs alone = {v_alone-vict:.4f} ETH")
print(f"final pool price = {yc/xc:.1f}")
```
```
victim alone: buys 9.0909 ETH, realized 3300.0 USDC/ETH
attacker buys 4.7619 ETH  (pool price now 3307.5)
victim buys 8.2816 ETH  realized 3622.5  (vs 3300.0 alone)
attacker sells 4.7619 ETH back for 17912.0 USDC  ->  profit 2912.0 USDC
victim ETH shortfall vs alone = 0.8093 ETH
final pool price = 3566.2
```
The sandwich is cleanly profitable: the attacker pays $15{,}000$ USDC for $4.762$ ETH, lets the victim push the price up, then sells the same ETH back for $17{,}912$ — a **$2{,}912$ USDC profit**. The victim buys $8.28$ ETH instead of $9.09$ (realized $3622.5$ vs $3300$ USDC/ETH, a **~9.8% worse fill**), losing $0.8093$ ETH. The LP meanwhile has absorbed the extra divergence loss from the price run to $3566$; the attacker's profit, the victim's shortfall, and the LP's additional loss all come out of the pool's curvature — one adverse-selection tax, three parties sharing it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming the pool marks fair price.** It marks the price arbitrageurs bring it, after paying their tax. Between CEX price moves, the AMM quote is stale by construction — that is the window MEV extracts. Measuring "fair" requires a reference (oracle/CEX), i.e. the [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]]/adverse-selection machinery.
2. **Fee tiers as an attack dial.** Low-fee pools are cheaper to sandwich; high-fee pools are harder to front-run but charge LPs' own rebalancing and users more. Choosing a tier is choosing your adverse-selection exposure, not just your revenue split.
3. **Bridge and funding risk are silent divergence-loss amplifiers.** An LP hedged on a perp pays funding; an LP holding wrapped tokens eats bridge-peg discount; both are "impermanent" costs that no amount of fee income analysis captures if you model only the local pool.
4. **Gas makes small-scale DeFi market making uneconomic.** Every action — deposit, rebalance, withdraw, hedge — costs gas plus priority fees. Below a size threshold the fixed costs exceed the edge, so the efficient scale of AMM market making is large, compounding the passive-maker disadvantage.

---

### 5. Canonical Literature & Study References

- **Daian, Philip et al.**, *Flash Boys 2.0: Frontrunning, Transaction Reordering, and Consensus Instability in Decentralized Exchanges* (2019), arXiv:1904.05234 — the canonical MEV taxonomy (including sandwiching) and its consensus-level origins.
- **Qin, Kaihua, Zhou, Liyi & Gervais, Arthur**, *Quantifying Blockchain Extractable Value* (2021), arXiv:2101.05511 — empirical MEV measurement and the "MEV = arbitrage + liquidation + sandwich" decomposition.
- **Capponi & Jia (2022)**, *The Anatomy of a Liquidity Provision in Automated Market Makers*, arXiv:2210.07852 — adverse selection in AMMs framed as the LP cost of arbitrage.
- **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25(5) — the VPIN framework that the MEV-as-toxic-flow mapping generalizes.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03 · Concentrated Liquidity & Uniswap v3]] · [[pillars/06-market-making/crypto-and-defi-market-making/index|Index Hub]]
- Forward: [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/market-impact-and-depth|Market Impact & Depth]]

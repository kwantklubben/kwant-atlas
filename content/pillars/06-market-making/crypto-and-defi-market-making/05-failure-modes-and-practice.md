---
title: "05 — Failure Modes & Practice: Fees vs LVR, Gas, Bridges, Protocol Risk"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - failure-modes
  - loss-versus-rebalancing
  - protocol-risk
  - gas-economics
---

**Basic Prerequisites:** [[pillars/06-market-making/crypto-and-defi-market-making/04-mev-sandwiching-and-arbitrage|04 · MEV & Sandwiching]].

---

### 1. Intuition & Practical Objective

Every structural advantage of the AMM (passivity, no inventory management, no quote management) is also its structural weakness. This page names the failures precisely so a practitioner can decide, in money terms, *whether to provide liquidity at all*. The objective is not cynicism — it is knowing exactly where the "free money from fees" story breaks.

The five failures, in one line each:

1. **Fees rarely cover divergence loss on volatile assets.** The LP earns fee income but loses the path-dependent **loss-versus-rebalancing (LVR)** to arbitrageurs; on volatile, low-turnover pools *all* standard fee tiers lose net.
2. **24/7, no circuit breakers, no halts.** A crash that would halt a CEX is just another (faster) arbitrage trade on-chain — and the LP cannot exit faster than the arbitrageur can trade.
3. **Protocol risk compounds market risk.** Smart-contract bugs, oracle manipulation, and bridge hacks are tail risks with no exchange backstop or settlement guarantee.
4. **Gas and priority fees are a fixed-cost tax.** Rebalancing concentrated liquidity, hedging, and withdrawing all burn gas; below a scale threshold, market making is uneconomic.
5. **The AMM has no inventory or adverse-selection controls.** Everything a human maker does with a reservation price and toxicity gating ([[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]], [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]]) is structurally absent.

---

### 2. Mathematical Ground Truth & Derivations

**Where the break-even lives.** The LP's net P&L (in numeraire, ignoring fees already described by the divergence-loss of [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]]) is

$$\text{net} = \text{fee income} - \text{LVR},$$

where LVR is the divergence loss *as a running, path-dependent cost* (Milionis et al. 2022), and fee income $=f\times$ (traded volume). Providing liquidity is profitable iff

$$\boxed{\;f \times \text{volume} \;>\; \mathrm{LVR}\;} .$$

**The instantaneous LVR rate.** Milionis, Moallemi, Roughgarden & Zhang (2022) prove that for a constant-product AMM the instantaneous rate of LVR is

$$\frac{d\mathrm{LVR}}{dt} = \tfrac18\,\sigma^2\,V,$$

with $V$ the pool value in numeraire and $\sigma$ the volatility of the price process — the same $\tfrac18\sigma^2$ that the small-move expansion of divergence loss ($\mathrm{DL}\approx s^2/8$) in [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]] seeded. Over a finite horizon the expected total LVR is $V_0(1-e^{-\sigma^2T/8})\approx \tfrac18\sigma^2V_0T$ for small $\sigma^2T$. **Since fee income scales with volume (roughly $\propto\sigma$) but LVR scales with $\sigma^2$, the required fee tier grows with volatility** — high-vol pools need high fee tiers and high turnover to break even, which is precisely why volatile tokens shed liquidity.

**Gas as a fixed cost.** On Ethereum-style chains, each on-chain action costs a base fee plus a priority fee (EIP-1559); MEV competition bids the priority fee up exactly when rebalancing matters most. Gas therefore behaves as a per-action fixed cost that shifts the break-even further toward large, infrequent, high-edge market making — the opposite of the "always-on passive" promise.

---

### 3. Computational Implementation — do the fees cover the LVR?

We simulate a constant-product pool over one year (drift-free geometric Brownian motion on the price, volatility $\sigma=0.6$ annualized). At every step an arbitrageur rebalances the pool to the fair price; we accumulate fee income at each fee tier against the realized LVR (the pool's mark-to-market divergence loss over the path).

```python
import math, random
random.seed(11)

sig = 0.6; T = 1.0; n = 200
dt  = T/n
sdt = sig*math.sqrt(dt)
k   = 10000.0; p0 = 1.0
def V(p): return 2.0*math.sqrt(k*p)
tiers = (1e-4, 5e-4, 3e-3)                 # 0.01%, 0.05%, 0.30%

def sim(npaths):
    tot_lvr = tot_vol = 0.0; tot_fee = {f:0.0 for f in tiers}
    for _ in range(npaths):
        p = p0; y = math.sqrt(k*p); v0 = V(p)
        lvr = 0.0; tv = 0.0; fee = {f:0.0 for f in tiers}
        for i in range(n):
            pn = p*math.exp(-0.5*sdt*sdt + sdt*random.gauss(0,1))
            yn = math.sqrt(k*pn)
            step = abs(yn-y); tv += step          # numeraire leg of the arbitrage trade
            for f in fee: fee[f] += f*step
            y = yn; p = pn
        lvr = v0 - V(p)                           # pool's divergence loss over the path
        tot_lvr += lvr; tot_vol += tv
        for f in fee: tot_fee[f] += fee[f]
    return tot_lvr/npaths, tot_vol/npaths, {f: tot_fee[f]/npaths for f in tiers}

LVR, vol, fee = sim(4000)
print(f"sigma=0.6/yr, 1yr: LVR={LVR:6.2f}  arbitrage volume={vol:6.1f}  turnover={vol/V(p0):.2f}x/yr")
for f, v in fee.items():
    print(f"  fee tier {f*100:>4.2f}%: fee income={v:6.2f}  net P&L={v-LVR:8.2f}")
print(f"  breakeven fee = LVR/volume = {LVR/vol*100:.2f}%")
```
```
sigma=0.6/yr, 1yr: LVR=  7.55  arbitrage volume= 331.9  turnover=1.66x/yr
  fee tier 0.01%: fee income=  0.03  net P&L=   -7.52
  fee tier 0.05%: fee income=  0.17  net P&L=   -7.38
  fee tier 0.30%: fee income=  1.00  net P&L=   -6.56
  breakeven fee = LVR/volume = 2.27%
```
**Reading the numbers.** With $\sigma=0.6$/yr and only $1.66\times$ annual turnover, the realized LVR is $7.55$ (per $200$ of pool value) while fee income at every Uniswap tier — $0.01\%$, $0.05\%$, $0.30\%$ — is a fraction of that. Net P&L is **negative for all three tiers**; the breakeven fee is $\approx 2.27\%$, far above any standard tier. This is the LVR literature's core empirical claim (Milionis et al. 2022; a16z LVR): low-fee, volatile, moderate-turnover pools transfer value from LPs to arbitrageurs. It also explains the failure mode list that follows — LPing is only a positive-expectation business at *high* turnover (where $f\times\text{volume}$ overtakes $\tfrac18\sigma^2V$) or on *low*-volatility pairs.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **LVR swamps fees on volatile pools (the #1 failure).** At $\sigma=0.6$/yr the required fee is $\approx2.3\%$ (§3); real pools on volatile tokens sit at $0.01$–$0.30\%$ tiers and bleed. Before adding liquidity, check whether $f\times\text{volume}>\tfrac18\sigma^2V$ — this is the single most important go/no-go test in DeFi market making.
2. **24/7 markets, no circuit breakers, no price bands.** A CEX halts, widens bands, or invokes a kill switch; an AMM can do none of these. In a flash crash the arbitrageur still trades and the divergence loss is realized instantly. Liquidity "always available" is also liquidity "always exposed."
3. **Protocol risk is additive and unhedgeable.** Smart-contract vulnerabilities, oracle manipulation (a wrong price feeds a liquidation or a swap), and bridge hacks can wipe the entire deposit, not just the divergence loss. There is no exchange guarantee and no settlement protection; the "risk-free spread" does not exist on-chain.
4. **Gas + priority fees are a per-action tax.** Rebalancing concentrated liquidity ([[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03]]), hedging, and withdrawing all consume gas, which MEV competition inflates exactly when action is most urgent. Below a size threshold the fixed costs exceed the edge — DeFi market making is inherently large-scale.
5. **No inventory or toxicity control.** The AMM can neither skew away from inventory nor widen against toxic flow. Every mitigation must be built *outside* the pool (hedging, range migration, exit rules) — the on-chain mirror of [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]]'s reservation-price discipline, minus the ability to actually control quotes.

---

### 5. Canonical Literature & Study References

- **Milionis, Moallemi, Roughgarden & Zhang (2022)**, *Automated Market Making and Loss-Versus-Rebalancing*, arXiv:2208.06046 — LVR, the $\tfrac18\sigma^2V$ rate, and the "fees minus LVR" decomposition reproduced above.
- **a16z Crypto**, *LVR: Quantifying the Cost of Providing Liquidity to Automated Market Makers* — the accessible statement that LVR depends on the price *trajectory* and accumulates trade-by-trade, unlike divergence loss.
- **Clark, Joseph (2020)**, *The Replicating Portfolio of a Constant Product Market*, SSRN 3550601 — the short-options view that makes the $\tfrac18\sigma^2$ "option premium" intuition precise.
- **Lehar & Parlour (2023)**, *Decentralized Exchange: The Uniswap Automated Market Maker* — empirical evidence that LPs systematically withdraw from volatile, high-LVR pools.
- **Daian et al. (2019)**, *Flash Boys 2.0*, arXiv:1904.05234 — the MEV/gas-economics mechanism behind the fee-tier attack threshold.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/crypto-and-defi-market-making/04-mev-sandwiching-and-arbitrage|04 · MEV & Sandwiching]] · [[pillars/06-market-making/crypto-and-defi-market-making/index|Index Hub]]
- Forward: [[pillars/06-market-making/crypto-and-defi-market-making/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding|Liquidity Risk & Funding]]

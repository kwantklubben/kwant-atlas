---
title: "01 - Liquidity Risk & Asset Pricing from Zero: the Illiquidity Premium"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - intuition
  - liquidity-premium
---

**Basic Prerequisites:** none beyond basic algebra.

---

### 1. Intuition & Practical Objective

Start with the question this whole folder answers: **why would two securities with identical future cash flows trade at different prices?**

The answer is the **cost of exiting**. A government bond you can sell into the middle of the quote in a millisecond for $99.90 costs you almost nothing to turn back into cash. A private loan or a small-cap stock that takes a week to sell, and whose sale itself pushes the price down, is worth *less to you today* — because when you eventually want the cash back, it will not be there for free. Rational investors demand to be paid for that: they bid the illiquid asset down until its expected return is high enough to compensate for the round-trip cost.

That extra required return is the **liquidity premium**. Three ideas, in increasing order of subtlety:

1. **The level of illiquidity is priced (Amihud–Mendelson).** More illiquid assets earn higher expected returns, roughly the spread *amortized over the holding period*: the less often you trade, the more the one-time cost can be spread out.
2. **The *risk* of illiquidity is priced too (Pastor–Stambaugh).** Beyond the average level, investors fear *changes* in liquidity. A stock that tends to fall precisely when the whole market's liquidity dries up is riskier and earns a premium — this is a **liquidity beta**, like a market beta but for liquidity instead of the market.
3. **Illiquidity is common and it spikes in bad times (Acharya–Pedersen; Bao et al.).** Illiquidity across assets moves together, and it worsens exactly in down markets — which is why the risk is so hard to hedge and so expensive.

> **One mental model to keep.** Liquidity is insurance with a price. In calm markets you almost never collect; in a crisis it is the difference between getting out at 99 and getting out at 60. The premium you see in *normal* expected returns is the market charging you, in advance, for the *states* where you most need to trade and can least afford to.

This folder is the **asset-pricing** view. The sibling folder [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (Pillar 4) asks the *funding* question — can you finance the position at all? — and its L-VaR and margin-spiral machinery. Here we ask: *given the cost of trading, what must prices and expected returns be?* They are two views of one phenomenon; a full picture needs both.

---

### 2. Mathematical Ground Truth & Derivations

**The amortization identity (Amihud–Mendelson 1986).** Suppose the round-trip cost of trading asset $i$ is a fraction $s_i$ of its value (the relative spread). If you hold it for $h$ years and trade once to buy and once to sell, the total cost is $2s_i$ over the life of the position, i.e. roughly $2s_i/h$ per year. To make the asset competitive with a liquid asset returning $r$, its gross required return must be

$$R_i \simeq r + \frac{s_i}{h},$$

where the precise constant depends on how the two sides of the cost are counted (Foucault et al. §9; a common form quotes the premium as $s/h$ with $s$ the one-way relative cost). **The premium shrinks as the holding period grows** — long-horizon investors can amortize a fixed cost over more time, so they demand less compensation. This is the classic rationale for why long-horizon (pension) money tolerates illiquid assets.

**Why the *level* shows up in prices.** If asset $i$ is illiquid (large $s_i$) and asset $j$ is liquid, the price of $i$ must be *lower* today so that, over the holding period, its expected return is the liquid rate plus the amortized cost. Equivalently, in a discount-factor language, illiquid assets are priced by a lower valuation because their future cash flows are worth less once you subtract what it costs to convert them into cash.

**Why the *risk* shows up too.** Now let liquidity vary over time. If aggregate liquidity $L_t$ can drop, then an asset whose payoff $r^i_t$ is *negatively* correlated with $L_t$ (it pays off badly exactly when trading gets expensive) is an asset that fails you in the states you need it. Risk-averse investors require compensation for holding it — the liquidity beta channel of [[pillars/06-market-making/liquidity-risk-and-asset-pricing/03-liquidity-as-a-priced-factor|03 · Liquidity as a Priced Factor]]. This is a *second, independent* premium over and above the level effect.

---

### 3. Computational Implementation — the premium in numbers

The level effect, quantified with the Amihud–Mendelson amortization. The print-verified output shows the whole point: **longer holding periods ⇒ smaller required premium** for the same spread.

```python
def required_premium(s, h):
    """Annualized excess return required to amortize one-way relative cost s
       over a holding period of h years (Amihud-Mendelson gross-return form)."""
    return s / h

s = 0.002  # 20 basis points one-way relative trading cost
print(f"One-way relative cost s = {s*10000:.1f} bp.  Required annual excess premium:")
for h in (0.02, 0.08, 0.5, 1.0):   # holding periods in years
    print(f"  hold {h:4.2f} yr -> {required_premium(s,h)*100:6.3f}%/yr")
```
```
One-way relative cost s = 20.0 bp.  Required annual excess premium:
  hold 0.02 yr -> 10.000%/yr
  hold 0.08 yr ->  2.500%/yr
  hold 0.50 yr ->  0.400%/yr
  hold 1.00 yr ->  0.200%/yr
```
A 20 bp cost is *nothing* if you hold for a year (0.2%/yr) but a *huge* 10% per year if you hold for a week. **This is why liquidity premia are widest in assets you trade often or must exit fast**, and why illiquidity is mostly a short-horizon phenomenon — exactly the reasoning the empirical cross-section confirms (small caps, bonds, private assets).

---

### 4. Failure Modes & First-Principles Breakdowns

- **The premium is not a constant.** It depends on the holding period, the *expected future* spread (not just today's), and the state of the world. Quoting "the" liquidity premium of an asset without the horizon is meaningless.
- **Level vs. risk are conflated.** A stock can be illiquid on average (big level premium) but have *low* liquidity risk (stable liquidity) — the two channels of §2 must be estimated separately or the premium is double-counted.
- **Prices already embed the premium.** You cannot "harvest" the liquidity premium by buying illiquid assets and hoping; part of the premium is compensation for *bearing the risk* that liquidity evaporates when you need out — see [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes]] and the [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|funding-side]] spiral.

---

### 5. Canonical Literature & Study References

- **Amihud & Mendelson (1986).** *Asset pricing and the bid-ask spread.* Journal of Financial Economics 17, 223–249. The origin of the liquidity-premium idea; the spread/holding-period relation.
- **Amihud (2002).** *Illiquidity and stock returns.* JFM 5, 31–56. The empirical anchor: expected illiquidity is priced cross-sectionally and over time.
- **Amihud, Mendelson & Pedersen (2013).** *Market Liquidity: Asset Pricing, Risk, and Crises.* Cambridge University Press. Ch 2 (why liquidity is priced) — the ideal first-read capstone.
- **Foucault, Pagano & Roell (2013).** *Market Liquidity.* Ch 9 (liquidity and asset prices) — the gross-return/amortization form.

---

### 6. Connected Graph Bridges

- Next: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/03-liquidity-as-a-priced-factor|03 · Liquidity as a Priced Factor]]
- Back: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Index Hub]]
- Sibling funding view: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (Pillar 4) · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]

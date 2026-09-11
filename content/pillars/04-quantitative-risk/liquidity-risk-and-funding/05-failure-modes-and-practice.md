---
title: "05 — Failure Modes & Practice: Horizon Blindness, Fire-Sale Externalities & Funding/Market Coupling"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - failure-modes
  - fire-sales
  - procyclicality
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]] and [[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · Liquidation Cost & L-VaR]].

---

### 1. Intuition & Practical Objective

Every liquidity measure this folder builds is *correct under an assumption that is false exactly when it matters*. This page names the three failures precisely, so a risk manager knows which number to distrust and how the failure shows up in money terms. It is the same discipline as [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|VaR's failure page]]: know where the model is an approximation so the residual can be measured.

The three failures, in one line each:
1. **Horizon blindness** — VaR scales market risk by $\sqrt T$ but the cost of *actually liquidating over $T$ days* scales worse than that; using a 1-day horizon for a 10-day exit understates the loss on both counts.
2. **Fire-sale externality** — a fund prices its own order's impact but not the *crowd's*; with shared collateral and correlated margin rules, private liquidation cost systematically understates social cost, and the gap is the contagion channel.
3. **Funding-vs-market coupling** — margin depends on volatility, and forced selling *causes* volatility; any model that treats the haircut as exogenous breaks precisely at the moment the coupling binds.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Horizon blindness, exactly.** The two loss terms scale differently with the liquidation horizon $T$:

| Term | Scaling in $T$ | Source |
|---|---|---|
| Market VaR (i.i.d.) | $\\sqrt T$ | $\mathrm{VaR}_T=\mathrm{VaR}_1\sqrt T$ (Hull §22.4) |
| Timing risk over the schedule | $\\sqrt T$ | price moves while you work the order |
| Impact cost of a rate-limited schedule | $\\sim T$ (linear-impact) | spreading $Q$ over $T$ days at $\alpha\cdot\text{ADV}$/day |

So the **ratio of total cost to a naive 1-day VaR grows like $\sqrt T$** from the risk term and can grow like $T$ from the schedule term: at $T=16$ days the linear-impact schedule cost is **$16/4=4\times$** the market-risk term per the $\sqrt T$ scaling. **Ignoring the horizon is not a small correction; it is a factor.**

**2.2 Fire-sale externality, exactly.** With linear impact ($\kappa=1/D$ per unit sold), a fund selling $Q_i$ into an aggregate $Q_{\text{agg}}=\sum_j Q_j$ bears a shortfall
$$
\text{Cost}_i=\frac{\kappa}{2}\,Q_i\,Q_{\text{agg}}\quad\text{(social)}\qquad\text{vs}\qquad \text{Cost}_i^{\text{priv}}=\frac{\kappa}{2}\,Q_i^{2}\quad\text{(private)}.
$$
Because $Q_{\text{agg}}\ge Q_i$, the private model **always understates** the cost by the factor $Q_{\text{agg}}/Q_i$. Two symmetric funds each selling $Q$ double their true cost relative to the private estimate — a **100% understatement** — and the discrepancy is the *pecuniary externality*: each fund's sale is cheaper to itself than it is to the system. This is why crowded trades (mortgage credit in 2007, the 2007 quant quake, 2020 Treasury basis) fail in unison rather than one at a time.

**2.3 The coupling, exactly.** Recover the margin from §2.2 of [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04]]:
$$
m=z_\alpha\,\sigma\sqrt{\Delta t_{\text{MPOR}}},\qquad \sigma \text{ and } \Delta t_{\text{MPOR}} \text{ both increasing in stress}.
$$
The derivative $\partial m/\partial(\text{forced selling})>0$ is the entire coupling: **the model input ($m$) is a function of the model's own output (forced-selling-induced volatility).** A static-haircut L-VaR is not merely imprecise; it is structurally blind to the spiral.

**2.4 Procyclicality of measured risk.** Historical-simulation VaR *falls* in calm markets (small shocks in the window) and *spikes* after losses. Because the margin $m=z_\alpha\sigma$ is procyclical too, the two reinforce: calm markets grant high leverage (low $m$, low measured risk), and the first shock collapses both. Supervisors counter with **stressed VaR/ES** (Basel II.5) and FRTB's liquidity horizons; the correction is a supervisory acknowledgement that "current" liquidity is the wrong scaling.

---

### 3. Computational Implementation — the externality, and the horizon gap

Two experiments. **(A)** Quantify the fire-sale externality: two funds each reasoning privately about their own order size. **(B)** Show the horizon gap between the market-risk term ($\sqrt T$) and the schedule cost (linear $T$). Stdlib only.

```python
import math

# (A) fire-sale externality: A prices only its own order, but B plays too
D   = 200_000.0                 # depth (shares per $1 move), so kappa = 1/D
QA  = QB = 60_000               # each fund must sell 60,000 shares
priv_A = QA * (QA / D) / 2                    # A ignores B's selling
joint  = QA * ((QA + QB) / D) / 2             # actual cost A faces when B also sells
print(f"depth D={D:,.0f} sh/$. A and B each must sell {QA:,} sh.")
print(f"A's assumed private cost          = ${priv_A:,.0f}")
print(f"A's actual cost when B also sells = ${joint:,.0f}")
print(f"unpriced externality on A         = ${joint-priv_A:,.0f}  ({(joint-priv_A)/priv_A*100:.0f}% understated)")

# (B) horizon: market risk scales sqrt(T), schedule/impact cost scales ~T
print("\nhorizon scaling of the two loss terms:")
for T in (1, 4, 9, 16):
    print(f"T={T:2d}d: sqrt-scaled VaR factor {math.sqrt(T):.2f}   linear liquidation-cost factor {T:.2f}"
          f"   ratio {T/math.sqrt(T):.2f}x")
```
```
depth D=200,000 sh/$. A and B each must sell 60,000 sh.
A's assumed private cost          = $9,000
A's actual cost when B also sells = $18,000
unpriced externality on A         = $9,000  (100% understated)

horizon scaling of the two loss terms:
T= 1d: sqrt-scaled VaR factor 1.00   linear liquidation-cost factor 1.00   ratio 1.00x
T= 4d: sqrt-scaled VaR factor 2.00   linear liquidation-cost factor 4.00   ratio 2.00x
T= 9d: sqrt-scaled VaR factor 3.00   linear liquidation-cost factor 9.00   ratio 3.00x
T=16d: sqrt-scaled VaR factor 4.00   linear liquidation-cost factor 16.00   ratio 4.00x
```

Panel (A): the *same order* costs A twice as much as its private model says the instant a peer is unwinding alongside it — and no amount of firm-level L-VaR diligence detects this, because the peer's order is not in A's data. Panel (B): the two terms diverge as $\sqrt T$ vs $T$; a 16-day liquidation schedule costs $4\times$ the market-risk term *in relative terms*, and the gap keeps widening.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Horizon blindness → "we can always exit."** Using a 1-day VaR for a position that takes 10 days to unwind understates market risk by $\sqrt{10}\approx3.16$ and omits the schedule cost entirely. Fix: horizon-matched VaR (FRTB liquidity horizons) plus an explicit liquidation-cost term ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03]]).
2. **Fire-sale externality → crowded-trade contagion.** Private liquidation cost $\propto Q_i^2$ vs social $\propto Q_iQ_{\text{agg}}$. Fix: system-level stress tests ([[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]), concentration limits, and margin rules that account for aggregate positioning — none of which a single fund has the incentive to impose on itself.
3. **Funding-market coupling ignored.** A constant haircut deletes the margin spiral by construction. Fix: make $m$ a function of $\sigma$ and MPOR, and stress both.
4. **Liquidity treated as diversifiable.** Illiquidity is *common across assets* (Hasbrouck–Seppi 2001; Chordia–Roll–Subrahmanyam 2000) and covaries with market returns. It is a *priced factor* (Pastor–Stambaugh 2003; Acharya–Pedersen 2005), so it does not average out in a portfolio — it *is* the tail dependence ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06]]).
5. **Calm-period calibration.** $\lambda$, $D$, and ADV are all procyclical. Calibrating impact from a calm sample understates stress-period cost by an order of magnitude — the mirror image of VaR's window-truncation problem. Use stressed parameters and re-estimate MPOR.
6. **The liquidity illusion of "liquid" assets.** On-the-run Treasuries are liquid individually; if everyone must sell them at once, the *aggregate* market liquidity is what binds, and it is far smaller than the sum of the individual estimates. This is the "liquidity illusion" — market liquidity is a public good that is over-consumed in good times.
7. **Model-risk of the impact model itself.** Linear vs square-root vs hybrid impact gives materially different costs at large $Q$ (quadratic overstates far out, linear understates per-unit). Report the model-dependence explicitly; do not present a single L-VaR point estimate as truth (see [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]). Note, too, that *market* liquidity and *funding* liquidity must be stressed together — scenario design that shocks only prices misses the margin spiral.

---

### 5. Canonical Literature & Study References

- **Brunnermeier & Pedersen** (2009) — the coupling $\partial m/\partial(\text{stress})$ and the spiral interaction. **Brunnermeier** (2009) — the 2007–08 case evidence for all three failures.
- **Shleifer & Vishny** (1997), *The Limits of Arbitrage* — performance-based arbitrage and fire sales; the externality's microfoundation.
- **Foucault, Pagano & Röell** (2013), Ch 9 (limits to arbitrage; crisis amplification when the liquidation discount is large) and Ch 3 (adverse selection ⇒ permanent impact, so liquidation *does* move the efficient price). *Verified in corpus.*
- **Hasbrouck** (2007), Ch 9.9 (Amihud/Amivest proxies and their pitfalls) and Ch 1.2 (depth/breadth/resiliency). *Verified in corpus.*
- **Pastor, L. & Stambaugh, R.** — *Liquidity Risk and Expected Stock Returns*, *JPE* 111(3) (2003) — liquidity as a priced, undiversifiable factor. (Pillar 6 refs.) **Acharya & Pedersen** (2005) — the liquidity-adjusted CAPM. (Corpus.)
- **BCBS** — *Principles for Sound Stress Testing Practices and Supervision* (2009, BIS) and the LCR/NSFR documents — the regulatory response to failures 2–4.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06 · Advanced Extensions (Liquidity Spirals & Systemic Risk)]]
- Siblings: [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|VaR Failure Modes]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]

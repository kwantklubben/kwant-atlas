---
title: "3.1.5 Failure Modes & Real-World Practice"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - basis-risk
  - hedging-friction
  - margin
  - model-risk
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/options-fundamentals-and-markets/04-no-arbitrage-and-bounds|04 · No-Arbitrage & Bounds]].

---

### 1. Intuition & Practical Objective

Every relationship on the previous pages assumes you can trade the **exact** underlying, **costlessly**, without limit, and settle on the model's schedule. Real markets break all four. The objective of this page is to name the breakages precisely and to *quantify* them, so that "the model says X" is never the end of the conversation - the residual is.

The four frictions, in one line each:

1. **Basis risk** - you hedge with a *related* instrument, not the asset, so the hedge is imperfect. This is the single largest practical failure of hedging (Hull Ch 3).
2. **Liquidity & margin** - a hedge you cannot fund or roll is not a hedge; margining and collateral are parts of the payoff (Hull Ch 2, 9).
3. **Contract-specification traps** - multipliers, delivery options, day-counts and dividend/split adjustments silently change the number.
4. **Model risk** - the no-arbitrage identities are safe, but the moment you *parameterise* (pick a $\sigma$, a carry, a correlation) you inherit estimation error.

> **The one-sentence essence.** "Textbook no-arbitrage assumes perfect substitutes and frictionless trading; practice replaces exact hedging with *minimum-variance* hedging and measures the leftover - the basis - instead of assuming it away."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Basis and the effective hedged price (Hull Ch 3.3)

$$
\text{Basis}=S-F \quad(\text{asset price} - \text{futures price of the contract used}).
$$

For a short hedge (you own the asset and will sell it), the effective price received is

$$
S_2+F_1-F_2=F_1+b_2,\qquad b_2=S_2-F_2 \text{ (the basis at close).}
$$

So the hedge locks in the **initial futures price plus the terminal basis** - not the initial spot. If the basis were zero at close, the hedge is perfect; the leftover risk is uncertainty in $b_2$, i.e. **basis risk**. Choose the delivery month as close as possible to, but **later than**, the hedge horizon to minimize it (Hull §3.3).

#### 2.2 Minimum-variance hedge ratio and hedge effectiveness (Hull eq. 3.1–3.2)

Regress $\Delta S=a+b\,\Delta F+\varepsilon$. The variance-minimising slope is $\rho\,\sigma_S/\sigma_F$, so

$$
\boxed{\,h^*=\rho\,\frac{\sigma_S}{\sigma_F}\,}\qquad N^*=h^*\frac{Q_A}{Q_F}.
$$

**Hedge effectiveness** $=$ the fraction of variance eliminated $=$ the regression $R^2=\rho^2$. Residual variance

$$
\operatorname{Var}(\Delta S-h^*\Delta F)=(1-\rho^2)\sigma_S^2.
$$

This is the quantitative version of "a cross-hedge is never exact": even a $\rho=0.928$ hedge (Hull's airline example) removes only $\rho^2=86\%$ of the variance. The **daily-settlement** version regresses *percentage* one-day changes, $h^*=\tilde\rho\,\tilde\sigma_S/\tilde\sigma_F$, $N^*=h^*V_A/V_F$, and **tailing** divides $N^*$ by $(1+r)$ for the interest effect.

#### 2.3 Structure as a failure mode (Hull Ch 2, 6)

- **Daily settlement / convexity.** Futures settle daily; forwards once at $T$. Equal prices only when $r$ is constant. For **interest-rate** futures a closed-form convexity adjustment separates them (Hull Ch 6.3, Ch 30).
- **Delivery options.** The short party of a Treasury-bond futures chooses *when* (wild card), *which* (cheapest-to-deliver), and *in what form* to deliver; each option **lowers** the futures price (Hull Ch 6.2).
- **Day-count.** Actual/360 vs Actual/365 distorts accrued interest by $\approx1.4\%$; applied across a book it is material.

#### 2.4 Where the identities still hold

Crucially, **put–call parity and the bounds do not need the model** - they survive every friction *if the hedges remain feasible*. What dies under frictions is (i) the exactness of the hedge, (ii) the uniqueness of the price (incomplete markets), and (iii) the assumption that you can capture a violation. A "violation" narrower than the transaction cost is not a trade.

---

### 3. Computational Implementation - basis risk in numbers

Standard library only (seeded RNG for reproducibility). It estimates the minimum-variance hedge ratio from simulated correlated price changes, confirms it matches $\rho\sigma_S/\sigma_F$, reports the hedge effectiveness $\rho^2$ (the fraction of variance *not* removed is the irreducible basis risk), computes the contract count, and shows the tailing adjustment.



The empirical slope $0.7808$ reproduces the theoretical $0.7798$ (Hull's airline cross-hedge, $\approx0.78$), the contract count $37.13\to37$ reproduces Hull's worked example, and the $13.88\%$ of variance **left over** ($1-\rho^2$) is the basis risk that no amount of hedging removes - it is a property of the *instrument*, not the analysis.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Basis risk is irreducible with a cross-hedge.** $h^*$ minimises variance, it does not eliminate it: residual $=(1-\rho^2)\sigma_S^2$. Choosing the wrong contract (delivery month *before* the horizon) can make the basis, and the risk, larger.
2. **Liquidity and margin are not frictions to ignore - they are constraints.** A hedge of $37$ futures contracts is only executable if the market can absorb it without moving, and only fundable if the margin account is funded. Illiquidity turns a "riskless" arbitrage into a loss; unfunded margin forces liquidation at the worst moment (Hull Ch 2, 9).
3. **Contract-specification traps.** The multiplier ($100\times$), the delivery options in bond futures, and the day-count convention each silently change the cash flows. The wild-card and cheapest-to-deliver options **lower** the futures price - a bid you must account for (Hull Ch 6.2).
4. **Model risk under parameterisation.** Bounds and parity are robust; the *inputs* are not. A single $\sigma$ cannot fit all strikes (the smile), the carry $b$ must match the instrument, and correlations used for cross-hedging are unstable. Every parameter is a place to be wrong.
5. **Leverage and the asymmetry of short options.** A naked short call has unbounded loss and a margin call that scales with the underlying. Under-margining plus leverage is the mechanism behind every headline derivatives blow-up.
6. **Dividend/split adjustment.** Unadjusted splits and mishandled cash dividends make both the payoff and the hedge ratio wrong by a factor - a pure specification error, not a market one.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 3 (basis, minimum-variance ratio eq. 3.1–3.3, hedge effectiveness $=R^2=\rho^2$, stack-and-roll), Ch 2 (margining, CCPs, delivery), Ch 6 §6.2–6.4 (delivery options, wild card, CTD, convexity), Ch 10.7 (option margins), Ch 19 (hedging in practice). *Per-chapter verification report in the corpus.*
- **Hull**, *Risk Management and Financial Institutions* - the leverage/liquidity failure narratives that complement Ch 3 here. *Corpus available.*
- **Shreve**, *Stochastic Calculus for Finance I*, §1.1 (the no-arbitrage bracket $d<1+r<u$ that a frictional market can violate), §3.5 (completeness - what "the" price requires).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/04-no-arbitrage-and-bounds|04 · No-Arbitrage & Bounds]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Index Hub]]
- Next: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/06-advanced-extensions|06 · Advanced Extensions]]
- Deeper failure analysis: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|Binomial · Failure Modes]] · [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]]
- Structure and counterparty: [[pillars/03-derivative-pricing/counterparty-risk-and-xva|Counterparty Risk & XVA]]

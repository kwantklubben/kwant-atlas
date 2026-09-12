---
title: "5.9.4 Carry & Styles Across Asset Classes"
tags:
  - pillar-portfolio-optimization
  - multi-asset-and-factor-allocation
  - carry
  - factor-styles
  - value-momentum-carry-defensive
  - roll-yield
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/03-factor-based-allocation|03 · Factor-Based Allocation]] and [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Factor Timing]].

---

### 1. Intuition & Practical Objective

"Style" is the cross-asset generalisation of a factor. The four canonical styles that recur across *every* asset class are **value, momentum, carry, and defensive** (sometimes "quality" or "low-risk"). This page focuses on the one that is *definable in every asset class without a valuation model* - **carry** - because carry is the cleanest bridge between an asset-class world and a factor world: it prices the term structure / roll-down / dividend / interest differential that each instrument pays merely for *staying still*.

**Carry, defined operationally:** the return you earn over the next period **if prices do not move**. It is not a forecast of price; it is the *structural* yield embedded in the instrument. It generalises:

| Asset class | Carry proxy | What it prices |
|---|---|---|
| Equity | dividend yield (minus financing) | earnings distribution |
| Government bond | yield-to-maturity / roll-down (minus funding) | term premium |
| FX | interest-rate differential (long high-yield vs low-yield) | rate differential |
| Commodities | roll yield = $(F-S)/S$ | storage / convenience / scarcity |
| Credit | credit spread (minus expected default loss) | credit risk premium |

The key empirical fact (Koijen, Moskowitz, Pedersen & Vrugt, "Carry," 2018): **carry predicts returns in every asset class, with the same sign.** High-carry assets earn more than low-carry assets, on average, because carry is a compensation for *risk* - and the risk is a **carry crash**: the strategies earn steadily and lose suddenly when the risk shows up.

> **The one-sentence essence.** "Carry is what an instrument pays you for standing still - the same signal in bonds, FX, commodities, and equities; it is a real premium *and* a real crash risk, which is why it must be sized, not simply maximised."

---

### 2. Mathematical Ground Truth & Derivations

**Carry as a conditional expectation.** Let $S_t$ be the spot and $P_t(T)$ the price of a claim on $S_T$. Define carry as the return under the assumption the *term structure stays unchanged*:

$$
c_t=\frac{P_t(T)-S_t}{S_t}+\underbrace{\frac{\text{income}}{S_t}}_{\text{coupon/dividend}}\quad\text{(futures form: }c_t=\Big(\frac{S_t-F_t}{F_t}\Big)\text{)}.
$$

Equivalently, in a one-factor term-structure model where the future spot equals today's forward, the expected excess return under unchanged prices is exactly the carry.

**Carry in a no-arbitrage framework.** Under $\mathbb{Q}$ the futures price is a martingale: $F_t=\mathbb{E}^{\mathbb{Q}}_t[S_T]$. The **basis** $b_t=S_t-F_t$ therefore isolates the risk premium that the *physical* measure adds: $\mathbb{E}^{\mathbb{P}}_t[S_T-S_t]=\underbrace{(F_t-S_t)}_{\text{carry}}+\underbrace{\text{risk premium}}_{\text{expected FX/spot change}}$. Carry is the deterministic part; the stochastic part is what you are *paid* to bear.

**Carry as a cross-sectional factor.** Standardise carry within the cross-section and go long the top, short the bottom:

$$
w_t\propto \text{rank}(c_t)-\overline{\text{rank}},\qquad r^{\text{carry}}_{t+1}=\sum_i w_{i,t}\,r_{i,t+1}.
$$

This is the *same* construction as a value or momentum factor, which is why carry slots directly into a factor-allocation framework (page 03): compute the factor covariance $\Sigma_f$, then optimise or risk-balance across value / momentum / carry / defensive.

**The four styles, cross-asset (the "style" premium family):**

| Style | Signal | Economic story |
|---|---|---|
| Value | cheap vs long-run fair value | over-extrapolation reversal |
| Momentum | past 12-month return | under-reaction / flows |
| Carry | yield if prices unchanged | risk premium / term structure |
| Defensive | low beta / low vol | leverage-aversion (betting-against-beta) |

**Why carry diversifies the others.** Value and momentum are negatively correlated; carry is closest to value (both like "cheap/high-yield"), defensive is closest to nothing. The style block therefore has low average pairwise correlation - the same diversification property that makes *factor allocation* efficient (page 03).

---

### 3. Computational Implementation - carry across asset classes

Runnable (numpy). It ranks six cross-asset carry proxies, simulates a "prices unchanged plus noise" return environment, and shows the carry-tilted portfolio out-earning the equal-weight one. Stdlib + numpy.




The equal-weight portfolio earns a *negative* annualised return ($-1.6\%$) because it holds the negative-carry leg (gold) and the price noise is unhelpful over a short sample; the carry-tilted long-only portfolio earns $+1.1\%$ and the long-short carry portfolio $+5.4\%$. The carry signal, not the volatile spot, does the work - and the spot noise is exactly the **carry-crash** channel that page 05 quantifies.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Carry is compensation for crash risk.** The realised return distribution is negatively skewed: steady gains punctuated by rare large losses (the "carry crash"). A carry-tilted portfolio needs explicit tail hedging or leverage discipline.
2. **Carry and momentum disagree - by construction.** Momentum buys what is *rising*, carry buys what is *yielding*; the two can be simultaneously long and short the same asset. Diversification across styles means *tolerating* being on the wrong side of one.
3. **Carry changes regime.** In a funding crisis, FX carry reverses violently as the high-yielders depreciate; in a commodity shortage, roll yield can flip sign. Carry must be *conditioned* (page 06).
4. **Roll yield $\ne$ return.** The $(F-S)/S$ term is the *expected* carry *if the term structure holds*; a persistent backwardation can be a symptom of scarcity, not free money.

---

### 5. References

- **Koijen, Moskowitz, Pedersen & Vrugt**, "Carry," *Journal of Financial Economics* 127(2):197–225, 2018
- **Asness, Moskowitz & Pedersen**, "Value and Momentum Everywhere," *Journal of Finance* 68(3):929–985, 2013
- **Frazzini & Pedersen**, "Betting Against Beta," *Journal of Financial Economics* 111(1):1–25, 2014
- **Ilmanen**, *Expected Returns* (2011)
- **Ang**, *Asset Management* (2014)

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/03-factor-based-allocation|03 · Factor-Based Allocation]]
- Forward: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Index Hub]]
- Cross-pillar: [[pillars/01-quantitative-research/factor-investing-and-timing/02-the-factor-zoo|The Factor Zoo]] · [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|Factor Crowding & Capacity]]

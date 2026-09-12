---
title: "3.1.3 Markets, Products & Contract Mechanics"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - exchange-vs-otc
  - contract-specification
  - margin
  - cost-of-carry
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/options-fundamentals-and-markets/02-options-mechanics-and-payoffs|02 · Options Mechanics & Payoffs]].

---

### 1. Intuition & Practical Objective

The previous two pages described *contracts*; this one describes **where they live and how the plumbing constrains their prices**. The practical objective: know the difference between an exchange-traded contract (standardised, cleared, margined daily) and an OTC contract (bespoke, bilateral or CCP-cleared, collateralised under an ISDA/CSA), know what a **contract specification** pins down, and know the **conventions** - multiplier, day-count, cost-of-carry - that silently change every number you compute.

The reason this is a *fundamentals* topic and not fine print: two contracts with the same payoff can trade at different prices if their **market structure** differs. Futures settle **daily** and their variation margin earns no interest; OTC forwards settle once at $T$; the same payoff under the two structures has slightly different value (the convexity difference, Hull §5.8 and Ch 6). And a contract's *specification* - the deliverable, the settlement, the multiplier - determines which asset you can hedge with and hence what "the" price even means.

> **The one-sentence essence.** "A derivative price is the price of a *replicating portfolio*; the market structure (exchange vs OTC, clearing, margin, day-count, multiplier) determines which instruments are actually available to build that portfolio - so structure is part of the model, not a footnote to it."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Exchange vs OTC - the structural difference (Hull Ch 1, 2)

| | Exchange-traded | OTC |
|---|---|---|
| Terms | Standardised (fixed expiry cycle, size, strikes) | Negotiated per trade |
| Clearing | Central counterparty (CCP) | Bilateral, or a CCP with margin |
| Margin | Initial + daily variation, marked to market | Collateral under an ISDA credit-support annex (CSA) |
| Cash flows | Realised **daily**; variation margin does not earn interest | Realised at maturity (or on margin calls, which do earn interest) |
| Scale (Dec 2019) | $\approx$ \$96.5T notional | ≈\$558.5T notional (gross market value $\approx$\$11.6T) |

#### 2.2 Contract specification - what gets pinned down (Hull Ch 2.1)

An exchange contract specifies the **asset** (and any grade/deliverable choice), the **contract size** (multiplier), the **delivery months / expiries**, the **settlement procedure** (physical vs cash), **price quotes**, and **price/position limits**. Option-specific items (Hull Ch 10.4):

- **Expiration cycle:** standard equity options expire on the **third Friday**; strikes are spaced \$2.50 / \$5 / \$10; a **class** shares the underlying, a **series** is one strike & expiry.
- **Settlement:** index options are **cash-settled** and quoted at $100\times$ the index; equity options are $100\times$ the premium.
- **Adjustments:** cash dividends normally do **not** adjust the contract; splits adjust strike and size by $K\to K\cdot m/n$, shares $\to n/m$; stock dividends and rights issues are handled ad hoc.
- **FLEX** options allow bespoke terms within the exchange framework.

#### 2.3 Margin mechanics (Hull Ch 2.2, 10.7)

**Futures.** At the *trader* level the maintenance margin is about $75\%$ of the initial margin; the account is marked to market **daily** and any balance above the initial margin may be withdrawn. In the delivery month the contract converges to spot, because otherwise a cash-and-carry (or its reverse) locks a profit.

**Options (short positions).** Buying an option requires **full payment, no margin** (options with life $<9$ months). Writing a naked option ties up margin:

$$
\text{naked call margin}=\max\!\big(100c+20\%\,S-100\max(K-S,0),\;100c+10\%\,S\big),
$$
$$
\text{naked put margin}=\max\!\big(100c+20\%\,K-100\max(S-K,0),\;100c+10\%\,K\big),
$$

with the second term the *floor*. Broad-index obligations use $15\%$ instead of $20\%$ in the first term. The $\max(\cdot)$ structure is exactly the "at least the out-of-the-money discount, but never less than the 10% floor" rule.

#### 2.4 The cost-of-carry dictionary - one master formula (Haug §1)

Every vanilla European model is the **same formula with one variable changed**:

$$
c=Se^{(b-r)T}N(d_1)-Xe^{-rT}N(d_2),\qquad
\begin{cases}
b=r & \text{non-dividend stock (BSM 1973)}\\
b=r-q & \text{index / continuous yield }q\text{ (Merton 1973)}\\
b=0 & \text{futures / forward (Black-76)}\\
b=r-r_f & \text{currency (Garman–Kohlhagen)}
\end{cases}
$$

This is the reason §3 exposes the carry $b$ as an explicit function argument. Feed the wrong $b$ and you misprice by exactly the missing $e^{-qT}$ or $e^{-r_fT}$ factor.

#### 2.5 Day-count and quote conventions (Hull Ch 6.1)

Interest accrues under a **day-count convention**: Actual/Actual (US Treasuries), $30/360$ (US corporates), Actual/360 (US money market); Actual/365 in Australia/Canada/NZ. Bonds quote a **clean price**; the cash paid is the **dirty price** $=$ clean price $+$ accrued interest. Rate futures are quoted as $100-R$ with a fixed $ $\$/\text{bp} value: \25 per bp for a \$1M three-month contract, \$41.67 per bp for a \$5M one-month SOFR (Hull Ch 6.3).

---

### 3. Computational Implementation - the conventions in numbers

Standard library only. This turns the specification, margin and day-count rules into concrete cash amounts.



The naked-call number decomposes cleanly: $100\times5$ premium $+20\%\times100\times55= $ \$1{,}100 of stock cover, minus zero OTM discount = \$1{,}600; the $10\%$ floor is $ $\$1{,}050, so the 20\%$ branch binds. **The margin is not a fee - it is collateral, and its size is set by the exchange to cover a plausible one-day move.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong carry $b$.** The single most common pricing bug: using $b=r$ for an index (should be $r-q$), for futures ($0$), or for FX ($r-r_f$). The error is a multiplicative factor $e^{(b_{\text{wrong}}-b_{\text{right}})T}$ on the forward leg.
2. **Futures $\ne$ forward when rates are stochastic.** Equal only when $r$ is constant (Hull §5.8); otherwise futures are slightly higher/lower, and for **interest-rate** futures the difference is the convexity adjustment (Hull Ch 6.3). Treating them as identical silently misprices long-dated rate hedges.
3. **Margin vs premium confusion.** Buying an option is a *cash* outflow of the full premium ($$\$325); writing one is *collateral* (\$1{,}600) plus a contingent liability. Conflating the two wrecks both the cash-flow model and the risk model.
4. **Ignoring settlement-timing differences.** Futures variation margin earns no interest; OTC/CCP variation margin does. Over long horizons this timing difference is exactly what separates forward and futures prices.
5. **Day-count sloppiness.** Actual/360 vs Actual/365 changes the accrued interest of a rate instrument by a factor of $\approx 365/360$ - small per trade, material across a book.
6. **Assuming standardisation is universal.** Only exchange contracts are standard; the OTC market (the larger one, $\approx$\$558.5T notional) negotiates every term, so "the" market price may not exist - only a dealer quote with a bid/ask.

---

### 5. References

- **Hull**, *Options, Futures, and Other Derivatives*
- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Hull & White** (via Hull

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/02-options-mechanics-and-payoffs|02 · Options Mechanics & Payoffs]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Index Hub]]
- Next: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/04-no-arbitrage-and-bounds|04 · No-Arbitrage & Bounds]]
- Structure $\to$ pricing: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · The Pricing Formulas]] (the $b$ dictionary in closed form)
- Clearing & collateral: [[pillars/03-derivative-pricing/counterparty-risk-and-xva|Counterparty Risk & XVA]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure|Interest Rate & Term Structure]]

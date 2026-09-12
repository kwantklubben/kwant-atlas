---
title: "4.11.2 Delta, Gamma, Vega"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - greeks
  - delta
  - gamma
  - vega-theta
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/risk-factor-sensitivities/01-from-zero-intuition|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · The Greeks & Dynamic Hedging]].

---

### 1. Intuition & Practical Objective

Pillar 3 *derives* the Greeks so that it can replicate an option and price it. Here the same five numbers are read the other way round: **they are the risk factors themselves.** A desk's option book is summarised, minute to minute, by five columns - delta, gamma, vega, theta, rho - and the limits, hedges and capital are written against those columns, not against the option prices.

The practical objective of this page is to make the **aggregation** step concrete. Sensitivities are *linear in position size*: if you hold $q$ options, your exposure is $q$ times the per-option Greek. Therefore

$$
\Delta_{\text{book}}=\sum_i q_i\,\Delta_i,\quad \Gamma_{\text{book}}=\sum_i q_i\,\Gamma_i,\quad \nu_{\text{book}}=\sum_i q_i\,\nu_i,\ \dots
$$

**The book has one delta even though it has forty trades.** That collapse - from a book of instruments to a vector of risk factors - is the whole trick, and it is also where the danger lives: the sum hides the *distribution* of curvature across strikes and maturities.

The two relations to internalise:

- **Gamma–theta (the carry identity).** A delta-hedged option earns $\tfrac12\Gamma(\Delta S)^2$ when the market moves and pays $\Theta\,\Delta t$ for the passage of time; risk-neutrally they cancel exactly:
$$
\tfrac12\Gamma S^2\sigma^2=-\Theta_{\text{driftless}}\qquad(\text{Haug §2.15}).
$$
Being long gamma is being long **realised variance** and short **implied variance**. This single sentence is the P&L of every option desk.
- **Delta-neutral P&L (Hull eq. 19.3).** $\Delta\Pi\approx\Theta\,\Delta t+\tfrac12\Gamma(\Delta S)^2$ - the local expansion that every risk report is built on.

---

### 2. Mathematical Ground Truth & Derivations

**The sensitivity table (generalized BSM; Haug §2, Hull Ch 19, both verified).** Notation: $c,p$ European call/put, $b$ cost of carry, $N$ the standard normal CDF, $n(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}$, $e=e^{(b-r)T}$.

| Sensitivity | Definition | Call | Put | Sign |
|---|---|---|---|---|
| **Delta** | $\partial V/\partial S$ | $e\,N(d_1)$ | $e\,(N(d_1)-1)$ | $+/-$ |
| **Gamma** | $\partial^2 V/\partial S^2$ | $\dfrac{e\,n(d_1)}{S\sigma\sqrt T}$ | *(identical)* | $+$ |
| **Vega** | $\partial V/\partial\sigma$ | $S\,e\,n(d_1)\sqrt T$ | *(identical)* | $+$ |
| **Theta** | $-\partial V/\partial T$ | $-\dfrac{S e\,n(d_1)\sigma}{2\sqrt T}-(b-r)Se\,N(d_1)-rXe^{-rT}N(d_2)$ | $-\dfrac{Se\,n(d_1)\sigma}{2\sqrt T}+(b-r)Se\,N(-d_1)+rXe^{-rT}N(-d_2)$ | usually $-$ |
| **Rho** | $\partial V/\partial r$ | $T X e^{-rT}N(d_2)$ | $-T X e^{-rT}N(-d_2)$ | $+/-$ |

**Conventions that matter in a risk system.** Vega and rho are quoted **per 1 vol/rate point** $=$ raw$/100$; theta **per day** $=$ raw$/365$. Gamma is a *pure* second derivative and has no point-scaling convention - a frequent source of cross-desk confusion. Note the structural facts a risk manager exploits: **gamma and vega are identical for calls and puts**, gamma peaks at-the-money and decays as $1/\sqrt T$; ATM vega *grows* as $\sqrt T$ (it is gamma's scale factor $S^2T$); **theta is the most negative at-the-money**; **rho is negligible for short-dated options**.

**The key identities (Haug §2.15, §2.3.3).**

$$
\Gamma=-\frac{2\Theta_{\text{driftless}}}{S^2\sigma^2},\qquad \nu=\Gamma\,\sigma S^2 T,\qquad \text{Vanna}=\frac{\partial\Delta}{\partial\sigma}=-e\,n(d_1)\frac{d_2}{\sigma},\qquad \text{Volga}=\frac{\partial^2V}{\partial\sigma^2}=\nu\frac{d_1d_2}{\sigma}.
$$

Vanna is the sensitivity of *delta* to vol - the reason a delta-hedged book acquires delta when the vol surface shifts. Volga is the convexity in vol - the reason long-dated wings pay so well in a vol spike. Both are **cross-Greeks**, and both live in the second-order matrix $H$ of [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes]].

**Greeks of forwards and futures (Hull eq. 19.5/19.6).** For a forward contract on an asset with yield $q$: $\Delta=e^{-qT}$; for a **futures** contract: $\Delta=e^{(r-q)T}$, and the hedge ratio is $H_F=e^{-(r-q)T}H_A$. The futures delta is *not* 1 - the daily settlement makes a futures position a levered spot position, which is why "hedging with futures" needs a scaling that "hedging with stock" does not.

---

### 3. Computational Implementation - the Haug cross-check and a real book

Two blocks: first reproduce the Haug Table 2-3 numbers that Pillar 3 verified, so the shared engine is proven; then aggregate a two-leg book and derive the delta hedge. Stdlib only.




**Read the aggregation.** The book is **long gamma (+1.38)** and **short theta (−1.27/day)** - the classic long-volatility posture: it makes money when the market moves and bleeds when it does not, and the gamma–theta identity says those are the *same* trade viewed from two sides. Note the sign discipline: **put gamma is positive and equals call gamma**, so it is the *position* that sets the sign - the short put leg contributes $(-50)\times0.027086=-1.3543$ of gamma, i.e. it *reduces* the book's long-gamma, while its delta contribution $(-50)\times(-0.283374)=+14.17$ *adds* to the book's delta. **Netting delta is arithmetic; netting gamma requires getting both the instrument sign and the position sign right, and they are different questions.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A delta-hedged book is not a risk-free book - it is a gamma book.** The hedge removes the first-order term only. Over one step the residual P&L is $\tfrac12\Gamma S^2[(\Delta S/S)^2-\sigma^2\Delta t]$, zero in expectation under $\mathbb{Q}$, but realised with standard deviation proportional to $|\Gamma|S^2\sigma\sqrt{\Delta t}$. Selling a delta-hedged book is selling insurance.
2. **Delta is regime-dependent through the moneyness.** $\Delta\to1$ deep ITM, $\Delta\to0$ deep OTM, and $\Gamma\to0$ in both limits - so the *same* notional can be a delta position or a gamma position depending on where spot sits. A book near the money can flip its gamma sign on a $2\%$ move.
3. **Vega is a *surface* sensitivity, not a scalar one.** $\nu$ assumes one $\sigma$; real books have a smile, so what is actually held is a **bucket** vega (per expiry) and **skew/smile** vega. Hedging a single aggregated vega number against a single ATM vol leaves the surface shape unhedged (see [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]]).
4. **Rho sign changes with the instrument.** Call rho $>0$, put rho $<0$ for stock options - but for **futures** options both are negative ($\rho=-Tc$, Haug §2.16). A book quoted in futures options gets its rate risk backwards if it uses equity-option intuition.
5. **Theta must be reported in the right time unit.** Theta per calendar day ($/365$) and per trading day ($/252$) differ by $45\%$; a desk that hedges to a per-trading-day theta limit while reporting per-calendar-day will always look comfortably inside the limit.

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) - Ch 19 §19.1–19.10 ($\Delta$-neutral P&L eq. 19.3, $\Theta+rS\Delta+\tfrac12\sigma^2S^2\Gamma=r\Pi$ eq. 19.4, Greeks of forwards/futures eq. 19.5/19.6, delta/gamma/vega-neutral construction, theta per day/trading day). *Verified in the corpus (`hull_ch19-23.md`).*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) - §2.3–2.16 (the full Greek set and the per-point/per-day scaling), §2.15 (the gamma–theta identity), §2.16 (futures-option rho). *Numerically re-verified here against Table 2-3.*
- **Taleb, Nassim Nicholas**: *Dynamic Hedging* (Wiley, 1997) - the practitioner's account of gamma/vega books, pin risk, and why aggregated Greeks lie.
- **J.P. Morgan / RiskMetrics**: *Technical Document*, 4th ed. (1996) - §6, the risk-factor mapping for options and the delta-gamma treatment of non-linearity.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · The Greeks & Dynamic Hedging]] (where these formulas are derived) · [[pillars/04-quantitative-risk/risk-factor-sensitivities/01-from-zero-intuition|01 · From Zero]]
- Continue: [[pillars/04-quantitative-risk/risk-factor-sensitivities/03-rates-and-key-rate-duration|03 · Rates & Key-Rate Duration]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] (why a scalar vega is not enough) · [[pillars/04-quantitative-risk/risk-factor-sensitivities/06-advanced-extensions|06 · Delta–Gamma VaR]]

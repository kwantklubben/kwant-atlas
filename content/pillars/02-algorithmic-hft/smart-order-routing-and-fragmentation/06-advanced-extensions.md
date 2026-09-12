---
title: "2.5.6 Advanced Extensions"
tags:
  - pillar-algorithmic-hft
  - smart-order-routing
  - latency
  - toxic-flow
  - advanced
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/03-sor-logic|03 - SOR Logic]] and [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/05-failure-modes-and-practice|05 - Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The greedy SOR of page 03 minimizes $\sum_i q_i(p_i+f_i)$ - price plus fee. Production routers minimize a **richer** effective price that also prices the two risks the basic objective ignores: **latency** (the quote may move before you arrive) and **toxicity** (the counterparty on the other side may be informed). This page builds the full objective, solves it, and shows how latency alone flips the optimal venue.

The advanced objective replaces the naive per-share cost with
$$
\hat p_i \;=\; p_i+f_i+\underbrace{\sigma\sqrt{L_i}}_{\text{latency/adverse-move}}+\underbrace{k\,\theta_i}_{\text{toxicity}},
$$
where $L_i$ is the venue's latency in ms, $\sigma$ the per-$\sqrt{\text{ms}}$ price diffusion, $\theta_i$ the venue's toxic-flow measure (e.g. VPIN or a realized-spread proxy), and $k$ a risk aversion. Three consequences follow:

1. **A cheaper quote can be a worse route.** If a venue's price advantage is smaller than its $\sigma\sqrt{L_i}$ penalty, the router must skip it - routing *away* from the toxic or too-slow quote.
2. **There is a crossover latency.** For any two venues there exists an $L^*$ below which the better-quoted venue wins and above which the faster venue does; the router should know it.
3. **Toxicity is venue-specific and time-varying.** Lit venues, inverted venues, and dark pools carry different $\theta_i$; SOR blends price, fee, latency, and toxicity dynamically.

> **The one-sentence essence.** "A production SOR minimizes quote + fee + $\sigma\sqrt{L}$ + toxicity, so it will deliberately route away from the venue displaying the best price when that venue is too slow or too toxic to be worth it."

---

### 2. Mathematical Ground Truth & Derivations

**The latency-aware objective.**
$$
\boxed{\;\min_{\{q_i\}}\;\sum_i q_i\big[\,p_i+f_i+\sigma\sqrt{L_i}\,\big]\quad\text{s.t.}\quad\sum_i q_i=Q,\;\;0\le q_i\le S_i,\;}
$$
a linear program solved by the same **greedy merge** as page 03, but now on the latency-adjusted effective price. The $\sigma\sqrt{L_i}$ term is the expected adverse move over $L_i$ ms (Brownian scaling from pages 05–06).

**Crossover latency.** Venue $i$ (better quote) vs venue $j$ (faster). Equal effective price when
$$
p_i+f_i+\sigma\sqrt{L_i}=p_j+f_j+\sigma\sqrt{L_j}\;\Longrightarrow\;\sqrt{L_j}=\frac{p_i+f_i-p_j-f_j}{\sigma}+\sqrt{L_i},
$$
so if $j$'s quoted advantage is $\Delta=p_i+f_i-(p_j+f_j)>0$ (per share, $i$ worse), venue $j$ is preferable for any $L_j<L^*$. Below the crossover the fast venue wins *even though its quote is worse*.

**Toxicity term.** Let $\theta_i$ be a venue's flow-toxicity (probability the counterparty is informed). The cost of taking liquidity is the expected adverse move conditional on trading against informed flow, $\theta_i\,(E[\text{adverse}\mid \text{informed}])$; a common one-parameter reduction is $k\theta_i$ with $k$ the conditional adverse move. VPIN and realized-spread are the standard empirical $\theta_i$ estimates ([[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]]).

**Limit vs market: the fill-probability term.** A maker route replaces $+f_t$ with $-f_m$ (a rebate) but multiplies the gain by the fill probability $\pi_\text{fill}$:
$$
\mathbb{E}[\text{maker cost}]=-f_m\,\pi_\text{fill}+\text{adverse-selection cost}\times\pi_\text{fill}+\text{opportunity cost}\times(1-\pi_\text{fill}),
$$
so rebate-chasing requires $\pi_\text{fill}$ to justify it - the link to [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]].

**Cointegration/uniqueness underpinning.** The objective is well-posed because venue prices are cointegrated to one efficient price (Hasbrouck Ch 10); the cross-venue basis is stationary, so the "best" venue is a well-defined, estimable quantity rather than an artifact.

---

### 3. Computational Implementation - latency-aware routing

Show that adding $\sigma\sqrt{L}$ flips the optimal venue, and compute the crossover latency. Standard library only; **re-executed and reproduced**.




**Read the numbers.** Venue **B** has the best raw quote (100.000) *and* a zero fee - a price-only router sends the whole order there. But B is 8 ms slow, and $\sigma\sqrt{L}=0.02\sqrt{8}=0.0566$ makes its true all-in cost **100.05657**, far worse than A's 100.00947. The latency-aware SOR routes 600 to **A** and 400 to **C** for a true cost of **100.01126** - saving **$45.31 per 1,000 shares** over the naive choice. And the crossover is brutal: B would only deserve the order if its latency fell below **0.2243 ms**, i.e. below every microsecond-tier venue's realistic floor. The "cheapest" quote was the most expensive route.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Price-plus-fee is not enough.** Any router without $\sigma\sqrt{L}$ will systematically prefer slow venues whose displayed edge is illusory - the single largest structural deficiency of a naive SOR.
2. **Toxicity is hidden.** $\theta_i$ is not in the quote; a venue can display a tight spread and still be where the informed flow goes. Without a toxicity term the router is a magnet for adverse selection ([[pillars/06-market-making/toxic-order-flow-and-vpin/index|VPIN]]).
3. **Rebate-chasing without fill probability.** The maker-rebate term $-f_m\pi_\text{fill}$ can be negative in expectation once missed fills and adverse selection are counted; posting for the rebate is a trade, not free money.
4. **Static objective in a moving market.** $\sigma$, $L_i$, and $\theta_i$ change intraday (news, volatility regimes). A router with fixed parameters is mis-optimized exactly when it matters most; the objective must be re-estimated on rolling windows.

---

### 5. References

- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007)
- **Easley, López de Prado & O'Hara** - "Flow toxicity and liquidity in a high-frequency world," *RFS* 25(5), 2012 (VPIN); and "The microstructure of the flash crash," *JPM*, 2011. *The toxicity measure $\theta_i$; `corpus/titles/refs/33Easley2012_flow_toxicity_and_liquidity_in.pdf`.*
- **Biais, Foucault & Moinas** - "Equilibrium fast trading," *JFE* 116(2), 2015. *The economics of the latency term.*
- **Colliard & Foucault** - "Trading fees and efficiency in limit order markets," *RFS* 25(11), 2012, and **Foucault, Pagano & Röell** - *Market Liquidity* (2013)

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Index Hub]]
- Toxicity: [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]]
- Fill probability & maker routes: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Latency & hardware: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]
- Scheduling the children: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms: VWAP, TWAP, POV]]

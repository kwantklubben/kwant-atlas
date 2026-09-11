---
title: "6.7.6 Advanced Extensions"
tags:
  - pillar-market-making
  - market-impact
  - transient-impact
  - propagator
  - cross-impact
  - no-dynamic-arbitrage
---

**Basic Prerequisites:** [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]] and [[pillars/06-market-making/market-impact-and-depth/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The linear and square-root models are *static*: impact appears instantly and either persists forever (permanent) or vanishes (temporary). Reality is **transient**: the price impact of a trade *builds up, peaks, and then decays over time* according to a kernel — and the shape of that kernel, not the size of the trade alone, determines whether a strategy can be manipulated. This page is the consolidation layer: the **propagator / transient-impact models** used in modern execution research, the constraints no-arbitrage imposes on them, and the phenomena (cross-impact, dark pools, Hawkes order flow) that lie just beyond the folder.

**Why the transient view matters.** Two trades of the same size have different impact depending on *when they occur relative to each other*. Selling 10% of ADV in one day is not the same as selling it over ten days: in the propagator picture the first trade's impact decays before the second arrives, so the realised cost is schedule- and path-dependent in a way the static decomposition cannot express. This is the model class behind the "impact decay" curves you see on execution desks, and it is the natural bridge to Pillar 2's scheduling problem.

> **The one-sentence essence.** "Impact is a convolution of order flow with a decay kernel — $S_t=S_0+\int_0^t h(\dot X_s)G(t-s)\,ds$ — and no-dynamic-arbitrage pins the kernel's tail ($G(\tau)\sim\tau^{-\gamma}$) to the impact function's concavity ($h(x)\sim|x|^\delta$) via $\gamma+\delta\ge1$."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The transient / propagator model

The **Bouchaud propagator** (and Gatheral's "JG model") writes the impact of a continuous execution strategy $X$ as a convolution:

$$
S_t=S_0+\int_0^t h\big(\dot X_s\big)\,G(t-s)\,ds,
$$

where $h$ is the instantaneous impact function (linear $h(x)=cx$, or concave $h(x)=c|x|^\delta\mathrm{sgn}(x)$) and $G$ is the **decay kernel** (the "propagator"). The discrete version applies a price move $h(\xi_{t_k})G(t_n-t_k)$ at each trade time $t_k$. The three headline results:

1. **Temporary + permanent are limits.** $G\equiv$ const $\Rightarrow$ all impact permanent; $G\to0$ instantly $\Rightarrow$ all impact temporary. Real markets sit between: $G$ decays slowly (a power law), so impact is *mostly* temporary but with a persistent tail.
2. **The decay can be inferred from the impact curve.** For a single metaorder, $G$ is (up to a factor) the *derivative of the post-trade price-reversion curve* — the observable object. Empirically `impact decays as a power law $G(\tau)\sim\tau^{-\gamma}$` with $\gamma\approx0.5$ (Bouchaud et al. 2004), matching the Bouchaud response relation $\beta=(1-\gamma)/2$ of page 04.
3. **The model reproduces the square-root law.** With $\delta=\tfrac12$ and $G(\tau)=\tau^{-\gamma}$, the peak impact of a metaorder of size $Q$ scales as $Q^{1/2}$ (§3), reconciling the static square-root fit of page 04 with a dynamic mechanism.

#### 2.2 No-dynamic-arbitrage (the key constraint)

Gatheral (2010) imposes that **no round-trip strategy can extract a riskless profit from its own price impact**. For $h(x)=c|x|^\delta\mathrm{sgn}(x)$ and $G(\tau)=\tau^{-\gamma}$:

$$
\boxed{\ \text{price manipulation exists}\iff \gamma+\delta<1\ }.
$$

Two structural consequences that every production impact model must satisfy:

- **Exponential decay is forbidden with nonlinear impact.** If $G$ is finite and continuous at $t=0$ (as exponential decay is) and $h$ is nonlinear, the model admits manipulation (Gatheral–Schied Prop. 22.14). The kernel must be *singular* at zero — impact decay must be a power law.
- **The empirical exponents sit on the boundary.** $\delta\approx0.5,\ \gamma\approx0.5\Rightarrow\gamma+\delta\approx1$: observed impact is *just barely* arbitrage-free. This is a genuine, surprising constraint from data + theory.

#### 2.3 Nonlinear impact in the execution problem

Almgren (2003) extends the linear execution problem to nonlinear impact functions and adds a "trading-enhanced risk" term: when impact is nonlinear, the optimal schedule is **no longer the closed-form $\sinh$ trajectory** — it must be solved numerically — but the qualitative behaviour survives (front-load when risk-averse, spread out when cost-averse). This is where the microstructure impact model (this folder) meets the stochastic-control scheduler (Pillar 2).

#### 2.4 Beyond a single asset: cross-impact

Trading one asset moves *correlated* assets' prices (a large S&P futures sell lifts the prices of its constituents' sells and moves other index products). The generalization is a **cross-impact matrix** $\Lambda_{ij}$: the price change of asset $i$ depends on the flow in asset $j$. The diagonal is Kyle's $\lambda$; the off-diagonals encode correlation and portfolio effects and are the frontier of practical impact modelling. (Almgren et al. 2005 explicitly neglect cross-impact — a stated limitation, not an oversight.)

#### 2.5 The order-flow process underneath

The propagator's $G$ is not free: it must be consistent with the *statistical* properties of order flow. Order signs are long-memory (autocorrelation $\sim\tau^{-\gamma}$ with $\gamma\approx0.5$, well described by a FARIMA or Hawkes process), and the empirically-correct choice of $G$ is the one that keeps the price a martingale with the right variance. This consistency requirement — "get the impact law and the order-flow memory from the same model" — is the deep content of Bouchaud, Farmer & Lillo (2009).

---

### 3. Computational Implementation — transient impact in action

Simulate a metaorder over a propagator with a power-law kernel $G(\tau)=\tau^{-\gamma}$. Show (i) the impact path building to a peak and then decaying, (ii) the effect of the decay exponent, and (iii) the square-root scaling of the peak impact with size. Stdlib only.

```python
import math

def impact_path(Q, T, M, gamma, delta, c=1.0):
    """Propagator impact: S_t - S_0 = sum_{s<t} h(xi_s) G(t-s),
       h(x) = c|x|^delta sign(x),  G(tau) = tau^-gamma.
       A metaorder of size Q executes uniformly over [0,T], then stops."""
    xi = [Q / T if t < T else 0.0 for t in range(M)]
    return [sum(c * (abs(xi[u]) ** delta) * ((t - u) ** (-gamma))
                for u in range(t) if xi[u]) for t in range(M)]

Q, T, M = 10000.0, 100, 300
for g in (0.5, 1.0):
    p = impact_path(Q, T, M, g, 0.5)
    peak = max(p); peak_t = p.index(peak)
    tail = p[peak_t + 100]
    print(f"gamma={g}: peak={peak:.3f} at t={peak_t};  100 steps after end={tail:.3f} ({100*tail/peak:.1f}% of peak)")

sizes = [100, 300, 1000, 3000, 10000, 30000]
peaks = [max(impact_path(q, T, M, 0.5, 0.5)) for q in sizes]
lx = [math.log(s) for s in sizes]; ly = [math.log(p) for p in peaks]
mx = sum(lx)/len(lx); my = sum(ly)/len(ly)
slope = sum((a-mx)*(b-my) for a,b in zip(lx,ly)) / sum((a-mx)**2 for a in lx)
print("peak impact by size:", [round(p, 2) for p in peaks])
print(f"log-log slope of peak impact vs Q = {slope:.4f}   (square-root law = 0.5)")
```

```
gamma=0.5: peak=185.896 at t=100;  100 steps after end=82.697 (44.5% of peak)
gamma=1.0: peak=51.874 at t=100;  100 steps after end=6.907 (13.3% of peak)
peak impact by size: [18.59, 32.2, 58.79, 101.82, 185.9, 321.98]
log-log slope of peak impact vs Q = 0.5000   (square-root law = 0.5)
```

Three results, straight from the propagator:
- **Impact peaks at the end of execution ($t=100$) and then decays** — the transient behaviour the static models miss.
- **Slower decay ($\gamma=0.5$) leaves 44.5% of the peak 100 steps after execution; fast decay ($\gamma=1.0$) leaves only 13.3%.** This is the "resilience" dial, now a continuous kernel rather than a binary permanent/temporary switch.
- **Peak impact scales as $Q^{0.5000}$** — the transient model *generates* the square-root law of page 04 rather than assuming it, with $\delta=\gamma=\tfrac12$ sitting exactly on Gatheral's no-arbitrage boundary $\gamma+\delta=1$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **An impact model that admits manipulation.** Any kernel that is finite/continuous at zero (exponential, Gaussian, a discrete grid) combined with nonlinear impact generates arbitrage (Gatheral–Schied). If your backtest "profits" by trading in circles, the impact model is the culprit, not a clever alpha.
2. **Estimating $G$ from too-short a window.** The decay exponent $\gamma\approx0.5$ is a *long-horizon* property; fitting it on a few minutes of data recovers an artefact of the sampling window. Impact decay estimates require the full reversion curve.
3. **Separating permanent from transient in one dataset.** The two are only jointly identified under a normalisation (in the generalized-Roll language, the structural {$\lambda,c,\sigma_u^2$} are under-identified from two autocovariances, though $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ *is* identified). Assuming one is zero — the usual "everything is temporary" or "everything is permanent" simplification — biases the other.
4. **Ignoring cross-impact in portfolio execution.** Diagonal-only models understate the cost of trading correlated baskets: the portfolio-level impact is larger than the sum of single-name impacts.
5. **Feeding a mis-specified kernel into an optimiser.** A scheduler (Pillar 2) is only as good as the impact model it consumes; optimising over a linear impact function while reality is square-root produces a schedule that is wrong in a *systematic, size-dependent* way.
6. **Assuming the order-flow process is memoryless.** If the underlying $G$/order-flow pair is inconsistent (e.g. short-memory flow with a long-memory kernel), the model's implied price variance no longer grows linearly in time — a simple, detectable inconsistency that is often ignored.

---

### 5. Canonical Literature & Study References

- **Gatheral, J. (2010)**, *No-dynamic-arbitrage and market impact*, Quantitative Finance 10(7), 749–759. *The propagator model, $\gamma+\delta\ge1$, exclusion of exponential decay. Primary PDF in corpus (`42Gatheral2010_...`).*
- **Gatheral, J. & Schied, A. (2013)**, *Dynamical models of market impact and algorithms for order execution*, in *Handbook on Systemic Risk*. *Rigorous synthesis; Theorem 22.13, Prop. 22.14, JG model (22.21), Remark 22.15. Primary PDF in corpus (`46_Gatheral_2013_...`).*
- **Bouchaud, J.-P., Gefen, Y., Potters, M. & Wyart, M. (2004)**, *Fluctuations and response in financial markets: the subtle nature of 'random' price changes*, Quantitative Finance 4(2), 176–190. *The propagator model and power-law impact decay.*
- **Bouchaud, J.-P., Farmer, J. D. & Lillo, F. (2009)**, *How markets slowly digest changes in supply and demand*. *Order-flow memory (FARIMA/Hawkes), impact concavity, and the consistency requirement. Primary PDF in corpus.*
- **Almgren, R. (2003)**, *Optimal execution with nonlinear impact functions and trading-enhanced risk*, Applied Mathematical Finance 10(1), 1–18. *Nonlinear impact in the execution problem. Primary PDF in corpus.*
- **Obizhaeva, A. & Wang, J. (2013)**, *Optimal trading strategy and supply/demand dynamics*, J. Financial Markets 16(1), 1–32. *Resilience and the block-ramp-block strategy.*
- **Bouchaud, J.-P., Bonart, J., Donier, J. & Gould, M. (2018)**, *Trades, Quotes and Prices: Financial Markets Under the Microscope*, CUP. *Book-length consolidation of the propagator/econophysics programme.*
- **Cartea, Á., Jaimungal, S. & Penalva, J. (2015)**, *Algorithmic and High-Frequency Trading*, CUP. *The stochastic-control counterpart; market impact models within the execution/market-making framework.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-impact-and-depth/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/market-impact-and-depth/04-the-square-root-law|04 · The Square-Root Law]] · [[pillars/06-market-making/market-impact-and-depth/index|Index Hub]]
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss Optimal Execution (Pillar 2)]] (the scheduler that consumes the transient model) · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]] (impact as a priced state variable)
- Related in-pillar: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (the informational driver of permanent impact) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (where the order-flow memory and book shape are observed) · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov Optimal Quoting]] (the maker's side of the same impact story)

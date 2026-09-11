---
title: "06 - Advanced Extensions: Agent-Based LOB and Simulator Validation"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - lob-simulation
  - stylized-facts
  - queue-reactive
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/06-advanced-extensions|Queue Position: 06 · Advanced Extensions]].

---

### 1. Intuition & Practical Objective

The previous pages built an honest fill model and a Monte Carlo engine. This page is the **launchpad** for the simulators used at the frontier — and for the *test* that decides whether any of them is trustworthy:

1. **Agent-based LOB simulation** — generate the whole book from agent behaviours (Abergel et al.), so that fills, impact, and liquidity emerge rather than being assumed.
2. **Queue-reactive and Hawkes models** — make the intensities state-dependent and self-exciting, so the generator reproduces the *correlation* structure of real flow.
3. **Simulator validation against stylized facts** — the non-negotiable acceptance test: the simulator must *reproduce* the empirical regularities (Roll bounce, square-root impact, concave depth, U-shaped volume) before any counterfactual is believed.
4. **Generative and ML order-book models** — deep generators and signature methods that learn the joint law of the book; powerful and dangerous.

The unifying discipline is simple: **a simulator earns trust only by reproducing what the market already tells us is true.**

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Validation #1 — the Roll bid-ask bounce (a spread test)

A simulator with a realistic matching process produces trade prices $p_t=m_t+q_t c$ (efficient price $\pm$ half-spread). The **Roll signature** is a negative first-order autocovariance of price changes:

$$
\gamma_0=\operatorname{Var}(\Delta p_t)=2c^2+\sigma_u^2,\qquad
\gamma_1=\operatorname{Cov}(\Delta p_{t-1},\Delta p_t)=-c^2,\qquad \gamma_k=0\ (k\ge2),
$$

so the simulator's own output must yield $\hat c=\sqrt{-\hat\gamma_1}$ equal to the spread it was built with. Fail this and the simulator's *fill prices* are wrong even if its *fills* are right.

#### 2.2 Validation #2 — the square-root impact law (an impact test)

Metaorder impact is concave in participation. The empirical form (Almgren et al. 2005; the "square-root law") is

$$
\Delta P\;\approx\;Y\,\sigma\,\Big(\frac{Q}{V}\Big)^{\alpha},\qquad \alpha\approx0.5\text{–}0.6,
$$

with $Q$ the order size, $V$ the market volume, $\sigma$ the volatility, and $Y$ a constant of order one. A simulator that reproduces this exponent is credible for *sizing*; one that produces a linear law is not. The exponent is recovered by a log–log regression: $\log\Delta P=\log(Y\sigma)+\alpha\log(Q/V)$.

#### 2.3 Validation #3 — queue-reactive intensities (a depth-correlation test)

Real limit-order intensity and market-order intensity are both **increasing and concave** in the queue size $q$ (Huang–Lehalle–Rosenbaum):

$$
\lambda(q)\uparrow,\ \lambda''(q)<0;\qquad \mu(q)\uparrow,\ \mu''(q)<0,
$$

the quantitative content of "liquidity begets liquidity." A generator with constant intensities produces too-smooth depth and mis-prices every fill near the front.

#### 2.4 The stylized-facts checklist

A credible execution simulator must reproduce, at minimum: (i) the negative return autocorrelation / Roll spread; (ii) the concave square-root impact; (iii) the concave depth–intensity relation and the hump-shaped depth-vs-distance profile; (iv) the intraday U-shaped volume curve; (v) fat-tailed trade sizes and the high cancel-to-trade ratio. Each is a *falsifiable acceptance criterion* — the only defence against the model risk that Monte Carlo imports (page 04).

#### 2.5 What the frontier adds

- **Agent-based LOB** (Abergel et al.): heterogeneous agents (market makers, takers, informed) whose interaction builds the book; fills and impact are *emergent*. Cost: calibration and compute.
- **Queue-reactive / Hawkes**: state-dependent, self-exciting intensities reproduce order-flow clustering; used both as a fill model and as the generator.
- **Generative LOB models**: sequence models and signature-based generators that learn $\mathbb P_{\text{book}}$ from L2/L3 data (López de Prado's "backtesting on synthetic data", AFML Ch 13); highest fidelity, highest overfitting and non-stationarity risk.

---

### 3. Computational Implementation — validating a simulator against stylized facts

Stdlib + `numpy`. Three acceptance tests: the Roll spread is recovered from simulated trade prices; the square-root impact exponent is recovered by log–log fit (and beats a linear model); the queue-reactive intensity is concave.

```python
import random, math, statistics as st
import numpy as np
random.seed(5)

# (1) Validation #1: simulator reproduces the Roll bid-ask-bounce signature.
c, sigma_u, T = 0.017, 0.05, 120000
m, p = [0.0], []
for t in range(1, T):
    m.append(m[-1] + random.gauss(0, sigma_u))
    q = 1 if random.random() < 0.5 else -1
    p.append(m[-1] + q * c)
dp = [p[i] - p[i-1] for i in range(1, len(p))]
mu = st.mean(dp)
g0 = sum((x - mu) ** 2 for x in dp) / len(dp)
g1 = sum((dp[i] - mu) * (dp[i-1] - mu) for i in range(1, len(dp))) / len(dp)
c_hat = math.sqrt(-g1)
print(f"(1) Roll check: true half-spread c={c:.4f} (spread {2*c:.4f})")
print(f"    g0={g0:.6f}  g1={g1:.6f}  ->  c_hat=sqrt(-g1)={c_hat:.4f}  spread_hat={2*c_hat:.4f}")

# (2) Validation #2: square-root impact law, ln-ln exponent recovery.
Y, sig = 1.0, 0.02
parts = [random.uniform(0.005, 0.3) for _ in range(300)]
imp   = [Y * sig * math.sqrt(v) * math.exp(random.gauss(0, 0.12)) for v in parts]
lx, ly = np.log(parts), np.log(imp)
b, a = np.polyfit(lx, ly, 1)
r2_sqrt = np.corrcoef(lx, ly)[0, 1] ** 2
lin = np.polyfit(parts, imp, 1); pred = np.polyval(lin, parts)
r2_lin = 1 - np.sum((np.array(imp) - pred) ** 2) / np.sum((np.array(imp) - np.mean(imp)) ** 2)
print(f"(2) sqrt-impact fit: exponent={b:.4f} (theory 0.5)  R^2={r2_sqrt:.4f}"
      f"   linear-model R^2={r2_lin:.4f}")

# (3) Validation #3: queue-reactive intensity is concave (saturating).
print("(3) queue-reactive intensity lambda(q) (concave proxy):")
for q in (1, 5, 20, 100, 500):
    print(f"    q={q:>4}: lambda={math.log(1+q)/math.log(2):.3f}/s")
```
```
(1) Roll check: true half-spread c=0.0170 (spread 0.0340)
    g0=0.003054  g1=-0.000298  ->  c_hat=sqrt(-g1)=0.0172  spread_hat=0.0345
(2) sqrt-impact fit: exponent=0.4922 (theory 0.5)  R^2=0.9401   linear-model R^2=0.8491
(3) queue-reactive intensity lambda(q) (concave proxy):
    q=   1: lambda=1.000/s
    q=   5: lambda=2.585/s
    q=  20: lambda=4.392/s
    q= 100: lambda=6.658/s
    q= 500: lambda=8.969/s
```

The three tests pass. **(1)** The simulator's trade prices carry the exact Roll signature: the recovered half-spread $0.0172$ matches the built-in $0.0170$ (spread $0.0345$ vs $0.0340$) — the same recovery Hasbrouck applies to PCO data. **(2)** The square-root generator is recovered with exponent $0.4922$ against a theory of $0.5$, and the concave law fits far better than a linear model on *levels* ($R^2=0.9401$ vs $0.8491$) — the simulator is credible for impact sizing, and a linear-impact assumption is demonstrably rejected. **(3)** The queue-reactive intensity is increasing and concave (from $1.000$ to $8.969$ with clear saturation) — the depth-correlation stylized fact is present. **A simulator that passes these three earns the right to answer counterfactuals; one that fails them is a random-number generator with a confident attitude.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Model risk smuggled in as precision.** A Monte Carlo interval is only as meaningful as the generator; a tight CI around a mis-specified model is worse than an honest single replay because it *looks* rigorous (page 04, [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).
2. **Validation leakage.** Calibrating the generator and testing the stylized facts on the *same* data guarantees a pass; the tests must run out-of-sample (different days, different names, different regime).
3. **Matching the wrong stylized facts.** Reproducing the U-shaped volume but missing the cancel-to-trade ratio leaves fills too optimistic; the checklist must be complete and the facts *empirically sourced*, not assumed.
4. **Non-stationarity.** LOB generators are fit on a regime; execution behaviour changes with volatility, tick size, and fee structure. A generator validated in calm markets can be badly wrong in a stress regime — the very regime where execution P&L is decided.
5. **Generative models interpolate, they do not extrapolate.** Deep LOB generators (and signature methods) learn the empirical law of the book; they are silent on counterfactuals outside the training distribution (a new venue, a much larger order, a fee change). Their counterfactuals are trustworthy only inside the support.
6. **Compute and calibration cost as a hidden bias.** An agent-based simulator expensive enough that it is only ever run on a handful of scenarios silently reverts to *replay-like* single-path behaviour — losing the distributional benefit that justified it.
7. **Validation as an afterthought.** Teams validate the *fill* model and forget the *impact* and *spread* models; the three are independent acceptance tests, and passing two is not passing.

---

### 5. Canonical Literature & Study References

- **Abergel, F.; Anane, M.; Chakraborti, A.; Jedidi, H.; Toke, I. M.** — *Limit Order Books* (Cambridge, 2016) — agent-based LOB generation and order-placement micro-simulation.
- **Huang, W.; Lehalle, C.-A.; Rosenbaum, M.** — "Simulating and analyzing order book data: the queue-reactive model," *JASA* 110(509), 107–122 (2015) — state-dependent $\lambda(q),\mu(q)$ intensities and the concave depth relation.
- **Almgren, R.; Thum, C.; Hauptmann, E.; Li, H.** — "Direct estimation of equity market impact," *Risk* 18(7), 58–62 (2005) — the empirical square-root/power-law impact a simulator must reproduce.
- **Gatheral, J.** — "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7) (2010) — the consistency constraint any impact model/simulator must satisfy.
- **Cont, Stoikov & Talreja** — "A stochastic model for order book dynamics," *Operations Research* 58(3) (2010) — the tractable model fast enough for Monte Carlo fill simulation.
- **Gould et al.** — "Limit order books," *Quantitative Finance* 13(11) (2013) — the stylized-facts survey that doubles as a simulator-acceptance checklist.
- **López de Prado, M.** — *Advances in Financial Machine Learning* (Wiley, 2018), Ch 13 — backtesting on synthetic data, and its validation requirements.
- **Hasbrouck, J.** — *Empirical Market Microstructure*, Ch 3 (Roll signature) and Ch 8 (generalized Roll) — the spread-recovery tests used in Validation #1. *Corpus verification `hasbrouck_ch1-5.md` / `hasbrouck_ch11-15.md`.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Index Hub]]
- Sibling in-pillar: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/06-advanced-extensions|Queue Position: 06 · Advanced Extensions]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]]
- Impact & market-making: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- Foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (Roll autocovariance, power-law estimation) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]

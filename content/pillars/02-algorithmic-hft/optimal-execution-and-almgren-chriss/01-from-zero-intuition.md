---
title: "01 - Optimal Execution from Zero: Why Big Orders Are Hard"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - intuition
  - market-impact
---

**Basic Prerequisites:** None. (For the impact-model view, [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]].)

---

### 1. Intuition & Practical Objective

You want to sell 1,000,000 shares of a stock trading at \$50. Your position is worth \$50m. The screen says \$50.00. **You cannot get \$50.00.** Try to sell the whole block in one click and you sweep every bid down to \$49.50 — you collect maybe \$49.7m. Work the order over three weeks and the price may drift anywhere, and the position is a \$50m bet you did not intend to hold. That is the entire problem in one paragraph.

This page builds the *why* with **no prior math needed**. Three ideas carry the whole subject:

1. **The cost of speed is market impact.** Pushing size into a book of finite depth moves the price against you. The harder you push, the worse each incremental share fills. Impact is the rent you pay for immediacy.

2. **The cost of patience is timing risk.** While you still hold shares, the market moves. Volatility doesn't care about your intentions. Holding inventory is taking a position.

3. **They trade off, and the trade-off has an optimum.** Cost falls with time; risk rises with time. There is a schedule that is best for *your* risk appetite — and for a linear impact model it is a specific, known curve (a decaying exponential, in continuous time).

Everything else in this folder is the mathematics of that third point.

> **The one-sentence essence.** "Selling fast costs impact, selling slow costs risk; the optimal schedule spends exactly as long as your risk aversion says is worth it."

---

### 2. Mathematical Ground Truth & Derivations

**The two cost curves.** For a constant-rate ("TWAP") liquidation of $X$ shares over a horizon $T$:

- **Impact cost** is paid on the trade *rate*. Total expected cost falls as $1/T$:
$$
E_{\text{impact}}(T) \approx \frac{\eta X^2}{T} + \tfrac12\gamma X^2,
$$
  where $\eta$ is the temporary-impact coefficient, $\gamma$ the permanent one, and $\tfrac12\gamma X^2$ is a constant that **does not depend on the schedule at all** (it is paid whichever way you trade).

- **Risk** is the standard deviation of the trading revenue, driven by holding inventory $x_t \approx X(1-t/T)$:
$$
V(T) = \sigma^2\!\int_0^T x_t^2\,dt \approx \frac{\sigma^2 X^2 T}{3},\qquad \operatorname{sd}(T)\approx \frac{\sigma X\sqrt T}{\sqrt 3}.
$$

**Choosing a horizon.** With risk aversion $\lambda$ (dollars of variance you will pay to save a dollar of expected cost), minimize $U(T)=E(T)+\lambda V(T)$:

$$
\frac{dU}{dT} = -\frac{\eta X^2}{T^2} + \frac{\lambda\sigma^2 X^2}{3}=0 \quad\Longrightarrow\quad \boxed{\;T^\star=\sqrt{\frac{3\eta}{\lambda\sigma^2}}=\sqrt3\,\theta\;},\qquad \theta\equiv\sqrt{\frac{\eta}{\lambda\sigma^2}}=\frac1\kappa .
$$

The quantity $\theta$ is the **half-life of the trade** (time to deplete the position by a factor $e$) and $\kappa=1/\theta$ is the **urgency**. Note what does *not* appear: $X$ and $T$ itself. With linear impact, **every basket of the same stock is liquidated on the same intrinsic time scale** — a counter-intuitive but exact consequence of cost and variance both scaling as $X^2$ (Almgren–Chriss 2000, §2.3).

---

### 3. Computational Implementation — the trade-off in numbers

The whole argument on one screen: for a TWAP liquidation, compute impact cost, risk standard deviation, and the utility $E+\lambda V$ as a function of the chosen horizon. Stdlib only.

```python
import math
X, gamma, eta, sigma, lam = 1e6, 2.5e-7, 2.5e-6, 0.95, 1e-6
print("Horizon-T trade-off for a TWAP liquidation (X = 1,000,000 shares)")
print(f"{'T(d)':>5} {'impact $':>12} {'risk sd $':>12} {'U = E + lam*V':>15}")
best = None
for T in (0.5, 1, 2, 3, 5, 10, 20, 40):
    E = 0.5*gamma*X*X + eta*X*X/T           # impact cost, falls with T
    V = sigma*sigma*X*X*T/3.0               # variance, rises with T
    U = E + lam*V
    print(f"{T:5.1f} {E:12,.0f} {math.sqrt(V):12,.0f} {U:15,.0f}")
    if best is None or U < best[1]: best = (T, U)
theta = math.sqrt(eta/(lam*sigma**2))
print(f"half-life theta = sqrt(eta/(lam*sigma^2)) = {theta:.4f} days")
print(f"utility-optimal horizon T* = sqrt(3)*theta = {math.sqrt(3)*theta:.4f} days")
print(f"grid best T = {best[0]} day")
```
```
Horizon-T trade-off for a TWAP liquidation (X = 1,000,000 shares)
 T(d)     impact $    risk sd $   U = E + lam*V
  0.5    5,125,000      387,836       5,275,417
  1.0    2,625,000      548,483       2,925,833
  2.0    1,375,000      775,672       1,976,667
  3.0      958,333      950,000       1,860,833
  5.0      625,000    1,226,445       2,129,167
 10.0      375,000    1,734,455       3,383,333
 20.0      250,000    2,452,889       6,266,667
 40.0      187,500    3,468,910      12,220,833
half-life theta = sqrt(eta/(lam*sigma^2)) = 1.6644 days
utility-optimal horizon T* = sqrt(3)*theta = 2.8828 days
grid best T = 3 day
```

Read down the columns: impact cost **falls** as $1/T$, risk sd **rises** as $\sqrt T$, and the sum $U$ has a clean interior minimum. The analytic optimum $T^\star=2.883$ days sits inside the grid's best ($T=3$). That U-shaped curve *is* optimal execution.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Just sell it all now" is not free.** Setting $T\to0$ sends impact cost $\to\infty$ while risk $\to0$. The minimum-variance schedule is a pure block — and it is the most expensive possible schedule. There is no schedule with zero cost.
2. **"Just wait for a good price" is also not free.** Setting $T\to\infty$ makes impact negligible but leaves the full position exposed to a random walk. The risk term $\sigma^2 X^2T/3$ grows without bound. Patience is a position.
3. **The half-life is a property of the *stock*, not the order.** With linear impact, $\theta=\sqrt{\eta/(\lambda\sigma^2)}$ does not contain $X$. Big baskets are *not* automatically traded slower — this is the linear-impact assumption talking, and it is precisely what [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes]] breaks with nonlinear impact.
4. **The cost split confuses beginners.** Permanent impact contributes only the constant $\tfrac12\gamma X^2$ — it is paid regardless of schedule. Only *temporary* impact and *risk* are optimizable. Missing this leads people to "optimize" a term that cannot move.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000), §1 (the model), §2.3 (the half-life $\theta=1/\kappa$ and its independence from portfolio size).
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 14 (implementation shortfall as the objective) and Ch 15 (the permanent/temporary decomposition; the $s_t^\star=\bar s/T$ zero-drift optimum).
- **Perold, André F.** — "The implementation shortfall: Paper versus reality," *Journal of Portfolio Management* 14(3), 4-9 (1988). *The benchmark this whole folder is graded against.*

---

### 6. Connected Graph Bridges

- Impact-model view: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (what $\eta,\gamma$ really are)
- Heuristic schedules: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] (TWAP is the $\lambda\to0$ limit of what comes next)
- Continue: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|02 - The Execution Problem]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Index Hub]]

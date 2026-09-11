---
title: "2.2.4 The Efficient Frontier of Execution and the Optimal Trajectory"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - efficient-frontier
  - risk-aversion
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/03-the-almgren-chriss-model|03 - The Almgren–Chriss Model]].

---

### 1. Intuition & Practical Objective

There is no single "best" execution schedule — only a **frontier**. For every level of risk you are willing to accept, there is a cheapest way to trade; for every level of cost, there is a lowest-risk way. Plot those best-possible pairs and you have the **efficient frontier of execution** (Almgren–Chriss 2000, §2). Picking $\lambda$ is then a client decision, and the trajectory follows: high $\lambda$ (impatient) sells fast and pays impact; low $\lambda$ (patient) sells slowly and carries risk.

This page has two deliverables: (a) how to **construct** the frontier and read off a strategy for a given $\lambda$, and (b) how to **describe/compare** trajectories using the half-life $\theta$ and the shape of $x_t$. The one operational rule is the tangency condition: choosing $\lambda$ selects the frontier point where the curve's slope equals $-\lambda$.

> **The one-sentence essence.** "The frontier is the lower envelope of attainable $(V,E)$ pairs — convex, with the risk-neutral TWAP point at its cost-minimal end — and minimizing $E+\lambda V$ is exactly drawing a line of slope $-\lambda$ tangent to that curve."

---

### 2. Mathematical Ground Truth & Derivations

**The frontier (AC §2.1, §2.4).** For fixed $X,T,\sigma,\eta$ the family $\{x^\star(\lambda):\lambda\ge0\}$ traces a curve $(V(\lambda),E(\lambda))$ in the (variance, cost) plane. Its structure:

- **Cost-minimal end ($\lambda=0$):** the "naive" strategy, $x_t=X(1-t/T)$, minimizing $E$ while taking maximum variance. This is TWAP.
- **Variance-minimal end ($\lambda\to\infty$):** liquidate at $t=0$; $V\to0$, $E\to\infty$ (in the continuous limit).
- **Convexity:** $d^2E/dV^2>0$ — the frontier is strictly convex, so each $\lambda$ selects a **unique** point, and the selection is the **tangency condition**
$$
\frac{dE}{dV}\Big|_{\lambda} = -\lambda .
$$
  The Lagrange multiplier $\lambda$ is literally (minus) the slope of the frontier at the chosen point. AC §3.1 identify it with the Arrow-Pratt absolute risk aversion $\lambda_u=-u''(w)/u'(w)$ of a quadratic utility, giving $U_{\text{util}}(x)=\lambda_u V(x)+E(x)$ — so "pick a point" and "maximize utility" are the same act.

**Trajectory invariants.** Three numbers summarize any AC trajectory:

| Symbol | Meaning | Formula | This example |
|---|---|---|---|
| $\kappa$ | urgency (inverse half-life) | $\sqrt{\lambda\sigma^2/\tilde\eta}$ | $0.6011\ /\text{day}$ |
| $\theta=1/\kappa$ | trade half-life ($e$-folding) | $\sqrt{\tilde\eta/(\lambda\sigma^2)}$ | $1.664$ days |
| $\kappa T$ | constraint regime | $T/\theta$ | $3.006$ |

**Reading $\kappa T$ (AC §2.3).** $\kappa T\ll1$: the horizon binds, temporary impact dominates, the curve approaches TWAP. $\kappa T\gg1$: risk dominates, the curve approaches the block and most liquidation occurs in the first fraction of $T$. There is no dependence on $X$: with linear impact, **all basket sizes of the same stock trade on the same time scale** — a direct consequence of impact and variance both scaling as $X^2$.

**Closed-form frontier (AC eq 20).** The pair $(E(\lambda),V(\lambda))$ along the frontier is available in closed form from the $\sinh$ trajectory; the practical route (used below) is simply to evaluate $E$ and $V$ numerically on the trajectory for a grid of $\lambda$ — no approximation, complete agreement with AC's Fig. 1.

---

### 3. Computational Implementation — building and reading the frontier

Sweep $\lambda$, compute each optimal trajectory, evaluate $(E,V)$, verify convexity and the tangency condition. numpy + stdlib.

```python
import math
import numpy as np
X, T, N = 1e6, 5.0, 250
sigma, gamma, eta, eps = 0.95, 2.5e-7, 2.5e-6, 0.02
tau, etat = T/N, 2.5e-6 - 0.5*2.5e-7*(5.0/250)

def traj(k):
    if k < 1e-9: return np.array([X*(1 - j/N) for j in range(N+1)])
    return np.array([X*math.sinh(k*(T - T*j/N))/math.sinh(k*T) for j in range(N+1)])

def EV(k):
    x = traj(k)
    E = 0.5*gamma*X*X + eps*X + etat/tau*np.sum(np.diff(x)**2)
    V = sigma*sigma*tau*np.sum(x[1:N]**2)
    return E, V

print("Efficient frontier  (E = expected cost $, sd = sqrt(V) $)")
print(f"{'lambda(1/$)':>12} {'kappa':>8} {'half-life d':>11} {'E $':>12} {'sd $':>12}")
for lam in (0, 1e-7, 5e-7, 1e-6, 2e-6, 5e-6, 2e-5):
    k = math.sqrt(lam*sigma**2/etat) if lam > 0 else 0.0
    E, V = EV(k)
    print(f"{lam:12.1e} {k:8.4f} {(1/k if k>1e-12 else float('inf')):11.3f} {E:12,.0f} {math.sqrt(V):12,.0f}")

# tangency: for lambda = 1e-6 the frontier slope dE/dV must equal -lambda
lam0 = 1e-6
E1,V1 = EV(math.sqrt(lam0*1.001*sigma**2/etat)); E2,V2 = EV(math.sqrt(lam0*0.999*sigma**2/etat))
slope = (E1-E2)/(V1-V2)
print(f"\ntangency: dE/dV at lambda=1e-6 = {slope:.4e}   (-lambda = {-lam0:.1e})  error {abs(slope+lam0)/lam0:.2%}")
# convexity: slopes must become more negative as V falls
Es,Vs = zip(*[EV(k) for k in np.linspace(0.2, 3.0, 40)])
sl = np.diff(np.array(Es))/np.diff(np.array(Vs))
d2 = np.diff(sl)/np.diff(0.5*(np.array(Vs)[:-1]+np.array(Vs)[1:]))
print(f"convexity: min d2E/dV2 = {d2.min():.3e}  (all positive: {bool((d2>0).all())})")
print(f"frontier slope: {sl[0]:.3e} (low kappa) -> {sl[-1]:.3e} (high kappa)")
```
```
Efficient frontier  (E = expected cost $, sd = sqrt(V) $)
 lambda(1/$)    kappa half-life d          E $         sd $
     0.0e+00   0.0000         inf      644,500    1,222,765
     1.0e-07   0.1901       5.261      652,188    1,155,349
     5.0e-07   0.4251       2.353      757,349      975,145
     1.0e-06   0.6011       1.664      921,572      850,375
     2.0e-06   0.8501       1.176    1,210,676      721,254
     5.0e-06   1.3442       0.744    1,823,508      571,622
     2.0e-05   2.6884       0.372    3,501,269      398,736

tangency: dE/dV at lambda=1e-6 = -1.0000e-06   (-lambda = -1.0e-06)  error 0.00%
convexity: min d2E/dV2 = 8.988e-19  (all positive: True)
frontier slope: -1.559e-07 (low kappa) -> -2.432e-05 (high kappa)
```

Three verified facts from AC §2: **(i)** the frontier is convex; **(ii)** each $\lambda$ selects the tangent point exactly; **(iii)** $\lambda=0$ reproduces TWAP ($E= $ \$644{,}500, sd = \$1{,}222{,}765). Note how cheap the first risk reduction is — moving from $\lambda=0$ to $\lambda=10^{-7}$ cuts the standard deviation by \$67k for only \7.7k of extra expected cost. This is AC's point that the naïve (TWAP) strategy is *never* efficient: a small cost buys a large variance reduction.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The frontier is a model output, not a market fact.** Every point assumes $\sigma,\eta,\gamma$ are known and constant. Change $\eta$ by 2x and the whole curve shifts; the "efficient" trajectory you chose may be dominated under the true parameters.
2. **$\lambda$ is not directly observable.** It is a preference, and it is easy to under- or over-state. Because $\theta\propto1/\sqrt\lambda$, a 4x $\lambda$ error is a 2x half-life error — a first-order mistake in how the order is worked.
3. **Variance is the wrong risk measure for tail events.** The frontier assumes Gaussian shortfall. On a jump or liquidity-crisis path the relevant risk is a quantile/expected-shortfall, not the second moment — AC themselves add the L-VaR (quantile) frontier for exactly this reason (AC §3.2).
4. **Convexity is an artifact of convex costs.** With concave or non-convex impact (capacity limits, block discounts) the frontier can become non-convex, breaking the unique-tangency selection and admitting randomized ("mixed") strategies.
5. **A convex frontier does not mean a stable trajectory.** The whole construction is ex-ante; the realized path wanders (that is what $V$ measures). Do not read the smooth curve as a prediction of realized cost.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000), §2.1 (definition of the frontier), §2.2 (explicit strategies, eqs 16-18), §2.3 (half-life and the $\kappa T$ regimes), §2.4 (structure, Fig. 1-2), §3.1 (utility and the Arrow-Pratt identification of $\lambda$).
- **Gueant, Olivier** — *The Financial Mathematics of Market Liquidity* (2016), Ch 1-2. *Frontier and its convexity in a modern, general setting.*
- **Cartea, A.; Jaimungal, S.; Penalva, J.** — *Algorithmic and High-Frequency Trading* (2015), Ch 6. *Mean-variance execution and the frontier.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 15. *Empirical sizes: cost scales linearly, risk scales with $\sqrt T$.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/03-the-almgren-chriss-model|03 - The Almgren–Chriss Model]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes & Practice]] → [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/06-advanced-extensions|06 - Advanced Extensions]]
- Portfolio analogue: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory & Mean–Variance]] (the same mean-variance frontier, one level up: allocations instead of schedules)
- Risk: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (why the L-VaR frontier exists)

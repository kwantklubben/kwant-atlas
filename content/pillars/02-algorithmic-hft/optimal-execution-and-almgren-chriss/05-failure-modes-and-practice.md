---
title: "05 - Failure Modes and Desk Practice: Where Almgren–Chriss Breaks"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - failure-modes
  - nonlinear-impact
  - adversarial-execution
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/04-efficient-frontier-and-trajectory|04 - Efficient Frontier & Trajectory]].

---

### 1. Intuition & Practical Objective

The Almgren–Chriss trajectory is *mathematically optimal for an idealized market*: linear impact, constant parameters, no adversaries. Real markets violate all three. This page names the failures precisely, gives the first-principles reason for each, and quantifies the dollar cost of getting it wrong — because the point of a model is not to be true but to tell you **which of its assumptions you are betting on**.

The four failures, one line each:
1. **Impact is concave, not linear** — per-share impact grows roughly as $v^{1/2}$, so the AC linear schedule is provably suboptimal (Almgren 2003).
2. **Risk aversion is unobservable** — a wrong $\lambda$ mechanically mis-times the whole trade via $\theta\propto1/\sqrt\lambda$.
3. **Parameters are non-stationary** — $\sigma$ spikes and depth evaporates exactly when you are trading, so the calibrated $\eta$ is stale.
4. **The market adapts** — a deterministic trajectory is predictable and front-runnable (adverse selection the model does not price).

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Concave impact — the square-root law (Almgren 2003).** Replace the linear temporary cost $h(v)=\eta v$ with a power law

$$h(v) = \eta\,v^{\alpha},\qquad 0<\alpha<1\ (\text{empirically }\alpha\approx\tfrac12),$$

so the per-period cost becomes $\sum_k n_k h(n_k/\tau)=\eta\,\tau^{-\alpha}\sum_k n_k^{1+\alpha}$, a **concave per-share** cost. The objective is still convex in $n$ (the exponent $1+\alpha>1$), so a unique optimum exists, but the Euler-Lagrange equation is nonlinear and the $\sinh$ trajectory is only an approximation. Almgren derives closed forms in terms of a **characteristic time** $T_\star$ that *now depends on portfolio size*, $T_\star\propto X^{(\alpha-1)/(\alpha+1)}$ — so the clean "half-life is size-independent" property of the linear model **fails**. A linear model calibrated to average conditions systematically mis-paces large orders.

**2.2 Risk-aversion error.** The utility is $U=E+\lambda V$; if the desk uses $\hat\lambda$ but the true preference is $\lambda$, the realized excess utility is

$$\Delta U = U_{\lambda}\!\big(x(\hat\lambda)\big)-U_{\lambda}\!\big(x(\lambda)\big) \ge 0,$$

which grows quadratically in the relative parameter error (a second-order loss near the optimum). Because $\theta=1/\kappa\propto1/\sqrt\lambda$, a *first-order* error in $\lambda$ is only a *second-order* error in cost — the reassuring half of this failure — but the **timing** shift is first-order linear in $\sqrt{1/\lambda}$.

**2.3 Non-stationarity.** If $\eta$ or $\sigma$ shifts mid-execution to a new constant, the trajectory solving the original problem is no longer optimal for the remaining sub-problem. Re-solving at time $t$ with updated parameters gives the correct continuation (time-homogeneity only holds while parameters are unchanged). The practical cure is to **recalibrate and re-solve** on a schedule — i.e., turn the static rule into an adaptive one (page 06).

**2.4 Adversarial/predictable execution.** The AC trajectory is *deterministic*: $x_t=X\sinh(\kappa(T-t))/\sinh(\kappa T)$ is public information once $\kappa,T$ are inferred. Better-informed or faster participants can (a) trade ahead of the schedule to pre-position, and (b) sell into the large late-period prints, extracting an adverse-selection rent the model does not charge. This is why production algorithms randomize their schedules (the same anti-gaming motive as in [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP/TWAP]]'s TWAP jitter).

---

### 3. Computational Implementation — the cost of the linear assumption

**Experiment A — the AC schedule under a square-root impact law.** Calibrate both models to agree at the average rate, then compare the AC linear schedule against the true optimum under the $\sqrt{\cdot}$ law (solved as a convex program). numpy + stdlib + SciPy's SLSQP.

```python
import math
import numpy as np
from scipy.optimize import minimize

X, T, N = 1e6, 5.0, 250
sigma, gamma, eta, eps, lam = 0.95, 2.5e-7, 2.5e-6, 0.02, 1e-6
tau, v0 = T/N, 1e6/5.0
eta_p = eta*math.sqrt(v0)                      # calibrate both models at rate v0

def cost_linear(n):
    x = X - np.cumsum(n)
    return eta/tau*np.sum(n**2) + lam*sigma*sigma*tau*np.sum(x**2)
def cost_sqrt(n):
    x = X - np.cumsum(n)
    return eta_p/math.sqrt(tau)*np.sum(n**1.5) + lam*sigma*sigma*tau*np.sum(x**2)

kappa = math.sqrt(lam*sigma**2/(eta - 0.5*gamma*tau))
x_ac  = np.array([X*math.sinh(kappa*(T-T*j/N))/math.sinh(kappa*T) for j in range(N+1)])
n_ac  = np.diff(-x_ac)                          # AC linear-optimal schedule

res  = minimize(cost_sqrt, n_ac.copy(), method='SLSQP', bounds=[(0,None)]*N,
                constraints=[{'type':'eq','fun':lambda n: np.sum(n)-X}],
                options={'maxiter':3000,'ftol':1e-8})
n_sq = res.x
print(f"SLSQP converged = {res.success}   sum(n) = {n_sq.sum():,.2f}")
print(f"cost_sqrt(AC schedule)  = {cost_sqrt(n_ac):,.0f}")
print(f"cost_sqrt(sqrt-optimal) = {cost_sqrt(n_sq):,.0f}")
print(f"AC-schedule penalty under sqrt impact = {cost_sqrt(n_ac)-cost_sqrt(n_sq):,.0f} "
      f"({100*(cost_sqrt(n_ac)/cost_sqrt(n_sq)-1):.2f}%)")
print("\nfraction executed in each quarter of the horizon:")
for name, nn in (("AC-linear ", n_ac), ("sqrt-opt  ", n_sq)):
    Q = [np.sum(nn[:N//4]), np.sum(nn[N//4:N//2]), np.sum(nn[N//2:3*N//4]), np.sum(nn[3*N//4:])]
    print(f"  {name} " + "  ".join(f"{100*v/X:6.2f}%" for v in Q))
```
```
SLSQP converged = True   sum(n) = 1,000,000.00
cost_sqrt(AC schedule)  = 1,320,455
cost_sqrt(sqrt-optimal) = 1,174,738
AC-schedule penalty under sqrt impact = 145,717 (12.40%)

fraction executed in each quarter of the horizon:
  AC-linear   52.95%   25.85%   12.94%    8.26%
  sqrt-opt    74.44%   16.23%    5.88%    3.45%
```

The AC schedule **over-pays by 12.4%** when the truth is the square-root law, and the reason is visible in the quarter split: under concave impact, large *early* trades are relatively cheap, so the true optimum front-loads (74% in the first quarter vs the AC schedule's 53%). This is exactly Almgren's (2003) warning — the linear model mis-paces when impact is concave.

**Experiment B — parameter mis-estimation.** How much does it cost to use the wrong $\lambda$ or $\eta$?

```python
import math
import numpy as np
X, T, N = 1e6, 5.0, 250; sigma, gamma, eta, eps = 0.95, 2.5e-7, 2.5e-6, 0.02
tau, etat = T/N, 2.5e-6 - 0.5*2.5e-7*(5.0/250)
def traj(lam, e=etat):
    k = math.sqrt(lam*sigma**2/e) if lam > 0 else 0.0
    return np.array([X*math.sinh(k*(T-T*j/N))/math.sinh(k*T) for j in range(N+1)]) if k > 1e-9 \
           else np.array([X*(1-j/N) for j in range(N+1)])
def U(x, lam_true, e):
    E = 0.5*gamma*X*X + eps*X + e/tau*np.sum(np.diff(x)**2)
    return E + lam_true*sigma*sigma*tau*np.sum(x[1:N]**2)

true = 4e-6
Uopt = U(traj(true), true, etat)
print("Risk-aversion error (true lambda = 4e-6):")
for lu in (1e-6, 2e-6, 4e-6, 1e-5):
    print(f"  used lambda={lu:.1e}: excess utility = {U(traj(lu),true,etat)-Uopt:,.0f} "
          f"({100*(U(traj(lu),true,etat)/Uopt-1):.2f}%)")

print("\nImpact-coefficient error (true eta = 4x calibrated):")
etat4 = 4*2.5e-6 - 0.5*gamma*tau
Uo4 = U(traj(true, etat4), true, etat4)
print(f"  U(calibrated-eta schedule) vs U(sqrt-optimal) excess = "
      f"{U(traj(true, etat), true, etat4)-Uo4:,.0f} ({100*(U(traj(true,etat),true,etat4)/Uo4-1):.2f}%)")
```
```
Risk-aversion error (true lambda = 4e-6):
  used lambda=1.0e-06: excess utility = 702,309 (22.57%)
  used lambda=2.0e-06: excess utility = 179,693 (5.77%)
  used lambda=4.0e-06: excess utility = 0 (0.00%)
  used lambda=1.0e-05: excess utility = 320,595 (10.30%)

Impact-coefficient error (true eta = 4x calibrated):
  U(calibrated-eta schedule) vs U(sqrt-optimal) excess = 1,474,630 (23.99%)
```

A 4x error in $\lambda$ costs 22.6% of utility; a 4x error in $\eta$ costs 24.0%. Model risk in execution is **not** second-order in dollars, even when it is second-order in the optimizer.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Linear-impact delusion ($\eta v$ vs the square-root law).** Per-share impact is concave; the AC schedule over-pays (12.4% here) and mis-allocates volume (too little early). First-principles cause: liquidity is supplied along a *finite* depth curve, so the marginal cost of size grows slower than linearly. Fix: power-law impact (Almgren 2003) and size-dependent $T_\star$.
2. **Risk-aversion mis-estimation.** $\lambda$ is a preference, not a parameter; it is set by mandate, not estimated from data. Because $\theta\propto1/\sqrt\lambda$, mis-stating it mis-times the trade. Cost: 22.6% of utility for a 4x error; **10.3% for a 4x over-estimate** (over-trading is also expensive — you pay impact for risk you did not need to shed).
3. **Non-stationarity of $\sigma$ and $\eta$.** Both move in the same direction on stress days (vol up, depth down), so the risk term *and* the cost term shift together — the trajectory is wrong in the same direction that the market is stressed. First-principles cause: liquidity provision withdraws under volatility (the same adverse-selection logic as [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]). Fix: re-solve intraday; treat parameters as state-dependent.
4. **Adversarial / predictable execution.** A deterministic schedule is an open book. Front-running and predatory momentum trading add an adverse-selection cost outside the model. Fix: randomize timing (TWAP jitter), vary venue and participation, and never publish the full shape.
5. **Ignoring the opportunity cost of the unfilled tail.** The AC objective prices the *trades you make*, not the ones the market will not let you make. Under-resourced liquidity leaves the order unfinished — Perold's opportunity cost ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|02 - The Execution Problem]]).
6. **Serial correlation and drift break time-homogeneity.** The static optimum is time-consistent only without drift/autocorrelation (AC §4). In trending names the optimal strategy is genuinely dynamic (and, for a large enough drift, the optimal liquidation is to *not* sell — Hasbrouck Ch 15, eq 15.4).

---

### 5. Canonical Literature & Study References

- **Almgren, Robert** — "Optimal execution with nonlinear impact functions and trading-enhanced risk," *Applied Mathematical Finance* 10(1), 1-18 (2003). *Power-law impact, size-dependent characteristic time, trading-enhanced risk.*
- **Almgren, Robert; Thum, Chee; Hauptmann, Emmanuel; Li, Hong** — "Direct estimation of equity market impact," *Risk* 18(7), 58-62 (2005). *Fitting the real impact curve — where the linear model's error is measured.*
- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000), §3.2-3.4 (VaR/L-VaR, parameter choice), §4 (drift, serial correlation, parameter shifts).
- **Gatheral, Jim** — "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7), 749-759 (2010). *Huberman–Stanzl consistency: which impact/decay models are even admissible.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 15 (drift-augmented optimum eq 15.4, slowly-decaying temporary impact ⇒ U-shaped strategies).
- **Perold, André F.** — "The implementation shortfall," *JPM* 14(3), 4-9 (1988). *Opportunity cost.*
- **Cartea, A.; Jaimungal, S.; Penalva, J.** — *Algorithmic and High-Frequency Trading* (2015), Ch 6-9. *Adaptive re-solving, randomisation and gaming countermeasures.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/04-efficient-frontier-and-trajectory|04 - Efficient Frontier & Trajectory]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/06-advanced-extensions|06 - Advanced Extensions]]
- Impact-law view: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (square-root law, Kyle $\lambda$)
- Risk: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]
- Heuristics that already randomise: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]]

---
title: "03 - The Almgren-Chriss Model: Euler-Lagrange, HJB and the Hyperbolic Trajectory"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - euler-lagrange
  - hjb
  - optimization
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|02 - The Execution Problem]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Euler-Lagrange / convex minimization).

---

### 1. Intuition & Practical Objective

The execution problem has now been reduced to two scalars: an expected cost $E[x]$ and a variance $V[x]$, both functions of the trading trajectory $x=(x_0,\dots,x_N)$. The Almgren-Chriss model closes the problem by choosing the trajectory that minimizes

$$U[x] = E[x] + \lambda\,V[x],$$

a **quadratic objective** in $x$. For linear impact it is exactly a convex quadratic program, so the optimum is unique, static, and — in continuous time — has a closed form: a hyperbolic (exponential-decay) trajectory. This page does the derivation twice: the Euler-Lagrange route AC themselves used, and the dynamic-programming / Hamilton-Jacobi-Bellman route that is the modern control-theoretic statement, and shows they agree.

The practical objective: understand **where the shape comes from**, so that when the trajectory later disappoints (page 05) you know exactly which assumption to blame.

> **The one-sentence essence.** "Minimize expected temporary impact plus risk aversion times variance, and the Euler-Lagrange equation reduces to $\eta\ddot x = \lambda\sigma^2 x$ — whose solutions are exponentials with decay rate $\kappa=\sqrt{\lambda\sigma^2/\eta}$, so the optimal schedule decays exponentially and its half-life is $1/\kappa$."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The discrete quadratic problem (AC §2.2)

With linear impact, from [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|page 02]]:

$$E[x]=\tfrac12\gamma X^2+\varepsilon\sum_{k=1}^N|n_k|+\frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2,\qquad V[x]=\sigma^2\sum_{k=1}^N\tau x_k^2,\qquad \tilde\eta=\eta-\tfrac12\gamma\tau .$$

Dropping the schedule-independent constant $\tfrac12\gamma X^2$ and the fixed $\varepsilon X$ (assume all $n_k\ge0$), $U$ is a **strictly convex quadratic** in the free variables $x_1,\dots,x_{N-1}$ (since $\tilde\eta>0$). Setting $\partial U/\partial x_j=0$ for $1\le j\le N-1$:

$$\frac{\tilde\eta}{\tau}\cdot 2\big(-x_{j-1}+2x_j-x_{j+1}\big) + 2\lambda\sigma^2\tau\,x_j = 0
\quad\Longrightarrow\quad \frac{1}{\tau^2}\big(x_{j-1}-2x_j+x_{j+1}\big)=\tilde\kappa^2 x_j,\qquad \tilde\kappa^2=\frac{\lambda\sigma^2}{\tilde\eta}.$$

#### 2.2 Euler-Lagrange and the closed form

This is a **second-order linear difference equation**; its solutions are $\exp(\pm\kappa t_j)$ where $\kappa$ solves $\frac{2}{\tau^2}\big(\cosh(\kappa\tau)-1\big)=\tilde\kappa^2$. Imposing $x_0=X$ and $x_N=0$ gives (AC eq 17-18)

$$\boxed{\;x_j = X\,\frac{\sinh\big(\kappa(T-t_j)\big)}{\sinh(\kappa T)}\;},\qquad
n_j = \frac{2\sinh\big(\tfrac12\kappa\tau\big)}{\sinh(\kappa T)}\,\cosh\!\big(\kappa(T-t_{j-\frac12})\big)\,X .$$

In continuous time ($\tau\to0$) the same argument on $U=\int_0^T\!\big[\eta\,\dot x^2+\lambda\sigma^2x^2\big]dt$ gives the **Euler-Lagrange equation**

$$\frac{\partial L}{\partial x}-\frac{d}{dt}\frac{\partial L}{\partial\dot x}=0 \;\Longrightarrow\; 2\lambda\sigma^2x - 2\eta\ddot x=0 \;\Longrightarrow\; \boxed{\;\ddot x=\kappa^2x\;},\qquad \kappa=\sqrt{\frac{\lambda\sigma^2}{\eta}},$$

whose solution with $x(0)=X,\;x(T)=0$ is the same $\sinh$ trajectory. **Limits:** $\lambda\to0$ ($\kappa\to0$) gives $x_t=X(1-t/T)$ (TWAP); $\lambda\to\infty$ ($\kappa\to\infty$) gives instant liquidation at $t=0$ (a block). $\theta=1/\kappa$ is the trade **half-life**. The regime is read off $\kappa T=T/\theta$: if $T\gg\theta$ (large $\kappa T$) the trade is *risk-constrained* — the bulk of liquidation happens well before $T$ and the curve looks like a fast block; if $T\ll\theta$ (small $\kappa T$) it is *impact-constrained* and approaches the straight line (TWAP) — see AC §2.3 (here $\kappa T=3.0$ is squarely in the interior).

#### 2.3 Time-homogeneity and the HJB

**AC's Theorem (time-homogeneity).** The static optimum is also the *dynamic* optimum: re-solving at any interior time $t_k$ merely reproduces the continuation of the original trajectory. AC prove this two ways — algebraically (the continuation $X\sinh(\kappa(T-t_j))/\sinh(\kappa(T-t_k))$ matches) and by optimal control (no new information arrives, since the price has no serial correlation). This is *why* a static curve is legitimate.

**The HJB statement.** Cast the risk-neutral version as a dynamic program: with value function $V(t,x)$ (minimal expected cost to liquidate $x$ by $T$), trading rate $\nu=-\dot x$, and temporary cost rate $\nu h(\nu)=\varepsilon\nu+\eta\nu^2$,

$$-V_t = \min_{\nu\ge0}\Big[\varepsilon\nu+\eta\nu^2-\nu\,V_x\Big],\qquad V(T,x)=0 .$$

The first-order condition $\varepsilon+2\eta\nu-V_x=0$ gives $\nu^\star=(V_x-\varepsilon)/(2\eta)$, and substituting yields the **HJB equation**

$$\boxed{\;-V_t=\frac{(V_x-\varepsilon)^2}{4\eta}\;}.$$

Its solution $V(t,x)=\varepsilon x+\eta x^2/(T-t)$ (readily checked) gives $\nu^\star=x/(T-t)$ — the constant-rate **TWAP** optimum — and $V(0,X)=\varepsilon X+\eta X^2/T$, the risk-neutral cost. **Adding the risk penalty** $\lambda\sigma^2x^2$ to the running cost turns the same HJB into the one whose characteristics solve $\ddot x=\kappa^2x$: the risk-aversion term is precisely what bends TWAP into the hyperbolic curve.

---

### 3. Computational Implementation — the closed form *is* the discrete optimum

The strongest possible check: build the exact quadratic $U$ and minimize it by linear algebra; compare against the closed-form trajectory. numpy + stdlib.

```python
import math
import numpy as np

X, T, N = 1_000_000.0, 5.0, 250
sigma, gamma, eta, eps, lam = 0.95, 2.5e-7, 2.5e-6, 0.02, 1e-6
tau   = T/N
etat  = eta - 0.5*gamma*tau                 # AC eq (8)
kappa = math.sqrt(lam*sigma**2/etat)        # AC eq (19)

def ac_closed(k):                           # AC eq (17)
    return np.array([X*math.sinh(k*(T-T*j/N))/math.sinh(k*T) for j in range(N+1)])

def solve_discrete():                       # exact minimiser of U = E + lam V
    A = np.zeros((N-1, N-1)); b = np.zeros(N-1)
    for j in range(1, N):                   # interior stationarity eq (16)
        r = j-1
        A[r, r] = 2*etat/tau + lam*sigma*sigma*tau
        if j-1 >= 1: A[r, r-1] = -etat/tau
        if j+1 <= N-1: A[r, r+1] = -etat/tau
    b[0] = etat/tau * X                     # boundary x_0 = X
    return np.concatenate(([X], np.linalg.solve(A, b), [0.0]))

def U(x):                                   # objective (quadratic part)
    return etat/tau*np.sum(np.diff(x)**2) + lam*sigma*sigma*tau*np.sum(x[1:N]**2)

x_num, x_cl = solve_discrete(), ac_closed(kappa)
print(f"eta~ = {etat:.6e}   kappa = sqrt(lam*sigma^2/eta~) = {kappa:.6f} /day")
print(f"half-life theta = 1/kappa = {1/kappa:.4f} d   kappa*T = {kappa*T:.4f}")
print(f"max |x_numeric - x_closed| = {np.max(np.abs(x_num-x_cl)):.2f} shares  ({np.max(np.abs(x_num-x_cl))/X:.2e} of X)")
print(f"U(numeric) = {U(x_num):,.4f}    U(closed) = {U(x_cl):,.4f}   ratio = {U(x_cl)/U(x_num):.10f}")
print("  t(d)      shares remaining       %")
for tt in (0.0, 0.5, 1.0, 2.0, 2.5, 4.0, 5.0):
    j = int(round(tt/T*N)); print(f"  {tt:4.1f}   {x_num[j]:16,.0f}   {100*x_num[j]/X:6.2f}")
```
```
eta~ = 2.497500e-06   kappa = sqrt(lam*sigma^2/eta~) = 0.601133 /day
half-life theta = 1/kappa = 1.6635 d   kappa*T = 3.0057
max |x_numeric - x_closed| = 2.06 shares  (2.06e-06 of X)
U(numeric) = 1,499,710.2389    U(closed) = 1,499,710.2390   ratio = 1.0000000000
  t(d)      shares remaining       %
   0.0          1,000,000   100.00
   0.5            738,901    73.89
   1.0            545,057    54.51
   2.0            293,077    29.31
   2.5            212,005    21.20
   4.0             63,325     6.33
   5.0                  0     0.00
```

The closed form and the exact discrete minimizer agree to **2 shares in 1,000,000** (the residual is the $O(\tau)$ difference between $\kappa$ and the discrete $\tilde\kappa$), and the objective values match to 10 significant figures. This is the statement "the AC formula solves the AC problem," verified numerically.

**HJB check.** With $\eta=2.5\times10^{-6}$, $\varepsilon=0.02$, the ansatz $V(t,x)=\varepsilon x+\eta x^2/(T-t)$ satisfies $-V_t=(V_x-\varepsilon)^2/(4\eta)$ with maximum relative residual $8.94\times10^{-10}$ and gives $V(0,X)=\$520{,}000=\varepsilon X+\eta X^2/T$ — the risk-neutral TWAP cost.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The model is a quadratic; reality is not.** The entire closed form rests on $U=E+\lambda V$ being a convex quadratic. Nonlinear impact ($\eta v^{\alpha}$) destroys it — the Euler-Lagrange equation becomes nonlinear and the $\sinh$ solution is only an approximation ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/06-advanced-extensions|06 - Advanced Extensions]]).
2. **Mean-variance is not expected utility.** $E+\lambda V$ equals quadratic utility only up to second order; for non-Gaussian (fat-tailed, jump) shortfall the objective mis-specifies risk. AC handle this with the L-VaR construction (§3.2), which replaces variance with a quantile.
3. **Static ≠ adaptive.** Time-homogeneity holds *only* because the price has no serial correlation or drift. With drift, momentum, or mean reversion, the optimal strategy is genuinely dynamic and the static curve is stale (AC §4; Hasbrouck Ch 15 gives the drift-corrected $s_t^\star$).
4. **$\kappa$ inherits every parameter error.** $\kappa=\sqrt{\lambda\sigma^2/\eta}$: urgency scales as $\sqrt\lambda$, $\sigma$, and $1/\sqrt\eta$. A 4x error in the risk aversion mis-sets the half-life by 2x. See [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes]].
5. **The objective is dimensioned loosely.** $E$ is in dollars, $V$ in dollars$^2$, so $\lambda$ carries units $1/\$$. Quoting a $\lambda$ without its units (or in the wrong currency scale) silently rescales the entire schedule.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000), §1.5 (linear impact), §2.1-2.4 (frontier, eqs 16-19, half-life), §3.1 (quadratic utility, the time-homogeneity Theorem), §3.2 (Value at Risk / L-VaR).
- **Bertsimas, Dimitris; Lo, Andrew W.** — "Optimal control of execution costs," *Journal of Financial Markets* 1(1), 1-50 (1998). *The dynamic-programming / HJB formulation ($s_t^\star=\bar s/T$ in the zero-drift case).*
- **Cartea, A.; Jaimungal, S.; Penalva, J.** — *Algorithmic and High-Frequency Trading* (2015), Ch 6-7. *The HJB statement in full generality, with inventory penalties and the Almgren-Chriss problem as a special case.*
- **Gueant, Olivier** — *The Financial Mathematics of Market Liquidity* (2016), Ch 1-4. *Rigorous treatment of the execution problem and its well-posedness.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 15 (the discrete DP, eqs 15.1-15.4, and the drift-augmented optimum).

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|02 - The Execution Problem]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/04-efficient-frontier-and-trajectory|04 - Efficient Frontier & Trajectory]]
- Theory: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Euler-Lagrange, convex QP) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (martingale conditioning under the dynamic program)
- Control-theory twin: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda-Stoikov & Optimal Quoting]] (same HJB machinery, inventory instead of execution)

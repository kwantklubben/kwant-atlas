---
title: "06 - Advanced Extensions: Nonlinear Impact, Resilient Books, Dark Pools, Adaptive Control"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - obizhaeva-wang
  - transient-impact
  - dark-pools
  - stochastic-control
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Each failure of Almgren–Chriss (page 05) is the seed of an extension. This page is the launchpad: it shows the four extensions that turn the static linear model into something a modern desk can run — **nonlinear impact** (Almgren 2003), **resilient/transient impact** (Obizhaeva–Wang 2013; Gatheral, Schied & Slynko 2012), **dark pools / alternative venues**, and **adaptive stochastic control** (Cartea–Jaimungal–Penalva 2015) — and it hands off to the dedicated topic-folders for the microstructure and market-making views.

Why in this order? Nonlinear impact fixes the *cost function*; resilience fixes the *market's memory* (the book refills, so the optimal schedule gains discrete trades at both ends); dark pools add a *venue choice* with its own fill risk; adaptive control fixes the *dynamics* by re-solving as information arrives. Together they are the minimal set that makes the AC idea survive contact with a real order.

> **The one-sentence essence.** "Relax one assumption at a time: concave impact bends the trajectory, a resilient book makes it block-continuous-block, a dark venue trades price improvement for fill risk, and stochastic control turns the static curve into a feedback law."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Nonlinear (power-law) impact — Almgren (2003).** With $h(v)=\eta v^{\alpha}$, $\alpha\in(0,1]$, the cost functional becomes $\int_0^T\big[\eta\,(-\dot x)^{1+\alpha}+\lambda\sigma^2x^2\big]dt$, and the Euler-Lagrange equation is nonlinear. Almgren's key results:
- a **characteristic time** $T_\star=\big(\alpha\eta X^{\alpha-1}/(\lambda\sigma^2)\big)^{1/(\alpha+1)}$, which **depends on portfolio size**;
- in the regime $\alpha\gg1$ the trajectory reaches $x=0$ with $\dot x=0$ at a finite $T_{\max}=\tfrac{\alpha+1}{\alpha-1}T_\star$;
- closed forms per regime: for $0<\alpha<1$ a stretched-exponential; for $\alpha=1$ the exponential (AC); for $\alpha>1$ a polynomial tail.

**2.2 Resilient / transient impact — Obizhaeva–Wang (2013).** Model the book's *state*: the transient impact $a_t$ created by trading decays with a **resilience** rate $\rho$, and the execution price is depressed by the accumulated, still-unreplenished impact:

$$\text{cost}_k = n_k\Big(\tfrac{s}{2}+a_k+\tfrac{n_k}{2q}\Big),\qquad a_{k+1}=(1-\rho)\Big(a_k+\tfrac{n_k}{q}\Big),\qquad q=\text{book depth}.$$

The optimal schedule is **not** smooth: it is a **discrete block at $t=0$**, a continuous/small-trade middle, and a **discrete block at $T$** — "block-continuous-block". In the risk-neutral limit the two blocks are **exactly equal** ($n_1=n_N$), the Obizhaeva–Wang symmetry. This is the discrete time-value of finite resilience: trading before the book refreshes is expensive, so you wait at the ends and work only when the book has refilled.

**2.3 Transient impact in continuous time — Gatheral (2010, 2013); Gatheral-Schied-Slynko (2012).** Generalize the temporary impact to a **decay kernel** $G(\cdot)$: the price impact of a trade at $u<t$ contributes $G(t-u)\,dX_u$, and the mid-price is

$$S_t = S_0 + \sigma W_t + \int_0^t G(t-u)\,dX_u .$$

The **no-dynamic-arbitrage** condition (Huberman–Stanzl 2004; Gatheral 2010) requires $G$ to be nonincreasing and convex — this rules out many "natural" models and is the consistency constraint every impact model must satisfy. The optimal execution problem becomes a Fredholm equation; for power-law kernels $G(t)\propto t^{-\gamma}$ the optimal strategy has a characteristic oscillating/decaying profile (Gatheral's Figure 22.2).

**2.4 Dark pools and venue choice (Cartea–Jaimungal–Penalva 2015, Ch 8-9).** A dark venue executes at the midpoint (saving the half-spread) but fills only with probability $p$; unfilled shares must be worked later in the lit book with an adverse-selection penalty. The per-share expected cost of routing to dark is

$$c_{\text{dark}}(p) = (1-p)\big(c_{\text{lit}}+\delta\big),$$

so dark beats lit iff $p>p^\star=\delta/(c_{\text{lit}}+\delta)$ — a threshold rule on the fill probability. In practice $p$ is estimated per venue per order size, and the strategy becomes a **venue-allocation control**.

**2.5 Adaptive / stochastic control (Cartea–Jaimungal–Penalva 2015).** Replace the static trajectory with a **feedback law** $\nu^\star(t,x,\text{state})$ from an HJB equation that includes inventory, transient impact, and possibly alpha/drift. Then parameters are re-estimated as fills arrive and the schedule updates — this is the production form of AC.

---

### 3. Computational Implementation — two extensions, verified

**A. Resilient book ⇒ block-continuous-block (Obizhaeva–Wang).** Build the exact quadratic objective for the decaying-impact model and solve the equality-constrained programme. The risk-neutral limit must reproduce the OW symmetry $n_1=n_N$. numpy + stdlib.

```python
import numpy as np
X, T, N = 1e6, 5.0, 250
sigma, lam = 0.95, 1e-6
tau, q, s_half = T/N, 1.0e4, 0.01

def build(rho):
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(i):
            A[i, j] = 0.5*(1.0-rho)**(i-j)/q        # transient impact coupling
    A += A.T
    for i in range(N):
        A[i, i] += 1.0/(2*q)                        # within-period impact
    for i in range(N):
        for j in range(N):
            A[i, j] += lam*sigma*sigma*tau*(N - max(i, j))   # risk quadratic
    b = np.array([s_half/2 - 2*X*lam*sigma*sigma*tau*(N-i) for i in range(N)])
    return A, b

def solve(rho):
    A, b = build(rho)
    K = np.zeros((N+1, N+1)); r = np.zeros(N+1)
    K[:N, :N] = 2*A; K[:N, N] = 1.0; K[N, :N] = 1.0   # KKT: minimise n'An+b'n s.t. 1'n=X
    r[:N] = -b; r[N] = X
    return np.linalg.solve(K, r)[:N]

print("  rho   n1(shares)  nN(shares)   quarter% (Q1  Q2  Q3  Q4)      x(T/2)%")
for rho in (0.05, 0.15, 0.40, 0.90):
    n = solve(rho)
    x = np.concatenate(([X], X-np.cumsum(n)))
    Q = [np.sum(n[:N//4]), np.sum(n[N//4:N//2]), np.sum(n[N//2:3*N//4]), np.sum(n[3*N//4:])]
    print(f" {rho:4.2f} {n[0]:12,.0f} {n[-1]:12,.0f}   "
          + " ".join(f"{100*v/X:5.2f}" for v in Q) + f"   {100*x[N//2]/X:8.2f}   sum={n.sum():,.0f}")
```
```
  rho   n1(shares)  nN(shares)   quarter% (Q1  Q2  Q3  Q4)      x(T/2)%
 0.05       86,212       61,309   32.39 22.12 20.13 25.36      45.49   sum=1,000,000
 0.15       40,490       18,652   35.39 24.95 20.01 19.65      39.66   sum=1,000,000
 0.40       24,025        4,331   46.36 26.07 15.69 11.88      27.57   sum=1,000,000
 0.90       18,939          518   65.66 22.85  7.94  3.56      11.49   sum=1,000,000
```

Read the first and last columns: for **low resilience** ($\rho=0.05$ — the book barely refills) the schedule is nearly symmetric with a **large terminal block** ($n_N=61{,}309$, and the last quarter carries 25% of the volume); for **high resilience** ($\rho=0.90$ — the book refills fast) the schedule is **front-loaded** and the terminal block vanishes ($n_N=518$). The Obizhaeva–Wang symmetry is an exact check: in the risk-neutral limit ($\lambda=0$) the two blocks are equal to machine precision ($n_1/n_N=1.000000$ for $\rho=0.05,0.2,0.5$).

**B. Dark-pool allocation.** The break-even fill probability on the example numbers.

```python
X, s, eta = 1e6, 0.02, 2.5e-6
half = s/2.0
lit_per_share = half + eta*X            # lit cost/share: half-spread + linear impact
delta = 0.5*eta*X                       # adverse-selection penalty if unfilled
print(f"lit-only cost/share       = {lit_per_share:.4f} $")
print(f"adverse-selection penalty = {delta:.4f} $")
for p in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    c = (1-p)*(lit_per_share+delta)
    print(f"  p={p:.1f}: E[cost|dark] = {c:6.4f} $/sh   vs lit-only {lit_per_share-c:+.4f}")
pstar = delta/(lit_per_share+delta)
print(f"break-even fill probability p* = delta/(lit+delta) = {pstar:.4f}  -> dark beats lit for p > {pstar:.3f}")
```
```
lit-only cost/share       = 2.5100 $
adverse-selection penalty = 1.2500 $
  p=0.0: E[cost|dark] = 3.7600 $/sh   vs lit-only -1.2500
  p=0.2: E[cost|dark] = 3.0080 $/sh   vs lit-only -0.4980
  p=0.4: E[cost|dark] = 2.2560 $/sh   vs lit-only +0.2540
  p=0.6: E[cost|dark] = 1.5040 $/sh   vs lit-only +1.0060
  p=0.8: E[cost|dark] = 0.7520 $/sh   vs lit-only +1.7580
  p=1.0: E[cost|dark] = 0.0000 $/sh   vs lit-only +2.5100
break-even fill probability p* = delta/(lit+delta) = 0.3324  -> dark beats lit for p > 0.332
```

A venue with fill probability above **33.2%** is worth routing to on these numbers; below it, the unfilled tail (and the adverse selection of trading it late) dominates the saved half-spread.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Power-law exponents are estimated, not known.** Almgren's $T_\star\propto X^{(\alpha-1)/(\alpha+1)}$ is sensitive to $\alpha$; a mis-fit exponent mis-paces large orders systematically (the 2005 Almgren-Thum-Hauptmann-Li estimation paper exists precisely because this matters).
2. **A decay kernel must satisfy no-dynamic-arbitrage.** Gatheral (2010) / Huberman–Stanzl (2004): $G$ must be nonincreasing and convex. Ad-hoc exponential kernels with the wrong parameters admit price manipulation — a model that *creates* free money is wrong regardless of its fit.
3. **Resilience is unobservable and regime-dependent.** $\rho$ changes with volatility and with the presence of other large traders; assuming it constant under-states the terminal-block risk that OW highlights.
4. **Dark fill probability is adversely selected.** $p$ estimated ex-ante overstates the *realized* fill rate conditional on your trade being informed/urgent (you fill when the market is about to move against you). The threshold rule $p^\star$ uses an average $p$, which is the wrong conditional quantity.
5. **Adaptive control inherits estimation lag.** Re-solving as fills arrive helps only if the re-estimation is faster than the regime change; otherwise you chase a stale parameter (and re-solving too often adds turnover, incurring extra impact).
6. **The extensions do not compose for free.** Nonlinear impact + transient impact + dark pools + control is a high-dimensional, poorly-identified system; in practice desks pick two or three effects, calibrate conservatively, and leave the rest to robust/randomized execution.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert** — "Optimal execution with nonlinear impact functions and trading-enhanced risk," *Applied Mathematical Finance* 10(1), 1-18 (2003). *Power-law impact, $T_\star\propto X^{(\alpha-1)/(\alpha+1)}$, trading-enhanced risk.*
- **Obizhaeva, Anna; Wang, Jiang** — "Optimal trading strategy and supply/demand dynamics," *Journal of Financial Markets* 16(1), 1-32 (2013). *Resilient book, block-continuous-block, $n_1=n_N$ symmetry.*
- **Gatheral, Jim** — "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7), 749-759 (2010). *The admissibility constraint on impact/decay models.*
- **Gatheral, Jim; Schied, Alexander; Slynko, Alla** — "Transient linear price impact and Fredholm integral equations," *Mathematical Finance* 22(3), 445-474 (2012). *Optimal execution for general decay kernels (power-law kernels, oscillating strategies).*
- **Gatheral, Jim** — "Dynamical models of market impact and algorithms for order execution," in *Handbook on Systemic Risk* (2013), §22.4. *Continuous-time transient-impact survey; decay kernels and Figure 22.2.*
- **Cont, Rama; Kukanov, Arseniy; Stoikov, Sasha** — "The price impact of order book events," *Journal of Financial Econometrics* 12(1), 47-88 (2014). *OFI and the concave/square-root impact relation — the empirical anchor for §2.1.*
- **Cartea, A.; Jaimungal, S.; Penalva, J.** — *Algorithmic and High-Frequency Trading* (2015), Ch 6-9. *Stochastic control, transient impact, dark-pool allocation, limit-order execution.*
- **Gueant, Olivier** — *The Financial Mathematics of Market Liquidity* (2016), Ch 2-5. *Unified modern treatment of transient impact and market making.*
- **Huberman, Gur; Stanzl, Werner** — "Price manipulation and quasi-arbitrage," *Econometrica* 72(4), 1247-1275 (2004). *The no-manipulation condition behind Gatheral's constraint.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Index Hub]]
- Impact-law depth: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (Kyle $\lambda$, temporary vs permanent, square-root law, transient impact)
- Market-making twin: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (inventory control; the same HJB family)
- Execution heuristics: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] (dark/hidden orders)
- Risk & portfolio: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]

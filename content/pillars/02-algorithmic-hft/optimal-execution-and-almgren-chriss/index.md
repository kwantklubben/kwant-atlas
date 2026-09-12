---
title: "2.2 Optimal Execution & Almgren–Chriss"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - market-impact
  - index-hub
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus & Optimization]] and [[foundations/stochastic-calculus/index|Stochastic Calculus]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Liquidating a large block is a **two-sided loss**. Trade fast and you pay the market its liquidity premium - **market impact**. Trade slowly and you hold inventory that drifts against you - **volatility risk**. Neither cost can be pushed to zero; every schedule trades one against the other. The Almgren–Chriss (2000) framework turns that conflict into a single, solvable optimization: **minimize expected cost plus a risk-aversion times the variance of cost**, and the solution is an explicit hyperbolic trading trajectory.

This folder is the **optimal-execution topic-folder** for Pillar 2. It is a *hub*: it gives you the **(a) fast formula lookup** below (job #1), and **(b) routes you to six sub-pages** that walk from zero-knowledge intuition through the execution problem, the Almgren–Chriss model, the efficient frontier and closed-form trajectory, the failure modes and desk practice, and the modern extensions (nonlinear impact, resilient books, dark pools, adaptive control).

> **The one-sentence essence.** "Expected liquidation cost rises as $\eta X^2/T$ (impact), its standard deviation rises as $\sigma X\sqrt{T/3}$ (risk); Almgren–Chriss picks the trajectory that minimizes $E+\lambda V$ - and with linear impact it is $x_t = X\,\sinh(\kappa(T-t))/\sinh(\kappa T)$ with urgency $\kappa=\sqrt{\lambda\sigma^2/\eta}$."

**Scope note (vs the sibling folder).** This folder is the *scheduling* view - how to trade a given order. For *why* the price moves and how to measure it, see [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (Kyle's $\lambda$, square-root law, transient impact). The two meet at the impact-parameter calibration $\eta,\gamma$.

*Primary verified sources:* Almgren & Chriss (2000); Almgren (2003); Obizhaeva & Wang (2013); Gatheral (2010, 2013); Cont, Kukanov & Stoikov (2014); Bertsimas & Lo (1998); Hasbrouck, *Empirical Market Microstructure* Ch 14-15 (verification report `hasbrouck_ch11-15.md` in the corpus); Cartea–Jaimungal–Penalva (2015); Gueant (2016). All numbers below were **re-executed and reproduced** (see §3).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $X$ = initial position to liquidate (units); $T$ = horizon; $N$ = number of trading intervals of length $\tau=T/N$; $t_k=k\tau$; $x_k$ = units still held at $t_k$ (so $x_0=X$, $x_N=0$); $n_k=x_{k-1}-x_k$ = units sold in interval $k$; $S_0$ = initial price; $\sigma$ = volatility (\$/share/√day); $\gamma$ = **permanent** impact coefficient (\$/share/\$share); $\eta$ = **temporary** impact coefficient ((\$/share)/(share/day)); $\varepsilon$ = fixed cost per share (half-spread + fees); $\lambda$ = risk-aversion (1/\$).

**Price dynamics (AC eqs 1-2).** Arithmetic random walk with permanent impact $g$, plus a temporary impact $h$ paid only on the shares traded:

$$
S_k = S_{k-1} + \sigma\sqrt{\tau}\,\xi_k - \tau\,g\!\left(\tfrac{n_k}{\tau}\right), \qquad \tilde S_k = S_{k-1} - h\!\left(\tfrac{n_k}{\tau}\right),
$$

with linear $g(v)=\gamma v$ and $h(v)=\varepsilon+\tfrac{\eta}{\tau}v$.

**Cost / risk (AC eqs 4-5, 8).** Expected shortfall and its variance, expressed in the trajectory $x$:

$$
\boxed{\;E[x] = \tfrac12\gamma X^2 + \varepsilon\sum_{k=1}^N |n_k| + \frac{\tilde\eta}{\tau}\sum_{k=1}^N n_k^2\;}, \qquad \boxed{\;V[x] = \sigma^2 \sum_{k=1}^N \tau\,x_k^2\;}, \qquad \tilde\eta = \eta - \tfrac12\gamma\tau .
$$

Note the constant $\tfrac12\gamma X^2$: **permanent impact costs the same no matter how you pace the trade** - only temporary impact and risk depend on the schedule. This is the single most useful simplification in the model.

**Objective and solution (AC §2).** Minimize $U(x)=E[x]+\lambda V[x]$. Setting $\partial U/\partial x_j=0$ gives the linear difference equation

$$
\frac{1}{\tau^2}\left(x_{j-1}-2x_j+x_{j+1}\right) = \tilde\kappa^2 x_j, \qquad \tilde\kappa^2 = \frac{\lambda\sigma^2}{\tilde\eta},
$$

whose solution with $x_0=X$, $x_N=0$ is the **hyperbolic (exponential-decay) trajectory**:

$$
\boxed{\;x_j = X\,\frac{\sinh\!\big(\kappa\,(T-t_j)\big)}{\sinh(\kappa T)}\;}, \qquad n_j = \frac{2\sinh\!\big(\tfrac12\kappa\tau\big)}{\sinh(\kappa T)}\cosh\!\big(\kappa(T-t_{j-\frac12})\big)\,X ,
$$

with the continuous-time urgency $\kappa=\sqrt{\lambda\sigma^2/\eta}$ (AC eq 19: $\kappa=\tilde\kappa+O(\tau)$).

**Quick-Reference Lookup** - the fast facts of this folder (all reproduced in §3):

| Quantity | Formula | Verified check |
|---|---|---|
| Urgency | $\kappa=\sqrt{\lambda\sigma^2/\eta}$ | $\lambda{=}10^{-6},\sigma{=}0.95,\eta{=}2.5{\times}10^{-6} \Rightarrow \kappa=0.6011/\text{day}$ |
| Trade half-life | $\theta=1/\kappa$ | $\theta=1.6635$ days; $\kappa T=3.006$ |
| Trajectory | $x_t=X\dfrac{\sinh(\kappa(T-t))}{\sinh(\kappa T)}$ | $x(1\text{d}){=}545{,}055$, $x(2.5\text{d}){=}212{,}003$ of $10^6$ |
| Risk-neutral limit | $\lambda\to0 \Rightarrow \kappa\to0,\; x_t=X(1-t/T)$ | TWAP |
| Infinitely risk-averse | $\lambda\to\infty \Rightarrow$ liquidate at $t=0$ | block |
| Expected cost | $\tfrac12\gamma X^2+\varepsilon X+\tfrac{\tilde\eta}{\tau}\sum n_k^2$ | TWAP $E= $ \$644{,}500; AC E= \$921{,}572 |
| Cost variance | $\sigma^2\sum\tau x_k^2$ | TWAP sd $= $ \$1{,}222{,}765; AC sd = \$850{,}375 |
| Efficient frontier | $E$ convex, increasing in $V$; selected by tangent slope $-\lambda$ | tangency error $0.00\%$ at $\lambda{=}10^{-6}$ |
| TWAP-horizon optimum | $T^\star=\sqrt3\,\theta$ | $\theta{=}1.664 \Rightarrow T^\star{=}2.883$ d |
| Implementation shortfall | $IS=$ execution cost $+$ opportunity cost (Perold 1988) | MC mean matches theory to $0.12\%$ |
| Nonlinear impact | $h(v)=\eta v^{\alpha}$; AC $\Rightarrow$ exact power-law solutions (Almgren 2003) | AC schedule $12.4\%$ penalty under $\sqrt{\cdot}$ law |

---

### 3. Computational Implementation - the formula engine

Runs on **numpy** (and stdlib) only. It reproduces every verified number above: the closed-form trajectory equals the exact discrete optimum to $\sim2$ shares in $10^6$, and the Monte Carlo implementation shortfall matches the closed-form $E$ and $V$.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the full failure analysis lives in [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes & Practice]]. In one line each:

1. **Impact-model risk** - the linear $h(v)=\eta v$ is empirically false (real per-share impact grows as $v^{0.5}$); the AC schedule is provably suboptimal under the true concave law, and the error is a real dollar cost.
2. **Risk-aversion misestimation** - $\lambda$ is not observable; the trajectory's half-life scales as $\sqrt{\lambda}$, so a 4x error in $\lambda$ doubles or halves your urgency.
3. **Non-stationarity** - $\sigma$, $\eta$ and the drift are assumed constant; volatility spikes and depth evaporation mid-execution break the assumed path and make the *static* trajectory stale.
4. **Predictability / predatory trading** - a deterministic trajectory is reverse-engineerable; faster participants front-run it, adding an adverse-selection cost the model ignores.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert; Chriss, Neil** - "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000). *The canonical paper; the source of eqs (1)-(20) above. Read §1-2 first, then §3 (utility, L-VaR).*
- **Almgren, Robert** - "Optimal execution with nonlinear impact functions and trading-enhanced risk," *Applied Mathematical Finance* 10(1), 1-18 (2003). *Extends linear impact to power laws $h(v)=\eta v^{\alpha}$; the source of the $\sqrt{\cdot}$ correction used in sub-page 05.*
- **Almgren, Thum, Hauptmann, Li** - "Direct estimation of equity market impact," *Risk* 18(7), 58-62 (2005). *How to fit $\eta$ (and the power $\alpha$) to real order data - the calibration companion.*
- **Obizhaeva, Anna; Wang, Jiang** - "Optimal trading strategy and supply/demand dynamics," *Journal of Financial Markets* 16(1), 1-32 (2013). *Resilient book: optimal schedule is discrete at both ends (block-continuous-block).*
- **Gatheral, Jim** - "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7), 749-759 (2010). *The consistency constraint (Huberman–Stanzl) every impact model must satisfy; rules out arbitrary decay kernels.*
- **Gatheral, Jim; Schied, Alexander; Slynko, Alla** - "Transient linear price impact and Fredholm integral equations," *Mathematical Finance* 22(3), 445-474 (2012). *Optimal execution for general (power-law) decay kernels.*
- **Bertsimas, Dimitris; Lo, Andrew W.** - "Optimal control of execution costs," *Journal of Financial Markets* 1(1), 1-50 (1998). *The dynamic-programming predecessor; gives $s_t^\star=\bar s/T$ under zero drift.*
- **Cartea, A.; Jaimungal, S.; Penalva, J.** - *Algorithmic and High-Frequency Trading* (2015), Ch 6-8. *The stochastic-control generalization (adaptive execution, dark pools, limit orders).*
- **Gueant, Olivier** - *The Financial Mathematics of Market Liquidity* (2016). *Rigorous modern monograph: execution and market making as one theory.*
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 14 (trading costs, implementation shortfall, Perold 1988) and Ch 15 (order splitting, temporary/permanent impact, DP, U-shaped strategies). *Corpus verification: `hasbrouck_ch11-15.md`.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Euler-Lagrange, convex QP) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (arithmetic Brownian motion, quadratic variation)
- Sibling in-pillar: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] (the *heuristic* schedules AC optimizes) · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Impact-model view: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (Kyle $\lambda$, square-root law, transient impact)
- Natural partner: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (the *inventory* risk-aversion control, mirror image of AC)
- Risk & portfolio: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (L-VaR) · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]

**Beginner:** start at [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05]]

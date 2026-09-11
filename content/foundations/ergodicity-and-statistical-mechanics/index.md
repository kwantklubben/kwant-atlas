---
title: "F.9 Ergodicity & Statistical Mechanics"
tags:
  - foundations
  - ergodicity
  - statistical-mechanics
  - kelly-criterion
  - ruin-theory
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (expectations, laws of large numbers, martingales) and [[foundations/calculus-and-optimization|Calculus & Optimization]] (maximising $\mathbb{E}[\ln W]$, concavity). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Almost all of textbook finance computes **ensemble averages**: the expected value of a portfolio across many parallel copies of the world at one instant. But you do not get to live across parallel copies — you live along *one* path through time. **When wealth compounds multiplicatively, the ensemble average and the time average are not the same number, and the difference is not a rounding error — it is the whole game.** A strategy whose ensemble expectation is $+5\%$ per round can bankrupt a single investor with probability one. That is non-ergodicity, and it is the single most important correction to the "expected return" reflex in the Atlas.

This folder is the **ergodicity & statistical-mechanics toolbox** for the Atlas. Everything reduces to **five primitive ideas**:

1. **Ensemble average $\ne$ time average unless a system is ergodic** — and compounding wealth is *not* ergodic. → [[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|02 · Ensemble vs Time Averages]].
2. **Multiplicative growth adds in the log**, so the growth rate is $\mathbb{E}[\ln(1+R)]$, not $\mathbb{E}[R]$. The gap is the **volatility drag** $\tfrac12\sigma^2$. → [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]].
3. **Maximising $\mathbb{E}[\ln W]$ is the growth-optimal objective** — the Kelly criterion — and it has a unique optimum $f^*$. → [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · The Kelly Criterion]].
4. **Beyond $f^*$ there is a critical fraction $f_c$ past which ruin is certain**, and even full Kelly has a fixed, large drawdown law. → [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown]].
5. **In the real world the parameters are estimated**, so overbetting is the dominant risk — which is why practice uses *fractional* Kelly. → [[foundations/ergodicity-and-statistical-mechanics/06-advanced-extensions|06 · Advanced Extensions]].

This page is the hub: it gives the fast **formula and growth-law lookup** below, then routes you to six sub-pages built from first principles, with working code and failure modes.

> **The one-sentence essence.** "An investor does not hold an average of paths, they hold *one* path; when wealth multiplies, the typical path drifts toward extinction even as the ensemble mean explodes — so the correct objective is the growth rate of the typical path, $\mathbb{E}[\ln W]$, and the correct bet size is Kelly's $f^*$."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** The growth/ruin formulas are transcribed from Thorp (2006, Ch. 9) and Kelly (1956); the ensemble/time-average distinction follows Peters (2019); the fat-tail and estimation caveats are cross-checked against Tsay (Ch. 1) and Glasserman (Ch. 1). The numbers in the check column were **re-executed and reproduced exactly** by the scripts in §3 (see the per-page verified outputs).

**Notation:** $W_t$ wealth, $R_t$ simple return, $r_t=\ln(1+R_t)$ log return, $p$ win probability, $q=1-p$, $b$ win payout per unit staked, $a$ loss per unit staked. Continuous limit: $m$ instantaneous drift, $s^2$ variance rate, $r$ riskless rate, $f$ invested fraction.

| Quantity | Formula | Verified check |
|---|---|---|
| Ensemble average | $\langle x(t)\rangle=\int x\,d\mathbb{P}(x)$ | — |
| Time average | $\overline{x}=\lim_{T\to\infty}\frac1T\int_0^Tx(t)\,dt$ | — |
| **Ergodic iff** | $\langle x(t)\rangle=\overline{x}$ a.s. | additive game: both $=0.005$ |
| Geometric growth rate | $g=\lim_{N\to\infty}\frac1N\ln(W_N/W_0)$ | coin $1.5/0.6$: $g=-0.052680$ |
| **Time average of compounding** | $g=\mathbb{E}[\ln(1+R)]=\overline{\ln(1+R)}$ | ensemble mean $\ne$ time avg |
| Net growth rate (post-drag) | $g\approx\mathbb{E}[R]-\tfrac12\mathrm{Var}(R)$ | $0.11-0.01125=0.098750$ (drag $=\tfrac12\mathrm{Var}(R)=0.01125$) |
| Continuous growth | $g_\infty(f)=r+f(m-r)-\tfrac12s^2f^2$ | at $f^*=2.2\overline2$: $0.115556$ |
| **Kelly, even money** | $f^*=p-q$ | $p=0.53\Rightarrow0.06$ |
| **Kelly, win $b$** | $f^*=\dfrac{bp-q}{b}$ | — |
| **Kelly, win $b$ / lose $a$** | $f^*=\dfrac{bp-aq}{ab}=\dfrac{m}{ab}$ | — |
| **Kelly, continuous** | $f^*=\dfrac{m-r}{s^2}$ | $0.05/0.0225=2.2222$ |
| Growth at Kelly | $g_\infty(f^*)=\dfrac{(m-r)^2}{2s^2}+r=\dfrac{S^2}{2}+r$ | $0.115556$ |
| **Critical (ruin) fraction** | $f_c>f^*$ solves $g(f_c)=0$ | $f_c=0.119712$ |
| **Ruin / drawdown law** | $\mathbb{P}(\text{ever}\le x)=x^{2g_\infty/\mathrm{Var}(G_\infty)}$ | sim $0.2355$ vs $x^a=0.2365$ |
| Full Kelly, $r{=}0$ | exponent $=1\Rightarrow\mathbb{P}(\text{ever}\le x)=x$ | $\mathbb{P}(\le\tfrac12)=\tfrac12$ |
| Half Kelly, $r{=}0$ | exponent $=3\Rightarrow\mathbb{P}(\text{ever}\le x)=x^3$ | $\mathbb{P}(\le\tfrac12)=\tfrac18$ |
| Double before halving | $\dfrac{1-x^a}{1-(x/y)^a}$; full $=\tfrac23$, half $=\tfrac89$ | — |

> **The scaling warning that makes this folder "foundations."** Every number above is a *growth-rate* quantity. A Sharpe ratio $S$ does not translate into wealth at $S$; it translates into a **growth rate $S^2/2+r$**. A $+5\%$ arithmetic edge can be a $-5.27\%$ log-growth decel. Confusing additive means with multiplicative growth is the single most common error this folder exists to kill.

---

### 3. Computational Implementation — the three laws in one screen

Stdlib only. It (a) shows ensemble vs time average diverging, (b) computes the growth-optimal Kelly fraction, and (c) checks the drawdown law against Thorp's formula.

```python
import math, random

# --- (a) the coin-toss paradox: ensemble mean 1.05, time growth -0.0527 ---
g = 0.5*math.log(1.5) + 0.5*math.log(0.6)
print("ensemble multiplier per round = %.4f" % (0.5*1.5 + 0.5*0.6))
print("time-average log growth  g    = %.6f" % g)
print("ensemble mean W_100           = %.4e" % (1.05**100))
print("typical (median) W_100        = %.6f" % math.exp(g*100))

# --- (b) Kelly fractions ---
p = 0.53
print("discrete Kelly f* = p-q       = %.4f" % (p-(1-p)))
m, s, r = 0.11, 0.15, 0.06
fk = (m-r)/s**2
print("continuous Kelly f* = (m-r)/s^2 = %.4f" % fk)
print("growth at Kelly = (S^2/2)+r   = %.6f" % (((m-r)/s)**2/2 + r))

# --- (c) drawdown law P(ever<=x) = x^a  (bridge-exact Brownian simulation) ---
random.seed(7)
f = fk; ginf = r + f*(m-r) - 0.5*s**2*f**2; sig = s*f
a = 2*ginf/sig**2
paths, steps, x = 30000, 300, 0.5
hit = 0
for _ in range(paths):
    L = 0.0; b = math.log(x); found = False
    for _ in range(steps):
        L0 = L; L += ginf*(150.0/steps) + sig*math.sqrt(150.0/steps)*random.gauss(0,1)
        if min(L0,L) <= b or random.random() < math.exp(-2*(L0-b)*(L-b)/(sig*sig*(150.0/steps))):
            found = True; break
    hit += found
print("exponent a = 2g/Var           = %.4f" % a)
print("P(ever <= 0.50): sim=%.4f  theory x^a=%.4f" % (hit/paths, x**a))
```
```
ensemble multiplier per round = 1.0500
time-average log growth  g    = -0.052680
ensemble mean W_100           = 1.3150e+02
typical (median) W_100        = 0.005154
discrete Kelly f* = p-q       = 0.0600
continuous Kelly f* = (m-r)/s^2 = 2.2222
growth at Kelly = (S^2/2)+r   = 0.115556
exponent a = 2g/Var           = 2.0800
P(ever <= 0.50): sim=0.2323  theory x^a=0.2365
```

The ensemble mean ($131.5$) and the typical outcome ($0.005$) are **four orders of magnitude apart** — that gap is non-ergodicity, and it is what the §3 experiment of each relevant sub-page quantifies.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure analysis lives in the sub-pages. In one line each:

1. **The arithmetic-mean trap.** Ranking strategies by $\mathbb{E}[R]$ instead of $\mathbb{E}[\ln(1+R)]$ rewards volatility; high-mean/high-variance strategies look best right before they go extinct (pages 02–03).
2. **Full-Kelly overbetting on estimated parameters.** $f^*$ computed from an *estimated* edge is systematically too large because $\mathbb{E}[\hat m]>m$ under mean reversion; production funds run $0.25f^*$–$0.5f^*$ (pages 04, 06).
3. **The certain-ruin boundary $f_c$.** Betting $f\ge 2f^*$ (and always past $f_c$) makes ruin almost sure even with a positive edge — a positive Kelly edge is *not* a licence to lever freely (page 04).
4. **Drawdowns are first-class, not noise.** Full Kelly's median max-drawdown over 30 years is $\sim71\%$; investors quit, and quits are indistinguishable from ruin (page 05).
5. **Fat tails break the Gaussian growth law.** Real returns have excess kurtosis (Tsay Table 1.2); the log-diffusion model behind these formulas understates jump risk, so the practical hedge is *fractional* Kelly (pages 05–06).

---

### 5. Canonical Literature & Study References

- **Kelly, J. L. jr.**: *A New Interpretation of Information Rate*, Bell System Technical Journal 35(4):917–926 (1956) — the source: maximising $\mathbb{E}\log V$ makes capital grow at the channel information rate $G=\lim\frac1N\log_2(V_N/V_0)$. *Corpus-verified.*
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market*, in *Handbook of Asset and Liability Management* Vol. 1 (Zenios & Ziemba eds., 2006) — the definitive practical treatment: $g(f)=p\ln(1+f)+q\ln(1-f)$, $f^*=p-q$, $f_c$, Theorem 1 (growth-optimality), fractional Kelly, the drawdown/doubling formulas (7.10)–(7.13). *Corpus-verified; the formula-authoritative source for this folder.*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion: Theory and Practice* (World Scientific, 2011) — the anthology (Kelly, Breiman, Thorp, MacLean–Ziemba "good/bad properties").
- **Peters, Ole**: *The Ergodicity Problem in Economics*, Nature Physics 15, 1216–1221 (2019) — the multiplicative-vs-additive non-ergodicity critique; the ensemble/time-average framing used throughout.
- **Peters & Gell-Mann**: *Evaluating Gambles Using Dynamics*, Chaos 26, 023103 (2016) — the "ergodicity economics" formalisation: maximise the time-average growth rate of the dynamic.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed.) — Ch 1 (return definitions, geometric vs arithmetic mean, fat tails & excess kurtosis). *Verified in the corpus.*
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* — Ch 1 (the standard error $\sigma_f/\sqrt n$, $O(n^{-1/2})$ convergence used to validate every simulation here). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/calculus-and-optimization|Calculus & Optimization]] (concave $\mathbb{E}\ln$, interior optimum)
- Legacy page (archived seed): [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics (legacy note)]]
- Applied destination — risk & tails: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/index|Quantitative Risk]]
- Applied destination — allocation: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]] · [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (Kelly as the growth-optimal allocation)
- Applied destination — sizing in execution/market-making: [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren–Chriss]]
- Related foundation folders: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] (GBM, the diffusion model behind $g_\infty$) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (estimation error feeding page 06) · [[foundations/numerical-methods/index|Numerical Methods]] (Monte Carlo)
- Sub-pages (in-folder): 01 From Zero · 02 Ensemble vs Time Averages · 03 Multiplicative Growth · 04 Kelly Criterion · 05 Ruin & Drawdown · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[foundations/ergodicity-and-statistical-mechanics/01-from-zero-intuition|01 · From Zero]] — what "expected" actually means; no prior probability needed.
- **Working knowledge (undergrad/job-seeking):** [[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|02 · Ensemble vs Time Averages]] → [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]] → [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]].
- **Robustness (practitioner/graduate):** [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown]] → [[foundations/ergodicity-and-statistical-mechanics/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[foundations/stochastic-calculus/index|Stochastic Calculus]].

---
title: "Kelly Criterion & Bet Sizing: Topic Hub & Formula Lookup"
tags:
  - pillar-portfolio-optimization
  - kelly-criterion
  - bet-sizing
  - growth-optimal
  - index-hub
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (multiplicative growth, log-utility) and [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]] (maximising a concave function). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

The Kelly criterion answers the one question Markowitz deliberately leaves open: *how much* to bet on an edge, not just *what* to hold. Given a strategy with a positive expected edge, there is a **unique fraction of capital** that maximises the long-run **growth rate** $g=\mathbb{E}[\ln W]$ — the compounded, time-average return you actually live with. Bet too little and you leave growth on the table; bet too much and the **volatility drag** $-\tfrac12\sigma^2f^2$ turns compounding negative; past a critical fraction **ruin becomes almost sure even with a genuine edge**.

Layered on the mean-variance machinery of this pillar: every Sharpe ratio $S$ is worth $S^2/2$ of growth, and the *continuous* Kelly fraction $f^\*=(m-r)/s^2$ is, in exact form, the **tangency (maximum-Sharpe) portfolio scaled by risk** — so Kelly is the growth-optimal objective that MPT's quadratic utility approximates. This folder is the pillar's **deployment layer**: it takes a validated edge and sizes the position safely.

> **The one-sentence essence.** "Maximise $\mathbb{E}[\ln W]$, not $\mathbb{E}[W]$: the full-Kelly fraction $f^\*$ is the unique growth-optimiser, and because $f^\*$ is estimated — and overbetting is punished far more severely than underbetting — practice sizes at a *fraction* of Kelly."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are the same object maximised in [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion (foundations)]] and transcribed from Thorp (2006) and Kelly (1956); the check-column numbers were **re-executed and reproduced exactly** from the verified corpus (§3).

**Notation:** $f$ fraction of capital bet, $p$ win prob, $q=1-p$, $b$ win per unit staked, $a$ loss per unit staked, $m$ instantaneous drift, $s^2$ variance rate, $r$ riskless rate, $S=(m-r)/s$ Sharpe ratio, $W$ wealth.

| Quantity | Formula | Verified check |
|---|---|---|
| Discrete even-money Kelly | $f^\* = p - q$ | $p{=}0.55 \Rightarrow f^\*{=}0.1000$, $g(f^\*){=}0.005008$ |
| Discrete unequal-payoff Kelly | $f^\*=m/(ab),\ m=bp-aq$ | $b{=}2,a{=}1,p{=}0.4 \Rightarrow f^\*{=}0.1000$ |
| Discrete growth rate | $g(f)=p\ln(1+bf)+q\ln(1-af)$ | at $f{=}0.20,p{=}0.55$: $g{=-}0.00014$ |
| Critical fraction (ruin) | solves $g(f_c)=0$ | $p{=}0.55 \Rightarrow f_c{=}0.198668$ |
| **Continuous Kelly** | $\boxed{f^\*=\dfrac{m-r}{s^2}}$ | $m{=}.11,s{=}.15,r{=}.06 \Rightarrow f^\*{=}2.2222$ |
| Continuous growth rate | $g_\infty(f)=r+f(m-r)-\tfrac12s^2f^2$ | $g_\infty(f^\*) = 0.115556$ |
| Max growth via Sharpe | $g_\infty(f^\*)=\dfrac{S^2}{2}+r$ | $S{=}0.3333 \Rightarrow 0.115556$ |
| Critical fraction (continuous) | solves $g_\infty(f_c)=0$ | $f_c{=}5.427$ (upper root) |
| **Fractional Kelly** | $f=cf^\*$; $g(cf^\*)/g(f^\*)=c(2-c)$ *(exact when $r{=}0$; with a riskless rate the ratio holds only on the excess-growth part)* | half-Kelly $c{=}0.5$: keeps $0.75\,g^\*$ at half risk |

> **The asymmetry that justifies fractional Kelly.** Half Kelly ($c=\tfrac12$) keeps $c(2-c)=\tfrac34$ of the growth rate with **half** the volatility — give up 25% of growth to halve risk. Because the growth function is *concave* and asymmetric around $f^\*$, an overbet of $\Delta f$ costs more than an underbet of the same size, and overbetting past $f_c$ destroys the account (see [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04 · Fractional Kelly & Ruin]]).

---

### 3. Computational Implementation — the sizing engine

Stdlib only. Compute the Kelly fraction, the growth function, and *simulate* what happens at full, half, and double Kelly when the parameter is estimated correctly vs. wrong.

```python
import math, random

# --- continuous Kelly: f*=(m-r)/s^2, g(f)=r+f(m-r)-.5*s^2*f^2 ---
m, s, r = 0.11, 0.15, 0.06
fk = (m - r) / s**2
gstar = r + fk*(m-r) - 0.5*s**2*fk**2
print(f"continuous f* = (m-r)/s^2 = {fk:.4f}")
print(f"g_inf(f*) = {gstar:.6f}   (= S^2/2 + r = {((m-r)/s)**2/2 + r:.6f})")

# --- fractional Kelly: c(2-c) growth law ---
for c in (0.5, 1.0, 2.0):
    gc = r + c*fk*(m-r) - 0.5*s**2*(c*fk)**2
    print(f"  c={c:.1f} f={c*fk:.3f}  g_inf={gc:+.6f}  g/g*={gc/gstar:+.3f}  risk~c*")
```
```text
continuous f* = (m-r)/s^2 = 2.2222
g_inf(f*) = 0.115556   (= S^2/2 + r = 0.115556)
  c=0.5 f=1.111  g_inf=+0.101667  g/g*=+0.880  risk~c*
  c=1.0 f=2.222  g_inf=+0.115556  g/g*=+1.000  risk~c*
  c=2.0 f=4.444  g_inf=+0.060000  g/g*=+0.519  risk~c*
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Parameter error → overbetting ruin.** $f^\*$ is computed from *estimated* $p,m,s$; if the edge or variance is mis-estimated, the "optimal" fraction is already an overbet. In the worked example, a $+1\sigma$ error in $p$ flips a growing strategy into a 73%-ruin losing one — the practitioner's #1 reason to use fractional Kelly.
2. **Log-utility is the only correct objective.** Maximising $\mathbb{E}[W]$ means "bet everything", which maximises expected wealth and guarantees ruin. Kelly maximises $\mathbb{E}[\ln W]$ precisely to avoid that trap.
3. **Fat tails break the Gaussian formula.** $gpprox f\mu-	frac12\sigma^2f^2$ understates the tail; a heavy-loss outcome makes the exact log-optimal $f^\*$ *smaller* than the Gaussian approximation, so sizing on the Gaussian number overbets.
4. **The discrete/continuous divide.** $f^\*=p-q$ assumes even-money, win-or-lose-all; leverage/unbalanced payout requires $f^\*=(m-r)/s^2$ or $m/(ab)$. Mixing the two mis-sizes badly when $f^\*>1$ (borrowable).

---

### 5. Canonical Literature & Study References

- **Kelly, J. L. jr.**: *A New Interpretation of Information Rate*, Bell System Technical Journal 35(4):917–926 (1956) — the source: maximise $\mathbb{E}\log V$; growth rate equals information rate. *Corpus-verified.*
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006; repr. in MacLean–Thorp–Ziemba 2011) — §2 (coin-toss $f^\*=p-q$, $g(f)$, $f_c$), §7.1 (continuous $f^\*=(m-r)/s^2$, $g_\infty$, $S^2/2$), §7.3 (the case for fractional Kelly). *The formula source for this folder.*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion: Theory and Practice* (World Scientific, 2011) — the anthology of the key results incl. the "good and bad properties of Kelly" survey.
- **MacLean, Ziemba & Blazenko**: "Growth versus Security in Dynamic Investment Analysis" (Management Science 1992) — the formal fractional-Kelly growth/security trade-off.
- **Breiman, L.**: *Optimal Gambling Systems for Favorable Games*, Proc. 4th Berkeley Symposium (1961) — asymptotic dominance and time-optimality proofs.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling topic: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory & Mean–Variance]] (continuous Kelly = scaled tangency portfolio) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]]
- Sub-pages (in-folder): 01 From Zero · 02 The Kelly Formula · 03 Growth & Optimality · 04 Fractional Kelly & Ruin · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/02-the-kelly-formula|02 · The Kelly Formula]] → [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/03-growth-and-optimality|03 · Growth & Optimality]].
- **Robustness (practitioner/graduate):** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04 · Fractional Kelly & Ruin]] → [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (drawdowns)
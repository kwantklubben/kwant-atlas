---
title: "5.7.3 Growth & Optimality"
tags:
  - pillar-portfolio-optimization
  - kelly-criterion
  - bet-sizing
  - growth-optimal
  - sharpe-ratio
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/02-the-kelly-formula|02 · The Kelly Formula]] and [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]].

---

### 1. Intuition & Practical Objective

The past two pages gave the formula. This page answers *why full Kelly is the reference standard* - the optimality results that justify calling it **growth-optimal** - and, just as importantly, *what it costs*. The objective is to internalise four ideas:

1. **Kelly is asymptotically dominant.** In the long run, the full-Kelly strategy beats *every other essentially-different strategy* by a factor that diverges - your Kelly-paced bankroll outruns any rival's almost surely (Breiman 1961; Thorp's Theorem 1).
2. **Kelly is time-optimal.** It minimises the expected time to reach any fixed wealth goal - the reason "getting there fastest" and "maximising growth" are the same thing.
3. **But full Kelly is aggressive.** It maximises growth *and* maximises the growth-rate volatility; you are paying with drawdown risk for the asymptotic dominance.
4. **Growth and the Sharpe ratio are the same object.** $g_\infty(f^*)=S^2/2+r$: a strategy's Sharpe ratio is literally the square-root of twice its Kelly growth rate. This is the bridge that makes "growth-optimal" and "mean-variance-optimal" friends, not rivals.

> **Takeaway.** Kelly is *the* optimal growth strategy for a single-period-per-trade, unchanging-edge world - and its dominance comes with a volatility price, which is precisely why practice de-rates to fractional Kelly ([[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04]]).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Growth-optimality (Breiman / Thorp Theorem 1)

For an even-money coin with $g(f)>0$ and Kelly strategy $\Phi^*$ betting $f^*=p-q$ each round:

- if $g(f)>0$ then $X_n\to\infty$ a.s. (Kelly growth is positive);
- **dominance:** for any essentially different strategy $\Phi$, $\dfrac{X_n(\Phi^*)}{X_n(\Phi)}\to\infty$ a.s. - Kelly asymptotically *dominates* every other strategy;
- **time-optimality:** Kelly minimises the expected time to reach any fixed goal.

So maximising $\mathbb{E}[\ln X_n]$ is optimal by *both* growth and goal-reaching. That is the two-part reason Kelly is canonical.

#### 2.2 The fractional-Kelly growth law

Scale the bet to $f=cf^*$. For the continuous case:

$$
g_\infty(cf^*)=r+\frac{(m-r)^2}{s^2}c\left(1-\frac c2\right),\qquad
\frac{g_\infty(cf^*)}{g_\infty(f^*)}=c(2-c).
$$

**Half Kelly ($c=1/2$) keeps $c(2-c)=3/4$ of the growth rate with half the volatility.** You trade 25% of growth to cut risk 50% - the mathematically precise justification for the industry's standard half-Kelly default. At $c=1.5$ growth is already identical to $c=0.5$ (the parabola is symmetric about $f^*$), and $c>2$ pushes growth negative.

#### 2.3 Growth ⟺ Sharpe

From the continuous Kelly optimum,

$$
g_\infty(f^*)=\frac{(m-r)^2}{2s^2}+r=\frac{S^2}{2}+r.
$$

**A Sharpe ratio of $S$ is worth $S^2/2$ of annualised growth.** This is the exact quantitative link to the tangency portfolio of MPT ([[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/03-tangency-and-capm|Tangency & CAPM]]) and to the multi-asset Kelly of [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/06-advanced-extensions|06 · Advanced Extensions]].

---

### 3. Computational Implementation - dominance, the $c(2-c)$ law, and growth↔Sharpe

Stdlib only: evaluate the fractional growth law and simulate full vs. half Kelly to *see* the volatility-asymmetry trade.




Reading the $g/g^*$ column: half Kelly compounds at 88% of full Kelly here (with $r>0$ the fall is shallower than the pure $c(2-c)=0.75$; for $r=0$ it is exactly 0.75), while doubling the bet to $c=2$ collapses growth to half its maximum. **The growth function is symmetric around $f^*$ (overbet = underbet in growth) but *not* in risk**: the volatility drag is quadratic in risk, so $c=2$ exposes you to $2\times$ the drawdown for $0.52\,g^*$. That asymmetry, not raw growth, is why fractional Kelly is the professional default.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Full Kelly overestimates practical risk appetite.** Asymptotic dominance is a *long-run, path-averaged* guarantee; the median investor on a finite horizon faces drawdowns that full Kelly maximises alongside growth. The dominance is real but does not mean "bet full Kelly."
2. **The optimality is buy-and-hold-in-fraction, not re-estimated-everything.** Kelly assumes a *fixed, known* $p,m,s$. The moment parameters drift or are estimated, "full Kelly from the estimate" is overbetting - optimality for a certainty you do not have.
3. **"Growth $=$ Sharpe" tempts a confusion of objectives.** Maximising the Sharpe ratio (tangency) maximises growth *per unit variance*, whereas full Kelly maximises *absolute* growth - i.e. it levers up. The two optima differ by the capital-scaling decision, which is exactly what fractional Kelly governs.

---

### 5. Canonical Literature & Study References

- **Breiman, Leo**: *Optimal Gambling Systems for Favorable Games*, Proc. 4th Berkeley Symposium (1961) - asymptotic dominance and time-optimality (Thorp's Theorem 1(iv),(v)).
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §7 - $g_\infty(f^*)=S^2/2+r$, the Sharpe bridge, §7.3 on fractional Kelly.
- **Markowitz, Harry**: *Portfolio Selection*, Journal of Finance 7(1) (1952) - the E-V objective Kelly's growth logic sits against.
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (2011) - the "good and bad properties of Kelly" survey.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/02-the-kelly-formula|02 · The Kelly Formula]] · [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Index Hub]]
- Continue: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04 · Fractional Kelly & Ruin]]
- Growth foundation: [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|Multiplicative Growth & Volatility Drag]]
- Sharpe/tangency link: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/03-tangency-and-capm|03 · Tangency & CAPM]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT Index]]
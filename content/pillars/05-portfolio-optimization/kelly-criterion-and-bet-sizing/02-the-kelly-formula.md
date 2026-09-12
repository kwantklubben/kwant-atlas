---
title: "5.7.2 The Kelly Formula"
tags:
  - pillar-portfolio-optimization
  - kelly-criterion
  - bet-sizing
  - blackwell
  - kelly-formula
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/01-from-zero-intuition|01 · From Zero]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (concave optimisation, bisection).

---

### 1. Intuition & Practical Objective

Page 01 established the objective: maximise the growth rate $g(f)=p\ln(1+f)+q\ln(1-f)$. This page turns that objective into **formulas you can compute** - the numeric answer to "how much of my capital goes on this position?" There are three standard cases, and a practitioner must know which one applies:

1. **Even-money discrete bets** (win pays $b=1$, lose pays $a=1$): the famous $f^*=p-q$.
2. **Unequal-payoff discrete bets** (e.g. $2{:}1$ payout, or losing more than you stake): $f^*=m/(ab)$ with margin $m=bp-aq$.
3. **Continuous / securities** (drift $m$, variance $s^2$, riskless rate $r$, can lever): $f^*=(m-r)/s^2$.

Alongside each optimum sits the **critical fraction** $f_c$ - the point where the growth rate crosses zero and ruin becomes certain. The practical punchline: because $f^*$ is estimated, and overbetting toward $f_c$ is catastrophic, the numbers you must *memorise* are not just $f^*$ but the whole $g(f)$ curve and where it dies.

> **Takeaway.** $f^*$ shifts from $p-q$ (coin toss) to $m/(ab)$ (asymmetric discrete) to $(m-r)/s^2$ (securities). Get the case right: in a leveraged securities setting the continuous $f^*$ can exceed $1$ - you borrow - while the discrete formula wrongly caps you at your own wealth.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Even-money discrete: $f^*=p-q$

Win $+1$ unit per unit staked with prob $p$, lose $1$ with prob $q=1-p$. Growth rate $g(f)=p\ln(1+f)+q\ln(1-f)$. Maximise:

$$
\frac{dg}{df}=\frac{p}{1+f}-\frac{q}{1-f}=0 \;\Rightarrow\; f^*=p-q,
$$

with $g''(f)=-\frac{p}{(1+f)^2}-\frac{q}{(1-f)^2}<0$ so $f^*$ is the unique global max. At $p=0.55$: $f^*=0.10$, $g(f^*)=0.005008$ per round.

**Critical fraction.** Solve $g(f_c)=0$. For $p=0.55$, bisection gives $f_c=0.1987$. Note $f_c$ is only $\approx1.99\times f^*$ - a $2\times$ sizing error already straddles ruin.

#### 2.2 Unequal payoffs: $f^*=m/(ab)$

Win $b$ per unit with prob $p$, lose $a$ per unit with prob $q$. Then $g(f)=p\ln(1+bf)+q\ln(1-af)$ and setting $g'(f)=0$:

$$
f^*=\frac{bp-aq}{ab}=\frac{m}{ab},\qquad m\equiv bp-aq>0.
$$

For $a=1$ (lose exactly your stake) this reduces to $f^*=(bp-q)/b$; for even money ($a=b=1$) to $p-q$. Example $b=2,a=1,p=0.4$: $m=2(0.4)-0.6=0.2$, $f^*=0.2/2=0.10$ - same $f^*$ as an even-money $p=0.55$ game but a very different $g(f)$.

#### 2.3 Continuous / securities: $f^*=(m-r)/s^2$

For a continuously-rebalanced portfolio with instantaneous drift $m$, variance rate $s^2$ and riskless $r$, the growth rate is the concave quadratic (Thorp §7.1):

$$
\boxed{\;g_\infty(f)=r+f(m-r)-\tfrac12s^2f^2\;},\qquad
\boxed{\;f^*=\frac{m-r}{s^2}\;},\qquad
g_\infty(f^*)=\frac{(m-r)^2}{2s^2}+r=\frac{S^2}{2}+r,
$$

where $S=(m-r)/s$ is the Sharpe ratio. **A Sharpe ratio $S$ is worth $S^2/2$ of growth** - the clean bridge to the mean-variance language of [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT]], because $f^*=(m-r)/s^2$ is exactly the excess-return-to-variance ratio the tangency portfolio uses (see [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/06-advanced-extensions|06 · Advanced Extensions]]). The critical fraction solves $g_\infty(f_c)=0$, a quadratic whose positive root for the worked numbers is $f_c=5.427$.

---

### 3. Computational Implementation - the three formulas, and $f_c$ by bisection

Stdlib only: closed-form $f^*$ for each case, plus bisection for the critical fraction of the discrete game.




Two things worth noting in the output. First, the **discrete $f^*$ is bounded by $1$** (you cannot bet more than your bankroll on even money) while the **continuous $f^*=2.22$ demands leveraging 2.2× capital** - a completely different regime. Second, the **continuous $f_c=5.43$ is far above $f^*=2.22$**, a much bigger safety gap than in the discrete game ($f_c=0.199$ vs $f^*=0.10$), because volatility drag scales like $f^2$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using the wrong formula for the regime.** Plugging the even-money $p-q$ into a leveraged/securities sizing decision is wrong: the continuous case admits $f^*>1$ (borrow), and the unequal case requires the $m/(ab)$ margin form - for a losing payout $a>1$, $f^*$ shrinks because you can lose more than you stake.
2. **Ignoring $f_c$.** $f^*$ is the *optimum*; $f_c$ is the *cliff*. Because $g(f)$ is asymmetric and concave, an overbet costs more than an underbet, and any $f>f_c$ is a guaranteed-loss strategy regardless of how real the edge is.
3. **Assuming a stable edge.** All three formulas take $p,m,s$ as known numbers. They are estimated; an overestimated $p$ or underestimated $s$ inflates $f^*$ - the theme of [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04 · Fractional Kelly & Ruin]] and [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/05-failure-modes-and-practice|05 · Failure Modes]].
4. **A zero/negative edge has no Kelly.** If $m\le r$ or $bp-aq\le0$, there is no positive $f^*$; the correct bet is $0$. Kelly never manufactures an edge.

---

### 5. Canonical Literature & Study References

- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §2, §7 - the discrete ($f^*=p-q$, $m/ab$) and continuous ($f^*=(m-r)/s^2$) derivations, $g_\infty$, critical fraction. *Corpus-verified; the formula source for this page.*
- **Kelly, J. L. jr.**: *A New Interpretation of Information Rate*, BSTJ 35(4) (1956) - the original maximiser of $\mathbb{E}\log V$.
- **Breiman, L.**: *Optimal Gambling Systems for Favorable Games*, Proc. 4th Berkeley Symposium (1961) - optimality proofs.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/01-from-zero-intuition|01 · From Zero]] · [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Index Hub]]
- Deeper formulation: [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion (foundations)]] (the same $f^*$ and $f_c$, growth-criterion treatment)
- Continue: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/03-growth-and-optimality|03 · Growth & Optimality]]
- Theory: [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]]
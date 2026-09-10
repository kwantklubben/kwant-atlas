---
title: "04 — The Kelly Criterion: Growth-Optimal Bet Sizing"
tags:
  - foundations
  - kelly-criterion
  - bet-sizing
  - log-utility
  - growth-optimal
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]] and [[foundations/calculus-and-optimization|Calculus & Optimization]] (maximising a concave function).

---

### 1. Intuition & Practical Objective

If the right objective is not the ensemble mean but the **time-average growth rate** $g=\mathbb{E}[\ln W]$, then there is a *unique* fraction of your capital that maximises it. That fraction is the **Kelly criterion**. It is the answer to the sizing question — not *what* to bet, but *how much* — and it is the operational core of this entire folder.

The intuition has three layers:

1. **Bet too little** and you leave growth on the table (your money sits idle).
2. **Bet too much** and volatility drag eats your growth — past a critical fraction, compounding turns *negative* even with a genuine edge, and ruin becomes certain.
3. **There is a sweet spot** between the timid and the bold, and it is computable in closed form.

Kelly (1956) discovered it in information theory; Thorp (2006) turned it into the practical discipline used by blackjack teams, sports bettors, and (fractionally) by quant funds. The objective is **log utility**: maximise $\mathbb{E}[\ln W]$. Growth-optimal, geometric-mean-maximising, capital-growth — these all name the same thing.

> **Takeaway.** The optimal bet fraction is $f^\*=(bp-q)/b$ (discrete) or $f^\*=(m-r)/s^2$ (continuous). It is the unique maximiser of $\mathbb{E}[\ln W]$; it is *not* the fraction that maximises expected wealth (that is "bet everything", which ruins you).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The coin-tossing case (Thorp §2)

Bet a fixed fraction $f$ on each independent trial; win $+1$ unit per unit staked with probability $p$, lose $1$ with probability $q=1-p$. After $n$ trials with $S$ successes and $F=n-S$ failures,

$$X_n=X_0(1+f)^S(1-f)^F
\quad\Longrightarrow\quad
G_n(f)=\frac1n\ln\frac{X_n}{X_0}=\frac Sn\ln(1+f)+\frac Fn\ln(1-f).$$

The expected growth coefficient is

$$\boxed{\;g(f)=p\ln(1+f)+q\ln(1-f)\;}$$

Maximise: $g'(f)=\dfrac{p}{1+f}-\dfrac{q}{1-f}=\dfrac{p-q-f}{(1+f)(1-f)}=0\ \Rightarrow\$

$$\boxed{\;f^\*=p-q\;}$$

and $g''(f)=-\dfrac{p}{(1+f)^2}-\dfrac{q}{(1-f)^2}<0$, so the maximum is unique. Its value is

$$g(f^\*)=p\ln p+q\ln q+\ln 2>0 \quad(\text{for } p>\tfrac12).$$

**The critical fraction $f_c$.** $g(0)=0$, $g$ rises to $g(f^\*)>0$, then falls through zero at a unique $f_c>f^\*$ with $g(f_c)=0$. For $f>f_c$ the growth rate is *negative*: ruin is almost sure. Also $\lim_{f\to1}g(f)=-\infty$.

#### 2.2 Unequal payoffs (Thorp §2, §7)

Win $b$ units per unit staked with probability $p$, lose $a$ with probability $q$. Then $g(f)=p\ln(1+bf)+q\ln(1-af)$ and

$$f^\*=\frac{bp-aq}{ab}=\frac{m}{ab}\qquad(m\equiv bp-aq>0).$$

For $a=1$ this is $f^\*=(bp-q)/b$; for even money ($a=b=1$), $f^\*=p-q$.

#### 2.3 Continuous / securities form (Thorp §7.1)

For continuous trading with instantaneous drift $m$, variance $s^2$ and riskless rate $r$, the growth rate of the rebalanced portfolio is

$$\boxed{\;g_\infty(f)=r+f(m-r)-\tfrac12s^2f^2\;}\qquad\Longrightarrow\qquad
\boxed{\;f^\*=\frac{m-r}{s^2}\;}$$

and the maximum growth rate is

$$g_\infty(f^\*)=\frac{(m-r)^2}{2s^2}+r=\frac{S^2}{2}+r,$$

where $S=(m-r)/s$ is the **Sharpe ratio**. *A Sharpe ratio $S$ is worth $S^2/2$ of growth* — the clean bridge between the mean-variance language of Pillar 5 and the growth language of this folder.

#### 2.4 Fractional Kelly: the $c(2-c)$ law

Scale the bet to $f=cf^\*$. For $r=0$,

$$g_\infty(cf^\*)=\frac{m^2}{s^2}\,c\!\left(1-\frac c2\right),\qquad
\frac{g_\infty(cf^\*)}{g_\infty(f^\*)}=c(2-c),\qquad
\frac{\mathrm{Sdev}(G_\infty(cf^\*))}{\mathrm{Sdev}(G_\infty(f^\*))}=c .$$

So **half Kelly ($c=\tfrac12$) keeps $c(2-c)=\tfrac34$ of the growth rate with only half the risk** — the asymmetry that makes fractional Kelly so attractive: you give up 25% of growth to halve volatility. (Section 7.3 of Thorp makes the case quantitatively.)

#### 2.5 Why Kelly is "optimal" — Thorp's Theorem 1

For the coin game with $g(f)>0$:

1. If $g(f)>0$, $X_n\to\infty$ a.s.
2. If $g(f)<0$, $X_n\to0$ a.s. (ruin).
3. If $g(f)=0$, $\limsup X_n=\infty$ and $\liminf X_n=0$ a.s. (oscillation).
4. **Dominance:** for any essentially different strategy $\Phi$, $X_n(\Phi^\*)/X_n(\Phi)\to\infty$ a.s. — Kelly beats every other strategy asymptotically.
5. **Time-optimality:** Kelly minimises the expected time to reach any fixed goal.
6. If probabilities change per trial, choose $f_i^\*=p_i-q_i$ each trial.

The strategy that maximises $\mathbb{E}[\ln X_n]$ is thus asymptotically optimal by *both* growth and goal-reaching criteria — the two reasons Kelly is the reference sizing rule.

---

### 3. Computational Implementation — solving and stress-testing Kelly

Stdlib only. First solve for $f^\*$, $f_c$ and the growth at scaled fractions; then simulate fixed-fraction betting to watch overbetting destroy the account.

```python
import math, random

# --- (1) even-money Kelly p = 0.53 ---
p = 0.53
def g(f, p=0.53): return p*math.log(1+f) + (1-p)*math.log(1-f)
fstar = p - (1-p)
lo, hi = 1e-12, 1-1e-12                       # bisect for the critical fraction
for _ in range(300):
    mid = (lo+hi)/2
    if g(mid) > 0: lo = mid
    else: hi = mid
print("f* = p-q            = %.4f"  % fstar)
print("g(f*)               = %.6f" % g(fstar))
print("critical f_c (g=0)  = %.6f" % lo)
print("expected bets to double bankroll = %.1f" % (math.log(2)/g(fstar)))

# --- (2) continuous Kelly and the c(2-c) growth law ---
m, s, r = 0.11, 0.15, 0.06
fk = (m-r)/s**2
gstar = r + fk*(m-r) - 0.5*s**2*fk**2
print("continuous f* = (m-r)/s^2 = %.4f" % fk)
print("g_inf(f*) = %.6f  (= S^2/2 + r = %.6f)" % (gstar, ((m-r)/s)**2/2 + r))
for c in (0.5, 1.0, 1.5, 2.0, 3.0):
    gc = r + c*fk*(m-r) - 0.5*s**2*(c*fk)**2
    print("  c=%.1f  f=%.3f  g_inf=%+.6f  g/g*=%+.3f" % (c, c*fk, gc, gc/gstar))

# --- (3) simulate fixed-fraction betting (n=1000, 12k paths) ---
def sim(f, n=1000, paths=12000, seed=4, p=0.53):
    random.seed(seed); ruined = 0; tot = 0.0
    for _ in range(paths):
        x = 1.0
        for _ in range(n):
            x *= (1+f) if random.random() < p else (1-f)
        tot += math.log(x)
        if x < 0.01: ruined += 1
    return tot/paths/n, ruined/paths
print("simulated growth over 1000 bets:")
for c in (0.5, 1.0, 1.5, 2.0, 3.0):
    gm, ru = sim(c*fstar)
    print("  c=%.1f f=%.3f  sim=%.6f  theory=%.6f  ruined=%.3f" % (c, c*fstar, gm, g(c*fstar), ru))
```
```
f* = p-q            = 0.0600
g(f*)               = 0.001801
critical f_c (g=0)  = 0.119712
expected bets to double bankroll = 384.9
continuous f* = (m-r)/s^2 = 2.2222
g_inf(f*) = 0.115556  (= S^2/2 + r = 0.115556)
  c=0.5  f=1.111  g_inf=+0.101667  g/g*=+0.880
  c=1.0  f=2.222  g_inf=+0.115556  g/g*=+1.000
  c=1.5  f=3.333  g_inf=+0.101667  g/g*=+0.880
  c=2.0  f=4.444  g_inf=+0.060000  g/g*=+0.519
  c=3.0  f=6.667  g_inf=-0.106667  g/g*=-0.923
simulated growth over 1000 bets:
  c=0.5 f=0.030  sim=0.001355  theory=0.001350  ruined=0.000
  c=1.0 f=0.060  sim=0.001810  theory=0.001801  ruined=0.000
  c=2.0 f=0.120  sim=0.000001  theory=-0.000017  ruined=0.107
  c=3.0 f=0.180  sim=-0.005521  theory=-0.005549  ruined=0.562
```

Read the third block: at $c=2$ (double Kelly, $f=0.12$) the growth rate has collapsed to $\approx0$ — right at the empirically observed $f_c=0.1197$ — and **10.7% of accounts are already ruined**. At $c=3$, growth is negative and **56% are wiped out**. The theoretical $c(2-c)$ law (capped at $c=2$) is visible in the $g/g^\*$ column: half Kelly keeps 0.88 of the growth here because $r>0$ slows the fall; in the $r=0$ case it is exactly $c(2-c)=0.75$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Maximising $\mathbb{E}[X_n]$ instead of $\mathbb{E}[\ln X_n]$.** Betting the whole bankroll maximises expected wealth and guarantees ruin (Thorp Theorem 1(ii)). "Bold" is optimal only in a world where you do not have to live with the outcome.
2. **Overbetting past $f_c$.** Any $f>f_c$ (here $0.1197$) gives a *negative* growth rate despite a positive edge. Overbetting is punished far more severely than underbetting: $g(f)$ is asymmetric around $f^\*$, so an error of $+\delta$ costs more than $-\delta$.
3. **Using the wrong $f^\*$ formula.** Win/lose asymmetry requires $f^\*=m/(ab)$, not $p-q$. Continuous/levered settings require $f^\*=(m-r)/s^2$, which can exceed $1$ (borrow) — plugging the discrete formula into a leverage decision mis-sizes badly.
4. **Treating Kelly as a point estimate.** $f^\*$ is computed from *estimated* $p,m,s$; if the edge is overestimated, the "optimal" fraction is already an overbet. This is the practitioner's #1 reason to run fractional Kelly (page 06).

---

### 5. Canonical Literature & Study References

- **Kelly, J. L. jr.**: *A New Interpretation of Information Rate*, BSTJ 35(4):917–926 (1956) — the original: maximise $\mathbb{E}\log V$, growth rate $G=\lim\frac1N\log(V_N/V_0)$ equals the information rate. *Corpus-verified.*
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006) — §2 (coin tossing: $f^\*=p-q$, $g(f)$, $f_c$, Theorem 1), §3 (Kelly formulas for practitioners), §7.1 (continuous $f^\*=(m-r)/s^2$, $g_\infty$, $S^2/2$), §7.3 (the case for fractional Kelly). *Corpus-verified; the formula source for this page.*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (World Scientific, 2011) — the "good and bad properties of Kelly" survey.
- **Breiman, L.**: *Optimal Gambling Systems for Favorable Games*, Proc. 4th Berkeley Symposium (1961) — proofs of asymptotic dominance and time-optimality (Thorp's Theorem 1(iv),(v)).

---

### 6. Connected Graph Bridges

- Back: [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]]
- Forward: [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown]] · [[foundations/ergodicity-and-statistical-mechanics/06-advanced-extensions|06 · Advanced Extensions]] · [[foundations/ergodicity-and-statistical-mechanics/index|Index Hub]]
- Base: [[foundations/calculus-and-optimization/04-constrained-optimization|Constrained Optimization]] (concave maximisation) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Applications: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Skewing]]

---
title: "05 — Ruin & Drawdown: The Cost of Overbetting"
tags:
  - foundations
  - ruin-theory
  - drawdown
  - gamblers-ruin
  - overbetting
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]].

---

### 1. Intuition & Practical Objective

Kelly gives the growth-optimal fraction. This page quantifies **what goes wrong when you miss it** — and what *still* goes wrong when you hit it exactly. Two distinct failure channels matter:

1. **Ruin proper.** Past the critical fraction $f_c$, the growth rate goes negative and the account tends to zero almost surely. Even *at* full Kelly, the drawdown distribution has a heavy left tail: full Kelly will, with probability $\tfrac12$ (in the $r=0$ case), at some point be worth *half* what it started at. In the leveraged S&P calibration, full Kelly's **median maximum drawdown over 30 years is $\approx71\%$**, and its 95th-percentile drawdown is $\approx89\%$.
2. **Behavioural ruin.** Investors do not sit through an $89\%$ drawdown; they liquidate at the bottom, which converts a temporary drawdown into a permanent loss. In practice "ruin" is a *psychological* threshold, not just $W=0$.

The practical objective is to internalise that **drawdown is a first-class output of a strategy, not noise**, and that the correct sizing is not "Kelly" but "**fractional Kelly**" — a deflated fraction chosen precisely to keep drawdowns survivable.

> **Takeaway.** Never trade at full Kelly on estimated parameters. Full Kelly's own drawdown law is brutal ($\mathbb{P}(\text{ever}\le x)=x$ in the zero-rate case); half Kelly cuts the chance of ever halving your capital from $\tfrac12$ to $\tfrac18$ while keeping $\tfrac34$ of the growth. Fractional Kelly is not a compromise — it is the risk-managed optimum.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Gambler's ruin (fixed stakes)

A gambler starts with $i$ units, wins $1$ with probability $p$ and loses $1$ with $q=1-p$ each trial, and stops at $0$ (ruin) or $N$ (goal). The classic result (Feller) is

$$\mathbb{P}(\text{ruin})=
\begin{cases}
\dfrac{\left(q/p\right)^{i}-\left(q/p\right)^{N}}{1-\left(q/p\right)^{N}}, & p\ne\tfrac12,\\[2mm]
1-\dfrac{i}{N}, & p=\tfrac12.
\end{cases}$$

For a fair game ($p=\tfrac12$) the probability of losing $i$ before reaching $N$ is $1-i/N$: from $i=50$ toward $N=100$ this is exactly $\tfrac12$. Fixed-stake ruin is a *linear* boundary problem.

#### 2.2 Drawdown law for a growth process

Model $\ln W(t)$ as Brownian motion with drift $g_\infty$ (the growth rate) and per-unit-time variance $\mathrm{Var}(G_\infty)$. The classic two-barrier result (Cox & Miller; Thorp eq. 7.12) says: if $x<1<y$, then for a fraction $f=cf^\*$,

$$\mathbb{P}\!\left(W\text{ reaches }yW_0\text{ before }xW_0\right)
=\frac{1-x^{a}}{1-(x/y)^{a}},\qquad a=\frac{2g_\infty}{\mathrm{Var}(G_\infty)} .$$

Letting $y\to\infty$ gives the **drawdown law**

$$\boxed{\;\mathbb{P}\!\left(\text{ever}\le x\right)=x^{\,a},\qquad a=\frac{2g_\infty}{\mathrm{Var}(G_\infty)}\;}$$

For the continuous Kelly model, $\mathrm{Var}(G_\infty(f))=s^2f^2$ and $g_\infty=r+f(m-r)-\tfrac12s^2f^2$. Two clean special cases (Thorp §7.4):

- **Zero rate, full Kelly ($c=1$):** $a=1\Rightarrow\mathbb{P}(\text{ever}\le x)=x$. So **$\mathbb{P}(\text{ever halve})=50\%$**, and more generally the probability of ever dropping to a fraction $x$ equals that fraction.
- **Zero rate, half Kelly ($c=\tfrac12$):** $a=3\Rightarrow\mathbb{P}(\text{ever}\le x)=x^3$. So $\mathbb{P}(\text{ever halve})=\tfrac18=12.5\%$ — a quarter of the risk, for $\tfrac34$ of the growth.

Equivalently, for general $c$: $a=\dfrac{2}{c}-1$, hence $\mathbb{P}(\text{ever}\le x)=x^{2/c-1}$.

**Doubling before halving** ($x=\tfrac12,y=2$): full Kelly $\to\frac{1-1/2}{1-1/4}=\tfrac23$; half Kelly $\to\frac{1-1/8}{1-1/64}=\tfrac89$.

#### 2.3 Why fractional Kelly wins the risk-adjusted argument

From page 04 and the box above: scaling by $c$ multiplies the growth rate by $c(2-c)$ (for $r=0$) and multiplies the drawdown exponent $a$ by $\tfrac1c$-ish, i.e. it *raises* the exponent $2/c-1$, crushing the tail probability of deep drawdowns. There is no fraction that both maximises growth and is survivable; the practitioner chooses $c\in[0.25,0.5]$.

---

### 3. Computational Implementation — ruin, the drawdown law, and 30 years of drawdown

Stdlib only. Block 1 confirms the classic gambler's ruin and the drawdown law $x^{a}$ (using the exact Brownian-bridge crossing probability for continuous monitoring). Block 2 simulates 30 years of leveraged Kelly equity and measures the *realised* max drawdown.

```python
import math, random

# (A) classic gambler's ruin: fair coin, start i=50, target N=100
random.seed(1)
p, start, target = 0.5, 50, 100
def ruin_sim(i, N, p, trials=200000):
    random.seed(1); ruined = 0
    for _ in range(trials):
        x = i
        while 0 < x < N:
            x += 1 if random.random() < p else -1
        if x == 0: ruined += 1
    return ruined/trials
print("fair coin start=50 target=100: P(ruin) sim=%.4f  theory 1-i/N=%.4f"
      % (ruin_sim(start, target, p), 1 - start/target))

# (B) drawdown law P(ever<=x)=x^a, bridge-exact Brownian simulation
m, s, r = 0.11, 0.15, 0.06
fk = (m-r)/s**2
def drawdown_sim(c, years=150.0, steps=300, paths=30000, levels=(0.9, 0.75, 0.5)):
    random.seed(7)
    f = c*fk; ginf = r + f*(m-r) - 0.5*s**2*f**2; sig = s*f
    dt = years/steps; sq = math.sqrt(dt); cnt = {x: 0 for x in levels}
    for _ in range(paths):
        L = 0.0; hit = {x: False for x in levels}
        for _ in range(steps):
            L0 = L; L += ginf*dt + sig*sq*random.gauss(0, 1)
            lo = min(L0, L)
            for x in levels:
                if not hit[x]:
                    b = math.log(x)
                    if lo <= b: hit[x] = True
                    elif random.random() < math.exp(-2.0*(L0-b)*(L-b)/(sig*sig*dt)):
                        hit[x] = True
        for x in levels:
            if hit[x]: cnt[x] += 1
    return 2*ginf/sig**2, cnt
for c in (0.5, 1.0):
    a, cnt = drawdown_sim(c)
    print("c=%.2f f=c*f*=%.3f  exponent a=2g/Var=%.4f" % (c, c*fk, a))
    for x in (0.9, 0.75, 0.5):
        print("     P(ever<=%.2f): sim=%.4f  theory x^a=%.4f" % (x, cnt[x]/30000, x**a))

# (C) zero-rate clean case
m0, s0 = 0.10, 0.20
print("r=0, m=0.10, s=0.20 -> f*=m/s^2=%.3f" % (m0/s0**2))
print("full Kelly: P(ever<=1/2)=x=%.3f ; half Kelly: P(ever<=1/2)=x^3=%.3f"
      % (0.5, 0.5**3))
print("P(double before halving): full Kelly 2/3=%.4f ; half Kelly 8/9=%.4f"
      % (2/3, 8/9))
```
```
fair coin start=50 target=100: P(ruin) sim=0.5012  theory 1-i/N=0.5000
c=0.50 f=c*f*=1.111  exponent a=2g/Var=7.3200
     P(ever<=0.90): sim=0.4618  theory x^a=0.4624
     P(ever<=0.75): sim=0.1240  theory x^a=0.1217
     P(ever<=0.50): sim=0.0065  theory x^a=0.0063
c=1.00 f=c*f*=2.222  exponent a=2g/Var=2.0800
     P(ever<=0.90): sim=0.8045  theory x^a=0.8032
     P(ever<=0.75): sim=0.5467  theory x^a=0.5497
     P(ever<=0.50): sim=0.2355  theory x^a=0.2365
r=0, m=0.10, s=0.20 -> f*=m/s^2=2.500
full Kelly: P(ever<=1/2)=x=0.500 ; half Kelly: P(ever<=1/2)=x^3=0.125
P(double before halving): full Kelly 2/3=0.6667 ; half Kelly 8/9=0.8889
```

The simulation reproduces $x^{a}$ to the third decimal at every level and both fractions — the drawdown law is not just an asymptotic abstraction. Note the *exponent* difference: $\tfrac12$-Kelly's $a=7.32$ versus full Kelly's $a=2.08$. That one number is why half Kelly's chance of ever halving is $0.0065$ instead of $0.2355$ at these parameters.

```python
import math, random
# (D) 30 years of daily leveraged-Kelly equity and its realised max drawdown
m, s, r = 0.11, 0.15, 0.06
fk = (m-r)/s**2
dt = 1.0/252; ndays = 30*252
md, sd, rd = m*dt, s*math.sqrt(dt), r*dt
def equity(c, paths=20000, seed=12):
    random.seed(seed); f = c*fk; mdd = []; final = []
    for _ in range(paths):
        W = 1.0; peak = 1.0; worst = 0.0
        for _ in range(ndays):
            X = md + (sd if random.random() < 0.5 else -sd)
            W *= 1.0 + (1.0-f)*rd + f*X
            peak = max(peak, W); worst = max(worst, 1.0 - W/peak)
        mdd.append(worst); final.append(W)
    mdd.sort(); final.sort()
    return mdd[len(mdd)//2], mdd[int(0.95*len(mdd))], final[len(final)//2]
for c in (0.5, 1.0):
    med, w95, fmed = equity(c)
    print("c=%.2f f=%.3f: median max-drawdown=%.1f%%  95th-pct=%.1f%%  median 30y wealth=%.2fx"
          % (c, c*fk, med*100, w95*100, fmed))
```
```
c=0.50 f=1.111: median max-drawdown=38.1%  95th-pct=55.2%  median 30y wealth=21.11x
c=1.00 f=2.222: median max-drawdown=70.9%  95th-pct=89.1%  median 30y wealth=32.03x
```

Half Kelly gives up about a third of the terminal wealth ($21.1\times$ vs $32.0\times$) to cut the median drawdown from $71\%$ to $38\%$ and the 95th-percentile drawdown from $89\%$ to $55\%$. **The $+52\%$ more wealth at full Kelly comes with a drawdown most real investors cannot hold through** — that is the entire case for fractional Kelly, in two lines.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating $f_c$ as a soft threshold.** Below $f_c$ you grow a.s.; above it you decay a.s. The penalty is not gradual — crossing $f_c$ flips the sign of the growth rate.
2. **Ignoring the drawdown law when choosing $c$.** Even full Kelly ($c=1$) has $\mathbb{P}(\text{ever halve})=\tfrac12$ at zero rates. If a $50\%$ drawdown would force liquidation, full Kelly is *not* optimal — the objective must include survival.
3. **Convexity of ruin to leverage.** Required leverage scales like $1/(1-T)$ under taxes and like $(m-r)/s^2$ under return estimates; small errors in $m$ or $s$ move you across $f_c$ because the growth function is flat at the top and steep at the edges.
4. **Fat tails invalidate the drawn-down law's Gaussian core.** Real returns jump (Tsay; Merton in [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Extensions]]); a single $-30\%$ gap can leap over a monitored barrier. The bridge simulation above assumes continuous paths — reality is worse, so treat the $x^a$ numbers as *optimistic*.
5. **Behavioural ruin as true ruin.** The mathematically "temporary" drawdowns of full Kelly are psychologically permanent. Sizing must respect the human, not just the diffusion.

---

### 5. Canonical Literature & Study References

- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006) — §3.2 (probability of ever being reduced to a fraction $x$, eq. 3.2), §7.1 (eq. 7.3, $t_k$), §7.3 (fractional Kelly), §7.4 (the remarkable drawdown/doubling formulas 7.10–7.13). *Corpus-verified.*
- **Feller, William**: *An Introduction to Probability Theory and Its Applications*, Vol. I — the gambler's ruin formula. *(Standard reference for §2.1.)*
- **Cox, D. R. & Miller, H. D.**: *The Theory of Stochastic Processes* — the two-absorbing-barrier Wiener solution (Example 5.5) behind Thorp eq. 7.12. *(Standard reference.)*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (2011) — the "good/bad properties" survey, including the drawdown critique of full Kelly.

---

### 6. Connected Graph Bridges

- Back: [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]]
- Forward: [[foundations/ergodicity-and-statistical-mechanics/06-advanced-extensions|06 · Advanced Extensions]] · [[foundations/ergodicity-and-statistical-mechanics/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|Brownian Motion & First Passage]] (barrier hitting) · [[foundations/probability-and-measure-theory|Probability & Measure Theory]]
- Applications: [[pillars/04-quantitative-risk/index|Quantitative Risk]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|Extreme Value Theory & Fat Tails]] · [[pillars/05-portfolio-optimization/index|Portfolio Optimization]]

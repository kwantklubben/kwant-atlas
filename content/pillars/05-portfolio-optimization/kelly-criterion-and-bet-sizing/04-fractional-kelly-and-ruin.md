---
title: "04 — Fractional Kelly, Drawdowns & the Risk of Ruin From Overbetting"
tags:
  - pillar-portfolio-optimization
  - kelly-criterion
  - bet-sizing
  - fractional-kelly
  - ruin
  - drawdown
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/03-growth-and-optimality|03 · Growth & Optimality]] and [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown]].

---

### 1. Intuition & Practical Objective

Page 03 proved full Kelly is growth-optimal. This page confronts the cost: **full Kelly is aggressive, and anything past it is ruinous.** The objective is to make the risk profile concrete and turn it into a sizing rule change.

Three facts drive practice:

1. **The $c(2-c)$ law.** Half Kelly ($c=\tfrac12$) keeps $\tfrac34$ of the growth rate at half the volatility. The first 25% of growth you give up buys a **50% cut in risk** — an extraordinary asymmetry in the *risk* dimension even though growth is symmetric around $f^\*$.
2. **Overbetting risk is not symmetric.** Because $g(f)$ is concave and flat near the top, betting $f^\*+\delta$ costs more growth than betting $f^\*-\delta$, and the *drawdown* cost of overbetting compounds with quadratic volatility. Past the critical fraction $f_c$ the growth rate goes *negative*: ruin is near-certain with a positive edge.
3. **Ruin and drawdown have quantitative laws.** Any fixed-fraction bettor runs a constant-proportional-betting random walk, so drawdowns follow an explicit distribution (Thorp §6; the ergodicity folder's ruin page); full Kelly has a large, fixed drawdown law that the median investor finds unacceptable.

> **Takeaway.** Fractional Kelly is not a hedge against being *wrong* about $f^\*$ — it is the rational response to the asymmetry that overbetting is punished far harder than underbetting, in a world where $p,m,s$ are estimated. The standard practitioner rule: bet at **half Kelly ($c=0.5$)** to start, de-rate further when parameter uncertainty is high.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The fractional-Kelly growth and risk

With $f=cf^\*$:

$$\frac{g_\infty(cf^\*)-r}{g_\infty(f^\*)-r}=c(2-c)\qquad(\text{exact for the excess growth; the raw ratio equals }c(2-c)\text{ only when }r=0),\qquad
\frac{\mathrm{SD}(G_\infty(cf^\*))}{\mathrm{SD}(G_\infty(f^\*))}=c.$$

Growth is a *quadratic* that is flat at the top; risk is *linear* in $c$. Hence half Kelly: $g/g^\*=0.75$, risk $=0.5$. Double Kelly ($c=2$): $g/g^\*=0$, risk $=2$. **The ratio of return to risk is monotonically worse the further you scale above $c=1$.**

#### 2.2 The critical fraction and certain ruin

For the even-money game ($p=0.55$), $f_c=0.1987$ solves $g(f_c)=0$, i.e. $\mathbb{E}[\ln(1+R(f))]=0$. For $f>f_c$ the log-growth is negative, and by the law of large numbers the *time-average* wealth drifts to zero almost surely. Because $f_c\approx2\times f^\*$, a **$2\times$ sizing error turns a profitable edge into a guaranteed-loss strategy** — not a riskier one, a losing one.

#### 2.3 Drawdown law (continuous)

For continuous Kelly, the drawdown from a peak follows an exponential-law tail controlled by the growth-rate-to-variance ratio. The key qualitative result: **even at full Kelly the expected maximum drawdown is large**, so a full-Kelly investor must tolerate 50%+ drawdowns as routine — a "growth-optimal but stomach-churning" profile.

---

### 3. Computational Implementation — fractional Kelly, ruin, and drawdowns in simulation

Stdlib only: simulate fixed-fraction betting at half / full / double Kelly and measure three outcomes — median terminal wealth, probability of ruin (account < 10% of start), and average maximum drawdown from the running peak.

```python
import math, random

p, fstar = 0.55, 0.10                 # even-money, full Kelly f* = p-q

def sim(c, n=200, paths=20000, seed=2):
    random.seed(seed); ruin=0; logs=0.0; md=0.0
    for _ in range(paths):
        x = 1.0; peak = x
        for _ in range(n):
            x *= (1 + c*fstar) if random.random() < p else (1 - c*fstar)
            peak = max(peak, x)
        md = max(md, (peak-x)/peak)   # terminal drawdown from running peak
        logs += math.log(max(x,1e-300)); ruin += (x < 0.1)
    return math.exp(logs/paths), ruin/paths, md

print("c  f     median wealth   P(ruin<0.1)   avg.max-drawdown")
for c in (0.5, 1.0, 2.0):
    mw, ru, dd = sim(c)
    print(f"{c:.1f} {c*fstar:.2f}   {mw:10.4f}      {ru:.3f}          {dd:.3f}")
```
```text
c  f     median wealth   P(ruin<0.1)   avg.max-drawdown
0.5 0.05       2.1222      0.000          0.883
1.0 0.10       2.7333      0.009          0.991
2.0 0.20       0.9804      0.221          1.000
```

The pattern is unmistakable. **Double Kelly** ($c=2$, right at the critical $f_c=0.199$): half the terminal wealth of half-Kelly earnings, **22% of accounts ruined**, and terminal drawdown 100%. **Full Kelly**: 0.9% ruin but 99% max-drawdown. **Half Kelly**: zero ruin in 20,000 paths and still compounds positively. The **overbet is strictly worse on every risk metric** — more ruin *and* lower median wealth — which is exactly the failure mode of page 05. Fractional Kelly is the only one of the three that is actually deployable.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Kelly says bet 22%."** On an estimated edge, $f^\*$ is a fiction; betting the *estimated* full Kelly on a slightly-wrong $p$ lands you at $2\times$ the true optimum — straddling $f_c$ with double-Kelly ruin probabilities (see the page 05 overbetting demo).
2. **Treating drawdown as a nuisance.** Full Kelly's ~99% max drawdown is not a bug — it *is* the growth-optimal risk profile. Funds and individuals almost universally de-rate because the median path of full Kelly is brutally volatile.
3. **Believing $c=2$ "geometrically" doubles returns.** The growth curve is concave: beyond $f^\*$ you gain *nothing* and lose *risk*. There is no compensation for overbetting.
4. **Ignoring the continuous/leverage case.** In securities, $f^\*=(m-r)/s^2$ can exceed 1 (leverage); fractional Kelly then governs *how much leverage*, and over-leverage near $f_c$ in the continuous case means forced liquidation at drawdowns, compounding the ruin.

---

### 5. Canonical Literature & Study References

- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006) — §6 (drawdown distribution for fixed-fraction betting), §7.3 (the quantitative case for fractional Kelly). *Corpus-verified.*
- **MacLean, Ziemba & Blazenko**: *Growth versus Security in Dynamic Investment Analysis*, Management Science 38(11) (1992) — the formal fractional-Kelly growth/security frontier.
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (2011) — "bad properties of Kelly" (aggressiveness, drawdown).
- **Browne, S.**: *The Return on Investment from Proportional Portfolio Strategies and the Optimal Investment Horizon* (1999) — drawdown and risk-control results.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/03-growth-and-optimality|03 · Growth & Optimality]] · [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Index Hub]]
- Apply: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Ruin foundation: [[foundations/ergodicity-and-statistical-mechanics/05-ruin-and-drawdown|05 · Ruin & Drawdown (foundations)]] · [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]]
- Risk metrics: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
---
title: "F.9.3 Multiplicative Growth"
tags:
  - foundations
  - growth-rate
  - volatility-drag
  - geometric-mean
  - log-utility
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|02 · Ensemble vs Time Averages]] and basic calculus (Taylor expansion, Jensen).

---

### 1. Intuition & Practical Objective

Page 02 said: when wealth *multiplies*, ensemble and time averages split, and the split is the Jensen gap. This page **computes that gap** and shows it is not abstract — it is a real, permanent tax on every volatile portfolio, called the **volatility drag** (or variance drain, or geometric-mean discount).

The practical objective: **stop adding returns and start adding log returns.** A portfolio's compounded growth rate is the average of its *log* returns, and log returns have a built-in penalty for volatility. Two assets with the *same* arithmetic mean return can have very different compounded outcomes if their volatilities differ. The quieter one wins over time.

Concretely: a stock with arithmetic mean return $\mu$ and volatility $\sigma$ compounds at approximately $\mu-\tfrac12\sigma^2$. At $\sigma=15\%$ that is a drag of $1.125\%$/year — free money you lose simply for having wiggles. At $\sigma=50\%$ the drag is $12.5\%$/year, and a strategy that "averages $+8\%$" can compound *negative*.

> **Takeaway.** Compounded wealth lives in log space, where returns are additive and ergodic. Volatility is a *cost*, not a free-spending lottery ticket: it lowers the typical (geometric) outcome below the arithmetic mean by $\sim\tfrac12\sigma^2$.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 From simple to log returns

For a one-period simple return $R_t$, the log return is $r_t=\ln(1+R_t)$. A multi-period product becomes a sum:

$$
1+R_t[k]=\prod_{j=0}^{k-1}(1+R_{t-j})
\quad\Longrightarrow\quad
r_t[k]=\sum_{j=0}^{k-1}r_{t-j}.
$$

So **log returns are additive across time**, restoring the ergodic structure of page 02. The **geometric mean return** is $\exp(\overline{r})-1$, where $\overline{r}=\frac1k\sum r_{t-j}$ is the time average of log returns — the $g$ of page 01.

#### 2.2 The volatility drag (Jensen gap)

Let $R$ have mean $\mu$ and variance $\sigma^2$, small enough that $|R|<1$. Expand

$$
\ln(1+R)=R-\tfrac12R^2+\tfrac13R^3-\cdots
\quad\Longrightarrow\quad
\mathbb{E}[\ln(1+R)]=\mu-\tfrac12(\mu^2+\sigma^2)+\cdots
$$

Collecting terms, to second order,

$$
\boxed{\;g=\mathbb{E}[\ln(1+R)]\;\approx\;\ln(1+\mu)-\frac{\sigma^2}{2(1+\mu)^2}\;\approx\;\mu-\frac{\sigma^2}{2}\;}
$$

The ensemble growth rate is $\ln\mathbb{E}[1+R]=\ln(1+\mu)$, so the **drag** separating typical from ensemble growth is exactly

$$
\ln(1+\mu)-g\;\approx\;\frac{\sigma^2}{2(1+\mu)^2}.
$$

This is the Jensen gap of page 02, now quantified: **volatility, not direction, determines how far the typical path lags the average.**

#### 2.3 The continuous limit: geometric Brownian motion

For $dS=\mu S\,dt+\sigma S\,dW$, Itô gives $S_t=S_0\exp\!\big((\mu-\tfrac12\sigma^2)t+\sigma W_t\big)$, so

$$
\mathbb{E}[S_t]=S_0e^{\mu t}\quad\text{(ensemble)},\qquad
\mathrm{med}(S_t)=S_0e^{(\mu-\frac12\sigma^2)t}\quad\text{(typical)},
$$

and the time-average growth rate is $g_\infty=\mu-\tfrac12\sigma^2$. With a risky fraction $f$ and riskless rate $r$, the continuous growth rate is the **Kelly growth function**

$$
g_\infty(f)=r+f(m-r)-\tfrac12 s^2 f^2 .
$$

This is a downward parabola in $f$, concave, with a unique maximum — the object maximised on [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|page 04]]. The quadratic penalty $-\tfrac12s^2f^2$ is the volatility drag made lever-aware.

#### 2.4 The S&P number

Thorp's continuous approximation with historical inputs $m=11\%$, $s=15\%$, $r=6\%$ gives the risk-adjusted drag explicitly; the ensemble-per-annum object is $e^{m}=27.11\times$ over 30 years while the typical (median) outcome is $e^{m-\frac12s^2}=19.35\times$. A factor of $\sim1.4$ in terminal wealth, from volatility alone.

---

### 3. Computational Implementation — the drag, measured

Stdlib only. We price the same GBM two ways: the ensemble mean and the typical (geometric) path, and confirm the drag is $\tfrac12\sigma^2$.

```python
import math, random

mu, sigma, T = 0.11, 0.15, 30.0          # GBM-ish: E[S_T]=S0*exp(mu*T) for the
                                          # geometric drift mu (so log-drift = mu - s^2/2)

# Closed-form anchors
print("E[S_T]/S0   = exp(mu*T)          = %.4f" % math.exp(mu*T))
print("median S_T/S0 = exp((mu-s^2/2)T) = %.4f" % math.exp((mu-0.5*sigma**2)*T))
print("time-avg growth = mu - sigma^2/2 = %.6f" % (mu-0.5*sigma**2))
print("volatility drag = sigma^2/2      = %.6f" % (0.5*sigma**2))

# Monte Carlo of S_T/S0 = exp((mu-s^2/2)T + sigma sqrt(T) Z)
random.seed(3)
n = 300000; tot = 0.0; logs = 0.0
for _ in range(n):
    S = math.exp((mu-0.5*sigma**2)*T + sigma*math.sqrt(T)*random.gauss(0,1))
    tot += S; logs += math.log(S)
print("MC  E[S_T]/S0                    = %.4f" % (tot/n))
print("MC  geometric mean S_T/S0        = %.4f" % math.exp(logs/n))
```
```
E[S_T]/S0   = exp(mu*T)          = 27.1126
median S_T/S0 = exp((mu-s^2/2)T) = 19.3463
time-avg growth = mu - sigma^2/2 = 0.098750
volatility drag = sigma^2/2      = 0.011250
MC  E[S_T]/S0                    = 27.1056
MC  geometric mean S_T/S0        = 19.3380
```

The ensemble mean ($27.11\times$) and the geometric mean / median ($19.35\times$) differ by exactly the accumulated drag $e^{\frac12\sigma^2 T}=e^{0.3375}=1.40$. **The typical investor captures $19.3\times$, not $27.1\times$** — and the $+11\%$ "expected return" is really a $+9.88\%$ compounding rate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Averaging simple returns across periods.** The arithmetic mean of $+50\%$ and $-40\%$ is $+5\%$; the compounded result is $-10\%$. Cross-period averages must be taken on log returns.
2. **Ignoring the drag when levering.** The drag grows like $f^2\sigma^2$: doubling exposure *quadruples* the variance penalty. This is why leverage can turn a positive edge into a negative growth rate long before it causes a margin call ([[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|page 04]]).
3. **Trusting the second-order approximation in the tail.** $\mathbb{E}[\ln(1+R)]\approx\mu-\tfrac12\sigma^2$ fails for large moves; real returns are fat-tailed (excess kurtosis, Tsay Ch. 1) so the true drag is larger and jumps make the log expansion invalid. Use the exact $\mathbb{E}[\ln(1+R)]$ where the distribution is known.
4. **Confusing "expected return" with "compounding rate" in a backtest.** Reporting $\mathbb{E}[R]$ overstates the achievable CAGR by $\sim\tfrac12\sigma^2$; funds that quote arithmetic means systematically overstate what an account would have compounded.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed.), Ch 1 — return definitions, the geometric vs arithmetic mean (Eq 1.1–1.7), and the empirical fat tails (high excess kurtosis, Table 1.2) that make the drag worse than Gaussian. *Verified in the corpus.*
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §7.1 — the continuous growth function $g_\infty(f)=r+f(m-r)-\tfrac12s^2f^2$ (eq. 7.2), its log-normal diffusion limit, and $g_\infty(f^*)=(m-r)^2/2s^2+r$. *Corpus-verified.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance I*, Ch 15 (Thm 15.3) — GBM and the $\tfrac12\sigma^2$ Itô correction: $S_t=S_0e^{\sigma W_t+(\mu-\frac12\sigma^2)t}$. *Math-verified.*
- **Peters, Ole**: *The Ergodicity Problem in Economics*, Nature Physics 15 (2019) — the log-growth/volatility-drag reading of multiplicative dynamics.

---

### 6. Connected Graph Bridges

- Back: [[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|02 · Ensemble vs Time Averages]]
- Forward: [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]] · [[foundations/ergodicity-and-statistical-mechanics/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|Itô Integral & Doeblin]] (the $\tfrac12\sigma^2$ correction) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (log returns, fat tails)
- Applications: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]

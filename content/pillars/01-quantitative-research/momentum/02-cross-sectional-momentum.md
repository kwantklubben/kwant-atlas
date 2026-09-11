---
title: "02 — Cross-Sectional Momentum: Ranking Winners & Shorting Losers"
tags:
  - pillar-quant-research
  - momentum
  - cross-sectional
  - wml
  - long-short
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (serial correlation) and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (inner products, rank).

---

### 1. Intuition & Practical Objective

Cross-sectional momentum (XSMOM) is the **Jegadeesh–Titman strategy**: every month, rank your universe by trailing 12-month return, **buy the winners and short the losers**, dollar-neutral, hold ~1 month, repeat. It is a *relative* bet — an asset "wins" because it beat its peers over the ranking window, regardless of the absolute direction of its return.

Two implementation facts shape everything:

1. **Skip the most recent month (the $12\text{-}1$ convention).** Rank on months $t-12\ldots t-2$, *not* $t-1$. The last month reverses (Jegadeesh 1990; Lehmann 1990) and, if included, drags the signal toward a trade that loses. This one convention is the single most important detail of the strategy.
2. **The portfolio is dollar-neutral by construction.** Rank weights $w_i\propto(\text{rank}_i-\frac{N+1}{2})$ sum to zero, so the long and short legs offset exactly — no net market exposure. The loser *short* leg is where both the profit and the crash risk live.

The verified US facts: winners decile (a *decile* = one tenth of the cross-section, i.e. a 10% rank bucket by past return) earns $\sim15\%$/yr, losers $\sim-2.5\%$/yr, WML (winners-minus-losers) has a Sharpe $\approx0.60$–$0.71$ and a *negative* CAPM beta $(-0.58)$ with annual alpha $\approx22\%$ (Daniel & Moskowitz 2016, 1927–2013). Momentum profits are essentially a **non-January** phenomenon (JT 2001).

---

### 2. Mathematical Ground Truth & Derivations

**Signal.** For asset $i$ with monthly returns $r_{i,t}$, the $12\text{-}1$ cumulative signal is
$$
R_i^{(12\text{-}1)}=\prod_{k=2}^{12}\big(1+r_{i,t-k}\big)-1.
$$

**Rank-to-weight map.** Rank assets by $R_i$ (1-indexed, best = $N$). Set
$$
w_i=\frac{\text{rank}_i-\frac{N+1}{2}}{\sum_{j=1}^N\big|\text{rank}_j-\frac{N+1}{2}\big|}.
$$
Because ranks run $1\ldots N$, the raw weights $(\text{rank}_i-\frac{N+1}{2})$ are symmetric about zero: the portfolio is **dollar-neutral** ($\sum_i w_i=0$) and **100% gross** ($\sum_i|w_i|=1$). The next-period WML return is $r^{\text{WML}}_{t+1}=\sum_i w_i\, r_{i,t+1}$.

**Why it earns (decomposition).** Moskowitz–Ooi–Pedersen (2012) decompose the expected cross-sectional momentum profit as
$$
\mathbb{E}\big[r^{\text{XS}}_{t,t+1}\big]=\frac{\operatorname{tr}(\Omega)}{N}-\frac{\mathbf{1}'\Omega\mathbf{1}}{N^2}+12\sigma_m^2, \qquad \Omega=\mathbb{E}\big[(R_{t-12,t}-12\mu)(R_{t,t+1}-\mu)'\big],
$$
where $\sigma_m^2$ is the cross-sectional variance of mean returns. The three channels:
1. **Own autocovariance** $\operatorname{tr}(\Omega)$ — time-series predictability (this is the TSMOM channel; *not* required for XSMOM).
2. **Cross-serial covariances** $-\mathbf{1}'\Omega\mathbf{1}$ — temporal lead-lag across assets (a past move in one asset predicts another's next return). *Negative* cross-serial covariances alone can generate XSMOM profits with *no* own autocorrelation (Lewellen 2002).
3. **Cross-sectional dispersion of unconditional means** $12\sigma_m^2$ — high-mean assets are also high-past-return assets on average.

**Why skip the last month.** If the one-month autocorrelation $\rho_1<0$ (reversal), then including $r_{i,t-1}$ in the signal loads the portfolio onto an asset whose next-month return is *negatively* predicted by its most recent move. Dropping month 1 removes this contamination, leaving the positive 2–12 month continuation.

---

### 3. Computational Implementation — the ranking engine

Standard library only. Builds the skip-month signal, verifies **dollar-neutrality and 100% gross leverage exactly**, and shows that the skip-month convention matters: skipping the last month preserves the premium, while including it destroys it (short-term reversal).

```python
import random
random.seed(7)

# XSMOM on synthetic monthly returns. Two layers:
#  (a) weak intermediate persistence -> 12-month momentum signal;
#  (b) strong one-month reversal of the latest innovation -> why we SKIP it.
N, T = 120, 240
mu  = [random.gauss(0.0, 0.018) for _ in range(N)]   # persistent rank drift
g   = [[0.0]*T for _ in range(N)]                    # momentum-generating returns
eps = [[0.0]*T for _ in range(N)]
phi = 0.10                                           # weak persistence
for i in range(N):
    for t in range(1, T):
        e = random.gauss(0.0, 0.07); eps[i][t] = e
        g[i][t] = mu[i] + phi*(g[i][t-1]-mu[i]) + e
kappa = 0.90                                         # one-month reversal strength
r = [[g[i][t] - kappa*(eps[i][t-1] if t >= 1 else 0.0) for t in range(T)] for i in range(N)]

def wml_series(skip=True):
    monthly = []
    for t in range(14, T-1):
        past = [1.0]*N
        for m in range(12):
            if skip and m == 0: continue             # skip the most recent month
            for i in range(N): past[i] *= (1.0 + r[i][t-1-m])
        order = sorted(range(N), key=lambda j: past[j])
        w = [0.0]*N
        for pos, i in enumerate(order):
            w[i] = (pos+1) - (N+1)/2.0               # 1-indexed ranks
        tot = sum(abs(x) for x in w); w = [x/tot for x in w]
        monthly.append(sum(w[i]*r[i][t] for i in range(N)))
    return monthly

def stats(s):
    m = sum(s)/len(s); sd = (sum((x-m)**2 for x in s)/len(s))**0.5
    return m, sd, m/sd, min(s)

for name, s in (("12m SKIP last month ", wml_series(True)), ("12m INCLUDE last month", wml_series(False))):
    mn, sd, sr, lo = stats(s)
    print(f"{name}: mean/mo {mn*100:+.3f}%  vol/mo {sd*100:.3f}%  SR {sr:+.3f}  worst {lo*100:+.2f}%")

# dollar-neutrality & 100% gross leverage at one arbitrary date
past = [1.0]*N
for m in range(1, 12):
    for i in range(N): past[i] *= (1.0 + r[i][200-m])
order = sorted(range(N), key=lambda j: past[j])
w = [0.0]*N
for pos, i in enumerate(order):
    w[i] = (pos+1) - (N+1)/2.0
tot = sum(abs(x) for x in w); w = [x/tot for x in w]
print(f"dollar neutrality  sum(w)   = {sum(w):+.3e}")
print(f"100% gross leverage sum|w| = {sum(abs(x) for x in w):.4f}")
```
```
12m SKIP last month : mean/mo +1.722%  vol/mo 0.983%  SR +1.751  worst -0.99%
12m INCLUDE last month: mean/mo -0.063%  vol/mo 0.921%  SR -0.068  worst -2.81%
dollar neutrality  sum(w)   = +0.000e+00
100% gross leverage sum|w| = 1.0000
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The loser short leg is where crashes live.** WML's profit and its crash risk both concentrate in the *short* losers. In a panic rebound the losers "crash up" (they are levered, high-beta, option-like), so the short leg loses violently — this is the entire momentum-crash mechanism (see [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]]).
2. **Skip-month violations destroy the edge.** Using month $t-1$ in the signal loads one-month reversal; the verified example above shows SR dropping from $+1.75$ to $-0.07$. This is a *first-principles* failure: wrong autocorrelation band.
3. **Beta exposure contamination.** Because winners are stocks that did well in the past, WML loads positively on whatever factor did well over the formation window — after market declines it is long low-beta, short high-beta (loser beta can exceed 3), giving time-varying, crash-prone exposure (Kothari–Shanken 1992; Grundy–Martin 2001).
4. **Multiple testing & crowding.** With 200+ papers and endless parameter sweeps over lookbacks/holdings, the published momentum Sharpe is inflated by selection; capacity and crowding compress realized returns (see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).

---

### 5. Canonical Literature & Study References

- **Jegadeesh & Titman (1993)**, *Returns to Buying Winners and Selling Losers*, J. Finance 48(1) — the original 1965–1989 US result; and **Jegadeesh & Titman (2001)**, *Profitability of Momentum Strategies*, J. Finance 56(2) — persistence in the 1990s, non-January effect, behavioral-vs-rational tests. *Verified corpus refs/13.*
- **Jegadeesh (1990)** and **Lehmann (1990)** — one-month reversal motivating the skip.
- **Moskowitz & Grinblatt (1999)** — industry-level momentum; **Rouwenhorst (1998, 1999)** — international/emerging.
- **Kothari & Shanken (1992)** and **Grundy & Martin (2001)** — time-varying betas of return-sorted portfolios.
- **Moskowitz, Ooi & Pedersen (2012)**, *Time Series Momentum* — §5 XSMOM/TSMOM decomposition. *Verified corpus refs/14.*

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]]
- Continue: [[pillars/01-quantitative-research/momentum/03-time-series-momentum|03 · Time-Series Momentum]] · [[pillars/01-quantitative-research/momentum/04-value-momentum-interaction|04 · Value–Momentum]]
- Failure analysis: [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/momentum/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling factor view: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (UMD / momentum factor)

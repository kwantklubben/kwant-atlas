---
title: "06 — Advanced Extensions: Johansen, Optimal Stopping & Dynamic Hedging"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - johansen
  - vecm
  - optimal-stopping
  - kalman-filter
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/02-cointegration-and-the-spread|02 · Cointegration & the Spread]] and [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/04-trading-rules-and-backtest|04 · Trading Rules & Backtest]].

---

### 1. Intuition & Practical Objective

Three extensions take StatArb beyond the two-asset t-test:

1. **Johansen's multivariate test** — instead of a *pair*, allow a *basket* and ask "how many* independent equilibrium relationships exist?" (the cointegrating rank). This is the correct tool when several assets share the same factors and you do not want to pre-pick a pair.
2. **Optimal stopping / stochastic control of the OU spread** — instead of fixed $2\sigma$ thresholds, solve for the thresholds that maximise expected return per unit time net of costs.
3. **Dynamic hedging (Kalman filter)** — replace the static OLS $\beta$ with a time-varying $\beta_t$ estimated recursively, so the hedge adapts when the relationship drifts (the bridge to [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filtering]]).

All three keep the OU spread at the centre; they differ in how many assets and how much structure they assume.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Johansen procedure (Tsay §8.6.2–8.6.3; Johansen 1988/1991)

Start from a VAR($p$) in levels and rewrite it in **error-correction** form for a $k$-dimensional $I(1)$ vector $x_t$:

$$\Delta x_t=\Pi x_{t-1}+\sum_{i=1}^{p-1}\Gamma_i\Delta x_{t-i}+a_t,\qquad \Pi=\sum_{i=1}^{p}\Phi_i-I=-\Phi(1).$$

The **rank of $\Pi$ is the cointegrating rank** $m$: $\Pi=\alpha\beta'$, with $\beta$ ($k\times m$) the cointegrating vectors and $\alpha$ the adjustment speeds.

**Estimation (the reduced-rank regression).** Run two auxiliary regressions and collect residuals:

$$R_{0t}=\Delta x_t-\text{proj on }(\Delta x_{t-1},\dots),\qquad R_{1t}=x_{t-1}-\text{proj on }(\Delta x_{t-1},\dots).$$

Form the moment matrices $S_{ij}=\tfrac1T\sum_t R_{it}R_{jt}'$, and solve the **generalised eigenvalue problem**

$$\big|\lambda S_{11}-S_{10}S_{00}^{-1}S_{01}\big|=0\;\Longrightarrow\;\hat\lambda_1\ge\dots\ge\hat\lambda_k.$$

The cointegrating vectors are the eigenvectors, normalised so $e'S_{11}e=I$.

**Tests (H0: rank $=m$).** Two standard statistics, with nonstandard (Brownian-motion) critical values:

$$LR_{\text{tr}}(m)=-(T-p)\sum_{i=m+1}^{k}\ln(1-\hat\lambda_i)\quad\text{(rank}=m\text{ vs }>m),$$

$$LR_{\max}(m)=-(T-p)\ln(1-\hat\lambda_{m+1})\quad\text{(rank}=m\text{ vs }m+1).$$

For $k=2$ with a restricted constant, the 95% critical values are $\approx15.41$ (rank $\le0$) and $\approx3.76$ (rank $\le1$): reject "no cointegration" if the first exceeds $15.41$, and fail to reject rank 1 if the second is below $3.76$.

#### 2.2 Multivariate StatArb (Avellaneda–Lee "generalized pairs trading")

Trade a stock against a *weighted portfolio* (basket) rather than a single peer. With factors $F_j$ and residuals $\tilde R_i=R_i-\sum_j\beta_{ij}F_j$, the "generalized" spread is the idiosyncratic residual $\tilde R_i$, and the same OU/z-score machinery applies per stock. Market-neutrality $\sum_i\beta_{ij}Q_i=0$ holds at the book level, so the net factor exposure cancels.

#### 2.3 Optimal stopping / thresholds (Elliott, van der Hoek & Malcolm 2005; Bertram 2010)

Model the spread as an OU process and the trade as a **first-passage problem**: enter at level $a$, exit at level $m$ ($a<m$ for a long-spread trade). The cycle time $T=T_1+T_2$ (entry→exit + exit→next entry) is random; the return per cycle is deterministic, $r(a,m,c)=m-a-c$ with cost $c$. By renewal theory the expected return and variance per unit time are

$$\mu(a,m,c)=\frac{r(a,m,c)}{\mathbb{E}[T]},\qquad \sigma^2(a,m,c)=\frac{r^2(a,m,c)\operatorname{Var}(T)}{\mathbb{E}^3[T]},$$

and $\mathbb{E}[T],\operatorname{Var}(T)$ come from the **first-passage-time density of the OU process** (Itô-transformed to a dimensionless system). Maximising a Sharpe-type objective over $(a,m)$ yields the optimal thresholds — recovering the fixed $2\sigma$ rule as a special (suboptimal-in-general) case.

#### 2.4 Dynamic hedge ratio (Kalman filter)

Let $\beta_t$ follow a random walk $\beta_t=\beta_{t-1}+w_t$ with observation $y_t=\alpha+\beta_t x_t+v_t$. The Kalman filter gives the one-step-ahead estimate $\hat\beta_{t|t-1}$; use it as the hedge ratio so the spread is $z_t=y_t-\hat\beta_{t|t-1}x_t$. This turns the static cointegration regression into an adaptive one — essential when $\beta$ drifts slowly (see the sibling topic for the full state-space derivation).

---

### 3. Computational Implementation — the Johansen trace test

Stdlib only. We simulate a genuine cointegrated bivariate system (random walk $x_1$, and $x_2=0.9\,x_1+$ stationary) so the true rank is **1**, then run the full Johansen reduced-rank regression with a 2×2 analytic generalised-eigenvalue solve.

```python
import math, random

def inv2(A):
    d=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    return [[A[1][1]/d,-A[0][1]/d],[-A[1][0]/d,A[0][0]/d]]
def mul2(A,B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]
def ols_cols(y, cols):                        # cols = regressor COLUMNS
    T=len(y); K=len(cols)
    XtX=[[sum(cols[i][t]*cols[j][t] for t in range(T)) for j in range(K)] for i in range(K)]
    Xty=[sum(cols[i][t]*y[t] for t in range(T)) for i in range(K)]
    A=[row[:]+[Xty[i]] for i,row in enumerate(XtX)]
    for c in range(K):
        p=max(range(c,K),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]
        for r in range(K):
            if r!=c:
                f=A[r][c]/A[c][c]
                for k in range(c,K+1): A[r][k]-=f*A[c][k]
    return [A[i][K]/A[i][i] for i in range(K)]

T=1000; rng=random.Random(2024)
x1=[0.0]*T
for t in range(1,T): x1[t]=x1[t-1]+rng.gauss(0,1)
s=[0.0]*T
for t in range(1,T): s[t]=0.8*s[t-1]+rng.gauss(0,0.6)
x2=[0.9*x1[t]+s[t] for t in range(T)]
P=[[x1[t],x2[t]] for t in range(T)]
dP=[[P[t][i]-P[t-1][i] for i in range(2)] for t in range(1,T)]

rows=list(range(1,len(dP)-1))
rows_reg=[[1.0,dP[r][0],dP[r][1]] for r in rows]          # [1, dP_{t-1}]
cols=[[rows_reg[k][j] for k in range(len(rows))] for j in range(3)]
R0=[[0.0,0.0] for _ in rows]; R1=[[0.0,0.0] for _ in rows]
for i in range(2):
    y0=[dP[r+1][i] for r in rows]; y1=[P[r][i] for r in rows]
    c0=ols_cols(y0,cols); c1=ols_cols(y1,cols)
    for k in range(len(rows)):
        R0[k][i]=y0[k]-sum(c0[j]*rows_reg[k][j] for j in range(3))
        R1[k][i]=y1[k]-sum(c1[j]*rows_reg[k][j] for j in range(3))
m=len(rows)
def S(A,B): return [[sum(A[k][i]*B[k][j] for k in range(m))/m for j in range(2)] for i in range(2)]
S00=S(R0,R0); S01=S(R0,R1); S10=S(R1,R0); S11=S(R1,R1)
M=mul2(inv2(S11), mul2(mul2(S10,inv2(S00)), S01))
tr=M[0][0]+M[1][1]; det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
disc=math.sqrt(max(tr*tr-4*det,0.0)); lam1=(tr+disc)/2; lam2=(tr-disc)/2
print(f"Johansen eigenvalues: lambda1={lam1:.4f}  lambda2={lam2:.4f}")
print(f"trace(r<=0) = {-m*math.log(1-lam1):7.2f}   (95% CV 15.41 -> reject 'no cointegration')")
print(f"trace(r<=1) = {-m*math.log(1-lam2):7.2f}   (95% CV  3.76 -> fail to reject rank 1)")
print("=> exactly one cointegrating vector, as simulated.")
```
```
Johansen eigenvalues: lambda1=0.0983  lambda2=0.0031
trace(r<=0) =  103.14   (95% CV 15.41 -> reject 'no cointegration')
trace(r<=1) =    3.12   (95% CV  3.76 -> fail to reject rank 1)
=> exactly one cointegrating vector, as simulated.
```

The procedure recovers the simulated rank exactly: the first trace statistic ($103.14$) is far above its critical value (reject "no cointegration"), while the second ($3.12$) sits below $3.76$ (a second vector is not supported). The estimated $\hat\lambda_1=0.0983$ is a measure of how strongly the equilibrium is restored by the error-correction term.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Johansen critical values depend on the deterministic spec.** The five cases (no constant, restricted constant, unrestricted constant, restricted/unrestricted trend; Tsay §8.6.1) have *different* tables. Resembling the wrong table invalidates the rank conclusion.
2. **Rank ≠ profitability.** A system can have rank 1 with an unfavourably *slow* adjustment ($\alpha$ small) or a spread whose $\sigma_{\text{eq}}$ is tiny relative to costs — econometrically cointegrated, economically untradeable.
3. **Basket legibility.** Trading a stock against a *basket* multiplies transaction costs and creates netting and borrow complexity; Avellaneda–Lee rely on the net ETF position being small, which need not hold in stress.
4. **Optimal-stopping thresholds assume stationarity.** The Elliott/Bertram solution is only optimal under a *fixed* OU; the moment the parameters drift or the equilibrium breaks, the "optimal" thresholds are worse than a plain stop.
5. **Kalman $\beta$ can chase noise.** If the state-noise variance is set too high, the hedge ratio over-fits recent co-movement and the spread becomes white noise by construction (a filter artefact, not cointegration).
6. **The nested risk.** These extensions add parameters to a problem whose *core* risk (structural break, Ch 5) they do not fix. More machinery is not robustness.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 8 §8.6.2 (Johansen MLE, auxiliary regressions Eq. 8.40–8.41, eigenvalues), §8.6.3 (trace Eq. and max-eigenvalue tests; TB3m/TB6m trace $83.27$ vs 95% CV $19.96$), §8.7 (3-regime threshold cointegration). *Math-verified in the corpus.*
- **Johansen, S.**, "Statistical Analysis of Cointegration Vectors", *Journal of Economic Dynamics and Control* 12(2–3), 1988; and *Econometrica* 59(6), 1991.
- **Avellaneda, M. & Lee, J.-H.**, *Quantitative Finance* 10(7), 2010 — §1 "generalized pairs-trading", §2 PCA/eigenportfolios.
- **Elliott, R. J., van der Hoek, J. & Malcolm, W. P.**, "Pairs Trading", *Quantitative Finance* 5(3), 2005 — OU optimal stopping.
- **Krauss, C.**, *J. Economic Surveys* 31(2), 2017 — §5 stochastic-control approach (Bertram renewal-theory thresholds, Eq. 23–25).
- **Harvey, A. C.**, *Forecasting, Structural Time Series Models and the Kalman Filter* — the state-space machinery for time-varying $\beta$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filtering]] (dynamic hedge ratio) · [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]] (factor choice for residuals)
- Foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] (for the OU first-passage solution)
- Cross-pillar: [[pillars/05-portfolio-optimization/transaction-costs-and-turnover-constraints|Transaction Costs & Turnover]]

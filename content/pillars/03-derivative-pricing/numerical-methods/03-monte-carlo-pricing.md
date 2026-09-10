---
title: "03 — Monte Carlo Pricing: the Estimator, Paths and Path Dependence"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - monte-carlo
  - sample-paths
  - path-dependent
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · The PDE & Feynman–Kac]].

---

### 1. Intuition & Practical Objective

Monte Carlo prices an option by *manufacturing the risk-neutral expectation one path at a time*. Draw a path of $S$ under $\mathbb{Q}$, evaluate the discounted payoff, repeat $n$ times, average. Its justification is the strong law; its error is the central limit theorem:

$$\hat\alpha_n=\frac1n\sum_{i=1}^nf(U_i)\ \xrightarrow{\text{a.s.}}\ \alpha,\qquad \hat\alpha_n-\alpha\ \approx\ \mathcal N\!\Big(0,\frac{\sigma_f^2}{n}\Big).$$

The practical objectives are three: (i) build the estimator and always attach a standard error; (ii) sample paths *exactly* when possible — for GBM the transition is lognormal so the simulation is exact, with **zero** discretisation bias; (iii) recognise the two structural costs — the $O(n^{-1/2})$ rate (four times the work per halving) and the fact that a payoff average is a *path functional* whose sampling requires care (Brownian bridge, monitoring dates).

Three "aha"s:

1. **The error rate is dimension-free.** $O(n^{-1/2})$ holds for an integral over $[0,1]^d$ for every $d$, whereas a product trapezoidal rule degrades as $O(n^{-2/d})$. At $d=10$ MC already wins outright — that is why basket and term-structure exotics are simulation problems.
2. **For GBM there is no discretisation.** $S(t_{i+1})=S(t_i)\exp[(r-\tfrac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z]$ is the *exact* law, not an approximation (Glasserman eq. 3.20–3.22). Bias only enters through the payoff's monitoring convention or through non-GBM dynamics.
3. **The estimator's error is a distribution, not a number.** A 100,000-path run gave $10.4754$ where a 10,000-path run gave $10.4180$ — both consistent with the closed form $10.4506$ within their standard errors. Quoting an MC price without its $\pm$ is meaningless.

---

### 2. Mathematical Ground Truth & Derivations

**The pricing identity** (Glasserman eq. 1.39, the same as Feynman–Kac's integral form):

$$V(0)=\mathbb{E}_\beta\!\left[\frac{V(T)}{\beta(T)}\right]=e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[\text{payoff}(S_T)] .$$

Simulate the **risk-neutral** dynamics — the drift is $r$, never $\mu$; the volatility is unchanged by the change of measure (Glasserman eq. 1.42: only the drift shifts under Girsanov).

**The path sampler.** For GBM the exact grid-point transition is

$$S(t_{i+1})=S(t_i)\exp\!\Big[\big(r-\tfrac12\sigma^2\big)(t_{i+1}-t_i)+\sigma\sqrt{t_{i+1}-t_i}\,Z_{i+1}\Big],$$

and for a Gaussian short rate the exact transition is likewise available (Glasserman eq. 3.43–3.45). *Nothing is discretised at the grid points* for these models.

**The Brownian bridge** (Glasserman eq. 3.7–3.8) — the tool that makes a path's intermediate values cheap and, later, makes barriers correct. Given $W(u)=x$ and $W(t)=y$ with $u<s<t$:

$$\mathbb E[W(s)\mid\cdot]=\frac{(t-s)x+(s-u)y}{t-u},\qquad \mathrm{Var}[W(s)\mid\cdot]=\frac{(s-u)(t-s)}{t-u}.$$

Two properties matter: (i) the conditional variance depends **only on the interval lengths**, not on the endpoint values — so bridge refinement is numerically stable; (ii) the *first* (coarsest) normal drives the largest share of path variance, which is why the bridge ordering is the standard dimension-reduction device for QMC (page 06).

**Path-dependent payoffs** (Glasserman §3.2): for discrete monitoring dates $t_1<\dots<t_m$,

- arithmetic Asian: $\bar S=\frac1m\sum_iS(t_i)$, payoff $(\bar S-K)^+$ — **no closed form**;
- geometric Asian: $\big(\prod_iS(t_i)\big)^{1/m}$, lognormal, with a **closed form** — hence a perfect control variate (page 04);
- barrier (down-and-out): $\mathbf 1\{\tau(b)>T\}(S(T)-K)^+$ with $\tau(b)=\inf\{t_i:S(t_i)<b\}$ — discretely monitored barrier prices depend on the monitoring frequency, and a grid-based simulation *misses* crossings between dates (fixed on page 05/06 by Brownian interpolation).

**The MSE framework** (Glasserman §1.1.3) — the honest budget statement. With bias $b\delta^\beta$, per-path cost $c\delta^{-\eta}$ and $n$ paths,

$$\mathrm{MSE}=\underbrace{\text{bias}^2}_{O(\delta^{2\beta})}+\underbrace{\text{variance}}_{O(1/n)},\qquad
\mathrm{RMSE}=O\!\big(s^{-\beta/(2\beta+\eta)}\big),$$

where $s$ is the work budget; unbiased simulation ($\beta\to\infty$) recovers $s^{-1/2}$, and the discretisation-aware case is page 04's (§2 efficiency rule) $s^{-\beta/(2\beta+1)}$.

---

### 3. Computational Implementation — estimator, error rate, bridge, Asian

Four checks in one script: the $O(n^{-1/2})$ RMSE law, a standard error from one batch, the bridge variance identity, and a path-dependent price against its exact geometric counterpart.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bsm_call(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return S*N(d1) - X*math.exp(-r*T)*N(d2)

S, X, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.20
exact = bsm_call(S, X, T, r, sig)
print(f"BSM call = {exact:.4f}")

# ---------- 1. the estimator and its O(n^-1/2) error ----------
def mc_euro_call(n, rng):
    tot = 0.0
    for _ in range(n):
        Z = rng.gauss(0.0, 1.0)
        ST = S*math.exp((r-0.5*sig**2)*T + sig*math.sqrt(T)*Z)   # exact GBM transition
        tot += max(ST-X, 0.0)
    return math.exp(-r*T)*tot/n

rng = random.Random(2026)
print("\nRMSE of the MC estimator over 200 independent batches:")
for n in (1000, 10000, 100000):
    e = [abs(mc_euro_call(n, rng)-exact) for _ in range(200)]
    rmse = math.sqrt(sum(x*x for x in e)/len(e))
    print(f"  n={n:<7d} RMSE = {rmse:.5f}   RMSE*sqrt(n) = {rmse*math.sqrt(n):.4f}")

# ---------- 2. standard error from the sample, one batch ----------
rng = random.Random(7)
n = 100000; acc = 0.0; acc2 = 0.0
for _ in range(n):
    Z = rng.gauss(0.0, 1.0)
    y = math.exp(-r*T)*max(S*math.exp((r-0.5*sig**2)*T + sig*math.sqrt(T)*Z)-X, 0.0)
    acc += y; acc2 += y*y
mean = acc/n; var = (acc2 - n*mean*mean)/(n-1)
se = math.sqrt(var/n)
print(f"\none batch n=100000: mean = {mean:.4f}, sample s.d. = {math.sqrt(var):.4f},"
      f" standard error = {se:.4f}  ->  95% CI = [{mean-1.96*se:.4f}, {mean+1.96*se:.4f}]")

# ---------- 3. Brownian bridge: variance identity, checked empirically ----------
s, t = 0.5, 1.0
xv = s*(t-s)/t                       # Var[W(s) - (s/t)W(t)]
rng = random.Random(3); N_ = 200000
vals = []
for _ in range(N_):
    Z1 = rng.gauss(0, 1); Z2 = rng.gauss(0, 1)
    Ws = math.sqrt(s)*Z1
    Wt = Ws + math.sqrt(t-s)*Z2
    vals.append(Ws - (s/t)*Wt)       # W(s) - (s/t)W(t) is the bridge at W(t)=0
m = sum(vals)/N_; v = sum((x-m)**2 for x in vals)/(N_-1)
print(f"\nBrownian bridge: X = W(s) - (s/t)W(t) with s={s}, t={t}")
print(f"  E[X]   theory = 0.000000   empirical = {m:+.5f}")
print(f"  Var[X] theory = s(t-s)/t = {xv:.6f}   empirical = {v:.6f}")

# ---------- 4. arithmetic Asian by MC, against the exact geometric Asian ----------
def geo_asian_closed(S, X, T, r, sig, m):
    dt = T/m; ts = [(i+1)*dt for i in range(m)]
    drift = sum((r-0.5*sig**2)*ti for ti in ts)/m
    v = (sig*sig/(m*m))*sum(min(ts[i], ts[j]) for i in range(m) for j in range(m))
    mlog = math.log(S) + drift
    EG = math.exp(mlog + 0.5*v)
    d1 = (mlog - math.log(X) + v)/math.sqrt(v); d2 = d1 - math.sqrt(v)
    return math.exp(-r*T)*(EG*N(d1) - X*N(d2))

def asian_mc(S, X, T, r, sig, m, npaths, seed, geom=False):
    rng = random.Random(seed); dt = T/m; tot = 0.0
    for _ in range(npaths):
        logS = math.log(S); av = 0.0; lsum = 0.0
        for i in range(m):
            logS += (r-0.5*sig**2)*dt + sig*math.sqrt(dt)*rng.gauss(0, 1)
            av += math.exp(logS); lsum += logS
        avg = math.exp(lsum/m) if geom else av/m
        tot += max(avg - X, 0.0)
    return math.exp(-r*T)*tot/npaths

m = 52
geo = geo_asian_closed(S, X, T, r, sig, m)
print(f"\nAsian (m={m} weekly fixings, S=X=100, T=1, r=5%, sigma=20%):")
print(f"  geometric average, closed form = {geo:.4f}")
print(f"  geometric average, MC          = {asian_mc(S,X,T,r,sig,m,200000,11,geom=True):.4f}")
print(f"  arithmetic average, MC         = {asian_mc(S,X,T,r,sig,m,200000,11):.4f}  (no closed form)")
```
```
BSM call = 10.4506

RMSE of the MC estimator over 200 independent batches:
  n=1000    RMSE = 0.49343   RMSE*sqrt(n) = 15.6036
  n=10000   RMSE = 0.13950   RMSE*sqrt(n) = 13.9499
  n=100000  RMSE = 0.04760   RMSE*sqrt(n) = 15.0529

one batch n=100000: mean = 10.4754, sample s.d. = 14.7083, standard error = 0.0465  ->  95% CI = [10.3843, 10.5666]

Brownian bridge: X = W(s) - (s/t)W(t) with s=0.5, t=1.0
  E[X]   theory = 0.000000   empirical = -0.00024
  Var[X] theory = s(t-s)/t = 0.250000   empirical = 0.250401

Asian (m=52 weekly fixings, S=X=100, T=1, r=5%, sigma=20%):
  geometric average, closed form = 5.6374
  geometric average, MC          = 5.6471
  arithmetic average, MC         = 5.8640  (no closed form)
```

Three verifications: the RMSE ratio between $n$ and $10n$ is $3.54$ and between $10^4$ and $10^5$ is $2.93$ — both $\approx\sqrt{10}=3.16$, and `RMSE*sqrt(n)` stays flat at $14$–$15.6$ (the theoretical $\sigma_f$); the bridge variance matches $s(t-s)/t=0.25$ to three decimals; and the MC geometric-Asian price $5.6471$ lands on its closed form $5.6374$ (within the $\approx0.05$ standard error of $2\times10^5$ paths). The arithmetic Asian — *no closed form* — prints $5.8640$, correctly above the geometric value (AM ≥ GM under $\mathbb{Q}$).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Discounting under the wrong measure.** $\mathbb E^{\mathbb P}[e^{-rT}(S_T-K)^+]$ depends on $\mu$ and is not the price; the drift must be $r$ (Glasserman eq. 1.41). The change of measure moves the drift only — volatility is invariant.
2. **Silent discretisation bias on a path functional.** A crude Euler path for GBM has weak order 1, and for a running maximum only $O(h^{1/2})$ — *even for Brownian motion* (Asmussen–Glynn–Pitman, cited in Glasserman §6.4). Averaging more paths does not remove bias; only a better scheme or Brownian interpolation does.
3. **Missing the barrier between monitoring dates.** A discrete grid under-detects crossings, so a discretely-sampled knock-out is *over*-valued and the continuous-barrier limit is approached only as $h\to0$. Fix: Brownian-interpolation survival probabilities (page 06).
4. **Reading the sample mean without the sample error.** $\sigma_f/\sqrt n$ is itself estimated; the reported standard error uses $s_f=\sqrt{\frac1{n-1}\sum(Y_i-\bar Y)^2}$ (Glasserman §1.1) and the interval is only asymptotically valid — heavy tails and importance sampling (page 04) break it badly.
5. **Payoff discontinuities destroy the naive error estimate.** Indicator payoffs (digital, barrier) have $\sigma_f^2$ driven by a thin region; the CLT still holds but convergence is governed by rare events, and plain MC needs enormous $n$ for deep-OTM contracts — the entry point for importance sampling.
6. **The long-horizon likelihood-ratio pathology.** For path-functionals the Radon–Nikodym derivative of a long path degenerates: under the twisted measure the average log-ratio converges to a strictly negative constant, so the weight falls to zero a.s. while its mean stays $1$ (Glasserman §4.6). The estimator remains unbiased but has an unusable variance — this is the structural failure of naive importance sampling on long horizons.

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1 §1.1–1.2 (estimator, CLT rate, dimension-free comparison, risk-neutral measure, eq. 1.39), Ch 2 (random-number generation, inverse transform, Box–Muller, Cholesky normals), Ch 3 §3.1–3.2 (Brownian bridge eq. 3.7–3.8; exact GBM eq. 3.20–3.22; Asian/barrier/lookback payoffs), §3.5 (jump diffusion).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.6 (sampling $S_T$, sampling through a tree, estimating Greeks from simulated paths).
- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 4 §4.4 (the Gauss–Weierstrass kernel is the Brownian transition density — the same object MC samples).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.5 (tree values that any MC price can be cross-checked against).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction & Efficiency]] → [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] (American MC, QMC)
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · Pricing Formulas]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]

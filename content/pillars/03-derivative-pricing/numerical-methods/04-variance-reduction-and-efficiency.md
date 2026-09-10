---
title: "04 — Variance Reduction & Monte-Carlo Efficiency"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - monte-carlo
  - variance-reduction
  - importance-sampling
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte-Carlo Pricing]].

---

### 1. Intuition & Practical Objective

Plain Monte Carlo is unbiased and dimension-free, and therefore *slow*: error falls as $n^{-1/2}$. Variance reduction attacks the constant, not the rate — replace $\sigma_f$ by something smaller while keeping the estimator unbiased. Four standard devices plus one budget rule:

| Device | One-line mechanism | Gain |
|---|---|---|
| **Antithetic** | pair each draw with its mirror $Z\mapsto-Z$ so the two errors cancel | modest (needs monotone payoff) |
| **Control variate** | subtract a correlated quantity whose mean is known | $\times\frac{1}{1-\rho^2}$ — the big one when $\rho$ is high |
| **Stratified / LHS** | sample each stratum (or each marginal) evenly | never hurts; removes inter-stratum variance |
| **Importance sampling** | sample where the payoff *is*, reweight by the likelihood ratio | enormous for rare events; *dangerous* if mis-tuned |

The practical objective is the **work-normalised** comparison: reduction factors are only meaningful at equal path counts and equal per-path cost, and the payoff is the *same* $\sigma/\sqrt n$ with a smaller $\sigma$ (or the same accuracy with fewer paths).

Three "aha"s:

1. **A control variate is a regression.** With optimal coefficient $b^*=\mathrm{Cov}(X,Y)/\mathrm{Var}(X)$ the variance ratio is exactly $1-\rho_{XY}^2$ (Glasserman eq. 4.4) — Corollary: $\rho=0.95$ buys $10\times$, $\rho=0.70$ buys only $2\times$. Correlation must be *high* to pay.
2. **Antithetics and stratification work on opposite ends of the path.** Antithetics pair whole paths; stratification partitions a *dominant scalar* (the terminal value, via the Brownian bridge). Only stratification removes the inter-stratum piece $\mathrm{Var}[\mathbb E[Y\mid X]]$ (eq. 4.44) — stronger than a control variate, which removes only the *linear* part.
3. **Importance sampling is the only method that can be worse than useless.** It can give infinite variance for a badly chosen proposal, and its weights degenerate on long horizons (Glasserman §4.6: the likelihood ratio tends to $0$ a.s. even though its mean is $1$). It is also the *only* way to price deep-OTM contracts at all.

---

### 2. Mathematical Ground Truth & Derivations

**Control variates** (Glasserman eqs. 4.1–4.4). With $Y$ the payoff and $X$ a control with known $\mathbb E[X]$:

$$\bar Y(b)=\frac1n\sum_{i=1}^n\big(Y_i-b(X_i-\mathbb E[X])\big),\qquad
\mathrm{Var}[Y_i(b)]=\sigma_Y^2-2b\sigma_X\sigma_Y\rho_{XY}+b^2\sigma_X^2,$$

$$b^*=\frac{\mathrm{Cov}[X,Y]}{\mathrm{Var}[X]}=\rho_{XY}\frac{\sigma_Y}{\sigma_X},\qquad
\frac{\mathrm{Var}[\bar Y-b^*(X̄-\mathbb E[X])]}{\mathrm{Var}[\bar Y]}=1-\rho_{XY}^2 .$$

Multiple controls: $b^*=\Sigma_X^{-1}\Sigma_{XY}$ (eq. 4.13) and the ratio is $1-R^2$. The coefficient is estimated by the OLS slope $b̂_n=\frac{\sum(X_i-\bar X)(Y_i-\bar Y)}{\sum(X_i-\bar X)^2}$ (eq. 4.5), which biases the *estimator* by only $O(1/n)$ while remaining asymptotically as precise as $b^*$ — quoting a CV price still requires care about the bias, but it is second-order.

**Antithetic variates** (eqs. 4.27–4.30).

$$\hat Y_{\mathrm{AV}}=\frac1n\sum_{i=1}^n\frac{Y_i+\tilde Y_i}{2},\qquad
\mathrm{Var}\!\left[\frac{Y+\tilde Y}{2}\right]=\frac{\sigma_Y^2}{2}(1+\rho_{Y\tilde Y}),$$

so the gain exists **iff** $\rho_{Y\tilde Y}<0$; a monotone simulation map guarantees it, and a *linear* payoff in $Z$ gives zero variance. Splitting $f=f_0+f_1$ into symmetric/antisymmetric parts shows antithetics kill $\mathrm{Var}[f_1]$ exactly.

**Stratified sampling** (eqs. 4.31–4.44). With strata of probability $p_i$ and allocation $q_i=n_i/n$:

$$\hat Y=\sum_i\frac{p_i}{q_i}\frac{1}{n_i}\sum_jY_{ij},\qquad
\sigma^2(q)=\sum_i\frac{p_i^2}{q_i}\sigma_i^2,\qquad
q_i^{\text{Neyman}}=\frac{p_i\sigma_i}{\sum_jp_j\sigma_j}\ \ \Big(\text{cost-aware: }\propto p_i\sigma_i/\sqrt{\tau_i}\Big).$$

Proportional allocation ($q_i=p_i$) gives $\mathrm{Var}=\sum_ip_i\sigma_i^2\le\sigma^2$ **always** — "stratified sampling can only help" — because

$$\mathrm{Var}[Y]=\underbrace{\mathrm{Var}[\mathbb E[Y\mid\eta]]}_{\text{removed by proportional stratification}}+\underbrace{\mathbb E[\mathrm{Var}[Y\mid\eta]]}_{\text{left}} .$$

**Latin hypercube** (eqs. 4.55–4.58) stratifies *every* marginal coordinate with $K$ bins: for any square-integrable $f$ and $K\ge2$, $\mathrm{Var}[\hat\alpha_{\text{LHS}}]\le\sigma^2/(K-1)$ (Owen Prop. 3), and asymptotically $\sigma_\varepsilon^2/K$ (Stein) — LHS removes the variance of the **additive part** of $f$. Caveat: it stratifies the *increments* of a Brownian path, not the terminal value; directing that requires the bridge.

**Importance sampling** (eqs. 4.73–4.91). If $g$ dominates $f$,

$$\alpha=\mathbb E[h(X)]=\tilde{\mathbb E}\!\left[h(X)\frac{f(X)}{g(X)}\right],\qquad
\hat\alpha_g=\frac1n\sum_{i=1}^nh(X_i)\frac{f(X_i)}{g(X_i)},\quad X_i\sim g,$$

with the zero-variance (unusable) choice $g\propto h\,f$. Two practical tilts:

- **exponential tilting**: $f_\theta(x)=e^{\theta x-\psi(\theta)}f(x)$, with likelihood ratio $e^{-\theta\sum X_i+n\psi(\theta)}$ (eq. 4.84);
- **drift tilt** for Gaussian paths ($Z\mapsto Z+\mu$): likelihood ratio $e^{-\mu'Z+\frac12\mu'\mu}$, where $\mu$ solves the fixed-point $\nabla F(\mu)=\mu'$ — the *optimal path* (eqs. 4.89–4.90).

**The efficiency rule** (Glasserman §1.1.3, §6.3.3): with bias $b\delta^\beta$, cost per path $\propto\delta^{-\eta}$ and work budget $s$,

$$\mathrm{RMSE}=O\!\big(s^{-\beta/(2\beta+\eta)}\big),\qquad\text{discretisation-aware: }\ \delta^*\propto s^{-1/(2\beta+1)},\quad \sqrt{\mathrm{MSE}}\propto s^{-\beta/(2\beta+1)} .$$

For $\beta=1$ (Euler) the budget rate is $s^{-1/3}$ versus $s^{-1/2}$ for an unbiased estimator: **discretisation costs you half the convergence exponent**, which is why exact sampling (page 03) and better schemes are worth more than more paths.

---

### 3. Computational Implementation — four reductions, measured

Each device is measured at a fixed path budget, against the closed form where one exists.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bsm_call(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return S*N(d1) - X*math.exp(-r*T)*N(d2)
def bsm_digital(S, X, T, r, sig):        # e^{-rT} P(S_T > X)
    d2 = (math.log(S/X)+(r-0.5*sig**2)*T)/(sig*math.sqrt(T))
    return math.exp(-r*T)*N(d2)

S, X, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.20
exact = bsm_call(S, X, T, r, sig)

def paths(n, seed, antithetic=False):
    rng = random.Random(seed); out = []
    for _ in range(n):
        Z = rng.gauss(0, 1)
        out.append(S*math.exp((r-0.5*sig**2)*T + sig*math.sqrt(T)*Z))
        if antithetic: out.append(S*math.exp((r-0.5*sig**2)*T - sig*math.sqrt(T)*Z))
    return out

# ---------- 1. plain vs antithetic ----------
def est_plain(n, seed):
    P = paths(n, seed); return math.exp(-r*T)*sum(max(p-X, 0.0) for p in P)/len(P)
def est_anti(n, seed):
    P = paths(2*n, seed, True); return math.exp(-r*T)*sum(max(p-X, 0.0) for p in P)/len(P)

print(f"BSM call = {exact:.4f}")
N_TOT = 40000                                   # equal number of paths for both estimators
vp = [est_plain(N_TOT, s) for s in range(40)]
va = [est_anti(N_TOT//2, s) for s in range(40)]
mp = sum(vp)/len(vp); ma = sum(va)/len(va)
sp = math.sqrt(sum((x-mp)**2 for x in vp)/len(vp))
sa = math.sqrt(sum((x-ma)**2 for x in va)/len(va))
print(f"\nantithetic, {N_TOT} paths per replication, 40 replications:")
print(f"  plain      mean={mp:.5f}  s.d.={sp:.5f}")
print(f"  antithetic mean={ma:.5f}  s.d.={sa:.5f}   VR factor = {(sp/sa)**2:.2f}x")

# ---------- 2. control variate: terminal stock (E^Q[e^{-rT} S_T] = S_0) ----------
rng = random.Random(51)
n = 50000; ys = []; xs = []
for _ in range(n):
    Z = rng.gauss(0, 1); ST = S*math.exp((r-0.5*sig**2)*T + sig*math.sqrt(T)*Z)
    ys.append(math.exp(-r*T)*max(ST-X, 0.0)); xs.append(math.exp(-r*T)*ST)   # E[x] = S = 100
yb = sum(ys)/n; xb = sum(xs)/n
sxy = sum((xs[i]-xb)*(ys[i]-yb) for i in range(n))/(n-1)
sxx = sum((xs[i]-xb)**2 for i in range(n))/(n-1)
b = sxy/sxx
corr = sxy/math.sqrt(sxx*sum((y-yb)**2 for y in ys)/(n-1))
cv = [ys[i] - b*(xs[i]-100.0) for i in range(n)]
print(f"\ncontrol variate (terminal asset, E[x]=100):")
print(f"  b* = {b:.4f}   corr(Y,X) = {corr:.4f}")
print(f"  plain    mean={yb:.5f}  s.d.={math.sqrt(sum((y-yb)**2 for y in ys)/(n-1)):.5f}")
print(f"  CV       mean={sum(cv)/n:.5f}  s.d.={math.sqrt(sum((c-sum(cv)/n)**2 for c in cv)/(n-1)):.5f}"
      f"   VR factor = {1/(1-corr**2):.2f}x")

# ---------- 3. control variate: geometric Asian for the arithmetic Asian ----------
def geo_asian_closed(S, X, T, r, sig, m):
    dt = T/m; ts = [(i+1)*dt for i in range(m)]
    drift = sum((r-0.5*sig**2)*ti for ti in ts)/m
    v = (sig*sig/(m*m))*sum(min(ts[i], ts[j]) for i in range(m) for j in range(m))
    mlog = math.log(S) + drift; EG = math.exp(mlog+0.5*v)
    d1 = (mlog - math.log(X) + v)/math.sqrt(v); d2 = d1-math.sqrt(v)
    return math.exp(-r*T)*(EG*N(d1) - X*N(d2))

mm = 12; dt = T/mm
rng = random.Random(99); n = 20000; A = []; G = []
for _ in range(n):
    logS = math.log(S); av = 0.0; lsum = 0.0
    for i in range(mm):
        logS += (r-0.5*sig**2)*dt + sig*math.sqrt(dt)*rng.gauss(0, 1)
        av += math.exp(logS); lsum += logS
    A.append(math.exp(-r*T)*max(av/mm - X, 0.0))
    G.append(math.exp(-r*T)*max(math.exp(lsum/mm) - X, 0.0))
Abar = sum(A)/n; Gbar = sum(G)/n
sAA = sum((a-Abar)**2 for a in A)/(n-1); sGG = sum((g-Gbar)**2 for g in G)/(n-1)
sAG = sum((A[i]-Abar)*(G[i]-Gbar) for i in range(n))/(n-1)
rho = sAG/math.sqrt(sAA*sGG); bc = sAG/sGG
cv = [A[i]-bc*(G[i]-geo_asian_closed(S,X,T,r,sig,mm)) for i in range(n)]
scv = sum((c-sum(cv)/n)**2 for c in cv)/(n-1)
print(f"\nArithmetic Asian (m={mm} monthly fixings) with geometric-Asian control:")
print(f"  geometric closed form = {geo_asian_closed(S,X,T,r,sig,mm):.4f}")
print(f"  plain  mean={Abar:.5f}  s.d.={math.sqrt(sAA):.5f}")
print(f"  corr(A,G) = {rho:.5f}   b* = {bc:.5f}")
print(f"  CV     mean={sum(cv)/n:.5f}  s.d.={math.sqrt(scv):.5f}   VR factor = {sAA/scv:.1f}x")

# ---------- 4. importance sampling for a deep-OTM digital ----------
K2 = 200.0
p_true = bsm_digital(S, K2, T, r, sig)
d2 = (math.log(S/K2)+(r-0.5*sig**2)*T)/(sig*math.sqrt(T))
mu = -d2                                  # mean shift that puts S_T at K2
def is_digital(n, seed, tilt):
    rng = random.Random(seed); tot = 0.0
    for _ in range(n):
        Z = rng.gauss(tilt, 1.0)
        ST = S*math.exp((r-0.5*sig**2)*T + sig*math.sqrt(T)*Z)
        lr = math.exp(-tilt*Z + 0.5*tilt*tilt)          # exact likelihood ratio
        tot += math.exp(-r*T)*(1.0 if ST > K2 else 0.0)*lr
    return tot/n
def plain_digital(n, seed):
    rng = random.Random(seed); tot = 0.0
    for _ in range(n):
        Z = rng.gauss(0, 1)
        ST = S*math.exp((r-0.5*sig**2)*T + sig*math.sqrt(T)*Z)
        tot += math.exp(-r*T)*(1.0 if ST > K2 else 0.0)
    return tot/n
print(f"\ndeep-OTM digital e^-rT P(S_T>200) = {p_true:.6f}  ({p_true*100:.4f}%)")
print(f"  importance-sampling tilt = -d2 = {mu:.4f}")
for name, fn, tilt in (("plain MC", plain_digital, 0.0), ("IS (tilt mu=-d2)", is_digital, mu)):
    vals = [fn(20000, s, tilt) if tilt else fn(20000, s) for s in range(40)]
    m = sum(vals)/len(vals); sd = math.sqrt(sum((x-m)**2 for x in vals)/len(vals))
    print(f"  {name:<20} mean={m:.6f}  s.d.={sd:.6f}  RMSE={sd:.6f}")
```
```
BSM call = 10.4506

antithetic, 40000 paths per replication, 40 replications:
  plain      mean=10.45393  s.d.=0.06288
  antithetic mean=10.44366  s.d.=0.02995   VR factor = 4.41x

control variate (terminal asset, E[x]=100):
  b* = 0.6712   corr(Y,X) = 0.9235
  plain    mean=10.36309  s.d.=14.68969
  CV       mean=10.46268  s.d.=5.63456   VR factor = 6.80x

Arithmetic Asian (m=12 monthly fixings) with geometric-Asian control:
  geometric closed form = 5.9402
  plain  mean=6.12306  s.d.=8.56588
  corr(A,G) = 0.99960   b* = 1.03178
  CV     mean=6.15677  s.d.=0.24163   VR factor = 1256.7x

deep-OTM digital e^-rT P(S_T>200) = 0.000435  (0.0435%)
  importance-sampling tilt = -d2 = 3.3157
  plain MC             mean=0.000476  s.d.=0.000121  RMSE=0.000121
  IS (tilt mu=-d2)     mean=0.000436  s.d.=0.000004  RMSE=0.000004
```

The numbers confirm the theory each time. Antithetic: $4.41\times$. Control variate for the European call: measured $6.80\times$ against the theoretical $1/(1-\rho^2)=1/(1-0.9235^2)=6.80$ — an exact match. Control variate for the arithmetic Asian: $1256.7\times$, driven entirely by $\rho=0.99960$ (a correlation of $0.9996$ is what "same payoff, closed form" buys). Importance sampling on a $0.0435\%$ event: RMSE falls from $1.21\times10^{-4}$ to $4\times10^{-6}$, a variance ratio of $\approx915\times$ — and the plain-MC mean is $9.4\%$ high while the IS mean is $0.2\%$ high.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A control variate that is only mildly correlated is a waste of code.** $\rho=0.70$ gives $1.96\times$; $\rho=0.30$ gives $1.10\times$. Corollary: use controls that are *almost the payoff* (geometric Asian, the underlying itself) and reject the rest.
2. **Antithetics can hurt.** If the payoff is not monotone in $Z$ (a straddle, a butterfly, a barrier), $\rho_{Y\tilde Y}>0$ and the paired estimator is *worse* than plain MC. Check $\rho<0$ before using it.
3. **Importance sampling with the wrong tilt has infinite variance.** Tilting too far concentrates on paths the payoff never reaches; the sampled variance reflects a heavy-tailed weight distribution, and the reported standard error is then a lie. The safe diagnostic is the *estimated second moment of the weight*, which must be finite and tame (Glasserman §4.6, Table 4.5: stratification on top of IS is what delivers the $10^3$–$10^4$ factors).
4. **Long-horizon likelihood-ratio degeneracy.** Under the twisted measure, $\frac1m\sum\log(f/g)\to c<0$ (Jensen/Glynn–Iglehart), so the likelihood ratio of a long path tends to $0$ a.s. even though $\mathbb E[\text{LR}]=1$ at every $m$. Any IS scheme whose weights are spread over many steps inherits this; the cure is a *drift* change (much narrower spread) rather than a per-step density change.
5. **Conflating variance with accuracy.** A $1256\times$ variance reduction on the Asian does **not** mean $1256\times$ accuracy: it means the same accuracy as $1256\times$ more paths, at the cost of one extra closed-form evaluation per path. Report the *work-normalised* efficiency, or the comparison is meaningless.
6. **The score/likelihood-ratio Greek explodes with the number of dates.** The LR score is a mean-zero martingale, so its variance grows with the monitoring count and blows up as the first interval $t_1\to0$. For path-dependent Greeks, use pathwise (page 06) with a smoothing correction, not raw LR.

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 4 §4.1 (control variates eqs. 4.1–4.20), §4.2 (antithetic 4.27–4.30), §4.3 (stratification 4.31–4.46), §4.4 (LHS 4.55–4.58), §4.5 (matching/weighted MC 4.60–4.72), §4.6 (importance sampling 4.73–4.91, GHS optimal path, weight degeneracy), §4.7 (qualitative ranking, Fig 4.16).
- **Glasserman**, Ch 1 §1.1.3 (efficiency and the $\mathrm{RMSE}=O(s^{-\beta/(2\beta+\eta)})$ framework) and Ch 6 §6.3.3 (MSE balancing, eqs. 6.47–6.48).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.7 (antithetic, control variate, importance sampling, stratified sampling, moment matching, quasi-random sequences — the practitioner's checklist version).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.5 (closed-form geometric-average and trinomial benchmarks used as controls and cross-checks).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte-Carlo Pricing]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] (QMC, American MC, pathwise Greeks)
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Advanced Extensions]] (jump-diffusion MC and the same variance toolbox)

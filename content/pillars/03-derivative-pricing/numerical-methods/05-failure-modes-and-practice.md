---
title: "05 — Failure Modes & Numerical Practice"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - failure-modes
  - stability
  - accuracy
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] and [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo Pricing]].

---

### 1. Intuition & Practical Objective

Every numerical price is wrong, and the only useful question is *how*. This page quantifies the five failure modes that actually bite in production, each tied to the first-principle assumption it violates:

1. **Crank–Nicolson rings at a kink** — stability without positivity.
2. **Explicit FDM blows up outside its CFL bound** — a violated stability condition.
3. **Euler discretisation biases every path functional** — weak order 1, and worse for extrema.
4. **Domain truncation silently prices a different contract** — a false boundary condition.
5. **Importance sampling makes things worse when mis-tilted** — an unbounded likelihood-ratio variance.

The discipline: measure the error against a benchmark you trust (a closed form, a tree, or a refined run) *before* believing a price.

---

### 2. Mathematical Ground Truth & Derivations

**The discrete maximum principle is what "no ringing" means.** For a two-level scheme $U^{n+1}=QU^n$, if $Q$ has non-negative entries and rows summing to at most one, then positivity of the input implies positivity of the output (Duffy Def 9.1, Lemma 11.1). Crank–Nicolson violates this at high frequency: its symbol is

$$
\rho_{\mathrm{CN}}(\xi)=\frac{1-2\lambda\sin^2(\xi/2)}{1+2\lambda\sin^2(\xi/2)}\ \longrightarrow\ -1 \quad (\text{high frequency}),
$$

so the highest modes flip sign every step and decay only slowly. *An unconditionally stable scheme can still be a ringing scheme.* The Richardson/Cooney cure is the extrapolated implicit-Euler scheme

$$
V(t+k)=2\,U_{k/2}^{(2)}-U_{k}^{(1)},\qquad U^{(1)}=(I+kA)^{-1}V,\quad U^{(2)}=(I+\tfrac k2A)^{-2}V,
$$

which is second-order *and* positive (Duffy eq. 6.36); the industrial variant is **Rannacher's method**: two fully implicit steps, then CN.

**The explicit stability bound in financial coordinates** (Duffy eqs. 12.15–12.18). For the BSM operator with a grid of step $h$ and $S_{\max}$ large,

$$
k\ \le\ \frac{h^2}{\sigma^2S_{\max}^2}\qquad(\text{equivalently }h\le\sigma^2S_j/r,\ \ k\le 1/(\sigma^2j^2+r)).
$$

The bound scales with $h^2$ but *inversely with $S_{\max}^2$*: the further out you truncate the domain to control failure mode 4, the more time steps failure mode 2 demands. That is the explicit scheme's trap.

**The MC bias budget** (Glasserman §6.1–6.3): Euler's weak order is $1$ — bias $\approx c\,h$ — while the sampling error is $\sigma/\sqrt n$. Balancing them with a work budget $s$ gives $h^*\propto s^{-1/(2\beta+1)}$ and $\sqrt{\mathrm{MSE}}\propto s^{-\beta/(2\beta+1)}$ (eqs. 6.47–6.48): for Euler ($\beta=1$) the achievable rate is $s^{-1/3}$, strictly worse than the unbiased $s^{-1/2}$. For running extrema/barriers the Euler-on-maximum scheme is only weak order $\le\tfrac12$ — bias removal requires **Brownian interpolation**:

$$
\hat M_i=\frac{\hat X_{i+1}+\hat X_i+\sqrt{(\hat X_{i+1}-\hat X_i)^2-2b_i^2h\log U_i}}{2},\qquad
\hat p_i=\mathbb P(\hat M_i\le B\mid\hat X_i,\hat X_{i+1})=1-\exp\!\left(-\frac{2(B-\hat X_i)(B-\hat X_{i+1})}{b(\hat X_i)^2h}\right).
$$

**Truncation boundary conditions.** The call's far-field condition $V(S_{\max},t)=S_{\max}-Ke^{-r(T-t)}$ is exact only in the limit. Duffy's own warning (Ch 4): "specifying boundary conditions for the Black–Scholes equation is somewhat of a black art"; his remedies are far-field truncation at a multiple of $K$, the transformation $x=S/(S+K)$ onto $(0,1)$ (coefficients vanish at the endpoints, so *no* boundary condition is needed), or the linearity condition $\partial^2V/\partial S^2=0$ (Hull eq. 21.x, Duffy B3).

---

### 3. Computational Implementation — the five failures, measured

One script, five experiments. Every number is compared against either the closed form or a refined reference run.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)
def bsm_call(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return S*N(d1)-X*math.exp(-r*T)*N(d2)

def thomas(lo, di, up, rh):
    n = len(rh); cp=[0.0]*n; dp=[0.0]*n
    cp[0]=up[0]/di[0]; dp[0]=rh[0]/di[0]
    for i in range(1, n):
        m = di[i]-lo[i]*cp[i-1]
        cp[i] = up[i]/m if i < n-1 else 0.0
        dp[i] = (rh[i]-lo[i]*dp[i-1])/m
    x=[0.0]*n; x[n-1]=dp[n-1]
    for i in range(n-2, -1, -1): x[i] = dp[i]-cp[i]*x[i+1]
    return x

S, X, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.20
exact = bsm_call(S, X, T, r, sig)

def solve_call(M, nt, Smax, mode):
    """mode: 'CN', 'implicit', 'Rannacher' (implicit first two steps, then CN)."""
    h = Smax/M; k = T/nt
    Sj = [j*h for j in range(M+1)]
    a=[0.0]*(M+1); b=[0.0]*(M+1); c=[0.0]*(M+1)
    for j in range(M+1):
        s2 = sig*sig*Sj[j]*Sj[j]
        a[j] = 0.5*s2/h**2-r*Sj[j]/(2*h); b[j] = -s2/h**2-r; c[j] = 0.5*s2/h**2+r*Sj[j]/(2*h)
    V = [max(Sj[j]-X, 0.0) for j in range(M+1)]
    for n in range(nt):
        w = {"CN":0.5, "implicit":1.0}.get(mode, 1.0 if n < 2 else 0.5)
        V0, VM = 0.0, Smax-X*math.exp(-r*(n+1)*k)
        lo=[0.0]*(M-1); di=[0.0]*(M-1); up=[0.0]*(M-1); rh=[0.0]*(M-1)
        for j in range(1, M):
            lo[j-1]=-w*k*a[j]; di[j-1]=1.0-w*k*b[j]; up[j-1]=-w*k*c[j]
            rh[j-1]=V[j]+(1.0-w)*k*(a[j]*V[j-1]+b[j]*V[j]+c[j]*V[j+1])
        rh[0] += w*k*a[1]*V0; rh[M-2] += w*k*c[M-1]*VM
        x = thomas(lo, di, up, rh)
        for j in range(1, M): V[j] = x[j-1]
        V[0], V[M] = V0, VM
    return Sj, V, h

# ---------- failure 1: Crank-Nicolson ringing in the GREEK profile ----------
print("second derivative (gamma) of the computed grid solution, M=200, S_max=200, T=1")
maxgamma_true = max(phi((math.log(sj/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)))/(sj*sig*math.sqrt(T))
                    for sj in [1.0*i for i in range(1, 200)])
print(f"  analytic max gamma on the grid           = {maxgamma_true:.5f}")
for nt in (4, 16, 64):
    line = []
    for mode in ("CN", "implicit", "Rannacher"):
        Sj, V, h = solve_call(200, nt, 200.0, mode)
        g = max((V[j+1]-2*V[j]+V[j-1])/h**2 for j in range(1, 200))
        line.append(f"{mode}={g:.5f}")
    print(f"  nt={nt:<3d} max computed gamma:  " + "   ".join(line))
print(f"  -> CN overshoots the true maximum; implicit and Rannacher (2 implicit steps) do not.")

# ---------- failure 2: explicit FDM and the CFL bound ----------
def explicit_bs(M, nt, Smax=400.0):
    h = Smax/M; k = T/nt
    Sj = [j*h for j in range(M+1)]
    a=[0.0]*(M+1); b=[0.0]*(M+1); c=[0.0]*(M+1)
    for j in range(M+1):
        s2 = sig*sig*Sj[j]*Sj[j]
        a[j] = 0.5*s2/h**2-r*Sj[j]/(2*h); b[j] = -s2/h**2-r; c[j] = 0.5*s2/h**2+r*Sj[j]/(2*h)
    V = [max(Sj[j]-X, 0.0) for j in range(M+1)]
    for n in range(nt):
        Vn = V[:]; V = [0.0]*(M+1)
        V[0], V[M] = 0.0, Smax-X*math.exp(-r*(n+1)*k)
        for j in range(1, M):
            V[j] = Vn[j]+k*(a[j]*Vn[j-1]+b[j]*Vn[j]+c[j]*Vn[j+1])
    j = int(S/h); f = (S-j*h)/h
    return (1-f)*V[j]+f*V[j+1]

kmax = (400.0/100)**2/(sig*sig*400.0**2)
print(f"\nexplicit scheme, M=100 (Crank-Nicolson needs no such bound): k_max = h^2/(sigma^2 S_max^2) = {kmax:.2e}")
for nt in (100, 200, 400, 4000):
    v = explicit_bs(100, nt)
    tag = 'STABLE (at the bound)' if abs(T/nt-kmax) < 1e-9 else ('STABLE' if T/nt < kmax else 'UNSTABLE')
    print(f"  nt={nt:<5d} (k={T/nt:.2e}) value = {v:>13.5e}   {tag}")

# ---------- failure 3: Euler discretisation bias, and the log-Euler fix ----------
def euro_call_mc(n, steps, seed, log_euler=False):
    rng = random.Random(seed); dt = T/steps; tot = 0.0
    for _ in range(n):
        if log_euler:
            ls = math.log(S)
            for _ in range(steps): ls += (r-0.5*sig**2)*dt+sig*math.sqrt(dt)*rng.gauss(0, 1)
            ST = math.exp(ls)
        else:
            s_ = S
            for _ in range(steps): s_ = s_*(1.0+r*dt+sig*math.sqrt(dt)*rng.gauss(0, 1))
            ST = s_
        tot += max(ST-X, 0.0)
    return math.exp(-r*T)*tot/n

print(f"\nEuler-Maruyama bias for the European call (exact = {exact:.4f}), 200000 paths x 4 seeds:")
for steps in (1, 2, 4, 8, 16):
    b = [euro_call_mc(200000, steps, s) for s in range(4)]
    m = sum(b)/len(b)
    print(f"  Euler steps={steps:<3d} mean = {m:.4f}   bias = {m-exact:+.4f}")
b = [euro_call_mc(200000, 1, s, log_euler=True) for s in range(4)]
print(f"  log-Euler steps=  1 mean = {sum(b)/len(b):.4f}   bias = {sum(b)/len(b)-exact:+.4f}  (exact for GBM)")

# ---------- failure 4: domain truncation, isolated from discretisation error ----------
print("\ndomain truncation, h fixed at 1.0 (M = S_max), nt=200:")
for Smax in (120.0, 150.0, 200.0, 400.0, 800.0):
    M = int(Smax)
    Sj, V, h = solve_call(M, 200, Smax, "CN")
    j = int(S/h); f = (S-j*h)/h
    val = (1-f)*V[j]+f*V[j+1]
    print(f"  S_max={Smax:6.0f}: value = {val:.5f}   error = {val-exact:+.5f}")

# ---------- failure 5: importance-sampling weight degeneracy ----------
def is_call(n, tilt, seed):
    rng = random.Random(seed); tot = 0.0
    for _ in range(n):
        Z = rng.gauss(tilt, 1.0)
        ST = S*math.exp((r-0.5*sig**2)*T+sig*math.sqrt(T)*Z)
        tot += math.exp(-r*T)*max(ST-X, 0.0)*math.exp(-tilt*Z+0.5*tilt*tilt)
    return tot/n

print(f"\nimportance sampling for the ATM call (exact = {exact:.4f}), 20000 paths x 20 seeds:")
for tilt in (0.0, 1.0, 2.0, 4.0):
    b = [is_call(20000, tilt, s) for s in range(20)]
    m = sum(b)/len(b); sd = math.sqrt(sum((x-m)**2 for x in b)/len(b))
    print(f"  tilt mu={tilt:<4.1f} mean = {m:>8.4f}  s.d. = {sd:.4f}")
```
```
second derivative (gamma) of the computed grid solution, M=200, S_max=200, T=1
  analytic max gamma on the grid           = 0.02182
  nt=4   max computed gamma:  CN=0.70717   implicit=0.02307   Rannacher=0.02211
  nt=16  max computed gamma:  CN=0.12813   implicit=0.02209   Rannacher=0.02185
  nt=64  max computed gamma:  CN=0.02182   implicit=0.02189   Rannacher=0.02183
  -> CN overshoots the true maximum; implicit and Rannacher (2 implicit steps) do not.

explicit scheme, M=100 (Crank-Nicolson needs no such bound): k_max = h^2/(sigma^2 S_max^2) = 2.50e-03
  nt=100   (k=1.00e-02) value =  -1.95782e+07   UNSTABLE
  nt=200   (k=5.00e-03) value =  -7.48485e+10   UNSTABLE
  nt=400   (k=2.50e-03) value =   1.04134e+01   STABLE (at the bound)
  nt=4000  (k=2.50e-04) value =   1.04110e+01   STABLE

Euler-Maruyama bias for the European call (exact = 10.4506), 200000 paths x 4 seeds:
  Euler steps=1   mean = 10.2075   bias = -0.2430
  Euler steps=2   mean = 10.3646   bias = -0.0860
  Euler steps=4   mean = 10.4381   bias = -0.0125
  Euler steps=8   mean = 10.4408   bias = -0.0098
  Euler steps=16  mean = 10.4697   bias = +0.0191
  log-Euler steps=  1 mean = 10.4534   bias = +0.0028  (exact for GBM)

domain truncation, h fixed at 1.0 (M = S_max), nt=200:
  S_max=   120: value = 10.23486   error = -0.21572
  S_max=   150: value = 10.44802   error = -0.00256
  S_max=   200: value = 10.44812   error = -0.00246
  S_max=   400: value = 10.44812   error = -0.00246
  S_max=   800: value = 10.44812   error = -0.00246

importance sampling for the ATM call (exact = 10.4506), 20000 paths x 20 seeds:
  tilt mu=0.0  mean =  10.4603  s.d. = 0.0651
  tilt mu=1.0  mean =  10.4594  s.d. = 0.0206
  tilt mu=2.0  mean =  10.4284  s.d. = 0.0481
  tilt mu=4.0  mean =  10.1557  s.d. = 1.1247
```

Read the five verdicts off the numbers: CN inflates the true maximum gamma $0.02182$ by $32\times$ at $\Delta t=0.25$ and is still off by $6\times$ at $\Delta t=0.0625$, while implicit and Rannacher stay within $6\%$ throughout; the explicit scheme returns $-1.96\times10^{7}$ and $-7.48\times10^{10}$ on the wrong side of its bound, then $10.41$ once inside it; Euler's bias is $-0.2430$ at a single step and falls roughly as $1/\text{steps}$, disappearing into the $\pm0.02$ Monte Carlo noise by 8 steps, while the log-Euler scheme is exact at **one** step; truncating at $S_{\max}=120$ costs $0.2157$ ($2.1\%$) and nothing improves past $S_{\max}=150$; and a tilt of $\mu=1$ cuts the digital-free call's standard error $3.2\times$ ($9.99\times$ in variance) while $\mu=2$ and $\mu=4$ make it *worse* than no tilt at all ($0.0481$ and $1.1247$ against $0.0651$).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Ringing without instability (CN at a kink).** CN's symbol is negative at high frequency, so the payoff kink's error alternates in sign and decays slowly. It is *stable*, hence convergent, hence wrong only in the Greek/high-frequency content — which is precisely what hedgers use. Fix: Rannacher (two implicit start-up steps), Richardson-extrapolated implicit Euler, or smooth the initial datum (Duffy Ch 33).
2. **Violating the CFL bound (explicit).** $k\le h^2/(\sigma^2S_{\max}^2)$ is a *hard* constraint: values of $-10^{7}$ are not "approximate", they are meaningless. Fix: switch to implicit/CN, or use exponential fitting whose stability is independent of $h$ (Duffy Ch 11).
3. **Discretisation bias masquerading as noise.** Euler's $-0.2430$ bias at one step is $\approx8.6\times$ the Monte Carlo standard error, so no path count removes it. Fix: the log transform (exact for GBM), a weak-order-2 scheme, or Richardson extrapolation $2\mathbb E[\hat X^h]-\mathbb E[\hat X^{2h}]$ (Glasserman eq. 6.43) — and for barriers/extrema, Brownian interpolation, since the Euler running-max scheme is only weak order $\le\frac12$.
4. **Truncation error is a *bias*, not a mesh error.** $S_{\max}=120$ produced a $2.1\%$ error that vanished when $S_{\max}\ge150$ — refining $h$ inside the truncated domain would never have fixed it. Fix: set $S_{\max}$ from a multiple of $K$ (or use $x=S/(S+K)$ to eliminate the boundary condition entirely) and *verify* by widening once.
5. **A badly tilted importance sampler is worse than none.** The variance of the likelihood ratio is the whole game; tilting towards a region the payoff does not reach inflates it. Diagnostic: monitor the second moment of the weights, and reach for stratification on top of IS rather than a bigger tilt.
6. **Reporting one number.** "The model says 10.42" is the failure mode that hides all five others. Report the price *plus* its error budget: $\pm$ MC standard error, the mesh/order term, the boundary term, and the scheme (CN vs Rannacher vs implicit).

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering* — Ch 6 (Richardson/extrapolated implicit Euler eq. 6.36, the ringing warning), Ch 9 (positive-type schemes Def 9.1), Ch 11 (discrete maximum principle, fitting, uniform convergence Thm 11.1), Ch 12 (explicit BS stability bounds 12.15–12.18), Ch 30 (boundary-condition taxonomy B1–B4, transformations, Rannacher), Ch 33 (non-smooth payoffs and CN oscillations).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering* — Ch 6 §6.1–6.2 (weak order 1, extrapolation 6.43), §6.3.3 (MSE balancing 6.47–6.48), §6.4 (running maxima, Brownian interpolation, survival probability 6.51), §6.5 (change of variables: log transform exact for GBM), §4.6 (IS weight degeneracy).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.8 (boundary conditions, the $\ln S$ change of variable as a convergence fix, implicit/explicit/CN trade-offs).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.2 (the CRR American put $4.692$ used as the benchmark in [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling robustness pages: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]

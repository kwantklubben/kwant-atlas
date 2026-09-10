---
title: "06 — Advanced Extensions: American, Multidimensional, QMC"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - american-options
  - adi
  - quasi-monte-carlo
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]].

---

### 1. Intuition & Practical Objective

The two families of pages 02–04 solve *linear* problems on *one* state variable. Three things break that: **(i) early exercise** turns the PDE into a free-boundary (variational-inequality) problem and the MC into a *stopping-time* problem; **(ii) extra factors** make a full grid cost $O(N^d)$ and force operator splitting; **(iii) high effective dimension** is where Monte Carlo's $n^{-1/2}$ starts to be beaten by *deterministic* point sets. This page is the launchpad for all three, each with a runnable check against a benchmark.

> **Why these three?** They are the exact three axes on which production pricing systems are chosen: exercise style, dimension, and dimension-free error. Everything else (Heston, LMM, jump PIDEs) is these solvers applied to a wider operator.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 American options: three equivalent statements

**Free boundary / complementarity** (Duffy eqs. 26.5–26.11). For an American put with exercise boundary $B(t)$:

$$\frac{\partial P}{\partial t}+\tfrac12\sigma^2S^2\frac{\partial^2P}{\partial S^2}+rS\frac{\partial P}{\partial S}-rP=0 \ \ \text{for }S>B(t),\qquad
P\ge\max(K-S,0)\ \ \text{everywhere},$$

with **smooth pasting** at the boundary $P(B(t),t)=K-B(t)$ and $\partial P/\partial S(B(t),t)=-1$, and terminal boundary $B(T)=K$. Equivalently: $\mathcal LP\le0$ and $P\ge g$, with $(\mathcal LP)\,(P-g)=0$ — a linear complementarity problem.

**Penalty regularisation** (Duffy eqs. 28.15–28.17). Replace the constraint by a large nonlinear reaction term:

$$f_\varepsilon(P_\varepsilon)=\frac1\varepsilon\,[g(S)-P_\varepsilon]^+ \qquad\text{or}\qquad f_\varepsilon(P_\varepsilon)=\frac{\varepsilon C}{P_\varepsilon+\varepsilon-q(S)},\quad q(S)=K-S,\ C\ge rK,$$

then $P_\varepsilon\to P$ in $L^\infty_{\text{loc}}$ as $\varepsilon\to0$ (Thm 28.2). The semi-implicit scheme (implicit in the linear terms, explicit in $f_\varepsilon$) satisfies the discrete constraint $P^n_j\ge\max(q,0)$ **iff** $k\le\varepsilon/(rK)$ (Thm 28.3) — a cheap, monotone, no-Newton route.

**Projected SOR on the LCP** (Duffy eq. 29.11, Thm 29.1).

$$z_j^{(k+1)}=b_j+\sum_{i<j}A_{ji}c_i^{(k+1)}-\sum_{i>j}A_{ji}c_i^{(k)},\qquad
c_j^{(k+1)}=\max\!\big(0,\ c_j^{(k)}+\omega\,z_j^{(k+1)}/A_{jj}\big),$$

convergent for any start **iff** $0<\omega<2$ (positive-definiteness of $A$ is what matters). For a put the projection max is against intrinsic value.

**Monte Carlo: Longstaff–Schwartz (LSM)** (Glasserman eqs. 8.46–8.52). Regress the realised discounted continuation value on basis functions of the current state,

$$\hat C_i(x)=\hat\beta_i'\psi(x),\qquad \hat\beta_i=\hat B_\psi^{-1}\hat B_{\psi V},\qquad
\hat V_{ij}=h_i(X_{ij})\ \text{if }h_i\ge\hat C_i(X_{ij}),\ \text{else}\ \hat V_{i+1,j}.$$

Two distinct estimators must not be confused: the **Tsitsiklis–van Roy regression DP** ($\hat V=\max\{h_i,\hat C_i\}$, biased **high** through Jensen when the basis is imperfect) and **LSM** (value taken from the *realised* continuation path, biased **low**: any implementable stopping rule is suboptimal). Duality closes the bracket (Glasserman eqs. 8.58, 8.65):

$$V_0=\sup_\tau\mathbb E[h_\tau]=\inf_M\mathbb E\!\left[\max_{k=1..m}\big(h_k(X_k)-M_k\big)\right]\ \Longrightarrow\ \text{low}\le V_0\le\text{dual upper}.$$

#### 2.2 Multidimensional: ADI and operator splitting

**Peaceman–Rachford ADI** (Duffy eqs. 19.7a–b, growth factor 19.5/19.6): each half-step is only *conditionally* stable, but the two-leg step is **unconditionally** stable and second order in time and space:

$$\frac{U^{n+\frac12}_{ij}-U^n_{ij}}{k/2}=\Delta^2_xU^{n+\frac12}_{ij}+\Delta^2_yU^{n}_{ij},\qquad
\frac{U^{n+1}_{ij}-U^{n+\frac12}_{ij}}{k/2}=\Delta^2_xU^{n+\frac12}_{ij}+\Delta^2_yU^{n+1}_{ij}.$$

Two hard limits from Duffy: a naive three-leg ADI in 3-D is **not** unconditionally stable (eq. 19.34 → use Douglas–Rachford), and **ADI breaks down with mixed derivatives** (eq. 19.37) — exactly the correlated multi-asset case. The fix is **Yanenko splitting**, treating the cross term explicitly (eqs. 20.8/20.9), or a general $m$-way split $L=L_1+\dots+L_m$ converging when the discrete operators commute (eqs. 20.21–20.24).

#### 2.3 Quasi-Monte Carlo

**Koksma–Hlawka** (Glasserman eq. 5.10): for a deterministic low-discrepancy set with star discrepancy $D^*$,

$$\left|\frac1n\sum_if(x_i)-\int f\right|\ \le\ V_{HK}(f)\,D^*,\qquad
D^*\le C(d,b)\,b^t\,\frac{(\log n)^d}{n}+O\!\Big(\frac{(\log n)^{d-1}}{n}\Big),$$

so QMC's error is $O(n^{-1+\varepsilon})$ against Monte Carlo's $O(n^{-1/2})$ — **conditional on finite Hardy–Krause variation $V_{HK}(f)$**, which fails for non-axis-aligned indicator payoffs (barriers) and is the reason QMC is applied to *smooth* integrands. Randomisation (**random shift / digit scrambling**) restores unbiasedness and gives valid error bars, with scrambled-net variance $O(n^{-(3-\varepsilon)})$ for smooth $f$ — a rate Monte Carlo can never reach.

---

### 3. Computational Implementation — three checks

**A. American put by three methods.** PSOR on the implicit-Euler PDE, a CRR tree as the benchmark, and LSM for the path view. Note the *sign* of the deviation in each case — LSM must sit below the benchmark.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bsm_put(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return X*math.exp(-r*T)*N(-d2)-S*N(-d1)

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

S, X, T, r, sig = 100.0, 95.0, 0.5, 0.08, 0.30
BS_EURO = bsm_put(S, X, T, r, sig)

def american_psor(M, nt, Smax, omega=1.2):
    """Implicit Euler in time + projected SOR (the discrete complementarity solver)."""
    h = Smax/M; k = T/nt
    Sj = [j*h for j in range(M+1)]
    g = [max(X-Sj[j], 0.0) for j in range(M+1)]            # intrinsic value
    a=[0.0]*(M+1); b=[0.0]*(M+1); c=[0.0]*(M+1)
    for j in range(M+1):
        s2 = sig*sig*Sj[j]*Sj[j]
        a[j] = 0.5*s2/h**2-r*Sj[j]/(2*h); b[j] = -s2/h**2-r; c[j] = 0.5*s2/h**2+r*Sj[j]/(2*h)
    V = g[:]
    for n in range(nt):
        V0, VM = X*math.exp(-r*(n+1)*k), 0.0
        lo=[0.0]*(M-1); di=[0.0]*(M-1); up=[0.0]*(M-1); rh=[0.0]*(M-1)
        for j in range(1, M):
            lo[j-1]=-k*a[j]; di[j-1]=1.0-k*b[j]; up[j-1]=-k*c[j]; rh[j-1]=V[j]
        rh[0] += k*a[1]*V0                                  # Dirichlet at S=0: P(0)=X
        for _ in range(400):                                # projected SOR sweeps
            err = 0.0
            for j in range(1, M):
                z = (rh[j-1]-lo[j-1]*(V[j-1] if j > 1 else V0)-up[j-1]*(V[j+1] if j < M-1 else VM))/di[j-1]
                new = max(g[j], V[j]+omega*(z-V[j]))
                err = max(err, abs(new-V[j])); V[j] = new
            if err < 1e-10: break
        V[0], V[M] = V0, VM
    j = int(S/h); f = (S-j*h)/h
    return (1-f)*V[j]+f*V[j+1]

def american_put_crr(S, X, T, r, sig, n):                  # benchmark: backward induction
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u
    p = (math.exp(r*dt)-d)/(u-d)
    val = [max(X-S*u**(n-i)*d**i, 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        val = [max(math.exp(-r*dt)*(p*val[i]+(1-p)*val[i+1]), X-S*u**(j-i)*d**i) for i in range(j+1)]
    return val[0]

def lsm_american_put(S, X, T, r, sig, m, npaths, seed, deg=2):
    """Longstaff-Schwartz: regress the realised continuation value, exercise if intrinsic wins."""
    rng = random.Random(seed); dt = T/m
    cash = [0.0]*npaths; pathS = [[0.0]*(m+1) for _ in range(npaths)]
    for p in range(npaths):
        s_ = S
        for i in range(1, m+1):
            s_ *= math.exp((r-0.5*sig**2)*dt+sig*math.sqrt(dt)*rng.gauss(0, 1))
            pathS[p][i] = s_
        cash[p] = max(X-pathS[p][m], 0.0)
    for i in range(m-1, 0, -1):
        cash = [c*math.exp(-r*dt) for c in cash]     # discount every path one step
        x = [pathS[p][i] for p in range(npaths)]
        ex = [max(X-x[p], 0.0) for p in range(npaths)]
        idx = [p for p in range(npaths) if ex[p] > 0.0]
        if len(idx) < deg+1: continue
        A_ = [[x[p]**k for k in range(deg+1)] for p in idx]
        yv = [cash[p] for p in idx]
        AtA = [[sum(A_[t][a]*A_[t][b] for t in range(len(idx))) for b in range(deg+1)] for a in range(deg+1)]
        AtY = [sum(A_[t][a]*yv[t] for t in range(len(idx))) for a in range(deg+1)]
        for c in range(deg+1):                       # Gaussian elimination on the normal equations
            piv = max(range(c, deg+1), key=lambda rr: abs(AtA[rr][c]))
            AtA[c], AtA[piv] = AtA[piv], AtA[c]; AtY[c], AtY[piv] = AtY[piv], AtY[c]
            for rr in range(c+1, deg+1):
                f = AtA[rr][c]/AtA[c][c]
                for cc in range(c, deg+1): AtA[rr][cc] -= f*AtA[c][cc]
                AtY[rr] -= f*AtY[c]
        beta = [0.0]*(deg+1)
        for rr in range(deg, -1, -1):
            beta[rr] = (AtY[rr]-sum(AtA[rr][cc]*beta[cc] for cc in range(rr+1, deg+1)))/AtA[rr][rr]
        for p in idx:
            cont = sum(beta[k]*x[p]**k for k in range(deg+1))
            if ex[p] > cont: cash[p] = ex[p]                 # exercise now
    vals = [cash[p]*math.exp(-r*dt) for p in range(npaths)]
    return sum(vals)/npaths

print(f"European put (BSM)          = {BS_EURO:.4f}")
print(f"American put (CRR n=1000)   = {american_put_crr(S,X,T,r,sig,1000):.4f}   <- benchmark")
print(f"American put (PSOR  M=200)  = {american_psor(200, 200, 400.0):.4f}")
print(f"American put (PSOR  M=400)  = {american_psor(400, 400, 400.0):.4f}")
print(f"American put (PSOR  M=800)  = {american_psor(800, 800, 400.0):.4f}")
for m, np_ in ((50, 200000),):
    v = lsm_american_put(S, X, T, r, sig, m, np_, 5)
    print(f"American put (LSM m={m}, {np_:>6d} paths) = {v:.4f}")
```
```
European put (BSM)          = 4.4494
American put (CRR n=1000)   = 4.6921   <- benchmark
American put (PSOR  M=200)  = 4.6818
American put (PSOR  M=400)  = 4.6854
American put (PSOR  M=800)  = 4.6890
American put (LSM m=50, 200000 paths) = 4.6765
```

The PSOR values converge *upward* to the tree benchmark ($4.6818\to4.6854\to4.6890$ against $4.6921$) — implicit-Euler-in-time is $O(k)$ and the domain is truncated at $S_{\max}=400$, so the residual $0.003$ is exactly the discretisation error of pages 02/05. The LSM value $4.6765$ sits **below** the true price, as the low-bias theorem demands, with the early-exercise premium versus the European $4.4494$ equal to $4.6765-4.4494=0.2271$ (the benchmark's premium is $0.2427$).

**B. Multidimensional: ADI versus explicit on the 2-D heat equation.** ADI is unconditionally stable; the explicit scheme is not, and the *initial condition* decides whether the instability shows.

```python
import math, random

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

def ic(nx, ny, step):
    u = [[(1.0 if step else math.sin(math.pi*i/nx)*math.sin(math.pi*j/ny)) for j in range(ny+1)]
         for i in range(nx+1)]
    if step:                                  # zero Dirichlet boundary for the step datum
        for i in range(nx+1): u[i][0] = 0.0; u[i][ny] = 0.0
        for j in range(ny+1): u[0][j] = 0.0; u[nx][j] = 0.0
    return u

def adi_2d(nx, ny, nt, T=0.1, step=False):
    """Peaceman-Rachford: (1-(k/2)A_x)U* = (1+(k/2)A_y)U^n ; (1-(k/2)A_y)U^{n+1} = (1+(k/2)A_x)U*."""
    hx = 1.0/nx; hy = 1.0/ny; k = T/nt
    u = ic(nx, ny, step)
    for _ in range(nt):
        U = [row[:] for row in u]
        for i in range(1, nx):                    # leg 1: implicit in x
            lo=[0.0]*(ny-1); di=[0.0]*(ny-1); up=[0.0]*(ny-1); rh=[0.0]*(ny-1)
            for j in range(1, ny):
                lo[j-1]=-(k/2)/hx**2; di[j-1]=1+k/hx**2; up[j-1]=-(k/2)/hx**2
                rh[j-1]=U[i][j]+(k/2)*(U[i][j+1]-2*U[i][j]+U[i][j-1])/hy**2
            x = thomas(lo, di, up, rh)
            for j in range(1, ny): u[i][j] = x[j-1]
        W = [row[:] for row in u]
        for j in range(1, ny):                    # leg 2: implicit in y
            lo=[0.0]*(nx-1); di=[0.0]*(nx-1); up=[0.0]*(nx-1); rh=[0.0]*(nx-1)
            for i in range(1, nx):
                lo[i-1]=-(k/2)/hy**2; di[i-1]=1+k/hy**2; up[i-1]=-(k/2)/hy**2
                rh[i-1]=W[i][j]+(k/2)*(W[i+1][j]-2*W[i][j]+W[i-1][j])/hx**2
            x = thomas(lo, di, up, rh)
            for i in range(1, nx): u[i][j] = x[i-1]
    return u[nx//2][ny//2]

def explicit_2d(nx, ny, nt, T=0.1, step=False):
    hx = 1.0/nx; hy = 1.0/ny; k = T/nt
    lam1 = k/hx**2; lam2 = k/hy**2
    u = ic(nx, ny, step)
    for _ in range(nt):
        U = [row[:] for row in u]
        for i in range(1, nx):
            for j in range(1, ny):
                u[i][j] = U[i][j]+lam1*(U[i+1][j]-2*U[i][j]+U[i-1][j])+lam2*(U[i][j+1]-2*U[i][j]+U[i][j-1])
    return u[nx//2][ny//2]

exact2d = math.exp(-2*math.pi**2*0.1)
print(f"\n2-D heat, u0 = sin(pi x) sin(pi y), t = 0.1 (exact centre value = {exact2d:.6f}):")
for nx, nt in ((20, 40), (40, 160), (40, 40)):
    print(f"  ADI  nx={nx:3d} nt={nt:4d}: {adi_2d(nx, nx, nt):.6f}")
for nx, nt in ((20, 1600), (40, 6400)):
    lam = 2*(1.0/nt)/(1.0/nx)**2
    print(f"  expl nx={nx:3d} nt={nt:4d} (lam1+lam2={lam:.2f}, smooth IC): {explicit_2d(nx,nx,nt):.6f}")
print("  step initial condition u0=1 (all Fourier modes excited):")
for nx, nt in ((20, 1600), (20, 400), (20, 60)):
    lam = 2*(0.1/nt)/(1.0/nx)**2
    rho = 1-4*lam
    u = explicit_2d(nx, nx, nt, step=True)
    print(f"    expl  nx={nx:3d} nt={nt:4d}: lam1+lam2={lam:.3f}  rho_max={rho:+.2f}  centre={u: .4e}")
u = adi_2d(20, 20, 60, step=True)
print(f"    P-R ADI nx=20 nt=60 (same coarse steps): centre={u:.6f}   (unconditionally stable)")
```
```

2-D heat, u0 = sin(pi x) sin(pi y), t = 0.1 (exact centre value = 0.138911):
  ADI  nx= 20 nt=  40: 0.139462
  ADI  nx= 40 nt= 160: 0.139051
  ADI  nx= 40 nt=  40: 0.139038
  expl nx= 20 nt=1600 (lam1+lam2=0.50, smooth IC): 0.139306
  expl nx= 40 nt=6400 (lam1+lam2=0.50, smooth IC): 0.139010
  step initial condition u0=1 (all Fourier modes excited):
    expl  nx= 20 nt=1600: lam1+lam2=0.050  rho_max=+0.80  centre= 2.2484e-01
    expl  nx= 20 nt= 400: lam1+lam2=0.200  rho_max=+0.20  centre= 2.2403e-01
    expl  nx= 20 nt=  60: lam1+lam2=1.333  rho_max=-4.33  centre= 1.7270e+33
    P-R ADI nx=20 nt=60 (same coarse steps): centre=0.225107   (unconditionally stable)
```

ADI matches the exact centre value $0.138911$ to three decimals at $40\times40$ nodes with only $40$ time steps, and at $\Delta t=0.1/60$ — where the explicit amplification factor is $\rho_{\max}=-4.33$ — ADI still returns a bounded $0.225107$ against the explicit scheme's $1.73\times10^{33}$. The smooth-IC explicit runs are *stable but inaccurate at coarse steps* (the same phenomenon as page 02), and the step IC is what exposes the instability: the discrete Laplacian annihilates a constant, so high-frequency content is required to see $\rho$ in action.

**C. Quasi-Monte Carlo: Halton versus pseudo-random in 8 dimensions.** The integrand is an 8-fixing geometric Asian, so an exact closed form exists to measure both estimators against; randomised (shifted) Halton supplies the error bar.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

def halton(n, dim):
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    pts = []
    for i in range(1, n+1):
        p = []
        for b in primes[:dim]:
            f, r, k = 1.0, 0.0, i
            while k > 0:
                f /= b; r += f*(k % b); k //= b
            p.append(r)
        pts.append(p)
    return pts

def invnorm(p):
    lo, hi = -8.0, 8.0
    for _ in range(45):                      # bisection on the normal CDF (stdlib only)
        mid = 0.5*(lo+hi)
        if 0.5*(1.0+math.erf(mid/math.sqrt(2.0))) < p: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

def geo_asian_8d(u, m=8):
    dt = 1.0/m; logS = math.log(100.0); lsum = 0.0
    for i in range(m):
        logS += (0.05-0.5*0.04)*dt + 0.2*math.sqrt(dt)*invnorm(min(max(u[i], 1e-12), 1-1e-12))
        lsum += logS
    return math.exp(-0.05)*max(math.exp(lsum/m)-100.0, 0.0)

def geo_asian_closed_8d(m=8, S=100.0, X=100.0, T=1.0, r=0.05, sig=0.2):
    dt = T/m; ts = [(i+1)*dt for i in range(m)]
    drift = sum((r-0.5*sig**2)*ti for ti in ts)/m
    v = (sig*sig/(m*m))*sum(min(ts[i], ts[j]) for i in range(m) for j in range(m))
    mlog = math.log(S)+drift; EG = math.exp(mlog+0.5*v)
    d1 = (mlog-math.log(X)+v)/math.sqrt(v); d2 = d1-math.sqrt(v)
    return math.exp(-r*T)*(EG*N(d1)-X*N(d2))

ref = geo_asian_closed_8d()
rng = random.Random(4)
NREP, NPTS = 15, 2000
mc_vals = [sum(geo_asian_8d([rng.random() for _ in range(8)]) for _ in range(NPTS))/NPTS for _ in range(NREP)]
qmc_vals = []
pts = halton(NPTS, 8)
for _ in range(NREP):
    shift = [rng.random() for _ in range(8)]
    qmc_vals.append(sum(geo_asian_8d([(p[d]+shift[d]) % 1.0 for d in range(8)]) for p in pts)/NPTS)
plain_halton = sum(geo_asian_8d(p) for p in pts)/NPTS
def rmse(v):
    m_ = sum(v)/len(v); return math.sqrt(sum((x-m_)**2 for x in v)/len(v))
print(f"\n8-D geometric Asian, exact closed form = {ref:.4f}")
print(f"  plain MC      ({NREP} x {NPTS}): mean = {sum(mc_vals)/len(mc_vals):.4f}   RMSE = {rmse(mc_vals):.4f}")
print(f"  shifted Halton({NREP} x {NPTS}): mean = {sum(qmc_vals)/len(qmc_vals):.4f}   RMSE = {rmse(qmc_vals):.4f}")
print(f"  plain Halton  (      {NPTS}): value = {plain_halton:.4f}   error = {plain_halton-ref:+.4f}")
print(f"  variance reduction from QMC = {(rmse(mc_vals)/rmse(qmc_vals))**2:.1f}x")
```
```

8-D geometric Asian, exact closed form = 6.1377
  plain MC      (15 x 2000): mean = 6.1762   RMSE = 0.1692
  shifted Halton(15 x 2000): mean = 6.1416   RMSE = 0.0302
  plain Halton  (      2000): value = 6.0202   error = -0.1174
  variance reduction from QMC = 31.4x
```

At 2,000 points in 8 dimensions, low-discrepancy points cut the RMSE from $0.1692$ to $0.0302$ — a $31.4\times$ variance reduction, roughly seven times the antithetic device of page 04 ($31.4/4.41$) and obtained at about a twentieth of the path count. Note also the honest counter-example in the same output: the *unrandomised* Halton value $6.0202$ is off by $-0.1174$, about four times the randomised RMSE. That is the **plateau / false-convergence** trap of Glasserman §5.5 — never use unrandomised QMC without skipping a burn-in and checking stability across $n$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **American pricing is a free-boundary problem, not a European formula.** Applying the closed form to an American put understates it by the early-exercise premium ($4.6921$ vs $4.4494$ — a $5.5\%$ error here). Every route must enforce $P\ge g$: projection (PSOR), penalty, front fixing, or an explicit exercise check (tree/LSM).
2. **The two Monte Carlo American estimators have opposite biases.** LSM is low-biased ($4.6765$ below $4.6921$) and the regression DP is high-biased; quoting one as "the price" without a duality upper bound hides which way the error points.
3. **ADI dies on cross derivatives.** The correlated multi-asset PDE contains $\rho\sigma_1\sigma_2S_1S_2\,\partial^2V/\partial S_1\partial S_2$; standard ADI is not unconditionally stable there (Duffy eq. 19.37) — use Yanenko splitting with the mixed term treated explicitly, or an iterative (Rothe + SOR/GS) solve.
4. **The three-leg ADI in 3-D is not stable.** Duffy eq. 19.34 is explicit: use Douglas–Rachford or simple splitting; a naive generalisation of the 2-D result is a silent blow-up.
5. **QMC requires finite variation and is not a black box.** Koksma–Hlawka's bound is useless when $V_{HK}(f)=\infty$ (barrier/indicator payoffs, non-axis-aligned regions), and unrandomised points can plateau at a wrong value (the $-0.1174$ above). Fix: smooth the integrand, use effective-dimension reduction (Brownian bridge / principal components for Gaussian vectors), and randomise for error bars.
6. **Grid methods do not scale in dimension.** FDM costs $O(N^d)$ memory; the practitioner's rule (Duffy Ch 24) is $1$–$3$ factors for FD/FEM, and Monte Carlo/meshless beyond. The boundary between the two families is therefore set by *dimension*, not by accuracy.

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering* — Ch 19 (Peaceman–Rachford 19.7, growth factors 19.5–19.6, 3-D caution 19.34, mixed derivatives 19.37, Douglas–Rachford 19.35), Ch 20–21 (Yanenko splitting 20.8–20.9, IMEX 21.19–21.21, compound/chooser systems), Ch 24 (multi-asset PDE, Rothe + SOR/GS), Ch 26 (free/moving boundaries, Stefan analogy, smooth pasting 26.8), Ch 27 (front fixing/Landau 27.1–27.36), Ch 28 (penalty 28.15/28.17, Thm 28.2–28.3), Ch 29 (variational inequality, PSOR 29.11, Thm 29.1).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering* — Ch 8 §8.2–8.6 (parametric stopping rules, stochastic mesh, LR mesh weights, regression/LSM 8.46–8.52, the high/low bias split), §8.7 (duality 8.58–8.65, nested simulation), Ch 5 (discrepancy, Koksma–Hlawka 5.10, Halton/Faure/Sobol' 5.14–5.26, randomised QMC 5.32, finance setting 5.33–5.34 and the plateau trap), Ch 7 (pathwise vs likelihood-ratio Greeks, 7.15–7.45).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.4 (alternative tree construction incl. trinomial $u=e^{\sigma\sqrt{3\Delta t}}$), §21.7 (variance reduction incl. quasi-random sequences), §21.8 (finite differences, early exercise from the grid).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.2 (American put $4.692$ at $n=1000$ — the benchmark used above), §4.5 (trinomial: European $13.1752$ vs BSM $13.1744$), Ch 3 (BAW and Bjerksund–Stensland analytic approximations as fast American alternatives).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward topics: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (whose 2-D PDE needs ADI/splitting) · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure Models]] (HJM/LMM simulation, Ch 3.6–3.7 of Glasserman)
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Advanced Extensions]] (American early exercise and jump-diffusion MC)
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]

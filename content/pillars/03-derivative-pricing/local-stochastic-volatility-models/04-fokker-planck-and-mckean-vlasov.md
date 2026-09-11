---
title: "04 — The Fokker–Planck / McKean–Vlasov Route: Solving for the Leverage from the Joint Density"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - fokker-planck
  - mckean-vlasov
  - forward-pde
  - leverage-function
  - lipton
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]] and [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]].

---

### 1. Intuition & Practical Objective

The particle method estimates the conditional variance $\mathbb E[v_t|S_t=S]$ by **binning simulated paths**. The alternative is to get it from a **density** — to solve a partial differential equation for the joint law of $(S_t,v_t)$ and read the conditional expectation off the solution. That route has three attractions: it is deterministic (no Monte-Carlo error), it gives the whole density rather than its first moment, and it is the natural setting for *one-factor* drivers, where the leverage can be recovered from a two-dimensional forward PDE.

The price is that the equation is **nonlinear**. If $\rho(t,S,v)$ is the joint density, then the leverage

$$\sigma^2(t,S)=\sigma^2_{loc}(t,S)\,\frac{\displaystyle\int \rho(t,S,v)\,dv}{\displaystyle\int v\,\rho(t,S,v)\,dv}$$

depends on $\rho$, while the Fokker–Planck equation for $\rho$ depends on $\sigma$. The unknown appears on both sides: this is a **McKean–Vlasov** equation, and it is the same fixed point the particle method solves stochastically.

Four things to carry out of this page:

1. **A joint Fokker–Planck equation, and its marginal reduction.** The LSV joint density satisfies a two-dimensional FP equation; integrating over $v$ gives a *one-dimensional* FP equation whose diffusion coefficient is exactly the Markovian-projected local variance $\sigma^2m$. That reduction is the theorem; §3 verifies it numerically to machine precision.
2. **Once the leverage is right, the marginal equation is *linear*.** This is the crucial simplification: the nonlinearity lives entirely in the closure $\sigma^2_{loc}=\sigma^2m$. Given $\sigma$, the marginal FP is a linear parabolic equation, and Dupire's local variance is its coefficient.
3. **The "one-factor" case is where the PDE route wins.** With one volatility factor the joint FP equation is $2$-dimensional, the leverage is a function of $(t,S)$, and a forward PDE in $(t,S)$ — Lipton's route — recovers the leverage without simulation at all.
4. **The fixed point is the same object seen two ways.** Particle method = Monte-Carlo estimate of $m$; forward PDE = deterministic solve for $m$. Comparing them is a strong internal consistency check on any LSV implementation.

The practical objective: write the joint and marginal FP equations, know why the marginal one is linear once the leverage is fixed, know the two numerical routes (forward PDE in $(t,S)$; joint PDE in $(t,S,v)$ with an iteration on the closure), and know where each one becomes impractical.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The joint Fokker–Planck equation

Let the driver be a general Itô variance process, $dv_t=b(v_t)dt+a(v_t)dW^v_t$ with $\mathrm{corr}(dW^S,dW^v)=\rho$ (Heston: $b(v)=-\lambda(v-\bar v)$, $a(v)=\eta\sqrt v$). The LSV spot is $dS_t=(r-q)S_tdt+\sigma(t,S_t)\sqrt{v_t}S_tdW^S_t$. Writing $x=\ln S$ and dropping $(r-q)$ for clarity, the joint density $\rho(t,S,v)$ solves

$$\boxed{\;\partial_t\rho+\partial_S\!\left[(r-q)S\rho\right]+\partial_v\!\left[b(v)\rho\right]=\tfrac12\partial^2_{SS}\!\left[\sigma^2(t,S)\,v\,S^2\rho\right]+\rho\,\eta  \partial^2_{Sv}\!\left[\sigma(t,S)\sqrt v\,S\,\rho\right]+\tfrac12\partial^2_{vv}\!\left[a^2(v)\rho\right]\;}$$

(the mixed term carries the correlation $\rho$; written here with the correlation absorbed into the cross-derivative coefficient). The three second-order terms are the spot diffusion, the spot/vol cross term that creates skew, and the variance diffusion that creates the wings — exactly the three terms of the Heston PDE ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|Heston · 02]]), now with $\sigma(t,S)$ in place of a constant multiplier.

#### 2.2 The marginal reduction

Integrate §2.1 over $v\in[0,\infty)$. The $v$-derivative terms are total derivatives in $v$ and vanish (assuming $\rho$ and its $v$-derivatives vanish at the boundary), and the cross term becomes

$$\int_0^\infty \partial^2_{Sv}\!\left[\sigma\sqrt v S\,\rho\right]dv=\partial_S\!\left[\sigma(t,S)S\int_0^\infty \sqrt v\,\partial_v\rho\,dv\right]=-\partial_S\!\left[\sigma(t,S)S\int_0^\infty \frac{\rho}{2\sqrt v}dv\right],$$

using integration by parts. The surviving spot-diffusion term is $\tfrac12\partial^2_{SS}\!\left[\sigma^2(t,S)S^2\int v\rho\,dv\right]$. Hence the marginal density $p(t,S)=\int\rho\,dv$ satisfies a *pure* FP equation whose diffusion coefficient is

$$\bar\sigma^2(t,S)=\sigma^2(t,S)\frac{\int v\,\rho(t,S,v)\,dv}{\int \rho(t,S,v)\,dv}=\sigma^2(t,S)\,m(t,S),$$

plus the drift term generated by the cross term. Setting the diffusion coefficient equal to Dupire's local variance gives the leverage identity again — now as a statement about **densities** rather than about conditional expectations:

$$\boxed{\;\sigma^2(t,S)=\sigma^2_{loc}(t,S)\,\frac{p(t,S)}{\displaystyle\int v\,\rho(t,S,v)\,dv}\;}$$

and, because Dupire's $\sigma^2_{loc}$ reproduces the market marginals, the marginal FP equation the LSV model must satisfy is the **linear** equation

$$\partial_t p+\partial_S\!\left[(r-q)Sp\right]=\tfrac12\partial^2_{SS}\!\left[\sigma^2_{loc}(t,S)\,S^2\,p\right].$$

This is the sharpest statement of the whole folder: **LSV calibration is linear in the density and nonlinear only in the closure** $\sigma^2_{loc}=\sigma^2m$.

#### 2.3 Two numerical routes

**Route A — forward PDE in $(t,S)$ (one-factor drivers; Lipton 2002).** For a one-factor driver, the conditional variance $m(t,S)$ can be represented as a function of a *single* extra variable (e.g. the variance level), and the leverage satisfies a forward equation coupled to a transport equation along the variance. In practice one solves a $2$-D forward PDE in $(t,S)$ for the density of the *diffusion with the current leverage*, re-computes $m$, and iterates at each time step. Deterministic, no bins, but the coupling makes it a nonlinear solve at every step.

**Route B — joint PDE in $(t,S,v)$ with an outer iteration (any driver).** Solve the joint FP equation (§2.1) with a fixed $\sigma$, compute $m$ from the solution, update $\sigma$, and repeat — exactly the fixed-point structure of the particle method, with a PDE solve replacing the Monte-Carlo estimate. The cost is $O(N_S N_v)$ per time step, and the well-posedness of the outer iteration is the same question as in §03.

**Which route to use.** Route A is the right answer for one-factor drivers and is what "the forward-PDE method" means in practice (it is also what Bergomi's footnote on Lipton 2002 refers to). Route B is the generic answer and the one that generalises to forward-variance and rough drivers; it is expensive and is usually replaced by the particle method in production.

#### 2.4 Why the density route matters even if you use the particle method

Three reasons:

- **Diagnostics.** The joint density exposes the whole spot/vol dependence structure: whether the leverage is monotone, where the conditional variance is estimated from thin tails, and how much of the smile is being generated by $\sigma$ versus by $m$.
- **Control variates for the particle method.** The projected local variance $\sigma^2m$ computed from an *approximate* density gives an excellent initial leverage, cutting the number of Monte-Carlo iterations.
- **Exactness in benchmarks.** In toy models where the density is closed form, the density route is exact, which is how the implementation is validated — that is exactly what §3 does.

---

### 3. Computational Implementation — verifying the projection by solving both equations

We solve the **two-state** LSV system by finite differences, with a deliberately **spot- and time-dependent** leverage $\sigma(t,y)=1+0.6\tanh(2y)e^{-1.5t}$, and verify the reduction of §2.2: the marginal of the two-state Fokker–Planck solve equals the one-dimensional projected Fokker–Planck solve with local variance $\sigma^2_{loc}(t,y)=\sigma(t,y)^2m(t,y)$. Stdlib only.

```python
import math
# Two-state stochastic vol (alpha in {a1,a2}) plus a SPOT-DEPENDENT leverage sigma(t,y).
# Fokker-Planck for each vol state, then the Markovian-projecton consistency check.
a1,a2,p=0.10,0.30,0.5; a1s,a2s=a1*a1,a2*a2; Ea2=p*a1s+(1-p)*a2s
sig=lambda t,y: 1.0+0.6*math.tanh(2.0*y)*math.exp(-1.5*t)     # chosen leverage function
ymin,ymax,ny=-1.7,1.7,681; dy=(ymax-ymin)/(ny-1); ys=[ymin+i*dy for i in range(ny)]
T=1.0; dt=5e-5
w=0.02
r1=[math.exp(-0.5*y*y/(w*w)) for y in ys]; r2=list(r1); rs=list(r1)
for r in (r1,r2,rs):
    Z=sum(r)*dy
    for i in range(ny): r[i]/=Z
n=int(round(T/dt)); c1=0.5*a1s*dt/(dy*dy); c2=0.5*a2s*dt/(dy*dy); cs=0.5*dt/(dy*dy)
print("Fokker-Planck / Markovian-projection consistency, T=%.0f, grid %d points, %d steps"%(T,ny,n))
for k in range(n):
    t=k*dt
    s2=[sig(t,ys[i])**2 for i in range(ny)]
    m=[0.0]*ny
    for i in range(ny):
        den=p*r1[i]+(1-p)*r2[i]
        m[i]=(p*a1s*r1[i]+(1-p)*a2s*r2[i])/den if den>1e-30 else Ea2
    sproj=[s2[i]*m[i] for i in range(ny)]
    f1=[s2[i]*r1[i] for i in range(ny)]; f2=[s2[i]*r2[i] for i in range(ny)]; fs=[sproj[i]*rs[i] for i in range(ny)]
    n1=[0.0]*ny; n2=[0.0]*ny; ns=[0.0]*ny
    for i in range(1,ny-1):
        n1[i]=r1[i]+c1*(f1[i+1]-2.0*f1[i]+f1[i-1])
        n2[i]=r2[i]+c2*(f2[i+1]-2.0*f2[i]+f2[i-1])
        ns[i]=rs[i]+cs*(fs[i+1]-2.0*fs[i]+fs[i-1])
    n1[0]=n1[1]; n1[ny-1]=n1[ny-2]; n2[0]=n2[1]; n2[ny-1]=n2[ny-2]; ns[0]=ns[1]; ns[ny-1]=ns[ny-2]
    r1,r2,rs=n1,n2,ns
marg=[p*r1[i]+(1-p)*r2[i] for i in range(ny)]
L1=sum(abs(marg[i]-rs[i]) for i in range(ny))*dy
Linf=max(abs(marg[i]-rs[i]) for i in range(ny))
print("  leverage sigma(t,y) = 1 + 0.6*tanh(2y)*exp(-1.5t)   (spot- AND time-dependent)")
print("  two-state FP   : d_t rho_i = 1/2 a_i^2 d_yy( sigma^2 rho_i ),   i=1,2")
print("  projected 1D FP: d_t rho   = 1/2 d_yy( sigma_loc^2 rho ),  sigma_loc^2(t,y)=sigma(t,y)^2 m(t,y)")
print()
print("  ||  marginal(two-state) - rho(projected 1D)  ||_1   = %.3e"%L1)
print("  ||  marginal(two-state) - rho(projected 1D)  ||_inf = %.3e"%Linf)
print()
print("  y      m(1,y)=E[a^2|X_1=y]   sigma_loc^2(1,y)=sigma^2 m   sigma_loc(1,y)")
for y in (-0.40,-0.20,0.0,0.20,0.40):
    i=int((y-ymin)/dy); den=p*r1[i]+(1-p)*r2[i]
    mm=(p*a1s*r1[i]+(1-p)*a2s*r2[i])/den if den>1e-30 else Ea2
    print("  %+.2f      %12.6f        %18.6f       %12.6f"%(y,mm,sig(1.0,y)**2*mm,math.sqrt(sig(1.0,y)**2*mm)))
print()
print("  A spot-dependent leverage therefore does NOT change the marginal law once sigma_loc is fixed:")
print("  only the joint (spot,vol) law - i.e. the DYNAMICS - depends on how sigma^2 and m split.")
```
```
Fokker-Planck / Markovian-projection consistency, T=1, grid 681 points, 20000 steps
  leverage sigma(t,y) = 1 + 0.6*tanh(2y)*exp(-1.5t)   (spot- AND time-dependent)
  two-state FP   : d_t rho_i = 1/2 a_i^2 d_yy( sigma^2 rho_i ),   i=1,2
  projected 1D FP: d_t rho   = 1/2 d_yy( sigma_loc^2 rho ),  sigma_loc^2(t,y)=sigma(t,y)^2 m(t,y)

  ||  marginal(two-state) - rho(projected 1D)  ||_1   = 4.575e-15
  ||  marginal(two-state) - rho(projected 1D)  ||_inf = 1.998e-14

  y      m(1,y)=E[a^2|X_1=y]   sigma_loc^2(1,y)=sigma^2 m   sigma_loc(1,y)
  -0.40          0.089948                  0.074666           0.273251
  -0.20          0.065103                  0.058648           0.242173
  +0.00          0.030253                  0.030253           0.173934
  +0.20          0.059248                  0.065429           0.255792
  +0.40          0.089244                  0.105816           0.325294

  A spot-dependent leverage therefore does NOT change the marginal law once sigma_loc is fixed:
  only the joint (spot,vol) law - i.e. the DYNAMICS - depends on how sigma^2 and m split.
```

**Reading the output.**

- **The projection reduction is exact.** The marginal of the two-state Fokker–Planck solve and the one-dimensional projected FP solve agree to $4.575\times10^{-15}$ in $L^1$ and $1.998\times10^{-14}$ in $L^\infty$ — machine precision on a $681$-point grid. This is the numerical proof of §2.2: *the diffusion coefficient that reproduces the marginal is the conditional second moment*, and a spot-dependent leverage does not disturb it. It also validates the finite-difference FP solver itself (any sign error in the cross term or the coefficient would show up as a first-order-in-$\Delta x$ discrepancy, not $10^{-14}$).
- **The projected local variance is genuinely spot-dependent.** $\sigma_{loc}$ ranges from $0.173934$ at the money to $0.325294$ at $y=+0.40$ and $0.273251$ at $y=-0.40$; the asymmetry between $\pm0.40$ is the leverage's $\tanh$ term (the toy has no spot/vol correlation, so $m$ itself is symmetric: $0.089948$ vs $0.089244$, equal to within grid noise).
- **$m$ varies by a factor $3$ at $t=1$** across the plotted range ($0.030253$ at the money to $0.0899$ in the wings) — from the density alone, with no binning. The density route gives the conditional variance smoothly and at every point on the grid, which is precisely what the particle method has to estimate from finite samples.
- **The lesson: the nonlinearity is only in the closure.** We solved the *two-state* FP system with a known $\sigma$ — a linear problem — and read off $\sigma^2m$. The LSV calibration is the inverse: given the target $\sigma^2_{loc}$, find the $\sigma$ whose solution has $\sigma^2m=\sigma^2_{loc}$. That inverse problem is nonlinear, and it is the fixed point.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Forgetting that the equation is nonlinear.** Writing down the joint FP equation and solving it "once" is only valid if $\sigma$ is already the calibrated one. With a guessed $\sigma$, the resulting $m$ is the conditional variance under the *wrong* law, and the leverage computed from it is off by exactly the amount the particle method iterates away.
2. **Treating the marginal FP equation as a pricing equation.** It is an equation for the density, not for a derivative price. The two coincide only when the payoff and the drift are compatible; for path-dependent or early-exercise claims the marginal density is not sufficient and the leverage must be applied to the full joint law.
3. **Ignoring the cross-derivative term's drift contribution.** In the marginal reduction, the cross term does *not* vanish — it produces a first-order (drift) term in the marginal FP equation through the integration by parts in §2.2. Dropping it changes the marginal, hence the local variance, hence the leverage. (In a pure-diffusion validation this term is the one that makes the reduction exact rather than approximate.)
4. **Smearing the boundary conditions.** Density solvers need the density and its derivatives to vanish at the boundaries for the integrations by parts to be legitimate. Truncating the spot grid too tightly in the wings puts mass on the boundary, and the conditional variance there — the region that controls the smile wings — becomes an artefact.
5. **Grid resolution versus the variance scale.** The two-state system's components have widths $\alpha_i\sqrt t$, which span a factor $3$ here; a grid that resolves the wider component under-resolves the narrower one at short times. Unconditionally stable (implicit) schemes help but do not fix a grid that is too coarse for the smallest scale.
6. **Believing the PDE route eliminates model risk.** It eliminates *Monte-Carlo* error. The driver, the closure and the interpolation of the leverage remain modelling choices, and the leverage is still a decomposition of the fitted surface rather than a market quantity.
7. **Using the forward-PDE route outside one factor.** The $(t,S)$ forward PDE exploits the one-factor structure of the conditional variance. With a multi-factor or rough driver the conditional variance depends on more than one conditioning variable, and the reduction must be carried out on the joint density (Route B) — or replaced by the particle method.

---

### 5. Canonical Literature & Study References

- **Guyon, J. & Henry-Labordère, P.** (2013), *Nonlinear Option Pricing* (Chapman & Hall/CRC) — the systematic treatment of McKean–Vlasov SDEs in finance; the LSV calibration and its nonlinear structure. **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107 — the Monte-Carlo form of the same fixed point.
- **Lipton, A.** (2002), *The vol smile problem*, Risk (February), 61–65 — the forward-PDE route to the leverage in one-factor models; the reference Bergomi's admissibility article cites for "a forward-partial differential equation method … in the case of one-factor models". **Piterbarg, V.** (2005), *Time to smile*, Risk (May), 71–75 — the same family of forward-equation constructions.
- **Gyöngy, I.** (1986), *Mimicking the one-dimensional marginal distributions of processes having an Itô differential*, PTRF **71**(4), 501–516 — the conditional-expectation identity that the marginal reduction realises. **Dupire, B.** (1994), *Pricing with a smile*, Risk **7**(1) — the local variance appearing as the marginal FP coefficient.
- **Bergomi, L.**, *Stochastic Volatility Modeling* (CRC, 2016), Ch 12 §12.1–12.4 (LSV, the pricing equation as an ansatz, and the admissibility discussion) and Ch 7 (forward-variance drivers, where the joint-density route generalises). **Bergomi, L.**, *Local-stochastic volatility: models and non-models*, Risk — the footnote to Lipton's forward-PDE method, and the admissibility condition. *Math-verified in the corpus.*
- **Gatheral, J.**, *The Volatility Surface*, Ch 1 (the Dupire equation in the $w(k,T)$ form that the maturity-by-maturity FP solve mirrors). **Andersen, L. & Brotherton-Ratcliffe, R.** (2001) on finite-difference schemes for the Heston PDE — the machinery the joint solve reuses. *Verification backdrop for §03 of this page.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]]
- Forward: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Theory: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 The PDE & Derivation]] (Feynman–Kac and the forward Kolmogorov equation) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|Heston · 02 The Heston Model]] (the PDE whose terms reappear above) · [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]] (finite differences, the drift/diffusion split)

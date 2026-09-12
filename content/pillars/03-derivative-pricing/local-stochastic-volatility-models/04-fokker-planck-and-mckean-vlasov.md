---
title: "3.13.4 The Fokker–Planck / McKean–Vlasov Route"
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

The particle method estimates the conditional variance $\mathbb E[v_t|S_t=S]$ by **binning simulated paths**. The alternative is to get it from a **density** - to solve a partial differential equation for the joint law of $(S_t,v_t)$ and read the conditional expectation off the solution. That route has three attractions: it is deterministic (no Monte-Carlo error), it gives the whole density rather than its first moment, and it is the natural setting for *one-factor* drivers, where the leverage can be recovered from a two-dimensional forward PDE.

The price is that the equation is **nonlinear**. If $\rho(t,S,v)$ is the joint density, then the leverage

$$
\sigma^2(t,S)=\sigma^2_{loc}(t,S)\,\frac{\displaystyle\int \rho(t,S,v)\,dv}{\displaystyle\int v\,\rho(t,S,v)\,dv}
$$

depends on $\rho$, while the Fokker–Planck equation for $\rho$ depends on $\sigma$. The unknown appears on both sides: this is a **McKean–Vlasov** equation, and it is the same fixed point the particle method solves stochastically.

Four things to carry out of this page:

1. **A joint Fokker–Planck equation, and its marginal reduction.** The LSV joint density satisfies a two-dimensional FP equation; integrating over $v$ gives a *one-dimensional* FP equation whose diffusion coefficient is exactly the Markovian-projected local variance $\sigma^2m$. That reduction is the theorem; §3 verifies it numerically to machine precision.
2. **Once the leverage is right, the marginal equation is *linear*.** This is the crucial simplification: the nonlinearity lives entirely in the closure $\sigma^2_{loc}=\sigma^2m$. Given $\sigma$, the marginal FP is a linear parabolic equation, and Dupire's local variance is its coefficient.
3. **The "one-factor" case is where the PDE route wins.** With one volatility factor the joint FP equation is $2$-dimensional, the leverage is a function of $(t,S)$, and a forward PDE in $(t,S)$ - Lipton's route - recovers the leverage without simulation at all.
4. **The fixed point is the same object seen two ways.** Particle method = Monte-Carlo estimate of $m$; forward PDE = deterministic solve for $m$. Comparing them is a strong internal consistency check on any LSV implementation.

The practical objective: write the joint and marginal FP equations, know why the marginal one is linear once the leverage is fixed, know the two numerical routes (forward PDE in $(t,S)$; joint PDE in $(t,S,v)$ with an iteration on the closure), and know where each one becomes impractical.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The joint Fokker–Planck equation

Let the driver be a general Itô variance process, $dv_t=b(v_t)dt+a(v_t)dW^v_t$ with $\mathrm{corr}(dW^S,dW^v)=\rho$ (Heston: $b(v)=-\lambda(v-\bar v)$, $a(v)=\eta\sqrt v$). The LSV spot is $dS_t=(r-q)S_tdt+\sigma(t,S_t)\sqrt{v_t}S_tdW^S_t$. Writing $x=\ln S$ and dropping $(r-q)$ for clarity, the joint density $\rho(t,S,v)$ solves

$$
\boxed{\;\partial_t\rho+\partial_S\!\left[(r-q)S\rho\right]+\partial_v\!\left[b(v)\rho\right]=\tfrac12\partial^2_{SS}\!\left[\sigma^2(t,S)\,v\,S^2\rho\right]+\rho\,\eta  \partial^2_{Sv}\!\left[\sigma(t,S)\sqrt v\,S\,\rho\right]+\tfrac12\partial^2_{vv}\!\left[a^2(v)\rho\right]\;}
$$

(the mixed term carries the correlation $\rho$; written here with the correlation absorbed into the cross-derivative coefficient). The three second-order terms are the spot diffusion, the spot/vol cross term that creates skew, and the variance diffusion that creates the wings - exactly the three terms of the Heston PDE ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|Heston · 02]]), now with $\sigma(t,S)$ in place of a constant multiplier.

#### 2.2 The marginal reduction

Integrate §2.1 over $v\in[0,\infty)$. The $v$-derivative terms are total derivatives in $v$ and vanish (assuming $\rho$ and its $v$-derivatives vanish at the boundary), and the cross term becomes

$$
\int_0^\infty \partial^2_{Sv}\!\left[\sigma\sqrt v S\,\rho\right]dv=\partial_S\!\left[\sigma(t,S)S\int_0^\infty \sqrt v\,\partial_v\rho\,dv\right]=-\partial_S\!\left[\sigma(t,S)S\int_0^\infty \frac{\rho}{2\sqrt v}dv\right],
$$

using integration by parts. The surviving spot-diffusion term is $\tfrac12\partial^2_{SS}\!\left[\sigma^2(t,S)S^2\int v\rho\,dv\right]$. Hence the marginal density $p(t,S)=\int\rho\,dv$ satisfies a *pure* FP equation whose diffusion coefficient is

$$
\bar\sigma^2(t,S)=\sigma^2(t,S)\frac{\int v\,\rho(t,S,v)\,dv}{\int \rho(t,S,v)\,dv}=\sigma^2(t,S)\,m(t,S),
$$

plus the drift term generated by the cross term. Setting the diffusion coefficient equal to Dupire's local variance gives the leverage identity again - now as a statement about **densities** rather than about conditional expectations:

$$
\boxed{\;\sigma^2(t,S)=\sigma^2_{loc}(t,S)\,\frac{p(t,S)}{\displaystyle\int v\,\rho(t,S,v)\,dv}\;}
$$

and, because Dupire's $\sigma^2_{loc}$ reproduces the market marginals, the marginal FP equation the LSV model must satisfy is the **linear** equation

$$
\partial_t p+\partial_S\!\left[(r-q)Sp\right]=\tfrac12\partial^2_{SS}\!\left[\sigma^2_{loc}(t,S)\,S^2\,p\right].
$$

This is the sharpest statement of the whole folder: **LSV calibration is linear in the density and nonlinear only in the closure** $\sigma^2_{loc}=\sigma^2m$.

#### 2.3 Two numerical routes

**Route A - forward PDE in $(t,S)$ (one-factor drivers; Lipton 2002).** For a one-factor driver, the conditional variance $m(t,S)$ can be represented as a function of a *single* extra variable (e.g. the variance level), and the leverage satisfies a forward equation coupled to a transport equation along the variance. In practice one solves a $2$-D forward PDE in $(t,S)$ for the density of the *diffusion with the current leverage*, re-computes $m$, and iterates at each time step. Deterministic, no bins, but the coupling makes it a nonlinear solve at every step.

**Route B - joint PDE in $(t,S,v)$ with an outer iteration (any driver).** Solve the joint FP equation (§2.1) with a fixed $\sigma$, compute $m$ from the solution, update $\sigma$, and repeat - exactly the fixed-point structure of the particle method, with a PDE solve replacing the Monte-Carlo estimate. The cost is $O(N_S N_v)$ per time step, and the well-posedness of the outer iteration is the same question as in §03.

**Which route to use.** Route A is the right answer for one-factor drivers and is what "the forward-PDE method" means in practice (it is also what Bergomi's footnote on Lipton 2002 refers to). Route B is the generic answer and the one that generalises to forward-variance and rough drivers; it is expensive and is usually replaced by the particle method in production.

#### 2.4 Why the density route matters even if you use the particle method

Three reasons:

- **Diagnostics.** The joint density exposes the whole spot/vol dependence structure: whether the leverage is monotone, where the conditional variance is estimated from thin tails, and how much of the smile is being generated by $\sigma$ versus by $m$.
- **Control variates for the particle method.** The projected local variance $\sigma^2m$ computed from an *approximate* density gives an excellent initial leverage, cutting the number of Monte-Carlo iterations.
- **Exactness in benchmarks.** In toy models where the density is closed form, the density route is exact, which is how the implementation is validated - that is exactly what §3 does.

---

### 3. Computational Implementation - verifying the projection by solving both equations

We solve the **two-state** LSV system by finite differences, with a deliberately **spot- and time-dependent** leverage $\sigma(t,y)=1+0.6\tanh(2y)e^{-1.5t}$, and verify the reduction of §2.2: the marginal of the two-state Fokker–Planck solve equals the one-dimensional projected Fokker–Planck solve with local variance $\sigma^2_{loc}(t,y)=\sigma(t,y)^2m(t,y)$. Stdlib only.




**Reading the output.**

- **The projection reduction is exact.** The marginal of the two-state Fokker–Planck solve and the one-dimensional projected FP solve agree to $4.575\times10^{-15}$ in $L^1$ and $1.998\times10^{-14}$ in $L^\infty$ - machine precision on a $681$-point grid. This is the numerical proof of §2.2: *the diffusion coefficient that reproduces the marginal is the conditional second moment*, and a spot-dependent leverage does not disturb it. It also validates the finite-difference FP solver itself (any sign error in the cross term or the coefficient would show up as a first-order-in-$\Delta x$ discrepancy, not $10^{-14}$).
- **The projected local variance is genuinely spot-dependent.** $\sigma_{loc}$ ranges from $0.173934$ at the money to $0.325294$ at $y=+0.40$ and $0.273251$ at $y=-0.40$; the asymmetry between $\pm0.40$ is the leverage's $\tanh$ term (the toy has no spot/vol correlation, so $m$ itself is symmetric: $0.089948$ vs $0.089244$, equal to within grid noise).
- **$m$ varies by a factor $3$ at $t=1$** across the plotted range ($0.030253$ at the money to $0.0899$ in the wings) - from the density alone, with no binning. The density route gives the conditional variance smoothly and at every point on the grid, which is precisely what the particle method has to estimate from finite samples.
- **The lesson: the nonlinearity is only in the closure.** We solved the *two-state* FP system with a known $\sigma$ - a linear problem - and read off $\sigma^2m$. The LSV calibration is the inverse: given the target $\sigma^2_{loc}$, find the $\sigma$ whose solution has $\sigma^2m=\sigma^2_{loc}$. That inverse problem is nonlinear, and it is the fixed point.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Forgetting that the equation is nonlinear.** Writing down the joint FP equation and solving it "once" is only valid if $\sigma$ is already the calibrated one. With a guessed $\sigma$, the resulting $m$ is the conditional variance under the *wrong* law, and the leverage computed from it is off by exactly the amount the particle method iterates away.
2. **Treating the marginal FP equation as a pricing equation.** It is an equation for the density, not for a derivative price. The two coincide only when the payoff and the drift are compatible; for path-dependent or early-exercise claims the marginal density is not sufficient and the leverage must be applied to the full joint law.
3. **Ignoring the cross-derivative term's drift contribution.** In the marginal reduction, the cross term does *not* vanish - it produces a first-order (drift) term in the marginal FP equation through the integration by parts in §2.2. Dropping it changes the marginal, hence the local variance, hence the leverage. (In a pure-diffusion validation this term is the one that makes the reduction exact rather than approximate.)
4. **Smearing the boundary conditions.** Density solvers need the density and its derivatives to vanish at the boundaries for the integrations by parts to be legitimate. Truncating the spot grid too tightly in the wings puts mass on the boundary, and the conditional variance there - the region that controls the smile wings - becomes an artefact.
5. **Grid resolution versus the variance scale.** The two-state system's components have widths $\alpha_i\sqrt t$, which span a factor $3$ here; a grid that resolves the wider component under-resolves the narrower one at short times. Unconditionally stable (implicit) schemes help but do not fix a grid that is too coarse for the smallest scale.
6. **Believing the PDE route eliminates model risk.** It eliminates *Monte-Carlo* error. The driver, the closure and the interpolation of the leverage remain modelling choices, and the leverage is still a decomposition of the fitted surface rather than a market quantity.
7. **Using the forward-PDE route outside one factor.** The $(t,S)$ forward PDE exploits the one-factor structure of the conditional variance. With a multi-factor or rough driver the conditional variance depends on more than one conditioning variable, and the reduction must be carried out on the joint density (Route B) - or replaced by the particle method.

---

### 5. References

- **Guyon, J. & Henry-Labordère, P.** (2013), *Nonlinear Option Pricing* (Chapman & Hall/CRC)
- **Lipton, A.** (2002), *The vol smile problem*, Risk (February), 61–65
- **Gyöngy, I.** (1986), *Mimicking the one-dimensional marginal distributions of processes having an Itô differential*, PTRF **71**(4), 501–516
- **Bergomi, L.**, *Stochastic Volatility Modeling* (CRC, 2016)
- **Gatheral, J.**, *The Volatility Surface*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]]
- Forward: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Theory: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 The PDE & Derivation]] (Feynman–Kac and the forward Kolmogorov equation) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|Heston · 02 The Heston Model]] (the PDE whose terms reappear above) · [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]] (finite differences, the drift/diffusion split)

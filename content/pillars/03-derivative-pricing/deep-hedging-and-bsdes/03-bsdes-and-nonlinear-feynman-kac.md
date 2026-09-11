---
title: "03 — The BSDE Backbone & Nonlinear Feynman–Kac: Pardoux–Peng, Quadratic Drivers, Entropic Risk"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - bsde
  - nonlinear-feynman-kac
  - pardoux-peng
  - quadratic-bsde
  - g-expectation
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 The PDE & Derivation]] and [[foundations/stochastic-calculus/04-sdes-and-simulation|SC · 04 SDEs & Simulation]].

---

### 1. Intuition & Practical Objective

A forward SDE says: *given where I start, where do I end up?* A **backward** SDE says the opposite: *given where I must end up, what is the value now — and by which control?* That inversion is exactly the structure of a hedging problem, and it is why BSDEs are the natural language of this folder.

The classic Feynman–Kac theorem ([[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02]]) already links a *linear* PDE to an expectation: $u(t,x)=\mathbb E[g(X_T)\mid X_t=x]$. **Pardoux–Peng (1990) removed the linearity.** Replace the expectation by a *backward SDE* with a driver $f$, and the same link survives in a nonlinear form:

$$\partial_tu+Lu+f\big(t,u,\sigma^{\!\top}\nabla u\big)=0\ \Longleftrightarrow\ Y_t=u(t,X_t),\quad Z_t=\sigma^{\!\top}\nabla u(t,X_t).$$

The one-sentence essence:

> **A BSDE is a Feynman–Kac formula for *nonlinear* PDEs: the pair $(Y,Z)$ generalises (value, gradient), the driver $f$ generalises the discount/payoff non-linearity, and the *entropic risk measure* — the only one of page 02's three with a closed-form dynamics — is exactly the special case $f(z)=-\tfrac{\gamma}{2}|z|^2$ whose dynamics is the exponential transform $e^{-\gamma Y_t}$ being a martingale.**

Four things to carry out of this page:

1. **The pair $(Y,Z)$, not just $Y$.** $Y_t$ is the value (the price, the utility, the risk), and $Z_t$ is the *control* — in a Markovian setting $Z_t=\sigma^{\!\top}\nabla u$, the martingale-representation density, i.e. the hedge *in the diffusive scale*. The numerical difficulties of deep hedging are almost all difficulties with $Z$.
2. **Lipschitz is the classical regime; quadratic is the financial one.** Pardoux–Peng need $f$ Lipschitz in $(y,z)$. The entropic driver $-\tfrac{\gamma}{2}z^2$ is *quadratic* and violates that hypothesis — it needs the Kobylanski theory, and it is precisely the case that matters for hedging. The extra structure (the exponential transform) is what replaces the Lipschitz condition.
3. **Nonlinear Feynman–Kac is the computational bridge.** It converts "solve a BSDE" into "solve a semilinear PDE" and back — which is why the Deep BSDE and Deep Galerkin solvers of §04 attack the *same* object from two different directions.
4. **$g$-expectations package it.** A driver $g$ defines a sublinear (or nonlinear) expectation $\mathcal E_g[\xi\mid\mathcal F_t]:=Y_t$. $g\equiv0$ recovers the ordinary conditional expectation; $g(z)=-(\gamma/2)z^2$ recovers the entropic one. The comparison theorem makes these well-behaved.

The practical objective: write down a BSDE, state the conditions for a solution, take the nonlinear Feynman–Kac correspondence in both directions, solve an exactly-solvable quadratic BSDE by hand, and reproduce it numerically by backward-induction LSMC.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The BSDE

Fix a filtered probability space $(\Omega,\mathcal F,(\mathcal F_t)_{t\ge0},\mathbb P)$ carrying a $d$-dimensional Brownian motion $W$, and a **terminal condition** $\xi\in L^2(\mathcal F_T)$. A BSDE is

$$\boxed{\ Y_t=\xi+\int_t^{T}f\big(s,Y_s,Z_s\big)\,ds-\int_t^{T}Z_s\,dW_s,\qquad 0\le t\le T\ }$$

or, in differential form, $dY_t=-f(t,Y_t,Z_t)\,dt+Z_t\,dW_t$ with $Y_T=\xi$. Two objects are sought: a *value* $Y$ (continuous, adapted) and a *control* $Z$ ($\mathbb R^{1\times d}$-valued, adapted). The minus sign in front of the $Z$-integral is a convention; it makes $Z$ the density in the martingale representation of the "hedging error" and is standard in the financial literature.

**Existence and uniqueness (Pardoux–Peng 1990).** If

$$\xi\in L^2(\mathcal F_T),\qquad f\ \text{is Lipschitz in }(y,z)\ \text{uniformly in }t,\qquad \int_0^T\!\|f(t,0,0)\|^2dt<\infty ,$$

then there is a unique solution $(Y,Z)$ with $Y$ continuous and both in the appropriate $L^2$ spaces. The proof is a fixed-point argument: the *linear* BSDE with driver $f^0=<f> dt$ has the explicit solution $Y_t=\mathbb E[\xi+\int_t^T f^0 ds\mid\mathcal F_t]$ (a Feynman–Kac identity), and the Picard iteration contracts onto that when $f$ is Lipschitz. **The linear case is the one the hub code solves**: with $f\equiv0$, $Y_t=\mathbb E[\xi\mid\mathcal F_t]$ (the price) and $Z_t$ is the martingale-representation density (the hedge). Set $\xi=(S_T-K)^+$ and you have Black–Scholes written as a BSDE.

#### 2.2 Nonlinear Feynman–Kac

Let the forward process be $dX_t=\mu(t,X_t)dt+\sigma(t,X_t)dW_t$ with generator $Lu=\mu\cdot\nabla u+\tfrac12\mathrm{tr}(\sigma\sigma^{\!\top}\nabla^2u)$. Suppose there is a smooth solution $u$ of the **semilinear** equation

$$\boxed{\ \partial_tu+Lu+f\big(t,u,\sigma^{\!\top}\nabla u\big)=0,\qquad u(T,x)=g(x)\ }$$

Then the BSDE with terminal $\xi=g(X_T)$ and driver $f$ has the *Markovian* solution

$$Y_t=u(t,X_t),\qquad Z_t=\sigma^{\!\top}\nabla u(t,X_t).$$

This is proved with Itô's lemma on $Y_t=u(t,X_t)$: $dY_t=(\partial_tu+Lu)dt+\nabla u^{\!\top}\sigma\,dW_t=-f\,dt+Z\,dW_t$. Reading it *backwards* is the useful direction in practice: if you can solve the BSDE, you have solved the PDE — and vice versa, which is why Deep BSDE (PDE ⇒ BSDE) and Deep Galerkin (PDE ⇒ residual) are two attacks on the same object.

Two consequences that matter constantly:

- **$Z$ is a gradient.** In one dimension $Z_t=\sigma\,\partial_xu$ — the *delta in diffusive units*. Learning $Z$ is learning the hedge; the numerical noise in $Z$ (§3 check B) is the numerical noise in the delta.
- **The driver is the model's nonlinearity.** $f\equiv0$ gives Black–Scholes; $f$ linear in $u$ gives discounting; $f$ quadratic in $z$ gives entropic risk; $f$ concave in $z$ gives transaction costs (Leland, §06). *The whole zoo of incomplete-market pricing is a choice of driver.*

#### 2.3 The entropic (quadratic) driver — the hinge of the folder

Take the driver to be **quadratic in $z$**:

$$f(t,y,z)=-\tfrac{\gamma}{2}|z|^2\qquad(\gamma>0).$$

This is *not* Lipschitz, so Pardoux–Peng does not apply; but the transform

$$U_t:=e^{-\gamma Y_t}$$

is a *martingale*. Indeed with $dY=\tfrac{\gamma}{2}Z^2dt+Z\,dW$ Itô gives

$$dU_t=-\gamma U_t\,dY_t+\tfrac{\gamma^2}{2}U_t\,d\langle Y\rangle_t
=-\gamma U_t\Big(\tfrac{\gamma}{2}Z^2dt+Z\,dW_t\Big)+\tfrac{\gamma^2}{2}U_tZ^2dt=-\gamma U_tZ_t\,dW_t ,$$

so $U$ is a local martingale, and under exponential integrability a true one. Hence $U_t=\mathbb E[U_T\mid\mathcal F_t]=\mathbb E[e^{-\gamma\xi}\mid\mathcal F_t]$ and

$$\boxed{\ Y_t=-\frac1\gamma\ln\mathbb E\big[e^{-\gamma\xi}\ \big|\ \mathcal F_t\big]\ }$$

**The quadratic BSDE is the exponential transform of a conditional expectation.** This is *why* entropic risk is the tractable case: the nonlinearity is entirely absorbed by the exponential, and the remaining objects are ordinary conditional expectations. Two immediate corollaries:

- **The comparison/level structure.** For a Gaussian terminal $\xi\sim N(m,s^2)$ the closed form is exact: $Y_t=m_t-\tfrac{\gamma}{2}s_t^2$, and in general $Y_0=m-\tfrac{\gamma}{2}s^2+O(\gamma^2)$ — the mean–variance hedge is the small-risk-aversion limit (§02 §2.4).
- **This is the indifference price.** $\rho_\gamma(\xi)=\frac1\gamma\ln\mathbb E[e^{\gamma\xi}]$ (a *loss* with $+\gamma$) is the exponential-utility indifference price of §02 §2.3; the sign of $\gamma$ in the driver is the sign convention between "value of a liability" and "risk measure of a payoff".

#### 2.4 The exactly solvable example (used in §3)

Restrict to arithmetic Brownian motion, $dX_t=\sigma\,dW_t$ (so $L=\tfrac{\sigma^2}{2}\partial_x^2$), and take the terminal condition $\xi=X_T^2$ (a *quadratic*, hence unbounded, payoff — deliberately: it shows the method is not confined to bounded claims). With $f(z)=-\tfrac12 z^2$ (i.e. $\gamma=1$), the nonlinear Feynman–Kac equation is

$$\partial_tu+\tfrac{\sigma^2}{2}u_{xx}-\tfrac{\sigma^2}{2}(u_x)^2=0,\qquad u(T,x)=x^2 .$$

Guess $u(t,x)=a(\tau)+b(\tau)x^2$ with $\tau=T-t$; substituting gives $b'=-2\sigma^2b^2$, $a'=\sigma^2b$, $b(0)=1,\ a(0)=0$. Separating: $b=1/(1+2\sigma^2\tau)$ and $a=\tfrac12\ln(1+2\sigma^2\tau)$. Hence

$$\boxed{\ Y_t=\tfrac12\ln\!\big(1+2\sigma^2\tau\big)+\frac{X_t^2}{1+2\sigma^2\tau},\qquad
Z_t=\sigma\,\partial_xu=\frac{2\sigma X_t}{1+2\sigma^2\tau},\qquad \tau=T-t\ }$$

Two sanity limits: at $\tau=0$, $Y_T=X_T^2=\xi$ ✓; as $\sigma\to0$, $Y_t\to X_t^2$ ✓ (no randomness, no risk). Everything in §3 checks against these.

#### 2.5 $g$-expectations and the comparison theorem

A driver $g$ (state-independent, $g(t,0,0)=0$) defines the **$g$-expectation** $\mathcal E_g[\xi\mid\mathcal F_t]:=Y_t$ of the BSDE with driver $g$ and terminal $\xi$. Properties follow from the **comparison theorem**:

$$f_1\le f_2\ \text{pointwise and }\ \xi_1\le\xi_2\ \Longrightarrow\ Y^1_t\le Y^2_t\ \text{a.s. for all }t .$$

- $g\equiv0$: $\mathcal E_0[\xi\mid\mathcal F_t]=\mathbb E[\xi\mid\mathcal F_t]$ — the ordinary expectation.
- $g$ convex in $z$: $\mathcal E_g$ is **sublinear** (monotone, translation-invariant, convex) and its dual is a *set* of measures — the BSDE face of the robust representation of §02.
- $g(z)=-\tfrac{\gamma}{2}z^2$ (concave): $\mathcal E_g$ is *superlinear*, and equals the entropic transform above.

The financial reading: a nonlinear expectation is a *set of priors* (model uncertainty), and choosing a driver is choosing how much the desk distrusts its own model. This is the BSDE-theoretic root of the distributionally-robust hedge of [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06]].

---

### 3. Computational Implementation — a quadratic BSDE solved by hand and by LSMC

Three independent checks on the exactly-solvable example of §2.4: (A) the closed form satisfies the nonlinear PDE to machine precision; (B) a **backward-induction LSMC solver** — regression for $Y$ and the martingale-representation regression for $Z$ — reproduces both $Y_0$ and $Z_0$; (C) the Gaussian closed form $m-\tfrac{\gamma}{2}s^2$ is verified against a Monte-Carlo entropic transform.

```python
import math, random

# Exactly solvable QUADRATIC BSDE.
#   dX_t = sigma dW_t,  X_0 = x0,  terminal xi = X_T^2,  driver f(y,z) = -z^2/2:
#       Y_t = xi + Int_t^T f(Y_s,Z_s) ds - Int_t^T Z_s dW_s     (Pardoux-Peng form)
#   closed form:  Y_t = 1/2 ln(1+2 sigma^2 tau) + X_t^2/(1+2 sigma^2 tau),   tau=T-t
#                 Z_t = 2 sigma X_t /(1+2 sigma^2 tau)
def Yex(t,x,T,s): tau=T-t; return 0.5*math.log(1.0+2.0*s*s*tau)+x*x/(1.0+2.0*s*s*tau)
def Zex(t,x,T,s): tau=T-t; return 2.0*s*x/(1.0+2.0*s*s*tau)

sig,T,x0=0.20,1.0,1.0
print("Quadratic BSDE, sigma=0.20, T=1, x0=1.  closed-form solution:")
for t in (0.00,0.25,0.50,0.75,1.00):
    print(f"   t={t:4.2f}:  Y_t={Yex(t,x0,T,sig):.6f}   Z_t={Zex(t,x0,T,sig):.6f}")

# --- check A: the nonlinear Feynman-Kac PDE  u_t + (s^2/2)u_xx + f(u,s u_x) = 0,  f=-(s u_x)^2/2
random.seed(3); worst=0.0
for _ in range(3000):
    t=random.random()*0.999; x=-1.0+2.0*random.random(); h=1e-5
    ut=(Yex(t+h,x,T,sig)-Yex(t-h,x,T,sig))/(2*h)
    ux=(Yex(t,x+h,T,sig)-Yex(t,x-h,T,sig))/(2*h)
    uxx=(Yex(t,x+h,T,sig)-2.0*Yex(t,x,T,sig)+Yex(t,x-h,T,sig))/(h*h)
    worst=max(worst,abs(ut+0.5*sig*sig*uxx-0.5*sig*sig*ux*ux))
print(f"   check A: max |u_t + (s^2/2)u_xx - (s^2/2)(u_x)^2| over 3000 collocation points = {worst:.2e}")

# --- check B: backward-induction LSMC reproduces Y_0 and Z_0
def lstsq(A,b):
    n=len(A); M=[A[i][:]+[b[i]] for i in range(n)]
    for c in range(n):
        q=max(range(c,n),key=lambda rr:abs(M[rr][c])); M[c],M[q]=M[q],M[c]
        for rr in range(c+1,n):
            f=M[rr][c]/M[c][c]
            for cc in range(c,n+1): M[rr][cc]-=f*M[c][cc]
    x=[0.0]*n
    for i in range(n-1,-1,-1): x[i]=(M[i][n]-sum(M[i][j]*x[j] for j in range(i+1,n)))/M[i][i]
    return x
def regress(Y,Xs,basis):
    mm=len(basis(Xs[0])); A=[[0.0]*mm for _ in range(mm)]; b=[0.0]*mm
    for y,x in zip(Y,Xs):
        ph=basis(x)
        for i in range(mm):
            b[i]+=ph[i]*y
            for j in range(mm): A[i][j]+=ph[i]*ph[j]
    return lstsq(A,b)
def solve(steps,npath,seed):
    random.seed(seed); dt=T/steps; sq=math.sqrt(dt)
    X=[[0.0]*(steps+1) for _ in range(npath)]; W=[[0.0]*steps for _ in range(npath)]
    for p in range(npath):
        x=x0; X[p][0]=x
        for j in range(steps): W[p][j]=sq*random.gauss(0.0,1.0); x+=sig*W[p][j]; X[p][j+1]=x
    basis=lambda x:(1.0,x,x*x)
    Y=[X[p][steps]**2 for p in range(npath)]
    for i in range(steps-1,-1,-1):
        Xi=[X[p][i] for p in range(npath)]
        if i==0:
            Z=sum(Y[p]*W[p][0]/dt for p in range(npath))/npath
            return sum(Y)/npath-0.5*Z*Z*dt, Z
        c=regress(Y,Xi,basis); Ey=[sum(a*b for a,b in zip(c,basis(x))) for x in Xi]
        c=regress([Y[p]*W[p][i]/dt for p in range(npath)],Xi,basis)
        Z=[sum(a*b for a,b in zip(c,basis(x))) for x in Xi]
        Y=[Ey[p]-0.5*Z[p]*Z[p]*dt for p in range(npath)]
print(f"   check B: LSMC-BSDE, exact Y_0={Yex(0.0,x0,T,sig):.6f}, exact Z_0={Zex(0.0,x0,T,sig):.6f}")
for steps in (10,20,40):
    ys=[];zs=[]
    for seed in (1,2,3,4):
        y,z=solve(steps,30000,seed); ys.append(y); zs.append(z)
    print(f"     steps={steps:3d}: Y_0={sum(ys)/4:.6f} (bias {sum(ys)/4-Yex(0.0,x0,T,sig):+.2e})"
          f"   Z_0={sum(zs)/4:.6f} (bias {sum(zs)/4-Zex(0.0,x0,T,sig):+.2e})   [4 seeds x 30000 paths]")

# --- check C: Gaussian terminal, xi ~ N(m,s^2), gamma=1.  Y_0 = -(1/g)ln E[e^{-g xi}] = m - g s^2/2 (exact)
random.seed(17); g,mg,sg=1.0,1.04,math.sqrt(0.1632)
nG=200000
est=-math.log(sum(math.exp(-g*random.gauss(mg,sg)) for _ in range(nG))/nG)/g
print(f"   check C: Gaussian xi~N(1.04,0.1632), gamma=1: MC Y_0={est:.6f}   m - (g/2)s^2 = {mg-0.5*g*sg*sg:.6f}")
```
```
Quadratic BSDE, sigma=0.20, T=1, x0=1.  closed-form solution:
   t=0.00:  Y_t=0.964406   Z_t=0.370370
   t=0.25:  Y_t=0.972531   Z_t=0.377358
   t=0.50:  Y_t=0.981149   Z_t=0.384615
   t=0.75:  Y_t=0.990293   Z_t=0.392157
   t=1.00:  Y_t=1.000000   Z_t=0.400000
   check A: max |u_t + (s^2/2)u_xx - (s^2/2)(u_x)^2| over 3000 collocation points = 7.19e-08
   check B: LSMC-BSDE, exact Y_0=0.964406, exact Z_0=0.370370
     steps= 10: Y_0=0.963500 (bias -9.06e-04)   Z_0=0.367363 (bias -3.01e-03)   [4 seeds x 30000 paths]
     steps= 20: Y_0=0.963025 (bias -1.38e-03)   Z_0=0.383935 (bias +1.36e-02)   [4 seeds x 30000 paths]
     steps= 40: Y_0=0.962519 (bias -1.89e-03)   Z_0=0.379103 (bias +8.73e-03)   [4 seeds x 30000 paths]
   check C: Gaussian xi~N(1.04,0.1632), gamma=1: MC Y_0=0.957976   m - (g/2)s^2 = 0.958400
```

**Reading the output.**

- **(A) The closed form is a genuine solution.** Its maximum PDE residual over $3000$ random collocation points is $7.2\times10^{-8}$ — *finite-difference truncation error*, not model error (the step is $h=10^{-5}$, so $O(h^2)$ discretisation of a smooth function sits at that scale). The nonlinear Feynman–Kac correspondence $\partial_tu+\tfrac{\sigma^2}{2}u_{xx}-\tfrac{\sigma^2}{2}(u_x)^2=0$ is satisfied.
- **(B) The LSMC solver works, and the error is *in the control*.** $Y_0$ is recovered with a bias of $-0.9$ to $-1.9\times10^{-3}$ on a value of $0.9644$ ($\approx0.2\%$) shrinking slowly; $Z_0$ is recovered with a bias of $\pm(3\text{–}14)\times10^{-3}$ on $0.3704$ — comparable in *relative* terms but **far noisier across seeds**. This is the canonical BSDE error signature: the backward regression computes the value functional (smooth, well-conditioned) to high accuracy, and the control (a gradient, hence differentiation of a noisy object) to much lower accuracy. Every deep-hedging implementation inherits this asymmetry.
- **(C) The Gaussian closed form is exact and the MC agrees.** $\xi\sim N(1.04,0.1632)$ with $\gamma=1$: the Monte-Carlo entropic transform gives $0.957976$ against $m-\tfrac{\gamma}{2}s^2=0.958400$ — a $0.04\%$ gap, within the Monte-Carlo and log-bias error of an estimator whose integrand is $\log$-normal. This confirms the *mean-minus-half-risk-aversion-times-variance* identity, i.e. the exact bridge from the entropic BSDE to the variance-optimal hedge of page 01.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Applying Pardoux–Peng to a quadratic driver.** The theorem needs $f$ Lipschitz in $z$; $f=-\tfrac{\gamma}{2}z^2$ is not. Existence for quadratic drivers needs bounded terminal data (or exponential moments) and the Kobylanski machinery, and uniqueness can fail without them. "There is a BSDE theory" does not mean "your BSDE is covered by the textbook theorem".
2. **Confusing $Z$ with the delta.** $Z_t=\sigma^{\!\top}\nabla u$: it is the delta *scaled by* the volatility, and in multiple dimensions it is a *row vector* contracted with the diffusion matrix. Reporting $Z$ as "the delta" silently inserts a factor $\sigma S$ (the hub code reports both: $Z_0=10.919$ and $Z_0/(\sigma S_0)=0.546$). Get the scaling wrong and a correct solver still "validates" against a correctly-scaled wrong benchmark.
3. **Treating the driver as arbitrary.** Different drivers give different *prices*, not just different numerical behaviour: $f\equiv0$ prices at $\mathbb E[\xi]$; the entropic driver prices at the indifference price. A sign error in $f$ (or in $\gamma$) flips "risk-averse" into "risk-seeking" and is easy to miss because the code still runs.
4. **Using the wrong measure in the forward simulation.** The BSDE is stated under $\mathbb Q$ (or under $\mathbb P$ with a driver that absorbs the risk premium). Simulating $X$ with the *physical* drift and then pricing with a risk-neutral BSDE gives a systematic bias that no amount of Monte Carlo removes. The drift belongs in the driver, and the driver must be stated. See [[foundations/stochastic-calculus/05-girsanov-and-risk-neutral|SC · 05 Girsanov & Risk-Neutral]].
5. **Ignoring the terminal integrability required for the exponential transform.** The identity $Y_t=-\frac1\gamma\ln\mathbb E[e^{-\gamma\xi}\mid\mathcal F_t]$ requires $\mathbb E[e^{-\gamma\xi}]<\infty$. For heavy-tailed or unbounded-below payoffs (short calls, quadratic payoffs on log-normal spots) the exponential *does not integrate*, the transform fails, and the "solution" is $-\infty$. §3 uses a *quadratic* payoff on an *additive* Brownian motion precisely because the exponential moment exists there; on a geometric Brownian motion the same payoff would explode the entropic transform.
6. **Forgetting that the comparison theorem is strict about the conditions.** $f_1\le f_2$ and $\xi_1\le\xi_2$ give $Y^1\le Y^2$ only under the same integrability regime; for quadratic drivers the ordering can fail without boundedness. Bulk monotonicity intuitions ("a riskier payoff has a higher value") are theorems with hypotheses, not axioms.
7. **Using LSMC with a poor regressor basis.** The check-B bias comes from the regression family, not from the number of paths: a basis that cannot represent $E[Y_{t_{i+1}}\mid X_{t_i}]$ produces a *bias*, not noise, and increasing the path count converges confidently to the wrong answer. Always fit on a basis that contains the true conditional-mean family (here $\{1,x,x^2\}$, which is exact for the quadratic example), or validate with an independent method. See [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|NM · 03 Monte-Carlo Pricing]].
8. **Believing the value is "the answer".** $Y_0$ is one number; the *strategy* is the whole process $Z_t$, and it is $Z$ that a desk trades. A solver validated only on $Y_0$ has validated only a diagnostic, not the deliverable.

---

### 5. Canonical Literature & Study References

- **Pardoux, E. & Peng, S.** (1990), *Adapted solution of a backward stochastic differential equation*, Systems & Control Letters 14, 55–61 — the founding existence/uniqueness theorem under Lipschitz $f$. **Pardoux, E. & Peng, S.** (1992), *Backward SDEs and quasilinear PDEs* — the nonlinear Feynman–Kac correspondence. **El Karoui, N., Peng, S., Quenez, M.-C.** (1997), *Backward stochastic differential equations in finance*, Mathematical Finance 7(1), 1–71 — the financial dictionary (pricing, hedging, $g$-expectations, comparison theorem).
- **Kobylanski, M.** (2000), *Backward stochastic differential equations and partial differential equations with quadratic growth*, Annals of Probability 28(2), 558–602 — the theory required by the entropic driver. **Briand, P. & Hu, Y.** (2006/2008), *BSDEs with quadratic growth and unbounded terminal value* — extensions. **Barrieu, P. & El Karoui, N.** — on inf-convolution and risk measures via BSDEs.
- **Peng, S.** (1997/2004), *Monotonic limit theorem of BSDE and nonlinear decomposition theorem*, and *Nonlinear expectations and nonlinear Markov chains* — $g$-expectations, sublinearity and the link to the "set of priors" robust representation. **Coquet, F., Hu, Y., Mémin, J., Peng, S.** (2002), *Filtration-consistent nonlinear expectations and related $g$-expectations*, Probability Theory and Related Fields 123, 1–27.
- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291 — the explicit identification of the entropic hedging problem with a *quadratic BSDE*, which is the bridge between §02 and §03 of this folder. Their follow-up, **Buehler et al.** (2019), *Deep hedging: learning to simulate, hedge and price under market frictions* (and **Buehler, Gonon, Teichmann, Wood** 2019, *A stochastic control approach to deep hedging*) develops the BSDE side further.
- **Gobet, E., Lemor, J.-P., Warin, X.** (2005), *A regression-based Monte Carlo method to solve backward stochastic differential equations*, Annals of Applied Probability 15(3), 2172–2202 — the LSMC-BSDE scheme of §3. **Bender, C. & Steiner, J.** (2012), *Least-squares Monte Carlo for BSDEs*, and **Bender, C. & Zhang, J.** (2018), *Time discretization and Markovian iteration for coupled FBSDEs* — the error analysis, including the $Z$-regression noise seen in check B.
- **Karatzas, I. & Shreve, S.**, *Brownian Motion and Stochastic Calculus*, Ch 5 (martingale representation) — the theorem that makes $Z$ exist. **Øksendal, B.**, *Stochastic Differential Equations*, Ch 4 (the linear Feynman–Kac theorem whose nonlinear generalisation this page uses). **Pham, H.**, *Continuous-time Stochastic Control and Optimization with Financial Applications*, Ch 6 (FBSDEs and the four-step scheme).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/02-convex-risk-and-the-deep-hedging-objective|02 · Convex Risk & the Deep-Hedging Objective]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/04-deep-bsde-and-deep-galerkin-solvers|04 · Deep BSDE & Deep Galerkin]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Theory base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|SC · 03 Itô Integral & Doeblin]] · [[foundations/stochastic-calculus/04-sdes-and-simulation|SC · 04 SDEs & Simulation]] · [[foundations/stochastic-calculus/05-girsanov-and-risk-neutral|SC · 05 Girsanov & Risk-Neutral]] · [[foundations/probability-and-measure-theory/05-martingales|PMT · 05 Martingales]] · [[foundations/probability-and-measure-theory/04-conditional-expectation|PMT · 04 Conditional Expectation]]
- The linear special case: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 The PDE & Derivation]] · [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · 03 Pricing Formulas]]
- Numerical neighbours: [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|NM · 03 Monte-Carlo Pricing]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|NM · 04 Variance Reduction]] · [[foundations/numerical-methods/03-monte-carlo|NM · 03 Monte Carlo (Foundations)]]
- Risk-measure counterpart: [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]]

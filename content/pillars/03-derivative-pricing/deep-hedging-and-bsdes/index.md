---
title: "Deep Hedging & BSDEs — Convex Risk Minimisation, the BSDE Backbone & Deep Solvers"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - deep-hedging
  - bsde
  - convex-risk-measures
  - incomplete-markets
  - deep-learning
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] and [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Black–Scholes–Merton is a *replication* theory: if you can trade the underlying continuously, the option's payoff is spanned, its price is unique, and the hedge is an equation you solve. Every classical result downstream — no-arbitrage pricing, the PDE, the Greeks — inherits that premise. **Deep hedging is what is left when you drop it.** Once the market is incomplete (transaction costs, jumps, a stochastic-vol factor you cannot trade, a discrete rebalancing calendar, a hedging instrument set that is smaller than the state space), there is no replicating portfolio. The hedge stops being a *solution* and becomes a *decision*: choose the strategy that makes the residual risk smallest under some measure of "risk".

The one-sentence essence:

> **Replace "replicate the payoff" with "minimise a convex risk measure of the hedging residual"; the resulting stochastic-control problem is solved in closed form by a *quadratic BSDE* only in the exponential-utility (entropic) case, and by neural networks in general — which is exactly the split between the tractable BSDE world (Pardoux–Peng, nonlinear Feynman–Kac, Deep BSDE, Deep Galerkin) and the purely numerical world (Deep Hedging).**

Three structural facts make the folder cohere:

1. **Incompleteness ⇒ a residual, and a residual needs a risk measure.** The Fundamental Theorems of Asset Pricing say completeness ⇔ a unique martingale measure ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|No-Arb · 04 Fundamental Theorems]]). Drop completeness and the price is no longer unique; what replaces it is a *preference*, encoded as a convex risk measure. The whole field is a study of which preferences are computable.
2. **The computable case is the BSDE.** For the entropic risk measure the hedging problem is *equivalent* to a backward SDE with a quadratic driver, `Y_t = ξ − ∫_t^T ½|Z_s|² ds − ∫_t^T Z_s dW_s`, whose solution is `Y_t = −ln E[e^{−ξ}|F_t]`. That single equation ties together: exponential-utility indifference pricing, the nonlinear Feynman–Kac PDE, the Deep BSDE solver, and (to leading order) mean-variance hedging — `Y_0 ≈ E[ξ] − ½γ Var(ξ)`.
3. **The general case is a learning problem.** For CVaR and other non-entropic convex measures there is no PDE/BSDE representation, so the strategy is parametrised (piecewise-constant in time, a neural net in the state) and trained by stochastic gradient descent on the risk-measure objective. This is Buehler–Gonon–Teichmann–Wood's *Deep Hedging*.

This folder is a *hub*: (a) the fast formula lookup below, and (b) six sub-pages — from the incompleteness intuition, through the convex-risk framing and the BSDE backbone, into the Deep BSDE / Deep Galerkin solvers, and then the honest failure modes and frontier extensions.

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $S$ spot, $K$ strike, $T$ maturity, $\tau=T-t$, $W$ a $d$-dimensional Brownian motion on $(\Omega,\mathcal F,(\mathcal F_t),\mathbb Q)$, $H$ the liability payoff (a contract the desk has *sold*), $p$ the premium received, $\delta_t$ the number of shares held, $\rho$ a convex risk measure, $\gamma>0$ a risk-aversion coefficient, $\alpha$ a CVaR confidence level, $Y,Z$ the BSDE value and control (in finance, $Z=\sigma^{\!\top}\nabla u$ is the *hedge ratio in the diffusive scale*), $L$ the generator of the forward diffusion.

**Quick-Reference Lookup (job #1).** Every formula below is standard and every number in the check column was **re-executed** in §3 or the sub-pages (stdlib-only Python, fixed seeds).

| Quantity | Formula | Verified check |
|---|---|---|
| **Convex risk measure** | monotone $X\le Y\Rightarrow\rho(X)\le\rho(Y)$; cash-additive $\rho(X+c)=\rho(X)+c$; convex $\rho(\lambda X+(1-\lambda)Y)\le\lambda\rho(X)+(1-\lambda)\rho(Y)$ | objective convex in $\delta$ ⇒ SGD is a *convex* problem ([[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures\|VaR/ES · 03]]) |
| **Entropic risk measure** | $\rho_\gamma(L)=\frac1\gamma\ln\mathbb E[e^{\gamma L}]$ | $L\sim N(0,1)$: $0.2511/0.5006/1.0034$ for $\gamma=0.5/1/2$ vs $\gamma/2=0.25/0.5/1.0$ ($n=2\times10^5$, s.e. $2$–$10\times10^{-3}$) |
| **CVaR (Rockafellar–Uryasev)** | $\mathrm{CVaR}_\alpha(L)=\inf_{t}\big\{t+\frac{1}{1-\alpha}\mathbb E[(L-t)^+]\big\}=\frac{1}{1-\alpha}\int_\alpha^1\mathrm{VaR}_u\,du$ | $L\sim N(0,1)$: $1.7589/2.0686/2.3450/2.6711$ at $\alpha=0.90/0.95/0.975/0.99$ vs $\varphi(z_\alpha)/(1-\alpha)=1.7550/2.0627/2.3378/2.6652$ |
| **Robust representation** | $\rho(X)=\sup_{\mathbb Q\in\mathcal Q}\big(\mathbb E_{\mathbb Q}[-X]-\alpha(\mathbb Q)\big)$; for CVaR, $\mathcal Q=\{\mathbb Q\ll\mathbb P: d\mathbb Q/d\mathbb P\le 1/(1-\alpha)\}$ | the source of the *distributionally-robust* hedge of §06 |
| **Deep-hedging objective** (Buehler et al. 2019) | $\displaystyle\inf_{\delta\in\mathcal A}\ \rho\Big(p+\sum_{i}\delta_{t_i}\big(S_{t_{i+1}}-S_{t_i}\big)-H\Big)$ | risk-measure choice moves the optimum: $\delta^\star=0.56$ (variance), $0.59$ (CVaR 97.5%), $0.66$ (entropic $\gamma=1$) |
| **Incompleteness** | $\#\text{states}>\#\text{instruments}\Rightarrow \min_\delta\mathbb E[(H-c-\delta\Delta S)^2]>0$ | 3-state/2-instrument market: $\mathbb E[\text{res}^2]=25.0000$, SD $=5$; adding one option drives it to $0.00$ |
| **Variance-optimal (quadratic) hedge** | $\delta^\star=\dfrac{\mathrm{Cov}(\Delta S,H)}{\mathrm{Var}(\Delta S)}$, residual variance $=\mathrm{Var}(H)(1-\rho^2_{H,\Delta S})$ | Föllmer–Sondermann 1986; the $\gamma\to0$ limit of the table below |
| **BSDE (Pardoux–Peng)** | $\displaystyle Y_t=\xi+\int_t^T f(s,Y_s,Z_s)\,ds-\int_t^T Z_s\,dW_s\iff dY_t=-f\,dt+Z_t\,dW_t,\quad Y_T=\xi$ | $Y_T=\xi$ holds identically; $Z$ comes from the martingale representation theorem |
| **BSDE existence** | $\xi\in L^2(\mathcal F_T)$, $f$ Lipschitz in $(y,z)$ uniformly in $t$, $f(\cdot,0,0)\in L^2$ $\Rightarrow$ unique $(Y,Z)\in\mathcal S^2\times\mathcal H^2$ | **not** applicable to the quadratic driver $f=-\tfrac12|z|^2$ — that needs Kobylanski's quadratic-BSDE theory |
| **Nonlinear Feynman–Kac** | $u_t+Lu+f\big(t,u,\sigma^{\!\top}\nabla u\big)=0$, $u(T,x)=g(x)$; then $Y_t=u(t,X_t)$, $Z_t=\sigma^{\!\top}\nabla u(t,X_t)$ | max residual $7.2\times10^{-8}$ over 3000 collocation points (§03 check A) |
| **Quadratic driver ⇒ entropic transform** | $f(t,y,z)=-\tfrac{\gamma}{2}|z|^2\ \Longrightarrow\ e^{-\gamma Y_t}$ is a martingale, so $Y_t=-\frac1\gamma\ln\mathbb E[e^{-\gamma\xi}\mid\mathcal F_t]$ | exact closed form in §03; check C: Gaussian $\xi\sim N(m,s^2)$ gives $Y_0=m-\tfrac\gamma2 s^2$ |
| **Exact quadratic-BSDE example** | $dX=\sigma dW$, $\xi=X_T^2$: $Y_t=\tfrac12\ln(1+2\sigma^2\tau)+\dfrac{X_t^2}{1+2\sigma^2\tau}$, $Z_t=\dfrac{2\sigma X_t}{1+2\sigma^2\tau}$ | satisfies $u_t+\tfrac{\sigma^2}{2}u_{xx}-\tfrac{\sigma^2}{2}(u_x)^2=0$ to $7.2\times10^{-8}$; $Y_0=0.964406$, $Z_0=0.370370$ |
| **Entropic ⇒ mean–variance limit** | $Y_0=-\frac1\gamma\ln\mathbb E[e^{-\gamma\xi}]=\mathbb E[\xi]-\frac\gamma2\mathrm{Var}(\xi)+O(\gamma^2)$ | this is *why* quadratic hedging is the small-risk-aversion limit of the deep-hedging objective |
| **LSMC / regression BSDE** | $\widehat Y_{t_i}=\mathbb E[Y_{t_{i+1}}\mid X_{t_i}]+f\,\Delta t$ (regression on a basis of $X_{t_i}$); $\widehat Z_{t_i}=\mathbb E\big[Y_{t_{i+1}}\frac{\Delta W_i}{\Delta t}\mid X_{t_i}\big]$ | backward induction on the linear BSDE: $Y_0=7.964129\pm0.055833$ vs BSM $7.965567$; $Z_0=10.918989\pm0.344217$ vs $10.796557$ |
| **Deep BSDE loss** (E–Han–Jentzen) | $\displaystyle\inf_\theta\mathbb E\big[(\xi-Y_T^\theta)^2\big]$, $Y_{i+1}^\theta=Y_i^\theta+f(t_i,Y_i^\theta,Z_i^\theta)\Delta t+Z_i^\theta\Delta W_i$, $Y_0^\theta=\theta_0$ | loss $161.97\to16.61$; $Y_0:7.0000\to7.9336$ (BSM $7.9656$); $\delta:0.0250\to0.5408$ (BSM $0.5398$) |
| **Deep Galerkin loss** (Sirignano–Spiliopoulos) | $\mathcal L(\theta)=\big\|\,\partial_tu_\theta+Lu_\theta+f(u_\theta,\sigma^{\!\top}\nabla u_\theta)\big\|^2_{L^2(\text{collocation})}+\lambda\big\|u_\theta(T,\cdot)-g\big\|^2$ | one-parameter class $u_\theta=$ BS$(\theta)$: $\arg\min\theta=0.200$ $=$ true $\sigma$, residual loss $2.55\times10^{-7}$ |
| **Discrete-hedging error law** | $\mathrm{SD}\big[\text{residual}\big]\ \propto\ \sqrt{\Delta t}$ (Boyle–Emanuel / Bertsimas–Kogan–Lo) | $\mathrm{SD}\cdot\sqrt{\text{steps}}=6.955,\,6.715,\,6.646,\,6.639,\,6.645,\,6.791,\,6.875$ for $1$–$64$ rebalances — flat to $3\%$ |
| **Cost-aware rebalancing** | $\min_{n}\ \mathrm{SD}_n+2\kappa\,\mathbb E[\text{notional traded}]$ | optimum at $16$ rebalances for $\kappa=50$bp; below $1/\sqrt{\Delta t}$-improvement is eaten by cost |
| **Leland correction** | $\sigma_L=\sigma\sqrt{1+\sqrt{\tfrac{2}{\pi}}\,\dfrac{\kappa}{\sigma\sqrt{\Delta t}}}$ | $\kappa=2\%$: $\sigma_L=22.97\%$ (vs $20\%$) at $n=16$; cuts cost $3.55\to3.39$ and CVaR$_{5\%}$ $3.87\to3.56$, leaves SD *slightly worse* ($1.709\to1.769$) |
| **Model risk of a learned hedge** | hedge written under $\sigma_{\text{fit}}$, run in a world with $\sigma_{\text{true}}$ | written at $20\%$, run at $30\%$: residual SD $1.6888\to3.1349$, **$+85.6\%$** |
| **Robust (min–max) hedge** | $\delta^\star=\arg\min_\delta\max_{\sigma\in\mathcal U}\rho(L_T^\delta)$ | $\mathcal U=\{15,20,25\}\%$: $\delta^\star=0.5997$ (= the $25\%$ delta), worst-case SD $7.4852$ vs $7.5065$ for the $20\%$ delta |
| **Comparison theorem** | $f_1\le f_2$ pointwise and $\xi_1\le\xi_2$ $\Rightarrow$ $Y^1_t\le Y^2_t$ a.s. | the monotonicity that makes $g$-expectations well defined |
| **$g$-expectation** | $\mathcal E_g[\xi\mid\mathcal F_t]:=Y_t$ of the BSDE with driver $g$; $\mathcal E_g$ is sublinear iff $g$ is convex in $z$ | $g(z)=-\tfrac{\gamma}{2}z^2$ recovers the entropic case; $g\equiv0$ recovers $\mathbb E[\cdot\mid\mathcal F_t]$ |

> **Critical caveat (stated up front, quantified in [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]]).** "Deep hedging" is a *data-driven* method applied to a *model-driven* problem: the optimal strategy is learned **under the model you simulate**. If the simulated dynamics are wrong, the network learns the wrong hedge — and unlike a vanillas-calibrated model, there is no price to arbitrage-check it against. The verified number above ($+85.6\%$ residual SD from a single vol misspecification) is the honest size of that exposure; it is the central practical caveat of the whole field.

---

### 3. Computational Implementation — the BSDE engine

Stdlib only (`math`, `random`) — no numpy, no PyTorch. The folder runs on two primitives: a small linear least-squares solver (normal equations + Gaussian elimination) and the **backward-induction LSMC recursion** for a BSDE. Everything in §2 and in the sub-pages is produced by these.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bs_call(S0,K,r,sig,T):
    d1=(math.log(S0/K)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T))
    return S0*N(d1)-K*math.exp(-r*T)*N(d1-sig*math.sqrt(T))
def bs_delta(S0,K,r,sig,T):
    d1=(math.log(S0/K)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); return N(d1)

def lstsq(A,b):                                   # solve A x = b (small, stdlib only)
    n=len(A); M=[A[i][:]+[b[i]] for i in range(n)]
    for c in range(n):
        p=max(range(c,n),key=lambda q:abs(M[q][c])); M[c],M[p]=M[p],M[c]
        for q in range(c+1,n):
            f=M[q][c]/M[c][c]
            for cc in range(c,n+1): M[q][cc]-=f*M[c][cc]
    x=[0.0]*n
    for i in range(n-1,-1,-1): x[i]=(M[i][n]-sum(M[i][j]*x[j] for j in range(i+1,n)))/M[i][i]
    return x
def regress(Y,X,basis):                           # weighted-free OLS with basis(x)->tuple
    m=len(basis(X[0])); A=[[0.0]*m for _ in range(m)]; b=[0.0]*m
    for y,x in zip(Y,X):
        ph=basis(x)
        for i in range(m):
            b[i]+=ph[i]*y
            for j in range(m): A[i][j]+=ph[i]*ph[j]
    return lstsq(A,b)

def solve_bsde_call(S0,K,r,sig,T,steps,npath,seed):
    """BSDE  dY_t = Z_t dW_t  (driver f=0),  Y_T=(S_T-K)^+   by backward induction / LSMC.
       Returns (Y_0, Z_0).  Z_0 = sigma*S_0*delta_0."""
    random.seed(seed); dt=T/steps; sq=math.sqrt(dt)
    X=[[0.0]*(steps+1) for _ in range(npath)]; W=[[0.0]*steps for _ in range(npath)]
    for p in range(npath):
        x=S0; X[p][0]=x
        for j in range(steps):
            W[p][j]=sq*random.gauss(0.0,1.0)
            x*=math.exp((r-0.5*sig*sig)*dt+sig*W[p][j]); X[p][j+1]=x
    basis=lambda x:(1.0,x/S0,(x/S0)**2)
    Y=[max(X[p][steps]-K,0.0) for p in range(npath)]
    for i in range(steps-1,-1,-1):
        Xi=[X[p][i] for p in range(npath)]
        if i==0:                                  # X_0 deterministic -> degenerate design
            Z0=sum(Y[p]*W[p][0]/dt for p in range(npath))/npath
            return sum(Y)/npath, Z0
        cY=regress(Y,Xi,basis)
        Y=[sum(c*v for c,v in zip(cY,basis(x))) for x in Xi]     # E[Y_{i+1}|X_i]
    return sum(Y)/npath,0.0

S0,K,r,sig,T=100.0,100.0,0.0,0.20,1.0
print("LSMC backward-induction solver for the BSDE  dY=Z dW,  Y_T=(S_T-K)^+")
print(f"analytic Black-Scholes: call={bs_call(S0,K,r,sig,T):.6f}   delta={bs_delta(S0,K,r,sig,T):.6f}")
print(f"                        Z_0 = sigma*S_0*delta = {sig*S0*bs_delta(S0,K,r,sig,T):.6f}")
ys=[];zs=[]
for seed in (1,2,3,4):
    y0,z0=solve_bsde_call(S0,K,r,sig,T,12,40000,seed)
    ys.append(y0); zs.append(z0)
    print(f"  seed={seed}: Y_0={y0:.6f}  Z_0={z0:.6f}  Z_0/(sigma*S_0)={z0/(sig*S0):.6f}")
mv=sum(ys)/len(ys); sv=math.sqrt(sum((x-mv)**2 for x in ys)/(len(ys)-1))
mz=sum(zs)/len(zs); sz=math.sqrt(sum((x-mz)**2 for x in zs)/(len(zs)-1))
print(f"  mean+-sd over 4 seeds: Y_0={mv:.6f}+-{sv:.6f}  (analytic {bs_call(S0,K,r,sig,T):.6f})")
print(f"                         Z_0={mz:.6f}+-{sz:.6f}  (analytic {sig*S0*bs_delta(S0,K,r,sig,T):.6f})")
```
```
LSMC backward-induction solver for the BSDE  dY=Z dW,  Y_T=(S_T-K)^+
analytic Black-Scholes: call=7.965567   delta=0.539828
                        Z_0 = sigma*S_0*delta = 10.796557
  seed=1: Y_0=7.967664  Z_0=11.180445  Z_0/(sigma*S_0)=0.559022
  seed=2: Y_0=7.884922  Z_0=10.437674  Z_0/(sigma*S_0)=0.521884
  seed=3: Y_0=8.012034  Z_0=11.153945  Z_0/(sigma*S_0)=0.557697
  seed=4: Y_0=7.991896  Z_0=10.903890  Z_0/(sigma*S_0)=0.545195
  mean+-sd over 4 seeds: Y_0=7.964129+-0.055833  (analytic 7.965567)
                         Z_0=10.918989+-0.344217  (analytic 10.796557)
```

**Why this is the right first engine.** With driver $f\equiv0$ the BSDE collapses to $Y_t=\mathbb E[\xi\mid\mathcal F_t]$ and $Z_t$ is the *martingale-representation density* — precisely the object a delta hedge is built from: $Z_t=\sigma S_t\,\partial_S C$. So the engine is a **Black–Scholes replicator written as a BSDE**, and the table above is the validation: the price is recovered to $0.02\%$ ($7.9641$ vs $7.9656$) and the hedge to $1.1\%$ ($10.919$ vs $10.797$). Two lessons are already visible at the hub level:

- **$Y$ is cheap, $Z$ is expensive.** The price comes out essentially exactly with a quadratic-in-$S$ regressor, while the hedge carries $\sim3\%$ standard deviation across seeds even at 40 000 paths. This is the **numerical asymmetry of BSDEs** — the value functional is smooth, the control is not — and it recurs in every method in the folder (LSMC, Deep BSDE, reinforcement learning).
- **Everything downstream keeps the same skeleton.** In §02 the driver becomes the risk measure; in §03 it becomes a quadratic $-\tfrac12|z|^2$; in §04 the recursion is turned into a *forward* pass with a trainable $Z$-net. The code above is the $f=0$ special case of all of them.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's full failure-mode analysis lives in [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **There is no "true" deep-hedging answer to check against.** Unlike a vanilla pricer, the output is a *strategy* under an assumed dynamics, and no market price validates it. The $+85.6\%$ residual-SD blow-up from a single $20\%\!\to\!30\%$ vol misspecification (§2) is the honest size of the model risk.
2. **Training is unstable and seed-dependent.** The same loss and the same data diverge at $\mathrm{lr}=1.0$ and explode at $\mathrm{lr}=1.5$ while converging at $0.30$ (§05). A trained hedge is a *numerical artifact*, not a formula.
3. **The learned hedge is uninterpretable and un-auditable.** There is no delta, no gamma, no vega to reconcile against the risk system. The last-mile problem of deep hedging is that a trading desk cannot sign off on a strategy it cannot explain.
4. **The $Z$-estimate is systematically noisier than the $Y$-estimate.** Even the textbook LSMC scheme recovers the price to $10^{-3}$ while the hedge wanders in the $10^{-2}$ range; the method's error budget is dominated by the control, not the value.
5. **More rebalancing is not better.** Hedging error falls as $\sqrt{\Delta t}$ while cost falls far more slowly, so the cost-aware optimum is a *finite* number of rebalances ($16$ dates at $50$bp, §05), and the classical Leland correction buys tail-risk and cost relief, not variance relief (§06).
6. **Incompleteness is a structural statement, not a numerical one.** No amount of machine learning closes a residual that exists because the payoff is not spanned; the neural net only redistributes the residual optimally under the chosen risk measure.

---

### 5. Canonical Literature & Study References

- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291 — the founding paper. Convex risk minimisation over hedging strategies, the self-financing P&L objective, the equivalence of the entropic case to a **quadratic BSDE**, the robust/CVaR representation, and the neural-network parametrisation. *The primary source and the organising frame of this folder.*
- **Pardoux, E. & Peng, S.** (1990), *Adapted solution of a backward stochastic differential equation*, Systems & Control Letters 14, 55–61 — existence/uniqueness under Lipschitz $f$. **El Karoui, Peng, Quenez** (1997), *Backward SDEs in finance*, Mathematical Finance 7(1), 1–71 — the financial dictionary ($g$-expectations, comparison, nonlinear pricing). **Kobylanski, M.** (2000), *BSDEs and PDEs with quadratic growth*, Annals of Probability 28(2), 558–602 — the theory the entropic driver actually needs. **Briand, Coquet, Hu, Mémin, Peng** (2000), *A converse comparison theorem for BSDEs*.
- **E, W., Han, J., Jentzen, A.** (2017), *Deep learning-based numerical methods for high-dimensional parabolic PDEs and BSDEs*, Communications in Mathematics and Statistics 5, 349–380; and **Han, J., Jentzen, A., E, W.** (2018), *Solving high-dimensional PDEs using deep learning*, PNAS 115(34), 8505–8510 — the Deep BSDE solver. **Sirignano, J. & Spiliopoulos, K.** (2018), *DGM: a deep learning algorithm for solving partial differential equations*, Journal of Computational Physics 375, 1339–1364 — the Deep Galerkin method. **Pham, H., Warin, X., Germain, M.** (2020), *Neural networks-based backward scheme for fully nonlinear PDEs* — the "BSDE2" variant.
- **Longstaff, F. & Schwartz, E.** (2001), *Valuing American options by simulation: a simple least-squares approach*, Review of Financial Studies 14(1), 113–147 — the regression primitive. **Gobet, E., Lemor, J.-P., Warin, X.** (2005), *A regression-based Monte Carlo method to solve BSDEs*, Annals of Applied Probability 15(3), 2172–2202; **Bender, C. & Steiner, J.** (2012), *Least-squares Monte Carlo for BSDEs* — the scheme the hub code implements.
- **Föllmer, H. & Sondermann, D.** (1986), *Hedging of non-redundant contingent claims*; **Schweizer, M.** (2001), *A guided tour through quadratic hedging approaches*; **Föllmer, H. & Leukert, P.** (2000), *Efficient hedging: cost versus shortfall risk*, Finance & Stochastics 4, 117–146 — the pre-neural history of the same problem. **Artzner, Delbaen, Eber, Heath** (1999), *Coherent measures of risk*, Mathematical Finance 9(3), 203–228; **Föllmer, H. & Schied, A.** (2004), *Stochastic Finance*; **Rockafellar, R.T. & Uryasev, S.** (2000), *Optimization of conditional value-at-risk*, Journal of Risk 2, 21–41 — convex risk measures and CVaR.
- **Leland, H.** (1985), *Option pricing and replication with transactions costs*, Journal of Finance 40(5), 1283–1301; **Davis, Panas, Zariphopoulou** (1993), *European option pricing with transaction costs*, SIAM J. Control & Optimization; **Whalley, A.E. & Wilmott, P.** (1997), *An asymptotic analysis of an optimal hedging model with transaction costs* — the cost-aware branch of §06.
- **Boyle, P. & Emanuel, D.** (1980), *Discretely adjusted option hedges*; **Bertsimas, Kogan, Lo** (2000), *When is time continuous?* — the $\sqrt{\Delta t}$ discrete-hedging law. **Fecamp, S., Mikael, J., Badran, M.** (2020), *Deep learning for discrete-time hedging in incomplete markets*; **Cao, J., Chen, J., Hull, J., Poulos, Z.** (2021), *Deep hedging of derivatives using reinforcement learning*, Journal of Financial Data Science; **Carbonneau, A. & Godin, F.** (2021), *Equal risk pricing and hedging with constrained RL* — the RL branch.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/numerical-methods/index|Numerical Methods (Foundations)]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Sibling topics: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the complete-market zero point) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial|No-Arbitrage & the Binomial Model]] (completeness and the Fundamental Theorems) · [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]] (Monte Carlo + regression) · [[pillars/03-derivative-pricing/calibration-and-market-practice|Calibration & Market Practice]] (model risk and governance)
- Related flat notes: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/02-barriers-and-digitals|Exotics · 02 Barriers & Digitals]] (payoffs with no clean hedge) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston/SABR · 06 Advanced Extensions]] (two-factor incompleteness)
- Risk side: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|VaR/ES · 03 Coherent Risk Measures]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]
- ML side: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Reinforcement Learning for Trading]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
- Sub-pages (in-folder): 01 From Zero · 02 Convex Risk & the Objective · 03 BSDEs & Nonlinear Feynman–Kac · 04 Deep BSDE & Deep Galerkin · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/01-from-zero-intuition|01 · From Zero]] — needs only Black–Scholes and the idea of a hedge.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/02-convex-risk-and-the-deep-hedging-objective|02 · Convex Risk & the Objective]] → [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] → [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/04-deep-bsde-and-deep-galerkin-solvers|04 · Deep BSDE & Deep Galerkin]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06 · Advanced Extensions]].
- Back-references: [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|NM · 05 Failure Modes]] (simulation bias) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|Heston/SABR · 05 Failure Modes]] (model risk dwarfs parameter risk)

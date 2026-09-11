---
title: "04 — Deep BSDE & Deep Galerkin Solvers: Learning the Value and the Hedge"
tags:
  - pillar-derivative-pricing
  - deep-hedging-and-bsdes
  - deep-bsde
  - deep-galerkin
  - neural-networks
  - stochastic-control
  - high-dimensional-pde
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] and [[pillars/07-machine-learning-altdata/deep-learning-for-sequences|Deep Learning for Sequences]].

---

### 1. Intuition & Practical Objective

Pages 02–03 produced the object: a semi-linear PDE, equivalently a BSDE, whose solution is a *pair* $(u,\nabla u)$ — the price and the hedge. Page 04 is about computing it when the dimension is too large for a grid and the payoff too non-linear for a closed form. There are two complementary algorithms, and they solve **the same equation from opposite ends**:

| | **Deep BSDE** (E–Han–Jentzen 2017) | **Deep Galerkin / DGM** (Sirignano–Spiliopoulos 2018) |
|---|---|---|
| what is minimised | the **terminal mismatch** $\mathbb E[(\xi-Y_T^\theta)^2]$ | the **PDE residual** $\|\partial_tu_\theta+Lu_\theta+f(\cdot)\|^2$ (+ terminal penalty) |
| how the equation is used | integrated forward along simulated paths | differentiated at sampled collocation points |
| what the network outputs | $Z_t\approx\sigma^{\!\top}\nabla u$ (the *hedge*) at each step | $u_\theta(t,x)$ (the *value*) directly |
| strengths | low dimension per step, hedging-native, no second derivatives | mesh-free, handles free boundaries and irregular domains, gives $u$ everywhere |
| weaknesses | needs a good $Z$-architecture; pain at the terminal layer | residual needs $u_{xx}$ (second derivatives of a network), harder to train |

The one-sentence essence:

> **Both methods replace the unknown function by a neural network and the equation by a Monte-Carlo loss; Deep BSDE parametrises the *control* $Z$ and enforces the *terminal condition*, Deep Galerkin parametrises the *value* $u$ and enforces the *differential equation* — and they exist because the classical curse of dimensionality (grid cost $\sim N^d$) is not shared by Monte Carlo or by gradient-based function approximation.**

Four things to carry out of this page:

1. **The loss is the whole algorithm.** Deep BSDE's loss is *only* the terminal mismatch — the dynamics are imposed *by construction* through the forward recursion $Y_{i+1}=Y_i+f\Delta t+Z_i\Delta W_i$. That is why it is often described as "a BSDE solved forward": there is no residual to estimate, hence no second derivatives, hence no discretisation of a differential operator.
2. **The trainable objects are the *hedge*, not the price.** The initial value $Y_0=\theta_0$ is a single scalar; everything else is $Z_t^\theta$. A solver that recovers the price but not the hedge has trained the 1-dimensional part of the problem and failed the infinite-dimensional part (§3 shows the price converging to $0.4\%$ while the hedge needs the same iterations to reach $0.2\%$).
3. **Deep BSDE is *not* inherently "deep".** The "deep" is in the *time* direction: the network is applied at each of $N$ time steps with shared or step-specific weights, so the composite map is $N$ layers deep. The per-step architecture is often shallow — a linear combination of a few features already reproduces Black–Scholes (§3).
4. **Dimension is the motivation.** For $d=100$ a finite-difference grid needs $\sim N^{100}$ nodes; the Deep BSDE of Han–Jentzen–E reaches $d=100$ with a handful of networks because the Monte Carlo error is dimension-free and the network represents the function compactly. This is *the* commercial argument for the method, and it applies to hedging (baskets, multi-factor models) exactly as it applies to pricing.

The practical objective: write down both loss functions, implement the Deep BSDE forward scheme with a from-scratch optimiser, understand why the terminal-mismatch loss contains no differential operator, and know the DGM residual's shape well enough to sanity-check it.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Deep BSDE loss (terminal-mismatch form)

Discretise $[0,T]$ into $N$ steps, $0=t_0<\dots<t_N=T$, $\Delta t=T/N$, $\Delta W_i=W_{t_{i+1}}-W_{t_i}$. Parametrise

$$Z_i^\theta=\varphi_i\big(X_{t_i};\theta_i\big),\qquad Y_0^\theta=\theta_0\ (\text{a scalar}),$$

and **define $Y$ by the forward recursion** (this is the whole trick — the backward SDE is turned into a forward one by treating $Y_0$ as the unknown):

$$\boxed{\ Y_{i+1}^\theta=Y_i^\theta+f\big(t_i,Y_i^\theta,Z_i^\theta\big)\Delta t+Z_i^\theta\,\Delta W_i,\qquad i=0,\dots,N-1\ }$$

and train by the *only* loss available,

$$\boxed{\ \theta^\star=\arg\min_\theta\ \mathbb E\Big[\big(\xi-Y_N^\theta\big)^2\Big]\ }$$

(E–Han–Jentzen 2017; E–Han–Jentzen 2018, PNAS). Why this is legitimate:

- **The dynamics are exact by construction.** Whatever $\theta$ is, the path $(Y_i^\theta)$ satisfies the *discretised* BSDE; only the terminal condition $Y_N=\xi$ can fail. Minimising the terminal mismatch therefore forces the discretised solution, and at the optimum $Y_0^\theta$ approximates $Y_0$ and $Z_i^\theta$ approximates $Z_{t_i}$.
- **No derivatives of the network appear.** The loss contains no $u_{xx}$; the drift of $Y$ is the driver, which is *known*. This is why Deep BSDE is easy to train relative to DGM.
- **The hedge comes for free.** $Z_t=\sigma^{\!\top}\nabla u$: the network *is* the hedge (in diffusive units). Deep BSDE is a hedging algorithm that happens to price.
- **Variance reduction is essential.** The gradient of the loss is an expectation over paths, so the Monte-Carlo error of the gradient is the training noise; antithetic sampling, common random numbers across iterations and batch-size control are what make it converge (see [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|NM · 04 Variance Reduction]]).

#### 2.2 The Deep Galerkin loss (residual form)

Parametrise the value directly, $u_\theta(t,x)$, and minimise the **PDE residual** on collocation points plus a terminal penalty,

$$\boxed{\ \mathcal L(\theta)=\underbrace{\big\|\partial_tu_\theta+Lu_\theta+f\big(t,u_\theta,\sigma^{\!\top}\nabla u_\theta\big)\big\|^2_{\text{collocation}}}_{\text{interior equation}}+\lambda\underbrace{\big\|u_\theta(T,\cdot)-g\big\|^2_{\text{boundary}}}_{\text{terminal condition}}\ }$$

(Sirignano–Spiliopoulos 2018). Because the residual is evaluated by sampling $(\Omega\times[0,T])$, the method needs **no mesh** — the same reason Monte Carlo beats finite differences in high dimension — but it demands second derivatives of the network ($Lu$ contains $\nabla^2u$), which are available by autodiff but noisy, and it must be trained to satisfy the terminal condition *and* the interior simultaneously (a balance that the weight $\lambda$ controls).

#### 2.3 The LSMC baseline (what the networks replace)

Before either method there was **least-squares Monte Carlo** (Longstaff–Schwartz 2001 for American options; Gobet–Lemor–Warin 2005 for BSDEs):

$$\widehat Y_{t_i}=\mathbb E\big[Y_{t_{i+1}}\mid X_{t_i}\big]+f\,\Delta t\ \ \text{estimated by regressing }Y_{t_{i+1}}\text{ on a basis of }X_{t_i},
\qquad
\widehat Z_{t_i}=\mathbb E\Big[Y_{t_{i+1}}\frac{\Delta W_i}{\Delta t}\ \Big|\ X_{t_i}\Big] .$$

The $Z$-estimator is exact for the *discretised* problem: since $\Delta W_i\perp\mathcal F_{t_i}$ and $\mathbb E[\Delta W_i^2]=\Delta t$, the martingale representation of $Y$ gives $\mathbb E[Y_{t_{i+1}}\Delta W_i/\Delta t\mid\mathcal F_{t_i}]=Z_{t_i}+O(\Delta t)$. The three methods then differ only in **the function class** used for the conditional expectation:

| method | function class for $E[Y_{t_{i+1}}\mid X_{t_i}]$ |
|---|---|
| LSMC (vanilla) | a fixed basis (polynomials, payoff functions) |
| LSMC + regression trees | trees / boosting (Longstaff–Schwartz's own suggestion) |
| Deep BSDE | a neural network, in the *time*-direction stack |
| Deep hedging | a neural network, applied to the *risk measure* over whole paths |

This table is the cleanest way to see the whole family: **the algorithms differ in what they plug into the regression slot, and in what they regress.**

---

### 3. Computational Implementation — Deep BSDE trained from scratch, and the DGM residual

We implement the Deep BSDE forward scheme with a **frozen-feature $Z$-net** — a one-hidden-layer network whose nonlinearities are fixed (`1, u, u², tanh`), leaving only the output weights trainable — so that the exact gradient is available in closed form and full-batch SGD needs no autodiff. That keeps the whole algorithm standard-library. We then verify the DGM residual loss on the same PDE with a one-parameter hypothesis class.

```python
import math, random

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bs_call(S0,K,r,s,T):
    d1=(math.log(S0/K)+(r+0.5*s*s)*T)/(s*math.sqrt(T)); return S0*N(d1)-K*math.exp(-r*T)*N(d1-s*math.sqrt(T))
def bs_delta(S0,K,r,s,T):
    d1=(math.log(S0/K)+(r+0.5*s*s)*T)/(s*math.sqrt(T)); return N(d1)
S0,K,r,sig,T=100.0,100.0,0.0,0.20,1.0

# ---- Deep BSDE (E-Han-Jentzen 2017) in the forward direction ----
#   Y_0 = theta (trainable); Y_{i+1} = Y_i + f(t_i,Y_i,Z_i)dt + Z_i.dW_i,  f = 0 here
#   Z_i = sum_k c[i][k] * phi_k(X_i/S0)   (a one-hidden-layer net with frozen nonlinearities)
#   loss = E[(Y_N - g(X_T))^2];  full-batch SGD
steps,npath,seed=4,20000,11
random.seed(seed); dt=T/steps; sq=math.sqrt(dt)
X=[[0.0]*(steps+1) for _ in range(npath)]; W=[[0.0]*steps for _ in range(npath)]
for p in range(npath):
    x=S0; X[p][0]=x
    for j in range(steps):
        W[p][j]=sq*random.gauss(0.0,1.0); x*=math.exp((r-0.5*sig*sig)*dt+sig*W[p][j]); X[p][j+1]=x
G=[max(X[p][steps]-K,0.0) for p in range(npath)]
def phi(u): return (1.0,u,u*u,math.tanh(3.0*(u-1.0)))
NF=4; NP=1+steps*NF
Phi=[[0.0]*NP for _ in range(npath)]
for p in range(npath):
    Phi[p][0]=1.0
    for i in range(steps):
        ph=phi(X[p][i]/S0)
        for k in range(NF): Phi[p][1+i*NF+k]=W[p][i]*ph[k]
def loss_and_grad(w):
    L=0.0; g=[0.0]*NP
    for p in range(npath):
        row=Phi[p]; YN=0.0
        for j in range(NP): YN+=row[j]*w[j]
        e=YN-G[p]; L+=e*e; ee=2.0*e
        for j in range(NP): g[j]+=ee*row[j]
    return L/npath,[x/npath for x in g]
w=[0.0]*NP; w[0]=7.0
for i in range(steps): w[1+i*NF+1]=0.5                       # start from a flat delta of 0.5
print("Deep-BSDE forward solver, European call, sigma=20%, T=1 (frozen-feature Z-net, SGD lr=0.5)")
print(f"analytic: call={bs_call(S0,K,r,sig,T):.6f}  delta={bs_delta(S0,K,r,sig,T):.6f}  Z_0={sig*S0*bs_delta(S0,K,r,sig,T):.6f}")
print(f"{'iter':>6}{'loss':>14}{'Y_0 (price)':>15}{'Z_0':>12}{'Z_0/(s*S0)':>13}")
for it in range(0,61):
    if it>0:
        _,g=loss_and_grad(w)
        for j in range(NP): w[j]-=0.5*g[j]
    if it in (0,1,3,10,30,60):
        Z0=sum(w[1+k]*phi(1.0)[k] for k in range(NF))
        print(f"{it:6d}{loss_and_grad(w)[0]:14.6f}{w[0]:15.6f}{Z0:12.6f}{Z0/(sig*S0):13.6f}")

# ---- Deep-Galerkin style residual loss: same backward PDE, one-parameter hypothesis class ----
#   PDE: u_t + (sigma^2/2) x^2 u_xx = 0,  u(T,x)=(x-K)^+.
#   Hypothesis class: u_theta(t,x) = Black-Scholes call with vol theta. The DGM loss is the
#   Monte-Carlo mean of the squared PDE residual over sampled (t,x); its minimiser must be theta=sigma.
print("")
print("Deep-Galerkin residual loss on  u_t + (sigma^2/2)x^2 u_xx = 0 , hypothesis u_theta = BS(theta)")
def Lres(t,x,theta):
    h=1e-4
    ut=(bs_call(x,K,r,theta,T-t-h)-bs_call(x,K,r,theta,T-t+h))/(2*h)      # d/dt u(t,x)
    uxx=(bs_call(x+h,K,r,theta,T-t)-2*bs_call(x,K,r,theta,T-t)+bs_call(x-h,K,r,theta,T-t))/(h*h)
    return ut+0.5*sig*sig*x*x*uxx
pts=[(0.01+0.98*random.random(),60.0+80.0*random.random()) for _ in range(400)]
print(f"   {'theta':>7}{'mean residual^2':>18}")
best=None
for i in range(0,37):
    th=0.10+0.005*i
    L=sum(Lres(t,x,th)**2 for t,x in pts)/len(pts)
    if best is None or L<best[1]: best=(th,L)
    if i%6==0: print(f"   {th:7.3f}{L:18.8f}")
print(f"   argmin theta = {best[0]:.3f}  (true sigma = {sig:.3f});  residual loss there = {best[1]:.3e}")
Z0=sum(w[1+k]*phi(1.0)[k] for k in range(NF))
print(f"   [Deep-BSDE network price Y_0={w[0]:.6f} vs Black-Scholes {bs_call(S0,K,r,sig,T):.6f},")
print(f"    network delta Z_0/(sigma S_0)={Z0/(sig*S0):.6f} vs Black-Scholes delta {bs_delta(S0,K,r,sig,T):.6f}]")
```
```
Deep-BSDE forward solver, European call, sigma=20%, T=1 (frozen-feature Z-net, SGD lr=0.5)
analytic: call=7.965567  delta=0.539828  Z_0=10.796557
  iter          loss    Y_0 (price)         Z_0   Z_0/(s*S0)
     0    161.973210       7.000000    0.500000     0.025000
     1     43.988169       8.020040    8.109287     0.405464
     3     33.832731       7.935635   10.562355     0.528118
    10     25.380790       7.930991   10.756827     0.537841
    30     18.071769       7.931348   10.793036     0.539652
    60     16.606330       7.933626   10.816050     0.540802

Deep-Galerkin residual loss on  u_t + (sigma^2/2)x^2 u_xx = 0 , hypothesis u_theta = BS(theta)
     theta   mean residual^2
     0.100       14.17102882
     0.130        6.50912865
     0.160        2.12684961
     0.190        0.13694936
     0.220        0.56783921
     0.250        3.66687299
     0.280        9.64419104
   argmin theta = 0.200  (true sigma = 0.200);  residual loss there = 2.553e-07
   [Deep-BSDE network price Y_0=7.933626 vs Black-Scholes 7.965567,
    network delta Z_0/(sigma S_0)=0.540802 vs Black-Scholes delta 0.539828]
```

**Reading the output.**

- **The Deep BSDE converges to the right price and the right hedge.** Loss falls $161.97\to16.61$; the price $Y_0$ goes from the initial guess $7.0000$ to $7.9336$ (Black–Scholes $7.9656$, a $0.4\%$ gap) and the hedge from $\delta=0.025$ (a deliberately wrong start) to $0.5408$ (Black–Scholes $0.5398$, $0.2\%$). By iteration $20$ both are essentially converged — the residual gap is the SGD step size, not a bias.
- **The floor of the loss is the discretisation, not the optimiser.** The loss bottoms out near $16.6$, i.e. an RMS terminal mismatch of $\sqrt{16.6}\approx4.1$ — the same order as the 4-step discrete-hedging error of [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]] ($\mathrm{SD}=3.32$ at $N{=}4$). A Deep BSDE loss that stops decreasing at a positive value is *not* a bug: it is the model's own residual. **This is the single most misread output of the whole method.**
- **The DGM residual has the right shape and the right minimiser.** The residual loss is $V$-shaped with an interior zero at $\theta=0.200$, exactly the true $\sigma$: the loss drops from $14.17$ ($\theta=0.10$) to $0.137$ ($\theta=0.19$), bottoms at $\theta=0.20$ with residual $2.55\times10^{-7}$ (finite-difference noise only), and rises again to $9.64$ at $\theta=0.28$. Note the *asymmetry*: the loss is larger and rises faster on the low-$\theta$ side, because the residual is $\propto(\sigma^2-\theta^2)$ — a useful reminder that a DGM loss is a *quadratic form in the wrong parameter*, and the network must find its minimum, not its "flat" region.
- **The $Z$-net matters more than the $Y$-scalar.** Sixteen of the seventeen trainable parameters sit in the $Z$-net ($4$ time steps $\times\ 4$ features); the price is one scalar. Everything in the convergence curve after iteration 3 is the *hedge* being refined. This is the algorithmic counterpart of the LSMC asymmetry of page 03.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading the loss floor as a training failure.** As above: a positive terminal-mismatch loss at the optimum is the *discretisation residual*. The correct diagnostic is whether the loss equals the model's own $\sqrt{\Delta t}$ hedging error, not whether it reaches zero.
2. **Not realising that with $f=0$ the price is *pinned* by the mean and all the learning is in $Z$.** Since $Z_i$ is $\mathcal F_{t_i}$-measurable and $\Delta W_i$ is independent of $\mathcal F_{t_i}$, $\mathbb E[Z_i\Delta W_i]=0$, so $\mathbb E[Y_N^\theta]=Y_0^\theta$ for *any* $Z$-net. Minimising $\mathbb E[(\xi-Y_N^\theta)^2]$ then forces $Y_0^\theta\to\mathbb E[\xi]$ (the mean-matching condition) and the $Z$-net can only reduce the *variance* of the mismatch. So in the linear case Deep BSDE is **variance-optimal hedging by variance reduction**, and a solver that converges to the right price has proved almost nothing about the hedge. (For $f\ne0$ the driver term breaks the mean-decoupling and $Y_0$ does depend on the strategy — another reason the entropic/quadratic case is genuinely more interesting than Black–Scholes.)
3. **Training the price and calling it a hedge.** $Y_0$ is one parameter; validate $Z$ against a known hedge — Black–Scholes in the complete-market limit, the BSDE $Z$ in an exactly-solvable case (page 03), or a finite-difference delta of an independently computed price. The price is not evidence about the strategy.
4. **Architecture mismatch between the $Z$-net and the true hedge.** The hedge is a function of the *state*; a $Z$-net that does not see the state (e.g. $Z_i$ a per-step constant) can never learn a delta that varies with moneyness. In the hub code the features are $(1,u,u^2,\tanh)$ in $u=X/S_0$ — chosen because the Black–Scholes delta is a smooth sigmoid-like function of $u$. A feature set that cannot represent the true $\nabla u$ produces a *bias*, not noise.
5. **Learning rate as a landmine.** [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]] shows the identical loss and data converging at $\mathrm{lr}=0.30$ and exploding at $1.50$; the stability threshold scales with the largest eigenvalue of the Monte-Carlo design matrix, which grows with the number of paths and the magnitude of the $Z$-features. There is no "safe default" — the learning rate must be tuned per problem, and the loss curve must be watched.
6. **Ignoring the SGD noise floor.** Full-batch SGD on a Monte-Carlo loss has gradient noise $\propto1/\sqrt{n_{\text{paths}}}$. Small learning rates stall above the true optimum; large rates bounce around it. The observable is the *variance of the loss across the last iterations*, not its mean.
7. **Using Deep Galerkin where Deep BSDE is appropriate (and vice versa).** DGM needs $\nabla^2u_\theta$: for a rough value function (digital payoffs at the money, barriers, early exercise) the second derivative is singular and the residual loss diverges. Deep BSDE integrates along paths and never differentiates the value — better for non-smooth payoffs. Conversely, DGM gives a *function* $u(t,x)$ for all $(t,x)$ and handles free boundaries naturally, which is why it is the method of choice for [[pillars/03-derivative-pricing/american-options-and-optimal-stopping|American options]] and [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/02-optimal-stopping-theory|obstacle/PDE formulations]].
8. **Assuming dimension-freeness means accuracy-freeness.** Monte Carlo error is dimension-free in *rate*, not in *constant*: for a $d$-dimensional problem the variance of the terminal mismatch grows with $d$ (a basket option has more residual risk), so the path count needed for a fixed accuracy grows. The correct claim is "$O(n^{-1/2})$ in *any* dimension", not "equally accurate in any dimension".
9. **Forgetting the barrier/terminal treatments.** Deep BSDE samples paths *forward*: a barrier or early-exercise feature must be encoded in the terminal condition or in the driver, and a naive implementation prices a *different* contract. DGM encodes it as a boundary penalty. In both cases the encoding error is silent.

---

### 5. Canonical Literature & Study References

- **E, W., Han, J., Jentzen, A.** (2017), *Deep learning-based numerical methods for high-dimensional parabolic partial differential equations and backward stochastic differential equations*, Communications in Mathematics and Statistics 5(4), 349–380 — the Deep BSDE algorithm. **Han, J., Jentzen, A., E, W.** (2018), *Solving high-dimensional partial differential equations using deep learning*, PNAS 115(34), 8505–8510 — the flagship $d=100$ demonstration (Hamilton–Jacobi–Bellman, Allen–Cahn, the Black–Scholes–Barenblatt equation). *The primary sources for §2.1 and §3.*
- **Sirignano, J. & Spiliopoulos, K.** (2018), *DGM: a deep learning algorithm for solving partial differential equations*, Journal of Computational Physics 375, 1339–1364 — the Deep Galerkin method of §2.2, with the residual-plus-boundary loss and the LSTM-style architecture. **Raissi, M., Perdikaris, P., Karniadakis, G.E.** (2019), *Physics-informed neural networks*, Journal of Computational Physics 378, 686–707 — the same residual-loss idea, different community.
- **Pham, H., Warin, X., Germain, M.** (2020), *Neural networks-based backward scheme for fully nonlinear PDEs*, SN Partial Differential Equations and Applications 2(16) — the "BSDE2" variant (network conditioned on the *whole* Brownian path). **Huré, C., Pham, H., Bachouch, A., Langrené, N.** (2021), *Deep neural networks algorithms for stochastic control problems on finite horizon* (Part I: convergence analysis; Part II: numerical simulations) — value-iteration Deep BSDE, the link to the dynamic programming of deep hedging. **Han, J., E, W.** (2016), *Deep learning approximation for stochastic control problems*.
- **Longstaff, F. & Schwartz, E.** (2001), *Valuing American options by simulation: a simple least-squares approach*, Review of Financial Studies 14(1), 113–147 — LSMC, the regression primitive that all the network methods generalise. **Gobet, E., Lemor, J.-P., Warin, X.** (2005), *A regression-based Monte Carlo method to solve backward stochastic differential equations*, Annals of Applied Probability 15(3), 2172–2202 — the BSDE version of the $Z$-regression. **Bender, C. & Steiner, J.** (2012), *Least-squares Monte Carlo for BSDEs*.
- **Buehler, H., Gonon, L., Teichmann, J., Wood, B.** (2019), *Deep Hedging*, Quantitative Finance 19(8), 1271–1291 — the same forward-scheme + neural-network architecture applied to the *risk measure* over the whole path instead of the terminal mismatch. **Buehler et al.** (2019), *Deep hedging: learning to simulate, hedge and price under market frictions*. **Fecamp, S., Mikael, J., Badran, M.** (2020), *Deep learning for discrete-time hedging in incomplete markets*, Journal of Computational Finance.
- **Beck, C., Becker, S., Cheridito, P., Jentzen, A., Neufeld, A.** (2019), *Deep splitting method for parabolic PDEs*; **Beck, C., E, W., Jentzen, A.** (2019), *Machine learning approximation algorithms for high-dimensional fully nonlinear PDEs and second-order BSDEs* — the $2$BSDE extension (nonlinear in the Hessian — the VIX/rough-vol world). **Gnoatto, A., Patacca, M., Picarelli, A.** (2023), *A deep solver for BSDEs with jumps* — the jump case, relevant to [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston/SABR · 06]].

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/03-bsdes-and-nonlinear-feynman-kac|03 · BSDEs & Nonlinear Feynman–Kac]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/02-convex-risk-and-the-deep-hedging-objective|02 · Convex Risk & the Objective]]
- Forward: [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Index Hub]]
- Numerics: [[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods]] · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|NM · 03 Monte-Carlo Pricing]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|NM · 04 Variance Reduction]] · [[foundations/numerical-methods/04-numerical-optimization|NM · 04 Numerical Optimization]] · [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|C&O · 05 Gradient & Newton Methods]]
- PDE / boundary cases: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|American Options & Optimal Stopping]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|American · 04 Free Boundary & Complementarity]] · [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|NM · 02 Finite-Difference Methods]]
- ML: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Reinforcement Learning for Trading]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|RL · 04 Policy Gradient & Actor-Critic]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]

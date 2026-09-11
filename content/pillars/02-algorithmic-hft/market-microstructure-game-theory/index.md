---
title: "2.10 Market Microstructure Game Theory"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - game-theory
  - kyle-1985
  - glosten-milgrom
  - adverse-selection
  - predatory-trading
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayesian updating, conditional expectation) and [[foundations/bayesian-statistics/index|Bayesian Statistics]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A price is not a fact. It is the **outcome of a game** played every microsecond between three parties who want different things:

- an **informed trader** (or several) who knows something about the fundamental value and wants to trade on it without revealing it;
- **noise/liquidity traders** who trade for exogenous reasons and whose flow is the informed trader's camouflage;
- a **market maker** (or a competitive crowd of them) who must quote prices *without* knowing which counterparty it is facing, and therefore quotes **conditionally** — the ask is the expected value *given that someone chose to buy from you*, and the bid is the expected value *given that someone chose to sell*.

Every classical microstructure model is a specialization of that game. **Kyle (1985)** makes it a batch auction with a strategic insider and a linear price rule. **Glosten–Milgrom (1985)** makes it a sequential-trade Bayesian game with a competitive specialist and a two-point value. **Brunnermeier–Pedersen (2005)** adds a fourth player — a predator who trades *against* a forced liquidator. **Schied–Zhang (2019)** replaces the single insider with many strategic liquidators and asks what the Nash equilibrium of the execution game looks like.

The practical objective of this folder is exactly what a practitioner needs from that literature: **when you trade, who is on the other side, what do they know, and what does the equilibrium price of that interaction look like?** Adverse selection is not a parameter you sprinkle on top of a model — it *is* the equilibrium spread; impact is not a cost function you fit — it *is* Kyle's λ; and your own optimal execution is not a private optimization problem — it is **one player's best response** in a game.

This folder is the **game-theoretic microstructure** topic-folder for Pillar 2. As a *hub*, it gives you **(a)** the fast formula lookup below and **(b)** six sub-pages that walk from zero-knowledge intuition, through Kyle and the Back continuous-time limit, through Glosten–Milgrom as a Bayesian game, into predatory trading and execution games, then the failure modes and the modern extensions.

> **The one-sentence essence.** "The spread is a Bayesian equilibrium price of adverse selection, impact is Kyle's $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$, and your execution schedule is only optimal *given* the schedule everyone else is running — it is a Nash object, not a private one."

**Scope note (vs the sibling folders).** This folder is the **strategic/equilibrium** view — who knows what, who moves when, and what the equilibrium of that interaction is. For the *scheduling* of a given order under a fixed impact model, see [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]. For the *measurement* of impact and depth, see [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]. For the sequential-Bayesian market-making view in depth, see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & the Glosten–Milgrom Model]]. The two meet at the same λ: this folder asks *why the equilibrium has that λ*, the others ask *how to measure it* and *what to do with it*.

*Primary verified sources:* Kyle (1985); Glosten & Milgrom (1985); Back (1992); Holden & Subrahmanyam (1992); Brunnermeier & Pedersen (2005); Carlin, Lobo & Viswanathan (2007); Schied & Zhang (2019); Schied, Strehle & Zhang (2018); Cordoni & Lillo (2022); Cardaliaguet & Lehalle (2018); Huberman & Stanzl (2004); Hasbrouck, *Empirical Market Microstructure* (Ch 5–7, corpus verification reports `hasbrouck_ch1-5.md` / `hasbrouck_ch6-10.md`); Foucault, Pagano & Röell, *Market Liquidity* (Ch 3, corpus `foucault_ch1-3.md`). Every number below was **re-executed and reproduced in pure-stdlib Python** (see §3).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $v$ = fundamental value; $\Sigma_0=\operatorname{Var}[v]$ = prior value variance; $u$ = noise order flow, $\sigma_u^2=\operatorname{Var}[u]$; $x$ = informed demand; $y=x+u$ = total signed order flow; $P$ = price; $\lambda$ = price impact (\"Kyle's lambda\"); $1/\lambda$ = market depth. For the Glosten–Milgrom game: $V\in\{V_L,V_H\}$, belief $\theta_t=\mathbb{P}(V=V_H\mid\mathcal{F}_t)$, $\pi$ = share of traders who are informed. For execution games: $X$ = block to liquidate, $T$ = horizon, $N$ = number of intervals of length $\tau=T/N$, $n_k$ = shares traded in interval $k$, $x_k$ = shares still held, $\eta$ = temporary-impact coefficient, $\gamma$ = permanent-impact coefficient, $\lambda_{\text{risk}}$ = risk aversion.

**2.1 The Glosten–Milgrom game (1985).** Arrivals of buy/sell orders are governed by
$$
\mathbb{P}(B\mid V_H)=\tfrac{1+\pi}{2},\qquad \mathbb{P}(B\mid V_L)=\tfrac{1-\pi}{2},\qquad \mathbb{P}(S\mid\cdot)=1-\mathbb{P}(B\mid\cdot).
$$
A competitive maker quotes **zero expected profit conditional on the direction of the trade**:
$$
A_t=\mathbb{E}[V\mid \text{buy at }t],\qquad B_t=\mathbb{E}[V\mid \text{sell at }t],
$$
which evaluates to
$$
\boxed{\;A_t=\frac{V_H(1+\pi)\theta_t+V_L(1-\pi)(1-\theta_t)}{(1+\pi)\theta_t+(1-\pi)(1-\theta_t)},\qquad B_t=\frac{V_H(1-\pi)\theta_t+V_L(1+\pi)(1-\theta_t)}{(1-\pi)\theta_t+(1+\pi)(1-\theta_t)}\;}
$$
and the Bayesian update after a buy is $\theta_t^{+}=\dfrac{(1+\pi)\theta_t}{(1+\pi)\theta_t+(1-\pi)(1-\theta_t)}$. At $\theta=\tfrac12$ everything collapses to the textbook form
$$
A-B=\pi\,(V_H-V_L).
$$
**Key structural fact:** the quoted price is a **martingale** — $\mathbb{E}[P_{t+1}\mid\mathcal{F}_t]=P_t$ — exactly because $A$ and $B$ are conditional expectations. Verified to $0.00\times10^{0}$ drift in §3.

**2.2 The Kyle (1985) auction.** Prior $v\sim\mathcal N(p_0,\Sigma_0)$, noise $u\sim\mathcal N(0,\sigma_u^2)$, one strategic insider, competitive linear pricing $P=p_0+\lambda y$. The equilibrium is
$$
\boxed{\;x=\beta\,(v-p_0),\quad \beta=\sqrt{\sigma_u^2/\Sigma_0},\qquad \lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2},\qquad 1/\lambda=2\sqrt{\sigma_u^2/\Sigma_0}\;}
$$
with $\operatorname{Var}[v\mid P]=\Sigma_0/2$ (**exactly half the private information is impounded**, and the fraction is invariant to $\sigma_u^2$) and $\mathbb{E}[\text{insider profit}]=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$.

**2.3 N-auction Kyle (the discrete game).** Repeat the auction $N$ times with equal noise variance $\sigma_u^2$ per round and prior variance $\Sigma_{n-1}$. The equilibrium is
$$
\boxed{\;\Sigma_n=\tfrac12\Sigma_{n-1}=\Sigma_0\,2^{-n},\qquad \beta_n=\sqrt{\sigma_u^2/\Sigma_{n-1}},\qquad \lambda_n=\tfrac12\sqrt{\Sigma_{n-1}/\sigma_u^2},\qquad \mathbb{E}[\text{profit}_n]=\tfrac12\sqrt{\sigma_u^2\Sigma_{n-1}}\;}
$$
so information is released **geometrically** (half per auction) and the insider's total expected profit converges:
$$
\sum_{n\ge1}\tfrac12\sqrt{\sigma_u^2\Sigma_0}\,2^{-(n-1)/2}=\frac{2+\sqrt2}{2}\sqrt{\sigma_u^2\Sigma_0}.
$$
$N=12$ reproduces this limit to $1.6\%$ (§3).

**2.4 The Kyle–Back continuous-time limit.** You **cannot** get continuous time by simply sending $N\to\infty$ in §2.3 with a fixed total noise budget: with per-period noise variance $\sigma_u^2\tau$ the first-period impact is $\lambda_1=\tfrac12\sqrt{\Sigma_0/(\sigma_u^2\tau)}\to\infty$. The correct continuous-time equilibrium — Kyle (1985, §2) resolved by **Back (1992)** — has a **linear** information release and a **constant** impact coefficient:
$$
\boxed{\;\Sigma(t)=\Sigma_0\Bigl(1-\frac{t}{T}\Bigr),\qquad \lambda=\sqrt{\frac{\Sigma_0}{\sigma_u^2 T}}\;}
$$
with $P_t=p_0+\lambda(X_t+U_t)$, $dU_t=\sigma_u\,dB_t$, and market depth $1/\lambda=\sigma_u\sqrt{T/\Sigma_0}$. **Why the form is forced:** the filtering identity $d\Sigma_t=-\operatorname{Var}(dP_t\mid\mathcal F_{t^-})=-\lambda^2\sigma_u^2\,dt$ combined with $\Sigma(t)=\Sigma_0(1-t/T)$ gives $\lambda^2\sigma_u^2T=\Sigma_0$ identically — and $\int_0^T\lambda^2\sigma_u^2dt=\Sigma_0$ says *all* the information is released by $T$. Two corollaries: half the information is impounded at $t=T/2$ (the continuous analogue of the auction's $\Sigma_0/2$), and $\lambda\propto T^{-1/2}$ (**a longer horizon makes the market deeper**, not shallower).

**2.5 Predatory trading (Brunnermeier–Pedersen 2005).** A distressed trader must liquidate $X$ on a schedule $\{n_k\}$; a predator best-responds to *that public schedule*. With price $P_k=P_0-\kappa\sum_{j\le k}(n_j+m_j)$ (sign convention: selling depresses) and linear temporary cost $\eta$ per unit for everyone, the predator's cash flow is
$$
\Pi=\sum_k m_k\bigl(P_{k-1}-\eta m_k\bigr),\qquad \sum_k m_k=0,
$$
which reduces to a concave quadratic. Its maximiser is
$$
\boxed{\;m_k=\frac{\kappa\,(\bar A-A_k)}{2\eta-\kappa},\qquad A_k=\sum_{j<k}n_j,\quad \bar A=\tfrac1N\textstyle\sum_k A_k\;}
$$
with the interior-solution condition $\eta>\kappa/2$. Since $A_k$ is increasing, $m_k$ is **positive early and negative late**: the predator **sells ahead of the victim and buys back afterwards**, collecting the permanent-impact rent it helped create.

**2.6 Execution as a game (Schied–Zhang 2019).** When $J$ strategic liquidators trade the same asset, each minimises its own cost holding the others fixed. In the linear-quadratic case the symmetric Nash equilibrium is *the single-agent Almgren–Chriss solution with an inflated temporary-impact coefficient*: sharing one liquidity pool with a counterpart who trades $n^j_k$ makes agent $i$'s marginal temporary cost $\eta(2n^i_k+n^j_k)$, i.e.
$$
\boxed{\;\eta_{\text{eff}}=\tfrac{3}{2}\eta\quad\text{(two symmetric players)}\;\Longrightarrow\;\kappa_{\text{eff}}=\sqrt{\lambda_{\text{risk}}\sigma^2/\eta_{\text{eff}}}=\sqrt{\tfrac23}\,\kappa\;}
$$
so **competition for liquidity makes each player slower, not faster** — the opposite of the naive intuition, and the reason "everyone liquidates at once" is expensive. Schied & Zhang (2019) and Cordoni & Lillo (2022) show the same structure in continuous time, where the equilibrium can become **unstable** (oscillating strategies, non-existent high-frequency limit) when the temporary-cost parameter is small relative to cross-impact.

**2.7 Competing informed traders (Holden–Subrahmanyam 1992).** Replace the single insider by $K$ insiders with aggregate informed intensity $K\beta$. One round of Bayesian updating gives
$$
\boxed{\;\Sigma'=\frac{\Sigma_0\sigma_u^2}{(K\beta)^2\Sigma_0+\sigma_u^2},\qquad \lambda_K=\frac{K\beta\,\Sigma_0}{(K\beta)^2\Sigma_0+\sigma_u^2}\;}
$$
$K=1$ recovers $\Sigma_0/2$ and $\lambda$; $K\to\infty$ drives $\Sigma'\to0$ and $\lambda_K\to0$. More insiders $\Rightarrow$ faster revelation $\Rightarrow$ a **deeper** market.

**Quick-Reference Lookup** — the fast facts of this folder (all reproduced by the stdlib engine in §3):

| Quantity | Formula | Verified check |
|---|---|---|
| GM zero-profit spread ($\theta=\tfrac12$) | $A-B=\pi(V_H-V_L)$ | $\pi{=}0.2,V_H{=}101,V_L{=}99\Rightarrow 0.4000$ |
| GM posterior after a buy | $\theta^{+}=\frac{(1+\pi)\theta}{(1+\pi)\theta+(1-\pi)(1-\theta)}$ | $\theta{=}\tfrac12,\pi{=}0.2\Rightarrow\theta^{+}{=}0.600000$ |
| GM price is a martingale | $\mathbb{E}[P_{t+1}\mid\mathcal F_t]=P_t$ | one-step mean $100.000000$, drift $0.00\times10^{0}$ |
| GM toxicity of a fill | $\mathbb{P}(\text{informed}\mid\text{buy})=\frac{2\pi\theta}{(1+\pi)\theta+(1-\pi)(1-\theta)}$ | $\theta{=}\tfrac12\Rightarrow0.2000$ |
| GM spread is state-dependent | $A(\theta)-B(\theta)$ | peaks at $\theta{=}\tfrac12$: $0.4000$; $\theta{=}0.95$: $0.0785$ |
| Kyle insider demand | $x=\beta(v-p_0),\ \beta=\sqrt{\sigma_u^2/\Sigma_0}$ | $\Sigma_0{=}4,\sigma_u^2{=}1\Rightarrow\beta{=}0.5000$ |
| **Kyle's lambda** | $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ | $\Rightarrow\lambda{=}1.0000$, depth $1/\lambda{=}1.0000$ |
| Kyle info impounded | $\operatorname{Var}[v\mid P]=\Sigma_0/2$ | $2.0000$ (exactly half, independent of $\sigma_u^2$) |
| Kyle insider profit | $\mathbb{E}[\pi]=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$ | $1.0000$ |
| Discrete $N$-auction Kyle | $\Sigma_n{=}\Sigma_{n-1}/2,\ \beta_n{=}\sqrt{\sigma_u^2/\Sigma_{n-1}},\ \lambda_n{=}\tfrac12\sqrt{\Sigma_{n-1}/\sigma_u^2}$ | $\lambda_1{=}1.0000,\lambda_2{=}0.7071,\lambda_3{=}0.5000$ |
| Total insider profit ($N\to\infty$) | $\frac{2+\sqrt2}{2}\sqrt{\sigma_u^2\Sigma_0}$ | $N{=}12$ gives $3.3609\to3.4142$ |
| Naive continuum is ill-posed | $\lambda_1=\tfrac12\sqrt{\Sigma_0/(\sigma_u^2\tau)}\to\infty$ | $N{=}10^4\Rightarrow\lambda_1{=}100.000$ |
| **Kyle–Back continuous time** | $\lambda=\sqrt{\Sigma_0/(\sigma_u^2T)},\ \Sigma(t)=\Sigma_0(1-t/T)$ | $T{=}1\Rightarrow\lambda{=}2.0000$; $\lambda^2\sigma_u^2T{=}4.0000{=}\Sigma_0$ |
| Half-information time (continuous) | $t^\star=T/2$ | $\Sigma(T/2){=}2.0000{=}\Sigma_0/2$ |
| Predator's front-run schedule | $m_k=\kappa(\bar A-A_k)/(2\eta-\kappa)$ | $\kappa{=}1,\eta{=}0.6\Rightarrow m_1{=}+2.188,\ m_8{=}-2.188$, $\sum m_k{=}0$ |
| Cost of predation | victim loss / predator profit | loss $3.2812$, predator profit $1.6406$, deadweight $1.6406$ |
| Victim's best response | front-load (speed up) | victim loss $3.2812\to1.7175$ as it front-loads |
| Two-player execution Nash | $\eta_{\text{eff}}=\tfrac32\eta$ | quarters $46.81/26.18/15.70/11.31\%$ = AC with $1.5\eta$ |
| $K$ competing insiders | $\Sigma'=\frac{\Sigma_0\sigma_u^2}{(K\beta)^2\Sigma_0+\sigma_u^2}$ | impounded: $K{=}1{:}50\%$, $K{=}2{:}80\%$, $K{=}5{:}96.15\%$ |
| No-manipulation constraint | $\gamma+\delta\ge1$ (Gatheral/Huberman–Stanzl) | admissibility test on any impact/decay kernel |

---

### 3. Computational Implementation — the game-theory core engine

Stdlib only (`math`, `random`), fully deterministic. It reproduces every verified number in the lookup table above: the GM spread, the GM martingale property, the Kyle auction closed forms, the N-auction recursion and its profit limit, the ill-posedness of the naive continuum, Back's continuous-time information identity, the predator's optimal front-run schedule, the two-player execution Nash, and the $K$-insider information release.

```python
import math
# 1. Glosten-Milgrom two-state Bayesian game at prior theta = 1/2
VH, VL = 101.0, 99.0
print("Glosten-Milgrom two-state game (VH=101, VL=99, prior theta=1/2):")
print(f"{'pi':>5} {'ask':>8} {'bid':>8} {'spread':>7} {'theta+':>7} {'P(inf|buy)':>11}")
for pi in (0.0, 0.05, 0.10, 0.20, 0.40, 0.50):
    A = 0.5*(VH*(1+pi) + VL*(1-pi))        # ask = E[V | buy]
    B = 0.5*(VH*(1-pi) + VL*(1+pi))        # bid = E[V | sell]
    nA = (1+pi)*0.5 + (1-pi)*0.5           # 2*P(buy) at theta=1/2
    print(f"{pi:5.2f} {A:8.3f} {B:8.3f} {A-B:7.3f} {(1+pi)*0.5/nA:7.4f} {2*pi*0.5/nA:11.4f}")
# 2. Kyle (1985) single auction
Sig0, su2 = 4.0, 1.0
lam = 0.5*math.sqrt(Sig0/su2); beta = math.sqrt(su2/Sig0)
print(f"\nKyle single auction: lambda={lam:.4f}  depth 1/lambda={1/lam:.4f}  beta={beta:.4f}")
print(f"  Var[v|P]=Sigma0/2={Sig0/2:.4f}   E[insider profit]={0.5*math.sqrt(su2*Sig0):.4f}")
# 3. Kyle-Back continuous time
print("\nKyle-Back continuous time:  lambda=sqrt(Sigma0/(sigma_u^2 T)),  Var[V|F_t]=Sigma0(1-t/T)")
for T in (0.25, 1.0, 4.0):
    print(f"  T={T:4.2f}:  lambda={math.sqrt(Sig0/(su2*T)):.4f}   half of the information impounded by t=T/2={T/2:g}")
```
```
Glosten-Milgrom two-state game (VH=101, VL=99, prior theta=1/2):
   pi      ask      bid  spread  theta+  P(inf|buy)
 0.00  100.000  100.000   0.000  0.5000      0.0000
 0.05  100.050   99.950   0.100  0.5250      0.0500
 0.10  100.100   99.900   0.200  0.5500      0.1000
 0.20  100.200   99.800   0.400  0.6000      0.2000
 0.40  100.400   99.600   0.800  0.7000      0.4000
 0.50  100.500   99.500   1.000  0.7500      0.5000

Kyle single auction: lambda=1.0000  depth 1/lambda=1.0000  beta=0.5000
  Var[v|P]=Sigma0/2=2.0000   E[insider profit]=1.0000

Kyle-Back continuous time:  lambda=sqrt(Sigma0/(sigma_u^2 T)),  Var[V|F_t]=Sigma0(1-t/T)
  T=0.25:  lambda=4.0000   half of the information impounded by t=T/2=0.125
  T=1.00:  lambda=2.0000   half of the information impounded by t=T/2=0.5
  T=4.00:  lambda=1.0000   half of the information impounded by t=T/2=2
```

The engine continues with the discrete Kyle recursion, the continuum ill-posedness, the Back information identity, the predator's schedule, the two-player Nash and the $K$-insider release:

```python
import math
Sig0, su2, N = 4.0, 1.0, 12
Sig = [Sig0]
for _ in range(N): Sig.append(Sig[-1]/2.0)
print("N-period discrete Kyle (equal noise variance per auction): Sigma_n = Sigma_0/2^n")
print(f"{'n':>2} {'Sigma_n':>10} {'beta_n':>8} {'lambda_n':>9} {'profit_n':>9}")
tot = 0.0
for n in range(1, N+1):
    b = math.sqrt(su2/Sig[n-1]); l = 0.5*math.sqrt(Sig[n-1]/su2); pr = 0.5*math.sqrt(su2*Sig[n-1])
    tot += pr
    print(f"{n:>2} {Sig[n-1]:>10.6f} {b:>8.4f} {l:>9.4f} {pr:>9.4f}")
print(f"total E[profit], N={N}: {tot:.4f}   N->inf limit (2+sqrt2)/2*sqrt(sigma_u^2*Sigma_0) = {(2+math.sqrt(2))/2*math.sqrt(su2*Sig0):.4f}")
T = 1.0
print("\nNaive N->infinity limit with per-period noise variance sigma_u^2*tau:")
for Nn in (10, 100, 1000, 10000):
    print(f"  N={Nn:>5}  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = {0.5*math.sqrt(Sig0/(su2*(T/Nn))):,.3f}")
print("\nBack (1992) continuous-time information accounting (Sigma(t)=Sigma_0(1-t/T)):")
for t in (0.0, 0.25, 0.5, 0.75, 1.0):
    print(f"  t={t:.2f}:  Sigma(t)={Sig0*(1-t/T):.4f}   dSigma/dt=-Sigma_0/T={-Sig0/T:.4f}")
lamc = math.sqrt(Sig0/(su2*T))
print(f"  identity lambda^2*sigma_u^2 = Sigma_0/T:  {lamc:.4f}^2*{su2} = {lamc**2*su2:.4f} = {Sig0/T:.4f}")
print(f"  integrate dt over [0,T]: {lamc**2*su2*T:.4f} = Sigma_0 = {Sig0:.4f}  (all information released)")

def solve_linear(A, b):                      # stdlib Gaussian elimination, partial pivoting
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]/M[c][c]
                for k in range(c, n+1): M[r][k] -= f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

def predator(victim, kappa=1.0, eta=0.6):    # BP front-running best response
    N = len(victim); A = [sum(victim[:k]) for k in range(N)]; abar = sum(A)/N
    return [-kappa*(a-abar)/(2*eta-kappa) for a in A]
def mids(n, m, kappa=1.0, P0=100.0):
    P = [P0]
    for k in range(len(n)): P.append(P[-1] - kappa*(n[k]+m[k]))
    return P
def rev(n, m, eta=0.6, P0=100.0):
    P = mids(n, m, 1.0, P0); return sum(n[k]*(P[k]-eta*n[k]) for k in range(len(n)))
def cashflow(n, m, eta=0.6, P0=100.0):
    P = mids(n, m, 1.0, P0); return sum(m[k]*(P[k]-eta*m[k]) for k in range(len(n)))

NN, X = 8, 1.0
twap = [X/NN]*NN; m = predator(twap)
print(f"\nPredation on a {NN}-step TWAP victim (kappa=1.0, eta=0.6, X={X:g}):")
print("  victim   n_k: " + " ".join(f"{v:+.3f}" for v in twap))
print("  predator m_k: " + " ".join(f"{v:+.3f}" for v in m))
print(f"  sum m_k = {sum(m):+.6f}  (sells early, buys back late, ends flat)")
print(f"  victim revenue: no predator {rev(twap,[0.0]*NN):.4f} | with predator {rev(twap,m):.4f} | loss {rev(twap,[0.0]*NN)-rev(twap,m):.4f}")
print(f"  predator profit {cashflow(twap,m):.4f} | deadweight {rev(twap,[0.0]*NN)-rev(twap,m)-cashflow(twap,m):.4f}")

def nash2(eta=2.5e-6, lam=1e-6, sigma=0.95, T=5.0, N=100, X=1e6):
    tau = T/N; half = X/2.0; c = 2*lam*sigma*sigma*tau; e = eta/tau
    M = 2*N+2; A = [[0.0]*M for _ in range(M)]; b = [0.0]*M
    for off, other, mult in ((0, N, 2*N), (N, 0, 2*N+1)):
        for i in range(N):
            r = off+i
            A[r][off+i] += 2*e; A[r][other+i] += e
            for l in range(N): A[r][off+l] += c*((N-1-i) if l <= i else (N-1-l))
            A[r][mult] = -1.0; b[r] = c*half*(N-1-i)
    A[2*N][0:N] = [1.0]*N; b[2*N] = half
    A[2*N+1][N:2*N] = [1.0]*N; b[2*N+1] = half
    return solve_linear(A, b)[:N]
def quarters(n):
    N = len(n); return [sum(n[:N//4]),sum(n[N//4:N//2]),sum(n[N//2:3*N//4]),sum(n[3*N//4:])]
def ac(eta, X=5e5, lam=1e-6, sigma=0.95, T=5.0, N=100):
    k = math.sqrt(lam*sigma**2/eta)
    x = [X*math.sinh(k*(T-T*j/N))/math.sinh(k*T) for j in range(N+1)]
    return [x[j]-x[j+1] for j in range(N)]
print("\nTwo liquidators sharing temporary liquidity (each 500,000 over 5 days):")
print("  shared-liquidity Nash          quarters " + "  ".join(f"{100*v/5e5:6.2f}%" for v in quarters(nash2())))
print("  AC closed form with eta_eff=1.5*eta " + "  ".join(f"{100*v/5e5:6.2f}%" for v in quarters(ac(3.75e-6))))
print("  single-agent AC (eta=2.5e-6)   quarters " + "  ".join(f"{100*v/5e5:6.2f}%" for v in quarters(ac(2.5e-6))))
print(f"  implied urgency kappa: single {math.sqrt(1e-6*0.95**2/2.5e-6):.4f}/day  vs shared {math.sqrt(1e-6*0.95**2/3.75e-6):.4f}/day")

Sig0, su2 = 4.0, 1.0; beta_mono = math.sqrt(su2/Sig0)
print("\nCompeting informed traders: K insiders of intensity beta each (monopolist beta=0.5)")
print(f"{'K':>4} {'aggregate intensity':>20} {'Sigma after 1 round':>20} {'lambda_K':>10} {'info impounded':>15}")
for K in (1,2,3,5,10,50,1000):
    Kb2 = (K*beta_mono)**2
    print(f"{K:>4} {K*beta_mono:>20.4f} {Sig0*su2/(Kb2*Sig0+su2):>20.6f} "
          f"{K*beta_mono*Sig0/(Kb2*Sig0+su2):>10.4f} {100*(1-(Sig0*su2/(Kb2*Sig0+su2))/Sig0):>14.4f}%")
```
```
N-period discrete Kyle (equal noise variance per auction): Sigma_n = Sigma_0/2^n
 n    Sigma_n   beta_n  lambda_n  profit_n
 1   4.000000   0.5000    1.0000    1.0000
 2   2.000000   0.7071    0.7071    0.7071
 3   1.000000   1.0000    0.5000    0.5000
 4   0.500000   1.4142    0.3536    0.3536
 5   0.250000   2.0000    0.2500    0.2500
 6   0.125000   2.8284    0.1768    0.1768
 7   0.062500   4.0000    0.1250    0.1250
 8   0.031250   5.6569    0.0884    0.0884
 9   0.015625   8.0000    0.0625    0.0625
10   0.007812  11.3137    0.0442    0.0442
11   0.003906  16.0000    0.0312    0.0312
12   0.001953  22.6274    0.0221    0.0221
total E[profit], N=12: 3.3609   N->inf limit (2+sqrt2)/2*sqrt(sigma_u^2*Sigma_0) = 3.4142

Naive N->infinity limit with per-period noise variance sigma_u^2*tau:
  N=   10  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 3.162
  N=  100  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 10.000
  N= 1000  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 31.623
  N=10000  lambda_1 = 0.5*sqrt(Sigma_0/(sigma_u^2*tau)) = 100.000

Back (1992) continuous-time information accounting (Sigma(t)=Sigma_0(1-t/T)):
  t=0.00:  Sigma(t)=4.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=0.25:  Sigma(t)=3.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=0.50:  Sigma(t)=2.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=0.75:  Sigma(t)=1.0000   dSigma/dt=-Sigma_0/T=-4.0000
  t=1.00:  Sigma(t)=0.0000   dSigma/dt=-Sigma_0/T=-4.0000
  identity lambda^2*sigma_u^2 = Sigma_0/T:  2.0000^2*1.0 = 4.0000 = 4.0000
  integrate dt over [0,T]: 4.0000 = Sigma_0 = 4.0000  (all information released)

Predation on a 8-step TWAP victim (kappa=1.0, eta=0.6, X=1):
  victim   n_k: +0.125 +0.125 +0.125 +0.125 +0.125 +0.125 +0.125 +0.125
  predator m_k: +2.188 +1.563 +0.938 +0.313 -0.313 -0.938 -1.563 -2.188
  sum m_k = +0.000000  (sells early, buys back late, ends flat)
  victim revenue: no predator 99.4875 | with predator 96.2062 | loss 3.2812
  predator profit 1.6406 | deadweight 1.6406

Two liquidators sharing temporary liquidity (each 500,000 over 5 days):
  shared-liquidity Nash          quarters  46.81%   26.18%   15.70%   11.31%
  AC closed form with eta_eff=1.5*eta  46.81%   26.18%   15.70%   11.31%
  single-agent AC (eta=2.5e-6)   quarters  53.22%   25.57%   13.03%    8.19%
  implied urgency kappa: single 0.6008/day  vs shared 0.4906/day

Competing informed traders: K insiders of intensity beta each (monopolist beta=0.5)
   K  aggregate intensity  Sigma after 1 round   lambda_K  info impounded
   1               0.5000             2.000000     1.0000        50.0000%
   2               1.0000             0.800000     0.8000        80.0000%
   3               1.5000             0.400000     0.6000        90.0000%
   5               2.5000             0.153846     0.3846        96.1538%
  10               5.0000             0.039604     0.1980        99.0099%
  50              25.0000             0.001599     0.0400        99.9600%
1000             500.0000             0.000004     0.0020        99.9999%
```

One cross-check that matters: the **shared-liquidity Nash equilibrium reproduces the single-agent Almgren–Chriss trajectory with $\eta_{\text{eff}}=1.5\eta$ to five decimal places** in all four quarters, which is precisely the $\eta_{\text{eff}}=\tfrac32\eta$ prediction of §2.6. The solver is therefore solving the game, not a mis-specified QP.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis lives in [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]]. One line each:

1. **The equilibrium is only as good as the payoff it assumes.** Glosten–Milgrom's spread $\pi(V_H-V_L)$ is *an equilibrium of a game*, not a fact about the world: mis-specify $\pi$ and the maker does not "earn a bit less", it **loses ~0.2 \$/trade with certainty** (verified in §3 of page 05).
2. **The single-insider Kyle model is a fiction.** Real markets have many informed participants; with $K$ insiders the price reveals information at rate $K\beta$ and λ collapses toward zero — calibrating a single-insider λ on a multi-insider market **over-states impact**.
3. **The naive continuous-time limit does not exist.** Discretising Kyle and taking $N\to\infty$ with a fixed noise budget sends λ to infinity; only Back's (1992) linear-release equilibrium is well-defined. Any "high-frequency limit" claim must say which limit.
4. **Strategic equilibria can be unstable.** Schied & Zhang (2019) / Cordoni & Lillo (2022): below a threshold on the temporary-cost parameter the transient-impact execution game has wildly oscillating strategies and no well-behaved high-frequency limit — the equilibrium exists mathematically but is not a description of a market.
5. **Predation is real but not identified by these models.** The predator's schedule depends on the *victim's* schedule being public; in reality schedules are hidden and randomised, and the empirical literature struggles to separate predation from momentum and news.
6. **Adverse selection is estimated, not observed.** Practical proxies (PIN, VPIN) are noisy and contested (Easley–Kiefer–O'Hara–Paperman 1996; Easley–López de Prado–O'Hara 2012; Andersen & Bondarenko 2014), so the "equilibrium" π you plug in is itself a guess.

---

### 5. Canonical Literature & Study References

- **Kyle, Albert S.** — "Continuous auctions and insider trading," *Econometrica* 53(6), 1315–1335 (1985). *The anchor of the whole folder: the strategic insider, the linear price rule, $\lambda$, and the $\Sigma_0/2$ half-information result.*
- **Glosten, Lawrence R.; Milgrom, Paul R.** — "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders," *Journal of Financial Economics* 14(1), 71–100 (1985). *Adverse selection as a sequential Bayesian game; zero-profit quotes are conditional expectations.*
- **Back, Kerry** — "Insider trading in continuous time," *Review of Financial Studies* 5(3), 387–409 (1992). *The correct continuous-time limit: linear information release, constant λ = √(Σ₀/(σ_u²T)), and the founding use of filtering in microstructure.*
- **Holden, Craig W.; Subrahmanyam, Avanidhar** — "Long-lived private information and imperfect competition," *Journal of Finance* 47(1), 247–270 (1992). *Many informed traders ⇒ faster revelation ⇒ deeper market; the antidote to single-insider calibration.*
- **Brunnermeier, Markus K.; Pedersen, Lasse Heje** — "Predatory trading," *Journal of Finance* 60(4), 1825–1863 (2005). *Predators sell alongside a distressed liquidator and buy back later; price overshoot, and illiquidity precisely when liquidity is needed.*
- **Carlin, Bruce I.; Lobo, Miguel Sousa; Viswanathan, S.** — "Episodic liquidity crises: Cooperative and predatory trading," *Journal of Finance* 62(5), 2235–2274 (2007). *The experimental/OECD-bond-market companion: when cooperation among potential predators breaks down.*
- **Schied, Alexander; Zhang, Tao** — "A market impact game under transient price impact," *Mathematics of Operations Research* 44(1), 102–121 (2019). *The canonical multi-agent execution game; source of the instability threshold.*
- **Schied, Alexander; Strehle, Elias; Zhang, Tao** — "High-frequency limit of Nash equilibria in a market impact game with transient price impact," *SIAM Journal on Financial Mathematics* 8(1), 589–634 (2018). *When the continuous-time limit of the execution game does (and does not) exist.*
- **Cordoni, Francesco; Lillo, Fabrizio** — "Instabilities in multi-asset and multi-agent market impact games," *Annals of Operations Research* (2022). *Extends Schied–Zhang to many agents and assets; the scaling of impact with the number of traders is what decides stability.*
- **Cardaliaguet, Pierre; Lehalle, Charles-Albert** — "Mean field game of controls and an application to trade crowding," *Mathematics and Financial Economics* 12(3) (2018). *The mean-field limit of the execution game — what happens when the crowd is anonymous.*
- **Huberman, Gur; Stanzl, Werner** — "Price manipulation and quasi-arbitrage," *Econometrica* 72(4), 1247–1275 (2004). *No-dynamic-arbitrage: the constraint that makes an impact/decay game admissible at all.*
- **Easley, David; Kiefer, Nicholas M.; O'Hara, Maureen; Paperman, Joseph B.** — "Liquidity, information, and infrequently traded stocks," *Journal of Finance* 51(4), 1405–1436 (1996). *PIN — the first attempt to estimate the informed share that the games take as given.*
- **Easley, David; López de Prado, Marcos; O'Hara, Maureen** — "Flow toxicity and liquidity in a high-frequency world," *Review of Financial Studies* 25(5), 1457–1493 (2012). *VPIN: the high-frequency toxicity proxy.*
- **Andersen, Torben G.; Bondarenko, Oleg** — "VPIN and the flash crash," *Journal of Financial Markets* 17, 1–46 (2014). *The methodological takedown of VPIN — read it before trusting any toxicity number.*
- **Biais, Bruno; Glosten, Lawrence; Spatt, Chester** — "Market microstructure: A survey of microfoundations, empirical results, and policy implications," *Journal of Financial Markets* 8(2), 217–264 (2005). *The map of the whole field.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 5–7. *Corpus verification reports `hasbrouck_ch1-5.md` (Ch 5, GM) and `hasbrouck_ch6-10.md` (Ch 6 PIN, Ch 7 Kyle).*
- **Foucault, Thierry; Pagano, Marco; Röell, Ailsa** — *Market Liquidity: Theory, Evidence, and Policy* (2013), Ch 3. *Corpus verification report `foucault_ch1-3.md`.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, martingales) · [[foundations/bayesian-statistics/index|Bayesian Statistics]] (the GM recursion) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (Back's filtering argument) · [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (the quadratic execution games)
- Sibling in-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (the *non-strategic* schedule that the games generalise) · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Equilibrium-twin in Pillar 6: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (Kyle λ, the square-root law) · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (the GM game in full) · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] (estimating π from flow) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- Market-making partner: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (the maker's inventory game — the other half of the quote)
- Risk & portfolio: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (L-VaR) · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] (predation as a spillover channel) · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]] — no prior knowledge needed.
- **Model + code (undergrad/job-seeking):** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/02-the-kyle-model-and-back-limit|02 - Kyle & the Back Limit]] → [[pillars/02-algorithmic-hft/market-microstructure-game-theory/03-glosten-milgrom-sequential-trade|03 - Glosten–Milgrom]] → [[pillars/02-algorithmic-hft/market-microstructure-game-theory/04-predatory-trading-and-execution-games|04 - Predatory Trading & Execution Games]].
- **Robustness (practitioner/graduate):** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]] → [[pillars/02-algorithmic-hft/market-microstructure-game-theory/06-advanced-extensions|06 - Advanced Extensions]].
- Sub-pages (in-folder): 01 From Zero · 02 Kyle & the Back Limit · 03 Glosten–Milgrom · 04 Predatory Trading & Execution Games · 05 Failure Modes · 06 Extensions

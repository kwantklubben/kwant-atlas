---
title: "06 - Advanced Extensions: Competing Insiders, Many-Agent Crowding, Stochastic Liquidity"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - holden-subrahmanyam
  - mean-field-games
  - trade-crowding
  - kyle-back
  - stochastic-liquidity
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Each failure on page 05 is the seed of an extension, and this page is the launchpad. Four extensions turn the classical games into objects a modern desk can actually run:

1. **Many informed traders (Holden–Subrahmanyam 1992).** The single strategic insider is replaced by $K$ competitors. Competition *accelerates* information revelation and *deepens* the market — quantified below: $\Sigma'/\Sigma_0$ falls from $50\%$ at $K=1$ to $80\%$, $90\%$, $96\%$ impounded at $K=2,3,5$.
2. **Many-agent execution games (Schied–Zhang 2019; Cordoni–Lillo 2022).** Replace two competing liquidators with $J$, and the equilibrium acquires a clean closed-form structure: the symmetric Nash is Almgren–Chriss with $\eta_{\text{eff}}=\tfrac{J+1}{2}\eta$. Crowding makes *each* agent slower, and the effect is quantitative and monotone.
3. **The mean-field / anonymous-crowd limit (Cardaliaguet–Lehalle 2018).** When $J$ is large and no agent's identity matters, the game becomes a mean-field game of controls; the object to solve is a coupling between an HJB equation and a Fokker–Planck equation for the crowd's aggregate position.
4. **Stochastic and transient liquidity.** Noise volume $\sigma_u^2$, prior uncertainty $\Sigma_0$ and resilience are random processes, not constants — which converts Kyle–Back into a *stochastic-liquidity* model and Almgren–Chriss into a stochastic-control problem.

Why this order? (1) fixes *who is informed*; (2) fixes *how many are trading*; (3) fixes *anonymity*; (4) fixes the *exogenous parameters*. Together they are the minimal set that lets the classical equilibrium survive contact with a real market.

> **The one-sentence essence.** "The game generalises along four axes — more informed traders (faster revelation, deeper market), more liquidators (an inflated effective impact coefficient), anonymity (a mean-field limit), and randomness in the parameters themselves (stochastic control) — and each generalisation has a closed-form signature you can compute."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 $K$ competing informed traders (Holden–Subrahmanyam 1992).** Keep Kyle's batch structure but let $K$ insiders each observe $v$ and each submit informed demand. With **aggregate** informed intensity $K\beta$ (so the total informed order is $K\beta(v-p_0)$) and noise $u\sim\mathcal N(0,\sigma_u^2)$, one round of Bayesian updating gives
$$
y=K\beta(v-p_0)+u,\qquad \operatorname{Var}(y)=(K\beta)^2\Sigma_0+\sigma_u^2,
$$
$$
\boxed{\;\Sigma'=\Sigma_0-\frac{(K\beta)^2\Sigma_0^2}{(K\beta)^2\Sigma_0+\sigma_u^2}=\frac{\Sigma_0\sigma_u^2}{(K\beta)^2\Sigma_0+\sigma_u^2},\qquad \lambda_K=\frac{K\beta\,\Sigma_0}{(K\beta)^2\Sigma_0+\sigma_u^2}\;}
$$
$K=1$ with $\beta=\sqrt{\sigma_u^2/\Sigma_0}$ recovers $\Sigma_0/2$ and $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ — the Kyle benchmark. As $K\to\infty$, $\Sigma'\to0$ (instant revelation) and $\lambda_K\to0$ (**infinite depth**). The economics is simple: competition among the informed forces each of them to trade more aggressively relative to their information, so the price learns faster and the market is *more* liquid, not less.

**Caveat, stated plainly.** The formula above treats the *aggregate* intensity $K\beta$ as given. Holden & Subrahmanyam's own result is subtly different: as $K$ rises, each insider becomes *less* aggressive individually, but the aggregate is still more aggressive than the monopolist's, and revelation is faster. The table below is therefore the correct *mechanism* with a deliberately transparent assumption; the qualitative conclusion (more informed $\Rightarrow$ faster revelation, deeper market) is theirs.

**2.2 $J$ symmetric liquidators sharing one pool.** Generalise page 04's two-player game. Agent $i$'s cost is
$$
C_i=\frac{\eta}{\tau}\sum_{k}n^i_k\Bigl(n^i_k+\sum_{j\ne i}n^j_k\Bigr)+\lambda_{\text{risk}}\sigma^2\tau\sum_k\bigl(x^i_k\bigr)^2,\qquad \sum_k n^i_k=\frac{X}{J},
$$
and the first-order condition in symmetric equilibrium $n^j_k=n^i_k=n_k$ is
$$
\frac{\eta}{\tau}\Bigl(2n_k+(J-1)n_k\Bigr)+[\text{risk terms}]=\mu\;\Longrightarrow\;\text{curvature}\;\frac{\eta(J+1)}{\tau},
$$
versus $2\eta/\tau$ for a single agent. Hence
$$
\boxed{\;\eta_{\text{eff}}=\frac{J+1}{2}\,\eta\;\Longrightarrow\;\kappa_{\text{eff}}=\sqrt{\frac{\lambda_{\text{risk}}\sigma^2}{\eta_{\text{eff}}}}=\kappa_1\sqrt{\frac{2}{J+1}}\;}
$$
so $J=2$ gives $\eta_{\text{eff}}=\tfrac32\eta$ and $\kappa_{\text{eff}}=\sqrt{2/3}\,\kappa_1$ (page 04's result), and $J=100$ gives $\kappa_{\text{eff}}\approx0.085$/day against $0.601$/day for a lone liquidator — **a seven-fold increase in the effective time-scale of the trade**. Verified to two decimals in all four quarters for $J=1,2,3,5$ below.

**2.3 Anonymity: the mean-field limit.** When $J$ is large and agents are anonymous, tracking each agent's schedule is hopeless; the right object is the *distribution* of positions. Cardaliaguet & Lehalle (2018) formulate this as a **mean-field game of controls**: an individual agent solves an HJB equation whose coefficients depend on the aggregate, while the aggregate position evolves according to a Fokker–Planck equation driven by the individual optimal controls. The fixed point of the two is the mean-field equilibrium. The practical upshot is that in a crowded trade the *market-wide* cost is a function of the crowd's total size and dispersion, not of any individual's order — which is why "trade crowding" is a first-class risk factor rather than a modelling nuisance.

**2.4 Transient impact and resilience.** Replace instantaneous impact by a decay kernel $G$: the impact of a trade at $u$ on the mid at $t$ is $G(t-u)\,dX_u$, i.e.
$$
S_t=S_0+\sigma W_t+\int_0^tG(t-u)\,dX_u .
$$
**No-dynamic-arbitrage** (Huberman–Stanzl 2004; Gatheral 2010) requires $G$ to be non-increasing and convex; models with the wrong kernel admit manipulation and are admissible only as curve-fits, never as equilibrium. For power-law kernels $G(t)\propto t^{-\gamma}$ the optimal strategy oscillates and decays (Gatheral's Figure 22.2), and — the punchline of Schied–Zhang–Cordoni–Lillo — the **multi-agent** game built on such a kernel becomes unstable below a threshold on the temporary-cost parameter.

**2.5 Stochastic liquidity.** Both of the model families above take $\sigma_u^2$ and $\Sigma_0$ as constants. In reality liquidity is stochastic and, worse, *correlated with informed flow*: on the days when $\Sigma_0$ and $\pi$ are largest, $\sigma_u^2$ is smallest. Kyle's model with an exogenous *stochastic* liquidity process (and its elaboration with a general volatility process) gives $\lambda_t$ as a **path-dependent** quantity — for a deterministic volatility profile $\lambda=\sqrt{\Sigma_0/\tau_T}$ with $\tau_T=\int_0^T\sigma_u^2(s)ds$, so what looks like "constant λ" in Back (1992) is really "constant λ *given a deterministic noise profile*". Replace that profile with a process and λ becomes a stochastic functional, which is why empirical λ estimates are so unstable across windows.

---

### 3. Computational Implementation — two extensions, verified

Stdlib only, one Gaussian eliminator, runtime under a second. Part A is the $K$-insider information release; Part B solves the $J$-agent shared-liquidity Nash and checks it against the closed-form $\eta_{\text{eff}}=\tfrac{J+1}{2}\eta$ prediction.

```python
import math

# ---------- Part A: K competing informed traders (Holden-Subrahmanyam 1992) ----------
Sig0, su2 = 4.0, 1.0
beta_mono = math.sqrt(su2/Sig0)
print("Competing informed traders: K insiders of intensity beta each (monopolist beta=0.5)")
print(f"{'K':>4} {'aggregate intensity':>20} {'Sigma after 1 round':>20} {'lambda_K':>10} {'info impounded':>15}")
for K in (1, 2, 3, 5, 10, 50, 1000):
    Kb2 = (K*beta_mono)**2
    print(f"{K:>4} {K*beta_mono:>20.4f} {Sig0*su2/(Kb2*Sig0+su2):>20.6f} "
          f"{K*beta_mono*Sig0/(Kb2*Sig0+su2):>10.4f} {100*(1-(Sig0*su2/(Kb2*Sig0+su2))/Sig0):>14.4f}%")
print(f"K=1 impounds exactly half: Sigma_0/2 = {Sig0/2:.4f}   (Kyle's half-information property)")

# ---------- Part B: J symmetric liquidators sharing one liquidity pool ----------
def solve_linear(A, b):
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]/M[c][c]
                for k in range(c, n+1): M[r][k] -= f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]
def nash_J(J, eta=2.5e-6, lam=1e-6, sigma=0.95, T=5.0, N=40, X=1e6):
    tau = T/N; per = X/J; c = 2*lam*sigma*sigma*tau; e = eta/tau
    M = J*N+J; A = [[0.0]*M for _ in range(M)]; b = [0.0]*M
    for i in range(J):
        off = i*N
        for k in range(N):
            r = off+k
            A[r][off+k] += 2*e
            for j in range(J):
                if j != i: A[r][j*N+k] += e                 # shared pool
            for l in range(N): A[r][off+l] += c*((N-1-k) if l <= k else (N-1-l))
            A[r][J*N+i] = -1.0; b[r] = c*per*(N-1-k)
        A[J*N+i][off:off+N] = [1.0]*N; b[J*N+i] = per
    return [solve_linear(A, b)[i*N:(i+1)*N] for i in range(J)]
def ac(eta, X, lam=1e-6, sigma=0.95, T=5.0, N=40):
    k = math.sqrt(lam*sigma**2/eta)
    x = [X*math.sinh(k*(T-T*j/N))/math.sinh(k*T) for j in range(N+1)]
    return [x[j]-x[j+1] for j in range(N)]
def q(n, X):
    N = len(n); return [sum(n[:N//4]),sum(n[N//4:N//2]),sum(n[N//2:3*N//4]),sum(n[3*N//4:])]
print("\nJ symmetric liquidators sharing one pool:  predicted eta_eff = (J+1)/2 * eta")
print(f"{'J':>3} {'eta_eff pred':>13}  {'Nash quarters (agent 1)':>34}  {'AC(eta_eff) quarters':>34}")
for J in (1, 2, 3, 5):
    per = 1e6/J; qq = q(nash_J(J)[0], per); ee = (J+1)/2*2.5e-6; aa = q(ac(ee, per), per)
    print(f"{J:>3} {ee:13.3e}  " + " ".join(f"{100*v/per:7.2f}%" for v in qq) + "  " + " ".join(f"{100*v/per:7.2f}%" for v in aa))
print("\nimplied individual urgency  kappa_eff = sqrt(lam*sigma^2/eta_eff):")
for J in (1, 2, 3, 5, 10, 100):
    ee = (J+1)/2*2.5e-6
    print(f"  J={J:>3}: eta_eff={ee:.3e}  kappa_eff={math.sqrt(1e-6*0.95**2/ee):.4f}/day")
```
```
Competing informed traders: K insiders of intensity beta each (monopolist beta=0.5)
   K  aggregate intensity  Sigma after 1 round   lambda_K  info impounded
   1               0.5000             2.000000     1.0000        50.0000%
   2               1.0000             0.800000     0.8000        80.0000%
   3               1.5000             0.400000     0.6000        90.0000%
   5               2.5000             0.153846     0.3846        96.1538%
  10               5.0000             0.039604     0.1980        99.0099%
  50              25.0000             0.001599     0.0400        99.9600%
1000             500.0000             0.000004     0.0020        99.9999%
K=1 impounds exactly half: Sigma_0/2 = 2.0000   (Kyle's half-information property)

J symmetric liquidators sharing one pool:  predicted eta_eff = (J+1)/2 * eta
  J  eta_eff pred             Nash quarters (agent 1)                AC(eta_eff) quarters
  1     2.500e-06    53.21%   25.57%   13.03%    8.19%    53.22%   25.57%   13.03%    8.19%
  2     3.750e-06    46.81%   26.18%   15.70%   11.31%    46.81%   26.18%   15.70%   11.31%
  3     5.000e-06    42.81%   26.30%   17.39%   13.49%    42.81%   26.30%   17.39%   13.49%
  5     7.500e-06    38.06%   26.23%   19.41%   16.30%    38.06%   26.23%   19.41%   16.30%

implied individual urgency  kappa_eff = sqrt(lam*sigma^2/eta_eff):
  J=  1: eta_eff=2.500e-06  kappa_eff=0.6008/day
  J=  2: eta_eff=3.750e-06  kappa_eff=0.4906/day
  J=  3: eta_eff=5.000e-06  kappa_eff=0.4249/day
  J=  5: eta_eff=7.500e-06  kappa_eff=0.3469/day
  J= 10: eta_eff=1.375e-05  kappa_eff=0.2562/day
  J=100: eta_eff=1.263e-04  kappa_eff=0.0845/day
```

Two readings:

- **Part A is a mechanism with a clean monotone signature.** $\Sigma'/\Sigma_0$ falls $0.50\to0.20\to0.10\to0.038$ as $K$ goes $1\to2\to3\to5$, and $\lambda_K$ falls from $1.0000$ to $0.1980$ at $K=10$ and $0.0020$ at $K=1000$. **More informed traders means a deeper market, not a shallower one** — the exact opposite of the naive "more informed = more dangerous" intuition, because competition forces each insider to reveal faster than they would like.
- **Part B is an exact closed form in disguise.** For $J=1,2,3,5$ the Nash equilibrium reproduces the single-agent Almgren–Chriss quarters computed at $\eta_{\text{eff}}=\tfrac{J+1}{2}\eta$ to within $0.01$ percentage points (the $J=1$ row differs by one hundredth of a point purely from the $N=40$ discretisation). The $\kappa_{\text{eff}}=\kappa_1\sqrt{2/(J+1)}$ law is therefore confirmed across the whole range: **individual urgency falls like $1/\sqrt J$, so a 100-way crowded exit is seven times slower per participant than a lone liquidation.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The $K$-insider formula assumes the aggregate intensity.** Holden & Subrahmanyam's actual equilibrium has each insider *reducing* intensity as $K$ rises; only the aggregate grows. Any calibration that plugs $K\beta_{\text{mono}}$ into $\lambda_K$ over-states how fast revelation speeds up.
2. **"More agents $\Rightarrow$ less urgent" is a modelling conclusion, not a law.** It comes from sharing a *temporary* impact pool with a fixed $\eta$. If agents instead compete for a *permanent* impact or for a fixed number of counter-parties, the sign can flip. Always state which friction is being shared.
3. **The mean-field limit is a limit.** Cardaliaguet–Lehalle's formulation is exact only as $J\to\infty$ with vanishing individual influence. In a market with three large dealers and ten thousand tiny ones, neither the finite-$J$ game nor the mean-field limit is the right description, and the intermediate regime is the hard one.
4. **Decay kernels must satisfy no-dynamic-arbitrage.** Huberman–Stanzl (2004) / Gatheral (2010): the transient kernel must be non-increasing and convex, or the model admits manipulation. A kernel chosen purely for fit can be inadmissible.
5. **Multi-agent transient-impact games can be unstable.** Schied & Zhang (2019), Cordoni & Lillo (2022): below a threshold on the temporary-cost parameter the equilibrium strategies oscillate and the high-frequency limit does not exist. Adding agents and assets changes *where* the threshold sits.
6. **Stochastic liquidity breaks $\lambda$ as a constant.** Once $\sigma_u^2$ is a process, $\lambda$ is a path-dependent functional; the "Kyle's lambda" your regression reports is a window average of a stochastic object. This is the first-principles reason λ estimates are unstable across samples.
7. **The extensions do not compose for free.** Few informed traders + many liquidators + transient impact + stochastic liquidity is a high-dimensional, poorly-identified system. In practice desks calibrate two or three effects conservatively and leave the rest to robust, randomised execution.
8. **Randomisation is the practical antidote to everything above.** Because each extension increases the value of *not being predictable*, the robust response is to randomise lot sizes, timing and venue — which converts a fragile equilibrium into a distribution over equilibria.

---

### 5. Canonical Literature & Study References

- **Holden, Craig W.; Subrahmanyam, Avanidhar** — "Long-lived private information and imperfect competition," *Journal of Finance* 47(1), 247–270 (1992). *The multi-insider model; the source of "more informed traders $\Rightarrow$ faster revelation".*
- **Admati, Anat R.; Pfleiderer, Paul** — "A theory of intraday patterns: Volume and price variability," *Review of Financial Studies* 1(1), 3–40 (1988). *Many insiders and intraday volume/volatility patterns; the companion to Holden–Subrahmanyam.*
- **Kyle, Albert S.; Obizhaeva, Anna A.** — "Market microstructure invariance," *Econometrica* 84(3), 975–1024 (2016). *Dimensional analysis of $\lambda$ and bet sizes across assets — what an "invariant" λ even means.*
- **Schied, Alexander; Zhang, Tao** — "A market impact game under transient price impact," *Mathematics of Operations Research* 44(1), 102–121 (2019). *The multi-agent execution game and its instability threshold.*
- **Cordoni, Francesco; Lillo, Fabrizio** — "Instabilities in multi-asset and multi-agent market impact games," *Annals of Operations Research* (2022). *How the scaling of impact with the number of agents and assets determines stability.*
- **Cardaliaguet, Pierre; Lehalle, Charles-Albert** — "Mean field game of controls and an application to trade crowding," *Mathematics and Financial Economics* 12(3) (2018). *The anonymous-crowd limit; HJB coupled to a Fokker–Planck equation.*
- **Gatheral, Jim** — "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7), 749–759 (2010). *The admissibility constraint on any transient-impact kernel.*
- **Huberman, Gur; Stanzl, Werner** — "Price manipulation and quasi-arbitrage," *Econometrica* 72(4), 1247–1275 (2004). *Which impact models admit manipulation; only linear schedules are manipulation-free.*
- **Back, Kerry** — "Insider trading in continuous time," *Review of Financial Studies* 5(3), 387–409 (1992). *The continuous-time benchmark the extensions generalise.*
- **Gatheral, Jim; Schied, Alexander; Slynko, Alla** — "Transient linear price impact and Fredholm integral equations," *Mathematical Finance* 22(3), 445–474 (2012). *Optimal execution for general decay kernels; the single-agent counterpart of §2.4.*
- **Baruch, Shmuel** — "Insider trading and risk aversion," *Journal of Financial Markets* 5(4), 451–464 (2002). *What happens to the Kyle equilibrium when the insider is risk-averse (the $K$-insider extension with a different friction).*
- **Cartea, Álvaro; Jaimungal, Sebastian; Penalva, José** — *Algorithmic and High-Frequency Trading* (2015), Ch 6–9. *Stochastic control with transient impact and stochastic liquidity — the practical face of §2.5.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/04-predatory-trading-and-execution-games|04 - Predatory Trading & Execution Games]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/02-the-kyle-model-and-back-limit|02 - Kyle & the Back Limit]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]]
- Multi-agent executions in the sibling folder: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/06-advanced-extensions|Almgren–Chriss: Advanced Extensions]] (nonlinear impact, resilient books, dark pools, adaptive control)
- Impact and crowding: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (transient impact, the square-root law) · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]]
- Risk of the crowd: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]
- Tools: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (the single-agent HJB the mean-field version generalises) · [[foundations/stochastic-calculus/index|Stochastic Calculus]]

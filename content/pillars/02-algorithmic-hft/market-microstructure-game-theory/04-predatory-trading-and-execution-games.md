---
title: "04 - Predatory Trading and Games Among Competing Liquidators"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - predatory-trading
  - brunnermeier-pedersen
  - execution-game
  - schied-zhang
  - nash-equilibrium
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (the non-strategic version of the same problem) and [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]].

---

### 1. Intuition & Practical Objective

Everything up to here assumed your schedule was *yours*. That is the single most dangerous assumption in execution. The moment your order is large enough to move the price, **your schedule becomes other people's information**, and the optimisation problem changes species: from a decision problem to a game.

Two distinct games matter, and they are played by different people:

**Game A — predation (Brunnermeier–Pedersen 2005).** Someone *must* liquidate: a fund is in redemption, a levered position hit a margin call, a desk is unwinding a basket. The trade is not optional and not patient. Now a predator who can infer the schedule has a strictly profitable move: **sell alongside the victim, early** — the joint selling depresses the price — and then **buy back** after the victim has finished, at the depressed price. The predator's round trip is a pure transfer out of the victim's pocket. The victim is not "unlucky"; it is being farmed. Brunnermeier & Pedersen's point is not merely redistribution: the predator's extra selling means **the market is least liquid exactly when liquidity is most needed**, and the resulting price overshoot can *trigger* further liquidations, propagating the crisis across assets.

**Game B — competing liquidators (Schied–Zhang 2019).** No predation, just many agents each trying to liquidate against the *same* liquidity pool. Each one, rationally, does not internalise the cost it imposes on the others. The Nash equilibrium is the object of interest, and its properties are not what a single-agent optimisation would suggest.

The practical objective of this page is to make both games computable. For predation, we solve the predator's best-response schedule in closed form and price the damage. For the competitive case, we solve the Nash equilibrium of the explicit linear-quadratic execution game with a stdlib Gaussian eliminator and verify that it collapses to the right single-agent benchmark.

> **The one-sentence essence.** "A public liquidation schedule is a gift to anyone faster than you: the predator sells ahead and buys back behind, and the equilibrium of many competing liquidators is *not* the single-agent optimum — it is the single-agent optimum with an inflated cost of trading fast."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Predation: the price path and who pays for it.**

**Setup.** Price is linear in cumulative *signed* flow, with a sign convention where **selling pushes the price down**:
$$P_k=P_0-\kappa\sum_{j\le k}\bigl(n_j+m_j\bigr),$$
where $n_k$ = victim's sales and $m_k$ = predator's sales (negative = the predator buys). Both face a temporary cost $\eta$ per unit sold (the concession needed to trade now). Execution at step $k$ happens at the *previous* mid, so the victim receives $P_{k-1}-\eta n_k$ per share and the predator's cash flow is $m_k(P_{k-1}-\eta m_k)$.

**The predator must round-trip**: $\sum_k m_k=0$. Its objective is
$$\Pi=\sum_k m_k\bigl(P_{k-1}-\eta m_k\bigr),\qquad P_{k-1}=P_0-\kappa\sum_{j<k}(n_j+m_j).$$
Substitute and write $A_k=\sum_{j<k}n_j$ (the victim's cumulative sales, the predator's only state variable):
$$\Pi=\underbrace{P_0\textstyle\sum_k m_k}_{=0}-\kappa\sum_k m_k A_k-\kappa\sum_k m_k\!\!\sum_{j<k}\!\!m_j-\eta\sum_k m_k^2 .$$
Using the identity $\sum_k m_k\sum_{j<k}m_j=-\tfrac12\sum_k m_k^2$ (valid whenever $\sum m_k=0$),
$$\Pi=-\kappa\sum_k m_kA_k-\Bigl(\eta-\frac{\kappa}{2}\Bigr)\sum_k m_k^2 .$$
This is **concave** iff $\eta>\kappa/2$ — the interior-solution condition. Maximising with a multiplier for $\sum m_k=0$:
$$\frac{\partial\Pi}{\partial m_k}=-\kappa A_k-2\Bigl(\eta-\frac\kappa2\Bigr)m_k-\mu=0\;\Longrightarrow\;\boxed{\;m_k=\frac{\kappa\,(\bar A-A_k)}{2\eta-\kappa}\;},\qquad \bar A=\frac1N\sum_k A_k .$$

**Read the sign.** $A_k$ is increasing in $k$ (the victim is selling), so $\bar A-A_k>0$ early and $<0$ late: **$m_k>0$ early (the predator sells) and $m_k<0$ late (it buys back).** The predator front-runs. This is the Brunnermeier–Pedersen mechanism in closed form, and it falls out of nothing but a concave quadratic.

**How much damage?** Writing $\Delta_P$ for the victim's revenue loss relative to the no-predator benchmark, we will find numerically (§3) that
$$\Delta_P>\Pi>0:$$
the victim loses **more** than the predator gains, the difference being the deadweight cost of the predator's own round trip through the temporary-impact term $\eta\sum m_k^2$. Predation is not a pure transfer — it destroys liquidity.

**The victim's counter.** Because $\bar A-A_k$ depends on the *shape* of the victim's schedule, the victim can reduce $m_k$ by making $A_k$ as flat as possible relative to the remaining volume — i.e. by **front-loading**. Speeding up reduces both the predator's informational advantage and the time over which permanent impact can be harvested. This is BP's practical prescription, and the model reproduces it (§3).

**2.2 Competing liquidators: the Nash game.** Now no predator: $J$ agents each liquidating $X/J$ against **one** liquidity pool. Agent $i$'s cost is
$$C_i=\frac{\eta}{\tau}\sum_{k=1}^{N}n^i_k\bigl(n^i_k+n^j_k\bigr)+\lambda_{\text{risk}}\sigma^2\tau\sum_{k=1}^{N}\bigl(x^i_k\bigr)^2,\qquad \sum_{k=1}^N n^i_k=\frac{X}{J},$$
where the first term is the shared temporary impact — **if both trade at step $k$, each pays for the aggregate flow $n^i_k+n^j_k$** — and the second is the standard inventory-risk penalty from Almgren–Chriss. This is a convex quadratic game, so the Nash equilibrium exists, is unique, and is found by solving each agent's first-order condition holding the other fixed.

In symmetric equilibrium $n^i=n^j=n$, the marginal temporary cost is $\eta(2n_k+n_k)/\tau=3\eta n_k/\tau$, versus $2\eta n_k/\tau$ for a single agent. Hence

$$\boxed{\;\eta_{\text{eff}}=\tfrac{3}{2}\eta\;\Longrightarrow\;\kappa_{\text{eff}}=\sqrt{\lambda_{\text{risk}}\sigma^2/\eta_{\text{eff}}}=\sqrt{\tfrac23}\,\kappa_1\;}$$

where $\kappa_1$ is the single-agent Almgren–Chriss urgency. **The market-wide liquidation is slower under competition than it would be for a monopolist facing only its own impact** ($0.4906$/day vs $0.6008$/day on the numbers below), because trading alongside a rival is expensive and each agent waits for the other. This is the exact opposite of the folk intuition "everyone rushes for the exit", and it is a genuine equilibrium effect: the rush happens in *impact*, not in *individual* speed.

**2.3 Where the game becomes unstable.** Schied & Zhang (2019) and Cordoni & Lillo (2022) show that in continuous-time transient-impact games this structure has a **threshold**. As the temporary-cost parameter falls relative to the cross-impact, the equilibrium strategies begin to **oscillate** — agents alternate buying and selling at ever-increasing frequency and amplitude — and the high-frequency limit of the equilibrium ceases to exist. The equilibrium still exists *mathematically* for each finite discretisation, but it stops being a description of a market. The practical reading: **an execution game with too little friction does not have a sensible answer**, which is why real desks add participation caps and randomised lot sizes even when the optimiser says not to.

---

### 3. Computational Implementation — two execution games, solved

Stdlib only (`math`, `random`, plus a 30-line Gaussian eliminator). Part A solves the predation game in closed form and prices it; Part B solves the two-player Nash equilibrium of the competing-liquidator game and cross-checks it against the closed-form Almgren–Chriss trajectory.

```python
import math

def solve_linear(A, b):                      # stdlib Gaussian elimination, partial pivoting
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]/M[c][c]
                for k in range(c, n+1): M[r][k] -= f*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

# ---------- Part A: predatory trading (Brunnermeier-Pedersen mechanism) ----------
def predator(victim, kappa=1.0, eta=0.6):    # m_k = kappa*(A_bar - A_k)/(2*eta - kappa)
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
def front(tot, N, c):
    w = [math.exp(-c*k) for k in range(N)]; s = sum(w); return [tot*x/s for x in w]

NN, X = 8, 1.0
twap = [X/NN]*NN; m = predator(twap)
print(f"Predation on an {NN}-step TWAP victim (kappa=1.0, eta=0.6, X={X:g}):")
print("  victim   n_k: " + " ".join(f"{v:+.3f}" for v in twap))
print("  predator m_k: " + " ".join(f"{v:+.3f}" for v in m))
print(f"  sum m_k = {sum(m):+.6f}  (sells early, buys back late, ends flat)")
print(f"  victim revenue: no predator {rev(twap,[0.0]*NN):.4f} | with predator {rev(twap,m):.4f} | loss {rev(twap,[0.0]*NN)-rev(twap,m):.4f}")
print(f"  predator profit {cashflow(twap,m):.4f} | deadweight {rev(twap,[0.0]*NN)-rev(twap,m)-cashflow(twap,m):.4f}")
print("\nVictim speeds up when it expects predation (N=8, kappa=1.0, eta=0.6):")
print(f"{'schedule':>18} {'rev no pred':>12} {'rev pred':>10} {'loss':>9} {'pred profit':>12}")
for lab, sch in (("TWAP uniform", twap), ("mild front-load", front(X,NN,0.3)), ("hard front-load", front(X,NN,0.9))):
    mm = predator(sch)
    print(f"{lab:>18} {rev(sch,[0.0]*NN):12.4f} {rev(sch,mm):10.4f} {rev(sch,[0.0]*NN)-rev(sch,mm):9.4f} {cashflow(sch,mm):12.4f}")
print("\nPredation vs market depth eta (TWAP victim):")
print(f"{'eta':>6} {'pred profit':>12} {'victim loss':>12}")
for eta in (0.55, 0.65, 0.8, 1.2, 2.0):
    mm = predator(twap, 1.0, eta)
    print(f"{eta:6.2f} {cashflow(twap,mm,eta):12.4f} {rev(twap,[0.0]*NN,eta)-rev(twap,mm,eta):12.4f}")

# ---------- Part B: two competing liquidators sharing one liquidity pool ----------
def nash2(eta=2.5e-6, lam=1e-6, sigma=0.95, T=5.0, N=100, X=1e6):
    tau = T/N; half = X/2.0; c = 2*lam*sigma*sigma*tau; e = eta/tau
    M = 2*N+2; A = [[0.0]*M for _ in range(M)]; b = [0.0]*M
    for off, other, mult in ((0, N, 2*N), (N, 0, 2*N+1)):     # FOC of each agent
        for i in range(N):
            r = off+i
            A[r][off+i] += 2*e                 # own temporary impact
            A[r][other+i] += e                 # shared-liquidity cross term
            for l in range(N):                 # gradient of the inventory-risk term
                A[r][off+l] += c*((N-1-i) if l <= i else (N-1-l))
            A[r][mult] = -1.0; b[r] = c*half*(N-1-i)
    A[2*N][0:N] = [1.0]*N; b[2*N] = half          # sum n^1 = X/2
    A[2*N+1][N:2*N] = [1.0]*N; b[2*N+1] = half    # sum n^2 = X/2
    return solve_linear(A, b)[:N]
def quarters(n):
    N = len(n); return [sum(n[:N//4]),sum(n[N//4:N//2]),sum(n[N//2:3*N//4]),sum(n[3*N//4:])]
def ac(eta, X=5e5, lam=1e-6, sigma=0.95, T=5.0, N=100):
    k = math.sqrt(lam*sigma**2/eta)
    x = [X*math.sinh(k*(T-T*j/N))/math.sinh(k*T) for j in range(N+1)]
    return [x[j]-x[j+1] for j in range(N)]
print("\nTwo liquidators sharing temporary liquidity (each 500,000 over 5 days):")
print("  shared-liquidity Nash               quarters " + "  ".join(f"{100*v/5e5:6.2f}%" for v in quarters(nash2())))
print("  AC closed form with eta_eff=1.5*eta quarters " + "  ".join(f"{100*v/5e5:6.2f}%" for v in quarters(ac(3.75e-6))))
print("  single-agent AC (eta=2.5e-6)        quarters " + "  ".join(f"{100*v/5e5:6.2f}%" for v in quarters(ac(2.5e-6))))
print(f"  implied urgency kappa: single {math.sqrt(1e-6*0.95**2/2.5e-6):.4f}/day  vs shared {math.sqrt(1e-6*0.95**2/3.75e-6):.4f}/day")
```
```
Predation on an 8-step TWAP victim (kappa=1.0, eta=0.6, X=1):
  victim   n_k: +0.125 +0.125 +0.125 +0.125 +0.125 +0.125 +0.125 +0.125
  predator m_k: +2.188 +1.563 +0.938 +0.313 -0.313 -0.938 -1.563 -2.188
  sum m_k = +0.000000  (sells early, buys back late, ends flat)
  victim revenue: no predator 99.4875 | with predator 96.2062 | loss 3.2812
  predator profit 1.6406 | deadweight 1.6406

Victim speeds up when it expects predation (N=8, kappa=1.0, eta=0.6):
          schedule  rev no pred   rev pred      loss  pred profit
      TWAP uniform      99.4875    96.2062    3.2812       1.6406
   mild front-load      99.4821    96.5270    2.9552       1.9945
   hard front-load      99.4577    97.7403    1.7175       2.1122

Predation vs market depth eta (TWAP victim):
   eta  pred profit  victim loss
  0.55       3.2812       6.5625
  0.65       1.0937       2.1875
  0.80       0.5469       1.0938
  1.20       0.2344       0.4688
  2.00       0.1094       0.2188

Two liquidators sharing temporary liquidity (each 500,000 over 5 days):
  shared-liquidity Nash               quarters  46.81%   26.18%   15.70%   11.31%
  AC closed form with eta_eff=1.5*eta quarters  46.81%   26.18%   15.70%   11.31%
  single-agent AC (eta=2.5e-6)        quarters  53.22%   25.57%   13.03%    8.19%
  implied urgency kappa: single 0.6008/day  vs shared 0.4906/day
```

Five things worth reading off this output:

1. **The predator's schedule has the Brunnermeier–Pedersen signature**: `+2.188, +1.563, +0.938, +0.313, −0.313, −0.938, −1.563, −2.188`. It **sells 4,375 units' worth of pressure early and buys it all back late**, ending exactly flat (`sum m_k = +0.000000`). The symmetry is not imposed — it is the solution.
2. **The victim's loss exceeds the predator's gain**: loss $3.2812$ vs profit $1.6406$, with **deadweight $1.6406$**. Half the damage is pure value destruction through the predator's own round-trip temporary cost. Predation is worse than a tax.
3. **Front-loading helps.** As the victim moves from TWAP to hard front-loading, its loss falls monotonically: $3.2812\to2.9552\to1.7175$. This is BP's counter-measure, recovered from the model rather than asserted.
4. **Predation is a low-liquidity phenomenon.** At $\eta=0.55$ (cheap liquidity, tight market) the predator clears $3.2812$; at $\eta=2.00$ (expensive liquidity) only $0.1094$. A predator needs a *wide* impact function to harvest, which is why predation is documented in stressed markets rather than in normal ones.
5. **The Nash cross-check is exact.** The shared-liquidity Nash equilibrium reproduces the single-agent Almgren–Chriss trajectory with $\eta_{\text{eff}}=1.5\eta$ in **all four quarters to two decimals** ($46.81/26.18/15.70/11.31$), confirming $\eta_{\text{eff}}=\tfrac32\eta$ and the implied urgency $0.4906=\sqrt{2/3}\times0.6008$. The game solver is solving the game.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The predator must know the schedule.** Equation $m_k=\kappa(\bar A-A_k)/(2\eta-\kappa)$ requires $A_k$ — the victim's cumulative volume — as a *known function*. In reality the schedule is hidden, randomised, and split across venues. This is the single biggest gap between the model and practice, and it is why production execution randomises the lot sequence and never publishes the full shape.
2. **Victim and predator are assumed to play sequentially.** The model is a *best response* to a fixed victim schedule, not a Nash equilibrium of a two-player game in which the victim also optimises knowing it is being farmed. Solving that coupled game is harder, and its equilibrium can be non-monotone.
3. **The interior-solution condition $\eta>\kappa/2$ is a real constraint.** Below it the predator's problem is unbounded (it would trade infinite size), which means the linear-impact model is being asked a question it cannot answer. Real frictions — position limits, risk limits, margin — are what bound it in practice, not the model.
4. **Instability in the competitive game (Schied–Zhang 2019; Cordoni & Lillo 2022).** With transient impact and small temporary cost, the Nash equilibrium strategies oscillate and the high-frequency limit fails to exist. Both the solution *and* its interpretability are parameter-dependent.
5. **Crowded-trade identification is nearly impossible empirically.** Brunnermeier–Pedersen's mechanism predicts price overshoot and elevated volume in stressed names; momentum, news, and mechanical deleveraging predict much of the same. Separating predation from coincidence is an open empirical problem, which is why the literature leans on theory and lab/OTC episodes.
6. **Everyone is assumed to be rational and to know everyone else's parameters.** The game-theoretic answer is only as good as the common-knowledge assumption. If your rival's $\eta$ differs from your estimate of it, the equilibrium you solved is not the one being played.
7. **The Nash solution is symmetric by construction here.** In reality agents differ in size, horizon, risk aversion and information. Asymmetric games can have multiple equilibria, and the "the" equilibrium of a crowded unwind is often a coordination breakdown rather than a unique point.

---

### 5. Canonical Literature & Study References

- **Brunnermeier, Markus K.; Pedersen, Lasse Heje** — "Predatory trading," *Journal of Finance* 60(4), 1825–1863 (2005). *The source. Predators sell alongside a distressed liquidator and buy back later; price overshoot, reduced liquidation value, spillover across traders and markets.*
- **Carlin, Bruce I.; Lobo, Miguel Sousa; Viswanathan, S.** — "Episodic liquidity crises: Cooperative and predatory trading," *Journal of Finance* 62(5), 2235–2274 (2007). *What happens when the potential predators can also cooperate with the victim; the "trigger strategy" outcome and its breakdown.*
- **Schied, Alexander; Zhang, Tao** — "A market impact game under transient price impact," *Mathematics of Operations Research* 44(1), 102–121 (2019). *The canonical multi-agent execution game; existence, uniqueness, and the instability threshold.*
- **Schied, Alexander; Strehle, Elias; Zhang, Tao** — "High-frequency limit of Nash equilibria in a market impact game with transient price impact," *SIAM Journal on Financial Mathematics* 8(1), 589–634 (2018). *When the continuous-time limit of the equilibrium exists and when it does not.*
- **Cordoni, Francesco; Lillo, Fabrizio** — "Instabilities in multi-asset and multi-agent market impact games," *Annals of Operations Research* (2022). *Scaling in the number of agents and assets as the driver of (in)stability.*
- **Cardaliaguet, Pierre; Lehalle, Charles-Albert** — "Mean field game of controls and an application to trade crowding," *Mathematics and Financial Economics* 12(3) (2018). *The anonymous-crowd limit of exactly the competitive game solved above.*
- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000). *The single-agent benchmark that the Nash equilibrium is measured against.*
- **Huberman, Gur; Stanzl, Werner** — "Price manipulation and quasi-arbitrage," *Econometrica* 72(4), 1247–1275 (2004). *Which price-impact games admit manipulation at all; the admissibility constraint on any linear game you write down.*
- **Carlin, Bruce I.; Lobo, Miguel Sousa; Viswanathan, S.** — see also their experimental/OTC work cited in the Schied–Strehle–Zhang literature for the empirical side of episodic liquidity crises.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/03-glosten-milgrom-sequential-trade|03 - Glosten–Milgrom]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/06-advanced-extensions|06 - Advanced Extensions]]
- The non-strategic benchmark: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (and its own [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|failure modes]], where predictable schedules are flagged)
- Systemic channel: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]
- Hiding from the game: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] (randomisation and jitter) · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation|Smart Order Routing & Fragmentation]]

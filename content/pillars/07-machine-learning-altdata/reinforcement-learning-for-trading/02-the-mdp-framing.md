---
title: "02 — The MDP Framing: State, Action, Reward & the Bellman Equations"
tags:
  - pillar-machine-learning
  - reinforcement-learning-for-trading
  - mdp
  - bellman-equation
  - markov-property
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/01-from-zero-intuition|01 · From Zero]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Before any algorithm, the *modelling* decision that determines everything: **what is the state, what are the actions, and what exactly is the reward?** This page is the formal spine of the folder. It writes trading as a **Markov Decision Process** $(\mathcal{S},\mathcal{A},P,R,\gamma)$, shows how the Bellman equations turn that into a solvable fixed point, and — most importantly — shows how to *look* at a trading problem and choose a state representation that actually satisfies the Markov property.

The practical objective: a reader should be able to take any trading decision ("rebalance this book", "liquidate this order", "quote this market") and write down a defensible MDP, then justify *why* the Bellman equation applies. If the state is wrong, every algorithm downstream is wrong in the same way.

**The three design questions, in order of importance:**

1. **Reward.** What am I maximizing? In execution: realized proceeds minus impact minus a risk penalty. In portfolio: log growth, or mean-variance, or a drawdown-adjusted return. The reward *is* the specification of the strategy.
2. **State.** What must I remember so that the future is conditionally independent of the deeper past? Inventory, time-to-deadline, price/vol features, outstanding order size. "Enough state" is a modelling claim, not a wish.
3. **Action.** What can I actually do, and on what grid? Shares-per-interval, limit-price offsets, target-position fractions. The action space's *shape* (discrete vs continuous) determines which algorithm (Q-learning vs policy gradient) is even applicable.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The MDP and the two Bellman equations

An MDP is the tuple $(\mathcal{S},\mathcal{A},P,R,\gamma)$ with transition kernel $P(s'\mid s,a)$ and expected reward $R(s,a)=\mathbb{E}[R_{t+1}\mid S_t=s,A_t=a]$. The **state-value** and **action-value** functions under policy $\pi$ are

$$
V^\pi(s)=\mathbb{E}_\pi[G_t\mid S_t=s],\qquad Q^\pi(s,a)=\mathbb{E}_\pi[G_t\mid S_t=s,A_t=a].
$$

Expanding $G_t=R_{t+1}+\gamma G_{t+1}$ gives the **Bellman expectation equation**

$$
V^\pi(s)=\sum_{a}\pi(a\mid s)\Big[R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)\,V^\pi(s')\Big],
$$

and, taking the max over actions, the **Bellman optimality equation**

$$
\boxed{\;V^*(s)=\max_{a}\Big[R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)\,V^*(s')\Big]\;}.
$$

The optimal action-value satisfies $Q^*(s,a)=R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)\max_{a'}Q^*(s',a')$ and the optimal policy is greedy, $\pi^*(s)=\arg\max_a Q^*(s,a)$.

#### 2.2 Contraction and existence

Define the Bellman optimality operator $(\mathcal{T}V)(s)=\max_a\big[R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)V(s')\big]$. For $\gamma<1$ it is a **$\gamma$-contraction** in the sup-norm: $\|\mathcal{T}V-\mathcal{T}U\|_\infty\le\gamma\|V-U\|_\infty$. By Banach's fixed-point theorem it has a **unique** fixed point $V^*$, and value iteration $V_{k+1}=\mathcal{T}V_k$ converges geometrically at rate $\gamma$. **This is why discounted RL works at all** — and why an undiscounted ($\gamma=1$) infinite-horizon trading problem needs care (it may not contract).

#### 2.3 The trading MDP, concretely

For **optimal execution** of $X_0$ shares over $T$ steps:
- **State** $S_t=(t,\,x_t)$ — time step and shares remaining (optionally a price/volatility feature).
- **Action** $A_t=v_t$ — shares to sell this interval, $0\le v_t\le x_t$ (discrete grid or continuous).
- **Reward** $R_{t+1}=v_t\,(S_t-\eta v_t)-h\,x_t$ — proceeds net of *temporary impact* $\eta v_t$ (linear or convex) and a *holding/risk penalty* $h\,x_t$ for the inventory you still carry.
- **Dynamics** $x_{t+1}=x_t-v_t$; price is typically a martingale under the reference measure, so the only control-relevant cost is impact plus the risk of holding.

This is the canonical RL-execution formulation (Nevmyvaka–Kearns; and the DP twin of Almgren–Chriss). The **holding penalty subsumes risk aversion**: larger $h$ (or smaller $\gamma$) makes the agent sell faster.

#### 2.4 The Markov property is engineered, not assumed

The chain $S_t$ must be such that $\mathbb{E}[R_{t+1}\mid S_t,A_t]=\mathbb{E}[R_{t+1}\mid \text{history}]$. Financial state is *deliberately constructed* to satisfy this: you include the **unfilled inventory** (not just total traded), **time-to-deadline**, and enough price statistics that the conditional expectation is stable. The regime-switching analogue — where the hidden state must be *inferred* — is [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|HMM & GMM]]; here we assume the state is observed.

---

### 3. Computational Implementation — build a stochastic MDP and verify the Bellman fixed point

Here the price is a genuine **2-state Markov chain** (sticky: stays with prob $0.7$), so the MDP is stochastic and the transition kernel is explicit. We solve it by value iteration and then verify the Bellman *optimality* equation holds to machine precision. Stdlib only.

```python
# ---- Stochastic execution MDP: price is a 2-state Markov chain, plus inventory ----
# states  = (price p in {9,11}) x (inventory x in {0,1,2});  x=0 is absorbing
# actions = a in {0,1} shares sold this step
# reward  = a*(p - k) - h*x                      (proceeds minus impact, minus holding)
# price kernel: P(stay)=0.7, P(switch)=0.3       (a genuine Markov transition)
gamma, k, h = 0.9, 1.0, 0.5
PS = {9: [(9, 0.7), (11, 0.3)], 11: [(11, 0.7), (9, 0.3)]}
S = [(p, x) for p in (9, 11) for x in (0, 1, 2)]
def R(p, x, a): return 0.0 if x == 0 else a*(p - k) - h*x

# value iteration -> V* then one-step lookahead -> Q*
V = {s: 0.0 for s in S}
for _ in range(500):
    Vn = {}
    for (p, x) in S:
        if x == 0: Vn[(p, x)] = 0.0; continue
        Vn[(p, x)] = max(R(p, x, a) + gamma*sum(pr*V[(pp, x-a)] for pp, pr in PS[p])
                         for a in (0, 1) if a <= x)
    V = Vn
Q = {(p, x): {a: R(p, x, a) + gamma*sum(pr*V[(pp, x-a)] for pp, pr in PS[p])
              for a in (0, 1) if a <= x} for (p, x) in S}

print("Q*(s,a) for the stochastic execution MDP")
for p in (9, 11):
    for x in (0, 1, 2):
        qs = Q[(p, x)] if x > 0 else {}
        pretty = "  ".join(f"a={a}:{v:7.3f}" for a, v in sorted(qs.items())) if qs else "(absorbing)"
        star = "" if x == 0 else f"   -> greedy a*={max(qs, key=qs.get)}"
        print(f"  p={p}, x={x}: {pretty}{star}")

# verify the Bellman OPTIMALITY equation residual is ~0
resid = 0.0
for (p, x) in S:
    if x == 0: continue
    rhs = max(R(p, x, a) + gamma*sum(pr*V[(pp, x-a)] for pp, pr in PS[p]) for a in (0, 1) if a <= x)
    resid = max(resid, abs(V[(p, x)] - rhs))
print(f"\nmax |V* - T(V*)| (Bellman optimality residual) = {resid:.2e}")
```
```
Q*(s,a) for the stochastic execution MDP
  p=9, x=0: (absorbing)
  p=9, x=1: a=0:  6.790  a=1:  7.500   -> greedy a*=1
  p=9, x=2: a=0: 12.595  a=1: 14.290   -> greedy a*=1
  p=11, x=0: (absorbing)
  p=11, x=1: a=0:  7.510  a=1:  9.500   -> greedy a*=1
  p=11, x=2: a=0: 13.575  a=1: 17.010   -> greedy a*=1

max |V* - T(V*)| (Bellman optimality residual) = 0.00e+00
```

Two things are worth reading off. First, the **Bellman residual is exactly zero** — value iteration has found the true fixed point $V^*=\mathcal{T}V^*$, the object every learning method in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03]] and [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04]] is trying to reach. Second, the **value is state-dependent**: $Q^*(11,\cdot)>Q^*(9,\cdot)$ because holding the same inventory in a high-price state is worth more, and the greedy action can differ across price states purely because the *future* price distribution differs. A state-blind policy could not express this.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **State aliasing (Markov violation).** If two genuinely different situations are mapped to the same state $s$, the Bellman backup averages over them and $Q^*(s,\cdot)$ is a blur of two problems. Classic in execution: forgetting the *remaining* order size, or the realized volatility that determines risk-aversion. The residual test (does $V\approx\mathcal{T}V$ on held-out paths?) is your detector.
2. **Reward–risk confusion.** Encoding risk as a big holding penalty $h$ and *also* discounting aggressively $\gamma$ double-counts impatience. Be explicit about which knob carries the risk aversion — for the continuous-time version, see [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren–Chriss]] where a single $\lambda$ does it cleanly.
3. **Diagnosing the wrong component.** When a trained agent underperforms, first recompute $V^*$ by value iteration on your *simulator* and check the agent reaches it. If it does and you still lose money, the **simulator (P, R) is wrong**, not the algorithm — the single most common misdiagnosis in trading-RL.
4. **Undiscounted infinite-horizon traps.** With $\gamma=1$ and a non-absorbing chain the contraction argument fails; value iteration can diverge and Q-learning has no fixed point guarantee. Discount, or impose a hard terminal liquidation.
5. **Action-space / grid mismatch.** Discretizing shares too coarsely can make the *intended* schedule unreachable; too finely and tabular methods explode. This is a modelling cost, not a bug to be tuned away (motivating function approximation in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03]]).

---

### 5. Canonical Literature & Study References

- **Sutton & Barto**, *Reinforcement Learning: An Introduction* (2nd ed., 2018) — Ch 3 (MDP formalism, returns, policies, value functions, Bellman optimality 3.19), Ch 4 (policy/value iteration, DP as the fixed-point view). *Primary reference for this page.*
- **Bertsekas**, *Dynamic Programming and Optimal Control*, Vol I, Ch 1–2 (contraction mapping, monotonicity, convergence of value iteration). *The rigorous foundation.*
- **Bertsimas, Dimitris & Lo, Andrew W.**: "Optimal Control of Execution Costs" (*J. Financial Markets* 1(1), 1998) — the DP formulation of execution as a state/control problem.
- **Nevmyvaka, Feng & Kearns** (ICML 2006) — the state/action/reward instantiation for RL execution; detailed in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06]].
- **Puterman, Martin L.**: *Markov Decision Processes* (1994) — the definitive MDP textbook (existence, contraction, policy iteration).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03 · Value-Based RL]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04 · Policy-Gradient & Actor-Critic]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Index Hub]]
- Theory base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- State inference (when the state is hidden): [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]]
- Continuous-time cousin: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]

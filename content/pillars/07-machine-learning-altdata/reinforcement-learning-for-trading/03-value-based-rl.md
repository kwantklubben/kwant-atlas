---
title: "7.7.3 Value-Based RL"
tags:
  - pillar-machine-learning
  - reinforcement-learning-for-trading
  - q-learning
  - temporal-difference
  - dqn
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/02-the-mdp-framing|02 · The MDP Framing]] and [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]].

---

### 1. Intuition & Practical Objective

Value-based RL learns *how good each action is* and then acts greedily. It never needs a model of the market: instead of predicting the next state's probability (as value iteration does), it **bootstraps** — it uses its own current estimate of the value of the next state to improve the current estimate, watching only the realized reward and the realized next state. The celebrated update is **Q-learning**, and its deep version is **DQN**.

Practical objective: understand *why* Q-learning works (it is stochastic approximation of the Bellman optimality operator), *when* it is the right tool in trading (small, discrete action spaces — execution, sizing, regime switching), and *why* the finance setting stresses it to breaking (non-stationarity, tiny samples).

The key idea in one line: **$Q(s,a)\leftarrow Q(s,a)+\alpha\,[\,r+\gamma\max_{a'}Q(s',a')-Q(s,a)\,]$** — move the estimate of the chosen action toward the *observed* reward plus the *discounted best* value you currently believe is reachable.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Temporal-difference learning

The **TD error** $\delta_t=R_{t+1}+\gamma V(S_{t+1})-V(S_t)$ is the surprise between the bootstrapped target and the current estimate. TD(0) nudges the value by $\alpha\delta_t$:

$$
V(S_t)\leftarrow V(S_t)+\alpha\big[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\big].
$$

TD is a *stochastic approximation* of the Bellman expectation backup; it converges to $V^\pi$ for a fixed policy under decaying step sizes (Robbins–Monro conditions $\sum\alpha_t=\infty,\,\sum\alpha_t^2<\infty$).

#### 2.2 Q-learning and the max operator

Off-policy Q-learning (Watkins & Dayan 1992) approximates the **optimality** operator regardless of the behaviour policy:

$$
\boxed{\;Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha\Big[R_{t+1}+\gamma\max_{a}Q(S_{t+1},a)-Q(S_t,A_t)\Big]\;}
$$

The $\max$ is what makes it *off-policy* (it learns about the greedy policy while behaving $\epsilon$-greedily). For tabular Q-learning with $\epsilon$-greedy exploration and decaying $\alpha$, $Q\to Q^*$ with probability 1 (Watkins & Dayan). SARSA is the on-policy variant, using the *actually taken* next action $Q(S_{t+1},A_{t+1})$ instead of the max — safer under risk (it accounts for exploratory mistakes) but converges to a different, more conservative policy.

#### 2.3 Why the max overestimates — and why that matters in finance

$\mathbb{E}[\max_a Q]\ge\max_a \mathbb{E}[Q]$ (Jensen). Because Q-learning maximizes over *noisy estimates*, it systematically **overestimates** values — the **maximization bias**. In trading, overestimation bias becomes **over-trading**: the agent believes actions are better than they are and acts when it should hold. Fixes: Double Q-learning (decouple action selection from evaluation), and its deep form Double DQN. This bias is *first-principles*, present in any maximization over noisy value estimates, and is a major reason naive RL agents trade too much.

#### 2.4 DQN: value-based RL with function approximation

When the state space is large (continuous price features, portfolios), a table is impossible; DQN (Mnih et al. 2015) approximates $Q(s,a;\theta)$ with a neural network and stabilizes the divergence-prone "deadly triad" (function approximation + bootstrapping + off-policy) using two tricks:
- **Experience replay** — store transitions $(s,a,r,s')$ in a buffer and sample minibatches, breaking temporal correlation.
- **Target network** — a slowly-updated copy $Q(\cdot;\theta^-)$ supplies the bootstrap target, freezing a moving goalpost.

Loss: $L(\theta)=\mathbb{E}_{(s,a,r,s')\sim\mathcal{D}}\big[\big(r+\gamma\max_{a'}Q(s',a';\theta^-)-Q(s,a;\theta)\big)^2\big]$.

**Finance caveat:** replay assumes stationarity — the same $(s,a)$ keeps its value across time. That assumption is *precisely* what markets violate, so replay buffers that span regimes silently mix incompatible data ([[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation — tabular Q-learning recovers $Q^*$ exactly

The single most convincing demonstration: run Q-learning with **no knowledge of $P$ or $R$** (only sampled transitions) on the liquidation MDP from [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|the hub]], and show it converges to the value-iteration solution. Stdlib only.

```python
import random

# ---- Liquidation MDP: r(x,a) = a*P - k*a^2 - h*x ;  deterministic x' = x - a ----
P, k, h, gamma, N = 10.0, 2.0, 1.0, 0.9, 3
def reward(x, a): return 0.0 if x == 0 else a*P - k*a*a - h*x

# exact V* by value iteration (ground truth the agent must recover)
V = [0.0]*(N+1)
for _ in range(500):
    V = [max(reward(x,a) + gamma*V[x-a] for a in range(x+1)) for x in range(N+1)]

# tabular Q-learning, learned from sampled episodes only (no knowledge of P or r)
random.seed(1)
Q = [[random.uniform(-1, 1) for _ in range(N+1)] for _ in range(N+1)]
for a in range(N+1):
    Q[0][a] = 0.0
for ep in range(20000):
    alpha = 0.5 / (1 + ep/2000.0)            # decaying step size
    eps   = 1.0 * max(0.0, 1 - ep/4000.0)    # decaying exploration
    x = N
    while x > 0:
        a = random.randint(0, x) if random.random() < eps else max(range(x+1), key=lambda aa: Q[x][aa])
        target = reward(x, a) + (gamma*max(Q[x-a][:x-a+1]) if x-a > 0 else 0.0)
        Q[x][a] += alpha*(target - Q[x][a])
        x -= a

Vq  = [max(Q[x][:x+1]) for x in range(N+1)]
pol = [max(range(x+1), key=lambda a: Q[x][a]) for x in range(N+1)]
print("            x=0      x=1      x=2      x=3")
print(f"V* exact   {V[0]:7.3f} {V[1]:7.3f} {V[2]:7.3f} {V[3]:7.3f}")
print(f"V_Q-learn  {Vq[0]:7.3f} {Vq[1]:7.3f} {Vq[2]:7.3f} {Vq[3]:7.3f}")
print(f"greedy*    {pol[0]:7d} {pol[1]:7d} {pol[2]:7d} {pol[3]:7d}")
print(f"max |V_Q - V*| = {max(abs(Vq[i]-V[i]) for i in range(N+1)):.4f}")
```
```
            x=0      x=1      x=2      x=3
V* exact     0.000   7.000  12.300  16.070
V_Q-learn    0.000   7.000  12.300  16.070
greedy*          0       1       1       1
max |V_Q - V*| = 0.0000
```

Q-learning, seeing only $(x,a,r,x')$ samples, reproduces the exact $V^*$ to $0.0000$ and the exact greedy policy $[0,1,1,1]$. **This is the promise of value-based RL**: learn the optimal control from experience, without a model. Note both hardcoded facts it needed — **exploration that decays** (otherwise it never visits and refines the good actions) and a **step-size schedule that decays** (otherwise the estimates never settle). Remove either and the result degrades; that sensitivity is the practical cost of being model-free.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Maximization bias → over-trading.** The $\max$ in Q-learning inflates values under noise (Jensen), so the learned policy acts too often. Use Double Q-learning / Double DQN. In a market with costs, "acting a little too often" is a direct, measurable P&L leak.
2. **Exploration is dangerous in trading.** $\epsilon$-greedy exploration *executes real trades* in production. Either explore only in simulation, or replace random exploration with *safe* exploration (small perturbations around a known-good baseline, e.g. TWAP).
3. **The deadly triad.** Function approximation + bootstrapping + off-policy can diverge. DQN's replay and target network are *stability hacks*, not proofs; the failure modes (semi-gradient divergence, Tsitsiklis & Van Roy) are real, especially with a non-stationary target.
4. **Replay assumes stationarity.** A huge replay buffer mixes transitions from different regimes; the network learns an average that is optimal for none. Time-limited buffers or regime-stratified replay help but do not solve it.
5. **Sample inefficiency.** Tabular Q-learning is *cheap* only because it is tiny. DQN needs $10^5$–$10^7$ transitions; finance gives one path. The usual workaround — train in a simulator — imports the simulator's biases wholesale (the sim-to-real gap, [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05]]).
6. **Discrete-action limitation.** Q-learning needs a $\max$ over a finite action set. Continuous sizing / portfolio weights require either discretization (coarse, and the grid itself is a modelling error) or the policy-gradient methods of [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04]].

---

### 5. Canonical Literature & Study References

- **Sutton & Barto**, *Reinforcement Learning: An Introduction* (2nd ed., 2018) — Ch 6 (TD learning), Ch 6.5 (Q-learning), Ch 7 (n-step, eligibility traces), Ch 9–11 (function approximation, the deadly triad, off-policy divergence). *Primary reference.*
- **Watkins, Christopher & Dayan, Peter**: "Q-learning" (*Machine Learning* 8, 1992) — convergence of tabular Q-learning.
- **van Hasselt, Hado; Guez, Arthur & Silver, David**: "Deep Reinforcement Learning with Double Q-learning" (AAAI 2016) — the maximization-bias fix.
- **Mnih, Volodymyr et al.**: "Human-level Control through Deep Reinforcement Learning" (*Nature* 518, 2015) — DQN: replay + target network.
- **Sutton, Richard S.**: "Learning to Predict by the Methods of Temporal Differences" (*Machine Learning* 3, 1988) — the original TD paper.
- **Deng, Yue et al.**: "Deep Direct Reinforcement Learning for Financial Signal Representation and Trading" (*IEEE TNNLS*, 2017) — a concrete (and realistically modest) deep-RL trading system.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/02-the-mdp-framing|02 · The MDP Framing]]
- Forward: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04 · Policy-Gradient & Actor-Critic]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Index Hub]]
- Function approximators: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] (LSTM/TCN/Transformer value networks)
- Practical application: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06 · Advanced Extensions (Execution RL)]]

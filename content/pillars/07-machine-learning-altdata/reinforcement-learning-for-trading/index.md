---
title: "Reinforcement Learning for Trading"
tags:
  - pillar-machine-learning
  - reinforcement-learning-for-trading
  - reinforcement-learning
  - mdp
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Supervised learning predicts a label; reinforcement learning (RL) **chooses an action and lives with the consequence**. In trading this is the correct abstraction for everything sequential and path-dependent: *how much to buy now given the inventory you still must liquidate, the impact you have already caused, and the risk you are carrying.* Unlike a return forecast, an execution or portfolio decision changes the state you will face next — sell too fast and you pay impact, sell too slow and you carry price risk. RL is the branch of machine learning that optimizes exactly this closed-loop, state-dependent control problem.

This folder is the **machine-learning pillar's control-theory topic-folder**. It is a *hub*: it (a) gives you the **fast algorithm lookup** below (job #1 of the topic), and (b) routes you to six sub-pages that build the intuition from zero, formalize the MDP, derive value-based and policy-gradient methods, name the failure modes honestly, and land on the one place RL has genuinely earned its keep in finance — **optimal trade execution**.

> **The one-sentence essence.** "Model trading as a Markov decision process — state (inventory, prices, time), action (how much to trade), reward (P&L net of costs) — and learn a *policy* that maximizes expected discounted reward; the hard parts are not the algorithms (Q-learning and policy gradients are a page of math) but the *reward design*, the *sim-to-real gap*, *non-stationarity*, and the fact that finance gives you one non-repeatable episode instead of a million resettable ones."

**Honesty clause (read before deploying anything).** RL is the most over-promised technique in quantitative finance. The results that survive scrutiny are narrow and specific — chiefly *execution / order-scheduling* under a known impact model (Nevmyvaka & Kearns 2006; Ning, Lin & Jaimungal 2018). End-to-end "RL beat the market" claims almost always fail out of sample because the simulator is wrong, the reward is gameable, and the market adapts. This folder teaches the machinery **and** the reasons it usually disappoints.

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** The Bellman equations and the four core updates. Notation: $S$ state, $A$ action, $R$ reward, $\gamma\in[0,1)$ discount, $\alpha$ learning rate, $\tau$ temperature, $\theta$ policy parameters, $\pi_\theta(a\mid s)$ policy, $V^\pi$, $Q^\pi$, $V^*=\max_\pi V^\pi$.

| Quantity | Equation |
|---|---|
| Return (discounted) | $G_t=\sum_{k=0}^{\infty}\gamma^k R_{t+k+1}$ |
| State value $V^\pi$ | $V^\pi(s)=\mathbb{E}_\pi\!\left[G_t\mid S_t=s\right]$ |
| Action value $Q^\pi$ | $Q^\pi(s,a)=\mathbb{E}_\pi\!\left[G_t\mid S_t=s,A_t=a\right]$ |
| **Bellman expectation** | $V^\pi(s)=\sum_a\pi(a\mid s)\!\left[R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)V^\pi(s')\right]$ |
| **Bellman optimality** | $V^*(s)=\max_a\!\left[R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)V^*(s')\right]$ |
| Optimal policy (greedy) | $\pi^*(s)=\arg\max_a Q^*(s,a)$ |
| **TD(0) value update** | $V(S_t)\leftarrow V(S_t)+\alpha\!\left[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\right]$ |
| **Q-learning update (off-policy)** | $Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha\!\left[R_{t+1}+\gamma\max_a Q(S_{t+1},a)-Q(S_t,A_t)\right]$ |
| **SARSA update (on-policy)** | $Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha\!\left[R_{t+1}+\gamma Q(S_{t+1},A_{t+1})-Q(S_t,A_t)\right]$ |
| **Policy-gradient theorem** | $\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\nabla_\theta\log\pi_\theta(A_t\mid S_t)\,G_t\right]$ |
| Softmax policy | $\pi_\theta(a\mid s)=\dfrac{e^{\theta_{s,a}/\tau}}{\sum_{a'}e^{\theta_{s,a'}/\tau}}$ |

**Verified checks (from §3, stdlib only).** Value iteration on the liquidation MDP gives $V^*=(0,\,7.000,\,12.300,\,16.070)$ with greedy policy $[0,1,1,1]$; a **tabular Q-learning agent recovers it to $0.0000$** max error; the **Bellman optimality residual** on the stochastic execution MDP is $0.00\times10^{0}$; a **REINFORCE** agent converges to the same greedy policy $[0,1,1,1]$.

> **The one caveat that matters.** All three families (DP, TD/Q-learning, policy gradient) are solving *the same* Bellman fixed point. If they disagree, the bug is in the *reward or the state*, not in the optimizer — which is why §4 and [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]] spend most of their time on reward and state design, not on algorithms.

---

### 3. Computational Implementation — the Bellman engine

This runs on the **standard library only**. It is the mental template for the whole folder: define a small trading MDP, solve it exactly with value iteration, and remember this number — every RL agent in the sub-pages must match it.

```python
import math

# ---- Toy liquidation MDP: state x = shares left, action a = shares sold now ----
# r(x,a) = a*P - k*a^2 - h*x   (revenue, convex temporary impact, holding penalty)
P, k, h, gamma, N = 10.0, 2.0, 1.0, 0.9, 3
def reward(x, a): return 0.0 if x == 0 else a*P - k*a*a - h*x

# Bellman optimality via value iteration (the ground truth every RL agent must match)
V = [0.0]*(N+1)
for _ in range(500):
    V = [max(reward(x,a) + gamma*V[x-a] for a in range(x+1)) for x in range(N+1)]
pol = [max(range(x+1), key=lambda a: reward(x,a) + gamma*V[x-a]) for x in range(N+1)]
print("Bellman value iteration (exact V* and greedy policy):")
for x in range(N+1):
    print(f"  x={x}: V*(x)={V[x]:7.4f}   greedy = sell {pol[x]}")
```
```
Bellman value iteration (exact V* and greedy policy):
  x=0: V*(x)= 0.0000   greedy = sell 0
  x=1: V*(x)= 7.0000   greedy = sell 1
  x=2: V*(x)=12.3000   greedy = sell 1
  x=3: V*(x)=16.0700   greedy = sell 1
```

Note the *non-monotone* optimal action: with $x$ shares left the agent sells **one** at a time even though selling all at once is available — convex impact ($ka^2$) makes gradual liquidation optimal. This is precisely the trade-off that Almgren–Chriss solves in closed form ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]) and that an RL agent must rediscover from experience.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full treatment lives in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Reward hacking** — the agent optimizes the *proxy* you wrote, not the objective you meant. A gross-P&L reward ignores impact, so the agent churns (verified: net value $9.00$ vs the correct $16.07$, a $7.07$ loss).
2. **The sim-to-real gap** — the agent overfits the simulator's micro-behaviour (fills, latency, impact). Your backtest environment is the model, and it is wrong.
3. **Non-stationarity** — a policy tuned to one regime (drift, vol, impact) decays in the next; the market is an adversary that arbitrages away your edge (verified: a stale drift policy loses $0.52$ immediately on a sign flip).
4. **Sample inefficiency** — finance offers *one* historical path and no resets; deep RL needs $10^5$–$10^7$ episodes. Simulation on a wrong impact model is the standard, and usually fatal, workaround.
5. **Backtest overfitting of the policy itself** — an RL agent with a large state/action space is an extremely flexible model; it will memorize noise unless evaluated with purged CV / deflated Sharpe ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|Financial ML Pitfalls · 05]]).

---

### 5. Canonical Literature & Study References

- **Sutton, Richard S. & Barto, Andrew G.**: *Reinforcement Learning: An Introduction* (2nd ed., MIT Press, 2018) — the canonical text; Ch 3 (MDPs, Bellman equations), Ch 4 (DP), Ch 6 (TD learning), Ch 9 (function approximation), Ch 13 (policy gradients). *The backbone for every sub-page here.*
- **Bertsekas, Dimitri P.**: *Dynamic Programming and Optimal Control*, Vol I–II — the rigorous DP/martingale foundation behind the Bellman equations.
- **Nevmyvaka, Yuriy; Feng, Yi & Kearns, Michael**: "Reinforcement Learning for Optimized Trade Execution" (ICML 2006) — the foundational execution-RL paper; the anchor of [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06 · Advanced Extensions]].
- **Bertsimas, Dimitris & Lo, Andrew W.**: "Optimal Control of Execution Costs" (*Journal of Financial Markets* 1(1), 1998) — the pre-RL dynamic-programming formulation of the same problem.
- **Moody, John & Saffell, Matthew**: "Learning to Trade via Direct Reinforcement" (*IEEE Trans. Neural Networks* 12(4), 2001) — recurrent RL optimizing a Sharpe-like differential objective directly on price series.
- **Mnih, Volodymyr et al.**: "Human-level Control through Deep Reinforcement Learning" (*Nature* 518, 2015) — DQN, the template for deep value-based agents.
- **Schulman, John et al.**: "Proximal Policy Optimization Algorithms" (arXiv:1707.06347, 2017) — PPO, the default policy-gradient method in finance RL frameworks (incl. Qlib's RL module).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory (Markov chains, conditional expectation)]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization (gradients, fixed points)]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series (Markov structure, non-stationarity)]]
- Sibling topics (in-pillar): [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] (the function approximators RL policies are built on) · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] (Markov state) · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] (why the backtest lies)
- Execution & cost cousins: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP/TWAP/POV]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]
- Sub-pages (in-folder): 01 From Zero · 02 The MDP Framing · 03 Value-Based RL · 04 Policy-Gradient & Actor-Critic · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/01-from-zero-intuition|01 · From Zero]] — no prior RL needed.
- **Formal + code (undergrad/job-seeking):** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/02-the-mdp-framing|02 · The MDP Framing]] → [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03 · Value-Based RL]] → [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04 · Policy-Gradient & Actor-Critic]].
- **Robustness (practitioner/graduate):** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06 · Advanced Extensions (Optimal Execution RL)]].
- Forward links: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren–Chriss]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]]

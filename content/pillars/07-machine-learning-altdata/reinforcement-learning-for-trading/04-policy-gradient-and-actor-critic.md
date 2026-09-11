---
title: "04 — Policy-Gradient & Actor-Critic: REINFORCE, A2C, PPO"
tags:
  - pillar-machine-learning
  - reinforcement-learning-for-trading
  - policy-gradient
  - reinforce
  - actor-critic
  - ppo
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03 · Value-Based RL]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]].

---

### 1. Intuition & Practical Objective

Value-based methods learn *values* and *derive* a policy by taking an argmax. Policy-gradient methods reverse it: **parameters the policy directly** and climb the gradient of expected return. The policy is a distribution $\pi_\theta(a\mid s)$ — a softmax over actions, a Gaussian over trade sizes — and we ascend $\nabla_\theta J(\theta)$.

Why bother? Because policy gradients handle what Q-learning cannot:
- **Continuous actions** — trade *any* fraction of inventory, not a grid.
- **Stochastic policies** — the optimal execution policy is genuinely randomized when time-to-deadline is unknown; a softmax/Gaussian *is* the right object.
- **The likelihood-ratio trick** — no $\max$ over noisy estimates, so no maximization bias and often smoother optimization.

The finance payoff is concrete: execution and portfolio-weight problems are *continuous-control* problems where the policy-gradient family (especially **PPO**) is the default. Practical objective: derive the policy-gradient theorem, implement REINFORCE with a baseline, and understand actor–critic as the variance-reduced version.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The objective and the score-function (REINFORCE) estimator

Define the performance objective $J(\theta)=\mathbb{E}_{\tau\sim\pi_\theta}[G_0]=\mathbb{E}_{\pi_\theta}\!\big[\sum_t\gamma^t R_{t+1}\big]$. The **policy-gradient theorem** (Sutton et al. 2000) states, for the episodic case,

$$
\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\sum_{t}\nabla_\theta\log\pi_\theta(A_t\mid S_t)\,G_t\right].
$$

The derivation uses the **likelihood-ratio identity** $\nabla_\theta \pi_\theta=\pi_\theta\,\nabla_\theta\log\pi_\theta$, which lets the gradient be estimated from *sampled trajectories alone* — no model of the environment. This is the REINFORCE estimator (Williams 1992):

$$
\theta\leftarrow\theta+\alpha\,\nabla_\theta\log\pi_\theta(A_t\mid S_t)\,G_t.
$$

**Intuition:** increase the log-probability of actions that led to high return, decrease it for low-return actions, weighted by how large the return was.

#### 2.2 Variance and the baseline

REINFORCE is unbiased but *high variance* — returns scale across orders of magnitude and the estimator uses the full noisy $G_t$. Subtracting any baseline $b(s)$ independent of the action leaves the estimate **unbiased** (because $\sum_a\pi_\theta(a\mid s)\nabla_\theta\log\pi_\theta(a\mid s)=0$) while shrinking variance:

$$
\nabla_\theta J\approx\nabla_\theta\log\pi_\theta(A_t\mid S_t)\,\big(G_t-b(S_t)\big).
$$

The optimal baseline is the state value $b(s)=V^\pi(s)$, turning the weight into the **advantage** $A_t=G_t-V(S_t)$ — *how much better than average this action was*. Using the TD error $\delta_t=R_{t+1}+\gamma V(S_{t+1})-V(S_t)$ as the advantage estimate gives **actor–critic**: the *actor* $\pi_\theta$ chooses actions, the *critic* $V_w$ estimates values and supplies the baseline.

#### 2.3 Actor–critic updates

Two time-scale updates: the critic regresses onto its bootstrapped target,
$$
w\leftarrow w+\beta\,\delta_t\nabla_w V_w(S_t),\qquad \delta_t=R_{t+1}+\gamma V_w(S_{t+1})-V_w(S_t),
$$
and the actor ascends the advantage-weighted log-policy, $\theta\leftarrow\theta+\alpha\,\delta_t\nabla_\theta\log\pi_\theta(A_t\mid S_t)$. **A2C** runs this synchronously across parallel environments; **PPO** (Schulman et al. 2017) replaces the raw step with a *clipped* importance-ratio objective
$$
L^{\text{CLIP}}(\theta)=\mathbb{E}\!\left[\min\!\big(r_t(\theta)A_t,\ \mathrm{clip}(r_t(\theta),1-\epsilon,1+\epsilon)A_t\big)\right],\quad r_t=\frac{\pi_\theta(A_t\mid S_t)}{\pi_{\theta_{\text{old}}}(A_t\mid S_t)},
$$
which bounds how far one update can move the policy — the reason PPO is the *stable* default in finance RL frameworks.

#### 2.4 The natural-gradient view

The softmax-policy parameter is not the "right" coordinate; the **natural gradient** $\tilde\nabla J=\mathcal{F}^{-1}\nabla J$ (Fisher information $\mathcal{F}$) rescales updates to be invariant to reparameterization and speeds convergence. TRPO, and to a first order PPO, are practical approximations of the natural-gradient step. For trading this matters because naive gradient descent on a squashed policy can stall in flat softmax regions.

---

### 3. Computational Implementation — REINFORCE learns the optimal execution policy

Same liquidation MDP as [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03]], now solved by **policy gradient**: a per-state softmax over actions, updated by the score-function rule with a running-mean baseline. It should converge to the same optimal policy value iteration found. Stdlib only.

```python
import random, math

# ---- Same liquidation MDP as 03, now solved by POLICY GRADIENT (REINFORCE) ----
P, k, h, gamma, N = 10.0, 2.0, 1.0, 0.9, 3
def reward(x, a): return 0.0 if x == 0 else a*P - k*a*a - h*x

random.seed(3)
theta = [[0.0]*(N+1) for _ in range(N+1)]     # softmax logits theta[x][a] for a in 0..x
base  = 0.0                                   # running-mean baseline (variance reduction)
softmax = lambda z: [math.exp(v-max(z))/sum(math.exp(u-max(z)) for u in z) for v in z]

def run_episode(alpha=0.02):
    global base
    x, traj = N, []
    while x > 0:
        p = softmax(theta[x][:x+1]); r = random.random(); c = 0.0; a = 0
        for i, pi in enumerate(p):
            c += pi
            if r < c: a = i; break
        traj.append((x, a, reward(x, a))); x -= a
    G, rets = 0.0, []
    for (_, _, rr) in reversed(traj):
        G = rr + gamma*G; rets.append(G)
    rets.reverse()
    for (x, a, _), Gt in zip(traj, rets):
        p = softmax(theta[x][:x+1])
        for i in range(x+1):
            theta[x][i] += alpha*(Gt-base)*((1.0 if i == a else 0.0) - p[i])   # score-function grad
    base += 0.01*(Gt - base)

for _ in range(100000):
    run_episode(0.02)

pol = [max(range(x+1), key=lambda a: theta[x][a]) for x in range(N+1)]
print("REINFORCE learned greedy policy :", pol, "   (exact optimal = [0, 1, 1, 1])")
for x in (2, 3):
    p = softmax(theta[x][:x+1])
    print(f"  pi(.|x={x}): " + "  ".join(f"a={a}:{p[a]:.3f}" for a in range(x+1)))
```
```
REINFORCE learned greedy policy : [0, 1, 1, 1]    (exact optimal = [0, 1, 1, 1])
  pi(.|x=2): a=0:0.000  a=1:1.000  a=2:0.000
  pi(.|x=3): a=0:0.000  a=1:0.999  a=2:0.001  a=3:0.000
```

The policy-gradient agent **recovers the exact optimal policy** $[0,1,1,1]$ found by value iteration, and the softmax becomes near-deterministic on the optimal action ($0.999$ on "sell 1" at $x=3$). Two lessons are visible in the code. First, the update is a pure **score-function** rule — `(1{a chosen} − π(a))` is $\nabla_\theta\log\pi_\theta$ for a softmax — requiring only sampled returns. Second, the **baseline `base`** is not cosmetic: without it the estimator's variance is large enough that this small problem converges slowly or erratically; with it, it is stable.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **High variance / slow learning.** The vanilla REINFORCE gradient is unbiased but noisy; on a low-SNR trading problem the variance can exceed the signal. Always use a baseline (a critic) and, in practice, GAE or a clipped objective.
2. **Reward scaling and P&L units.** Policy gradients are sensitive to return magnitude — P&L in dollars vs basis points change the effective learning rate drastically. Normalize the reward; otherwise "one big trade" dominates the gradient.
3. **Entropy collapse and premature determinism.** A softmax policy can sharpen to a suboptimal action early and then never explore out of it (the positive-feedback loop of "chosen → reinforced"). Monitor policy entropy; add an entropy bonus.
4. **The critic's bootstrap bias.** Actor–critic uses a *bootstrapped* critic, so it inherits the sim-to-real gap and the deadly-triad instability of value-based methods — you have not escaped the Bellman target, only softened it.
5. **Off-policy correction instabilities.** PPO/TRPO need the ratio $r_t$ to stay near $1$; under heavy non-stationarity the "old" policy is quickly irrelevant and the clips bind, stalling learning. In finance this is severe because a single update can span a regime change.
6. **Deterministic-evaluation trap.** A stochastic policy looks good in expectation but a *deterministic* deployment of its mean can be much worse (and vice-versa). Always evaluate the *deployed* policy, not just $J(\theta)$ — see [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Sutton, Richard S. & Barto, Andrew G.**: *Reinforcement Learning: An Introduction* (2nd ed., 2018) — Ch 13 (policy-gradient methods, the policy-gradient theorem 13.5, REINFORCE, baselines, actor–critic).
- **Williams, Ronald J.**: "Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning" (*Machine Learning* 8, 1992) — the original REINFORCE.
- **Sutton, Richard S.; McAllester, David; Singh, Satinder & Mansour, Yishay**: "Policy Gradient Methods for Reinforcement Learning with Function Approximation" (NeurIPS 2000) — the policy-gradient theorem with the compatible-function-approximation result.
- **Schulman, John et al.**: "Proximal Policy Optimization Algorithms" (arXiv:1707.06347, 2017) — PPO; the stable default in trading-RL frameworks (including Qlib's RL module).
- **Mnih, Volodymyr et al.**: "Asynchronous Methods for Deep Reinforcement Learning" (ICML 2016) — A3C/A2C, the parallel-advantage actor–critic template.
- **Konda, Vijay & Tsitsiklis, John**: "Actor-Critic Algorithms" (NeurIPS 1999) — the two-time-scale actor–critic convergence result.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03 · Value-Based RL]]
- Forward: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Index Hub]]
- Optimizers base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Function approximators: [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
- Continuous-control application: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]

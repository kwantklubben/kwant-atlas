---
title: "01 — Reinforcement Learning for Trading from Zero: Intuition & the Why"
tags:
  - pillar-machine-learning
  - reinforcement-learning-for-trading
  - intuition
  - sequential-decision
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory (conditional expectation)]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of reinforcement learning with **no prior RL knowledge needed**. The objective is one idea: **some financial decisions are not predictions but *actions* whose consequences change the situation you will face next — and those are exactly the problems a supervised model cannot solve.**

Start with the dumbest question: *why isn't a return forecast enough?* A supervised model answers "what will the price do?" That is a *prediction*. But a trader's problem is "given what I hold and where I am in the day, how much do I trade *now*?" That is a *decision*. The two differ because the decision feeds back:

1. **The action changes the state.** Sell 5,000 shares now and the price moves; the price you get for the *next* 5,000 is worse. A forecaster treats the market as a fixed backdrop; the trader's own trades *are part of the market* for as long as the order is working.

2. **The reward is delayed and path-dependent.** You cannot score a single trade in isolation. The value of selling slowly is that you avoid impact (good now) but carry risk (bad later). Judgment requires a *sequence* of actions, judged by the total.

3. **Only trial-and-error can find the policy.** There is no labelled dataset of "the optimal number of shares to sell at 10:03 for this inventory." You have to try, observe the P&L, and adjust. That loop — *act, observe reward, update policy* — is reinforcement learning.

**Three "aha"s.**

1. **RL is goal-directed control, not prediction.** The object learned is a *policy* $\pi(a\mid s)$: a mapping from *situations* to *actions*. It is not a forecast; it is a plan you can execute.
2. **The reward function is the whole game.** You do not get credit for a "clever" algorithm. You get credit for the objective you encoded. Get the reward wrong and a brilliant optimizer will faithfully maximize the wrong thing ([[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **Context matters — "always do X" is rarely optimal.** The optimal action depends on the state. This is why even a *one-step* trading decision, done right, is state-dependent.

---

### 2. Mathematical Ground Truth & Derivations

**The decision loop, formally.** At each time step $t$ the agent observes a state $S_t$, picks an action $A_t\sim\pi(\cdot\mid S_t)$, receives reward $R_{t+1}$, and lands in a new state $S_{t+1}$. The agent's goal is to maximize the expected **discounted return**

$$
G_t=\sum_{k=0}^{\infty}\gamma^{k}R_{t+k+1},\qquad \gamma\in[0,1).
$$

The discount $\gamma$ is not a technicality — in trading it is the *time value of waiting*: a dollar of P&L realized later is worth less, and for an execution problem $\gamma$ encodes how much you fear the price wandering while your order is unfilled.

**The value of acting — the action-value function.** The natural object is $Q^\pi(s,a)$, the expected return of taking action $a$ in state $s$ and then following policy $\pi$:

$$
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[G_t\mid S_t=s,\,A_t=a\right].
$$

A policy is *better* if its $Q$ is larger; the best possible policy obeys the **Bellman optimality equation**

$$
Q^*(s,a)=R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)\,\max_{a'}Q^*(s',a'),
$$

and the optimal action in any state is simply $a^*=\arg\max_a Q^*(s,a)$. **This one equation is the target every value-based method in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/03-value-based-rl|03 · Value-Based RL]] chases.** Policy-gradient methods in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04]] reach the same objective by climbing the gradient of expected return instead.

**Why the Markov assumption is a modelling choice, not a gift.** The Bellman equation is exact only if $S_t$ summarizes everything relevant about the past — the **Markov property**. In trading you *engineer* this: inventory, time-to-deadline, realized volatility, imbalance. If your state omits something the reward depends on (e.g. the unfilled part of your order), the MDP is misspecified and no algorithm saves you. (Compare the Markov-switching state of [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|HMM & GMM]].)

---

### 3. Computational Implementation — the smallest possible trading MDP

The most convincing way to *see* "state-dependent policy beats a fixed rule": a one-step contextual decision with three market states. In each state the agent may **trade** (earn a noisy edge $\alpha_s$, pay a cost $c$) or **hold** (earn $0$). The exact optimum is "trade iff $\alpha_s>c$," but RL has to *discover* which states those are by sampling. Stdlib only.

```python
import random

# ---- One-step "contextual" trading MDP: 3 market states, trade or hold ----
# Trading in state s pays a noisy alpha E[a_s]; holding pays 0; acting costs COST.
states = {0: 0.30, 1: -0.10, 2: 0.55}     # true expected payoff of TRADING in each state
COST = 0.20
def sample(s): return random.gauss(states[s], 0.8)

# --- exact optimum: trade iff expected payoff exceeds the cost ---
print("state : E[trade]   trade? (exact)")
for s, e in states.items():
    print(f"  {s}   :  {e:+.2f}     {'YES' if e > COST else 'no'}")

# --- RL by trial and error: epsilon-greedy running-mean estimate of Q(state,action) ---
random.seed(0)
Q = {(s, a): 0.0 for s in states for a in (0, 1)}    # a=1 trade, a=0 hold
Nvis = {(s, a): 0 for s in states for a in (0, 1)}
for _ in range(4000):
    s = random.choice(list(states))
    a = random.randint(0, 1) if random.random() < 0.3 else max((0, 1), key=lambda x: Q[(s, x)])
    r = (sample(s) - COST) if a == 1 else 0.0
    Nvis[(s, a)] += 1
    Q[(s, a)] += (r - Q[(s, a)]) / Nvis[(s, a)]      # running mean

print("\nlearned: Q(state,trade) vs Q(state,hold) -> policy")
for s in states:
    q = Q[(s, 1)]
    print(f"  state {s}: Q(trade)={q:+.3f}  Q(hold)={Q[(s,0)]:+.3f}  -> learned action = {'trade' if q > Q[(s,0)] else 'hold'}")
```
```
state : E[trade]   trade? (exact)
  0   :  +0.30     YES
  1   :  -0.10     no
  2   :  +0.55     YES

learned: Q(state,trade) vs Q(state,hold) -> policy
  state 0: Q(trade)=+0.096  Q(hold)=+0.000  -> learned action = trade
  state 1: Q(trade)=-0.364  Q(hold)=+0.000  -> learned action = hold
  state 2: Q(trade)=+0.360  Q(hold)=+0.000  -> learned action = trade
```

The learned policy **matches the exact optimum** (trade in states 0 and 2, hold in state 1) and the learned $Q$ values track the true edge minus cost ($+0.30-0.20\approx+0.10$, $+0.55-0.20\approx+0.35$, $-0.10-0.20\approx-0.30$), with the gap being sampling noise. **The state dependence is the whole point**: "always trade" would have traded in state 1 and destroyed value. RL found the *conditional* rule from experience.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "it's just a fancy classifier" trap.** RL is not supervised learning with a different loss. If your problem has no *action that affects the next state*, use supervised learning — RL only adds variance and complexity. If it *does* feed back (impact, inventory, risk limits), supervised learning is structurally wrong.
2. **Reward misspecification.** The agent maximizes exactly what you wrote. Reward raw P&L and the agent learns to trade aggressively (ignoring impact); reward trade *count* and it learns to churn. The objective you *intend* must be the objective you *encode* — see [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/05-failure-modes-and-practice|05 · Failure Modes]].
3. **The Markov-state illusion.** "More features" is not the same as "enough state." If the reward depends on hidden variables (queue position, unfilled size, regime), the learned policy is optimizing a misspecified world. This is the RL analogue of omitted-variable bias.
4. **Discounting as a hidden risk preference.** $\gamma$ silently sets how much the agent fears the future. Set it carelessly and you have smuggled in a risk attitude you never chose; it interacts directly with the risk-aversion of Almgren–Chriss ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren–Chriss]]).

---

### 5. Canonical Literature & Study References

- **Sutton, Richard S. & Barto, Andrew G.**: *Reinforcement Learning: An Introduction* (2nd ed., 2018) — Ch 1 (the RL problem), Ch 2 (multi-armed bandits, explore/exploit), Ch 3 (MDPs, return, value functions, Bellman). *This page is Ch 1–3 in finance clothing.*
- **Bertsekas, Dimitri P.**: *Dynamic Programming and Optimal Control*, Vol I — the value-function formalism behind Bellman.
- **Nevmyvaka, Feng & Kearns** (ICML 2006) — the execution-RL paper; skim the introduction for *why* trading is an RL problem, then read the detail in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06 · Advanced Extensions]].
- **López de Prado, Marcos**: *Advances in Financial Machine Learning*, Ch 1 — why supervised financial ML already struggles, the necessary backdrop for what RL can and cannot add.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Sibling: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] (the Markov state of the market) · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
- Continue: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/02-the-mdp-framing|02 · The MDP Framing]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Index Hub]]
- Execution context: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]

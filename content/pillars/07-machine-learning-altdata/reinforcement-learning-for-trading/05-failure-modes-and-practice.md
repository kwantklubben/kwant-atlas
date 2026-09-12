---
title: "7.7.5 Failure Modes & Real-World Practice"
tags:
  - pillar-machine-learning
  - reinforcement-learning-for-trading
  - failure-modes
  - reward-hacking
  - sim-to-real
  - non-stationarity
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04 · Policy-Gradient & Actor-Critic]] and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]].

---

### 1. Intuition & Practical Objective

RL for trading is *mathematically beautiful and empirically disappointing in specific, namable ways*. This page names them precisely so a practitioner knows which assumptions to distrust and how the failures show up in money terms. The objective is not cynicism - it is the discipline of knowing exactly where an RL pipeline breaks so the residual risk can be measured and bounded.

The failures, one line each:
1. **Reward hacking** - the agent maximizes your *proxy* for profit, not profit; a wrong reward is faithfully exploited.
2. **The sim-to-real gap** - the learned policy is optimal for the *simulator's* micro-behaviour (fills, latency, impact), which is a model and therefore wrong.
3. **Non-stationarity** - a policy tuned to one regime (drift, vol, impact, flow) decays or inverts in the next.
4. **Sample inefficiency** - finance gives one non-repeatable path and no resets; deep RL wants millions of resettable episodes.

> **The one-line takeaway.** "RL is an *optimizer*: it will find and exploit every discrepancy between your reward, your simulator, and reality. In trading, that discrepancy is not a nuisance - it is the entire problem."

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.** Every RL guarantee (Q-learning convergence, policy-gradient ascent) rests on a **fixed MDP**:
- **(A1) A correct reward $R$** - the encoded scalar equals the true objective (net-of-cost P&L plus the intended risk penalty).
- **(A2) A correct simulator $P$** - the transition model the agent trains in matches the market's response to its actions (impact, fills, latency).
- **(A3) Stationarity** - $P$ and $R$ do not change over the training/deployment horizon.
- **(A4) Enough resettable samples** - the agent can revisit states repeatedly to average out noise.

No assumption holds cleanly in markets, and each failure is *quantifiable*.

**Reward hacking, formally.** The agent solves $\max_\theta \mathbb{E}_{\pi_\theta}[\sum_t R^{\text{proxy}}_t]$, which equals the true objective only if $R^{\text{proxy}}=R^{\text{true}}$. A gross-P&L reward omits impact $k v^2$ and holding cost $h x$, so the *optimal* policy under $R^{\text{proxy}}$ is the front-loaded "sell everything immediately" policy - optimal for the proxy, catastrophic for real net P&L.

**Sim-to-real, formally.** Let $P^\star$ be the true market and $P_\theta$ the simulator. The deployed value is $J_{P^\star}(\pi^\ast_{\text{sim}})$, whereas the agent optimized $J_{P_{\text{sim}}}(\cdot)$. The gap is bounded by a *simulator-mismatch* term (analogous to the simulation lemma):
$$
\big|J_{P^\star}(\pi)-J_{P_{\text{sim}}}(\pi)\big|\lesssim\frac{\gamma}{(1-\gamma)^2}\,\big\|P^\star-P_{\text{sim}}\big\|_\infty\,R_{\max},
$$
so **any** simulator error is amplified by $1/(1-\gamma)^2$. Long-horizon ($\gamma\to1$) execution RL is therefore *extremely* sensitive to getting the impact model right.

**Non-stationarity, formally.** If the reward/transition changes at an unknown time $\tau$ (regime shift), the value function learned for $t<\tau$ carries a **misspecification term** in the new regime of the same form as in [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/04-non-stationarity-and-samples|04 · Non-Stationarity & Samples]]: even a *perfectly* fit policy is wrong by the parameter change. A learned *policy* is a statement about the *current* data-generating process, and its guarantees expire when that process changes.

---

### 3. Computational Implementation - the failures, in numbers

Two experiments on the liquidation MDP from the hub. **Experiment 1** trains an agent to maximize *gross* proceeds (no impact, no holding cost) - the "obvious" reward - and then scores it under the *true* net objective; the wrong reward produces a measurably worse policy. **Experiment 2** trains on one market regime (expected price rising) and deploys in the opposite regime (price falling), quantifying the non-stationarity loss. Stdlib only.




This is the whole folder's warning, made numeric.

- **EXP1.** The "obvious" gross-P&L reward yields the policy `[0,1,2,3]` - *sell everything, immediately* - because with impact and holding cost deleted, there is no downside to speed. Evaluated under the true objective it earns $9.00$ against the correct policy's $16.07$: **the wrong reward cost $7.07$, a $44\%$ haircut**, purely from specifying $R$ badly. The agent did exactly what it was told; the specification was the bug.
- **EXP2.** The policy tuned to a *rising* market (`mu=+0.5`) - which sensibly *waits* to sell - loses $0.52$ relative to the oracle when the market *falls* (`mu=-0.5`), because waiting is now wrong. The loss is modest only because this MDP is tiny; the point is categorical: **the optimal policy for one regime is not the optimal policy for another, and the agent has no idea the regime changed.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Reward hacking (A1 fails).** The deepest and most common failure. Gross P&L → over-trading; Sharpe-only reward → the agent exploits the estimation of mean/variance (e.g. huge leverage in a lucky window); "trade count" reward → churn. *Mitigations:* reward net-of-cost P&L with an explicit risk penalty; **penalize turnover directly**; use differential/Sharpe-like objectives (Moody–Saffell) only with care; validate the reward by checking that a *known-good baseline* (e.g. TWAP) scores sensibly under it.
2. **The sim-to-real gap (A2 fails).** The agent exploits simulator artifacts - instant fills at mid, no queue position, a too-benign impact model, zero latency. Bound above by $\frac{\gamma}{(1-\gamma)^2}\|P^\star-P_{\text{sim}}\|$, so it is *worst exactly where RL is most attractive* (long-horizon execution). *Mitigations:* conservative impact models, **validating the simulator's own P&L against real fills**, and preferring short-horizon, tightly-constrained problems where simulator error cannot compound.
3. **Non-stationarity (A3 fails).** Impact, volatility, and flow regimes shift; a learned policy is a claim about a data-generating process whose guarantees expire (EXP2). *Mitigations:* regime-conditional policies ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|HMM & GMM]] for state inference), online/meta-learning, short replay windows, conservative trust regions (PPO), and constant monitoring with automated de-risking.
4. **Sample inefficiency (A4 fails).** Deep RL needs $10^5$–$10^7$ resettable episodes; markets deliver *one* history. Training in a simulator imports A2; training on history overfits. *Mitigation:* don't use RL where a closed-form or DP solution exists - for linear-impact execution it does ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren–Chriss]]), so RL must *beat* that baseline to justify itself.
5. **Backtest overfitting of the policy.** An RL agent with a large state/action space is the most flexible model in the toolbox and will memorize noise. Apply purged/embargoed CV and the deflated Sharpe ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|Pitfalls · 05]]) to the *policy's* out-of-sample equity curve, not just a supervised model's predictions.
6. **Reproducibility & evaluation noise.** Deep-RL results are notoriously seed-sensitive (Henderson et al. 2018); a single lucky seed can look like alpha. Report distributions over seeds, and never compare a single run against a baseline.
7. **Live-state mismatch.** In production the agent's observed state differs from training (latency, partial fills, dropped packets), and it reacts to those differences - a closed-loop failure with no supervised analogue. Guard with a deterministic fallback (e.g. revert to TWAP if the policy's actions deviate past a bound).

---

### 5. Canonical Literature & Study References

- **Sutton & Barto**, *Reinforcement Learning: An Introduction* (2nd ed., 2018) - Ch 11 (function approximation, off-policy divergence), Ch 17 (frontiers, including the reward-design problem). *The reward-specification caution is theirs.*
- **Henderson, Peter et al.**: "Deep Reinforcement Learning that Matters" (AAAI 2018) - the reproducibility/seed-variance reality check every trading-RL claim should answer to.
- **Moody, John & Saffell, Matthew**: "Learning to Trade via Direct Reinforcement" (*IEEE TNN* 12(4), 2001) - the differential-Sharpe objective; useful, and a textbook example of a *gameable* reward.
- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (2018) - Ch 11 (dangers of backtesting), Ch 14 (Deflated Sharpe) - the hygiene this page insists on.
- **Nevmyvaka, Feng & Kearns** (ICML 2006) - read for how *carefully* an honest execution-RL study scopes its claims (and for the caveats in [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06]]).
- **Hasselt, van; Guez & Silver**: "Deep RL with Double Q-learning" (AAAI 2016) - the overestimation bias fix relevant to over-trading.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/04-policy-gradient-and-actor-critic|04 · Policy-Gradient & Actor-Critic]] · [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/06-advanced-extensions|06 · Advanced Extensions (Execution RL)]]
- Hygiene cousins: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|Financial ML Pitfalls · 05 · Failure Modes]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]
- Non-stationarity: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/04-non-stationarity-and-samples|Non-Stationarity & Samples]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]]
- Execution baseline to beat: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]

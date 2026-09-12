---
title: "5.7.5 Failure Modes & Practice"
tags:
  - pillar-portfolio-optimization
  - kelly-criterion
  - bet-sizing
  - estimation-error
  - fat-tails
  - fractional-kelly
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04 · Fractional Kelly & Ruin]] and [[foundations/statistics-and-inference/index|Statistics & Inference]].

---

### 1. Intuition & Practical Objective

Every Kelly formula in the earlier pages takes $p,m,s$ as **known**. In real trading they are estimated from finite, noisy data - and the pivot of the whole folder is that **$f^*$ is maximally sensitive to exactly the parameters that are hardest to estimate**. The objective of this page is to make the failure modes concrete and to hand you the professional de-rating playbook.

Four failure modes dominate:

1. **Parameter-estimation error → overbetting.** If your estimated edge is too optimistic (a $+1\sigma$ draw on $p$) your "$f^*$" is an overbet, and an overbet of $2\times$ is already at the critical fraction - a turned-negative growth rate and near-certain ruin despite a real edge.
2. **Fat tails.** $g\approx f\mu-\tfrac12\sigma^2f^2$ understates how bad the bad state is. A heavy loss-tail makes the exact log-optimal $f^*$ *smaller* than the Gaussian approximation, so sizing on the Gaussian number overbets.
3. **Non-ergodicity / finite horizon.** Kelly's dominance is a long-run, almost-sure result; a single path with a finite horizon and a big early drawdown can kill a strategy that is asymptotically optimal.
4. **Drawdown / leverage interaction.** In the continuous levered case, overbetting near $f_c$ meets margin calls at exactly the worst moment - the drawdown and funding failures compound.

> **Takeaway.** The single most important practitioner law in the whole folder: **if you are not sure about your parameters, you must not bet full Kelly.** De-rate to half Kelly as a default and further on parameter uncertainty - because overbetting is punished asymmetrically harder than underbetting, being wrong about $f^*$ in the *upward* direction is far more dangerous than being wrong downward.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Estimation error: the overbet threshold

With a true win probability $p_{\text{true}}$ and an estimate $\hat p$ from $n$ trials, $\text{SD}(\hat p)=\sqrt{p_{\text{true}}(1-p_{\text{true}})/n}$. If you bet full Kelly on $\hat p$ while the truth is $p_{\text{true}}$, your deployed fraction is $f=2\hat p-1$. The *true* growth rate at that $f$ is

$$
g_{\text{true}}(f)=p_{\text{true}}\ln(1+f)+(1-p_{\text{true}})\ln(1-f).
$$

If $\hat p>p_{\text{true}}$ pushes $f$ above the true critical $f_c^{\text{true}}$, $g_{\text{true}}(f)<0$ and the strategy turns into a **guaranteed-loss machine** - the estimate flipped the sign of the realised growth rate.

Concretely (below): truth $p=0.52$, $\hat p=0.57$ (a $+1\sigma$ estimate from $n=100$), so you bet $f=0.14$; true Kelly is $0.04$ and the true $g(0.14)=-0.0043<0$. **A 3.5× overbet.** The realised outcome: median wealth collapses to ~0 and ~73% of accounts are under 1% of starting capital in 2,000 bets.

#### 2.2 Fat tails understate the true ruin

The Gaussian/continuous approximation $g\approx f\mu-\tfrac12\sigma^2f^2$ is exact only for log-normal returns. A heavy-loss tail (jump risk) contributes large negative log-returns that the second-order expansion misses. The exact log-optimal $f^*=\arg\max_f\sum_i p_i\ln(1+f\,r_i)$ is then *smaller* than the Gaussian $\mu/\sigma^2$ estimate, so a Gaussian-sized bet is an overbet in tail reality. Worked below: exact $f^*=0.581$ vs Gaussian $f^*_{\text{gauss}}=0.766$, and the Gaussian bet materially raises the ruin probability.

---

### 3. Computational Implementation - demonstrated failure modes

Stdlib only. (a) Estimation error flipping a positive edge into ruin; (b) heavy-tail log-optimal vs Gaussian sizing.




The two blocks are the folder's two most important "do not do this" results. **(a)** A single-standard-deviation optimism about $p$ turns your *positive-edge* strategy into one that loses 99.995% of capital with **72.8%** probability of ending below 1% - while the correctly-sized true-Kelly bet grows a bankroll $4.9\times$ with zero such ruin. **(b)** Even with an exact mean and variance, the Gaussian Kelly $f^*=0.766$ is 32% larger than the true log-optimal $f^*=0.581$ because it ignores the $-60\%$ tail; sizing on the Gaussian number is a silent overbet (an overbet of ~32%, which steepens the ruin curve sharply).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Overbetting is asymmetric in danger.** An underbet costs a little growth; an overbet past $f_c$ flips the sign of the growth rate. If you must err, err *down* - hence half Kelly as the operating default. This is the single sentence to carry out of this folder.
2. **Gaussian variance is not SD of log growth under jumps.** Fat tails mean the true drag exceeds $\tfrac12\sigma^2$; jump risk is invisible to a second-order expansion. Estimate the exact $\mathbb{E}[\ln(1+fR)]$ over the empirical/parametric heavy-tailed distribution, not a normal approximation.
3. **Backtest optimism.** $p,m,s$ measured in-sample over a regime shift are systematically optimistic; the "edge" a backtest reports is a biased input to $f^*$. Fractional Kelly here is model-risk management, not timidity.
4. **Leverage × drawdown × margin.** In the continuous case an overbet near $f_c$ produces drawdowns that trigger margin calls at the trough; the forced de-lever locks in ruin. De-risking must happen *pre* drawdown, which fractional Kelly does by construction.

---

### 5. Canonical Literature & Study References

- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §7.3 - the case for fractional Kelly under parameter uncertainty. *Corpus-verified.*
- **MacLean, Thorp & Ziemba (eds.)**: *The Kelly Capital Growth Investment Criterion* (2011) - the "good and bad properties" survey, incl. estimation errors and fractional Kelly.
- **MacLean, Ziemba & Blazenko**: *Growth versus Security in Dynamic Investment Analysis*, Management Science (1992) - the growth/security frontier that motivates de-rating.
- **Chopra & Ziemba**: *The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice* (JPM 1993) - errors in means dominate, the same estimation-error lesson in the MPT sibling folder.
- **Bouchaud & Potters**: *Theory of Financial Risk and Derivative Pricing* - fat tails and why normal approximations misprice extreme risk.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/04-fractional-kelly-and-ruin|04 · Fractional Kelly & Ruin]] · [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Index Hub]]
- Estimation-error sibling: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · MPT Failure Modes]]
- Fat tails: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[foundations/ergodicity-and-statistical-mechanics/06-advanced-extensions|06 · Advanced Extensions (foundations)]]
- Continue: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/06-advanced-extensions|06 · Advanced Extensions]]
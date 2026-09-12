---
title: "2.4.3 Fill-Probability Models"
tags:
  - pillar-algorithmic-hft
  - fill-probability
  - survival-analysis
  - limit-order-execution
  - hazard-rate
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/02-the-order-queue|02 · The Order Queue]].

---

### 1. Intuition & Practical Objective

Page 02 gave the mechanics; this page turns them into **estimable models of fill probability**. The practical objective: given a queue position $x$, a flow rate, and a cancellations process, produce two numbers a trading system can act on - **(i) $\mathbb{P}(\text{fill by }T)$** and **(ii) the expected time to fill**. Along the way we connect the queue view to the **survival/hazard** view of the empirical literature (Lo–MacKinlay–Zhang 2002): a limit order "lives" until it fills or is cancelled, and its hazard is a function of the book state.

The organising idea: **fill probability is a first-passage probability.** In the pure-trade model the time to fill is negative-binomial; add cancellations and it speeds up in proportion to how far back you are; let the flow rate depend on the state and you have a queue-reactive model (page 04).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Pure-trade fill probability (negative-binomial)

Trades are a Poisson process of rate $\mu$. Discretise to ticks where a trade unit arrives with probability $p$. The time to fill $x$ units is

$$
\tau_x = \text{time to accumulate } x \text{ successes} \sim \text{NegBin}(x,p),\qquad
\mathbb{P}(\tau_x = k)=\binom{k-1}{x-1}p^{x}(1-p)^{k-x},
$$

$$
\mathbb{E}[\tau_x] = \frac{x}{p}=\frac{x}{\mu},\qquad \mathrm{Var}[\tau_x]=\frac{x(1-p)}{p^{2}}.
$$

Hence the **fill-probability curve** over a horizon $T$:

$$
\boxed{\;\mathbb{P}(\tau_x \le T)=\mathbb{P}\big(\text{Bin}(T,p)\ge x\big)=I_p(x,\,T-x+1)\;}
$$

where $I_p$ is the regularised incomplete beta function. Two features matter: it is **steep in $x$** (position dominates), and the **relative dispersion** $\mathrm{sd}/\mathrm{mean}=\sqrt{(1-p)/x}$ *shrinks* with $x$ - deep orders have timely fills that are comparatively predictable, front orders have noisy waits.

#### 2.2 Adding cancellations (uniform)

Let cancels arrive with probability $pc$ per tick and remove a uniformly random live order from total depth $Q$. A cancel is ahead of you with probability $x/Q$, so the **effective per-tick outflow coefficient** is

$$
\text{outflow rate} = p + pc\cdot\frac{x}{Q}.
$$

When $x$ is large (deep in the queue) $\frac{x}{Q}\to1$ and cancels help maximally; when you are near the front ($x\ll Q$) cancels barely help. This *position-dependent cancel benefit* is the tractable signature of the real phenomenon.

#### 2.3 The Cont–Kukanov fill function (random outflow)

The general statement (Cont & Kukanov 2017): for queue position $x$ ahead, order size $L$, and random outflow $\xi$ with distribution $F$,

$$
\boxed{\;\mathbb{E}[\text{filled}] = \int \Big[(\xi-Q)^+ - (\xi-Q-L)^+\Big]\,dF(\xi)\;}
$$

The **fill ratio** $\mathbb{E}[\text{filled}]/L$ is the quantity a placement algorithm maximises subject to adverse-selection and fee costs. This is what we compute on page 06.

#### 2.4 The survival / hazard view (Lo–MacKinlay–Zhang)

Write $\tau$ = time from submission to execution-or-cancel. The **hazard** $\lambda(t)=\lim_{dt\to0}\frac{\mathbb{P}(t<\tau\le t+dt\mid\tau>t)}{dt}$ is the instantaneous execution rate given the order is still alive. Lo–MacKinlay–Zhang (2002) estimate $\lambda(t)$ as a function of covariates (distance from the quote, spread, volatility, time of day) and find execution hazards that **decay** with survival time - an order still unfilled after a long spell is trading "against" the flow and is more likely to be cancelled than executed. The queue model *predicts* this: long survival with a large $x$ means either the flow died or the position is stuck, both of which raise the cancel-to-fill ratio.

---

### 3. Computational Implementation - closed form vs Monte Carlo

Stdlib only. Model A computes the negative-binomial fill probability by exact binomial summation and checks it against direct simulation. Model B adds uniform cancellations and shows how much they lift the fill probability.




The closed form and simulation agree to $<0.003$ across the grid - the negative-binomial law is exactly the FIFO fill-time law. Then Model B shows how **cancellations dominate**: at position 25 in a 200-lot queue, raising the cancel rate from $0$ to $0.10$ takes the fill probability from $0.009$ to $0.899$ - a hundredfold change driven entirely by the *front of the queue disappearing*, not by any trade of your own. This is precisely why fill models that ignore cancels are wrong in the most expensive direction: the cancels that help your fill are the ones that flee when the market turns, i.e. the ones that *precede adverse moves*.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ignoring cancellations.** A trade-only fill model understates fill probability in *normal* conditions and massively overstates it in stressed conditions (when cancels vanish). Both directions are costly.
2. **Point estimates without dispersion.** $\mathbb{P}(\text{fill})$ alone hides the variance. The variance of the wait drives inventory risk; a fill model that reports a mean but not a distribution cannot size a position safely.
3. **Calibrating $p$ on aggregate trade rate.** Your fill rate is governed by the trade rate *at your price level*, not the stock's average. Level-specific flow is the right input; using consolidated volume mis-times fills.
4. **Stationary flow assumption.** Real arrival rates are time-varying and autocorrelated (clustering). A single $p$ mis-prices fills across the day - the gateway to the state-dependent intensities of page 04.

---

### 5. Canonical Literature & Study References

- **Lo, MacKinlay & Zhang** (2002), *J. Financial Economics* 65(1), 31–71 - the econometric survival/hazard model of limit-order execution; the empirical counterpart to the queue-model fill probability.
- **Cont, Kukanov & Stoikov** (2014), *J. Financial Markets* 17 - the order-flow-imbalance price-impact law and the empirical queue accounting behind the fill function.
- **Cont & Kukanov** (2017), §2 - the fill function $(\xi-Q)^+-(\xi-Q-L)^+$ and its use in placement optimisation.
- **Gould et al.** (2013), §5 - empirical execution and cancellation frequencies, and the hazard/conditional-frequency evidence.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/02-the-order-queue|02 · The Order Queue]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/04-queue-reactive-models|04 · Queue-Reactive Models]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/01-from-zero-intuition|01 · From Zero]]

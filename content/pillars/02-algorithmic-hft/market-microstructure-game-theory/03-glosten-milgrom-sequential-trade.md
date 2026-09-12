---
title: "2.10.3 Glosten–Milgrom"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - glosten-milgrom
  - adverse-selection
  - bayesian-updating
  - martingale
  - sequential-trade
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]] and [[foundations/bayesian-statistics/index|Bayesian Statistics]] (Bayes' rule, conditional expectation).

---

### 1. Intuition & Practical Objective

The two-point, one-shot model of page 01 is a snapshot. The real game is a **sequence**: trades arrive one at a time, the maker updates her belief after every one of them, and re-quotes. Glosten & Milgrom (1985) showed that this sequential structure - not the size of the trade, not inventory, not hedging - is by itself enough to produce a spread that **behaves like a real one**: it is positive at maximum uncertainty, it narrows as information is revealed, and the price it generates is a martingale.

The essential insight is a change of what "the price" means. There is no single price. There is a **bid** and an **ask**, and each is the expected value of the asset *conditional on the direction of the trade that is about to occur*. The maker is not setting a price she believes; she is setting **two prices, each conditioned on being adversely selected in a known direction.**

Three structural results carry the rest of the folder:

- **The quotes are the maker's own posteriors.** $A=\mathbb{E}[V\mid\text{buy}]$ and $B=\mathbb{E}[V\mid\text{sell}]$ are, mechanically, the two possible Bayesian updates of the current belief. The quote is the update, pre-computed.
- **The price is a martingale.** Because the quotes are conditional expectations, the expected next price equals the current price *exactly* - no drift, no "adverse selection drag" term, nothing.
- **Adverse selection is an equilibrium, not an assumption.** Nobody in the model is *assuming* a spread. The spread is the unique price at which a competitive maker does not lose money to informed flow. If you enter the game with a different spread, you either bleed (too tight) or are picked off by order-flow competition (too wide).

> **The one-sentence essence.** "The maker's bid and ask are her two possible Bayesian posteriors of the asset's value after seeing a sell and after seeing a buy - so the spread is the *change in belief* the two directions imply, and the resulting price process is a martingale by construction."

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** $V\in\{V_L,V_H\}$, prior belief $\theta_t=\mathbb{P}(V=V_H\mid\mathcal F_t)$, informed share $\pi$. Arrivals:
$$
\mathbb{P}(B\mid V_H)=\frac{1+\pi}{2},\qquad \mathbb{P}(B\mid V_L)=\frac{1-\pi}{2},\qquad \mathbb{P}(S\mid\cdot)=1-\mathbb{P}(B\mid\cdot).
$$

**Zero-profit quotes (the equilibrium).** Competition forces expected profit to zero *conditional on the direction of the trade* - a maker cannot cross-subsidise the ask with the bid, because any maker who tried would be picked off on one side. Hence
$$
A_t=\mathbb{E}[V\mid B,\mathcal F_t],\qquad B_t=\mathbb{E}[V\mid S,\mathcal F_t].
$$
Writing $n_A=(1+\pi)\theta_t+(1-\pi)(1-\theta_t)$ and $n_B=(1-\pi)\theta_t+(1+\pi)(1-\theta_t)$ (these are twice the arrival probabilities), Bayes' rule gives

$$
\boxed{\;A_t=\frac{V_H(1+\pi)\theta_t+V_L(1-\pi)(1-\theta_t)}{(1+\pi)\theta_t+(1-\pi)(1-\theta_t)},\qquad B_t=\frac{V_H(1-\pi)\theta_t+V_L(1+\pi)(1-\theta_t)}{(1-\pi)\theta_t+(1+\pi)(1-\theta_t)}\;}
$$

**The belief recursion.** $A_t$ *is* the posterior after a buy, so
$$
\boxed{\;\theta_t^{+}=\frac{\mathbb{P}(B\mid V_H)\,\theta_t}{\mathbb{P}(B\mid V_H)\theta_t+\mathbb{P}(B\mid V_L)(1-\theta_t)}=\frac{(1+\pi)\theta_t}{(1+\pi)\theta_t+(1-\pi)(1-\theta_t)}=\frac{(1+\pi)\theta_t}{n_A}\;}
$$
and symmetrically $\theta_t^{-}=(1-\pi)\theta_t/n_B$. At $\theta=\tfrac12$: $\theta^{+}=(1+\pi)/2$ and $\theta^{-}=(1-\pi)/2$, so the spread at maximum uncertainty is
$$
A-B=\pi(V_H-V_L).
$$

**The martingale property (exact).** Arrival probabilities at the current belief are $\mathbb{P}(B)=\tfrac12 n_A$ and $\mathbb{P}(S)=\tfrac12 n_B$. Therefore, using the expressions above,
$$
\mathbb{E}[P_{t+1}\mid\mathcal{F}_t]=\tfrac12 n_A\cdot\frac{V_H(1+\pi)\theta+V_L(1-\pi)(1-\theta)}{n_A}+\tfrac12 n_B\cdot\frac{V_H(1-\pi)\theta+V_L(1+\pi)(1-\theta)}{n_B}
$$
$$
=\tfrac12\big[V_H\theta\big((1+\pi)+(1-\pi)\big)+V_L(1-\theta)\big((1-\pi)+(1+\pi)\big)\big]=V_H\theta+V_L(1-\theta)=P_t.
$$
**Zero drift, exactly, at every belief.** Verified to machine precision in §3.

**Information eventually gets revealed.** The belief is a bounded martingale, so it converges; the only absorbing points of the recursion are $\theta\in\{0,1\}$. Since informed arrivals always push in the direction of the true value, $\theta_t\to\mathbf 1\{V=V_H\}$ almost surely. **This is the sequential-trade analogue of Kyle's $\Sigma(t)\to0$** and the reason a market "learns".

**Toxicity of a fill.** The probability that a trade you just received came from an informed counterparty is
$$
\mathbb{P}(\text{informed}\mid B)=\frac{\pi\,\theta_t}{\mathbb{P}(B)}=\frac{2\pi\theta_t}{n_A}\qquad\big(\;=\pi\ \text{at }\theta=\tfrac12\;\big).
$$
This is the number a market maker actually cares about, and - crucially - it is **not constant**: it moves with $\theta$, so the value of a fill depends on where in the learning process you are.

---

### 3. Computational Implementation - the sequential Bayesian game, simulated

Stdlib only. First the exact recursion and the martingale check at machine precision; then the dynamics over long paths.




Four readings:

1. **The drift is exactly `0.00e+00`.** Not "small", not "within sampling error" - the martingale property is an algebraic identity of the recursion, and the simulation confirms it numerically to all displayed digits.
2. **$\theta^{+}=0.600000$ from a $0.500000$ prior.** A single buy moves the maker's belief by 10 percentage points at $\pi=0.20$. That belief move *is* the ask: the maker sells at 100.20 because that is her expected value given the buyer showed up.
3. **Learning is fast and asymmetric.** Over 400 independent 300-trade days, the mean terminal belief is $0.999971$ when $V=V_H$ and $0.000434$ when $V=V_L$. The engine does not merely "tend toward" the truth; it is essentially certain by trade 300. This is the sequential-trade engine behind "prices impound information".
4. **Toxicity equals the informed share at maximum uncertainty** ($0.2000$) and moves away from it as the belief departs from $\tfrac12$ - which is exactly the mechanism behind the failure in page 05.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The maker is assumed to price the *average* trade.** Glosten–Milgrom's maker cannot condition on size, venue, or timing. Real makers can and do - which is why the equilibrium spread in practice is a *function of order attributes*, not a scalar. The model is a lower bound on the sophistication of real liquidity provision.
2. **$\pi$ is assumed constant and common knowledge.** Both the informed share and the two-point value structure are equilibrium *inputs*, not outputs. If $\pi$ changes and the maker does not re-estimate, page 05 shows the loss is first-order in the error.
3. **Trade direction must be observable.** The whole recursion depends on labelling each trade buy or sell. With electronic order books the classifier (the Lee–Ready rule, tick tests) is imperfect; classification error feeds directly into the belief recursion and biases $\theta$.
4. **Information is short-lived and single-shot.** The informed trader knows $V$ once and trades, and then the game ends at $\theta\in\{0,1\}$. Real informed flow is *long-lived* - an informed trader may want to trade into several days of arrivals, which changes the equilibrium entirely (Holden–Subrahmanyam 1992; page 06).
5. **The informed trader is assumed to be non-strategic in the GM version.** In Glosten–Milgrom the informed trader trades *every* time in the correct direction - no attempt to disguise or time. Kyle's insider is strategic about *size*; a full game would be strategic about both size and timing across many rounds.
6. **Competition is modelled as the absence of profit, not as entry.** Zero-profit quotes are an assumption about how many makers there are and how fast they can enter. With finite capital the equilibrium can sit above zero-profit indefinitely.

---

### 5. Canonical Literature & Study References

- **Glosten, Lawrence R.; Milgrom, Paul R.** - "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders," *Journal of Financial Economics* 14(1), 71–100 (1985). *Sections 2–3 give the recursion and the zero-profit quotes; §4 discusses the price process and its martingale property.*
- **Easley, David; O'Hara, Maureen** - "Price, trade size, and information in securities markets," *Journal of Financial Economics* 19(1), 69–90 (1987). *Adds trade size to the sequential game - the immediate generalisation of the model above.*
- **Glosten, Lawrence R.** - "Is the electronic open limit order book inevitable?" *Journal of Finance* 49(4), 1127–1161 (1994). *The sequential-trade logic taken to the limit order book, where the "quotes" become the whole schedule.*
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 5 (the Bayesian specialist; the recursion above is his §5.2). *Corpus verification `hasbrouck_ch1-5.md`.*
- **Foucault, Thierry; Pagano, Marco; Röell, Ailsa** - *Market Liquidity: Theory, Evidence, and Policy* (2013), Ch 3. *Corpus verification `foucault_ch1-3.md`; §3.2 has the cleanest statement of the martingale property.*
- **Biais, Bruno; Glosten, Lawrence; Spatt, Chester** - "Market microstructure: A survey of microfoundations, empirical results, and policy implications," *Journal of Financial Markets* 8(2), 217–264 (2005). *Where this model sits in the full taxonomy.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/02-the-kyle-model-and-back-limit|02 - Kyle & the Back Limit]] (the continuous-value counterpart) · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/04-predatory-trading-and-execution-games|04 - Predatory Trading & Execution Games]]
- The game in full detail: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & the Glosten–Milgrom Model]]
- Measuring the inputs: [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] (estimating $\pi$) · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]] (how much of a quoted spread is adverse selection)
- Formal machinery: [[foundations/bayesian-statistics/index|Bayesian Statistics]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (martingale convergence - why $\theta_t\to\mathbf 1\{V=V_H\}$)

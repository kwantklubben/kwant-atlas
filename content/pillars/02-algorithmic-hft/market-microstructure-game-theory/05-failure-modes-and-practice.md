---
title: "2.10.5 Failure Modes and Desk Practice"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - failure-modes
  - adverse-selection
  - model-risk
  - vpin
  - non-stationarity
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-game-theory/04-predatory-trading-and-execution-games|04 - Predatory Trading & Execution Games]].

---

### 1. Intuition & Practical Objective

Every model in this folder is an **equilibrium of a game whose payoffs are assumed to be common knowledge**. That is a much stronger demand than "the parameters are roughly right", and it fails in a characteristically nasty way: when the game's payoffs are mis-specified, the equilibrium you are *playing* is not the equilibrium you *solved*, and the error does not show up as noise - it shows up as a **systematic transfer of money, every trade, in the same direction**.

This page names the failures precisely, gives the first-principles reason for each, and **quantifies the dollar cost** of the two that matter most: mis-specifying the adverse-selection equilibrium, and mis-specifying the informed share that the equilibrium takes as given.

The six failures, one line each:

1. **Adverse selection is estimated, not observed.** The equilibrium spread is linear in $\pi$; a wrong $\pi$ is a *first-order* money error, not a variance term.
2. **The equilibrium spread is state-dependent, and desks quote constants.** $A(\theta)-B(\theta)$ collapses toward zero as the belief sharpens, so a constant spread is wrong on every trade even if it is right on average.
3. **The single informed trader is a fiction.** With $K$ informed participants the revelation rate scales with $K\beta$ and $\lambda$ falls; calibrating a single-insider $\lambda$ over-states impact (page 06).
4. **The game is non-stationary.** $\pi$, $\Sigma_0$, $\sigma_u^2$ and the impact coefficients all move with news, volatility and time of day. A static equilibrium is a snapshot of a moving object.
5. **Toxicity proxies are contested.** PIN and VPIN are the practical surrogates for $\pi$, and the empirical literature does not agree that they measure it (Easley–López de Prado–O'Hara 2012 vs Andersen & Bondarenko 2014).
6. **Predation is real but rarely identified.** The mechanism's signatures are indistinguishable from momentum and news in most data.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The cost of a mis-specified informed share.** The maker's equilibrium quotes are $A(\theta;\hat\pi)$ and $B(\theta;\hat\pi)$ - but the world draws trades with $\pi_{\text{true}}$. The maker's expected profit per trade is
$$
\mathbb{E}[\text{P\&L}\mid \hat\pi,\pi]=\tfrac12 n_A(\theta;\hat\pi)\,\bigl[A(\theta;\hat\pi)-\mathbb{E}[V\mid B;\pi]\bigr]+\tfrac12 n_B(\theta;\hat\pi)\,\bigl[\mathbb{E}[V\mid S;\pi]-B(\theta;\hat\pi)\bigr],
$$
where the expectations on the right use the **true** $\pi$. When $\hat\pi=\pi$ it is identically zero. When $\hat\pi\ne\pi$ it is **not** second-order:
- $\hat\pi<\pi$: quotes too tight. The maker is picked off on the informed flow, and loses at a rate proportional to the shortfall in the spread - the P&L is *strictly negative* and grows linearly with $\pi-\hat\pi$.
- $\hat\pi>\pi$: quotes too wide. The maker earns a positive spread, but on these numbers only a small fraction of the shortfall, because the *conditional* losses to the informed flow are already sunk. In a model with competing makers the wide quotes lose order flow and the profit vanishes.

Crucially, in this game **the loss is not a sampling error that averages out over a day**. It is the same signed amount on every trade until the maker updates $\hat\pi$. This is the practical meaning of "adverse selection is an equilibrium rather than an assumption": get the equilibrium wrong and you are *systematically on the losing side of a transfer*.

**2.2 Why a constant spread cannot be the equilibrium.** With $n_A=(1+\pi)\theta+(1-\pi)(1-\theta)$ and $n_B=(1-\pi)\theta+(1+\pi)(1-\theta)$,
$$
A(\theta)-B(\theta)=\frac{V_H(1+\pi)\theta+V_L(1-\pi)(1-\theta)}{n_A}-\frac{V_H(1-\pi)\theta+V_L(1+\pi)(1-\theta)}{n_B}.
$$
At $\theta=\tfrac12$ this is $\pi(V_H-V_L)$. At the extremes $n_A$ and $n_B$ diverge asymmetrically and the spread **collapses**: as $\theta\to1$ both $n_A\to1+\pi$ and $n_B\to1-\pi$, and the two conditional expectations converge on $V_H$. Numerically (§3): the spread falls from $0.4000$ at $\theta=\tfrac12$ to $0.0785$ at $\theta=0.95$. A desk quoting the *average* spread is quoting too wide when the market is already informed and too tight when it is not - and the too-tight end is where the money is lost.

**2.3 The toxicity of a fill is state-dependent.** We derived
$$
\mathbb{P}(\text{informed}\mid B)=\frac{2\pi\theta}{n_A},\qquad \mathbb{P}(\text{informed}\mid B)\Big|_{\theta=1/2}=\pi.
$$
So the answer to "what was the chance my last fill was informed?" is **not** a constant: it is $0.0909$ at $\theta=0.20$, $0.2000$ at $\theta=0.50$ and $0.2857$ at $\theta=0.80$ for $\pi=0.2$. Any execution logic that treats toxicity as a fixed property of the *name* is mis-specified; toxicity is a property of the *state*.

**2.4 Non-stationarity: everything moves together.** $\Sigma_0$ (prior uncertainty), $\sigma_u^2$ (noise volume) and $\pi$ (the informed share) are correlated in the worst possible direction. On a news day, $\Sigma_0\uparrow$ and $\pi\uparrow$ simultaneously, so $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ *and* the spread $\pi(V_H-V_L)$ both jump - in the direction that makes a yesterday-calibrated model under-charge on both. And $\lambda=\sqrt{\Sigma_0/(\sigma_u^2T)}$ in continuous time depends on the *horizon*, so the same flow implies different impact at different measurement horizons. A single $\lambda$ is a statement about a (name, regime, horizon) triple.

**2.5 Estimation: PIN, VPIN and the identification problem.** The practical surrogates for $\pi$ are:
- **PIN** (Easley–Kiefer–O'Hara–Paperman 1996): a three-parameter mixture ($\alpha$ = information-event probability, $\mu$ = informed arrival rate, $\varepsilon$ = noise arrival rate) estimated by maximum likelihood, giving $\text{PIN}=\alpha\mu/(\alpha\mu+2\varepsilon)$. This *is* an equilibrium-based estimator, but its identification rests on the assumption that information events occur once per day and that buy/sell classification is correct.
- **VPIN** (Easley–López de Prado–O'Hara 2012): the volume-bucketed order-imbalance $\mathbb{E}[|V_B-V_S|]/V$. Cheap, high-frequency, and **contested** - Andersen & Bondarenko (2014) show it has almost no power to predict toxicity and that its "flash crash" evidence is a construction artefact.

The lesson is not "use a better proxy". It is that **the $\pi$ the equilibrium needs is a latent payoff-relevant object, and every observable surrogate for it is a noisy, contested statistic.** The discipline is to treat the spread as a *range* and to re-estimate $\pi$ continuously, not to fix it.

---

### 3. Computational Implementation - the cost of getting the game wrong

Stdlib only. Part 1 tabulates the equilibrium spread against the maker's belief for three different assumed $\pi$; Part 2 simulates the maker's P&L per trade over many days when it assumes $\hat\pi$ but the world runs at $\pi_{\text{true}}=0.2$; Part 3 shows the toxicity of a fill is state-dependent.




What this measures:

1. **The equilibrium is correct exactly where it should be.** At $\hat\pi=\pi_{\text{true}}=0.2$ the maker's P&L per trade is $+ $\$0.00029 - zero to within Monte-Carlo noise on 480,000 trades. That is the validation of the whole framework: get the game right and the maker breaks even.
2. **Getting it wrong is a first-order, signed cost.** Quoting as if there were **no** informed flow ($\hat\pi=0$) costs the maker **$-$ \$0.19816 per trade, on 100% of trades**. At a modest 10,000 shares/day that is -\$1,982/day, or roughly -$$$$\$0.5m/year - from a single scalar mis-estimate, with no variance reduction available.
3. **The asymmetry is brutal and worth internalising.** Under-estimating $\pi$ (too-tight quotes) costs $-0.198$. Over-estimating it ($\hat\pi=0.5$) "earns" only $+0.023$ - a *tenth* of the magnitude, and that is before accounting for the order flow a wide quoter loses. The payoff to a maker is **convex in the wrong direction**: being too tight is punished far harder than being too wide is rewarded.
4. **The spread is a state-dependent object.** The true equilibrium spread runs $0.4000$ at $\theta=0.5$ down to $0.0785$ at $\theta=0.95$, i.e. it falls by a factor of **5** as the belief sharpens. The two mis-specified columns show the cost of a constant-spread assumption: quoting the $\hat\pi=0.5$ spread at $\theta=0.95$ ($1.0000$) is more than **12x** the true equilibrium ($0.0785$).
5. **Toxicity moves with the state, not with the name.** $0.0909\to0.2000\to0.2857$ as $\theta$ moves from $0.20$ to $0.80$, at a *fixed* $\pi=0.2$. Any flow-toxicity metric that is a property of the instrument rather than of the current belief is measuring the wrong thing.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Equilibrium mis-specification is a transfer, not a variance.** Cost: $-$ \$0.198/trade for \hat\pi=0$ against $\pi_{\text{true}}=0.2$; zero at $\hat\pi=\pi_{\text{true}}$. First-principles cause: the spread is *linear* in $\pi$, so the error is *linear* in the error of $\pi$ - there is no second-order protection anywhere in this game.
2. **The state-dependence of the equilibrium is ignored in practice.** Spreads collapse by 5x as beliefs sharpen, and toxicity moves by 3x. First-principles cause: the equilibrium quotes are conditional expectations, and conditionals are functions of the belief, not constants. Fix: quote off your belief, and re-estimate the belief continuously.
3. **Single-insider calibration over-states impact.** With $K$ informed traders the information is impounded at rate $K\beta$: $\Sigma'=\Sigma_0\sigma_u^2/((K\beta)^2\Sigma_0+\sigma_u^2)$ falls to $50\%$, $80\%$, $90\%$, $96\%$ of the prior for $K=1,2,3,5$ (page 06). A $\lambda$ fitted assuming one insider is too large for a market with many. First-principles cause: competition among the informed *accelerates* revelation, which *deepens* the market.
4. **Non-stationarity has a signature direction.** On stress days $\Sigma_0$ and $\pi$ rise together, so both $\lambda$ and the spread increase - exactly when you most need your model to be right. First-principles cause: liquidity provision withdraws under uncertainty (the same adverse-selection logic as [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]). Fix: state-dependent parameters, re-solved intraday.
5. **Toxicity proxies are contested and fragile.** PIN requires an MLE with an unobservable information-event structure; VPIN is cheap but Andersen & Bondarenko (2014) find it has negligible predictive power and that its flash-crash evidence is constructed. First-principles cause: these are *proxies* for a latent equilibrium object; the map from data to $\pi$ is not invertible without strong assumptions.
6. **Predation and momentum are observationally close.** Both produce elevated volume and a directional price move in stressed names. First-principles cause: the models differ in *who knows what*, which is unobserved; identifying predation requires an instrument for the victim's forced-ness that data rarely provides.
7. **Zero-profit quotes assume free entry of liquidity providers.** With finite maker capital the equilibrium spread sits above zero-profit, and the "fair" spread computed here becomes a *lower bound* rather than the market's spread. Confusing the two under-estimates the cost of provision.
8. **The models are silent on venue.** All of the machinery above is single-venue. Fragmentation, dark venues, and fee structures change the equilibrium by changing what a maker can condition on (see [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation|Smart Order Routing & Fragmentation]]).

---

### 5. References

- **Easley, David; Kiefer, Nicholas M.; O'Hara, Maureen; Paperman, Joseph B.** - "Liquidity, information, and infrequently traded stocks," *Journal of Finance* 51(4), 1405–1436 (1996). *PIN: the MLE estimator of the informed share the games take as given.*
- **Easley, David; López de Prado, Marcos; O'Hara, Maureen** - "Flow toxicity and liquidity in a high-frequency world," *Review of Financial Studies* 25(5), 1457–1493 (2012). *VPIN.*
- **Andersen, Torben G.; Bondarenko, Oleg** - "VPIN and the flash crash," *Journal of Financial Markets* 17, 1–46 (2014). *The critique: VPIN's predictive power and its flash-crash evidence both fail under scrutiny. Read it before using any toxicity number.*
- **Glosten, Lawrence R.; Harris, Lawrence E.** - "Estimating the components of the bid/ask spread," *Journal of Financial Economics* 21(1), 123–142 (1988). *How to decompose a *measured* spread into adverse-selection and other components
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007)
- **Almgren, Robert; Chriss, Neil** - "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000)
- **Brunnermeier, Markus K.; Pedersen, Lasse Heje** - "Predatory trading," *Journal of Finance* 60(4), 1825–1863 (2005). *The theory that is hardest to identify empirically.*
- **Andersen, Torben G.; Bondarenko, Oleg**

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/04-predatory-trading-and-execution-games|04 - Predatory Trading & Execution Games]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/03-glosten-milgrom-sequential-trade|03 - Glosten–Milgrom]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/06-advanced-extensions|06 - Advanced Extensions]]
- Measurement of the inputs: [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]
- Model risk discipline: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]
- The non-strategic failure list, for comparison: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|Almgren–Chriss: Failure Modes & Practice]]

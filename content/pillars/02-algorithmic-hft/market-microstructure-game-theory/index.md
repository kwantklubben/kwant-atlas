---
title: "2.10 Market Microstructure Game Theory"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - game-theory
  - kyle-1985
  - glosten-milgrom
  - adverse-selection
  - predatory-trading
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayesian updating, conditional expectation) and [[foundations/bayesian-statistics/index|Bayesian Statistics]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A price is not a fact. It is the **outcome of a game** played every microsecond between three parties who want different things:

- an **informed trader** (or several) who knows something about the fundamental value and wants to trade on it without revealing it;
- **noise/liquidity traders** who trade for exogenous reasons and whose flow is the informed trader's camouflage;
- a **market maker** (or a competitive crowd of them) who must quote prices *without* knowing which counterparty it is facing, and therefore quotes **conditionally** - the ask is the expected value *given that someone chose to buy from you*, and the bid is the expected value *given that someone chose to sell*.

Every classical microstructure model is a specialization of that game. **Kyle (1985)** makes it a batch auction with a strategic insider and a linear price rule. **Glosten–Milgrom (1985)** makes it a sequential-trade Bayesian game with a competitive specialist and a two-point value. **Brunnermeier–Pedersen (2005)** adds a fourth player - a predator who trades *against* a forced liquidator. **Schied–Zhang (2019)** replaces the single insider with many strategic liquidators and asks what the Nash equilibrium of the execution game looks like.

The practical objective of this folder is exactly what a practitioner needs from that literature: **when you trade, who is on the other side, what do they know, and what does the equilibrium price of that interaction look like?** Adverse selection is not a parameter you sprinkle on top of a model - it *is* the equilibrium spread; impact is not a cost function you fit - it *is* Kyle's λ; and your own optimal execution is not a private optimization problem - it is **one player's best response** in a game.

This folder is the **game-theoretic microstructure** topic-folder for Pillar 2. As a *hub*, it gives you **(a)** the fast formula lookup below and **(b)** six sub-pages that walk from zero-knowledge intuition, through Kyle and the Back continuous-time limit, through Glosten–Milgrom as a Bayesian game, into predatory trading and execution games, then the failure modes and the modern extensions.

> **The one-sentence essence.** "The spread is a Bayesian equilibrium price of adverse selection, impact is Kyle's $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$, and your execution schedule is only optimal *given* the schedule everyone else is running - it is a Nash object, not a private one."

**Scope note (vs the sibling folders).** This folder is the **strategic/equilibrium** view - who knows what, who moves when, and what the equilibrium of that interaction is. For the *scheduling* of a given order under a fixed impact model, see [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]. For the *measurement* of impact and depth, see [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]. For the sequential-Bayesian market-making view in depth, see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & the Glosten–Milgrom Model]]. The two meet at the same λ: this folder asks *why the equilibrium has that λ*, the others ask *how to measure it* and *what to do with it*.

*Primary verified sources:* Kyle (1985); Glosten & Milgrom (1985); Back (1992); Holden & Subrahmanyam (1992); Brunnermeier & Pedersen (2005); Carlin, Lobo & Viswanathan (2007); Schied & Zhang (2019); Schied, Strehle & Zhang (2018); Cordoni & Lillo (2022); Cardaliaguet & Lehalle (2018); Huberman & Stanzl (2004); Hasbrouck, *Empirical Market Microstructure* (Ch 5–7, corpus verification reports `hasbrouck_ch1-5.md` / `hasbrouck_ch6-10.md`); Foucault, Pagano & Röell, *Market Liquidity* (Ch 3, corpus `foucault_ch1-3.md`). Every number below was **re-executed and reproduced in pure-stdlib Python** (see §3).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $v$ = fundamental value; $\Sigma_0=\operatorname{Var}[v]$ = prior value variance; $u$ = noise order flow, $\sigma_u^2=\operatorname{Var}[u]$; $x$ = informed demand; $y=x+u$ = total signed order flow; $P$ = price; $\lambda$ = price impact (\"Kyle's lambda\"); $1/\lambda$ = market depth. For the Glosten–Milgrom game: $V\in\{V_L,V_H\}$, belief $\theta_t=\mathbb{P}(V=V_H\mid\mathcal{F}_t)$, $\pi$ = share of traders who are informed. For execution games: $X$ = block to liquidate, $T$ = horizon, $N$ = number of intervals of length $\tau=T/N$, $n_k$ = shares traded in interval $k$, $x_k$ = shares still held, $\eta$ = temporary-impact coefficient, $\gamma$ = permanent-impact coefficient, $\lambda_{\text{risk}}$ = risk aversion.

**2.1 The Glosten–Milgrom game (1985).** Arrivals of buy/sell orders are governed by
$$
\mathbb{P}(B\mid V_H)=\tfrac{1+\pi}{2},\qquad \mathbb{P}(B\mid V_L)=\tfrac{1-\pi}{2},\qquad \mathbb{P}(S\mid\cdot)=1-\mathbb{P}(B\mid\cdot).
$$
A competitive maker quotes **zero expected profit conditional on the direction of the trade**:
$$
A_t=\mathbb{E}[V\mid \text{buy at }t],\qquad B_t=\mathbb{E}[V\mid \text{sell at }t],
$$
which evaluates to
$$
\boxed{\;A_t=\frac{V_H(1+\pi)\theta_t+V_L(1-\pi)(1-\theta_t)}{(1+\pi)\theta_t+(1-\pi)(1-\theta_t)},\qquad B_t=\frac{V_H(1-\pi)\theta_t+V_L(1+\pi)(1-\theta_t)}{(1-\pi)\theta_t+(1+\pi)(1-\theta_t)}\;}
$$
and the Bayesian update after a buy is $\theta_t^{+}=\dfrac{(1+\pi)\theta_t}{(1+\pi)\theta_t+(1-\pi)(1-\theta_t)}$. At $\theta=\tfrac12$ everything collapses to the textbook form
$$
A-B=\pi\,(V_H-V_L).
$$
**Key structural fact:** the quoted price is a **martingale** - $\mathbb{E}[P_{t+1}\mid\mathcal{F}_t]=P_t$ - exactly because $A$ and $B$ are conditional expectations. Verified to $0.00\times10^{0}$ drift in §3.

**2.2 The Kyle (1985) auction.** Prior $v\sim\mathcal N(p_0,\Sigma_0)$, noise $u\sim\mathcal N(0,\sigma_u^2)$, one strategic insider, competitive linear pricing $P=p_0+\lambda y$. The equilibrium is
$$
\boxed{\;x=\beta\,(v-p_0),\quad \beta=\sqrt{\sigma_u^2/\Sigma_0},\qquad \lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2},\qquad 1/\lambda=2\sqrt{\sigma_u^2/\Sigma_0}\;}
$$
with $\operatorname{Var}[v\mid P]=\Sigma_0/2$ (**exactly half the private information is impounded**, and the fraction is invariant to $\sigma_u^2$) and $\mathbb{E}[\text{insider profit}]=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$.

**2.3 N-auction Kyle (the discrete game).** Repeat the auction $N$ times with equal noise variance $\sigma_u^2$ per round and prior variance $\Sigma_{n-1}$. The equilibrium is
$$
\boxed{\;\Sigma_n=\tfrac12\Sigma_{n-1}=\Sigma_0\,2^{-n},\qquad \beta_n=\sqrt{\sigma_u^2/\Sigma_{n-1}},\qquad \lambda_n=\tfrac12\sqrt{\Sigma_{n-1}/\sigma_u^2},\qquad \mathbb{E}[\text{profit}_n]=\tfrac12\sqrt{\sigma_u^2\Sigma_{n-1}}\;}
$$
so information is released **geometrically** (half per auction) and the insider's total expected profit converges:
$$
\sum_{n\ge1}\tfrac12\sqrt{\sigma_u^2\Sigma_0}\,2^{-(n-1)/2}=\frac{2+\sqrt2}{2}\sqrt{\sigma_u^2\Sigma_0}.
$$
$N=12$ reproduces this limit to $1.6\%$ (§3).

**2.4 The Kyle–Back continuous-time limit.** You **cannot** get continuous time by simply sending $N\to\infty$ in §2.3 with a fixed total noise budget: with per-period noise variance $\sigma_u^2\tau$ the first-period impact is $\lambda_1=\tfrac12\sqrt{\Sigma_0/(\sigma_u^2\tau)}\to\infty$. The correct continuous-time equilibrium - Kyle (1985, §2) resolved by **Back (1992)** - has a **linear** information release and a **constant** impact coefficient:
$$
\boxed{\;\Sigma(t)=\Sigma_0\Bigl(1-\frac{t}{T}\Bigr),\qquad \lambda=\sqrt{\frac{\Sigma_0}{\sigma_u^2 T}}\;}
$$
with $P_t=p_0+\lambda(X_t+U_t)$, $dU_t=\sigma_u\,dB_t$, and market depth $1/\lambda=\sigma_u\sqrt{T/\Sigma_0}$. **Why the form is forced:** the filtering identity $d\Sigma_t=-\operatorname{Var}(dP_t\mid\mathcal F_{t^-})=-\lambda^2\sigma_u^2\,dt$ combined with $\Sigma(t)=\Sigma_0(1-t/T)$ gives $\lambda^2\sigma_u^2T=\Sigma_0$ identically - and $\int_0^T\lambda^2\sigma_u^2dt=\Sigma_0$ says *all* the information is released by $T$. Two corollaries: half the information is impounded at $t=T/2$ (the continuous analogue of the auction's $\Sigma_0/2$), and $\lambda\propto T^{-1/2}$ (**a longer horizon makes the market deeper**, not shallower).

**2.5 Predatory trading (Brunnermeier–Pedersen 2005).** A distressed trader must liquidate $X$ on a schedule $\{n_k\}$; a predator best-responds to *that public schedule*. With price $P_k=P_0-\kappa\sum_{j\le k}(n_j+m_j)$ (sign convention: selling depresses) and linear temporary cost $\eta$ per unit for everyone, the predator's cash flow is
$$
\Pi=\sum_k m_k\bigl(P_{k-1}-\eta m_k\bigr),\qquad \sum_k m_k=0,
$$
which reduces to a concave quadratic. Its maximiser is
$$
\boxed{\;m_k=\frac{\kappa\,(\bar A-A_k)}{2\eta-\kappa},\qquad A_k=\sum_{j<k}n_j,\quad \bar A=\tfrac1N\textstyle\sum_k A_k\;}
$$
with the interior-solution condition $\eta>\kappa/2$. Since $A_k$ is increasing, $m_k$ is **positive early and negative late**: the predator **sells ahead of the victim and buys back afterwards**, collecting the permanent-impact rent it helped create.

**2.6 Execution as a game (Schied–Zhang 2019).** When $J$ strategic liquidators trade the same asset, each minimises its own cost holding the others fixed. In the linear-quadratic case the symmetric Nash equilibrium is *the single-agent Almgren–Chriss solution with an inflated temporary-impact coefficient*: sharing one liquidity pool with a counterpart who trades $n^j_k$ makes agent $i$'s marginal temporary cost $\eta(2n^i_k+n^j_k)$, i.e.
$$
\boxed{\;\eta_{\text{eff}}=\tfrac{3}{2}\eta\quad\text{(two symmetric players)}\;\Longrightarrow\;\kappa_{\text{eff}}=\sqrt{\lambda_{\text{risk}}\sigma^2/\eta_{\text{eff}}}=\sqrt{\tfrac23}\,\kappa\;}
$$
so **competition for liquidity makes each player slower, not faster** - the opposite of the naive intuition, and the reason "everyone liquidates at once" is expensive. Schied & Zhang (2019) and Cordoni & Lillo (2022) show the same structure in continuous time, where the equilibrium can become **unstable** (oscillating strategies, non-existent high-frequency limit) when the temporary-cost parameter is small relative to cross-impact.

**2.7 Competing informed traders (Holden–Subrahmanyam 1992).** Replace the single insider by $K$ insiders with aggregate informed intensity $K\beta$. One round of Bayesian updating gives
$$
\boxed{\;\Sigma'=\frac{\Sigma_0\sigma_u^2}{(K\beta)^2\Sigma_0+\sigma_u^2},\qquad \lambda_K=\frac{K\beta\,\Sigma_0}{(K\beta)^2\Sigma_0+\sigma_u^2}\;}
$$
$K=1$ recovers $\Sigma_0/2$ and $\lambda$; $K\to\infty$ drives $\Sigma'\to0$ and $\lambda_K\to0$. More insiders $\Rightarrow$ faster revelation $\Rightarrow$ a **deeper** market.

**Quick-Reference Lookup** - the fast facts of this folder (all reproduced by the stdlib engine in §3):

| Quantity | Formula | Verified check |
|---|---|---|
| GM zero-profit spread ($\theta=\tfrac12$) | $A-B=\pi(V_H-V_L)$ | $\pi{=}0.2,V_H{=}101,V_L{=}99\Rightarrow 0.4000$ |
| GM posterior after a buy | $\theta^{+}=\frac{(1+\pi)\theta}{(1+\pi)\theta+(1-\pi)(1-\theta)}$ | $\theta{=}\tfrac12,\pi{=}0.2\Rightarrow\theta^{+}{=}0.600000$ |
| GM price is a martingale | $\mathbb{E}[P_{t+1}\mid\mathcal F_t]=P_t$ | one-step mean $100.000000$, drift $0.00\times10^{0}$ |
| GM toxicity of a fill | $\mathbb{P}(\text{informed}\mid\text{buy})=\frac{2\pi\theta}{(1+\pi)\theta+(1-\pi)(1-\theta)}$ | $\theta{=}\tfrac12\Rightarrow0.2000$ |
| GM spread is state-dependent | $A(\theta)-B(\theta)$ | peaks at $\theta{=}\tfrac12$: $0.4000$; $\theta{=}0.95$: $0.0785$ |
| Kyle insider demand | $x=\beta(v-p_0),\ \beta=\sqrt{\sigma_u^2/\Sigma_0}$ | $\Sigma_0{=}4,\sigma_u^2{=}1\Rightarrow\beta{=}0.5000$ |
| **Kyle's lambda** | $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ | $\Rightarrow\lambda{=}1.0000$, depth $1/\lambda{=}1.0000$ |
| Kyle info impounded | $\operatorname{Var}[v\mid P]=\Sigma_0/2$ | $2.0000$ (exactly half, independent of $\sigma_u^2$) |
| Kyle insider profit | $\mathbb{E}[\pi]=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$ | $1.0000$ |
| Discrete $N$-auction Kyle | $\Sigma_n{=}\Sigma_{n-1}/2,\ \beta_n{=}\sqrt{\sigma_u^2/\Sigma_{n-1}},\ \lambda_n{=}\tfrac12\sqrt{\Sigma_{n-1}/\sigma_u^2}$ | $\lambda_1{=}1.0000,\lambda_2{=}0.7071,\lambda_3{=}0.5000$ |
| Total insider profit ($N\to\infty$) | $\frac{2+\sqrt2}{2}\sqrt{\sigma_u^2\Sigma_0}$ | $N{=}12$ gives $3.3609\to3.4142$ |
| Naive continuum is ill-posed | $\lambda_1=\tfrac12\sqrt{\Sigma_0/(\sigma_u^2\tau)}\to\infty$ | $N{=}10^4\Rightarrow\lambda_1{=}100.000$ |
| **Kyle–Back continuous time** | $\lambda=\sqrt{\Sigma_0/(\sigma_u^2T)},\ \Sigma(t)=\Sigma_0(1-t/T)$ | $T{=}1\Rightarrow\lambda{=}2.0000$; $\lambda^2\sigma_u^2T{=}4.0000{=}\Sigma_0$ |
| Half-information time (continuous) | $t^\star=T/2$ | $\Sigma(T/2){=}2.0000{=}\Sigma_0/2$ |
| Predator's front-run schedule | $m_k=\kappa(\bar A-A_k)/(2\eta-\kappa)$ | $\kappa{=}1,\eta{=}0.6\Rightarrow m_1{=}+2.188,\ m_8{=}-2.188$, $\sum m_k{=}0$ |
| Cost of predation | victim loss / predator profit | loss $3.2812$, predator profit $1.6406$, deadweight $1.6406$ |
| Victim's best response | front-load (speed up) | victim loss $3.2812\to1.7175$ as it front-loads |
| Two-player execution Nash | $\eta_{\text{eff}}=\tfrac32\eta$ | quarters $46.81/26.18/15.70/11.31\%$ = AC with $1.5\eta$ |
| $K$ competing insiders | $\Sigma'=\frac{\Sigma_0\sigma_u^2}{(K\beta)^2\Sigma_0+\sigma_u^2}$ | impounded: $K{=}1{:}50\%$, $K{=}2{:}80\%$, $K{=}5{:}96.15\%$ |
| No-manipulation constraint | $\gamma+\delta\ge1$ (Gatheral/Huberman–Stanzl) | admissibility test on any impact/decay kernel |

---

### 3. Computational Implementation - the game-theory core engine

Stdlib only (`math`, `random`), fully deterministic. It reproduces every verified number in the lookup table above: the GM spread, the GM martingale property, the Kyle auction closed forms, the N-auction recursion and its profit limit, the ill-posedness of the naive continuum, Back's continuous-time information identity, the predator's optimal front-run schedule, the two-player execution Nash, and the $K$-insider information release.




The engine continues with the discrete Kyle recursion, the continuum ill-posedness, the Back information identity, the predator's schedule, the two-player Nash and the $K$-insider release:




One cross-check that matters: the **shared-liquidity Nash equilibrium reproduces the single-agent Almgren–Chriss trajectory with $\eta_{\text{eff}}=1.5\eta$ to five decimal places** in all four quarters, which is precisely the $\eta_{\text{eff}}=\tfrac32\eta$ prediction of §2.6. The solver is therefore solving the game, not a mis-specified QP.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the full analysis lives in [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]]. One line each:

1. **The equilibrium is only as good as the payoff it assumes.** Glosten–Milgrom's spread $\pi(V_H-V_L)$ is *an equilibrium of a game*, not a fact about the world: mis-specify $\pi$ and the maker does not "earn a bit less", it **loses ~0.2 \$/trade with certainty** (verified in §3 of page 05).
2. **The single-insider Kyle model is a fiction.** Real markets have many informed participants; with $K$ insiders the price reveals information at rate $K\beta$ and λ collapses toward zero - calibrating a single-insider λ on a multi-insider market **over-states impact**.
3. **The naive continuous-time limit does not exist.** Discretising Kyle and taking $N\to\infty$ with a fixed noise budget sends λ to infinity; only Back's (1992) linear-release equilibrium is well-defined. Any "high-frequency limit" claim must say which limit.
4. **Strategic equilibria can be unstable.** Schied & Zhang (2019) / Cordoni & Lillo (2022): below a threshold on the temporary-cost parameter the transient-impact execution game has wildly oscillating strategies and no well-behaved high-frequency limit - the equilibrium exists mathematically but is not a description of a market.
5. **Predation is real but not identified by these models.** The predator's schedule depends on the *victim's* schedule being public; in reality schedules are hidden and randomised, and the empirical literature struggles to separate predation from momentum and news.
6. **Adverse selection is estimated, not observed.** Practical proxies (PIN, VPIN) are noisy and contested (Easley–Kiefer–O'Hara–Paperman 1996; Easley–López de Prado–O'Hara 2012; Andersen & Bondarenko 2014), so the "equilibrium" π you plug in is itself a guess.

---

### 5. Canonical Literature & Study References

- **Kyle, Albert S.** - "Continuous auctions and insider trading," *Econometrica* 53(6), 1315–1335 (1985). *The anchor of the whole folder: the strategic insider, the linear price rule, $\lambda$, and the $\Sigma_0/2$ half-information result.*
- **Glosten, Lawrence R.; Milgrom, Paul R.** - "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders," *Journal of Financial Economics* 14(1), 71–100 (1985). *Adverse selection as a sequential Bayesian game; zero-profit quotes are conditional expectations.*
- **Back, Kerry** - "Insider trading in continuous time," *Review of Financial Studies* 5(3), 387–409 (1992). *The correct continuous-time limit: linear information release, constant λ = √(Σ₀/(σ_u²T)), and the founding use of filtering in microstructure.*
- **Holden, Craig W.; Subrahmanyam, Avanidhar** - "Long-lived private information and imperfect competition," *Journal of Finance* 47(1), 247–270 (1992). *Many informed traders ⇒ faster revelation ⇒ deeper market; the antidote to single-insider calibration.*
- **Brunnermeier, Markus K.; Pedersen, Lasse Heje** - "Predatory trading," *Journal of Finance* 60(4), 1825–1863 (2005). *Predators sell alongside a distressed liquidator and buy back later; price overshoot, and illiquidity precisely when liquidity is needed.*
- **Carlin, Bruce I.; Lobo, Miguel Sousa; Viswanathan, S.** - "Episodic liquidity crises: Cooperative and predatory trading," *Journal of Finance* 62(5), 2235–2274 (2007). *The experimental/OECD-bond-market companion: when cooperation among potential predators breaks down.*
- **Schied, Alexander; Zhang, Tao** - "A market impact game under transient price impact," *Mathematics of Operations Research* 44(1), 102–121 (2019). *The canonical multi-agent execution game; source of the instability threshold.*
- **Schied, Alexander; Strehle, Elias; Zhang, Tao** - "High-frequency limit of Nash equilibria in a market impact game with transient price impact," *SIAM Journal on Financial Mathematics* 8(1), 589–634 (2018). *When the continuous-time limit of the execution game does (and does not) exist.*
- **Cordoni, Francesco; Lillo, Fabrizio** - "Instabilities in multi-asset and multi-agent market impact games," *Annals of Operations Research* (2022). *Extends Schied–Zhang to many agents and assets; the scaling of impact with the number of traders is what decides stability.*
- **Cardaliaguet, Pierre; Lehalle, Charles-Albert** - "Mean field game of controls and an application to trade crowding," *Mathematics and Financial Economics* 12(3) (2018). *The mean-field limit of the execution game - what happens when the crowd is anonymous.*
- **Huberman, Gur; Stanzl, Werner** - "Price manipulation and quasi-arbitrage," *Econometrica* 72(4), 1247–1275 (2004). *No-dynamic-arbitrage: the constraint that makes an impact/decay game admissible at all.*
- **Easley, David; Kiefer, Nicholas M.; O'Hara, Maureen; Paperman, Joseph B.** - "Liquidity, information, and infrequently traded stocks," *Journal of Finance* 51(4), 1405–1436 (1996). *PIN - the first attempt to estimate the informed share that the games take as given.*
- **Easley, David; López de Prado, Marcos; O'Hara, Maureen** - "Flow toxicity and liquidity in a high-frequency world," *Review of Financial Studies* 25(5), 1457–1493 (2012). *VPIN: the high-frequency toxicity proxy.*
- **Andersen, Torben G.; Bondarenko, Oleg** - "VPIN and the flash crash," *Journal of Financial Markets* 17, 1–46 (2014). *The methodological takedown of VPIN - read it before trusting any toxicity number.*
- **Biais, Bruno; Glosten, Lawrence; Spatt, Chester** - "Market microstructure: A survey of microfoundations, empirical results, and policy implications," *Journal of Financial Markets* 8(2), 217–264 (2005). *The map of the whole field.*
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 5–7. *Corpus verification reports `hasbrouck_ch1-5.md` (Ch 5, GM) and `hasbrouck_ch6-10.md` (Ch 6 PIN, Ch 7 Kyle).*
- **Foucault, Thierry; Pagano, Marco; Röell, Ailsa** - *Market Liquidity: Theory, Evidence, and Policy* (2013), Ch 3. *Corpus verification report `foucault_ch1-3.md`.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, martingales) · [[foundations/bayesian-statistics/index|Bayesian Statistics]] (the GM recursion) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (Back's filtering argument) · [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (the quadratic execution games)
- Sibling in-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (the *non-strategic* schedule that the games generalise) · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Equilibrium-twin in Pillar 6: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (Kyle λ, the square-root law) · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (the GM game in full) · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] (estimating π from flow) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- Market-making partner: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (the maker's inventory game - the other half of the quote)
- Risk & portfolio: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (L-VaR) · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] (predation as a spillover channel) · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]

**Beginner:** start at [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05]]

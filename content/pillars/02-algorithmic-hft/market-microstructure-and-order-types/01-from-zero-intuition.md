---
title: "2.1.1 Market Microstructure from Zero"
tags:
  - pillar-algorithmic-hft
  - microstructure
  - intuition
  - market-mechanics
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types - Hub]] (or none - this page needs no prior finance).

---

### 1. Intuition & Practical Objective

This page builds the *why* of market microstructure with **no prior trading knowledge**. The goal is one idea: **a market is a mechanism that prices *immediacy*, and every order you send is a request to buy or sell that immediacy at a rate set by whoever is willing to wait.**

Start with the dumbest question: *who is on the other side of my trade?* Somebody, somewhere, is holding the opposite position. In a modern electronic market that someone is a **matching engine**: a deterministic program that pairs buy and sell instructions by published rules - first by **price** (best price first), then by **time** (first-in-first-out among equal prices). Nobody negotiates; the rules are the contract.

Three "aha"s take you from "I click buy" to a working mental model:

1. **There are two kinds of traders in every fill.** The *maker* posts a resting order and *supplies* liquidity (they wait); the *taker* sends an order that *crosses* the spread and *consumes* it (they act now). The maker earns the spread as compensation for waiting and for the risk of being wrong; the taker pays it as the price of certainty. The **bid-ask spread** *is* the price of immediacy.

2. **"The price" is really several prices at once.** At one instant there is a best bid, a best ask, a mid, a *micro-price* (size-weighted), a last-trade price, and hypothetical prices for buying *more* size. Hasbrouck (Ch 1) stresses this: prices are multiple and mechanism-dependent. Microstructure is the study of those gaps.

3. **Waiting is not free - it is a loan you make to strangers.** A resting limit order is an option written *for free* to everyone else: they may fill you exactly when your price has become bad (you get **adversely selected**) and leave you alone when it has become good. That asymmetry - not commission - is the true cost of liquidity provision.

**The landscape in one picture.** Orders are *typed instructions*; venues are *mechanisms* that accept them: **exchanges** (continuous limit-order markets, sometimes with call auctions at the open/close), **dark pools** (no displayed quotes, often midpoint matching), and **OTC / dealer markets** (a dealer quotes a two-sided price and you trade against their balance sheet). Every later Pillar 2 topic - execution algorithms, optimal execution, fill probability, low-latency systems - is downstream of the vocabulary on this page.

> **The one-sentence essence.** "Microstructure is the economics of immediacy: makers wait and are paid the spread while bearing adverse selection, takers cross and pay it, and the matching engine decides who is first."

---

### 2. Mathematical Ground Truth & Derivations

**The Roll model: decomposing a trade price (Hasbrouck Ch 3).** The simplest formal statement of the idea that the spread is a waiting cost. Let the *efficient* (latent consensus) price follow a random walk, $m_t=m_{t-1}+u_t$ with $\mathrm{Var}(u_t)=\sigma_u^2$, and let a dealer/liquidity supplier charge a half-spread $c$ around it. The observed **trade price** is

$$
p_t=m_t+q_t c,\qquad q_t=\begin{cases}+1 & \text{buy}\\-1 & \text{sell}\end{cases},
$$

with buys/sells equally likely and serially independent of $u_t$. Define price changes $\Delta p_t=p_t-p_{t-1}$. Then

$$
\Delta p_t=c\,(q_t-q_{t-1})+u_t.
$$

Taking moments (and using $\mathrm{Var}(q_t)=1$, $\mathrm{Cov}(q_t,q_{t-1})=0$):

$$
\boxed{\;\gamma_0\equiv\mathrm{Var}(\Delta p_t)=2c^2+\sigma_u^2,\qquad \gamma_1\equiv\mathrm{Cov}(\Delta p_{t-1},\Delta p_t)=-c^2\;}
$$

and all higher autocovariances vanish. This is the *entire* content of the Roll model: the bid-ask **bounce** ($c^2$) creates a *negative* first-order autocorrelation in trade-price changes, while the efficient-price innovation contributes only contemporaneous variance. Inverting:

$$
\boxed{\;c=\sqrt{-\gamma_1},\qquad \sigma_u^2=\gamma_0+2\gamma_1,\qquad \text{quoted spread}=2c=2\sqrt{-\gamma_1}.\;}
$$

**Why this matters.** The spread $2c$ is *estimable from trade prices alone* - a pure microstructure signal hidden inside an otherwise near-random-walk price series. Empirically (Hasbrouck Ch 3, PCO Oct 2003) $\hat\gamma_1=-0.0000294$ gives $c= $ \$0.017, spread \0.034, close to the observed time-weighted NYSE average of \$0.032 - a striking confirmation.

**The same spread, from information (Foucault Ch 1; Hasbrouck Ch 5).** The Roll $c$ is a cost of *waiting*; the Glosten–Milgrom spread is a cost of *being picked off*. With informed arrival proportion $\mu$ and value dispersion $(V_H-V_L)$, the symmetric-prior spread is $A-B=(V_H-V_L)\,\mu$ - the model-free intuition that **more adverse selection widens the spread.** Both costs coexist: the quoted spread pays for order processing, inventory, *and* adverse selection at once.

---

### 3. Computational Implementation - recovering the spread from trade prices

Simulate the Roll data-generating process and recover $c$ from the autocovariances, exactly as an econometrician would from tape data. Standard library only; **re-executed and reproduced**.




**Read the numbers.** The near-exact recovery $\hat{c}=0.0195$ versus the true $c=0.02$ (and $\hat\gamma_1=-0.00038$ versus theory $-0.00040$) shows the bounce signal survives in a price series whose innovations are five times larger ($\sigma_u=0.10$) than the spread component - the spread is small but *systematic*, so autocovariance exposes it. The last two lines are the whole economics of liquidity: taking costs $2$ bps, making *earns* $2$ bps **but only when the order fills** - and the orders that fill are disproportionately the ones you did not want to fill.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing "the price" with the executed price.** The last trade, the mid, and the price you will actually get are three different numbers. The beginner error is to model execution at the mid; you *cross* the spread as a taker and *forgo* it as a maker.
2. **Treating the spread as a fee.** The half-spread $c$ is not a constant toll - it *widens* with adverse selection, volatility, and inventory stress (Foucault Ch 3). Quoting a fixed spread through a news event is a guaranteed loss to informed flow.
3. **Ignoring adverse selection when providing liquidity.** Passive orders earn the spread *on average across all fills*, but the fills are not a random sample: they cluster in the states where the price is about to move against you. A resting order is a short option; see [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 1 (the field, multiple simultaneous prices, liquidity = depth/breadth/resiliency) and Ch 3 (the Roll model, PCO calibration). *Verified in `hasbrouck_ch1-5.md`.*
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013), Ch 1 (liquidity and price discovery, the liquidity-definition triad, the spread as the primary illiquidity measure). *Verified in `foucault_ch1-3.md`.*
- **Harris, Larry** - *Trading and Exchanges* (2003). *The accessible map of traders, orders, and venues - the best zero-knowledge companion to this page.*
- **O'Hara, Maureen** - *Market Microstructure Theory* (1995). *The model-based foundation beneath the Roll and Glosten–Milgrom ideas.*

---

### 6. Connected Graph Bridges

- Continue: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/02-order-types|02 · Order Types]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Index Hub]]
- Book mechanics: [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- The spread, decomposed: [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]

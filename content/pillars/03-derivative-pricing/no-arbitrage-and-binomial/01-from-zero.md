---
title: "3.2.1 No-Arbitrage from Zero"
tags:
  - pillar-derivative-pricing
  - no-arbitrage-and-binomial
  - intuition
  - replication
  - delta-hedging
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]. No prior derivatives knowledge.

---

### 1. Intuition & Practical Objective

Start with the dumbest question: *why does an option have a price at all?* A stock has a price because it pays future cash flows. An option is only a contract. Its value comes from a different mechanism - you can **manufacture** its payoff out of the stock and a bank account. If the manufacturing cost is knowable, the option must trade at that cost, because otherwise you sell the option and build the payoff yourself (or the reverse) and pocket a risk-free difference.

The one-period binomial is the smallest market where this works. The stock starts at $S_0$ and over one period becomes either $uS_0$ or $dS_0$. There are exactly two uncertain states, and we have exactly two instruments - the stock and the bond. Two instruments, two states: the replication equations are a **square linear system**, so they have a solution. That is the entire reason the binomial model prices derivatives, and it is worth seeing the algebra once by hand.

Three "aha"s:

1. **You can always build the payoff.** Choose $\Delta$ shares and a bond position $B$ so that $\Delta S_1+B(1+r)$ equals the claim in *both* states. Two equations, two unknowns - solvable, unconditionally.
2. **Therefore the price is forced.** If the option trades at anything other than $\Delta S_0+B$, buy the cheap one and sell the expensive one. No probabilities were mentioned.
3. **Real-world probabilities drop out.** The system never used the physical chance of "up". What is left is a *reweighted* average - the risk-neutral probabilities - that behaves like a probability distribution and prices everything.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The model and the no-arbitrage bracket

Stock $S_0>0$, factors $0<d<u$, money market $1\to(1+r)$, so $S_1(H)=uS_0$, $S_1(T)=dS_0$ (Shreve eq. 1.1). The model is arbitrage-free **iff**

$$
\boxed{\;d<1+r<u\;}
$$

- If $1+r\le u$: the bond weakly dominates the stock in the up state, so nobody holds stock - the model is economically degenerate (Shreve §1.1).
- If $d\ge 1+r$: borrow at rate $r$, buy one share; you owe $(1+r)S_0$ and hold at least $dS_0\ge(1+r)S_0$ in every state, strictly more when the stock rises. That is arbitrage.

This is the discrete ancestor of every "no free lunch" condition in the pillar, and the reason a binomial tree needs a *strictly interior* risk-free growth factor (Björk Prop 2.3 states the non-strict form $d\le 1+R\le u$; the strict form, Prop 2.26, guarantees positive martingale weights).

#### 2.2 Replication → delta → price

Sell a claim with unknown price $V_0$; hedge with $\Delta_0$ shares financed by $V_0-\Delta_0S_0$ in the money market. Require the portfolio to reproduce the payoff in both states (Shreve 1.3–1.4):

$$
V_1(H)=\Delta_0S_1(H)+(1+r)(V_0-\Delta_0S_0),\qquad V_1(T)=\Delta_0S_1(T)+(1+r)(V_0-\Delta_0S_0).
$$

Subtract - the bond term cancels and the unknown price drops out - leaving the **replicating delta**:

$$
\boxed{\;\Delta_0=\frac{V_1(H)-V_1(T)}{S_1(H)-S_1(T)}=\frac{f_u-f_d}{S_0(u-d)}\;}\qquad(1.6)
$$

Substituting back gives the **arbitrage price** with the risk-neutral weights

$$
\tilde p=\frac{1+r-d}{u-d},\qquad \tilde q=\frac{u-1-r}{u-d}=1-\tilde p,\qquad V_0=\frac{1}{1+r}\big[\tilde p f_u+\tilde q f_d\big].\qquad(1.8\text{–}1.9)
$$

By the bracket, $\tilde p,\tilde q\in(0,1)$ and $\tilde p+\tilde q=1$: they are a legitimate probability measure $\widetilde{\mathbb P}$ - the **risk-neutral measure** - *derived* from (1.3)–(1.4), with no relation to the real coin-toss probabilities.

#### 2.3 Two periods: re-hedge, then backward induction

The same argument repeats at every node. At time 1 in state $\omega_1$ the hedger holds $\Delta_1(\omega_1)$ shares and wealth $X_1(\omega_1)=\Delta_0S_1(\omega_1)+(1+r)(V_0-\Delta_0S_0)$. Working backwards from $V_2=(S_2-K)^+$:

$$
V_1(H)=\frac{\tilde pV_2(HH)+\tilde qV_2(HT)}{1+r},\quad V_1(T)=\frac{\tilde pV_2(TH)+\tilde qV_2(TT)}{1+r},\quad V_0=\frac{\tilde pV_1(H)+\tilde qV_1(T)}{1+r},
$$

$$
\Delta_1(\omega_1)=\frac{V_2(\omega_1,H)-V_2(\omega_1,T)}{S_2(\omega_1,H)-S_2(\omega_1,T)}.
$$

This is **backward induction / dynamic replication**: rebalance the hedge at each step so the portfolio lands on the payoff at maturity. It is the discrete template of BSM's continuous delta-hedge ([[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|BSM · 04 Greeks & Hedging]]).

---

### 3. Computational Implementation - replication, verified

Take Shreve's Example 1.1 parameters: $S_0=4,u=2,d=\tfrac12,r=\tfrac14$, and price a European put with $K=5$ (payoffs $f_u=0$, $f_d=3$). Stdlib only.




The hedge is a **short** position of half a share plus $3.20$ in the bank; it pays exactly $0$ or $3$ as required, so the option *must* cost $1.20$. Nothing in this calculation knew whether the coin is fair.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing $\tilde p$ with a forecast.** $\tilde p$ is the number that makes the replication algebra close, not a belief about the market. If you swap in your own view of "up", you leave the arbitrage-free price and start generating your own, non-tradeable, number.
2. **Forgetting the bracket.** If a reader plugs a large $\Delta t$ into $u=e^{\sigma\sqrt{\Delta t}}$ without checking $u>1+r$, the "risk-neutral probability" leaves $[0,1]$ and the tree silently admits arbitrage ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **Replicating in one period, then holding.** One-period delta is correct only until the stock moves. The two-period example re-derives $\Delta_1$ at each node; a fixed delta leaves residual risk - the discrete ancestor of gamma risk.
4. **Assuming the payoff is replicable forever.** Two states and two instruments made the system square. With jumps or untraded factors it stops being square, no hedge exists, and the price is no longer unique ([[pillars/03-derivative-pricing/no-arbitrage-and-binomial/04-fundamental-theorems|04 · Fundamental Theorems]]).

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance I*, §1.1 - the bracket $d<1+r<u$ with its economic justification, the replication equations (1.3)–(1.4), delta (1.6), risk-neutral probabilities (1.8) and the price (1.9); §3.2 the abstract one-step APT. *Math-verified in the corpus (Example 1.1 params reused here).*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 2 - one-period model, arbitrage portfolio (Def 2.2), no-arbitrage (Prop 2.3), replicating weights (eqs 2.2–2.3), risk-neutral valuation (Prop 2.11).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13.1–13.2 - the same one-step delta (eq 13.1) and risk-neutral valuation (eqs 13.2–13.3).

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]]
- Continue: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/02-no-arbitrage-and-risk-neutral|02 · No-Arbitrage & Risk-Neutral]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton/01-from-zero-intuition|BSM · 01 From Zero]]

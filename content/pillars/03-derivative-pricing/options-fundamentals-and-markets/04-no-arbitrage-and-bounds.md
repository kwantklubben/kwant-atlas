---
title: "3.1.4 No-Arbitrage Bounds, Parity & Early Exercise"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - put-call-parity
  - price-bounds
  - early-exercise
  - arbitrage
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/options-fundamentals-and-markets/03-markets-and-products|03 · Markets & Products]].

---

### 1. Intuition & Practical Objective

This page is the **model-free spine** of the pillar. Before Black–Scholes, before any assumption about volatility or lognormal prices, there are relationships an option price *cannot* violate without creating free money. The practical objective: have the bounds, put–call parity, and the early-exercise rules at your fingertips, because they are (a) the first sanity check on any quoted price and (b) the only results that survive when the model is wrong.

The central object is **put–call parity**. It says a call plus a discounted strike is the *same cash-flow stream* as a put plus the stock - so the two must cost the same. It is not a model; it is an *identity* built from two portfolios that pay identically in every state of the world. Every quoted option price in a liquid market obeys it to within the bid/ask spread. When it is violated, a **conversion** (buy the cheap side, sell the rich side, hold the hedge to expiry) locks a riskless profit.

> **The one-sentence essence.** "Two portfolios with identical payoffs in every state must have identical prices; applied to a call and a put this gives $c+Xe^{-rT}=p+S_0$ - model-free, volatility-free, and the tightest thing you can say about an option price before you commit to a dynamics."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The six factors, and the bounds they imply (Hull Ch 11.1)

The **six inputs** to any European option price are $S_0$, $K$, $T$, $\sigma$, $r$, and dividends. Table 11.1's direction of effects: $c$ rises with $S_0,\sigma,r,T$ and falls with $K$ and dividends; $p$ rises with $K,\sigma,r$ (via discounting) and falls with $S_0$; American options are worth at least as much as European.

**Upper bounds** (Hull 11.1–11.3):

$$
c\le S_0,\qquad C\le S_0,\qquad P\le K,\qquad p\le Ke^{-rT}.
$$

**Lower bounds** (Hull 11.4–11.5, no dividends):

$$
c\ge\max(S_0-Ke^{-rT},\,0),\qquad p\ge\max(Ke^{-rT}-S_0,\,0).
$$

The lower bound for a call is *strictly greater* than the intrinsic value $\max(S_0-K,0)$ for a positive rate - you are not obliged to pay $K$ until $T$. This gap is why a deep-ITM American *call* is still never exercised early.

#### 2.2 Put–call parity (Hull 11.6; Haug 1.13)

$$
c+Ke^{-rT}=p+S_0.
$$

**Derivation by replication.** Portfolio A: one call $+$ cash $Ke^{-rT}$. Portfolio B: one put $+$ one share. At expiry both are worth $\max(S_T,K)$:

$$
A_T=\max(S_T-K,0)+K=\max(S_T,K),\qquad B_T=\max(K-S_T,0)+S_T=\max(S_T,K).
$$

Identical payoffs, identical price today, hence parity. **Generalized form** (Haug 1.18) for any carry $b$:

$$
c-p=Se^{(b-r)T}-Xe^{-rT}=e^{-rT}\big(Se^{bT}-X\big),
$$

which specializes to stock ($b=r$): $c-p=S-Xe^{-rT}$; index ($b=r-q$): $c-p=Se^{-qT}-Xe^{-rT}$; futures ($b=0$): $c-p=(F-X)e^{-rT}$; currency ($b=r-r_f$): $c-p=Se^{-r_fT}-Xe^{-rT}$.

**American bounds** (Hull 11.7) are inequalities, because early exercise breaks the replication: $S_0-K\le C-P\le S_0-Ke^{-rT}$.

#### 2.3 Early exercise (Hull 11.5–11.6; Shreve §7)

- **American call, non-dividend stock: never optimal to exercise early**, so $C=c$. Two reasons: exercising destroys the insurance value of the option, and you pay $K$ earlier than necessary, forgoing interest.
- **American put: early exercise can be optimal** when deep ITM, more attractive as $S_0$ falls, $r$ rises, $\sigma$ falls. Hence $P\ge\max(K-S_0,0)$ and $\max(K-S_0,0)\le P\le K$.
- **Dividends** change the call story: exercise is optimal only *just before an ex-dividend date*; with known dividends $D$, the bounds and parity become
$$
c\ge\max(S_0-D-Ke^{-rT},0),\quad p\ge\max(D+Ke^{-rT}-S_0,0),\quad c+D+Ke^{-rT}=p+S_0.
$$

---

### 3. Computational Implementation - parity, bounds, an arbitrage, and early exercise

Standard library only. It reproduces a Haug-verified parity number, checks the Hull bounds, *executes* a parity-violation arbitrage and shows the riskless profit is the same at every terminal price, and solves a two-period tree where the American put strictly beats the European (Shreve's worked example).



Three verified statements in one run: parity pins the put at $8.37909$; the arbitrage profit $+1.97543$ is **identical at $S_T=90,105,120$** - that is what "riskless" means; and the American put's extra $0.4000$ comes entirely from exercising at the down node ($3.00$ intrinsic beats $2.00$ continuation).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Parity is model-free - bounds are too, but only if the hedges are feasible.** The arbitrage above requires **shorting the stock** and borrowing at $r$. With short-sale constraints, borrow costs, or a hard-to-borrow name, parity can persist violated for a long time. This is the structural route into the frictions catalogued in [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes]].
2. **Using the European formula on an American put.** The early-exercise premium ($0.4000$ even in a two-period tree) is *not* small. Applying the closed form understates the price.
3. **Reading parity as a statement about the model.** Parity holds for *any* dynamics - it is not evidence that the lognormal/BSM formula is right. Believing otherwise confuses an identity with a theory.
4. **Forgetting the discounting in the lower bound.** $c\ge S_0-K$ is **false**; the correct floor is $S_0-Ke^{-rT}$, which is higher. A naive floor lets you "trade" a non-existent arbitrage.
5. **The dividend form.** With known dividends, parity becomes $c+D+Ke^{-rT}=p+S_0$; omitting $D$ makes an in-the-money call look underpriced by exactly the dividend's present value.
6. **Ignoring the bid/ask.** In practice parity is violated by the spread almost always, and by a *little* - a "violation" you cannot actually capture after costs is not an arbitrage.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 11 §11.1–11.7 (six factors, upper/lower bounds, put–call parity and its arbitrage tables, American bounds, early-exercise rules, dividend adjustments) and Ch 12 (the parity relation between covered call and protective put).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1.2 (parities and symmetries: eq. 1.13–1.25, including put–call symmetry and supersymmetry). *Numerically verified.*
- **Shreve**, *Stochastic Calculus for Finance I*, §1.1 (the discrete no-arbitrage bracket $d<1+r<u$), §3.5 (completeness), §5.1–5.2 (American algorithm, smallest supermartingale), and §7 (the no-early-exercise theorem for convex payoffs with $g(0)=0$). *Math-verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/03-markets-and-products|03 · Markets & Products]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Index Hub]]
- Next: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- This is the seed of the pillar: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial|No-Arbitrage & the Binomial Model]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]]
- Parity in closed form: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · The Pricing Formulas]]

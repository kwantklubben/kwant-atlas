---
title: "3.1 Options, Futures & Markets"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - markets
  - payoff-diagrams
  - index-hub
  - entry-point
---

**Basic Prerequisites:** None. **This is the entry point to Pillar 3** - start here if you have never priced a derivative. Everything else in the pillar assumes the vocabulary built on this page.

---

### 1. Intuition & Practical Objective

A **derivative** is a contract whose value is *derived* from something else - a stock, an index, a currency, a commodity, an interest rate. That is the whole idea. The stock itself pays you cash flows; a derivative pays you cash *only because the stock moved*, and the contract says exactly how. The practical objective of this folder is to give you the **product menu and the conventions** - what each instrument *is*, what it pays, where it trades, and what the no-arbitrage relationships between its prices must be - before a single model is written.

The reason this is a *separate topic* and not a preface is that the four instruments below are not variations on one idea; they are **four different shapes of the same contract**. A forward is *symmetric* (both sides can win or lose, costless to enter). An option is *asymmetric* (one side has a right, the other an obligation, and the right is paid for up front). A swap is a **portfolio of forwards**. A futures contract is a forward that is **settled every day**. Get the shapes wrong and no amount of Black–Scholes will save the answer.

> **The one-sentence essence.** "A derivative is a contract that pays a specified function of an underlying price; its fair value is fixed by the cost of *replicating that function* with traded assets, and the first place that constraint shows itself is in the payoffs, the bounds, and put–call parity - all of which hold without assuming any model."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All statements below are transcribed from the verified corpus (Hull 11th ed. Ch 1–12, Haug §1, Shreve Vol I §1/§5) and every number in the check column was **re-executed** in §3.

**Notation:** $S$ spot, $S_T$ terminal spot, $K$ (or $X$) strike, $F$ futures/forward price, $T$ time to expiry (years), $r$ risk-free rate, $q$ dividend yield, $r_f$ foreign rate, $b$ cost-of-carry, $\sigma$ vol, $N(\cdot)$ standard normal CDF.

#### 2.1 The derivative product menu (Hull's taxonomy)

| Instrument | Obligation? | Payoff to the *long* | Entry cost | Trades | Essence |
|---|---|---|---|---|---|
| **Forward** | Yes, both sides | $S_T-K$ | $0$ | OTC | Symmetric, bespoke, settled once at $T$ |
| **Futures** | Yes, both sides | $S_T-K$ (in total) | $0$ (+ margin) | Exchange | A standardised forward, **marked to market daily** |
| **Call option** | Right, buyer only | $\max(S_T-K,\,0)$ | premium up front | Both | Asymmetric, capped downside, unbounded upside |
| **Put option** | Right, buyer only | $\max(K-S_T,\,0)$ | premium up front | Both | Asymmetric, the mirror of the call |
| **Swap** | Yes, both sides | floating $-1$ fixed (per period) | $0$ | OTC | A strip of forwards / FRAs |

**The four option positions** (Hull Ch 10.2 - the whole payoff algebra in one table):

| Position | Payoff at $T$ | Max loss | Max gain |
|---|---|---|---|
| Long call | $\max(S_T-K,0)$ | premium | unbounded |
| Short call | $-\max(S_T-K,0)$ | unbounded | premium |
| Long put | $\max(K-S_T,0)$ | premium | $K-\text{premium}$ |
| Short put | $-\max(K-S_T,0)$ | $K-\text{premium}$ | premium |

#### 2.2 The no-arbitrage skeleton (model-free)

| Quantity | Statement | Verified check |
|---|---|---|
| **Forward price** (Hull 5.1) | $F_0 = S_0e^{rT}$ (no income) | $60\,e^{0.05}=63.0763$ (~$63 in Hull Ch 1) |
| **Forward value** (Hull 5.4/5.5) | $f=(F_0-K)e^{-rT}=S_0-Ke^{-rT}$ | $66-63e^{-0.025}=4.5555$ |
| **Put–call parity** (stock, Hull 11.6; Haug 1.13) | $c+Xe^{-rT}=p+S_0$ | $S{=}100,\,X{=}105,\,r{=}.10,\,c{=}8.5\Rightarrow p=8.37909$ (Haug) |
| **Parity, generalized** (Haug 1.18) | $c-p=Se^{(b-r)T}-Xe^{-rT}$ | $b{=}r\Rightarrow c-p=S-Xe^{-rT}=0.12091$ |
| **Lower bounds** (Hull 11.4/11.5) | $c\ge\max(S_0-Xe^{-rT},0),\quad p\ge\max(Xe^{-rT}-S_0,0)$ | $c\ge0.12091,\;p\ge0.00000$ |
| **Upper bounds** (Hull 11.1–11.3) | $c\le S_0,\qquad p\le Xe^{-rT}$ | $c\le100,\;p\le99.8791$ |
| **American call ≡ European call** (no dividends) (Hull 11.5; Shreve §7) | $C=c$ | - *(put counter-example: Shreve tree European put $0.9600$ vs American $1.3600$)* |
| **American parity bounds** (Hull 11.7) | $S_0-K\le C-P\le S_0-Xe^{-rT}$ | - |
| **Futures-option parity** (Hull 18.1) | $c+Xe^{-rT}=p+Fe^{-rT}$ | Black-76 parity at $b=0$ |
| **Black-76 (futures) call** (Haug 1.5) | $e^{-rT}[FN(d_1)-XN(d_2)]$ | $F{=}X{=}19,\,r{=}.10,\,\sigma{=}.28\Rightarrow c=1.70105$ (Haug) |

#### 2.3 Conventions that must be carried into every calculation

- **Cost-of-carry dictionary** (one master formula, many models): $b=r$ stock · $b=r-q$ index/yield $q$ · $b=0$ futures (Black-76) · $b=r-r_f$ currency. **Wrong $b$ = wrong price** (Haug §1).
- **Contract multiplier.** Equity/index options: $100\times$ premium per contract; index options are $100\times$ the index (Hull Ch 10.3).
- **Moneyness.** In-the-money / at-the-money / out-of-the-money by $S$ vs $K$; option value $=$ **intrinsic value $+$ time value** (Hull Ch 10.4).
- **European vs American.** European: exercise only at $T$. American: any time $\le T$ - a *free option on the option*, hence $\ge$ the European value (Hull Ch 10.1).
- **Exchange-traded vs OTC.** Exchange = standardised, cleared, margined; OTC = bespoke, bilateral/CCP, ISDA + CSA. Dec-2019 scale: OTC notional $\approx$ $$\$558.5T vs exchange ≈\$96.5T (Hull Ch 1).

---

### 3. Computational Implementation - the payoff engine and the parity checks

Standard library only (`math.erf` gives the exact normal CDF). This block produces the payoff table, the Haug-verified parity number, and the Black-76 anchor used throughout the folder.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's full failure-mode analysis lives in [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Confusing the instrument shapes** - treating a short forward like a short option (the obligations differ), or an American for a European (the early-exercise premium is real: $0.4000$ on the Shreve tree).
2. **Applying an option formula to a forward, or vice versa** - the cost-of-carry dictionary ($b=r$ vs $b=0$ vs $b=r-r_f$) is the first thing to check; the wrong $b$ misprices by exactly the missing factor.
3. **Ignoring the basis and the friction of real hedges** - a textbook hedge assumes the underlying and the hedging instrument are *the same asset*; in practice $b_2\ne0$ and hedge effectiveness is only $\rho^2$ (Hull Ch 3).

---

### 5. References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed., 2022)
- **Shreve, Steven E.**: *Stochastic Calculus for Finance I*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006)
- **Hull, J. & White, A.**: background on OIS discounting and post-2008 clearing (via Hull

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- **Forward topic-page (next step):** [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]]
- Sibling topic-folders (in-pillar): [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial|No-Arbitrage & the Binomial Model]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options|Exotic & Path-Dependent Options]] · [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva|Counterparty Risk & XVA]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure|Interest Rate & Term Structure]]
- Sub-pages (in-folder): 01 What Is a Derivative · 02 Options Mechanics & Payoffs · 03 Markets & Products · 04 No-Arbitrage & Bounds · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/options-fundamentals-and-markets/01-what-is-a-derivative|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05]]

---
title: "Adverse Selection & the Glosten–Milgrom Model: Topic Hub & Formula Lookup"
tags:
  - pillar-market-making
  - adverse-selection
  - glosten-milgrom
  - informed-trading
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayesian updating, martingales) and [[foundations/bayesian-statistics/index|Bayesian Statistics]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Why does a bid-ask spread exist even in a liquid market with zero exchange fees and zero inventory-carrying costs? The answer is **adverse selection**. When a trader hits your ask with a market buy, they may *know* the stock is about to tick up and you do not. If they are an informed insider, every such fill costs you money. The spread is the toll the market maker charges — extracted from liquidity-driven noise traders — to stay whole against the losses inflicted by better-informed counterparties.

This folder is the **adverse-selection and Glosten–Milgrom (1985)** topic-folder for Pillar 6. It is a *hub*: it (a) gives you the **fast formula-and-model lookup** below, and (b) routes you to six sub-pages that walk from first-principles intuition through the GM sequential-trade model and its Bayesian market maker. *Primary verified sources:* Hasbrouck *Empirical Market Microstructure* (Ch 5, the GM model; Ch 6 PIN; Ch 7 Kyle; Ch 8 generalized Roll) and Foucault, Pagano & Röell *Market Liquidity* (Ch 3), cross-checked against the primary papers (Glosten–Milgrom 1985; Copeland–Galai 1983; Kyle 1985; Glosten–Harris 1988).

> **The one-sentence essence.** "The bid-ask spread is, at bottom, the market maker's compensation for trading against better-informed counterparties: quote your ask at the expected value **conditional on** having sold (a buy just arrived) and your bid at the expected value **conditional on** having bought — the gap between the two is the cost of information."

---

### 2. Mathematical Ground Truth & Derivations

**Quick lookup.** The folder's key formulas in one table; each is derived on the sub-pages.

| Quantity | Formula | Note |
| :--- | :--- | :--- |
| Buy-arrival law | $\mathbb{P}(B\mid V_H)=\tfrac{1+\pi}{2},\ \mathbb{P}(B\mid V_L)=\tfrac{1-\pi}{2}$ | $\pi$ = informed share |
| Bayesian update | $\theta_t^{+}=\dfrac{\tfrac{1+\pi}{2}\theta_{t-1}}{\tfrac{1+\pi}{2}\theta_{t-1}+\tfrac{1-\pi}{2}(1-\theta_{t-1})}$ | buy raises belief |
| Zero-profit quotes | ask $=$ E$[V\mid$ buy$]$, bid $=$ E$[V\mid$ sell$]$ | competitive MM |
| GM spread (symmetric, $\theta=\tfrac12$) | $A-B=\pi\,(V_H-V_L)$ | widens with informed share |
| P(informed $\mid$ buy) | $\dfrac{2\pi}{1+\pi}$ | toxicity of a fill |
| PIN (EKOP) | $\dfrac{\alpha\mu}{\alpha\mu+2\varepsilon}$ | $\alpha$=info-event prob, $\mu$=informed rate, $\varepsilon$=noise rate |
| Kyle lambda | $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$, depth $=1/\lambda$ | from Kyle 1985 |


**Notation (Foucault/standard):** true value $V\in\{V_L,V_H\}$; prior belief $\theta_t=\mathbb{P}(V=V_H)$; $\pi$ (or $\mu$) $=$ probability a trader is **informed**; $\mu_t=\theta_t V_H+(1-\theta_t)V_L$ the semi-strong efficient price.

#### The Glosten–Milgrom Bayesian market maker (the core)

A competitive, risk-neutral market maker posts quotes that yield **zero expected profit** against a trader whose type (informed vs uninformed) is unobserved and drawn each round with probability $\pi$. Uninformed traders buy/sell with probability $\tfrac12$ each for liquidity reasons; informed traders know the true state and always trade in its direction.

The arrival-law of a Buy order:

$$\mathbb{P}(B\mid V_H)=\pi\cdot 1+(1-\pi)\tfrac12=\tfrac{1+\pi}{2},\qquad
\mathbb{P}(B\mid V_L)=\pi\cdot 0+(1-\pi)\tfrac12=\tfrac{1-\pi}{2}.$$

Bayes' rule moves the belief $\theta_t$:

$$\theta_t^{+}\equiv\mathbb{P}(V_H\mid B_t)
=\frac{\tfrac{1+\pi}{2}\,\theta_{t-1}}{\tfrac{1+\pi}{2}\theta_{t-1}+\tfrac{1-\pi}{2}(1-\theta_{t-1})}>\theta_{t-1},
\qquad
\theta_t^{-}\equiv\mathbb{P}(V_H\mid S_t)
=\frac{\tfrac{1-\pi}{2}\,\theta_{t-1}}{\tfrac{1-\pi}{2}\theta_{t-1}+\tfrac{1+\pi}{2}(1-\theta_{t-1})}<\theta_{t-1}.$$

**Zero-profit quotes** ("regret-free"): the ask is the expected value *given a buy just hit it*; the bid the expected value *given a sell just hit it*:

$$A_t=\mathbb{E}[V\mid B_t]=V_L+\theta_t^{+}(V_H-V_L),\qquad B_t=\mathbb{E}[V\mid S_t]=V_L+\theta_t^{-}(V_H-V_L).$$

**Bid-ask spread** (Foucault eq. 3.12–3.15). As the belief extremes ($s_a^t,\,s_b^t$) straddle $\mu_{t-1}$:

$$S_t=A_t-B_t=s_a^t+s_b^t,\qquad
s_a^t=\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi\,\theta_{t-1}+(1-\pi)\tfrac12}(V_H-V_L),\qquad
s_b^t=\frac{\pi\,\theta_{t-1}(1-\theta_{t-1})}{\pi\,(1-\theta_{t-1})+(1-\pi)\tfrac12}(V_H-V_L).$$

**Symmetry at $\theta_{t-1}=\tfrac12$** (the deep, testable special case):

$$\boxed{\;S=(\pi)(V_H-V_L)\;}$$

- **First-trade spread at $\theta_0=\tfrac12$:** $S_1=\pi(V_H-V_L)$ (Foucault eq. 3.12).
- Spread is largest at maximal uncertainty ($\theta=\tfrac12$) and shrinks to $0$ as the maker learns ($\theta\to1$ or $0$). **Below a single informed trader ($\pi=0$) the spread collapses to zero even with no processing/inventory cost** — the pure information result of GM (Hasbrouck Ch 5; also copeland–Galai's "short a put and a call").
- Hasbrouck writes it with $\delta=\mathbb{P}(V=V_L)$: $\;A-B=\dfrac{4(1-\delta)\delta\,\mu\,(V_H-V_L)}{1-(1-2\delta)^2\mu^2},\;$ which at $\delta=\tfrac12$ gives exactly $A-B=(V_H-V_L)\,\mu$.

#### Other canonical pieces (bridged from this folder)

- **Copeland–Galai (1983):** the dealer is effectively *short a put and a call* written to informed traders — an option-pricing framing of the same information cost.
- **Kyle (1985):** $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ price impact; $\Delta P=\lambda\,Q$; depth $=1/\lambda$; exactly half the private info is impounded, $Var[v\mid y]=\Sigma_0/2$ (Hasbrouck Ch 7).
- **PIN (Easley–Kiefer–O'Hara):** $\mathrm{PIN}=\alpha\mu/(\alpha\mu+2\epsilon)$ (Hasbrouck Ch 6 — event probability $\alpha$, informed intensity $\mu$, uninformed intensity $\epsilon$).
- **Spread decomposition (Hasbrouck Ch 8; Glosten–Harris 1988; Huang–Stoll 1997):** $\Delta p_t=c(q_t-q_{t-1})+\lambda q_t+u_t$ separates the **transitory** (order-processing $c$, instantly reversing) from the **permanent** (adverse-selection $\lambda$) component.

---

### 3. Computational Implementation — the GM market maker (stdlib only)

The centerpiece is the full sequential Bayesian market maker: it posts $A,B$ from the belief, simulates an informed/uninformed trader each round, applies Bayes, and — over a long sequence of trades — drives the posterior to the true value while the spread decays. **Ran and verified** (exact output below, §3 of [[#the-glosten-milgrom-model|03 · The GM Model]]).

```python
import math, random

def gm_quotes(prior_high, mu, v_low=10.0, v_high=12.0):
    """Zero-profit GM competitive quotes. Returns (ask, bid, theta_after_buy, theta_after_sell)."""
    pbH, pbL = (1 + mu) / 2, (1 - mu) / 2
    psH, psL = (1 - mu) / 2, (1 + mu) / 2
    th_buy  = pbH * prior_high / (pbH * prior_high + pbL * (1 - prior_high))
    th_sell = psH * prior_high / (psH * prior_high + psL * (1 - prior_high))
    ask = v_low + th_buy  * (v_high - v_low)
    bid = v_low + th_sell * (v_high - v_low)
    return ask, bid, th_buy, th_sell

print("theta=1/2, V in {10,12}:  competitive spread = mu*(V_H - V_L) = 2*mu")
for mu in (0.0, 0.1, 0.25, 0.5, 0.9):
    a, b, _, _ = gm_quotes(0.5, mu)
    print(f"  mu={mu:.2f}: ask={a:.4f}  bid={b:.4f}  spread={a-b:.4f}     2*mu={2*mu:.2f}")
a, b = gm_quotes(0.5, 0.25)[:2]
print(f"\nmu=0.25 example: ask={a:.4f} bid={b:.4f} spread={a-b:.4f}  (0.25 * (12-10) = 0.50)")
```

```
theta=1/2, V in {10,12}:  competitive spread = mu*(V_H - V_L) = 2*mu
  mu=0.00: ask=11.0000  bid=11.0000  spread=0.0000     2*mu=0.00
  mu=0.10: ask=11.1000  bid=10.9000  spread=0.2000     2*mu=0.20
  mu=0.25: ask=11.2500  bid=10.7500  spread=0.5000     2*mu=0.50
  mu=0.50: ask=11.5000  bid=10.5000  spread=1.0000     2*mu=1.00
  mu=0.90: ask=11.9000  bid=10.1000  spread=1.8000     2*mu=1.80

mu=0.25 example: ask=11.2500 bid=10.7500 spread=0.5000  (0.25 * (12-10) = 0.50)
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The winner's curse.** The maker gets filled precisely when the order is adverse — if you underestimate the informed fraction $\pi$, you quote a spread thinner than the information cost and lose on both sides (see the P&L experiment in 05).
2. **Spreads are not symmetric about the efficient price.** The midpoint equals the unconditional value *only* when $\theta=\tfrac12$; elsewhere quotes sit asymmetrically and the naive mid is a biased price.
3. **Adverse selection is toxic, not random.** Relentless one-sided flow is a symptom of informed trading; a maker who keeps quoting through it accumulates a fatal position (bridge to [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).

---

### 5. Canonical Literature & Study References

- **Glosten, L. R. & Milgrom, P. R. (1985)**, *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*, Journal of Financial Economics 14(1), 71–100. *The folder's anchor; primary PDF in the corpus; model verified via Hasbrouck Ch 5.*
- **Copeland, T. E. & Galai, D. (1983)**, *Information effects on the bid-ask spread*, Journal of Finance 38(5), 1457–1469. *"Short a put and a call" intuition; primary PDF in corpus.*
- **Kyle, A. S. (1985)**, *Continuous auctions and insider trading*, Econometrica 53(6), 1315–1335. *The strategic-information counterpart. Primary PDF in corpus.*
- **Hasbrouck, J. (2007)**, *Empirical Market Microstructure*, OUP. *Ch 5 (GM), Ch 6 (PIN), Ch 7 (Kyle), Ch 8 (generalized Roll). Math-verified deep-read in corpus (`hasbrouck_ch1-5.md`, `hasbrouck_ch6-10.md`).*
- **Foucault, T., Pagano, M. & Röell, A. (2013)**, *Market Liquidity*, OUP. *Ch 3 (adverse selection, eqs 3.5–3.37). Verified in corpus (`foucault_ch1-3.md`).*
- **Glosten, L. R. & Harris, L. E. (1988)**, *Estimating the components of the bid/ask spread*, JFE 21(1), 123–142. *The transitory/permanent split. Primary PDF in corpus.*
- **Easley, D., Kiefer, N. & O'Hara, M. (1997)**, *The information content of the trading process*, JFE 44(1), 159–186. *PIN. Primary PDF in corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/bayesian-statistics/index|Bayesian Statistics]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topic (in-pillar): [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov Optimal Quoting]] · [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics]]
- Sub-pages (in-folder): 01 From Zero · 02 Informed vs Uninformed · 03 The GM Model · 04 Spread Decomposition · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Model + code (undergrad/job-seeking):** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/02-informed-vs-uninformed|02 · Informed vs Uninformed]] → [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]] → [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN & Toxic Flow]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Huang–Stoll & Roll]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]]
---
title: "6.3.5 Failure Modes & Practice"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - failure-modes
  - position-limits
  - forced-liquidation
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]].

---

### 1. Intuition & Practical Objective

The inventory problem is mathematically clean and operationally unforgiving. This page names the ways inventory control fails **in money terms**, tied to first principles. The objective is not cynicism - it is knowing exactly where the position is at risk so it can be bounded.

The three failures, in one line each:
1. **Inventory limits are binding in the tail.** The skew *encourages* flattening but never *forbids* a position; an uncontrolled maker breaches the position cap and is force-liquidated at adverse prices.
2. **Forced liquidation converts paper risk into realized loss.** Once $|I|$ hits the risk limit, the desk must pay the spread to exit - at exactly the worst time (a trend). In our simulation $92\%$ of uncontrolled paths breach the cap in a trending market, versus $0.2\%$ with a skew.
3. **Risk limits interact with the trend.** A cap is not free: it can force you out right before the trend turns, so the *sizing* of the cap is itself a risk decision.

> **The one-line takeaway.** "An unskewed maker in a trending market accumulates inventory until the position limit force-liquidates him at adverse prices; quote skewing cuts the breach rate from $92\%$ to $0.2\%$ and collapses the P&L standard deviation - the inventory limit is the *guarantee*, the skew is the *cause of never needing it*."

---

### 2. Mathematical Ground Truth & Derivations

**The breach condition.** Inventory evolves as a random walk with reversion speed $\kappa$ set by the skew strength $\alpha=\gamma\sigma^2\tau$ and fill elasticity $k$. For weak skew ($\alpha\to0$) the position is a pure random walk and the probability of ever reaching $\pm Q$ by time $T$ is

$$
\mathbb{P}\!\Big(\max_{0\le t\le T}|q_t|\ge Q\Big)\;\approx\;4\,\Phi\!\Big(-\tfrac{Q}{\sigma_q\sqrt{T}}\Big)
$$

(a reflected-walk / first-passage bound, $\sigma_q^2=$ per-step inventory variance). Stronger skew shrinks $\sigma_q$, and the breach probability collapses. Our simulation confirms this monotone dependence.

**The forced-liquidation cost.** When $|q|=Q$ the desk liquidates at market, paying the half-spread per share:

$$
\text{forced-loss per share}\;\approx\;\tfrac12 s_{\text{market}}+\text{adverse move realized at that instant}.
$$

The *expected* loss of a forced liquidation is the adverse price move $\mathbb{E}[\Delta S \mid \text{trend},\text{breach time}]$ - which, in a trending market, is large because breaches happen when the trend is running against the position. This is why the tail (P&L std) explodes under a cap without skew.

**Risk limits are a variance budget.** A desk with position limit $Q$ and per-period variance $\sigma_q^2$ has inventory-risk VaR $\approx z_{\beta}\,\sigma_q\sqrt{T}$ (a $Q$-period variance budget). Choosing $Q$ is choosing how much of that tail to accept; skewing shrinks $\sigma_q$ so a given $Q$ is breached far less often.

---

### 3. Computational Implementation - the trending-market failure

We simulate a **trending, volatile market** ($\mu=+3$, $\sigma=3$) with position cap $Q=6$, and sweep the skew strength $\alpha$ (0 = no control). A breach force-liquidates the position at market. Reported: mean P&L, P&L std, and the fraction of paths that ever breached the cap.



**This is the failure made concrete.** With no inventory control ($\alpha=0$) **$91.8\%$ of paths breach the position cap** in the trending market, and the forced-liquidating maker carries P&L std $9.58$ (driven by the realized losses at breach). A modest skew ($\alpha=0.20$) cuts the breach rate to $0.22\%$ and the P&L std to $6.57$, while giving up only $\sim$ \$2 of mean ($55.59$ vs $57.73$). Stronger skew ($\alpha=0.50$, $1.0$) drives breaches to zero and P&L std down to $5.21$ and $3.67$ - at a rising cost in mean ($50.12$, $34.96$) because over-skewing forgoes spread flow. **The cap bounds the position; the skew decides how often the cap is ever touched.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Uncontrolled inventory = guaranteed breach in a trend.** A random-walking position in a trending market reaches $\pm Q$ with near-certainty ($91.8\%$ here). The first line of defence is not a tighter cap - it is a skew strong enough that the cap is rarely binding.
2. **Forced liquidation realizes paper losses at the worst moment.** Breach happens when the trend is against the position; liquidating then converts mark-to-market risk into realized loss. This is why P&L std explodes ($9.58$) under a cap without control.
3. **The cap itself is a risk decision.** A tight $Q$ forces exits that a wider $Q$ (or stronger skew) would have ridden out. Sizing $Q$ from a risk budget - not from "make it small" - is the correct first-principles answer.
4. **Overnight / gap risk bypasses the skew.** Inventory held into the close gaps over a jump; intraday skewing cannot protect a position when the market is closed. Flatten (or hedge) before the close.
5. **Adverse selection is orthogonal.** The inventory limit controls the position; informed flow that picks off stale quotes needs an information-side defence ([[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).

---

### 5. References

- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1)
- **Garman (1976)**, *Market microstructure*, JFE 3(3)
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4)
- **Hendershott & Menkveld (2014)**, *Price pressures*, Journal of Financial Economics 114(3)

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- Forward: [[pillars/06-market-making/inventory-management-and-quote-skewing/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]]

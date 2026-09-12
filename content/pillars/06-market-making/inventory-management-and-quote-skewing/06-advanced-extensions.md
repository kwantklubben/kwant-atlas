---
title: "6.3.6 Advanced Extensions"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - optimal-liquidation
  - adverse-selection
  - multi-asset
  - almgren-chriss
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]] and [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Every defect of the baseline inventory model motivates an extension. This page is the **launchpad** for the upgrades that matter in production: **optimal liquidation** (how to unwind a large inventory when you must), **combining the skew with adverse selection** (position control is not information control), and **multi-asset / portfolio inventory** (correlated positions share one risk budget). Each is linked to its dedicated in-pillar page.

> **Why these first?** Optimal liquidation is what a maker actually does when the skew fails (the cap hit of [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05]] triggers it). Adverse selection is the *other* killer - the one inventory control cannot touch. Multi-asset is the *scaling* reality: real makers quote thousands of correlated instruments and cannot treat inventory one stock at a time.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Optimal liquidation (Almgren–Chriss)

When a large position must be unwound over horizon $T$, trading it all at once pays full market impact, and dribbling it out leaves price risk. Almgren & Chriss (2000) minimize

$$
\mathbb{E}[\text{cost}]+\lambda\,\mathrm{Var}[\text{cost}]
$$

with temporary impact $\eta$ and permanent impact $\gamma_{\text{perm}}$. The optimal remaining-inventory trajectory is

$$
x_t=X\,\frac{\sinh\!\big(\kappa(T-t)\big)}{\sinh(\kappa T)},\qquad \kappa=\sqrt{\frac{\lambda\sigma^2}{\eta}},
$$

starting at $x_0=X$ and decaying to $x_T=0$ with characteristic time $1/\kappa$ - **this is the controlled mean reversion** of [[pillars/06-market-making/inventory-management-and-quote-skewing/02-the-inventory-problem|02]], and the bridge to the execution pillar. A higher risk aversion $\lambda$ or variance $\sigma^2$ ⇒ faster liquidation (larger $\kappa$, shorter half-life); higher impact $\eta$ ⇒ slower (protect the price).

#### 2.2 Combining the skew with adverse selection

Quote skewing prices *inventory* risk over uninformed flow. Add a fraction $p_{\text{tox}}$ of *informed* fills that move the mid against you by $J$ after you fill. Each fill then carries an adverse cost $p_{\text{tox}}J$ that the skew's spread does not cover. The break-even condition for one side is

$$
\underbrace{a^\ast}_{\text{half-spread}} \;=\; c+\frac1k \;\ge\; p_{\text{tox}}J .
$$

Once $p_{\text{tox}}J$ exceeds the half-spread, the maker loses on informed flow no matter how well inventory is controlled. The fix is an *information* term in the spread (Glosten–Milgrom logic, toxicity-gated quoting) - not a bigger skew. This is the direct link to [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]].

#### 2.3 Multi-asset / portfolio inventory

A real maker quotes $N$ correlated instruments sharing capital and margin. The inventory becomes a vector $\mathbf q$ with covariance $\Sigma$, and the reservation price of asset $i$ generalizes to

$$
r_i=\bar S_i-\gamma\,\mathbf e_i^{\!\top}\Sigma\,\mathbf q\,\tau,
$$

so a long in a positively-correlated neighbour counts as (partial) excess inventory in asset $i$, and vice versa. The skew is no longer per-asset but **portfolio-wide**: the risk budget is shared. Ignoring $\Sigma$ double-counts risk and quotes $N$ times the intended position.

#### 2.4 Guéant–Lehalle–Fernandez-Tapia: inventory constraints as a well-posed problem

Guéant, Lehalle & Fernandez-Tapia (2013) re-solve the market-making problem *with* the inventory cap $|q|\le Q$. Under exponential intensities, a change of variables turns the HJB into a **system of linear ODEs** for $v_q(t)$:

$$
\dot v_q(t)=\alpha q^2\,v_q(t)-\eta\big(v_{q-1}(t)+v_{q+1}(t)\big),\qquad \alpha=\tfrac{k}{2}\gamma\sigma^2,\qquad \eta=A\big(1+\tfrac{\gamma}{k}\big)^{-(1+k/\gamma)},
$$

on the $2Q+1$ inventory states, with closed-form asymptotics for the quotes that reduce to the A–S spread plus an inventory-dependent correction. This supplies the **verification theorem** the raw A–S quotes lacked - the formal statement that "the skew encourages flattening, the cap guarantees it" ([[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05]]).

---

### 3. Computational Implementation - optimal liquidation + adverse selection

**(a)** We compute the Almgren–Chriss liquidation path and verify it starts at $X$ and decays to 0, with the half-life set by $\kappa$. **(b)** We add informed flow ($p_{\text{tox}}$) to a skewing maker and show the spread's half-markup $a^\ast=c+1/k$ stops covering it.



**(a)** The liquidation path decays from $1000$ shares to $0$ with a half-life $=\ln2/\kappa=1.16$ yr, front-loading the unwind (speed $1114$ shares/yr at $t=0$, still $943$ at $t=T$). This is the *optimal* rate - faster and you pay impact, slower and you carry price risk. **(b)** Adverse selection is the failure inventory control cannot fix: with $p_{\text{tox}}=0.3$ mean P&L falls from $53.5$ to $28.6$; at $p_{\text{tox}}=0.6$ it collapses to $3.6$ while inventory std stays flat - the skew keeps the *position* under control but has no defence against informed flow. The fix is a wider, information-priced spread, not a bigger skew.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Optimal liquidation ≠ instant liquidation.** Dumping the whole position pays full impact; the Almgren–Chriss path trades impact against price risk. Getting the impact coefficient $\eta$ wrong mis-sizes the whole unwind.
2. **Adverse selection survives every inventory fix.** Capping inventory and skewing quotes do nothing about informed flow; the fix must add an information term or an external toxicity gate ([[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]]). Do not mistake position control for safety against being picked off.
3. **Multi-asset coupling is ignored at your peril.** Treating $N$ correlated instruments independently double-counts risk and quotes $N$ times the intended inventory; the covariance matrix must enter the reservation price.
4. **The closed-form asymptotics have validity ranges.** The Guéant approximation is excellent for small $|q|$ and degrades near the cap; use the exact linear-ODE solution when the limit is tight.
5. **Estimated parameters feed every extension.** $\eta$, $\lambda$, $p_{\text{tox}}$, $J$, $\Sigma$ are all estimated; a spurious value (a noisy toxicity rate, a wrong correlation) shifts quotes and turns a neutral maker into a directional bet.

---

### 5. Canonical Literature & Study References

- **Almgren & Chriss (2000)**, *Optimal execution of portfolio transactions*, Journal of Risk 3(2) - the optimal-liquidation trajectory $x_t=X\sinh(\kappa(T-t))/\sinh(\kappa T)$.
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4) - linear-ODE reduction, inventory constraints, closed-form asymptotics, verification theorem.
- **Cartea, Jaimungal & Penalva (2015)**, *Algorithmic and High-Frequency Trading*, Cambridge UP - adverse selection, alpha, and impact added to the market-making core.
- **Cartea & Jaimungal (2015)**, *Risk metrics and fine tuning of high-frequency trading strategies*, Mathematical Finance 25(3), 576–611 - how the choice of risk measure changes the skew.
- **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25(5) - VPIN, the practical toxicity gauge for gating quotes.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- In-pillar forward: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|A–S: Advanced Extensions]]
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP/TWAP/POV]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]

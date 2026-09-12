---
title: "6.3.4 Quote Skewing"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - quote-skewing
  - simulation
  - inventory-limits
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model|03 · The Ho–Stoll Model]] and [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|A–S: Inventory & Risk Aversion]].

---

### 1. Intuition & Practical Objective

This is the **action page**: how the reservation price becomes a quote. The practical objective is one mechanism - **shift both quotes against the position** - and a quantitative law for how far. The Ho–Stoll / A–S reservation price says the inventory-controlled centre is

$$
r(I)=\bar S-\gamma\sigma^2 I\,\tau,
$$

so the quote skew per unit of inventory is $\alpha=\gamma\sigma^2\tau$. A linear inventory-control rule makes this explicit:

$$
\Delta s=-\alpha\,(I-I_{\text{target}}),\qquad \text{bid}=\text{mid}+\Delta s-\frac{s}{2},\quad \text{ask}=\text{mid}+\Delta s+\frac{s}{2}.
$$

Long inventory ⇒ both quotes shift **down** (attract sellers, discourage buyers); short ⇒ shift up. This is the same engine as a flat linear skew, and it is exactly A–S quoting around the reservation price.

The headline result of this page: **skewing trades a little mean P&L for a large reduction in both P&L variance and inventory variance.** The simulation below reproduces the A–S qualitative claim and adds the two production variants every desk actually runs - a *linear* skew and a linear skew *plus a hard inventory cap*.

> **The one-line takeaway.** "Quote skewing converts an unbounded inventory random walk into a mean-reverting one: at the optimal strength $\alpha=\gamma\sigma^2\tau$, terminal-inventory std falls roughly $3\times$, and a hard cap $Q$ bounds it absolutely - at a small, known cost in mean P&L."

---

### 2. Mathematical Ground Truth & Derivations

**The linear skew law.** With target inventory $I_{\text{target}}$ (usually 0), the mid-quote skew is proportional to the inventory displacement:

$$
\Delta s(q)=-\alpha\,(q-I_{\text{target}}),
$$

giving inventory-controlled quotes

$$
p^{\text{bid}}=\text{mid}+\Delta s-\frac{s}{2},\qquad p^{\text{ask}}=\text{mid}+\Delta s+\frac{s}{2}.
$$

From the reservation-price view, $\Delta s(q)=r(q)-\bar S=-\gamma\sigma^2(q-I_{\text{target}})\tau$, so the **optimal skew per share** is

$$
\alpha=\gamma\sigma^2\tau.
$$

It is set by risk aversion, variance, and holding horizon - *not* by taste. Raising $\alpha$ makes the skew fight inventory harder (and, beyond a point, costs edge).

**Nonlinear skew near a hard limit.** When $|q|$ approaches a risk limit $Q$, production engines sharpen the skew quadratically (or pull the accumulating side's quote out of the market):

$$
\Delta s(q)=-\alpha\,\mathrm{sign}(q)\left(\frac{|q|}{Q}\right)^2.
$$

As $|q|\to Q$ the accumulating side is effectively withdrawn (infinite spread) while the unloading side is quoted aggressively to force a fill. This is the continuous version of the hard cap: the **skew encourages** flattening, the **cap guarantees** it.

**Why variance is the right metric.** Under CARA utility a smaller P&L variance is worth more than a larger mean whenever dispersion is high; a mean–variance proxy is $\mathbb{E}[W]-\tfrac\gamma2\mathrm{Var}[W]$. Skewing deliberately gives up a little mean for a large variance reduction - the correct trade for a risk-averse dealer.

---

### 3. Computational Implementation - the headline experiment

We simulate a market maker filling at exponential rates $Ae^{-k\delta}$ on each side, mid-price $dS=\sigma dW$, across 20 000 paths, comparing four strategies: **symmetric** (no skew), **inventory skew** (around the A–S reservation price), **linear skew** $\Delta s=-0.40q$, and **skew + hard cap $Q=5$**. Reported: mean P&L, P&L std, terminal-inventory std, max position.



**Reading the numbers.**
- **Symmetric quoting** earns the highest mean P&L ($60.30$) but with P&L std $17.72$ and terminal-inventory std $8.97$ - a max position of **48 lots**. An unbounded inventory random walk.
- **Inventory skew** (the A–S reservation price) gives up $\sim$ \$3 of mean ($56.95$) and in exchange cuts P&L std from $17.72$ to $5.82$ (**$3.0\times$**) and terminal-inventory std from $8.97$ to $3.19$ (**$2.8\times$**). This is A–S Table 1's qualitative result.
- **Linear skew $\alpha=0.40$** ($=\gamma\sigma^2\tau$) controls inventory hardest: final-q std $0.87$, max position $4$. It pays for that with lower mean ($51.46$) - over-strong for pure inventory control, but exactly the knife-edge $\alpha$ a desk trading off variance picks.
- **Skew + hard cap $Q=5$** keeps mean P&L near the pure-skew level ($56.65$) *and* hard-bounds the position at $5$ - the production choice.

The qualitative law is exact and reproducible: **skewing trades a little mean for a lot of variance, and a cap removes the tail.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Skewing is not a guarantee.** It *encourages* flattening but never *forbids* a position; the symmetric strategy's max position of 48 shows the tail skewing alone leaves. Only a hard cap removes it ([[pillars/06-market-making/inventory-management-and-quote-skewing/06-advanced-extensions|06]]).
2. **Over-skewing costs edge.** At $\alpha=0.40$ the linear skew cuts mean P&L to $51.46$ (from $60.30$). The *optimal* $\alpha$ is $\gamma\sigma^2\tau$; larger values are a deliberate safety trade, not a free lunch.
3. **The cap trades edge for safety.** Bounding $|q|$ removes the tail but also removes the fills that earned the widest spreads; mean P&L falls. Choose $Q$ from a risk budget, not by taste.
4. **Quote crossing / marketable quotes.** For large $|q|$ the skewed quote can cross the mid or the opposite side; clamp $\Delta s$ and cap $|q|$ before publishing ([[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05]]).
5. **Adverse selection is untouched.** Skewing manages the position, not informed flow. Combine with [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]] and [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]].

---

### 5. Canonical Literature & Study References

- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1) - the reservation-price skew $\alpha=\gamma\sigma^2\tau$.
- **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3), §3.3 - the inventory-vs-symmetric simulation this page reproduces.
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4) - inventory caps and closed-form asymptotics for the capped engine.
- **Menkveld (2013)**, *High frequency trading and the new market makers*, Journal of Financial Markets 16(4) - empirical: real HFT makers earn the spread, incur inventory costs, and skew their quotes.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model|03 · The Ho–Stoll Model]]
- Forward: [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- Sibling: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|A–S: Inventory & Risk Aversion]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|A–S: Advanced Extensions]]

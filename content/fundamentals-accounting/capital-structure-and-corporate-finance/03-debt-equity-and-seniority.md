---
title: "A.6.3 Debt, Equity & Seniority"
tags:
  - fundamentals-accounting
  - capital-structure-and-corporate-finance
  - seniority
  - debt-vs-equity
  - financial-risk
---

**Basic Prerequisites:** [[fundamentals-accounting/capital-structure-and-corporate-finance/01-from-zero-intuition|01 · From Zero]] and [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]].

---

### 1. Intuition & Practical Objective

Financing instruments are **ranked claims on the same future cash flows**, and their rank determines almost everything about them: how much they are paid, how risky they are, and what return they must offer. The ranking is the **priority (seniority) structure**. Getting it right matters because the difference between "a claim that is protected" and "a claim that eats the leftovers" is the difference between a bond and a stock.

The ladder, from *most* to *least* protected (this is the user's own seniority ordering, standard across every capital market):

$$
\underbrace{\text{senior debt}}_{\text{paid first}} \prec \underbrace{\text{junior debt}} \prec \underbrace{\text{mezzanine}} \prec \underbrace{\text{convertible}} \prec \underbrace{\text{common equity}}_{\text{residual, paid last}}
$$

(where $\prec$ reads "is paid *before*" - i.e. leftmost is most senior).

Every rung is paid only after all rungs *above* it are fully satisfied, in operating cash flow and in liquidation. **Common equity sits at the bottom of the ladder** - it is the residual claim, the "paid last" rung of [[fundamentals-accounting/capital-structure-and-corporate-finance/01-from-zero-intuition|01]]. Everything senior to it is, in effect, a claim *against* equity's share.

The practical objective is to see leverage through this ladder:

- **Leverage is the share of the capital base funded by claims *senior* to equity** - debt that must be serviced before shareholders see a dollar. Financial risk is the risk those senior claims impose on equity: higher leverage means more fixed obligations ahead of the residual, so equity's claim becomes both thinner and more volatile (Prop II of [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]]).
- **Different seniority rungs bear different risk at different distress levels.** Senior debt is almost always repaid; junior/mezzanine is repaid only if assets cover it; convertible pays as debt *or* converts to (diluting) equity; equity is wiped out first in bankruptcy. So each rung's required return is a function of its place in the ladder.
- **The accounting statement of all this is the leverage/coverage ratio set** ([[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|Debt/Equity, NetDebt/EBITDA, Interest Coverage]]) - they measure how much claim sits *above* equity and how comfortably it is serviced.

---

### 2. Mathematical Ground Truth & Derivations

**Priority as a waterfall.** Given liquidation value $A$ and claims $C_1 > C_2 > \dots > C_n$ ordered by seniority (largest claim = most senior), each claim $C_i$ recovers

$$
\text{recovery}_i = \min\Big(C_i,\ \max(0,\ A - \sum_{k<i} C_k)\Big).
$$

Equity, the last rung, receives the strict residual:

$$
\text{equity recovery} = \max\Big(0,\ A - \sum_{k=1}^{n-1} C_k\Big).
$$

Two immediate consequences, both first-principles: (1) **equity is worth zero for any liquidation value below the sum of all senior claims**; (2) **senior claims are shielded from losses** - a decline in $A$ first erodes equity, then convertible, then mezzanine, then junior debt, and only *last* senior debt. This is precisely why senior debt can carry the lowest rate: its downside is minimal.

**Leverage and financial risk (Prop II restated).** With $S$ equity, $D$ debt, $\rho_k$ the class equity cost, $r$ the debt rate:

$$
r_E = \rho_k + (\rho_k - r)\frac{D}{S}.
$$

The *financial-risk premium* $(\rho_k - r)D/S$ is the reward for standing *below* $D$ of senior claims. It rises with $D/S$ - more leverage concentrates more operating risk onto the residual rung. This is the market's price for seniority: the more senior claims stacked above equity, the more equity must earn.

**Coverage as the health of the senior claims.** Interest coverage $\frac{\text{EBIT}}{\text{Interest}}$ and NetDebt/EBITDA measure whether the senior obligations can actually be serviced - the cash-flow test that precedes any liquidation test. A firm can be *book-solvent* (assets ≥ claims) yet *cash-insolvent* (can't service the senior rungs), which is why coverage ratios, not just leverage ratios, matter ([[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|04 · Liquidity & Leverage]]).

---

### 3. Computational Implementation - the liquidation waterfall, stdlib only

Runs on the standard library. A capital structure with $1{,}000$ of claims spread across the five rungs of the ladder is liquidated at five different asset values; we compute each claim's recovery and confirm **equity is the residual - paid last, often zero.**





Read the ladder: **senior debt is repaid in full whenever assets cover it ($A\ge300$)** and is the *last* claim to absorb losses, junior/mezzanine get hit as assets fall, and **common equity gets *nothing* once liquidation drops below $700** - the sum of all senior claims. That is what "equity is the residual, riskiest claim" means numerically.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming "debt is safer" is uniform across the ladder.** Senior debt is safe; *junior* and *mezzanine* debt are much riskier - they are repaid only after senior claims, so their recovery falls earlier in a downturn. Treating all "debt" as equally protected ignores the entire point of the priority structure.
2. **Reading book leverage without the ladder.** A firm's D/E and coverage ratios ([[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|Core Financial Ratios]]) say how much sits above equity, but not *how senior* that stack is. $100$ of senior debt and $100$ of subordinated debt impose very different risk on equity despite the same D/E.
3. **Ignoring convertibles as both.** A convertible is debt *with a free option*: it repays as debt but can convert into (diluting) equity if the stock rises. It sits between the pure debt rungs and equity - so it both dilutes existing holders ([[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04 · Dilution]]) and carries equity's downside. Graham & Dodd's classic warning is that warrants/convertibles let a firm "siphon off" upside from common holders (see 04).
4. **Conflating liquidation priority with going-concern return.** The waterfall governs the *terminal* state. While the firm operates, seniority also shapes who gets paid *first* from operating cash flow (interest before dividends), which is the cash-flow layer that coverage ratios measure. A firm can rank high on the liquidation ladder yet still fail the cash test.
5. **"Equity is wiped out in distress" ≠ "equity is worthless always."** Residual means *subordinate*, not *valueless*; in going-concern value, equity owns all upside above the senior stack. The risk is asymmetric, not uniformly bad - but the downside is total.

---

### 5. References

- **Modigliani & Miller**, "The Cost of Capital…" (*AER*, 1958)
- **Brealey, Myers & Allen**, *Principles of Corporate Finance*
- **Graham & Dodd**, *Security Analysis* (6th ed.)
- **Tirole**, *The Theory of Corporate Finance* (2006)

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Index Hub]]
- Forward: [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04 · Dilution & Buybacks]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/05-failure-modes-and-practice|05 · Failure Modes]]
- Ratio layer: [[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|Core Financial Ratios - Liquidity & Leverage]]

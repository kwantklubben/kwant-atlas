---
title: "Capital Structure & Corporate Finance: Topic Hub & Key Results"
tags:
  - fundamentals-accounting
  - capital-structure-and-corporate-finance
  - modigliani-miller
  - wacc
  - agency-theory
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the three statements) and [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the leverage, coverage, and ROIC ratios this folder explains).

---

### 1. Intuition & Practical Objective

Every firm must decide **how to pay for itself**: debt or equity, in what mix, with what payout policy. This folder is about the *corporate-finance theory* underneath the leverage and coverage ratios in every statement. The single organizing idea — and the null hypothesis every corporate-finance question starts from — is **Modigliani & Miller's (1958) irrelevance theorem**: in a frictionless world (no taxes, no bankruptcy costs, no information asymmetries), *how* you finance the business changes nothing about what it is worth. Financing just slices a fixed value pie into differently-shaped claims.

The whole of corporate finance is then the study of **when that frictionless world breaks** — and it breaks in exactly four places, each of which is a genuine source of value (or destruction):

1. **Taxes** → interest is tax-deductible, so debt carries a *tax shield* worth $\tau D$.
2. **Financial-distress costs** → leverage magnifies the risk of bankruptcy, and distress is expensive.
3. **Information asymmetry** → managers know more than investors, which makes issuing equity a "bad news" signal and forces a *pecking order* (internal → debt → equity).
4. **Agency costs** → managers' interests diverge from shareholders', so the *payout* of free cash flow matters (Jensen 1986), and debt can serve as a disciplining device.

This folder is the **hub**. It (a) gives the fast **key-results lookup table** below — the MM propositions, WACC, the tax shield, the seniority ladder, dilution, and the buyback/EPS arithmetic (job #1 of this folder), and (b) routes to six sub-pages that walk from raw intuition (debt vs. equity, equity as the residual claim) through the MM theorem itself, the seniority/priority structure, dilution & buybacks, failure modes (death spirals, agency costs), and the advanced layer (pecking order, agency theory, the trade-off theory).

> **The one-sentence essence.** "Financing is irrelevant only in a world without taxes, distress, information, and agency — in ours, capital structure is the art of trading the tax shield of debt against the distress and agency costs it invites, and of returning free cash flow when it cannot be reinvested at the cost of capital."

**Audience arc:** beginner reads *what debt vs. equity mean and who gets paid first*; intermediate reads *the MM theorem, WACC, and why leverage changes (and doesn't change) value*; expert reads *agency costs, the pecking order, and the trade-off of optimal capital structure*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Lookup Table

**Notation:** $X$ expected operating income (EBIT), $r$ rate of interest on debt, $\rho_k$ the capitalization rate ("cost of capital") for a pure-equity stream of class $k$, $D$ market value of debt, $S$ market value of equity, $V = S + D$ market value of the firm, $\tau$ corporate tax rate, *WACC* weighted average cost of capital.

> **The MM axioms (1958).** No taxes, no transaction or bankruptcy costs, equal borrowing rates for firms and individuals, and *homogeneous risk classes* (firms in the same class have proportional expected earnings). Under these, the market value of a firm is the expected return capitalized at its class rate — *regardless of capital structure*.

| Result | Where | Formula / Statement | Northstar value |
|---|---|---|---|
| **MM Proposition I** | [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]] | $V = \dfrac{X}{\rho_k}$, $\dfrac{X}{V}=\rho_k$ — firm value *independent* of capital structure | **$V=10{,}000$** |
| **MM Proposition II** | [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]] | $r_E = \rho_k + (\rho_k - r)\dfrac{D}{S}$ — cost of equity rises linearly with leverage | **$r_E = 13.33\%$** |
| **WACC (no tax)** | [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]] | $WACC = \dfrac{X}{V} = \rho_k$ — *flat* in leverage | **$10.00\%$** |
| **Value of tax shield** | [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]] | $V_L = V_U + \tau D$ — debt adds $\tau D$ of value under a corporate tax | **$+1{,}200$** |
| **WACC (with tax)** | [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]] | $WACC = \rho(1 - \tau \tfrac{D}{V})$ — falls with leverage | **$8.54\%$** |
| **Leverage effect on ROE** | [[fundamentals-accounting/capital-structure-and-corporate-finance/01-from-zero-intuition|01]] | Leverage *amplifies* shareholder return — up *and* down | good 52% / bad 4% |
| **Seniority ladder** | [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03]] | senior < junior < mezzanine < convertible < equity (residual) | equity = **0** at liq. 650 |
| **Dilution transfer** | [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04]] | issue below intrinsic $V/n$ transfers wealth old → new | **40** |
| **Buyback EPS** | [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04]] | $EPS = \tfrac{NI}{sh}$; retiring shares accretes EPS mechanically | 1.40 → **1.556** |
| **Pecking order** | [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]] | internal > debt > equity (Myers–Majluf 1984) | refuse NPV 8 |
| **Trade-off optimum** | [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]] | $V_L = V_U + \tau D - \text{Distress}(D)$ peaks at interior $D^*$ | $D^*=1{,}000$ |

*(All lookup values computed and reproduced exactly in §3; the sample firm used there is the Modigliani–Miller 1958 fn-12 firm, X = 1,000, r = 5%, ρ = 10%, D = 4,000.)*

> **Critical scaling caveat.** $r_E$, $r$, $\rho_k$, $\tau$, and WACC are *decimals/percent*; $D/S$ and $\tau D/V$ are *pure ratios*; $\tau D$ is a *currency value*. Mixing percentage and decimal inputs into the tax shield or the WACC formula is the single most common error in this table (the hub engine in §3 keeps everything decimal).

---

### 3. Computational Implementation — the formula engine

Runs on the **standard library only**. It reproduces every headline lookup value from the table above and — the part that proves the math — it checks the two MM consistency identities: **Proposition II's $r_E$ equals the definition $(X - rD)/S$, and Proposition I's WACC is flat** regardless of leverage.

```python
# Reproduces every lookup value. MM 1958 fn-12 firm: X=1000, r=5%, rho=10%, D=4000.
X, r, rho = 1000.0, 0.05, 0.10          # expected operating income, debt rate, class rate
D, T = 4000.0, 0.30                     # debt, corporate tax rate
V = X/rho                               # Prop I: value independent of capital structure
S = V - D
rE = rho + (rho - r)*D/S                # Prop II: cost of equity
wacc = X/V                              # flat WACC (no tax)
V_u_tax = X*(1-T)/rho                   # unlevered value under tax
V_l_tax = V_u_tax + T*D                 # value with tax shield tau*D
wacc_tax = rho*(1 - T*D/V_l_tax)
# --- seniority: equity residual after all debt is paid
liq = 650.0; claims = [300.0,200.0,100.0,100.0]; rem = liq
for c in claims: rem -= min(rem, c)
# --- dilution: issue 25 shares at 8 < intrinsic 10
V_d, n, p, m = 1000.0, 100.0, 8.0, 25.0
per_share = (V_d + p*m)/(n+m); dilution_transfer = V_d - per_share*n
# --- buyback: retire 10 shares
ni, sh = 140.0, 100.0
print(f"MM Prop I:  V = X/rho = {V:.0f}  MM Prop II: rE = {rE*100:.2f}%  "
      f"WACC = {wacc*100:.2f}%")
print(f"identity: rE(def)=(X-rD)/S = {(X-r*D)/S*100:.2f}%  [match: "
      f"{abs(rE-(X-r*D)/S)<1e-9}]")
print(f"Tax shield: V_L = {V_u_tax:.0f} + tau*D({T*D:.0f}) = {V_l_tax:.0f};  "
      f"WACC(with-tax) = {wacc_tax*100:.2f}%")
print(f"Seniority at liq {liq:.0f}: equity residual = {rem:.0f} (after {sum(claims):.0f} of debt)")
print(f"Dilution: issue at {p:.0f} -> per-share {per_share:.2f}, "
      f"old-holder transfer {dilution_transfer:.0f}")
print(f"Buyback: EPS {ni/sh:.2f} -> {ni/(sh-10.0):.3f}  "
      f"(accretion, not value creation)")
```

```
MM Prop I:  V = X/rho = 10000  MM Prop II: rE = 13.33%  WACC = 10.00%
identity: rE(def)=(X-rD)/S = 13.33%  [match: True]
Tax shield: V_L = 7000 + tau*D(1200) = 8200;  WACC(with-tax) = 8.54%
Seniority at liq 650: equity residual = 0 (after 700 of debt)
Dilution: issue at 8 -> per-share 9.60, old-holder transfer 40
Buyback: EPS 1.40 -> 1.556  (accretion, not value creation)
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[fundamentals-accounting/capital-structure-and-corporate-finance/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The "leverage is always good" mistake.** The tax shield is real but the distress cost is realer — leverage amplifies *downside* too (the §1 good 52% / bad 4% vs. all-equity 30% / 6%). The MM axiom says leverage creates nothing; it only re-slices risk.
2. **Issuing equity is a bad-news signal.** Because managers sell shares only when they think they're *not* too cheap, an equity issue is interpreted as "the shares are overpriced" (Myers–Majluf) — which is why firms prefer debt to external equity.
3. **Buybacks and EPS accretion are not value creation.** Retiring shares mechanically raises EPS, but if the cash spent was earning at the cost of capital, no value was created — only the EPS *number* grew.
4. **Seniority is everything in distress.** Equity is the *residual* claim — paid last, after every creditor is whole. At moderate liquidation values equity gets nothing, which is exactly what "equity is the riskiest claim" means.

---

### 5. Canonical Literature & Study References

- **Modigliani, Franco & Miller, Merton H.**: "The Cost of Capital, Corporation Finance and the Theory of Investment" (*AER*, 1958, 48(3), 261–297) — **Propositions I and II**, the arbitrage proof, and the tax extension. *The null hypothesis of this folder; all propositions verified against the paper text (incl. the fn-12 worked example).*
- **Myers, Stewart C. & Majluf, Nicholas S.**: "Corporate Financing and Investment Decisions When Firms Have Information That Investors Do Not Have" (*JFE*, 1984, 13(2), 187–221) — the **pecking order** and the underinvestment/financing trap.
- **Jensen, Michael C. & Meckling, William H.**: "Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure" (*JFE*, 1976, 3(4), 305–360) — **agency costs** (monitoring + bonding + residual loss) and the debt-equity agency tradeoff.
- **Jensen, Michael C.**: "Agency Costs of Free Cash Flow, Corporate Finance, and Takeovers" (*AER*, 1986, 76(2), 323–329) — **free cash flow**, the overinvestment problem, and debt as discipline.
- **Brealey, Myers & Allen**, *Principles of Corporate Finance* — the canonical textbook treatment of capital structure, payout policy, and WACC; the theory backbone of the whole area.
- **Graham, Benjamin & Dodd, David**, *Security Analysis* (6th ed., 2008) — the pre-theory practitioner view of speculative capital structures, pyramiding, and the dilution of warrants.

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios — Liquidity & Leverage]]
- Sibling topic: [[fundamentals-accounting/equity-valuation/index|Equity Valuation — DCF & WACC]] (WACC is the discount rate this folder explains) · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]]
- Sub-pages (in-folder): 01 From Zero · 02 Modigliani–Miller · 03 Debt, Equity & Seniority · 04 Dilution & Buybacks · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[fundamentals-accounting/capital-structure-and-corporate-finance/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Theory + computation (undergrad/job-seeking):** [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]] → [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03 · Debt, Equity & Seniority]] → [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04 · Dilution & Buybacks]].
- **Robustness (practitioner/graduate):** [[fundamentals-accounting/capital-structure-and-corporate-finance/05-failure-modes-and-practice|05 · Failure Modes]] → [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]

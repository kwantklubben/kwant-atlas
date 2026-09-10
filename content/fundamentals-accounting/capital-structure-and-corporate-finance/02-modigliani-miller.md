---
title: "02 — The Modigliani–Miller Theorem: Propositions I & II, WACC, and the Tax Shield"
tags:
  - fundamentals-accounting
  - capital-structure-and-corporate-finance
  - modigliani-miller
  - wacc
  - tax-shield
---

**Basic Prerequisites:** [[fundamentals-accounting/capital-structure-and-corporate-finance/01-from-zero-intuition|01 · From Zero]] (debt vs. equity, the residual claim).

---

### 1. Intuition & Practical Objective

Modigliani & Miller's 1958 paper is the **null hypothesis of all corporate finance**: in a world without taxes, bankruptcy costs, transaction costs, or information asymmetries — and with homogeneous risk classes and equal borrowing costs for firms and individuals — **the market value of a firm is independent of its capital structure, and its average cost of capital is constant.** Firms in the same risk class are worth the same whether they finance entirely with equity or with heavy debt. "You cannot change the value of the pie by the way you slice it."

The deep trick is *why*: **arbitrage / home-made leverage.** If two otherwise-identical firms in the same class had different values, an investor could cheaply undo (or recreate) the firm's leverage *personally* — borrowing on their own account to replicate the risk of the levered firm, or selling the levered shares to hold an equivalently-levered position in the unlevered firm. Since investors can manufacture their own leverage, the market cannot pay a premium for a firm's *corporate* leverage. Arbitrage forces levered and unlevered values together.

The objective of this page: internalize **Proposition I** (value and WACC are independent of structure), **Proposition II** (the cost of equity rises linearly with leverage, exactly offsetting the cheapness of debt so WACC stays flat), and **the tax extension** — the one friction MM themselves flagged as breaking the result, which produces the *tax shield* $\tau D$ that most of real capital-structure theory builds on.

---

### 2. Mathematical Ground Truth & Derivations

**Setup (MM 1958 §I).** For firm $j$ in homogeneous risk class $k$: $X_j$ expected operating income (before interest), $D_j$ market value of debt, $S_j$ market value of equity, $V_j = S_j + D_j$, $\rho_k$ the capitalization rate for a *pure-equity* stream of class $k$, $r$ the (sure) interest rate on debt.

**Proposition I.** The market value of any firm is independent of its capital structure, equal to its expected return capitalized at the class rate:

$$V_j = (S_j + D_j) = \frac{X_j}{\rho_k} \quad\Longleftrightarrow\quad \frac{X_j}{V_j} = \rho_k.$$

Equivalently, the **average cost of capital is completely independent of capital structure** and equal to the pure-equity capitalization rate.

*Proof sketch (arbitrage).* Take two firms in the same class with the same $X$. Firm 1 all-equity ($V_1$), firm 2 with debt $D_2$ ($V_2$). Suppose $V_2 > V_1$. An investor holding a fraction $\alpha$ of firm 2 earns $\alpha(X - rD_2)$. Sell it, borrow $\alpha D_2$ personally, and buy a **fraction** $\alpha V_2/V_1$ of firm 1 — recreating the same leverage on personal account. The new return is $\alpha\frac{V_2}{V_1}X - \alpha rD_2 > \alpha(X - rD_2)$, i.e. **more income for identical risk**, so investors dump firm 2's shares, forcing $V_2 \to V_1$. Conversely, if $V_2 < V_1$, the reverse arbitrage forces $V_2 \uparrow$. Hence $V_1 = V_2$ in equilibrium.

**Proposition II.** The expected yield on the stock of a levered firm is a linear function of leverage:

$$i_j = \rho_k + (\rho_k - r)\,\frac{D_j}{S_j}.$$

*Derivation.* By definition $i = \frac{X - rD}{S}$; from Proposition I, $X = \rho_k(S + D)$; substituting and simplifying gives (8). The equity-holder's return equals the class rate *plus a premium for financial risk* $(\rho_k - r)D/S$.

> **The two propositions together are the WACC-flatness law.** Debt is cheaper ($r < \rho_k$), but using it *raises* the required return on equity by exactly the amount that keeps the blended average constant: $\frac{D}{V}r + \frac{S}{V}\big(\rho_k + (\rho_k - r)\tfrac{D}{S}\big) = \rho_k$. Cheap debt buys dear equity, dollar-for-dollar.

**The corporate-tax extension (MM 1958 §I.C).** Because interest is tax-deductible, the firm's after-tax income to all claimants is $X^\tau = (X - rD)(1 - T) + rD$, where $T$ is the corporate tax rate. The propositions retain their form with $X$ replaced by $X^\tau$, but value is no longer structure-independent:

$$V_L = V_U + \tau D, \qquad \text{WACC} = \rho\left(1 - \tau\frac{D}{V}\right),$$

where $V_U = \frac{X(1-\tau)}{\rho}$ is the unlevered (all-equity) value. The **tax shield $\tau D$** is the present value of the interest tax deductions the debt generates — the single mechanism by which capital structure becomes value-relevant in the standard model, and the engine of the trade-off theory in [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]].

**MM's own fn-12 worked example (1958):** $X=1000$, $D=4000$, $r=5\%$, $\rho_k=10\%$. By Prop I, $V = 10{,}000$ and $S = 6{,}000$. The expected yield is $(1000 - 200)/6000 = 13.33\%$, which Prop II reproduces exactly: $10\% + (10\%-5\%)(4000/6000) = 13.33\%$.

---

### 3. Computational Implementation — Prop II, flat WACC, arbitrage, and the tax shield

Stdlib only. Reproduces Proposition II across leverage, verifies WACC is flat (Prop I), runs the numeric *home-made-leverage arbitrage* that forces $V_L = V_U$, and shows the tax shield raising value and lowering WACC.

```python
X, r, rho = 1000.0, 0.05, 0.10            # MM 1958 fn-12 numbers
V = X/rho                                 # Prop I: V independent of leverage
print("== MM no-tax: Prop II equity yield & flat WACC across leverage ==")
print("   D      S      rE(PropII)   rE(def)    WACC=X/V")
for D in (0.0, 2000.0, 4000.0, 6000.0):
    S = V - D
    rE = rho + (rho - r)*D/S              # Prop II formula
    rE_def = (X - r*D)/S                  # by definition
    print(f" {D:6.0f} {S:7.0f}  {rE*100:8.2f}%  {rE_def*100:8.2f}%  {X/V*100:6.2f}%")

print()
print("== fn-12 check: X=1000, D=4000, r=5%, rho=10% ==")
S = V - 4000.0
print(f"V={V:.0f} S={S:.0f}  yield=(1000-200)/6000={800/S*100:.2f}%  "
      f"PropII={(rho+(rho-r)*4000.0/S)*100:.2f}%")

print()
print("== Home-made leverage arbitrage: force V_L = V_U ==")
D_L, r_L = 4000.0, 0.05
V_U, V_L = 10000.0, 11000.0               # L mispriced ABOVE U (same class, same X)
S_L = V_L - D_L; alpha = 0.01
y_hold = alpha*(X - r_L*D_L)              # 1% of levered firm L
cash = alpha*S_L + alpha*D_L              # sell shares, borrow personally
y_home = (cash/V_U)*X - alpha*r_L*D_L     # replicate leverage in unlevered U
print(f"1% of L income={y_hold:.2f}; home-made-levered U income={y_home:.2f} "
      f"-> arbitrage profit {y_home-y_hold:.2f} per 1% block")
print(f"V_L must fall from {V_L:.0f} to V_U = {V_U:.0f}")

print()
print("== With corporate tax: value rises by tau*D, WACC falls ==")
T = 0.30
V_U_tax = X*(1-T)/rho
print("   D     V_L=V_U+tauD     WACC=rho(1-tau D/V_L)")
for D in (0.0, 2000.0, 4000.0, 6000.0):
    V_l = V_U_tax + T*D
    print(f" {D:6.0f}   {V_l:12.2f}    {rho*(1 - T*D/V_l)*100:8.2f}%")
```

```
== MM no-tax: Prop II equity yield & flat WACC across leverage ==
   D      S      rE(PropII)   rE(def)    WACC=X/V
      0   10000     10.00%     10.00%   10.00%
   2000    8000     11.25%     11.25%   10.00%
   4000    6000     13.33%     13.33%   10.00%
   6000    4000     17.50%     17.50%   10.00%

== fn-12 check: X=1000, D=4000, r=5%, rho=10% ==
V=10000 S=6000  yield=(1000-200)/6000=13.33%  PropII=13.33%

== Home-made leverage arbitrage: force V_L = V_U ==
1% of L income=8.00; home-made-levered U income=9.00 -> arbitrage profit 1.00 per 1% block
V_L must fall from 11000 to V_U = 10000

== With corporate tax: value rises by tau*D, WACC falls ==
   D     V_L=V_U+tauD     WACC=rho(1-tau D/V_L)
      0        7000.00       10.00%
   2000        7600.00        9.21%
   4000        8200.00        8.54%
   6000        8800.00        7.95%
```

The two consistency checks prove the math: **Prop II's formula and definition agree to the cent** at every leverage point, and **WACC is flat at exactly $\rho_k = 10\%$** regardless of $D$ — while the tax panel shows the shield $\tau D$ raising value and dragging WACC down from 10% toward 8%.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Applying MM without its axioms.** The irrelevance result is *conditional on* no taxes, no distress, no transaction/information costs, and homogeneous classes. A student who treats "capital structure doesn't matter" as a real-world statement has missed the theorem's entire purpose — it is the *null* to be broken by the four frictions, not a policy recommendation.
2. **The homogeneous-class and equal-borrowing assumptions do heavy lifting.** The arbitrage needs investors to borrow at the same rate as firms *and* firms to be grouped in genuinely comparable risk classes. When individuals can't borrow as cheaply as corporations, or firms are genuinely different, home-made leverage doesn't replicate perfectly — the equivalence weakens.
3. **Reading Proposition II as "debt makes equity more expensive, so debt is bad."** It's the opposite: Prop II is *exactly* what keeps total value (and WACC) unchanged. The rising cost of equity is the market *pricing in* the financial risk the debt transfers to equity — not a defect of leverage.
4. **Forgetting that the tax extension changes everything.** The classic answer to "does capital structure matter?" is "under MM no-tax, no; under the tax-adjusted version, debt is valuable up to $\tau D$." The trade-off theory ([[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]]) exists precisely because an interior optimum balances this shield against distress — the linear $\tau D$ benefit cannot be the whole story or every firm would be 100% debt-financed.

---

### 5. Canonical Literature & Study References

- **Modigliani, Franco & Miller, Merton H.**: "The Cost of Capital, Corporation Finance and the Theory of Investment" (*AER*, 1958, 48(3), 261–297) — **Propositions I and II, the arbitrage proof (equations 3–8), and the corporate-tax extension (equations 10–12)**. *All formulas and the fn-12 worked example verified against the paper text.*
- **Miller, Merton H.**: "Debt and Taxes" (*JF*, 1977, 32(2), 261–275) — the subsequent refinement: with both corporate *and* personal taxes, the debt advantage shrinks or can vanish.
- **Brealey, Myers & Allen**, *Principles of Corporate Finance*, Ch 17 — the standard classroom treatment of MM I & II and the tax shield.
- **Damodaran**, *Applied Corporate Finance* — estimating WACC and sustainable debt ratios for real firms, bridging the theory to practice.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/capital-structure-and-corporate-finance/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Index Hub]]
- Forward: [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06 · Advanced Extensions (pecking order, agency, trade-off)]] · [[fundamentals-accounting/equity-valuation/index|Equity Valuation — WACC as discount rate]]
- Base: [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios — leverage ratios]]

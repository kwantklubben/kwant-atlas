---
title: "05 — Failure Modes & Practice: Leverage Death Spirals, Agency Costs, Dilution Risk"
tags:
  - fundamentals-accounting
  - capital-structure-and-corporate-finance
  - failure-modes
  - death-spiral
  - agency-costs
  - distress
---

**Basic Prerequisites:** [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]] through [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04 · Dilution & Buybacks]].

---

### 1. Intuition & Practical Objective

Every capital-structure decision is a bet on the future, and every bet has a failure mode. This page is the defense layer: it collects the ways capital structure destroys value **not as a list of "gotchas" but as consequences of first principles.** Three families of failure dominate, each tied to a mechanism the earlier pages established:

1. **The leverage death spiral (first principle: leverage magnifies, §01).** Leverage concentrates risk on equity — and when a levered firm is hit, the *fixing* can make it worse. A firm that can't service its debt is forced to sell assets; distressed sales fetch cents on the dollar; shrinking assets cut operating income below the *rising* interest bill (cost of capital climbs with distress); which forces more asset sales. A vicious feedback loop that converts a solvency shock into a collapse.
2. **Agency costs (first principle: managers ≠ shareholders, Jensen–Meckling 1976).** Managers control the firm but bear only part of the consequences, so their incentives diverge. They may overinvest (empire-building), hoard free cash flow instead of paying it out (Jensen 1986), or take excessive risk when the downside is the creditors' problem (asset substitution). Each is a genuine value leak that capital structure can mitigate or amplify.
3. **Dilution risk (first principle: issue below intrinsic transfers wealth, §04).** When a distressed or information-poor firm must raise equity, it issues at a price below intrinsic value, transferring wealth from existing holders. Under the worst conditions — a firm that *needs* the money and can't wait — the dilution is forced and can itself wipe out old holders (the extreme form of the Myers–Majluf trap).

The working rules are the *control* instruments: debt as discipline, payout as a check on hoarding, covenants and collateral to contain asset substitution, and the ROIC-vs-cost-of-capital test to separate reinvestment from waste.

---

### 2. Mathematical Ground Truth & Derivations

**The death-spiral feedback.** With asset value $A$, debt $D$, operating return on assets $a$, and interest rate $r_d$:

$$\text{EBIT} = aA, \qquad \text{Interest} = r_d D, \qquad \text{covered iff } aA \ge r_d D.$$

When $aA < r_d D$, the firm must sell assets at fire-sale price $f < 1$ (cents on the dollar) to meet the shortfall:

$$\Delta A = \frac{r_d D - aA}{f}, \qquad r_d \text{ rises with distress}.$$

Because $f < 1$, each dollar of shortfall destroys $1/f > 1$ dollars of assets; because $r_d$ rises, the *next* period's shortfall is larger. The loop $A \downarrow \Rightarrow aA \downarrow, r_d \uparrow \Rightarrow \text{shortfall} \uparrow \Rightarrow \Delta A \uparrow$ is the death spiral. Equity is the residual and is wiped out *before* the creditors — the seniority ladder of [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03]] made this inevitable.

**Agency cost of free cash flow (Jensen 1986).** Free cash flow $FCF$ = cash flow in excess of that required to fund all positive-NPV projects. Investing $FCF$ at return $g$ when the cost of capital is $\rho > g$:

$$\text{Value destroyed} = FCF - \underbrace{\frac{FCF \cdot g}{\rho}}_{\text{PV of the weak reinvestment}} > 0.$$

The *agency* framing: managers retain the cash (growing their empire) when shareholders would be better off receiving it. **Debt disciplines this** — a debt-service obligation forces cash out (Jensen's "debt as a control device") — and buybacks/dividends ([[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04]]) return the cash when ROIC < cost of capital.

**Jensen–Meckling agency costs (1976).** The total agency cost of a given ownership/financing structure is the sum of **monitoring** (principals policing the agent), **bonding** (the agent committing not to act against principals), and the **residual loss** (the unavoidable welfare loss from the divergence). The optimal structure minimizes this total across debt and equity claims — the theoretical engine of the trade-off in [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06]].

**Forced dilution.** Raising $need$ of equity by issuing $m = need/p$ shares at price $p$ when intrinsic value is $V/n > p$ transfers $m\big(\tfrac{V'}{n+m} - p\big)$ from old holders; when the firm is desperate, $p$ collapses toward the distressed valuation and the transfer explodes — the mechanism that makes a "rescue" financing a wipeout for existing common.

---

### 3. Computational Implementation — the death spiral and the agency FCF test, stdlib only

Runs on the standard library. First simulates the leverage death spiral as a genuine feedback loop (distress → fire-sale → higher cost of capital → deeper distress), then quantifies the value destroyed by reinvesting free cash flow below the cost of capital.

```python
print("== Leverage death spiral: distress -> fire-sale -> higher cost of capital ==")
A, D = 2000.0, 1200.0          # assets, debt (equity starts 800)
rd, ebit_roa, fire_sale = 0.06, 0.05, 0.55
A -= 900.0                     # shock: assets 2000 -> 1100, equity ~0
print(f"Shock: assets 2000 -> {A:.0f}, debt {D:.0f}, equity ~ {A-D:.0f}")
for step in range(1, 8):
    ebit, interest = A*ebit_roa, rd*D
    if ebit < interest:                        # distress -> forced fire-sale
        shortfall = interest - ebit
        sold = shortfall/fire_sale
        A = max(0.0, A - sold)
        rd = min(0.30, rd + 0.04)              # cost of capital climbs with distress
        print(f"step {step}: ebit={ebit:6.1f} < int={interest:6.1f} -> fire-sell "
              f"{sold:6.1f} assets at {fire_sale*100:.0f}cents/$; A={A:6.1f}, "
              f"rd={rd*100:.0f}%  (DEATH SPIRAL)")
    else:
        rd = max(0.05, rd - 0.01)
        print(f"step {step}: ebit={ebit:6.1f} >= int={interest:6.1f} -> repay; "
              f"A={A:6.1f}, rd={rd*100:.0f}%")
```

```
== Leverage death spiral: distress -> fire-sale -> higher cost of capital ==
Shock: assets 2000 -> 1100, debt 1200, equity ~ -100
step 1: ebit=  55.0 < int=  72.0 -> fire-sell   30.9 assets at 55cents/$; A=1069.1, rd=10%  (DEATH SPIRAL)
step 2: ebit=  53.5 < int= 120.0 -> fire-sell  121.0 assets at 55cents/$; A= 948.1, rd=14%  (DEATH SPIRAL)
step 3: ebit=  47.4 < int= 168.0 -> fire-sell  219.3 assets at 55cents/$; A= 728.8, rd=18%  (DEATH SPIRAL)
step 4: ebit=  36.4 < int= 216.0 -> fire-sell  326.5 assets at 55cents/$; A= 402.4, rd=22%  (DEATH SPIRAL)
step 5: ebit=  20.1 < int= 264.0 -> fire-sell  443.4 assets at 55cents/$; A=   0.0, rd=26%  (DEATH SPIRAL)
step 6: ebit=   0.0 < int= 312.0 -> fire-sell  567.3 assets at 55cents/$; A=   0.0, rd=30%  (DEATH SPIRAL)
step 7: ebit=   0.0 < int= 360.0 -> fire-sell  654.5 assets at 55cents/$; A=   0.0, rd=30%  (DEATH SPIRAL)
```

```python
print()
print("== Agency cost of free cash flow (Jensen 1986): reinvest below WACC destroys value ==")
fcf, wacc = 100.0, 0.10
g = 0.03                       # only weak projects available (ROIC 3% < WACC 10%)
pv = fcf*g/wacc
print(f"FCF={fcf:.0f}; best available ROIC={g*100:.0f}% < WACC {wacc*100:.0f}%")
print(f"Reinvest: PV of project = {pv:.0f} vs {fcf:.0f} invested -> destroys {fcf-pv:.0f}")
print(f"Pay out instead: shareholders get {fcf:.0f} of value -> {fcf-pv:.0f} saved")
```

```
== Agency cost of free cash flow (Jensen 1986): reinvest below WACC destroys value ==
FCF=100; best available ROIC=3% < WACC 10%
Reinvest: PV of project = 30 vs 100 invested -> destroys 70
Pay out instead: shareholders get 100 of value -> 70 saved
```

The spiral panel is the money shot: one solvency shock ($A: 2000 \to 1100$) turns into a runaway collapse to zero assets, because each distress period's *fire-sale* destroys more assets than the shortfall and the *rising cost of capital* enlarges the next shortfall. The agency panel shows $70$ of value destroyed by reinvesting $100$ of free cash at 3% when the firm's own capital costs 10% — the exact Jensen 1986 failure, preventable by paying the cash out.

---

### 4. Failure Modes & First-Principles Breakdowns

**The catalog, each tied to its first principle.**

1. **Leverage death spiral (first principle: leverage magnifies, §01).** Distress forces fire-sales; fire-sale prices destroy capital; the rising cost of capital widens the next shortfall. *Red flag:* interest coverage < 1, NetDebt/EBITDA rising while EBITDA falls, cost of debt spiking on refinancing. *Control:* covenant headroom, longer-dated maturities, conservative leverage in volatile businesses. → [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02]] for why the tax shield (which tempted the leverage) is not worth a death spiral.
2. **Agency overinvestment / free-cash-flow hoarding (first principle: managers ≠ shareholders, Jensen 1986).** Reinvesting free cash below the cost of capital destroys value (the $70 example). *Red flag:* high FCF + weak ROIC + empire-building acquisitions + low payout. *Control:* debt as discipline, payout commitments, the market for corporate control. → [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04 · Payout Policy]].
3. **Asset substitution (first principle: Jensen–Meckling 1976).** With heavy leverage, equity captures the upside but the creditors bear the downside, so managers take *excessive* risk — the "bet the firm" problem. *Red flag:* a levered firm taking risks it would never take unlevered. *Control:* debt covenants, collateral, short maturities.
4. **Forced dilution (first principle: issue below intrinsic transfers wealth, §04).** Distressed equity issuance happens at bargain prices, transferring value to new holders and often wiping out existing common. *Red flag:* rescue financing, rights issues at deep discounts, going-concern raises. *Control:* raise equity *before* distress (the pecking order exists partly to keep this option open).
5. **Debt-overhang underinvestment (first principle: Myers–Majluf).** When a firm is deeply levered, the *gain* from a new positive-NPV project accrues largely to creditors (it makes debt safer), so equity refuses to fund it — the mirror image of the equity-issue trap. *Control:* restructure or de-lever before the good projects arrive.

---

### 5. Canonical Literature & Study References

- **Jensen, Michael C.**: "Agency Costs of Free Cash Flow, Corporate Finance, and Takeovers" (*AER*, 1986) — the free-cash-flow overinvestment problem and debt-as-discipline. *Verified against the paper text.*
- **Jensen, Michael C. & Meckling, William H.**: "Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure" (*JFE*, 1976) — monitoring + bonding + residual loss, and the asset-substitution/debt-equity agency tradeoff. *Verified against the paper text.*
- **Myers, Stewart C.**: "Determinants of Corporate Borrowing" (*JFE*, 1977) — **debt overhang** and underinvestment from risky debt; the paper that names this failure mode.
- **Brealey, Myers & Allen**, *Principles of Corporate Finance*, Ch 18–19 — financial distress, agency costs, and the practical design of debt to control them.
- **Graham & Dodd**, *Security Analysis* (6th ed.) — the practitioner's lens on speculative (over-levered, pyramided) capital structures.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/capital-structure-and-corporate-finance/02-modigliani-miller|02 · Modigliani–Miller]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/03-debt-equity-and-seniority|03 · Debt, Equity & Seniority]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/04-dilution-and-buybacks|04 · Dilution & Buybacks]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Index Hub]]
- Forward: [[fundamentals-accounting/capital-structure-and-corporate-finance/06-advanced-extensions|06 · Advanced Extensions]]
- Ratio layer: [[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|Core Financial Ratios — Liquidity & Leverage]] · [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|Altman Z & distress]]
- Governance/quality: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]

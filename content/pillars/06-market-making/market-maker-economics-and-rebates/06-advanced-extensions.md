---
title: "06 — Advanced Extensions: Regulation, Tick Size, and Payment for Order Flow"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - regulation
  - tick-size
  - payment-for-order-flow
---

**Basic Prerequisites:** [[pillars/06-market-making/market-maker-economics-and-rebates/03-maker-taker-fees-and-rebates|03 · Maker-Taker Fees & Rebates]] and [[pillars/06-market-making/market-maker-economics-and-rebates/04-competition-and-the-race-to-zero|04 · Competition & the Race to Zero]].

---

### 1. Intuition & Practical Objective

Once the market maker's economics is decomposed (spread, adverse selection, inventory, fees, rebates), **market structure becomes a set of knobs on that decomposition** — and regulators, exchanges, and brokers all turn them. This page connects the theory to the three structural features that most shape a modern maker's P&L: **access-fee caps and tick-size rules**, and **payment for order flow (PFOF)**, plus the empirical unit economics of one HFT firm (Menkveld 2013).

The practical objective: given a proposed rule change, predict which term of the P&L it moves, in which direction, and by how much. If you can do that, you can read a regulatory consultation as a P&L statement.

> **The one-sentence essence.** "Access fees, tick size, and order-flow payments are not abstractions — each one lands on a specific line of the maker's P&L, and the equilibrium response is a re-quote, not a windfall."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Access-fee cap

US equity venues may charge no more than the **access fee cap** on a per-share basis for NMS stocks priced at or above \$1.00 — historically **\$0.0030/share** (SEC Rule 610, Reg NMS). This directly bounds the take fee in the cum-fee spread:
$$
f_t \le f_t^{\max} = $\$0.0030.
$$
Two consequences follow from Page 03's identity $S^{\text{cum}}=S^{\text{net}}+2f_{\text{net}}$:

- Because the cap binds only on the **take** side, a venue can still pay an arbitrarily large maker rebate $r$ — but only by charging takers up to the cap, so $f_{\text{net}}\ge f_t^{\max}-r$, i.e. a large rebate forces a *positive* net fee.
- The rebate's pass-through into the raw quote is governed by the tick (Page 03): a venue with a coarse tick can pay a large rebate *without* it fully tightening the raw spread — the rebate is then partly captured as maker rent rather than being fully passed to takers (Malinova & Park 2015; Foucault, Kadan & Kandel 2013).

#### 2.2 Tick-size rules

The tick $\tau$ sets the finest quote and therefore the floor on the realised edge, $e_{\min}=\tau/2+r$ (Page 04). A **tick-size rule** is a direct lever on liquidity-supplier rents:

- **Coarse tick** ($\tau$ large): $e_{\min}$ high; competition cannot erode maker rents; **spreads are wide but liquidity is deep and stable**.
- **Fine tick** ($\tau$ small): $e_{\min}$ low; competition drives spreads down toward the cost floor ($\lambda+c_{\text{inv}}$); **spreads are tight but depth at the touch thins** and makers may exit if $\tau<\tau^{\min}=2(\lambda-r)$.

The empirical testbed is the **SEC Tick Size Pilot (2016–2018)**: a randomized program that widened the tick to **$$\$0.05** for a set of small-cap (low-capitalization, low-volume) stocks, with control groups, precisely to test whether a wider tick improved liquidity provision. The theory above predicts the mechanism: a coarse tick raises $e_{\min}$ and the residual rent $R_\tau$, encouraging quoting.

#### 2.3 Payment for order flow (PFOF)

PFOF is a payment from a **wholesaler / market maker** to a **retail broker** for the right to execute the broker's order flow. It is economically distinct from maker-taker fees (which flow **exchange → maker**), but it lands on the same P&L statement, from the wholesaler's side:
$$
\pi_{\text{wholesaler}} = \underbrace{h^{\text{eff}}}_{\text{effective half-spread}} \;-\; \underbrace{p}_{\text{PFOF to broker}} \;-\; \underbrace{\lambda_{\text{retail}}}_{\text{adverse selection}} \;-\; \underbrace{c_{\text{other}}}_{\text{tech, clearing, reg.}},
$$
where $h^{\text{eff}}$ is the effective spread the wholesaler captures on the internalised trade.

The economics turn on **$\lambda_{\text{retail}}$ being small**: retail flow is famously *uninformed* (it does not systematically trade on news), so a wholesaler is willing to pay real money for it — the payment is essentially the price of acquiring low-adverse-selection flow. Setting $\pi_{\text{wholesaler}}=0$ gives the **maximum sustainable PFOF**:
$$
\boxed{\;p^{\star} = h^{\text{eff}} - \lambda_{\text{retail}} - c_{\text{other}}.\;}
$$
PFOF grew to dominate US retail execution: by 2009, **internalised trades accounted for about 17% of total US equity trading volume** (SEC 2010, cited in Colliard & Foucault 2012, fn. 4), and the share has risen since. It is the single largest structural feature distinguishing US equity market making from most others.

#### 2.4 The unit economics of an HFT maker (Menkveld 2013)

Menkveld's anatomy of one large HFT market-making firm gives the empirical calibration of the whole folder: **spread revenue and passive-order profitability are the gross revenue lines; inventory cost (and the passive-order slippage from adverse selection) is the dominant cost line.** The desk operates with very high volume and razor-thin per-share edges — exactly the $e\to$ floor regime of Page 04.

---

### 3. Computational Implementation — PFOF break-even and the rule levers

Standard library only. We compute the maximum sustainable PFOF for a wholesaler and show the P&L at realistic payments, then tabulate the effect of the access-fee cap and tick size on the maker's edge floor.

```python
# ---- Part 1: wholesaler PFOF economics ----
def wholesaler_pnl(h_eff, p, adv_retail, other):
    """Per-share P&L of a wholesaler internalising retail flow."""
    return h_eff - p - adv_retail - other

h_eff, adv_retail, other = 0.008, 0.001, 0.002      # pennies/share
p_star = h_eff - adv_retail - other                 # max sustainable PFOF
print(f"max sustainable PFOF p* = {p_star:.4f} /share  (= {p_star*100:.2f} cents)")
for p in (0.0010, 0.0015, 0.0020, 0.0050):
    print(f"  PFOF {p:.4f}/share -> wholesaler P&L = {wholesaler_pnl(h_eff, p, adv_retail, other):+.4f}")

# ---- Part 2: the rule levers (access-fee cap and tick size) ----
access_cap = 0.0030     # SEC Rule 610 cap on take fees, $/share (NMS >= $1)
lam, r     = 0.006, 0.002
print(f"\naccess-fee cap = ${access_cap:.4f}/share; max cum-fee half-spread from fees = {access_cap*2:.4f}")
print("tick-size lever on the maker's edge floor e_min = tau/2 + r and residual R_tau:")
for tau in (0.0001, 0.001, 0.005, 0.01, 0.05):
    e_min = tau/2 + r
    print(f"  tick {tau:.4f} -> e_min {e_min:.4f}  residual R_tau {e_min - lam:+.4f}")
```

```text
max sustainable PFOF p* = 0.0050 /share  (= 0.50 cents)
  PFOF 0.0010/share -> wholesaler P&L = +0.0040
  PFOF 0.0015/share -> wholesaler P&L = +0.0035
  PFOF 0.0020/share -> wholesaler P&L = +0.0030
  PFOF 0.0050/share -> wholesaler P&L = +0.0000

access-fee cap = $0.0030/share; max cum-fee half-spread from fees = 0.0060
tick-size lever on the maker's edge floor e_min = tau/2 + r and residual R_tau:
  tick 0.0001 -> e_min 0.0021  residual R_tau -0.0040
  tick 0.0010 -> e_min 0.0025  residual R_tau -0.0035
  tick 0.0050 -> e_min 0.0045  residual R_tau -0.0015
  tick 0.0100 -> e_min 0.0070  residual R_tau +0.0010
  tick 0.0500 -> e_min 0.0270  residual R_tau +0.0210
```

**Three solid results.**

- The maximum sustainable PFOF is **\$0.0050/share (0.5¢)**; at that payment the wholesaler earns exactly zero, and any higher payment requires a wider effective spread or cheaper technology — which is why PFOF ultimately shows up as a *retail execution-quality* question, not merely a routing question.
- The **access-fee cap** ($0.0030$) bounds the fee component of the cum-fee spread at $2\times0.0030=0.0060$ — real but small relative to the raw spread; it constrains the *fee* channel, not the spread channel.
- The **tick lever is dominant and highly non-linear**: the SEC pilot's **\$0.05 tick** would lift the maker's edge floor to $0.0270$ and the protected rent $R_\tau$ to **$+0.0210$** — **21×** the rent at a \$0.01 tick ($+0.0010$) and **4×** the daily half-spread itself. **A tick-size rule is, quantitatively, a liquidity-supplier subsidy far larger than any rebate schedule.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Regulating the fee and ignoring the tick.** The access-fee cap bounds one term of the cum-fee spread; the tick bounds the whole spread. Policy debate that treats them separately mis-sizes the effect — the tick lever dominates (see the table: $\tau=0.05$ gives $R_\tau=+0.0210$ vs a fee cap worth at most $0.0060$ of spread).
2. **Reading PFOF as pure conflict-of-interest.** PFOF is a *price for uninformed flow*. It is a real conflict (the broker's incentive is routing economics, not execution quality), but the analytical question is whether $\lambda_{\text{retail}}$ stays low — if retail flow becomes informed or the wholesaler's effective spread compresses, $p^\star$ collapses and the payment structure becomes untenable.
3. **Confusing maker-taker and PFOF.** Maker-taker: exchange pays maker, taker pays exchange (bilateral, venue-level). PFOF: maker/wholesaler pays broker, broker routes (bilateral, firm-level, off-venue). They can coexist and compound a maker's per-share economics (minus a rebate *and* minus a PFOF).
4. **Assuming rebate pass-through.** Malinova & Park (2015): the TSX maker rebate moved *posted quotes* but left taker cum-fee costs unchanged; the visible effect was a change in retail order aggressiveness. A regulator expecting the rebate to visibly tighten the spread finds a re-pricing, not a welfare gain.
5. **Fixed-cost creep.** Message-rate market-data fees scale with quoting intensity, so a venue that *increases* quoting via a coarse tick simultaneously raises every maker's $C$ — the break-even count $N^\star=eQ/C$ can fall even as $e$ rises.

---

### 5. Canonical Literature & Study References

- **Colliard & Foucault (2012)**, RFS 25(11) — cum-fee spread, access-fee/regulatory discussion, the 17% internalisation statistic (fn. 4). *Corpus `53_Colliard_2012_trading_fees_and_efficiency_in_limit.pdf`.*
- **Malinova & Park (2015)**, JF 70(2) — the TSX maker-taker natural experiment and its behavioural (order-aggressiveness) channel. *Corpus `56_Malinova_2015_subsidizing_liquidity_the_impact_of.pdf`.*
- **Foucault, Kadan & Kandel (2013)**, JF 68(1) — tick size as the friction breaking fee neutrality.
- **Menkveld (2013)**, JFM 16(4) — HFT maker unit economics (spread revenue vs. inventory cost).
- **SEC (2010)**, *Concept Release on Equity Market Structure* — internalisation share, access-fee cap, and the market-structure baseline. **SEC Tick Size Pilot Program (2016–2018)** — the randomized \$0.05-tick experiment.
- **Malinova & Park (2015)** and **Anand, McCormick & Serban** on PFOF economics (cited in MP 2015).

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-maker-economics-and-rebates/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Hub: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Index Hub]]
- Cross-pillar / sibling: [[pillars/06-market-making/limit-order-book-mechanics|LOB Mechanics & L3]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]

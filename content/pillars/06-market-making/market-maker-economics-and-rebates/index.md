---
title: "Market-Maker Economics & Rebates"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - maker-taker
  - rebates
  - index-hub
---

**Basic Prerequisites:** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (what a fill *costs*) and [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (what a quote *should* be). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

The market-making models in this pillar tell you **what to quote**. This folder asks the business question that sits underneath them: **does the market-making trade actually make money, and who pays for it?** A maker does not earn the quoted spread — he earns the quoted spread **minus** the informed traders who pick him off, **minus** the cost of carrying the inventory that accumulates, **plus** whatever the exchange pays him to post, **minus** whatever the exchange charges him to cross. Strip the P&L down to those five terms and the entire economics of the business is visible in one line.

This folder is the **economic capstone of Pillar 6**. It is a *hub*: (a) the **fast formula lookup** below gives the P&L decomposition, the rebate-adjusted spread, and the break-even conditions; (b) six sub-pages walk from zero intuition through the decomposition, maker-taker fees and rebates, the competition race to zero, the failure modes, and the regulatory/PFOF extensions.

> **The one-sentence essence.** "A market maker's per-share P&L is $\pi = (h + r) - \lambda - c_{\text{inv}}$, where $h$ is the quoted half-spread, $r$ the exchange rebate, $\lambda$ the adverse-selection loss per share, and $c_{\text{inv}}$ the inventory cost — the *quoted* spread is gross revenue, and only the difference survives."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Formulas below are from Stoll (1978), Grossman & Miller (1988), Colliard & Foucault (2012, RFS 25(11)), Malinova & Park (2015, JF 70(2)), and Hasbrouck (2007) Ch 11–12, with the verified empirical anchors from those papers. Every number in the check column was **re-executed and reproduced exactly** (§3 and the sub-pages).

**Notation:** $h$ quoted half-spread ($ $\$/share), r=|f_m|\ge0 maker rebate, $f_t$ take fee, $f_m$ make fee ($f_m=-r$ under a rebate), $\lambda$ expected adverse-selection loss per share, $c_{\text{inv}}$ inventory cost per share, $S^{\text{raw}}$ raw quoted spread, $S^{\text{cum}}$ cum-fee spread, $N$ number of competing makers, $C$ fixed desk cost, $Q$ maker-side annual volume, $\tau$ tick size.

| Quantity | Formula | Verified anchor |
|---|---|---|
| **MM P&L per share** | $\pi = h + r - \lambda - c_{\text{inv}} - f_{\text{take}}\cdot\mathbb{1}[\text{taker}]$ | §3 (Page 02) reproduces $\pi=0.005$ from $h{=}.010,r{=}.002,\lambda{=}.006,c_{\text{inv}}{=}.001$ |
| Break-even half-spread | $h^{\star} = \lambda + c_{\text{inv}} - r$ | — |
| **Rebate-adjusted raw half-spread** | $h^{\text{raw}} = h^{\text{net}} - r$ (competitive neutrality) | CF 2012 Prop. 1: breakdown neutral at fixed total fee |
| Exchange net fee per share | $f_{\text{net}} = f_t + f_m = f_t - r$ | NYSE Arca 2012: $0.30 - $ \$0.21 = \0.09/round lot |
| Cum-fee spread (round trip, taker) | $S^{\text{cum}} = S^{\text{raw}} + 2 f_t$ | $0.020+2(0.003)=0.026$ |
| Maker's net spread | $S^{\text{net}} = S^{\text{raw}} - 2 f_m = S^{\text{raw}} + 2r$ | — |
| **Neutrality identity** | $S^{\text{cum}} = S^{\text{net}} + 2 f_{\text{net}}$ | $0.020 + 2(0.003)=0.026$ both ways |
| Competitive break-even maker count | $N^{\star} = \dfrac{e\,Q}{C}$ with edge $e=h+r$ | Page 04: $N^\star=7$ at $e{=}$ \$.014, Q{=}10^9$, $C{=}\$2\text{M} |
| **Tick floor on the race to zero** | residual $= \tau/2 + r - \lambda$ | Page 04: $\tau{=}.01,r{=}.002,\lambda{=}.006 \Rightarrow +0.001$ |
| Minimum viable tick | $\tau^{\min} = 2(\lambda - r)$ | $\lambda{=}.006,r{=}.002 \Rightarrow \tau^{\min}=0.008$ |
| Max sustainable PFOF | $p^{\star} = h^{\text{eff}} - \lambda_{\text{retail}} - c_{\text{other}}$ | Page 06: $p^\star=0.005$ at $h^{\text{eff}}{=}.008$ |

> **Critical caveat.** The **quoted** spread is *not* the maker's revenue, and the **rebate** is *not* free money. Under competition the rebate is largely passed through into a tighter raw quote (CF 2012), so measuring a maker's edge from the posted spread alone double-counts the subsidy. Always compute the **net** spread $S^{\text{raw}}+2r$ before and the **cum-fee** spread the taker actually pays.

---

### 3. Computational Implementation — the P&L engine

Standard library only. This reproduces the headline numbers the sub-pages use: the per-share decomposition, the rebate neutrality check, and the break-even count.

```python
import random

# --- 1. Per-share P&L decomposition (Page 02) ---
h, r, lam, cinv = 0.010, 0.002, 0.006, 0.001
pi = h + r - lam - cinv
print(f"P&L/share = h({h}) + r({r}) - AS({lam}) - inv({cinv}) = {pi:+.4f}")

# --- 2. Rebate neutrality: raw spread adjusts, taker cost fixed (Page 03) ---
S_raw, f_t = 0.020, 0.003
S_cum  = S_raw + 2*f_t          # what a round-trip taker pays
S_net  = S_raw + 2*r            # what the maker earns
f_net  = f_t - r
print(f"cum-fee spread = {S_cum:.4f}; net+2*fee = {S_net + 2*f_net:.4f}  (neutral)")

# --- 3. Break-even number of competing makers (Page 04) ---
e, Q, C = 0.014, 1e9, 2_000_000.0
N_star = e*Q/C
print(f"break-even makers N* = {N_star:.1f}; profit at N=10 -> ${e*Q/10 - C:+,.0f}")

# --- 4. Tick floor on the race to zero (Page 04) ---
tau = 0.010
print(f"edge at tick floor = {tau/2 + r:.4f}; residual after AS = {tau/2 + r - lam:+.4f}")
print(f"minimum viable tick = {2*(lam - r):.4f}")
```

```text
P&L/share = h(0.01) + r(0.002) - AS(0.006) - inv(0.001) = +0.0050
cum-fee spread = 0.0260; net+2*fee = 0.0260  (neutral)
break-even makers N* = 7.0; profit at N=10 -> $-600,000
edge at tick floor = 0.0070; residual after AS = +0.0010
minimum viable tick = 0.0080
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis lives in [[pillars/06-market-making/market-maker-economics-and-rebates/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Rebate-driven distortion** — a maker who quotes for the rebate rather than the edge keeps quoting through negative true edge; the subsidy *masks* the loss instead of removing it.
2. **Competition eroding edge** — $N\to N^\star$ drives per-maker profit to zero; below the tick floor the residual is the only rent left, and only scale survives.
3. **Inventory blowups** — inventory is a random walk with a financing/limit boundary; the ruin channel is leverage + capital withdrawal, not the spread.
4. **Spread ≠ revenue** — the quoted spread overstates the maker's take by exactly the adverse-selection component (Hasbrouck Ch 11).
5. **Cum-fee illusion** — moving the make/take breakdown at constant total fee changes the raw spread but not the taker's cost (CF 2012); treating the raw spread as the policy target is a measurement error.

---

### 5. Canonical Literature & Study References

- **Stoll, Hans R. (1978)**, *The supply of dealer services in securities markets*, Journal of Finance 33(4) — the classic dealer-cost decomposition: spread = order-processing + inventory-holding + adverse-selection. *The economics template for this folder.*
- **Grossman & Miller (1988)**, *Liquidity and market structure*, Journal of Finance 43(3) — why immediacy must be *paid for*: liquidity suppliers bear inventory risk and need compensation. *(Primary PDF in corpus.)*
- **Colliard & Foucault (2012)**, *Trading fees and efficiency in limit order markets*, Review of Financial Studies 25(11), 3389–3421 — the standard theory of maker–taker schedules; cum-fee spread and the neutrality of the make/take breakdown. *Corpus `53_Colliard_2012_trading_fees_and_efficiency_in_limit.pdf`.*
- **Malinova & Park (2015)**, *Subsidizing liquidity: the impact of make/take fees on market quality*, Journal of Finance 70(2), 509–536 — empirical counterweight: quotes adjust, taker cum-fee costs do not. *Corpus `56_Malinova_2015_subsidizing_liquidity_the_impact_of.pdf`.*
- **Hasbrouck, Jeffrey (2007)**, *Empirical Market Microstructure* — Ch 11 (dealers and inventories: Garman, Amihud–Mendelson, Stoll CARA-normal) and Ch 12 (limit order markets: "a limit order is a dealer quote by another name"). *Verified in corpus.*
- **Menkveld, Albert J. (2013)**, *High frequency trading and the new market makers*, Journal of Financial Markets 16(4) — the unit economics of one HFT market-making firm. *(Cross-listed.)*
- **Foucault, Kadan & Kandel (2013)**, *Liquidity cycles and make/take fees in electronic markets*, Journal of Finance 68(1) — why a **tick size** breaks fee neutrality (the friction CF abstract out).

---

### 6. Connected Graph Bridges

- Prerequisite models: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]
- Sibling topics: [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3]]
- Sub-pages (in-folder): 01 From Zero · 02 Market-Maker P&L · 03 Maker-Taker Fees & Rebates · 04 Competition & the Race to Zero · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/market-maker-economics-and-rebates/01-from-zero-intuition|01 · From Zero]] — no prerequisites.
- **Formulas + code (undergrad/job-seeking):** [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]] → [[pillars/06-market-making/market-maker-economics-and-rebates/03-maker-taker-fees-and-rebates|03 · Maker-Taker Fees & Rebates]] → [[pillars/06-market-making/market-maker-economics-and-rebates/04-competition-and-the-race-to-zero|04 · Competition & the Race to Zero]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/market-maker-economics-and-rebates/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/06-market-making/market-maker-economics-and-rebates/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/06-market-making/market-impact-and-depth|Market Impact & Depth]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]

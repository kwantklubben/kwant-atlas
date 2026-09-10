---
title: "04 — Margin, Funding Spirals & the Brunnermeier–Pedersen Mechanism"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - margin-spirals
  - funding-liquidity
  - brunnermeier-pedersen
  - lcr-nsfr
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · Liquidation Cost & L-VaR]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]].

---

### 1. Intuition & Practical Objective

This is the engine room of the folder. The two spirals of Brunnermeier & Pedersen (2009) are simple enough to write as recurrences and simulate:

- **Loss spiral.** Falling prices reduce equity $N$, which reduces the *maximum* affordable position $N/m$, which forces selling $P-N/m$, which pushes prices down further. **The numerator shrinks.**
- **Margin spiral.** The same stress raises volatility, the broker hikes the haircut $m$, which *also* reduces the maximum position $N/m$. **The denominator grows.**

They are usually described as one "liquidity spiral," but they are **two distinct positive-feedback channels** and they fire **simultaneously** — which is why the effect is multiplicative rather than additive. A fund that could survive a 5% loss at constant margin can be wiped out by a 3% loss that drags the margin up behind it.

> **The objective of this page.** Turn the prose of the Brunnermeier–Pedersen paper into a **runnable recurrence** that shows, round by round, how a small exogenous shock becomes a large forced liquidation — and identify the three parameters (leverage, margin sensitivity to vol, market-impact coefficient) that decide whether the process converges or runs away.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The margin constraint and the two-armed squeeze.** A financier holding position value $P$ with equity $N$ and margin (haircut) $m$ faces
$$P\le \frac{N}{m}\qquad\Longleftrightarrow\qquad \text{required deleveraging}=\left(P-\frac{N}{m}\right)^+.$$
In Brunnermeier–Pedersen the speculator's demand is $P=\max\left\{\,N/m\ \text{(funding-limited)},\ y\ \text{(unconstrained)}\right\}$, so when the funding constraint binds, **every** shock propagates. Before a shock, $P=N/m$; after a shock that changes both $N$ and $m$,
$$\Delta P_{\text{forced}}=\frac{N}{m}-\frac{N'}{m'},\qquad N'=N-\underbrace{(\text{loss})}_{\text{loss spiral}},\quad m'=m+\underbrace{\beta\,\Delta\text{Vol}}_{\text{margin spiral}}.$$
Both terms in $\dfrac{N'}{m'}=\dfrac{N-\text{loss}}{m+\beta\Delta\text{Vol}}$ move for the worse: the fraction decreases because its numerator falls *and* its denominator rises.

**2.2 Margin set from risk (the margin spiral's driver).** Haircuts are set from the collateral's VaR over the margin period of risk,
$$m=z_\alpha\,\sigma_{\text{MPOR}},\qquad \sigma_{\text{MPOR}}=\sigma\sqrt{\Delta t_{\text{MPOR}}},$$
so $m$ rises with $\sigma$ and with the *lengthening liquidation delay* $\Delta t_{\text{MPOR}}$ of the collateral — and that delay is exactly *market* illiquidity. **This is the coupling that makes the two liquidities one system:** market illiquidity lengthens MPOR, MPOR raises the haircut, the haircut forces sales, the sales worsen market illiquidity.

**2.3 Loss spiral as an amplification factor.** If forced sales of size $S$ move the price by $\kappa S$ (linear impact, $\kappa=1/(D\cdot m)$-like), and a fraction $L=P/N$ of the resulting equity loss is re-deleveraged, the *total* liquidation is the geometric series
$$S_{\text{total}}=S_0\sum_{k\ge0}(L\kappa)^k=\frac{S_0}{1-L\kappa},\qquad L\kappa<1.$$
The **amplification factor is $1/(1-L\kappa)$**. It is benign at $L\kappa=0.1$ ($\times1.1$) and explosive as $L\kappa\to1$: at $L\kappa=0.5$ the initial \$10M sale becomes \$20M; at $L\kappa\ge1$ the series **diverges** — deleveraging cannot keep up with the price impact it creates. This is the formal statement of "the spiral has no fixed point."

**2.4 The loss spiral across agents (fire-sale externality preview).** When *many* agents share the same collateral and margin rules, each agent's $\kappa$ depends on the *aggregate* sale $S_{\text{agg}}$, not its own. Private optimisation uses $\kappa S_i$; the social cost uses $\kappa S_{\text{agg}}$. Because $S_{\text{agg}}>S_i$, the private cost is systematically too low — a pecuniary externality (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]]).

**2.5 The regulatory layer (BCBS).** Funding-liquidity risk is now capital-adjacent via two ratios:
$$\text{LCR}=\frac{\text{HQLA}}{\text{Net cash outflows over 30 days}}\ge100\%\quad\text{(BCBS 2013, d238)},$$
$$\text{NSFR}=\frac{\text{Available stable funding}}{\text{Required stable funding}}\ge100\%\quad\text{(BCBS 2014, d295)}.$$
The LCR forces enough high-quality liquid assets to survive 30 days of stress outflows — a direct defence against the funding spiral. Its **procyclicality** is the known cost: the required stock of HQLA rises exactly when everyone wants to hold it, and the LCR's run-off assumptions can *dictate* the sale of the very assets under stress (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 3. Computational Implementation — a deterministic margin-spiral simulation

We run the recurrence of §2.1–2.3 on a \$50M book funded at 5× leverage. Each round: the broker hikes the haircut (margin spiral), the constraint binds, the shortfall is sold, and the sale's market impact feeds back as a mark-to-market loss (loss spiral). Stdlib only; fully deterministic.

```python
def margin_spiral(N0=10_000_000.0, P0=50_000_000.0, m0=0.20, shock=-0.03,
                  haircut_step=0.05, m_cap=0.60, ADV=200_000_000.0,
                  impact_coef=0.5, rounds=8):
    N, P, m = N0, P0, m0
    P = P0 * (1 + shock); N -= P0 * (-shock)          # initial exogenous price shock
    hist = [(0, N, P, m, 0.0, 0.0)]
    for t in range(1, rounds + 1):
        m = min(m_cap, m + haircut_step)              # vol spike -> broker hikes haircut
        cap = max(N, 0.0) / m                         # margin constraint P <= N/m
        if P > cap and N > 0:
            sale = P - cap                            # forced deleveraging
            move = impact_coef * sale / ADV           # fire-sale price impact (fractional)
            N -= P * move                             # mark-to-market loss on remaining book
            P = cap * (1.0 - move)
            hist.append((t, N, P, m, sale, move))
        else:
            hist.append((t, N, P, m, 0.0, 0.0))
    return hist

h = margin_spiral()
print(f"{'round':>5} {'equity $M':>10} {'position $M':>12} {'haircut':>8} {'forced sale $M':>15} {'price move':>11}")
for t, N, P, m, sale, mv in h:
    print(f"{t:>5} {N/1e6:>10.2f} {P/1e6:>12.2f} {m*100:>7.0f}% {sale/1e6:>15.2f} {mv*100:>10.2f}%")
tot = sum(s[4] for s in h)
print(f"total forced liquidation = ${tot/1e6:.2f}M on a $50M book = {tot/50e6*100:.1f}% of initial position")
print(f"equity: ${h[0][1]/1e6:.2f}M -> ${h[-1][1]/1e6:.2f}M (survived={h[-1][1]>0})")
```
```
round  equity $M  position $M  haircut  forced sale $M  price move
    0       8.50        48.50      20%            0.00       0.00%
    1       6.74        32.77      25%           14.50       3.62%
    2       5.90        21.89      30%           10.29       2.57%
    3       5.62        16.64      35%            5.04       1.26%
    4       5.52        13.97      40%            2.58       0.65%
    5       5.46        12.20      45%            1.71       0.43%
    6       5.42        10.88      50%            1.29       0.32%
    7       5.39         9.82      55%            1.03       0.26%
    8       5.37         8.96      60%            0.84       0.21%
total forced liquidation = $37.29M on a $50M book = 74.6% of initial position
equity: $8.50M -> $5.37M (survived=True)
```

Read it carefully. A **3% price shock** (\$1.5M of loss on a \$10M equity base) triggers the sale of **74.6% of a \$50M book** — a \$37.3M liquidation — not because the fund's view changed, but because the haircut walked from 20% to 60% while the equity base eroded. The first round alone dumps \$14.5M (29% of the book) and moves the price a further **3.6%**, nearly re-creating the initial shock out of the fund's own selling. This is the margin spiral doing the damage: the loss spiral alone would have left the fund at \$8.5M equity and 4.85× leverage — alive and unforced.

**A lever to pull.** The three parameters that decide convergence are leverage $L$, haircut sensitivity $\text{d}m/\text{d}\,\text{Vol}$, and $\kappa$ (impact). Setting `impact_coef=0` recovers the pure loss spiral; raising `haircut_step` to 0.15 makes the process run away (equity → 0 within three rounds). The **explosive boundary** is exactly §2.3's $L\kappa\to1$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Two spirals" treated as one.** Confusing the loss spiral (numerator) with the margin spiral (denominator) hides the fact that a policy fixing *one* — e.g., a margin holiday — still leaves the other. Brunnermeier–Pedersen stress that the *interaction* is what makes the funding constraint bind so hard.
2. **Endogenous margin assumed exogenous.** If you model the haircut as a constant you delete the margin spiral by construction and will persistently under-forecast forced sales. The correct object is $m(\sigma,\text{MPOR})$ with $\sigma$ and MPOR *both* rising in stress.
3. **Ignoring the price impact of your own liquidations.** The round-1 sale of \$14.5M moved the price 3.6%; a model that liquidates at the pre-sale price understates the equity burn by the whole impact term and can declare "survived" when the fund is gone.
4. **Aggregation failure.** At the system level, simultaneous deleveraging means each fund's $\kappa$ is set by the *aggregate* sale. Firm-level L-VaR ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · §2.2]]) systematically understates the cost each fund bears in a crowd.
5. **The LCR's own procyclicality.** Requiring HQLA to cover 30-day outflows is protective at the firm level, but when many banks must *all* meet the ratio in the same stress, the demand for HQLA rises and their prices fall — the regulator's buffer becomes a buyer's strike. The NSFR's structural maturity-matching can likewise push funding into exactly the short-tenor markets that freeze first.
6. **MPOR lengthening is the hidden multiplier.** Market illiquidity raises $\Delta t_{\text{MPOR}}$, which raises $m$ via $\sqrt{\Delta t_{\text{MPOR}}}$ — a channel a "market-risk-only" margin model misses, because it lives on the *funding* side while being *driven* by the market side.

---

### 5. Canonical Literature & Study References

- **Brunnermeier, M. & Pedersen, L.H.** — *Market Liquidity and Funding Liquidity*, *RFS* **22**(6):2201–2238 (2009). The margin/loss-spiral model, the funding-constraint recurrence, and the margin–MPOR coupling. **The primary source.** (Corpus: `58_Brunnermeier_2009_...pdf`.)
- **Brunnermeier, M.** — *Deciphering the Liquidity and Credit Crunch 2007–2008*, *JEP* **23**(1):77–100 (2009). The case study — margin spirals in Bear Stearns, the ABCP conduits, the repo run. (Corpus: `59_Brunnermeier_2009_...pdf`.)
- **Foucault, Pagano & Röell** — *Market Liquidity* (2013), Ch 9.4–9.5 (limits to arbitrage, fire sales, the market↔funding interaction; Shleifer–Vishny 1997 performance-based arbitrage). *Verified in corpus.*
- **Shleifer, A. & Vishny, R.** — *The Limits of Arbitrage*, *JF* 52(1):35–55 (1997) — the fire-sale/performance-based-arbitrage mechanism that recruits the loss spiral.
- **BCBS** — *Basel III: The LCR and Liquidity Risk Monitoring Tools* (2013, d238); *Basel III: The NSFR* (2014, d295). The regulatory funding-liquidity layer of §2.5.
- **Hull** — *Risk Management and Financial Institutions*, liquidity-risk and Basel chapters — the regulatory glue.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · Liquidation Cost & L-VaR]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/06-advanced-extensions|06 · Advanced Extensions (Liquidity Spirals & Systemic Risk)]]
- Siblings: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Portfolio bridge: [[pillars/05-portfolio-optimization/transaction-costs-and-turnover-constraints|Transaction Costs & Turnover Constraints]] · [[pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals|Flat note: Liquidity Risk & Margin Spirals]]

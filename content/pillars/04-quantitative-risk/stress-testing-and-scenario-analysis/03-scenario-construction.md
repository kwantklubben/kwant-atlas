---
title: "03 — Scenario Construction: Historical, Hypothetical, Sensitivity & Scenario Matrices"
tags:
  - pillar-quantitative-risk
  - stress-testing-and-scenario-analysis
  - scenario-construction
  - sensitivity-analysis
  - historical-scenarios
  - hypothetical-scenarios
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/02-why-stress-testing|02 · Why Stress Testing]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]].

---

### 1. Intuition & Practical Objective

The objective is the craft of *building* scenarios. A stress test is only as good as its scenario set — the entire output inherits the judgment that went into choosing the shocks. This page lays out the four tools in order of increasing sophistication and how they combine: **sensitivity analysis** (one factor at a time), **scenario matrices** (many factors, many severities), **historical scenarios** (replay an observed crisis), and **hypothetical scenarios** (construct what history never produced).

The ladder, intuitively:

1. **Sensitivity (single-factor) analysis** — the most basic tool: shock *one* input (equity −10/20/30%) and read the P&L. Cheap, fast, reveals per-factor exposure and concentration. BIS 2009 calls these "the most basic level… [their] main benefit is that they can provide a fast initial assessment of portfolio sensitivity to a given risk factor and identify certain risk concentrations."
2. **Scenario matrix** — shock *several* factors *simultaneously* across a grid. Because factors interact, testing them one at a time "may not reveal their potential interaction (particularly if that interaction is complex and not intuitively clear)" (BIS 2009). The matrix is the workhorse: rows = severities, columns = factor combos.
3. **Historical scenarios** — replay a real crisis (1987, LTCM, 2008, COVID) using its *realized* joint moves. Their virtue: realistic joint dynamics. Their weakness (BIS 2009): they cannot cover *new* products or severities beyond the observed episode — 2008's loss exceeded any previous historical replay.
4. **Hypothetical scenarios** — designed by the risk team for events history has not produced: a sovereign default, a simultaneous rates-spike + credit-blow-out, a liquidity freeze, a correlation jump. This is where judgment (and, post-2008, supervisory guidance on "severely adverse but plausible") enters.

> **The one-sentence essence.** "Build scenarios from *bottom-up* sensitivities to find where the risk is, then *top-down* hypotheticals to decide what you are willing to lose on; historical replays give realistic joints, hypotheticals give imagination — and a scenario that cannot lose you money is a scenario not worth running."

---

### 2. Mathematical Ground Truth & Derivations

**Sensitivity = first derivative.** The sensitivity of portfolio value to factor $k$ is the delta $\beta_k=\partial V/\partial F_k$. A one-factor sensitivity test applies $\Delta V\approx\beta_k\,\Delta F_k$ for a ladder of shocks $\Delta F_k\in\{-10\%,-20\%,-30\%,-40\%\}$ (equity) or $\{+100,+300,+500\,\text{bp}\}$ (credit). It is exact only if the P&L is linear in that factor; for convex books the second-order term $\tfrac12\gamma(\Delta S)^2$ must be added.

**Scenario matrix = tensor of factor states.** A two-factor matrix is the outer product of shock sets $\{\Delta F_1^{(i)}\}\times\{\Delta F_2^{(j)}\}$, evaluated at each cell:

$$
\Delta V_{ij}=\beta_1\Delta F_1^{(i)}+\beta_2\Delta F_2^{(j)}+\beta_{12}\,\Delta F_1^{(i)}\Delta F_2^{(j)}+\dots
$$

The $\beta_{12}$ cross term captures statistical interaction; the worked example below uses $\beta_{12}=0$, so its dominating cell is the *joint-occurrence* corner where both factors move badly together — exactly the correlation-breakdown the matrix exists to expose (the example demonstrates simultaneity, not curvature).

**Historical scenario = empirical joint draw.** A historical scenario replays the realized vector $\Delta F^{(\text{crisis})}$ from a specific date range. It is not a random draw from the unconditional return distribution; it is the *joint realization* of that period, so it automatically carries the realized correlations (which during a crisis → 1). Formally it is a single point in factor space, picked from history rather than constructed.

**Hypothetical scenario = constructed point.** The team specifies each $\Delta F_k$ by judgment (informed by historical extremes + economic logic). The craft constraint is *plausibility*: the shocks should be mutually consistent with an underlying story (a "2008-like" recession implies equity, credit, and rates moving in the coherent directions, not arbitrary opposites). BIS 2009 emphasizes scenarios must be **"severe but plausible."**

**Choosing severity.** A common discipline is to calibrate the hypothetical to the *historical worst* plus a margin: take each factor's realized worst stress (e.g. equity $-57\%$ peak-to-trough 2008), then construct a "worse than 2008" version to test capital adequacy — this is the logic behind CCAR's severely-adverse scenario (see [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/06-advanced-extensions|06]]).

---

### 3. Computational Implementation — sensitivity grid + scenario matrix

Stdlib only. First a one-factor sensitivity grid on the example fund, then a two-factor scenario matrix (equity × credit) that exposes the interaction corner.

```python
NAV = 100e6
B_EQ = 0.5; B_CR = -60_000.0; B_RT = -30_000.0
def pnl(eq_pct, cr_bps, rt_bps):
    return B_EQ*NAV*eq_pct + B_CR*cr_bps + B_RT*rt_bps

print("One-factor sensitivity grid (equity only, rates/credit unchanged):")
for e in (-0.10,-0.20,-0.30,-0.40):
    print(f"  equity {e*100:+6.1f}%  ->  P&L {pnl(e,0,0)/1e6:+9.2f} M$")

print("\nScenario matrix (row = equity shock, col = credit bp):")
print("          credit bps: " + "".join(f"{c:>9d}" for c in (0,100,300,500)))
for e in (-0.10,-0.20,-0.30):
    row = f"  equity {e*100:5.1f}%      "
    for c in (0,100,300,500):
        row += f"{pnl(e,c,0)/1e6:9.2f}"
    print(row)
```
```
One-factor sensitivity grid (equity only, rates/credit unchanged):
  equity  -10.0%  ->  P&L     -5.00 M$
  equity  -20.0%  ->  P&L    -10.00 M$
  equity  -30.0%  ->  P&L    -15.00 M$
  equity  -40.0%  ->  P&L    -20.00 M$

Scenario matrix (row = equity shock, col = credit bp):
          credit bps:         0      100      300      500
  equity -10.0%          -5.00   -11.00   -23.00   -35.00
  equity -20.0%         -10.00   -16.00   -28.00   -40.00
  equity -30.0%         -15.00   -21.00   -33.00   -45.00
```
Reading the matrix: equity-only sensitivity tops out at $-$20M, but the **corner cell** (equity $-30\%$ *and* credit +500bp) is $-$45M — more than twice the single-factor worst. A one-at-a-time sensitivity study would have called the fund's risk "$-$20M"; the matrix reveals the real tail is the *joint* shock. **This is why regulators require multi-factor scenarios, not just ladders.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Interaction blindness (single-factor-only).** Testing factors one at a time misses cross terms — as the matrix above shows, the joint corner dominates. BIS 2009 flags this explicitly: scenarios must be run *together* because the interaction is "complex and not intuitively clear."
2. **Historical-scenario stagnation.** Replaying only observed crises guarantees you are always preparing for the *last* war. BIS 2009: historical scenarios "were not able to capture risks in new products," and their "severity levels and duration… proved to be inadequate" in 2008. Historical scenarios must be *augmented* with hypothetical severity margins.
3. **Plausibility blindness (hypothetical-scenario side).** The opposite failure: inventing arbitrary shocks that violate economic logic (e.g. equities −80% with credit *tightening*). An implausible scenario wastes effort and is dismissed by management. The discipline is *internal consistency*: every scenario should have a coherent story tying its shocks together.
4. **Severity ratchet-up failure.** Even when teams built hypotheticals pre-2008, they were "generally only moderate," and "it was difficult for risk managers to obtain senior management buy-in for more severe scenarios" (BIS 2009). The governance failure — not the math — was the binding constraint. Regulators answered with supervisory scenarios (CCAR/EBA) precisely because firms would not self-inflict severity.

---

### 5. Canonical Literature & Study References

- **BCBS**, *Principles for Sound Stress Testing Practices and Supervision* (2009, CN14) — §"Scenario selection": sensitivity vs scenario analysis, historical vs hypothetical, the pre-crisis failures of insufficient severity and buy-in. *Directly verified source for this page.*
- **Hull**, *OFOD*, Ch 22 — linear/quadratic P&L mapping (eq. 22.6–22.8) that the sensitivity and matrix cells evaluate.
- **McNeil, Frey & Embrechts**, *QRM*, Ch 13 — scenario design and the interplay of historical and hypothetical approaches.
- **Bellini**, *Stress Testing and Risk Integration in Banks* (2016) — hands-on construction of scenario sets and their aggregation across risk types.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/02-why-stress-testing|02 · Why Stress Testing]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Index Hub]]
- Continue: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/04-reverse-stress-testing|04 · Reverse Stress Testing]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] (the historical-simulation side of "scenarios from data")

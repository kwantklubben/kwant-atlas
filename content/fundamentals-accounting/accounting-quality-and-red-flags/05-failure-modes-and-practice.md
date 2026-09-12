---
title: "A.5.5 Failure Modes & Practice"
tags:
  - fundamentals-accounting
  - accounting-quality-and-red-flags
  - failure-modes
  - earnings-quality
  - practice
---

**Basic Prerequisites:** [[fundamentals-accounting/accounting-quality-and-red-flags/02-the-accrual-anomaly|02 · The Accrual Anomaly]] through [[fundamentals-accounting/accounting-quality-and-red-flags/04-red-flags-and-shenanigans|04 · Red Flags & Shenanigans]].

---

### 1. Intuition & Practical Objective

Pages 02–04 gave you instruments: the accrual ratio, the discretionary-accrual models, the archetype checklist. This page is the **honesty layer** - the ways each instrument fails, each failure traced to a first principle rather than presented as a gotcha. If the hub's checklist is the *engine*, this page is the *quality control on the engine itself*.

The deepest principle, stated once and used everywhere below:

> **Every quality measure is a *difference between two accounting numbers*, and accounting numbers are jointly produced by the same firm under the same rules. So the measures share blind spots: manipulation that moves both sides of the difference equally is invisible, and manipulation that reverses is self-erasing.**

Three consequences follow directly and are the spine of this page: **(1) accruals reverse, so a single-year measure is timing-luck; (2) everything booked to cash cancels out of balance-sheet accruals; (3) consolidation and comparability changes make time-series screens read structure as quality.**

---

### 2. Mathematical Ground Truth & Derivations

**Reversal - why the accrual identity is a difference, not a level.** Accruals sum to zero over the life of the firm (you can defer recognition, never eliminate it). So if firm $F$ injects $X$ of accruals in year 1, year 2 carries $-X$:

$$
\text{NI}_1 = \text{CF}_1 + X, \qquad \text{NI}_2 = \text{CF}_2 - X, \qquad \text{NI}_1+\text{NI}_2 = \text{CF}_1+\text{CF}_2.
$$

The cumulative *earnings* are unchanged; only the *timing* moved. Therefore the only accrual measure that is robust to reversal timing is the **cumulative** one:

$$
\text{cumulative CFO/NI} = \frac{\sum_{t=1}^{T}\text{CFO}_t}{\sum_{t=1}^{T}\text{NI}_t} \;<\; 1 \;\Rightarrow\; \text{earnings were booked that never became cash.}
$$

A single-year accrual ratio cannot distinguish "manipulating upward this year" from "reversing last year's manipulation" - they have opposite signs and the same cause. This is why the *trend* and the *cumulative* version outrank the level.

**Blindness to cash-side games.** Write the Sloan measure as a sum of differences of balance-sheet changes. Fabricate a *cash* sale of amount $X$: both $\Delta CA$ (via cash) and $\Delta Cash$ rise by $X$, so

$$
(\Delta CA - \Delta Cash) \;\text{is unchanged by } X.
$$

The accrual measure is *algebraically incapable* of seeing it. The same cancellation kills the CFO/NI ratio as a detector once the fake cash is booked as operating inflow. **Consequence:** the balance-sheet toolbox detects *timing* manipulation; it does not detect *fabrication*.

**Comparability and the ratio's denominator.** A screen compares this year's ratio to last year's - which assumes the two years are comparable. An acquisition breaks that assumption:

$$
\text{CFO}\uparrow \text{ by the acquired firm's cash flows}, \qquad \text{NI}\uparrow \text{ by the acquired firm's earnings}, \qquad \frac{\text{CFO}}{\text{NI}} \text{ reads as "improving quality"}
$$

even when the acquirer's own operations are deteriorating. The same logic applies to $\Delta CA$, goodwill, and any balance-sheet stock after a material transaction. The practice rule is mechanical: **flag the year a material acquisition or divestiture occurred, and never read a quality trend straight through it.**

**Composite scores reward improvement, not level.** A binary signal like $\Delta\text{ROA}>0$ is *scale-free* - it cannot tell whether the firm went from $+15\%$ to $+16\%$ or from $-15\%$ to $-2\%$. Both score 1. Any composite built from directional signals inherits this and will rank a deeply distressed firm that is merely *deteriorating less slowly* alongside a genuinely strong one.

---

### 3. Computational Implementation - four ways the screens lie

Stdlib only. Four failure modes, each demonstrated with the minimum arithmetic that produces the failure, so the mechanism is undeniable rather than asserted.



Mode 3 is the one to remember: the **$+50$** of fabricated cash revenue moves the Sloan accrual expression by exactly **zero**. The instrument is not weak here - it is *structurally* blind.

---

### 4. Failure Modes & First-Principles Breakdowns

**The catalogue, each tied to its first principle.**

1. **Timing luck mistaken for quality (first principle: accruals reverse).** A one-year accrual ratio conflates manipulation with the reversal of last year's manipulation. *Rule:* use *trend* and *cumulative* measures; never act on a single year's accrual ratio. → [[fundamentals-accounting/accounting-quality-and-red-flags/02-the-accrual-anomaly|02 · The Accrual Anomaly]].
2. **Structural blindness to cash-side fabrication (first principle: the difference cancels).** Fabricated cash revenue leaves balance-sheet accruals untouched and *improves* CFO/NI. *Rule:* for accounts with cash-side exposure, use external evidence (channel checks, customer filings, returns, receivables *aging*) - the ratio will never tell you.
3. **Comparability breaks (first principle: time-series ratios assume a stable entity).** Acquisitions, divestitures, FX, and accounting-standard changes (IFRS/ASC adoptions, lease capitalisation) all reset the level. *Rule:* mark the break year; rebuild the series on a constant-perimeter basis or skip the comparison. → [[fundamentals-accounting/accounting-quality-and-red-flags/04-red-flags-and-shenanigans|04 · Red Flags & Shenanigans]].
4. **The proxy you chose determines the answer (first principle: "quality" is not one construct).** Accruals-based, persistence-based, smoothness-based and restatement-based measures rank firms differently - and can rank them *oppositely*. *Rule:* name the construct before you screen (Dechow, Ge & Schrand's whole point) and never mix proxies into a single "quality score" without saying what it means.
5. **Extreme-performance contamination (first principle: benchmarks under-control for performance).** Poorly performing firms have extreme accruals for legitimate reasons, and every discretionary-accrual model over-rejects in those samples. *Rule:* add a performance control, or restrict the sample, or report that you did not. → [[fundamentals-accounting/accounting-quality-and-red-flags/03-detecting-earnings-management|03 · Detecting Earnings Management]].
6. **Look-ahead and survivorship (first principle: data hygiene).** Using *restated* fundamentals to test a quality screen bakes the outcome into the input; testing on today's live firms drops every delisted fraud. *Rule:* point-in-time, as-reported data, delisting returns included. → [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]].
7. **Directional composites reward non-death (first principle: binary signals are scale-free).** "Improving" from a catastrophic base scores the same as "improving" from excellence. *Rule:* pair every binary signal with a *level* condition (e.g. ROA > 0, not merely rising).
8. **Discretion is not fraud (first principle: a residual is a residual).** Discretionary accruals measure *deviation from your model* - which includes legitimate judgement, differing policy, and superior growth. *Rule:* treat every quality flag as a question, and state the innocent explanation you ruled out.

---

### 5. Canonical Literature & Study References

- **Dechow, Patricia, Ge, Weili & Schrand, Catherine**: "Understanding Earnings Quality: A Review of the Proxies, Their Determinants and Their Consequences" (*JAE*, 50(2–3), 344–401, 2010) - the definitive map of every quality proxy, and the source of failure modes 4 and 5. **The single most important reference on this page.**
- **Sloan, Richard G.**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 71(3), 289–315, 1996) - the accrual measure whose blind spots this page catalogues, and the reversal property central to mode 1.
- **Dechow, Sloan & Sweeney**: "Detecting Earnings Management" (*TAR*, 70(2), 193–225, 1995) - the low-power and extreme-performance findings behind failure modes 5 and 8.
- **Schilit, Perler & Engelhart**: *Financial Shenanigans* (McGraw-Hill, 4th ed., 2020) - the games that exploit each blind spot; particularly strong on the cash-flow and footnote layers that ratios cannot reach.
- **Chan, Jegadeesh & Lakonishok**: "Earnings Quality and Stock Returns" (*JF*, 61(2), 769–806, 2006) - evidence that the nondiscretionary component of accruals *also* predicts returns, which undercuts the naive "high accruals = fraud" reading (mode 8).
- **Mulford, Charles W. & Comiskey, Eugene E.**: *The Financial Numbers Game* (Wiley, 2002) - how to reverse-engineer aggressive accounting choices back to the underlying economics.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/accounting-quality-and-red-flags/03-detecting-earnings-management|03 · Detecting Earnings Management]] · [[fundamentals-accounting/accounting-quality-and-red-flags/04-red-flags-and-shenanigans|04 · Red Flags & Shenanigans]] · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Index Hub]]
- Forward: [[fundamentals-accounting/accounting-quality-and-red-flags/06-advanced-extensions|06 · Advanced Extensions]] (the Beneish M-score, and proxies that avoid some of these traps)
- Parallel defense layer: [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|Ratio Red Flags]]
- Data hygiene and incentives: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]] (debt-covenant and bonus-plan incentives that trigger management)

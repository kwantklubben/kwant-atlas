---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - fundamentals-accounting
  - equity-valuation
  - failure-modes
  - sensitivity
  - margin-of-safety
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]].

---

### 1. Intuition & Practical Objective

A DCF is *arithmetic*; its accuracy is entirely the accuracy of its inputs. This page names the failure modes precisely so a practitioner knows **where to distrust the model and how the errors show up in money terms** — and it ends with the decision rule that turns a valuation into an investment: the **margin of safety**.

The three failures, in one line each:

1. **GIGO forecasts** — revenue, margin and reinvestment assumptions are guesses, and they dominate the output.
2. **Terminal-value dominance** — $70$–$80\%$ of value is the perpetuity, so $g_n$ and $K_c$ *are* the valuation.
3. **Wrong cost of capital / mismatched discounting** — a rate error silently moves value by $14$–$16\%$ before you notice.

And the practice discipline: **buy well below intrinsic value**, because intrinsic value is an estimate, not a fact.

---

### 2. Mathematical Ground Truth & Derivations

**Where the errors enter.** Value is a *ratio-like* function of its drivers, so small input errors compound:

$$
V_0=\frac{\text{FCFF}_1}{K_c-g},\qquad \text{FCFF}_1=\text{Revenue}\times\text{Margin}\times(1-t)\times(1-\text{RR}).
$$

Two structural facts:

- **The denominator amplifies.** $\dfrac{\partial V}{\partial g}=\dfrac{\text{FCFF}_1}{(K_c-g)^2}$ and $\dfrac{\partial V}{\partial K_c}=-\dfrac{\text{FCFF}_1}{(K_c-g)^2}$. A $1\%$ change in *either* moves value by roughly $\dfrac{0.01}{K_c-g}\approx 9\%$ at $K_c-g=0.106$ — and *non-linearly as $g\to K_c$*.
- **Terminal share.** For an explicit window $n$ and perpetuity,

$$
\text{TV share}=\frac{\text{PV}(\text{TV})}{\text{PV}(\text{explicit})+\text{PV}(\text{TV})},
$$

which for a growing firm approaches $1$ quickly. The model is *mostly* a statement about the stable state.

**The margin of safety (Graham).** If intrinsic value $\hat V$ is an estimate, the rational response is to require a buffer before buying:

$$
\text{buy if }P\le(1-m)\,\hat V,\qquad m\in[20\%,40\%].
$$

The margin converts valuation uncertainty into a *decision rule*: you are paid for being approximately right and protected against being precisely wrong.

---

### 3. Computational Implementation — the failures in numbers

Stdlib only. It measures GIGO sensitivity, terminal dominance via the denominator, the wrong-rate error, and converts value into a buy rule.

```python
def pv(cfs, r):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs, 1))

def per_share(margin=0.20, rr=0.50, g1=0.10, w=0.10, gs=0.03,
              rev0=1000.0, tax=0.25, cash=250.0, debt=600.0, shares=100.0):
    rev, f = rev0, []
    for _ in range(5):
        rev *= (1 + g1)
        f.append(rev * margin * (1 - tax) * (1 - rr))
    ev = pv(f, w) + f[-1] * (1 + gs) / (w - gs) / (1 + w) ** 5
    return (ev + cash - debt) / shares

base = per_share()
print(f"base per-share = {base:.2f}")

# GIGO: a 2-point margin move and a 10-point reinvestment move
for m in (0.18, 0.20, 0.22):
    print(f"  margin {m:.0%}: " + "  ".join(f"{per_share(margin=m, rr=rr):6.2f}"
                                            for rr in (0.40, 0.50, 0.60)))

# terminal dominance: value vs (WACC, stable g) on a single-stage firm
print("  TI operating value across WACC x g:")
for w in (0.13, 0.156, 0.17):
    print(f"    WACC={w:.3f}: " + "  ".join(f"{212.2/(w-g):7.0f}" for g in (0.03, 0.04, 0.05, 0.06)))

# mismatched discount rate (Damodaran Illustration 2.1)
cfe = [50, 60, 68, 76.2, 83.49]; cff = [90, 100, 108, 116.2, 123.49]
ve_ok = pv(cfe[:-1] + [cfe[-1] + 1603.008], 0.13625)
ve_bad = pv(cfe[:-1] + [cfe[-1] + 1603.008], 0.0994)
print(f"  equity @ wrong rate: {ve_ok:.0f} -> {ve_bad:.0f} ({ve_bad/ve_ok-1:+.1%})")

# margin of safety
for f in (1.0, 0.80, 2/3):
    print(f"  pay {f:.0%} of intrinsic -> buy below {base*f:.2f}")
```
```
base per-share = 11.29
  margin 18%:  12.47    9.81    7.15
  margin 20%:  14.24   11.29    8.33
  margin 22%:  16.02   12.76    9.51
  TI operating value across WACC x g:
    WACC=0.130:    2122     2358     2652     3031
    WACC=0.156:    1684     1829     2002     2210
    WACC=0.170:    1516     1632     1768     1929
  equity @ wrong rate: 1073 -> 1248 (+16.4%)
  pay 100% of intrinsic -> buy below 11.29
  pay 80% of intrinsic -> buy below 9.03
  pay 67% of intrinsic -> buy below 7.52
```
Read the numbers: a **$2$-point margin** swing ($18\%\to22\%$) moves the value **$+28.5\%$ to $+33.0\%$** depending on the reinvestment rate (e.g. $12.47\to16.02$ at $rr{=}0.40$), a **$0.40\to0.60$ reinvestment-rate** swing at fixed $20\%$ margin spans $\pm26\%$ ($8.33\to14.24$), and a **$1$-point move in $g$** moves the single-stage value $10$–$18\%$ (e.g. $2002\to2210$). One wrong discount rate moves equity $+16.4\%$. **No spreadsheet can out-precision its assumptions** — which is why the practitioner's answer is a *range plus a margin of safety*, not a point estimate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **GIGO forecasts.** Revenue growth, margins, and reinvestment are the model's real inputs. Sensitivity tables (above) should accompany every DCF; a single point estimate is dishonest about how little is known.
2. **Terminal-value dominance.** $70$–$80\%$ of value is the perpetuity; the five-year detail is largely theatre. Test $g_n$ and $K_c$ specifically, cap $g_n$ at $r_f$, and never let $g_n\to K_c$.
3. **Wrong cost of capital.** Using WACC for equity flows (or a beta/ERP not matched to the cash flow) shifts value $13$–$16\%$ with no visible sign in the model. Match cash flow to discount rate *mechanically*.
4. **Precision illusion.** Reporting \$11.29 to the cent implies accuracy that the inputs do not support. Report a range; the margin of safety is the engineered response to that uncertainty.
5. **Anchoring to price.** The most common real-world failure is not mathematical but psychological: reverse-engineering assumptions until the model "confirms" the current market price. Intrinsic value must be estimated *independently* of price.
6. **Ignoring the decision rule.** A valuation with no buy rule is trivia. The output of the exercise is "buy below \$9.03", not "fair value is \$11.29".

---

### 5. Canonical Literature & Study References

- **Damodaran**, *Investment Valuation*, Ch 2 (mismatching cash flows and rates — Illustration 2.1), Ch 12 & 15 (stable-growth limits; why the terminal term dominates), and *The Dark Side of Valuation* (valuing the firms where clean DCF assumptions break).
- **Graham**, *The Intelligent Investor*, Ch 8 & 20 — "margin of safety" as the central concept; the buy rule that this page's last line operationalises.
- **Graham & Dodd**, *Security Analysis* — asset-value floors and earnings power as cross-checks on the DCF.
- **Koller et al. (McKinsey)**, *Valuation*, Ch 15 — error-checking a DCF and running scenario/sensitivity analysis professionally.
- **Fridson & Alvarez**, *Financial Statement Analysis: A Practitioner's Guide* — realistic interpretation warnings when the inputs misbehave.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Forward: [[fundamentals-accounting/equity-valuation/06-advanced-extensions|06 · Relative Valuation & Advanced Extensions]]
- Risk: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
- Research: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (overfitting the forecast to the past)

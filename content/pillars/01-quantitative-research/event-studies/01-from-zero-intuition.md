---
title: "01 — Event Studies from Zero: Intuition & the Why"
tags:
  - pillar-quant-research
  - event-studies
  - intuition
  - abnormal-returns
  - market-efficiency
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (return aggregation) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (expectations).

---

### 1. Intuition & Practical Objective

This page builds the *why* of event studies with **no prior event-study knowledge needed**. The objective is one idea: **to measure how a specific corporate event moved a stock price, you cannot just look at the price move — you must subtract what the stock would have done anyway, on that day, for reasons unrelated to the event.** That subtraction is the entire method, and everything else is refinement.

Start with the dumbest question: *why can't we just read the +2% jump on the announcement date?* Because on any given day a stock also moves for the market (the whole index rose or fell), for its sector, for general news, and for plain noise. A stock can gain 2% on the announcement day for *no* event reason at all — because the market rallied 1.5% that day. So the event's true contribution is the **residual**: observed return *minus* the return the stock "should" have earned given everything *other* than the event.

Three steps, three "aha"s:

1. **Expected return = the "no-event" counterfactual.** Define a *normal* (expected) return — what the stock would earn if the event had not happened. The simplest version (Brown & Warner's **mean-adjusted** model) uses the stock's own average daily return in a quiet *estimation window* before the event. Abnormal return = observed − that average.

2. **Abnormal return is a wealth effect.** The abnormal return at the event is a direct measure of the *unanticipated change in securityholder wealth* caused by the event (Kothari–Warner 2007). A +3% abnormal return says "this event transferred ~3% of firm value, over and above market/risk effects." Because rational investors price news instantly, most of the effect shows up on the announcement day itself — which is why the method works even with a window of one to three days.

3. **Aggregate across firms to cancel noise.** One firm's abnormal return is dominated by idiosyncratic noise (a single +3% event on a 2%-volatility stock is swamped). Average the abnormal returns over *many* firms that shared the *same type* of event; the noise averages toward zero and the common signal survives. This cross-sectional aggregation is the statistical heart of the method.

---

### 2. Mathematical Ground Truth & Derivations

**The return decomposition** (Kothari–Warner 2007, eq. 1–2). Write the observed return as a normal component plus an abnormal component:

$$
R_{it} = K_{it} + e_{it},
$$

where $K_{it}$ is the expected (normal) return under a given model and $e_{it}$ is the abnormal return. Equivalently,

$$
e_{it} = R_{it} - K_{it},
$$

the difference between the return *conditional on the event* and the expected return *unconditional on the event*.

**Mean-adjusted model** (Brown–Warner 1980/85, eq. 1–2). The normal return is the stock's own estimation-window average:

$$
K_{it} = \bar R_i = \frac{1}{L}\sum_{k}R_{ik}, \qquad AR_{it} = R_{it} - \bar R_i,
$$

over an estimation window (BW use days $-244$ to $-6$, ~239 observations) chosen *before* the event so it cannot be contaminated by the event itself.

**Why "abnormal return" is a test of efficiency.** If markets are semi-strong efficient, the abnormal return should be nonzero *only* in the narrow window around the announcement and zero afterward. Systematically nonzero abnormal returns *after* the event are inconsistent with efficiency — they would support a profitable (pre-cost) trading rule (Kothari–Warner 2007, §3.2.2). This is exactly the logic that makes event studies the "cleanest evidence we have on efficiency" (Fama 1991).

---

### 3. Computational Implementation — the simplest abnormal return

This is the entire method in four lines — the mean-adjusted model from Brown & Warner. Stdlib only.

```python
import random
random.seed(3)

# A firm's "normal" return = its average return in a pre-event estimation window.
# Abnormal return = observed - expected.  That is the whole idea.
est = [random.gauss(0.0003, 0.020) for _ in range(239)]   # estimation window
normal = sum(est)/len(est)                                # expected (no-event) return
event_day_return = 0.025                                  # firm moved +2.5% on the event
abnormal = event_day_return - normal

print(f"mean 'normal' return (estimation window) = {normal*100:+.3f}% per day")
print(f"event-day observed return                = {event_day_return*100:+.3f}%")
print(f"ABNORMAL return = observed - expected    = {abnormal*100:+.3f}%")
```
```
mean 'normal' return (estimation window) = -0.217% per day
event-day observed return                = +2.500%
ABNORMAL return = observed - expected    = +2.717%
```

The firm moved +2.5%, but once we subtract its usual −0.22% baseline, the *abnormal* return is +2.72% — slightly larger, because the firm happened to trend down when it "should" have been flat. The event's true, unanticipated wealth effect is the residual, not the raw move.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "raw-return" trap.** Looking at the *raw* price move instead of the abnormal return mistakes market drift and firm beta for event impact. Brown–Warner explicitly flag a "Raw Returns" variant (mean-adjusted with $\bar R_i$ forced to zero) that finds spurious abnormal performance when the average return is positive — because it ignores the baseline the stock would have earned anyway.
2. **The estimation window must be clean.** If the estimation window (before the event) itself contains value-relevant events, the baseline $\bar R_i$ is biased and every abnormal return is off by that bias.
3. **One firm tells you nothing.** A single +3% abnormal return on a 2%-volatility stock is statistically indistinguishable from noise. The method only works when abnormal returns are averaged over a cross-section of firms sharing the event type — see [[pillars/01-quantitative-research/event-studies/02-event-study-methodology|02 · Methodology]].
4. **Expected-return model is a choice.** "Abnormal" is only defined *relative to a model of normal returns*. A different benchmark (mean-adjusted vs market model vs Fama–French) gives a different abnormal return — event studies are joint tests of the event *and* the benchmark (see [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]]).

---

### 5. Canonical Literature & Study References

- **Brown & Warner (1980)**, *Measuring Security Price Performance*, JFE 8(3) — the mean-adjusted / market-model measures and the return decomposition. *Verified refs/49.*
- **Brown & Warner (1985)**, *Using Daily Stock Returns: The Case of Event Studies*, JFE 14(1) — eq. 1–2 (mean-adjusted returns), the estimation-window design. *Verified refs/50, read in full.*
- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance Ch. 1 — the abnormal-return decomposition (eq. 1–2) and its interpretation as a wealth effect. *Verified refs/52, read in full.*
- **Fama (1991)**, *Efficient Capital Markets: II*, J. Finance 46(5) — event studies as "the cleanest evidence we have on efficiency."

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[pillars/01-quantitative-research/event-studies/02-event-study-methodology|02 · Event-Study Methodology]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/momentum/02-cross-sectional-momentum|Cross-Sectional Momentum]] (averaging a signal across many assets — the same aggregation logic)

---
title: "7.5.3 The Alt-Data Pipeline"
tags:
  - pillar-machine-learning
  - alternative-data-pipelines-and-evaluation
  - data-pipeline
  - point-in-time
  - as-of-join
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/01-from-zero-intuition|01 · From Zero]] and basic Python/pandas. The timestamp discipline formalizes [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|Data Sources · 05 Failure Modes]].

---

### 1. Intuition & Practical Objective

A raw alt-data delivery - a daily card-spend dump, a weekly foot-traffic file, a scrape of product pages - is **not a signal**. It is an irregular, entity-inconsistent, hindsight-contaminated pile of facts. The pipeline is the machinery that turns it into a *tradeable, point-in-time* feature without silently importing the future. This page is the build sheet for that machinery.

The five stages, and what each one is really guarding against:

1. **Ingest** - land the raw delivery *immutably*, with its **arrival timestamp**. Never overwrite; the raw layer is your audit trail.
2. **Store** - every fact carries **two clocks**: `event_time` ($t_E$, when it happened) and `knowledge_time` ($t_K$, when you learned it). The pair *is* the schema (AFML §2.2.1: vendors index by the period end, which is exactly $t_E$ - a trap).
3. **Clean** - reconcile entities to a stable key (CIK/ticker↔vendor ID), de-duplicate, and **never** let a later restatement reach backwards in time.
4. **Feature** - aggregate to a homogeneous *bar* aligned to a tradeable universe (AFML §2.3: raw irregular ticks → regularized table), computed strictly from records with $t_K\le t$.
5. **Evaluate** - measure predictive power **out of sample**, with the *same* PIT function used in production ([[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal|04 · Evaluating Signal]]).

> **The one rule that matters most.** A feature at time $t$ may be a function only of records whose **knowledge time** is $\le t$. Aligning to the **event** time is the single most common and most lethal alt-data bug, and it is trivially testable.

---

### 2. Mathematical Ground Truth & Derivations

**The provenance tuple.** A vendor fact is not a scalar; it is a record

$$
r=\big(\underbrace{\text{key}}_{\text{entity}},\ \underbrace{v}_{\text{value}},\ \underbrace{t_E}_{\text{event time}},\ \underbrace{t_K}_{\text{knowledge time}}\big),\qquad t_K \ge t_E \text{ always}.
$$

**The point-in-time (as-of) join.** The feature at decision time $t$ is the *most recent record already known*, i.e. a left-as-of join on knowledge time:

$$
x_t \;=\; \operatorname{last}\big\{\,v(r)\;:\;t_K(r)\le t\,\big\}\qquad(\text{not }t_E(r)\le t).
$$

**The look-ahead gap.** Define the leak of using event-time alignment as the interval over which a record is used but not yet knowable:

$$
\Delta_{\text{leak}}(r) = t_K(r)-t_E(r) \;=\; \text{vendor lag} + \text{your ingest delay}.
$$

A naive join assigns $r$ to *every* $t\in[t_E,t_K)$ - trading on information that did not exist. The measured IC of that join is not the signal's IC; it is a **measurement of $\Delta_{\text{leak}}$**.

**Staleness under an honest join.** A PIT feature is, by construction, *stale*: at $t$ you hold the value from $t-\delta$ where $\delta$ is the age of the freshest known record. This is the mechanism behind the decay of [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/01-from-zero-intuition|01 · From Zero]]: the average staleness $\bar\delta$ plays the role of the delay $d$ in $e^{-\lambda\bar\delta}$.

**Bars (regularization).** Irregular raw events are aggregated into a homogeneous series. Time bars sample at fixed intervals; *information-driven* bars (tick, volume, dollar, imbalance bars) sample when activity arrives (AFML §2.3, eqs. for tick/volume/dollar/imbalance/run bars). For alt-data aggregates (weekly card panels, daily scrapes), the "bar" is the aggregation window - and it must be closed only on **known** data.

---

### 3. Computational Implementation - making the leak visible

numpy only. Build a latent signal, deliver it with a knowledge lag, and compare two joins: **naive** (assign the record to its event date) and **PIT** (only records with $t_K\le t$). The naive join scores as if it had the oracle; the PIT join scores what you would actually have earned.




The **naive** join reproduces the *oracle* IC exactly ($+0.0646$): it is trading on a value it could not have had, so the backtest looks perfect. The **PIT** join - the only one you can run live - scores $+0.0283$, **43.8%** of the oracle, and the leak is a **+0.0363** inflation: more than the honest signal itself. A 3-day lag halved the edge; longer lags would kill it entirely. This is the entire point of the pipeline in one table.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Event-time joins (the cardinal sin).** Assigning a value to $t_E$ instead of $t_K$ - the way vendors index "the last day of the report period" (AFML §2.2.1) - inflates the IC by exactly the leak above. The fix is architectural: store $t_K$, join as-of on $t_K$.
2. **Restatement time-travel.** A vendor corrects Q1's value in Q3 and overwrites the row; if your store keeps only the latest value, your *historic* features change when you re-run. **Version the record** (multiple $t_K$ rows) so history is immutable.
3. **Entity-resolution drift.** Vendor IDs ≠ CIK/ticker; a mis-mapped entity silently assigns one company's footfall to another, creating a signal that is pure mislabeling. Reconcile explicitly and log the mapping as-of each date.
4. **Timezone and calendar mismatch.** "Daily" means close-of-market in one feed, UTC midnight in another; aggregating across calendars double-counts or drops a day - a *deterministic* fake signal. Pin a single calendar.
5. **Aggregation-window leak.** A "weekly" bar whose window closes Friday but which you can only compute Monday is a 3-day-leaked feature if you label it as Friday's. The bar's timestamp must be its **availability**, not its window end.

---

### 5. References

- **López de Prado**, *Advances in Financial Machine Learning*, **§2.2.1** (fundamental data reported with a lapse; backfilled/reinstated values; the "indexed by last date in the report" error) and **§2.3** (bars: standard time bars and information-driven tick/volume/dollar/imbalance/run bars
- **Guida, Tony**, *Big Data and Machine Learning in Quantitative Investment* (Wiley, 2019)
- **Kolanovic & Krishnamachari**, *Big Data and AI Strategies* (J.P. Morgan, 2017)
- **Data-sources discipline in-repo:** [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|Data Sources · 05 Failure Modes & Practice]]

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/02-alt-data-landscape|02 · Alt-Data Landscape]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal|04 · Evaluating Signal]] → [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/05-failure-modes-and-practice|05 · Failure Modes]]
- Feature/target construction downstream: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (official bars, triple-barrier labels, sample weights)
- Provenance discipline upstream: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] · [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|EDGAR & XBRL]]

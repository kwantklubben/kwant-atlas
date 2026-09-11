---
title: "7.5 Alternative Data Pipelines & Evaluation"
tags:
  - pillar-machine-learning
  - alternative-data-pipelines-and-evaluation
  - alternative-data
  - point-in-time
  - index-hub
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (correlations, regression, the t-statistic) and [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (timestamps, vendors, point-in-time hygiene). No prior ML needed. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Traditional market data — prices, volumes, filings — is **universally available**. Every fund reads the same tape, so any edge it contains is arbitraged to near zero within seconds. *Alternative data* is everything else: the **primary information** that has not yet reached the other sources (López de Prado, AFML §2.2.4). Before Exxon reported, someone watched the tankers; before a retailer guided up, someone counted the parking lot, monitored the card spend, or scraped the web prices. Alt-data's promise is **information that arrives weeks before it is reflected in price** — and its cost is that the data is dirty, irregularly timestamped, expensive, and easy to backtest into a fantasy.

The alt-data lifecycle has five stages — hold these in your head:
1. **Ingest** — pull raw vendor delivery (files, API, stream).
2. **Store** — persist with **two timestamps**: when the event happened and when you learned it.
3. **Clean** — reconcile entities (CIK/ticker↔vendor id), de-duplicate, handle restatements.
4. **Feature** — aggregate into a point-in-time signal aligned to a tradeable universe.
5. **Evaluate** — measure whether it predicts a forward return *out of sample and without leakage*.

This folder is the **hub**. It (a) gives the fast **alt-data category lookup** and the two evaluation numbers (IC and decay half-life) below — job #1 of this folder — and (b) routes you to six sub-pages that climb from raw intuition to vendor economics and signal combination.

> **The one-sentence essence.** "Alternative data is only a signal if it is (i) *primary* — not yet in prices — and (ii) *honestly timestamped* — a value is usable only at its **knowledge date**, never its event date — and everything downstream is the discipline of *measuring a weak, decaying correlation without leaking the future*."

**Audience arc:** the beginner learns *what alt-data is and why it is different from the tape*; the intermediate learns *the pipeline and how to test a dataset honestly (IC, decay)*; the expert learns *vendor economics, uniqueness, and signal combination*. The sub-pages are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Quick Lookup

**Notation.** $x_t$ = the alt-data signal at time $t$; $y_{t+1}$ = the forward return it is meant to predict; $t_E$ = **event time** (when the real-world fact occurred); $t_K$ = **knowledge time** (when the record entered your database); $\lambda$ = decay rate; $B$ = breadth (number of independent bets per year); $N$ = cross-section size.

**The point-in-time identity** (the single rule that separates a real backtest from a fantasy):

$$
\text{usable}(t) = \{\text{records}: t_K \le t\}, \qquad\text{never}\qquad \{\text{records}: t_E \le t\}.
$$

Aligning a record to its **event** date — the way vendors index "the last day of the report period" (AFML §2.2.1) — injects up to one full reporting lag of look-ahead.

**Alpha decay & half-life.** A proprietary edge decays as the data is resold and arbitraged:

$$
\text{IC}(t) = \text{IC}_0\,e^{-\lambda t}, \qquad t_{1/2}=\frac{\ln 2}{\lambda}.
$$

**The evaluation statistics** (the "does this dataset have signal?" measures):

$$
\text{IC}_p=\operatorname{corr}\big(x^{(p)},y^{(p)}\big),\qquad \text{ICIR}=\frac{\overline{\text{IC}}}{\sigma_{\text{IC}}},\qquad t=\text{ICIR}\sqrt{P}.
$$

**The Fundamental Law of Active Management** (Grinold & Kahn) — why every *unique* signal is worth hunting:

$$
\text{IR}=\text{IC}\cdot\sqrt{B}\cdot\text{TC}\quad(\text{TC}=\text{transfer coefficient});\qquad\text{combining }n\text{ alphas, pairwise corr }\rho:\quad \text{IC}_{\text{comb}}=\text{IC}\sqrt{\frac{n}{1+(n-1)\rho}}.
$$

**The alt-data category lookup** (job #1). Categories per AFML §2.2.4 (after Kolanovic & Krishnamachari 2017):

| Category | Typical sources | Update | PIT gotcha | Canonical failure mode |
|---|---|---|---|---|
| **Individuals** | Social media, news, web-search trends, job postings | minutes–daily | Sentiment scored **after** the fact; revisions | Backfill/revision leak; bot & survivorship in the panel |
| **Business processes** | Card-transaction panels, transaction data, corporate/government records | daily–quarterly | Panel membership changes; vendor lags 2–5 days | **Panel bias**: an issuing bank leaves, spend "drops 30%" |
| **Sensors** | Satellite imagery, geolocation, weather, CCTV/tanker tracking | daily–weekly | Cloud cover; coverage of the *same* stores changes | **Coverage drift** read as a demand collapse |
| **Analytics (derived)** | Vendor-computed signals (sentiment scores, foot-traffic indices) | varies | You inherit the vendor's (opaque) look-ahead | Black-box methodology; not reproducible |
| **Market/execution** | Tick & L3 order-book feeds (e.g. Databento), quote data | ms | Timestamp = exchange vs receipt; roll/stitch errors | Microstructure noise overfit; survivorship of delisted names |

> **Critical caveat — freshness, not just cleanliness.** Vendors differ in *cost* and in *when the value becomes knowable*. A card panel aggregated weekly and delivered on a 3-day lag means the freshest value you may legally use at $t$ is 3–10 days old. Fix the lag convention once and hold it constant; the discipline that formalizes it is [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes (Data Sources)]].

**Verified quick-reference (reproduced on the sub-pages; see §3):**

| Quantity | Where | Verified value (this folder) |
|---|---|---|
| Look-ahead IC inflation (naive vs PIT) | §3 / 03 | naive $+0.0646$ vs PIT $+0.0283$ (PIT is $43.8\%$ of oracle) |
| Alpha fraction capturable at delay $d$ | 01 | 7-day half-life: $d{=}20\text{d}\Rightarrow 13.8\%$; $d{=}60\text{d}\Rightarrow 0.3\%$ |
| Required IC for IR$=1$ at breadth 252 | 02 | $0.0630$ |
| Cross-sectional ICIR & $t$-stat | 04 | ICIR $0.919$, $t=14.59$ (true IC $0.05$) |
| Fitted decay $\hat\lambda$ vs true $0.12$ | 04 | $\hat\lambda=0.1175$ (half-life 5.90 vs 5.78) |
| Backfill inflation of IC | 05 | PIT $+0.4509$ → backfilled $+0.6069$ ($+0.1561$) |
| Survivorship bias | 05 | all-firm $+6.43\%$ vs survivor $+9.38\%$ ($+2.95\%$/yr) |
| Uniqueness $1-R^2$ of a new signal | 06 | $0.185$ / $0.773$ / $0.990$ vs corr $0.90/0.48/0.10$ |

---

### 3. Computational Implementation — the minimal honest evaluation

The whole point in ~20 lines: build an alt-data signal, and show the **same** signal scores a perfect IC when read at its event date and a realistic one when read point-in-time. numpy only; stdlib works too.

```python
import numpy as np

rng = np.random.default_rng(11)
T, LAG = 400, 3
x = np.zeros(T); x[0] = rng.normal()
for t in range(1, T):
    x[t] = 0.95*x[t-1] + rng.normal(0, 0.3)     # latent alt-data signal (AR(1))
y = 0.010*x + rng.normal(0, 0.05, T)            # forward return
knowledge = np.arange(T) + LAG                  # value known only LAG days after event

def ic(a, b):
    m = ~np.isnan(a) & ~np.isnan(b)
    a2, b2 = a[m] - a[m].mean(), b[m] - b[m].mean()
    return float((a2*b2).sum()/np.sqrt((a2**2).sum()*(b2**2).sum()))

pit = np.full(T, np.nan)
for t in range(T):
    avail = np.where(knowledge <= t)[0]
    if avail.size:
        pit[t] = x[avail[-1]]
print(f"NAIVE IC (read at event date)      = {ic(x, y):+.4f}")
print(f"PIT   IC (only values known at t)  = {ic(pit, y):+.4f}")
print(f"look-ahead inflation                = {ic(x,y) - ic(pit,y):+.4f}")
```
```
NAIVE IC (read at event date)      = +0.0646
PIT   IC (only values known at t)  = +0.0283
look-ahead inflation                = +0.0363
```

---

### 4. Failure Modes & First-Principles Breakdowns (hub signposts)

The full analysis lives in [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Look-ahead / point-in-time violation** — reading a value at its *event* date instead of its *knowledge* date ($t_K$) injects the reporting lag into the backtest; the first principle is that **a dataset is a function of when you looked at it** (the §3 run shows the IC is *doubled* by this one mistake).
2. **Backfill & survivorship bias** — vendors overwrite history with corrected values and keep only today's survivors; both flatter the backtest while the *true* universe looked worse leading in.
3. **Overfitting the evaluation** — testing one dataset is innocent; testing thousands and keeping the best is the multiple-testing crime, and an alt-data signal at $N{=}60$ names has $\text{IC}$ noise $\approx 1/\sqrt{60}$ — comparable to the signal itself.

---

### 5. Canonical Literature & Study References

- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (Wiley, 2018) — **§2.2.1** (fundamental data is reported *with a lapse*; backfilled/reinstated values; the "indexed by period-end" error), **§2.2.4** (alternative data = *primary* information; the individuals/business-process/sensors taxonomy, citing Kolanovic & Krishnamachari), **§2.3** (bars: making irregular raw data into a regularized table), **Ch. 7** (leak-proof cross-validation), **Ch. 11** (backtest errors). *The spine of this folder; corpus PDF verified.*
- **Kolanovic, Marko & Krishnamachari, Rajesh T.**: *Big Data and AI Strategies: Machine Learning and Alternative Data Approach to Investing*, J.P. Morgan Global Quantitative & Derivatives Strategy (2017) — the industry-defining alt-data taxonomy (individuals / business processes / sensors). *Corpus reference.*
- **Guida, Tony**: *Big Data and Machine Learning in Quantitative Investment* (Wiley, 2019) — the most complete practitioner treatment of the *end-to-end* alt-data pipeline: sourcing, cleaning, feature generation, backtesting. *Corpus [CORE] for this sub-topic.*
- **AIMA / SS&C Technologies**: *Casting the Net: How Hedge Funds Are Using Alternative Data* (2017) — the standard industry survey (~\$720bn AUM respondents) on which datasets funds buy and the practical pain points. *Corpus [CORE]; ideal orientation reading.*
- **Grinold, Richard C. & Kahn, Ronald N.**: *Active Portfolio Management* — the Fundamental Law of Active Management, $\text{IR}=\text{IC}\sqrt{B}\text{TC}$ (2nd ed., Ch. 6), the origin of "breadth beats raw IC."
- **Luo, Yin et al.**: "Seven Sins of Quantitative Investing" (Deutsche Bank, 2014) — survivorship, look-ahead, storytelling, data snooping, ... (quoted in AFML Ch. 11). *The failure-mode checklist.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (correlation, IC, $t$-stat) · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (why a weak true edge dies in the noise)
- Data provenance: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (timestamps, vendors, PIT hygiene) · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (turning the cleaned panel into a modelable signal + target)
- Evaluation discipline: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (deflated Sharpe, selection bias) · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]]
- Sibling topic: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Financial NLP & Transcripts]] (alt-data one important special case: text)
- Sub-pages (in-folder): 01 From Zero · 02 Alt-Data Landscape · 03 The Pipeline · 04 Evaluating Signal · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/01-from-zero-intuition|01 · From Zero]] — why alt-data is different, and why latency eats alpha, with the decay demo.
- **Landscape + economics (undergrad/job-seeking):** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/02-alt-data-landscape|02 · Alt-Data Landscape]] (the taxonomy, breadth, uniqueness).
- **Build the pipeline (intermediate):** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/03-the-pipeline|03 · The Pipeline]] → [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/04-evaluating-signal|04 · Evaluating Signal]].
- **Robustness (practitioner/graduate):** [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Financial NLP & Transcripts]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]

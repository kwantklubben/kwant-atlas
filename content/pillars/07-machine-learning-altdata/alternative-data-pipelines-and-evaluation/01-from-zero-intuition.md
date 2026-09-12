---
title: "7.5.1 Alternative Data from Zero"
tags:
  - pillar-machine-learning
  - alternative-data-pipelines-and-evaluation
  - intuition
  - alpha-decay
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (correlation). Everything else is built from scratch on this page.

---

### 1. Intuition & Practical Objective

This page builds the *why* of alternative data with **no prior alt-data knowledge needed**. The objective is one idea: **an edge is only worth what it is worth *before* the rest of the market can see it - so the value of a dataset is decided as much by its timing as by its information content.**

Start with the dumbest question: *if a dataset predicts returns, why doesn't its edge last?* Because a predictive dataset is a temporary *informational monopoly*. You know the retailer's card spend before it reports; you trade; the price drifts toward the number; the earnings arrive; the drift is gone. The moment the vendor sells the same feed to twenty other funds, all twenty trade the same drift, the drift is compressed into a shorter window, and the edge *decays* - not because the information was wrong, but because it stopped being private. López de Prado's rule of thumb (AFML §2.2.4) is the right instinct: the datasets worth the most are the ones that are **hard to store, manipulate, and operate** - because your competitors gave up on them, processed them wrong, or never tried.

Three "aha"s:

1. **Primary, not derived.** Alt-data is *primary information* - it has not yet made it into fundamentals, prices, or analyst commentary (AFML §2.2.4). The tankers moved before the earnings; the parking lots emptied before guidance. Derived analytics (a vendor's "sentiment score") are convenient, but they are priced, opaque, and you are not the sole buyer.
2. **Latency is not a detail - it is the product.** A signal with a 1-week half-life is badly eroded if you can only trade it after 5 days (39% of it is already gone, and the rest is arbitraged). A signal with a 1-year half-life barely notices a week of delay. The *same* information content is a great dataset or a useless one depending on the clock.
3. **Decay is measurable, and therefore plannable.** You do not have to guess how fast an edge dies: fit $\text{IC}(t)\approx\text{IC}_0 e^{-\lambda t}$ to overlapping-horizon ICs, read off the half-life $t_{1/2}=\ln 2/\lambda$, and decide whether your pipeline is fast enough to capture it.

---

### 2. Mathematical Ground Truth & Derivations

**The decay model.** Let the signal's information coefficient at lag $t$ after the event be

$$
\text{IC}(t)=\text{IC}_0\,e^{-\lambda t},\qquad \lambda>0 \text{ the decay rate},\qquad \text{Sharpe}(t)=\text{Sharpe}_0\,e^{-\lambda t}.
$$

This is the continuous-time version of "the alpha is competed away at rate $\lambda$," and it is what the corpus flat-page states directly: high-frequency datasets decay in hours, quarterly alt-data in one to two years.

**Half-life and the value of speed.** Solving $\text{IC}(t_{1/2})=\tfrac12\text{IC}_0$ gives $\lambda=\ln 2/t_{1/2}$. The total alpha available over all horizons from now is the integral

$$
A=\int_0^\infty \text{IC}_0\,e^{-\lambda t}\,dt=\frac{\text{IC}_0}{\lambda}=\frac{\text{IC}_0\,t_{1/2}}{\ln 2}.
$$

If your pipeline delivers the value only at delay $d$ (vendor lag + your processing), the alpha you can still capture is

$$
A(d)=\int_d^\infty \text{IC}_0\,e^{-\lambda t}\,dt=\frac{\text{IC}_0}{\lambda}e^{-\lambda d}
\quad\Longrightarrow\quad \boxed{\;\frac{A(d)}{A}=e^{-\lambda d}=e^{-(\ln 2)\,d/t_{1/2}}\;}.
$$

**Read the boxed formula twice.** The fraction you keep depends *only* on the ratio of your delay to the signal's half-life, $d/t_{1/2}$. A "slow" pipeline (days) is fatal to a fast signal and irrelevant to a slow one. This is the mathematical reason the whole alt-data industry is organized around *latency* and *exclusivity*, not just data volume.

**Decay as a reversion to no-information.** Equivalently, $\text{IC}(t)\to0$ as $t\to\infty$: eventually the information is public and priced, so the residual predictability vanishes. A dataset whose "IC" does *not* decay with horizon is either a genuine slow fundamental signal (rare) or a leak (common - see [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation - how much alpha survives your latency

Stdlib only. This tabulates the boxed formula: for signals with different half-lives, what fraction of the total alpha remains when you can only trade after delays $d=1,5,20,60$ days - and it hands you the *absolute* alpha (`IC0/λ`) so you can see why a fast signal is a small prize even if you are quick.




Read the table. A **7-day half-life** signal (fast card/foot-traffic panel) loses 39% of its edge in 5 days and 86% in 20 days - only a low-latency pipeline can monetize it. A **365-day half-life** signal (slow fundamental alt-data) still keeps 89% of its edge after two months of delay. And the absolute magnitude (`IC0/λ`) says the slow signal is worth **52×** more in total alpha-days. **Speed matters for fast signals; patience is rewarded for slow ones - and the two are different businesses.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"I'll use the data when it arrives" - ignoring the arrival lag in the *backtest*.** The decay math is about the *real* edge; the leak is about the *simulated* one. If your backtest aligns values to their event date while your live pipeline can only act on them 3–5 days later, you will overstate the captured fraction by exactly $1-e^{-\lambda d}$ - for the 7-day signal at $d{=}5$, that is **39% of the edge that does not exist live**.
2. **Assuming decay is exponential (and constant $\lambda$).** Real decay is often *step-like* (a competitor launches → the edge collapses) or *hump-shaped* (covered later, then re-emerges). The exponential fit is a useful first-order model, not a law; treat $\hat\lambda$ as an estimate with error, and re-fit as the vendor sells more.
3. **Confusing uniqueness with information.** A dataset can be genuinely predictive *and* worthless: if twenty funds already trade it, its decay is near-instant and its residual IC is zero. The first principle of §1 - hard-to-process is promising - is really a statement about *decay rate*, not about accuracy.
4. **The latency-feature trap.** Latency is not only about trade delay: a feature computed from a *raw* feed that itself is revised (e.g., a vendor's daily "footfall" restated a week later) has an *effective* delay larger than its nominal one. Audit revision timestamps, not just delivery timestamps.

---

### 5. References

- **López de Prado**, *Advances in Financial Machine Learning*, **§2.2.4** (alternative data is *primary* information; "data that is hard to store, manipulate and operate is always the most promising"; the individuals/business-process/sensors taxonomy). *The primary source for the framing on this page.*
- **Kolanovic & Krishnamachari**, *Big Data and AI Strategies* (J.P. Morgan, 2017)
- **Guida, Tony**, *Big Data and Machine Learning in Quantitative Investment* (Wiley, 2019)
- **Grinold & Kahn**, *Active Portfolio Management*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Index Hub]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]]
- Forward: [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/02-alt-data-landscape|02 · Alt-Data Landscape]] → [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/03-the-pipeline|03 · The Pipeline]]
- Where the numbers come from: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (vendor lags, PIT hygiene) · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (turning the cleaned panel into a signal)

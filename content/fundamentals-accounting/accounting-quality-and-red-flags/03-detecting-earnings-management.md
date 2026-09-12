---
title: "A.5.3 Detecting Earnings Management"
tags:
  - fundamentals-accounting
  - accounting-quality-and-red-flags
  - earnings-management
  - discretionary-accruals
  - jones-model
---

**Basic Prerequisites:** [[fundamentals-accounting/accounting-quality-and-red-flags/02-the-accrual-anomaly|02 · The Accrual Anomaly]] (total accruals and persistence).

---

### 1. Intuition & Practical Objective

Page 02 gave you *total* accruals and showed they predict returns. But "this firm has high accruals" is a weak accusation: a firm growing sales 40% *should* have high accruals - receivables grow with sales, inventory grows with sales, and none of that is dishonest. The accusation a forensic analyst actually wants to make is stronger and narrower: **how much of this firm's accruals cannot be explained by its economic circumstances?** That residual is **discretionary accruals** - the part a manager chose, as opposed to the part the business forced.

Dechow, Sloan & Sweeney (1995) is the paper that put this on a rigorous footing. It does not propose one model; it **evaluates a family of competing models** for the nondiscretionary benchmark and asks two questions that decide everything:

1. **Specification** - does the model falsely flag innocent firms (type I error)?
2. **Power** - does the model actually catch real earnings management (type II error)?

Their answers, which are the operating manual for every discretionary-accrual study since:

- **On random samples, all the models are fine.** Specification is not the problem.
- **For small manipulations, all the models are weak.** They have low power for earnings management of **1–5% of total assets** - i.e. plenty of real-world manipulation is simply invisible to these tools.
- **When performance is extreme (very good or very bad years), all models reject the null too often.** This is the killer: the models mis-specify precisely in the firms you most care about, because they fail to fully control for performance.
- **A modified version of the Jones (1991) model has the most power**, because it adjusts for the one thing the original Jones model wrongly assumes: that *revenue is nondiscretionary*.

The practical objective: build the Jones and Modified Jones machinery from scratch, see *why* the modification matters, and internalise the humility that comes with "all models are weak for small manipulations."

---

### 2. Mathematical Ground Truth & Derivations

**The decomposition.** Start from total accruals scaled by lagged total assets, $TA_t$. A model of the *nondiscretionary* component lets you split them:

$$
\text{TA}_t = \underbrace{\text{NDA}_t}_{\text{model says this is normal}} + \underbrace{\text{DA}_t}_{\text{the residual = "management"}}.
$$

**Model 1 - Healy (1985).** Nondiscretionary accruals are a **constant** (the average total accruals of the estimation period). Simple, and appropriate if accruals are white noise around a stable mean.

**Model 2 - DeAngelo (1986).** Nondiscretionary accruals are **last period's total accruals** - a random-walk benchmark, a special case of Healy with a one-year estimation period. Better if accruals follow a random walk.

**Model 3 - the Jones (1991) model.** Relaxes "constant" by explicitly modelling *economic circumstances*:

$$
\text{NDA}_t = \alpha_1\!\left(\frac{1}{A_{t-1}}\right) + \alpha_2\!\left(\frac{\Delta REV_t}{A_{t-1}}\right) + \alpha_3\!\left(\frac{PPE_t}{A_{t-1}}\right), \tag{6}
$$

where $\Delta REV_t$ is the revenue change, $PPE_t$ is gross property/plant/equipment, $A_{t-1}$ is lagged total assets, and the $(1/A_{t-1})$ term is a scaling control. The firm-specific parameters are estimated by OLS **in an estimation period** free of hypothesised management:

$$
\frac{TA_t}{A_{t-1}} = a_1\!\left(\frac{1}{A_{t-1}}\right) + a_2\!\left(\frac{\Delta REV_t}{A_{t-1}}\right) + a_3\!\left(\frac{PPE_t}{A_{t-1}}\right) + \nu_t.
$$

Jones reports the model explains about **a quarter** of the variation in total accruals.

**Model 4 - the Modified Jones model (Dechow, Sloan & Sweeney's recommendation).** The flaw in Jones: it assumes *revenue is nondiscretionary*, so a manager who stuffs revenue at year-end inflates $\Delta REV$, the model *attributes* that rise to "normal," and the manipulation is subtracted away - the estimate of DA is **biased toward zero**. The fix: in the **event period only**, adjust the revenue change for the change in receivables:

$$
\boxed{\;\text{NDA}_t = \alpha_1\!\left(\frac{1}{A_{t-1}}\right) + \alpha_2\!\left(\frac{\Delta REV_t - \Delta REC_t}{A_{t-1}}\right) + \alpha_3\!\left(\frac{PPE_t}{A_{t-1}}\right)\;} \tag{7}
$$

Parameters come from the **original** Jones estimation. The logic: it is easier to manage earnings through **credit sales** than cash sales, and a credit sale raises receivables. Subtracting $\Delta REC$ removes the receivable-side inflation from the "normal" benchmark, so the managed revenue stays in the residual where it belongs. The model's *assumption* is the reverse of Jones's: **all** change in credit sales in the event period is treated as management.

**Model 5 - the Industry model (Dechow & Sloan 1991).** Nondiscretionary accruals track the industry median rather than the firm's own revenue/PPE:

$$
\text{NDA}_t = \gamma_1 + \gamma_2\,\text{median}_{industry}\!\left(\frac{TA_t}{A_{t-1}}\right).
$$

Good when industry factors dominate; bad when a firm's circumstances diverge from its peers, and dangerous when a manipulation is *common across an industry* (it hides in the median).

> **The performance-control warning (the paper's biggest practical lesson).** All models are mis-specified in extreme-performance firm-years: the benchmark fails to capture how accruals *should* move when performance is unusual, so the residual absorbs performance rather than management. Any discretionary-accrual test built on an extreme-performance sample must add a performance control or it will find "management" everywhere.

---

### 3. Computational Implementation - Jones vs. Modified Jones, from scratch

Stdlib only, no numpy: the OLS is solved with normal equations and Gaussian elimination. The script simulates a firm panel whose total accruals follow the Jones process, injects a *known* amount of credit-sales earnings management, estimates the model on an **unmanaged estimation period**, and then measures the average discretionary accrual each model recovers. It runs the experiment at two manipulation sizes, because the size is what determines whether detection is even possible.



The output is exactly the paper's story, reproduced on simulated data. **Jones recovers 0.0720 of a true 0.0800 - a −0.0080 bias toward zero, because it "explains away" 10% of the injection as normal revenue.** Modified Jones recovers 0.0822 (bias $+0.0022$). At **1% of assets** the picture inverts the naive expectation: Jones misses the manipulation entirely (detection 0.00), while Modified Jones catches most of it (0.64) - the *power* advantage Dechow et al. found.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Low power is the base case, not a bug.** Nobody's discretionary-accrual model reliably detects management below ~5% of assets. If your screen finds "no earnings management" at a firm, the honest statement is *"no management large enough for this tool to see"* - and small manipulation is common and durable. Report the power, never just the p-value.
2. **Extreme performance contaminates the residual.** A firm having a catastrophic year *must* have extreme accruals (write-downs, provisions). The benchmark under-controls for it, so DA spikes and the model screams "management" when the truth is "a bad year." Add a performance control (e.g. lagged ROA) or restrict the sample.
3. **The models eat the manipulation they are meant to find.** Jones removes revenue-driven management; the Industry model removes management common to the whole industry; a model with a performance control removes performance-driven management. Every control you add removes *both* nondiscretionary accruals and the discretionary accruals correlated with them. This is the fundamental tension: **you can never fully separate the two, only trade bias against variance.**
4. **Parameter estimation needs a clean estimation period.** If the firm manages earnings every year (serial manipulation), the estimation period is contaminated and the benchmark is wrong. Dechow et al.'s assumption - reported earnings are *unmanaged* in the estimation window - is an assumption about circumstances, not a fact; when it fails, DA is unreliable.
5. **Discretion is not the same as fraud.** Discretionary accruals measure *deviation from a model*, which includes legitimate business judgement, differing accounting policies, and a firm merely growing faster than its peers. Treating every high-DA firm as fraudulent is the model's most common misuse.

---

### 5. References

- **Dechow, Patricia M., Sloan, Richard G. & Sweeney, Amy P.**: "Detecting Earnings Management" (*TAR*, 70(2), 193–225, 1995)
- **Jones, Jennifer J.**: "Earnings Management During Import Relief Investigations" (*JAR*, 29(2), 193–228, 1991)
- **Healy, Paul M.**: "The Effect of Bonus Schemes on Accounting Decisions" (*JAE*, 7, 85–107, 1985)
- **DeAngelo, Linda E.**: "Accounting Numbers as Market Valuation Substitutes…" (*JAR*, 24(2), 400–420, 1986)
- **Healy, Paul M. & Wahlen, James M.**: "A Review of the Earnings Management Literature…" (*Accounting Horizons*, 13(4), 365–383, 1999)
- **Dechow, Ge & Schrand**: "Understanding Earnings Quality…" (*JAE*, 2010)

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/accounting-quality-and-red-flags/02-the-accrual-anomaly|02 · The Accrual Anomaly]] · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Index Hub]]
- Forward: [[fundamentals-accounting/accounting-quality-and-red-flags/04-red-flags-and-shenanigans|04 · Red Flags & Shenanigans]] (the qualitative games this machinery tries to quantify) · [[fundamentals-accounting/accounting-quality-and-red-flags/06-advanced-extensions|06 · Advanced Extensions]] (the Beneish M-score as a non-residual alternative)
- Method: [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/index|Quantitative Research]] (specification vs. power is the same trade-off everywhere)

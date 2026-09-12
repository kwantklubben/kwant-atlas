---
title: "4.14.4 ESG Scores, Temperature Alignment & the Carbon Premium"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - esg-ratings
  - carbon-premium
  - temperature-alignment
  - greenium
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · Physical & Transition Risk]] and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (cross-sectional regression, standard errors).

---

### 1. Intuition & Practical Objective

Two distinct products are routinely confused under the ESG label, and a quant must separate them: a **rating** (an ordinal summary of a firm's ESG *performance*, produced by a private methodology) and a **price signal** (a return premium or discount in the cross-section, produced by the market). The first is an input you must audit; the second is an equilibrium fact you can measure. This page covers both, plus the third object in the family: **temperature alignment**, which converts an emissions trajectory into a single number in °C.

Three things a practitioner must know before using any of them:

1. **A rating is an aggregation of contested indicators, and the aggregation itself is proprietary.** Berg, Kölbel & Rigobon (2022) decompose the divergence between six major raters into **scope** (which attributes are assessed), **measurement** (which indicator measures a given attribute) and **weight** (how indicators are combined), and find the average pairwise rating correlation is only **0.54**, ranging $0.38$–$0.71$ - against $\approx0.99$ for credit ratings. The decomposition attributes **56% of the divergence to measurement, 38% to scope and only 6% to weights**. That ordering is the punchline: aligning weighting schemes - the obvious fix - would remove almost nothing. The problem is *how the data are generated*.
2. **Temperature alignment is an interpolation between benchmark pathways, not a measurement.** Given a portfolio's cumulative emissions over a horizon, one finds the two IPCC/NGFS-consistent pathways it sits between and interpolates a temperature. It is a *benchmarking device*: transparent, monotone, and entirely dependent on the benchmark table and the emissions boundary feeding it.
3. **The cross-sectional price of carbon emissions has been documented with *both* signs.** Bolton & Kacperczyk (2021) find that US stocks of firms with **higher** total CO2 emissions earn **higher** returns, controlling for size, book-to-market and other predictors - a **carbon (brown) premium** interpreted as compensation for transition risk. Pástor, Stambaugh & Taylor (2021) show theoretically that **green** assets command **lower** expected returns (investors accept a lower return for green holdings - a "greenium") but can outperform *after climate-concern shocks*, because they hedge transition risk. These are not contradictory: a **level** effect (a greenium in expected returns) and a **news** effect (green outperformance when climate concerns rise) coexist. In the green-bond market the level effect was measured by Zerbib (2019) as a yield premium of roughly $-2$ basis points for green bonds.

The practical objective: build a score, measure its instability, map a portfolio to a temperature, and estimate the carbon premium - **with standard errors attached**, because a premium without an error bar is a story.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 How an ESG score is built (and why raters disagree)

Following Berg, Kölbel & Rigobon's notation, rater $k$'s rating of firm $f$ is a linear aggregation of category scores $C_{fkj}$ with rater-specific weights $w_{kj}$:

$$
\boxed{\ R_{fk}=\sum_{j\in\mathcal C_k} C_{fkj}\,w_{kj},\qquad w_{kj}\ge0\ }
$$

Three divergence channels follow immediately:
$$
\underbrace{\mathcal C_k\ne\mathcal C_{k'}}_{\text{scope}},\qquad \underbrace{C_{fkj}\ne C_{fk'j}\ \text{on the same attribute}}_{\text{measurement}},\qquad \underbrace{w_{kj}\ne w_{k'j}}_{\text{weight}}.
$$

Taking variances of $D^{k,k'}_{f}=R_{fk}-R_{fk'}$ and splitting by an arithmetic decomposition gives the reported shares $(38\%,56\%,6\%)$. **Consequence for a quant:** the rating is a *noisy proxy* whose noise is not independent across the object being measured - hence a rater fixed effect (a "halo") beyond idiosyncratic noise.

**Rank agreement.** Because ratings are ordinal in use, the appropriate agreement statistic is the **Spearman rank correlation**: replace each $R_{fk}$ by its average rank $\bar r_{fk}$ (ties share the mean rank) and take the Pearson correlation of the rank vectors,
$$
\rho_s=\frac{\sum_f(\bar r_{f}-\bar{\bar r})(\bar r'_{f}-\bar{\bar r'})}{\sqrt{\sum_f(\bar r_f-\bar{\bar r})^2}\sqrt{\sum_f(\bar r'_f-\bar{\bar r'})^2}}.
$$

#### 2.2 Implied temperature rise by benchmark-pathway interpolation

Let a portfolio have cumulative emissions intensity $C$ (tCO2e per $ $\$1m of revenue over the horizon), and let \{(T_j,C_j)\}_{j=1}^m$ be a table of benchmark pathways with increasing temperature outcomes and increasing cumulative intensities. The ITR is the piecewise-linear interpolation

$$
\boxed{\ \mathrm{ITR}(C)=T_j+(T_{j+1}-T_j)\frac{C-C_j}{C_{j+1}-C_j}\quad\text{for }C\in[C_j,C_{j+1}],\qquad \mathrm{ITR}=T_1\ \text{for }C\le C_1\ }
$$

with **no extrapolation beyond the last benchmark**: a portfolio worse than the worst pathway is reported as "worse than $T_m$", not as a fabricated $4.1^\circ$C. The physical justification for a monotone cumulative-emissions-to-warming map is the TCRE relation (IPCC AR5: $0.8$–$2.5^\circ$C per 1000 PgC, i.e. $\approx0.2$–$0.7^\circ$C per 1000 GtCO2); the *benchmark table* is a modelling choice, and belongs in the disclosure.

#### 2.3 The carbon premium as a cross-sectional regression

The canonical specification regresses realised returns on a measure of emissions exposure with controls:

$$
r_f=a+b\,\ln E_f+\mathbf c^{\top}\mathbf X_f+\varepsilon_f,\qquad \hat b=(\mathbf X^{\top}\mathbf X)^{-1}\mathbf X^{\top}\mathbf r,\qquad \widehat{\mathrm{se}}(\hat b_j)=\sqrt{\hat\sigma^2\,[(\mathbf X^{\top}\mathbf X)^{-1}]_{jj}}
$$

with $\hat\sigma^2=\mathrm{RSS}/(n-k)$. Interpretation:
- $\hat b>0$ (brown premium): high-emitting firms earned *higher* realised returns, the Bolton–Kacperczyk finding - compensation for transition risk.
- $\hat b<0$ (greenium in realised returns): the low-emission firms outperformed - the Pástor–Stambaugh–Taylor regime after a climate-concern shock.
Both regimes are *the same estimator on different samples*, which is exactly the discipline the carbon-premium literature requires: report the sample, the shock, and the standard error. A premium is a **conditional** moment, not a constant.

---

### 3. Computational Implementation - score divergence, temperature alignment and the premium

Three panels: (A) three raters scoring eight firms, with rank correlations; (B) implied temperature rise for a portfolio under two emissions boundaries; (C) an OLS that recovers the carbon premium and then shows its sampling dispersion. Standard library only.




**Panel (A).** Firm **A** is ranked $2.5$ by R1 and $8.0$ (last) by R3 - the *identical* firm, the *identical* pillars, only different weights and one alternative environmental indicator. Four of eight firms move three or more places. The mean rank correlation is $+0.439$, in the same regime as Berg et al.'s $0.54$ empirical average. **A portfolio "constructed on ESG scores" is constructed on a rater, not on a fact.**

**Panel (B).** The ITR interpolation gives $1.98^\circ$C for this book - but $82.8\%$ of the cumulative emissions come from the coal and oil holdings. Widen the boundary to Scope 1+2+3 and the same portfolio is *beyond the $3.2^\circ$C benchmark*: the interpolation refuses to extrapolate, which is the correct behaviour (§2.2). **The alignment label is a boundary choice, not a property of the holdings.**

**Panel (C).** The OLS recovers the planted premium exactly ($+0.0180$ vs $+0.018$; $-0.0200$ vs $-0.020$) on identical firms under two pricing regimes - the brown-premium and greenium cases of §2.3, in one estimator. But four disjoint subsamples of the *same* regime give $\hat b\in[+0.0114,+0.0217]$: **the sign is stable, the magnitude is not.** That is the honest report of a carbon premium.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating a rating as a variable with small measurement error.** Rating divergence is structural, not noise: measurement contributes $56\%$ and it is *correlated across categories within a rater* (the halo effect), so averaging raters does not cleanly cancel it (Berg et al. 2022).
2. **Rating restatement (the "rewriting history" problem).** ESG data providers have retroactively revised historical scores, so a backtest built on a vendor's *as-of-today* history is using information that was not available in real time - a look-ahead bias generated by the data vendor rather than by the researcher (Berg, Fabisik & Sautner). Tests of ESG signals must use point-in-time vintages.
3. **Weight-shifting as a "fix".** Because weights explain only $6\%$ of divergence, re-weighting the pillars changes the label without changing the disagreement; the binding constraint is measurement and scope.
4. **ITR as a measured quantity.** An ITR is an interpolation against a chosen benchmark table, computed from a chosen scope boundary, over a chosen horizon. Reporting "$1.98^\circ$C" without the table, the boundary and the horizon is reporting a spreadsheet cell as a physical fact.
5. **Reading a carbon premium without a sample.** $\hat b$ flips sign with the regime (panel C) and its magnitude varies by a factor of two across subsamples. A premium is a *conditional* moment: quote the period, the controls and the standard error.
6. **Ignoring the demand-side explanation.** A "greenium" in expected returns (Pástor–Stambaugh–Taylor) is an equilibrium consequence of investor preferences, not evidence that green assets are safer; it coexists with a brown *risk* premium. Confusing the preference-driven and risk-driven components mis-specifies the hedge.
7. **Scope/aggregation laundering in alignment metrics.** Portfolio-level intensity can be reduced by *reweighting* rather than by real-world change - the mechanical decomposition between "portfolio mix" and "financed emissions" must be disclosed, or a portfolio's ITR becomes a portfolio-construction artefact.

---

### 5. Canonical Literature & Study References

- **Berg, F., Kölbel, J.F. & Rigobon, R.** - *Aggregate Confusion: The Divergence of ESG Ratings*, *Review of Finance* **26**(6):1315–1344 (2022) - the scope/measurement/weight decomposition ($38\%/56\%/6\%$), the correlation range $0.38$–$0.71$, and the rater (halo) effect. *Primary source, read from the corpus PDF.*
- **Berg, F., Fabisik, K. & Sautner, Z.** - *Rewriting History II: The (Un)Predictable Past of ESG Ratings* (ECGI Finance Working Paper 708/2020; circulated as *Is History Repeating Itself?*) - retroactive restatement of ESG history and the resulting look-ahead bias.
- **Bolton, P. & Kacperczyk, M.** - *Do investors care about carbon risk?*, *Journal of Financial Economics* **142**(2):517–549 (2021) - the carbon (brown) premium in US equities.
- **Pástor, Ľ., Stambaugh, R.F. & Taylor, L.A.** - *Sustainable investing in equilibrium*, *Journal of Financial Economics* **142**(2):550–571 (2021) - greenium in expected returns; and *Dissecting green returns*, *Journal of Financial Economics* **146**(2):403–424 (2022) - climate-news-driven outperformance and its reversal.
- **Zerbib, O.D.** - *The effect of pro-environmental preferences on bond prices: Evidence from green bonds*, *Journal of Banking & Finance* **98**:39–60 (2019) - the green-bond yield premium (order $-2$ basis points).
- **Andersson, M., Bolton, P. & Samama, F.** - *Hedging Climate Risk*, *Financial Analysts Journal* **72**(3):13–32 (2016) - carbon-efficient portfolios at equal tracking error.
- **TCFD**, *Recommendations* (2017) and **SBTi**, *Foundations for Science-Based Net-Zero Target Setting* - the pathway/budget logic behind temperature alignment.
- **IPCC**, *Climate Change 2013: The Physical Science Basis* (AR5, WG1 Ch. 12) - TCRE, the physical basis for a cumulative-emissions-to-warming map.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · Physical & Transition Risk]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios & Stress Testing]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (where a carbon factor would be estimated) · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Timing]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]

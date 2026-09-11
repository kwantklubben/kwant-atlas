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

1. **A rating is an aggregation of contested indicators, and the aggregation itself is proprietary.** Berg, Kölbel & Rigobon (2022) decompose the divergence between six major raters into **scope** (which attributes are assessed), **measurement** (which indicator measures a given attribute) and **weight** (how indicators are combined), and find the average pairwise rating correlation is only **0.54**, ranging $0.38$–$0.71$ — against $\approx0.99$ for credit ratings. The decomposition attributes **56% of the divergence to measurement, 38% to scope and only 6% to weights**. That ordering is the punchline: aligning weighting schemes — the obvious fix — would remove almost nothing. The problem is *how the data are generated*.
2. **Temperature alignment is an interpolation between benchmark pathways, not a measurement.** Given a portfolio's cumulative emissions over a horizon, one finds the two IPCC/NGFS-consistent pathways it sits between and interpolates a temperature. It is a *benchmarking device*: transparent, monotone, and entirely dependent on the benchmark table and the emissions boundary feeding it.
3. **The cross-sectional price of carbon emissions has been documented with *both* signs.** Bolton & Kacperczyk (2021) find that US stocks of firms with **higher** total CO2 emissions earn **higher** returns, controlling for size, book-to-market and other predictors — a **carbon (brown) premium** interpreted as compensation for transition risk. Pástor, Stambaugh & Taylor (2021) show theoretically that **green** assets command **lower** expected returns (investors accept a lower return for green holdings — a "greenium") but can outperform *after climate-concern shocks*, because they hedge transition risk. These are not contradictory: a **level** effect (a greenium in expected returns) and a **news** effect (green outperformance when climate concerns rise) coexist. In the green-bond market the level effect was measured by Zerbib (2019) as a yield premium of roughly $-2$ basis points for green bonds.

The practical objective: build a score, measure its instability, map a portfolio to a temperature, and estimate the carbon premium — **with standard errors attached**, because a premium without an error bar is a story.

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

Taking variances of $D^{k,k'}_{f}=R_{fk}-R_{fk'}$ and splitting by an arithmetic decomposition gives the reported shares $(38\%,56\%,6\%)$. **Consequence for a quant:** the rating is a *noisy proxy* whose noise is not independent across the object being measured — hence a rater fixed effect (a "halo") beyond idiosyncratic noise.

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
- $\hat b>0$ (brown premium): high-emitting firms earned *higher* realised returns, the Bolton–Kacperczyk finding — compensation for transition risk.
- $\hat b<0$ (greenium in realised returns): the low-emission firms outperformed — the Pástor–Stambaugh–Taylor regime after a climate-concern shock.
Both regimes are *the same estimator on different samples*, which is exactly the discipline the carbon-premium literature requires: report the sample, the shock, and the standard error. A premium is a **conditional** moment, not a constant.

---

### 3. Computational Implementation — score divergence, temperature alignment and the premium

Three panels: (A) three raters scoring eight firms, with rank correlations; (B) implied temperature rise for a portfolio under two emissions boundaries; (C) an OLS that recovers the carbon premium and then shows its sampling dispersion. Standard library only.

```python
# c5_scores.py — ESG-rating disagreement, implied temperature rise, carbon premium (page 04 §3)
import math, random

# ---------- (A) three raters, one set of firms: why ESG scores disagree ----------
firms = ["A", "B", "C", "D", "E", "F", "G", "H"]
E_  = [90, 45, 70, 55, 30, 80, 60, 40]        # environmental pillar (raters 1 & 2)
S_  = [40, 85, 60, 55, 70, 30, 75, 65]        # social pillar
G_  = [35, 40, 80, 50, 90, 45, 60, 75]        # governance pillar
Ep  = [60, 55, 65, 50, 40, 70, 55, 60]        # rater 3's *different indicator* for the same attribute
W   = [(0.50, 0.25, 0.25), (0.20, 0.40, 0.40), (1/3, 1/3, 1/3)]
Edata = [E_, E_, Ep]
raters = ["R1  (E-tilted weights)", "R2  (S/G-tilted weights)", "R3  (equal weights, alt E data)"]
sc = [[W[k][0] * Edata[k][i] + W[k][1] * S_[i] + W[k][2] * G_[i] for i in range(8)] for k in range(3)]


def ranks(v):
    """1 = best; ties share the average rank."""
    o = sorted(range(len(v)), key=lambda i: -v[i]); out = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and abs(v[o[j + 1]] - v[o[i]]) < 1e-9:
            j += 1
        for t in range(i, j + 1):
            out[o[t]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return out


def pearson(x, y):
    n = len(x); mx = sum(x) / n; my = sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (sx * sy)


rk = [ranks(s) for s in sc]
for k in range(3):
    best = sorted(firms, key=lambda f: rk[k][firms.index(f)])[:3]
    print(f"(A) {raters[k]:32s} top-3: {best}")
    print(f"    ranks  " + "  ".join(f"{f}={rk[k][i]:.1f}" for i, f in enumerate(firms)))
cors = []
for a in range(3):
    for b in range(a + 1, 3):
        c = pearson(rk[a], rk[b]); cors.append(c)
        print(f"    Spearman  R{a+1}-R{b+1} = {c:+.3f}")
print(f"    mean pairwise rank correlation = {sum(cors)/len(cors):+.3f}   (Berg et al. 2022: mean 0.54, range 0.38-0.71)")
mv = [abs(rk[0][i] - rk[2][i]) for i in range(8)]
print(f"    firms moving >= 3 ranks, R1 -> R3: {sum(1 for m in mv if m >= 3)} of 8   (largest move {max(mv):.1f} places)")

# ---------- (B) implied temperature rise by benchmark-pathway interpolation ----------
book = [("Coal utility", 0.10, 90_000.0), ("Oil major", 0.15, 45_000.0), ("Cement", 0.05, 40_000.0),
        ("Tech", 0.40, 2_500.0), ("Bank", 0.30, 900.0)]
bench = [(1.5, 12_000.0), (1.8, 16_000.0), (2.1, 21_000.0), (2.7, 30_000.0), (3.2, 40_000.0)]
C = sum(w * ci for _, w, ci in book)


def itr(c):
    """Interpolate between benchmark pathways; None beyond the worst benchmark."""
    if c <= bench[0][1]:
        return bench[0][0]
    for (t0, c0), (t1, c1) in zip(bench, bench[1:]):
        if c <= c1:
            return t0 + (t1 - t0) * (c - c0) / (c1 - c0)
    return None


fmt = lambda c: f"{itr(c):.2f}C" if itr(c) is not None else "> 3.2C (beyond benchmark scale)"
print(f"(B) portfolio cumulative emissions intensity = {C:,.0f} tCO2e per $m revenue")
print(f"    implied temperature rise (ITR) = {fmt(C)}")
big = sorted(book, key=lambda x: -x[1] * x[2])
print(f"    {big[0][0]} + {big[1][0]} supply {100*(big[0][1]*big[0][2]+big[1][1]*big[1][2])/C:.1f}% of those cumulative emissions")
print(f"    same portfolio, Scope 1+2   data -> ITR = {fmt(19_020.0)}")
print(f"    same portfolio, Scope 1+2+3 data -> ITR = {fmt(100_000.0)}")

# ---------- (C) the carbon premium: OLS recovering a planted coefficient ----------
def ols(X, y):
    """Returns (beta, se). Augmented [X'X | I | X'y] Gauss-Jordan gives the inverse and the solution."""
    k = len(X[0]); n = len(X); w = 2 * k + 1
    M = [[0.0] * w for _ in range(k)]
    for a in range(k):
        for b in range(k):
            M[a][b] = sum(X[i][a] * X[i][b] for i in range(n))
        M[a][k + a] = 1.0
        M[a][2 * k] = sum(X[i][a] * y[i] for i in range(n))
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        d = M[c][c]
        M[c] = [v / d for v in M[c]]
        for r in range(k):
            if r != c:
                f = M[r][c]
                M[r] = [M[r][j] - f * M[c][j] for j in range(w)]
    beta = [M[i][2 * k] for i in range(k)]
    rss = sum((y[i] - sum(beta[a] * X[i][a] for a in range(k))) ** 2 for i in range(n))
    s2 = rss / (n - k)
    return beta, [math.sqrt(s2 * M[i][k + i]) for i in range(k)]


def make(seed, beta_em, n):
    random.seed(seed); X = []; y = []
    for _ in range(n):
        le = random.gauss(0.0, 1.0); bm = random.gauss(0.0, 1.0)
        X.append([1.0, le, bm])
        y.append(0.02 + beta_em * le + 0.03 * bm + random.gauss(0.0, 0.06))
    return X, y


print("(C) cross-section  r_i = a + b*ln(E_i) + c*BM_i + e_i   (n = 400, noise sd 0.06, identical firms)")
for label, planted, seed in (("calm period           ", 0.018, 1), ("climate-concern period", -0.020, 1)):
    (a, b, c), (_, sb, sc_) = ols(*make(seed, planted, 400))
    print(f"    {label}:  b_hat = {b:+.4f} (se {sb:.4f}, t = {b/sb:+.1f})  [planted {planted:+.3f}]   c_hat = {c:+.4f} (t = {c/sc_:+.1f})")
print("    stability of b_hat on four disjoint subsamples of the calm-period data (n = 100 each):")
ests = []
for s in (11, 12, 13, 14):
    (_, b, _), (_, sb, _) = ols(*make(s, 0.018, 100))
    ests.append(b)
    print(f"      seed {s}: b_hat = {b:+.4f} (se {sb:.4f})")
print(f"      range [{min(ests):+.4f}, {max(ests):+.4f}]  ->  the premium is estimated, not observed")
```
```
(A) R1  (E-tilted weights)           top-3: ['C', 'A', 'G']
    ranks  A=2.5  B=7.5  C=1.0  D=7.5  E=5.5  F=4.0  G=2.5  H=5.5
(A) R2  (S/G-tilted weights)         top-3: ['C', 'E', 'G']
    ranks  A=7.0  B=5.0  C=1.5  D=6.0  E=1.5  F=8.0  G=3.0  H=4.0
(A) R3  (equal weights, alt E data)  top-3: ['C', 'E', 'H']
    ranks  A=8.0  B=5.0  C=1.0  D=6.0  E=2.5  F=7.0  G=4.0  H=2.5
    Spearman  R1-R2 = +0.226
    Spearman  R1-R3 = +0.171
    Spearman  R2-R3 = +0.922
    mean pairwise rank correlation = +0.439   (Berg et al. 2022: mean 0.54, range 0.38-0.71)
    firms moving >= 3 ranks, R1 -> R3: 4 of 8   (largest move 5.5 places)
(B) portfolio cumulative emissions intensity = 19,020 tCO2e per $m revenue
    implied temperature rise (ITR) = 1.98C
    Coal utility + Oil major supply 82.8% of those cumulative emissions
    same portfolio, Scope 1+2   data -> ITR = 1.98C
    same portfolio, Scope 1+2+3 data -> ITR = > 3.2C (beyond benchmark scale)
(C) cross-section  r_i = a + b*ln(E_i) + c*BM_i + e_i   (n = 400, noise sd 0.06, identical firms)
    calm period           :  b_hat = +0.0180 (se 0.0028, t = +6.5)  [planted +0.018]   c_hat = +0.0316 (t = +10.5)
    climate-concern period:  b_hat = -0.0200 (se 0.0028, t = -7.2)  [planted -0.020]   c_hat = +0.0316 (t = +10.5)
    stability of b_hat on four disjoint subsamples of the calm-period data (n = 100 each):
      seed 11: b_hat = +0.0182 (se 0.0056)
      seed 12: b_hat = +0.0114 (se 0.0061)
      seed 13: b_hat = +0.0217 (se 0.0050)
      seed 14: b_hat = +0.0212 (se 0.0060)
      range [+0.0114, +0.0217]  ->  the premium is estimated, not observed
```

**Panel (A).** Firm **A** is ranked $2.5$ by R1 and $8.0$ (last) by R3 — the *identical* firm, the *identical* pillars, only different weights and one alternative environmental indicator. Four of eight firms move three or more places. The mean rank correlation is $+0.439$, in the same regime as Berg et al.'s $0.54$ empirical average. **A portfolio "constructed on ESG scores" is constructed on a rater, not on a fact.**

**Panel (B).** The ITR interpolation gives $1.98^\circ$C for this book — but $82.8\%$ of the cumulative emissions come from the coal and oil holdings. Widen the boundary to Scope 1+2+3 and the same portfolio is *beyond the $3.2^\circ$C benchmark*: the interpolation refuses to extrapolate, which is the correct behaviour (§2.2). **The alignment label is a boundary choice, not a property of the holdings.**

**Panel (C).** The OLS recovers the planted premium exactly ($+0.0180$ vs $+0.018$; $-0.0200$ vs $-0.020$) on identical firms under two pricing regimes — the brown-premium and greenium cases of §2.3, in one estimator. But four disjoint subsamples of the *same* regime give $\hat b\in[+0.0114,+0.0217]$: **the sign is stable, the magnitude is not.** That is the honest report of a carbon premium.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating a rating as a variable with small measurement error.** Rating divergence is structural, not noise: measurement contributes $56\%$ and it is *correlated across categories within a rater* (the halo effect), so averaging raters does not cleanly cancel it (Berg et al. 2022).
2. **Rating restatement (the "rewriting history" problem).** ESG data providers have retroactively revised historical scores, so a backtest built on a vendor's *as-of-today* history is using information that was not available in real time — a look-ahead bias generated by the data vendor rather than by the researcher (Berg, Fabisik & Sautner). Tests of ESG signals must use point-in-time vintages.
3. **Weight-shifting as a "fix".** Because weights explain only $6\%$ of divergence, re-weighting the pillars changes the label without changing the disagreement; the binding constraint is measurement and scope.
4. **ITR as a measured quantity.** An ITR is an interpolation against a chosen benchmark table, computed from a chosen scope boundary, over a chosen horizon. Reporting "$1.98^\circ$C" without the table, the boundary and the horizon is reporting a spreadsheet cell as a physical fact.
5. **Reading a carbon premium without a sample.** $\hat b$ flips sign with the regime (panel C) and its magnitude varies by a factor of two across subsamples. A premium is a *conditional* moment: quote the period, the controls and the standard error.
6. **Ignoring the demand-side explanation.** A "greenium" in expected returns (Pástor–Stambaugh–Taylor) is an equilibrium consequence of investor preferences, not evidence that green assets are safer; it coexists with a brown *risk* premium. Confusing the preference-driven and risk-driven components mis-specifies the hedge.
7. **Scope/aggregation laundering in alignment metrics.** Portfolio-level intensity can be reduced by *reweighting* rather than by real-world change — the mechanical decomposition between "portfolio mix" and "financed emissions" must be disclosed, or a portfolio's ITR becomes a portfolio-construction artefact.

---

### 5. Canonical Literature & Study References

- **Berg, F., Kölbel, J.F. & Rigobon, R.** — *Aggregate Confusion: The Divergence of ESG Ratings*, *Review of Finance* **26**(6):1315–1344 (2022) — the scope/measurement/weight decomposition ($38\%/56\%/6\%$), the correlation range $0.38$–$0.71$, and the rater (halo) effect. *Primary source, read from the corpus PDF.*
- **Berg, F., Fabisik, K. & Sautner, Z.** — *Rewriting History II: The (Un)Predictable Past of ESG Ratings* (ECGI Finance Working Paper 708/2020; circulated as *Is History Repeating Itself?*) — retroactive restatement of ESG history and the resulting look-ahead bias.
- **Bolton, P. & Kacperczyk, M.** — *Do investors care about carbon risk?*, *Journal of Financial Economics* **142**(2):517–549 (2021) — the carbon (brown) premium in US equities.
- **Pástor, Ľ., Stambaugh, R.F. & Taylor, L.A.** — *Sustainable investing in equilibrium*, *Journal of Financial Economics* **142**(2):550–571 (2021) — greenium in expected returns; and *Dissecting green returns*, *Journal of Financial Economics* **146**(2):403–424 (2022) — climate-news-driven outperformance and its reversal.
- **Zerbib, O.D.** — *The effect of pro-environmental preferences on bond prices: Evidence from green bonds*, *Journal of Banking & Finance* **98**:39–60 (2019) — the green-bond yield premium (order $-2$ basis points).
- **Andersson, M., Bolton, P. & Samama, F.** — *Hedging Climate Risk*, *Financial Analysts Journal* **72**(3):13–32 (2016) — carbon-efficient portfolios at equal tracking error.
- **TCFD**, *Recommendations* (2017) and **SBTi**, *Foundations for Science-Based Net-Zero Target Setting* — the pathway/budget logic behind temperature alignment.
- **IPCC**, *Climate Change 2013: The Physical Science Basis* (AR5, WG1 Ch. 12) — TCRE, the physical basis for a cumulative-emissions-to-warming map.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · Physical & Transition Risk]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios & Stress Testing]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (where a carbon factor would be estimated) · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Timing]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]

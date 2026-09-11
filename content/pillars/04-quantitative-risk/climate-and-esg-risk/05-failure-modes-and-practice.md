---
title: "05 — Failure Modes & Real-World Practice: Greenwashing, Data Quality & Non-Stationarity"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - failure-modes
  - greenwashing
  - data-quality
  - look-ahead-bias
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/climate-and-esg-risk/04-esg-scores-and-the-carbon-premium|04 · ESG Scores & the Carbon Premium]].

---

### 1. Intuition & Practical Objective

Climate and ESG risk are *mathematically* ordinary — a weighted average, a cost identity, a quantile, a regression — and *operationally* treacherous. This page names the failure modes precisely so a risk manager knows which input to distrust and how the failure shows up in a number. The objective is not cynicism; it is the discipline of knowing that in this domain **the dominant error term lives in the data definition, not in the estimator.**

Three failure modes, in one line each:

1. **Data-quality failure (the technical meaning of greenwashing).** A sustainability label that the underlying data cannot support at the stated boundary. It is not primarily a lie by a firm; it is the *normal* output of a measurement pipeline in which scope, rater, vintage and weights are all discretionary. Greenwashing is the *name* for the aggregate effect, and it is the same species as look-ahead bias and survivorship bias in quantitative research: an artefact of how the data were generated, invisible in the mathematics.
2. **Non-stationarity.** Both the policy path and the market's pricing of carbon change regime; a fitted carbon beta is a *conditional* moment, and its out-of-sample value can have the opposite sign.
3. **Scenario resolution limits.** A finite scenario set cannot express a high confidence level: with $N$ scenarios of maximum weight $p_{\max}$, the quantile is identified only for $\alpha\le 1-p_{\max}$ ([[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · §2.2]]).

The practical lesson is a change of *reporting discipline*: publish the boundary, the rater and vintage, the pass-through and the benchmark table **alongside** the number, because those four choices move the answer more than any modelling refinement.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The four axes of freedom of a climate number

Any reported climate metric $m$ is a function $m=m(\mathcal B;\mathcal R;\mathcal V;\Theta)$ of the **boundary** $\mathcal B$ (which scopes), the **rater/methodology** $\mathcal R$ (which indicators and weights), the **vintage** $\mathcal V$ (as-of date of the data) and the **economic parameters** $\Theta$ (pass-through, damage coefficient, benchmark table). The first three are *definitional* — they have no error bars, only alternatives; the fourth is a model. The measured swings in this folder:

| Axis | Defensible range | Swing in the reported number | Verified (§) |
|---|---|---|---|
| **Boundary** (Scope 1+2 vs 1+2+3), same firm/year | both standards-compliant | intensity $16.0\to216.0$ tCO2e per $\$1$m = **$13.5\times$** | 01 §3 |
| **Boundary** in temperature alignment | same holdings | $\mathrm{ITR}=1.98^\circ$C $\to$ beyond the $3.2^\circ$C benchmark | 05 §3(B) |
| **Rater** (weights + indicator choice) | three mainstream methodologies | mean rank correlation **$+0.439$**; largest rank move **$5.5$** places; top-5 overlap **$3/5$** | 04 §3(A), 05 §3(A) |
| **Vintage** (retroactive restatement) | one historical revision | **$1$ of $5$** top-5 names changes | 05 §3(A) |
| **Economic parameter** (pass-through $\lambda$) | $\lambda\in[0,0.8]$ | $\$30$/t shock: $-15.33\%\to-3.07\%$ = **$5.0\times$** | hub §3 |
| **Economic parameter** (damage $\theta$) | disclosure-dependent | physical loss is **linear in $\theta$** — the parameter *is* the answer | 02 §3(B) |
| **Scenario count** $N$ | 6 archetypes, $p_{\max}=0.20$ | confidence ceiling $\alpha\le1-p_{\max}=0.80$ | 03 §3 |

Read the last two rows against the first three: the *model* parameters are the ones practitioners argue about, while the *definitional* axes produce larger swings and are usually reported as settled facts. **That inversion is the failure mode.**

#### 2.2 Label instability: rigorous statistics for a soft property

For a universe of $n$ names scored by raters $A$ and $B$ with ranks $r^A_f,r^B_f$, define the **rank-instability rate** and the **top-$k$ overlap**:

$$\boxed{\ R_k=\frac{1}{n}\#\{f:\ |r^A_f-r^B_f|\ge k\},\qquad O_k=\frac{|\mathrm{Top}_k(A)\cap\mathrm{Top}_k(B)|}{k}\ }$$

Both are computed from ranks only, so they are invariant to the raters' scales — the correct way to compare incommensurable scores. A **restatement** is a third rank vector $r^{A'}_f$ (the same rater's history after revision); the exposure to it is $|\mathrm{Top}_k(A)\setminus\mathrm{Top}_k(A')|/k$. **Point-in-time rule:** a backtest of any ESG signal must use the *as-of-vintage* score $R_{f,k,t}$, not the as-of-today history $R_{f,k,T}$; otherwise the vendor's revisions leak tomorrow's information into yesterday's portfolio ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged CV & Backtest Hygiene]]).

#### 2.3 Parameter drift

For a climate risk model with parameter vector $\theta$ (e.g. a carbon beta $b$), define the **drift** between an in-sample fit and an out-of-sample evaluation
$$\delta=\frac{\hat\theta_{\mathrm{OOS}}}{\hat\theta_{\mathrm{IS}}}-1 .$$
A model used as a hedge ratio requires $|\delta|$ small. A model used as a *risk measure* only needs the correct sign — which is why the honest use of a carbon beta is scenario conditioning, not hedging ([[pillars/04-quantitative-risk/climate-and-esg-risk/06-advanced-extensions|06 · §2]]).

#### 2.4 Greenwashing as a data-quality failure, formally

Let a claim be a statement about the true sustainability attribute $S_f$ (e.g. true financed emissions). A pipeline produces an estimate $\hat S_f=s(\mathcal B,\mathcal R,\mathcal V)$. The **greenwashing gap** for a portfolio $P$ is a statement-level quantity,
$$\mathrm{GG}=\Big|\hat S_P-\mathbb E[S_P\mid \mathcal B,\mathcal V]\Big|,$$
i.e. the divergence between what the label asserts and what the *same pipeline, honestly bounded*, would support. Note the definition deliberately holds $\mathcal B$ and $\mathcal V$ fixed: the failure is not picking a wide boundary (that is legal and disclosed), it is asserting a claim at a boundary or vintage the pipeline does not support. This is why **disclosure harmonisation** — not more sophisticated mathematics — is the regulatory response (IOSCO's ESG ratings and data-products work; the EU's sustainable-finance disclosure framework), and why the divergence literature (Berg et al. 2022) frames the issue as one of *data generation*, not of statistical technique.

---

### 3. Computational Implementation — measuring the three failures

Panel (A) quantifies label instability and a retroactive restatement; (B) shows the scope boundary flipping a temperature classification; (C) shows a fitted carbon beta changing sign out of sample. Standard library only.

```python
# c6_failure.py — greenwashing as a data-quality failure (page 05 §3)
import math, random

# ---------- (A) the same eight firms, three raters: label instability ----------
firms = ["A", "B", "C", "D", "E", "F", "G", "H"]
E_  = [90, 45, 70, 55, 30, 80, 60, 40]
S_  = [40, 85, 60, 55, 70, 30, 75, 65]
G_  = [35, 40, 80, 50, 90, 45, 60, 75]
Ep  = [60, 55, 65, 50, 40, 70, 55, 60]
W   = [(0.50, 0.25, 0.25), (0.20, 0.40, 0.40), (1/3, 1/3, 1/3)]
Edata = [E_, E_, Ep]
names = ["R1", "R2", "R3"]
sc = [[W[k][0] * Edata[k][i] + W[k][1] * S_[i] + W[k][2] * G_[i] for i in range(8)] for k in range(3)]


def top5(v):
    return set(sorted(range(len(v)), key=lambda i: -v[i])[:5])


for pair in ((0, 1), (0, 2), (1, 2)):
    inter = top5(sc[pair[0]]) & top5(sc[pair[1]])
    print(f"(A) top-5 overlap {names[pair[0]]}-{names[pair[1]]} = {len(inter)}/5  "
          f"(names dropped by {names[pair[1]]}: {sorted(firms[i] for i in top5(sc[pair[0]]) - top5(sc[pair[1]]))})")

# restatement: the rater retroactively cuts the two most emissions-exposed firms' E pillar
E2 = list(E_); E2[0] -= 20; E2[5] -= 20
sc2 = [W[0][0] * E2[i] + W[0][1] * S_[i] + W[0][2] * G_[i] for i in range(8)]
before, after = top5(sc[0]), top5(sc2)
print(f"    rater R1 top-5 before restatement: {sorted(firms[i] for i in before)}")
print(f"    rater R1 top-5 after  restatement: {sorted(firms[i] for i in after)}")
print(f"    names swapped = {len(before-after)} of 5  -> a backtested 'sustainable' label is not stable")

# ---------- (B) the scope boundary flips the temperature classification ----------
bench = [(1.5, 12_000.0), (1.8, 16_000.0), (2.1, 21_000.0), (2.7, 30_000.0), (3.2, 40_000.0)]


def itr(c):
    """Interpolate between benchmark pathways; None beyond the worst benchmark."""
    if c <= bench[0][1]:
        return bench[0][0]
    for (t0, c0), (t1, c1) in zip(bench, bench[1:]):
        if c <= c1:
            return t0 + (t1 - t0) * (c - c0) / (c1 - c0)
    return None


fmt = lambda c: f"{itr(c):.2f}C" if itr(c) is not None else "> 3.2C off-scale"
for label, C in (("Scope 1+2", 19_020.0), ("Scope 1+2+3", 100_000.0)):
    t = itr(C)
    tag = "below 2C" if (t is not None and t <= 2.0) else ">2C misaligned"
    print(f"(B) same portfolio, {label:12s}: cumulative {C:>9,.0f} t/$m -> ITR {fmt(C):>16s}  [{tag}]")
print(f"    the classification flips and the 'net-zero' label is a measurement choice, not a fact")

# ---------- (C) a carbon-beta model that does not survive out of sample ----------
def ols(X, y):
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


def sample(seed, n, beta_em):
    random.seed(seed); X = []; y = []
    for _ in range(n):
        le = random.gauss(0.0, 1.0); bm = random.gauss(0.0, 1.0)
        X.append([1.0, le, bm]); y.append(0.02 + beta_em * le + 0.03 * bm + random.gauss(0.0, 0.06))
    return X, y


(_, b_in, _), (_, se_in, _) = ols(*sample(21, 60, 0.018))
(_, b_out, _), (_, se_out, _) = ols(*sample(99, 40, 0.0))
print(f"(C) carbon-beta premium fitted on 60 firms: b = {b_in:+.4f} (se {se_in:.4f}, t = {b_in/se_in:+.1f})")
print(f"    same model on an independent 40-firm no-premium sample: b = {b_out:+.4f} (se {se_out:.4f}, t = {b_out/se_out:+.1f})")
print(f"    relative parameter drift = {100*(b_out/b_in-1):+.0f}%  -> a non-stationary beta, not a hedge ratio")
```
```
(A) top-5 overlap R1-R2 = 3/5  (names dropped by R2: ['A', 'F'])
(A) top-5 overlap R1-R3 = 3/5  (names dropped by R3: ['A', 'F'])
(A) top-5 overlap R2-R3 = 5/5  (names dropped by R3: [])
    rater R1 top-5 before restatement: ['A', 'C', 'E', 'F', 'G']
    rater R1 top-5 after  restatement: ['A', 'C', 'E', 'G', 'H']
    names swapped = 1 of 5  -> a backtested 'sustainable' label is not stable
(B) same portfolio, Scope 1+2   : cumulative    19,020 t/$m -> ITR            1.98C  [below 2C]
(B) same portfolio, Scope 1+2+3 : cumulative   100,000 t/$m -> ITR > 3.2C off-scale  [>2C misaligned]
    the classification flips and the 'net-zero' label is a measurement choice, not a fact
(C) carbon-beta premium fitted on 60 firms: b = +0.0231 (se 0.0079, t = +2.9)
    same model on an independent 40-firm no-premium sample: b = -0.0060 (se 0.0076, t = -0.8)
    relative parameter drift = -126%  -> a non-stationary beta, not a hedge ratio
```

**Panel (A).** Two of the three rater pairs agree on only $O_5=3/5$ of the top five — the "leaders" list is a different list depending on who is asked, and $R_2$ and $R_3$ (which share underlying data) agree perfectly at $5/5$. A **single retroactive revision** to two firms' environmental pillar moves one name ($20\%$) in and out of the top five. That is the operational content of point-in-time discipline: the label a backtest "would have" assigned is not recoverable from today's vendor file.

**Panel (B).** The identical portfolio is "below $2^\circ$C" on a Scope 1+2 basis and *beyond the worst benchmark* on a Scope 1+2+3 basis. No holdings changed; only the boundary. The interpolation correctly refuses to extrapolate, and the reported temperature is nevertheless quoted to two decimals in most investor materials.

**Panel (C).** A carbon beta fitted at $\hat b=+0.0231$ ($t=+2.9$, apparently strong) is $-0.0060$ ($t=-0.8$) on an independent sample drawn from a no-premium regime — a drift of $-126\%$, with a sign flip. **A carbon beta is a regime-conditional statistic**; using it as a hedge ratio without a regime model is using yesterday's map.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Greenwashing = data-quality failure, not an estimator failure.** Definitional axes (boundary, rater, vintage) swing the number more than any modelling refinement (§2.1). Fix the *disclosure* — pin the boundary, the rater, the vintage and the weights — before touching the model. Cross-link: this is the same discipline as purged cross-validation and point-in-time features in [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Backtest Hygiene]].
2. **Look-ahead bias from vendor restatements.** ESG history is revised retroactively; a signal backtested on as-of-today history is not a backtest. Require point-in-time vintages and archive the as-of score with every signal.
3. **Aggregating raters to "fix" divergence.** Because measurement divergence is $56\%$ and includes a correlated rater (halo) effect, a simple average of raters reduces but does not remove the bias — and it destroys the interpretability of the score. Report the rater and the dispersion.
4. **Confusing the preference premium with the risk premium.** A greenium in expected returns (investor preferences) and a brown risk premium (transition-risk compensation) coexist; a strategy that assumes one only will be wrong about the other's sign ([[pillars/04-quantitative-risk/climate-and-esg-risk/04-esg-scores-and-the-carbon-premium|04 · §2.3]]).
5. **Using a scenario count as a confidence level.** The ceiling $\alpha\le1-p_{\max}$ is a hard limit; a "$99\%$ climate VaR" from six scenarios is the worst narrative relabelled ([[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · §4.3]]).
6. **Double-counting transition and physical risk.** They are anti-correlated *by scenario design*; summing independent stresses overstates the total ([[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · §4.6]]).
7. **Reporting a point on a curve.** Stranding ($\mathrm{SF}(p)$), physical damage ($\theta$) and pass-through ($\lambda$) are all *curves or ranges* misreported as points. Publish the sensitivity, not just the central number.
8. **Governance: the number used for marketing is the number used for risk.** If the same metric drives both a fund's label and its limit, the incentive to choose the favourable boundary is structural. Separate the *disclosure* metric from the *risk* metric, and fix both in policy.

---

### 5. Canonical Literature & Study References

- **Berg, F., Kölbel, J.F. & Rigobon, R.** — *Aggregate Confusion: The Divergence of ESG Ratings*, *Review of Finance* **26**(6):1315–1344 (2022) — the decomposition and the rater (halo) effect behind §2.4. *Primary source.*
- **Berg, F., Fabisik, K. & Sautner, Z.** — *Rewriting History II: The (Un)Predictable Past of ESG Ratings* (ECGI Finance Working Paper 708/2020) — retroactive revisions and the look-ahead bias quantified in §3(A).
- **IOSCO** — *Final Report on ESG Ratings and Data Products Providers* (2021) and the *Statement on Sustainability Disclosure* — the supervisory response to divergence (disclosure harmonisation). *[REG]*
- **BCBS** — *Climate-related Financial Risks — Measurement Methodologies* (2021) — the supervisory catalogue of data gaps and methodological limits. *[REG]*
- **Bolton, P. & Kacperczyk, M.** (2021) and **Pástor, Ľ., Stambaugh, R.F. & Taylor, L.A.** (2021, 2022) — the competing premium/greenium regimes of §3(C).
- **Kupiec, P.**, *Techniques for Verifying the Accuracy of Risk Measurement Models*, *J. Derivatives* 3(2) (1995) — the backtesting discipline that a climate stress test cannot inherit in the usual way ([[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|VaR/ES · 05]]).
- **López de Prado, M.**, *Advances in Financial Machine Learning* (Wiley, 2018), Ch. 7 (purged cross-validation) and Ch. 11 (backtest overfitting) — the general point-in-time discipline applied here to ESG data.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/climate-and-esg-risk/04-esg-scores-and-the-carbon-premium|04 · ESG Scores & the Carbon Premium]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/climate-and-esg-risk/06-advanced-extensions|06 · Advanced Extensions (Euler Allocation, Carbon-Adjusted PD)]]
- Sibling: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alternative Data Pipelines & Evaluation]] · [[pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index|Financial NLP & Transcripts]] (greenwashing claims are textual, and text is where the label is asserted) · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]

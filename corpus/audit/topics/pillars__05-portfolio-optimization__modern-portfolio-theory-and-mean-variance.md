# Audit Report — `content/pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/`

Scope: 7 files (index.md + 01..06). Sole adversarial reviewer. Audited spelling/typos (prose only, code/LaTeX excluded), every boxed formula + worked numeric example (Merton $A,B,C,D$ machinery, frontier parabola, GMV, generic frontier weights, tangency, max-Sharpe identity, CML, SML/CAPM, two-fund separation, two-asset min-variance weight, long-only/KKT frontier, shrinkage, robust MVO), every ```python block (run + stdout-diff), and cross-page coherence (prereqs, jargon first-use, wikilinks, contradictions). Corpus checked: `corpus/verified/*` (no portfolio source present), `corpus/pillar5-portfolio-optimization.md`, and the primary PDFs `corpus/titles/refs/pillar5/BestGrauer1991…pdf` and `…/ChopraZiemba1993.pdf`.

## 1. Verdict

**ACCEPT_WITH_FIXES.** Core mathematics is clean: **every boxed formula and every worked number re-derived independently (stdlib + `numpy.linalg`) and reproduced exactly**; all **8/8 python blocks run (exit 0, stdlib-only) and their stdout matches the documented fences exactly**; all **21 unique wikilinks (84 link instances) resolve**; no spelling typos or doubled words in prose. Best & Grauer's headline numbers were verified line-by-line against the primary PDF (Table 5, Table 7). One **substantive factual error** (the Chopra–Ziemba ratio, stated backwards and internally contradictory) plus six minor notation/imprecision/code issues need fixing:

1. **05:33** — the Chopra–Ziemba (1993) error-importance ratios are **mis-assigned** (μ-vs-σ² stated as 2×; correct is ~11×). [HIGH]
2. **05:22, 05:106** — same mislabel repeated: "errors in $\Sigma$" should be "errors in *variances*". [MED]
3. **index:38** — the multiplier system is typeset with `\begin{vmatrix}` (determinant bars) instead of `bmatrix`. [LOW]
4. **06:28** — "…$20^{th}$-century ESL Ch 3–4" (ESL is 21st-century). [LOW]
5. **02:91–92** — dead, misnamed placeholder code (`wt` is $\Sigma^{-1}\mathbf 1$, *not* the tangency portfolio; comment claims it is "replaced below" but it is not). [LOW]
6. **04:31** — $\lambda_i w_i=0$ reuses $\lambda$, already the budget multiplier on the same page (§2). [LOW]
7. **05:29** — $\partial w/\partial\mu_j=\Sigma^{-1}e_j\cdot(\text{scalar})$ omits the multiplier-derivative terms; only the amplification *conclusion* is correct. [LOW]

## 2. Issues table

| File:Line | Problem (stated) | Correct | Severity |
|---|---|---|---|
| 05:33 | ``cost(μ error) ≈ 10–11× cost(Σ error), cost(μ error) ≈ 2× cost(σ² error)`` | Chopra & Ziemba (1993), quoted verbatim: *"errors in means are 11 times as damaging as errors in **variances** and over 21 times as damaging as errors in **covariances**"*; and *"errors in variances are about **twice** as important as errors in covariances."* So the **10–11×** factor belongs to **variances** (σ²), **not** to $\Sigma$; the **2×** factor is **variance-vs-covariance**, **not** μ-vs-σ². Correct pair: `cost(μ) ≈ 11× cost(σ²)`, `cost(σ²) ≈ 2× cost(covariance)`. As written, "μ ≈ 2× σ²" understates μ-dominance of variance errors by ~5×. | **HIGH (math/fact)** |
| 05:22 | "errors in $\mu$ are ~10–11× more damaging than errors in $\Sigma$ in the MV objective" | Should be "than errors in **variances** (σ²)". Internally contradictory: line 33 says μ dominates $\Sigma$ by 10–11× but σ² (a subset of $\Sigma$) by only 2× — impossible. Also propagated at **05:106** ("Chopra–Ziemba's ~10–11× factor"). | **MED (fact)** |
| index:38 | `\begin{vmatrix}C&A\\A&B\end{vmatrix}\begin{vmatrix}\lambda\\\gamma\end{vmatrix}=\begin{vmatrix}1\\\mu^*\end{vmatrix}` | `vmatrix` renders **determinant bars**; this is a matrix/vector *equation*. Use `bmatrix` as 02:33 does for the identical object. | LOW (notation) |
| 06:28 | "…the same regularization spirit as ridge regression in Linear Algebra/$20^{th}$-century ESL Ch 3–4." | ESL (Hastie/Tibshirani/Friedman) is **2001/2009** — 21st-century, not "20th". 01:92 refers to the same book without the century tag. Fix: drop "20^{th}-century". | LOW (fact) |
| 02:91–92 | `wt=z.copy()` then `lam=(0.12-...)…` `# placeholder, replaced by true tangency below` | `z=\Sigma^{-1}\mathbf1`, so `wt` is *not* the tangency portfolio (it is the unnormalised min-var direction); `lam` is never used and nothing is printed. The prose (02:94) concedes this, but the dead block is misleading in a page whose whole point is tangency. Fix: delete lines 91–92 or rename/comment honestly. | LOW (code) |
| 04:31 | "complementary slackness $\lambda_i w_i=0$" | The multiplier on $w\ge0$ is distinct from the budget multiplier $\lambda$ used at 04:26 in the same section. Rename the non-negativity multipliers $\nu_i$ (or $\mu_i$) to avoid collision. | LOW (notation) |
| 05:29 | `∂w/∂μ_j = Σ^{-1}e_j · (scalar multipliers)` | For the tangency solution $w=\Sigma^{-1}(\mu-r_f\mathbf1)/k$, $\partial w/\partial\mu_j=\Sigma^{-1}\!\left[e_j/k-(\mu-r_f\mathbf1)(\partial k/\partial\mu_j)/k^2\right]$ — two terms, both through $\Sigma^{-1}$, but *not* $\Sigma^{-1}e_j$ alone. The amplification claim is right; the identity is loose. Fix: state it as "∝ $\Sigma^{-1}\times(\text{rank-1 corrections})$". | LOW (imprecision) |

Numeric-claim provenance notes (not counted as errors — values are correct):
- **index:19 / index:51** assert the check-column numbers were "reproduced exactly from the verified corpus" and cross-checked against `numpy`. `corpus/verified/*` contains no portfolio-theory book; the numbers *are* reproducible (I re-ran them) and *do* match `numpy.linalg.inv/solve` to machine precision, so the claim is only loosely worded.
- **05:114** "Verified in the corpus" for Best & Grauer — the paper lives at `corpus/titles/refs/pillar5/BestGrauer1991_SensitivityMeanVarianceEfficient.pdf` (not `corpus/verified/`); I verified its numbers there and they are **exactly** as stated.
- **index:21** "a linear combination of the riskless asset with *any* two frontier funds spans the whole efficient set" — with cash present the spanning pair is {cash, $w_{\text{tan}}$}, not "cash + two funds". Wording nit.

No spelling typos, no doubled words, no broken sentences found in prose (code fences and LaTeX excluded; `pyspellchecker` + manual pass, only hyphenated technical compounds and proper names flagged).

## 3. Math verified

Worked universe throughout: $\mu=[0.08,0.12,0.16]$, $\Sigma=\begin{smallmatrix}0.100&0.040&0.016\\0.040&0.180&0.032\\0.016&0.032&0.250\end{smallmatrix}$, $r_f=0.04$.

- **$\Sigma$ construction** (index:28): $0.30\sqrt{.1\cdot.18}=0.04025\to0.040$; $0.10\sqrt{.1\cdot.25}=0.01581\to0.016$; $0.15\sqrt{.18\cdot.25}=0.03182\to0.032$ ✓ (implied corr 0.30/0.10/0.15 ✓).
- **Merton scalars** $A=\mathbf1'\Sigma^{-1}\mu,\ B=\mu'\Sigma^{-1}\mu,\ C=\mathbf1'\Sigma^{-1}\mathbf1,\ D=BC-A^2$ (index:31) ✓. Values $A{=}1.53150,\ B{=}0.18447,\ C{=}14.48325,\ D{=}0.32622$ ✓ (numpy: 1.531496/0.184468/14.483247/0.326215).
- **Frontier parabola** $\sigma^2=(C\mu^2-2A\mu+B)/D$ (index:36, 02:37) ✓; at $\mu{=}0.14$: $0.12115$, $\sigma{=}0.3481$ ✓; $d^2\sigma^2/dR^2=2C/D>0$ ✓; asymptote slope $\pm\sqrt{D/C}=\pm0.15008$ ✓ (re-derived: $\sigma\approx\sqrt{C/D}\,\mu$).
- **GMV** $\mu_{\text{mv}}{=}A/C{=}0.10574$, $\sigma^2_{\text{mv}}{=}1/C{=}0.06905$, $w_{\text{mv}}{=}\Sigma^{-1}\mathbf1/(\mathbf1'\Sigma^{-1}\mathbf1){=}[0.569,0.219,0.212]$ ✓ (numpy: [0.56879,0.21886,0.21235]).
- **Generic frontier portfolio** $w^f(R^*)=\Sigma^{-1}\!\big(\tfrac{B-AR^*}{D}\mathbf1+\tfrac{CR^*-A}{D}\mu\big)$ (02:34) ✓ — sign-checked: $\mathbf1'w^f{=}1$, $\mu'w^f{=}R^*$; and the index multiplier system $\begin{smallmatrix}C&A\\A&B\end{smallmatrix}[\lambda,\gamma]'=[1,\mu^*]'$ (index:38) has the same solution ✓. $\mu^*{=}0.12\!\Rightarrow\![0.354,0.292,0.354]$, $\sigma{=}0.2794$ ✓.
- **Tangency** $w_{\text{tan}}=\Sigma^{-1}(\mu-r_f\mathbf1)/\mathbf1'\Sigma^{-1}(\mu-r_f\mathbf1)$ (03:26) ✓; $[0.2124,0.3402,0.4474]$, $\sigma{=}0.30641$ ✓. Validity $r_f<A/C$ ✓ ($0.04<0.10574$).
- **Max-Sharpe identity** $\text{SR}^2_{\max}=(\mu_t-r_f)^2/\sigma_t^2=Cr_f^2-2Ar_f+B$ (index:40, 03:30) ✓ — direct quadratic form $\checkmark$ 0.0851214679398 vs $Cr_f^2-2Ar_f+B$ 0.0851214679398 (agree to 1e-16). $\text{SR}=0.29176$ ✓.
- **CML** $\mu=r_f+\text{SR}_{\max}\sigma$ (03:31) ✓; blends $\theta{=}0.5\to(0.1532,0.0847)$, $\theta{=}1\to(0.3064,0.1294)$ ✓.
- **SML/CAPM** $\mu_i-r_f=\beta_i(\mu_M-r_f)$, $\beta_i=\sigma_{iM}/\sigma_M^2=\Sigma_i\!\cdot\! w_M/\sigma_M^2$ (index:42, 03:34) ✓ — betas $0.4474/0.8949/1.3423$, residuals $0.00$ (identity holds exactly at the tangency "market") ✓. Identity check $(\mu-r_f\mathbf1)=k\Sigma w_t$, $k=(\mu_M-r_f)/\sigma_M^2$ ✓.
- **Two-fund separation** $w=w_{\text{mv}}+\lambda(w_{\text{tan}}-w_{\text{mv}})$ (index:43, 02:43) ✓ — $\lambda{=}0.60272$ reproduces $w(0.12){=}[0.354,0.292,0.354]$ with max error $3.3\times10^{-16}$ ✓ (4e-16 as stated). Merton decomposition $w=R^*g+h$ with $\mathbf1'g{=}0$, $\mathbf1'h{=}1$ ✓.
- **Two-asset** $\sigma_p^2=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\rho\sigma_1\sigma_2$ and $w^*=(\sigma_2^2-\rho\sigma_1\sigma_2)/(\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2)$ (01:29,01:33) ✓ — stationary point re-derived; equal-vol $\Rightarrow w^*{=}1/2$ ✓; $\rho{=}0.8,\sigma_{1,2}{=}0.25/0.40\Rightarrow w^*{=}1.28$ ✓.
- **Long-only/KKT frontier** (04:26–33) ✓ — @$R^*{\ge}0.16$ corner $[0,0,1]$, $\sigma{=}\sqrt{0.250}{=}0.50$ ✓; min-var already long-only-feasible (all weights positive) so the floor is slack up to $R^*\!\approx\!0.106$ ✓.
- **Shrinkage** $\hat\Sigma(\delta)=(1-\delta)S+\delta F$, Ledoit–Wolf Frobenius-loss target, small eigenvalues lifted by shrinkage (06:26–28) ✓.
- **Robust MVO** $\max_w\min_{(\mu,\Sigma)\in\mathcal U}(w'\mu-\tfrac12\lambda w'\Sigma w)$, SOCP (06:30–32) ✓ (**note 06:31 uses $\lambda$ as a risk-aversion scalar — fine, different page from 04**).
- **Black–Litterman** implied returns $\Pi=\gamma\Sigma w_{\text{mkt}}$ (06:36) ✓.
- **Best & Grauer (1991), primary PDF** — 100-asset universe, mean increase to drive the most sensitive asset out: **1 asset = 0.08%**, 5 = 0.18%, 10 = 0.30% (Table 7 "Most sensitive asset"); **50 assets = 11.60%** (Table 5/7 averages) = "half the universe" ✓; main text: *"there is virtually no change in its expected return or standard deviation"* ✓ — matches 05:36 and index:116 exactly.

## 4. Code run / match stats

| File | Block | Runs (exit 0) | Stdout matches doc |
|---|---|---|---|
| index.md | §3 frontier engine | ✓ | ✓ |
| 01-from-zero-intuition.md | two-asset vol + $w^*$ | ✓ | ✓ |
| 02-the-efficient-frontier.md | block 1 (frontier trace) | ✓ | ✓ (shared fence) |
| 02-the-efficient-frontier.md | block 2 (two-fund span) | ✓ | ✓ (shared fence) |
| 03-tangency-and-capm.md | tangency + SML + CML | ✓ | ✓ |
| 04-min-variance-and-constraints.md | min-var + long-only grid | ✓ | ✓ |
| 05-failure-modes-and-practice.md | 5-asset blow-up | ✓ | ✓ |
| 06-advanced-extensions.md | shrinkage sweep | ✓ | ✓ |

**8/8 blocks run successfully (stdlib only — `math`/`itertools`; no external deps); 8/8 stdout match the documented output fences exactly, including whitespace.** Notes: (a) 02's two blocks share a single merged output fence at line 131 — concatenated stdout of both blocks matches it line-for-line. (b) index §3 imports `math` twice (lines 54 & 70) — harmless. (c) All blocks are fully deterministic (Gauss–Jordan inversion, Jacobi eigenvalues, fixed grid) — no RNG, no timing/nondeterminism flags. (d) The `numpy` cross-check claim (index:51) independently confirmed: `numpy.linalg.inv/solve` reproduces every value to machine precision.

## 5. Links & coherence

- **21 unique wikilinks (84 instances), all resolve** — 12 as `pillars/…` targets, 4 as `foundations/…`, no broken links. Forward links to `constraints-and-transaction-costs`, `black-litterman`, `covariance-shrinkage-and-denoising`, `risk-parity-and-equal-risk-contribution`, `hierarchical-risk-parity`, `pillars/04-quantitative-risk` all exist.
- **Prerequisites:** index:11 declares folder-level prereqs *Linear Algebra* **and** *Calculus & KKT* for pages 02–06, with 01 carrying a smaller self-stated prereq (01:10, Linear Algebra only) — consistent. Sub-pages are sequenced internally (02: LA+Calculus; 03: 02; 04: 02+Calculus; 05: 04; 06: 05+Statistics). **Minor framing tension:** 06 adds *Statistics & Inference*, which is not in the index's folder-level "02–06" list — not a hard error, but the index's §6 "Foundational base" line (index:134) omits it too.
- **Jargon first-use:** quadratic program, efficient frontier, tangency/Sharpe-optimal, two-fund separation, CML, SML, GMV/min-var, estimation-error maximizer, condition number, shrinkage, uncertainty set/SOCP are all defined at or before first substantive use. The hub uses "SML" in §1 before its §2 definition — acceptable for a lookup hub.
- **Cross-page contradictions:** none in the numeric "verified numbers" column (index matches 02/03/04/05/06 outputs throughout), **except** the μ-vs-$\Sigma$-vs-σ² inconsistency at 05:22/05:33 (item 1–2 above) — the only internal contradiction found.
- Code blocks are runnable exactly as documented; every "Stdlib only" claim is true.

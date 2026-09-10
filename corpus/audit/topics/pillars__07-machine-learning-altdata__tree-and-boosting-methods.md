# Audit Report — `content/pillars/07-machine-learning-altdata/tree-and-boosting-methods/`

Scope: 7 files (`index.md` + `01`..`06`). Sole adversarial reviewer. Audited spelling/typos (prose only; code & LaTeX excluded), every boxed formula and worked numeric example, every ` ```python ` block (run, chained in one namespace where a page has several; stdout diffed against the trailing output fence), and cross-page coherence (prereqs, jargon, wikilinks, contradictions). Source of truth for ESL equation numbers: `corpus/verified/esl_ch6-10.md`, `esl_ch11-18.md`.

## 1. Verdict

**ACCEPT_WITH_FIXES.** The folder is in good shape. All **7/7** `python` blocks execute (exit 0) and every byte of stdout matches its documented output fence exactly; all **20** unique wikilinks resolve to real files/`index.md`; no spelling/typo, doubled-word, or malformed-sentence issues were found in prose. Every boxed formula and every prose numeric claim was re-derived and/or re-executed and checks out — CART split (9.13), SSE fast form, Gini/deviance (9.17), cost-complexity (9.16), bagging (8.51–8.52), RF variance decomposition (15.1), OOB, RF `m`/node-size defaults, boosting recursion & pseudo-residual, AdaBoost weight (10.1, half-log-odds 10.16), the XGBoost second-order objective / optimal leaf weight / split gain / Ω penalty, shrinkage, MDI (10.42–43) and MDA.

Three defects remain, all on pages 04 and the hub, one of which is a genuine (if minor) math-notation error:

1. **`04:144` (MEDIUM, math/notation).** The interaction-order result is stated in terms of **depth**, but ESL's $J$ is the number of **terminal nodes**. As written ("depth-$J$ tree captures interactions of order $J-1$") the statement is off by one and contradicts its own trailing clause; ESL (§10.11) reads "tree **size** $J$ limits interaction order to $J-1$; stumps ($J=2$) = main effects only" (verified: `corpus/verified/esl_ch6-10.md:108`).
2. **`04:137` (LOW, terminology + internal inconsistency).** The depth-2 base learners are called "**stumps**-of-depth-2". A stump is a **depth-1** tree (one split, 2 terminal nodes); the code uses `depth=2` (4 leaves). This also contradicts the same page's own §3 opener, line 58: "We boost **depth-2 trees**".
3. **`index:41` (LOW, same defect propagated to the hub).** The lookup table's verified-check cell reads "400 **stumps**: single $0.9888\to0.6733$" — same mislabelling of the depth-2 base learner.

No wrong signs, constants, or inverted directions were found anywhere else.

## 2. Issues table

| File:Line | Problem (stated) | Correct | Severity |
|---|---|---|---|
| 04:144 | "A **depth-$J$** tree captures interactions of order $J-1$ (ESL 10.28); stumps ($J=2$) are purely additive." | ESL's $J$ is the **terminal-node count**, not depth. Replace "depth-$J$" with "$J$-terminal-node" (or "a tree of size $J$"). The trailing "stumps ($J=2$)" clause then becomes consistent with ESL §10.11 ("tree size J limits interaction order to J−1; stumps (J=2) = main effects only"). The cited eq 10.28 (boosting-tree sum) is also the wrong anchor — the interaction-order result is §10.11. | **MEDIUM (math/notation)** |
| 04:137 | "400 boosted **stumps-of-depth-2** reach $0.6733$" — and the base learner in the code is `fit_tree(..., depth=2)`. | A stump is depth-1 / 2 terminal nodes. The base learner is a **depth-2 tree** (4 leaves). Fix to "400 boosted depth-2 trees". Contradicts the same page, line 58 ("We boost depth-2 trees"). | **LOW (terminology/coherence)** |
| index:41 | Lookup row "Boosting stagewise form (ESL 10.28) … **400 stumps**: single $0.9888\to0.6733$". | Same: the page-04 experiment boosts **depth-2 trees**, not stumps. Change "400 stumps" → "400 depth-2 trees". | **LOW (terminology)** |

No spelling typos, no doubled words, no broken sentences found in prose (code fences and LaTeX excluded; 150+ misspelling dictionary patterns scanned, zero hits).

### Observations (not counted as errors)

- **SHAP is absent.** The audit brief lists SHAP among the formulas to verify; the folder deliberately uses the AFML importance triplet **MDI / MDA / SFI** instead and contains no SHAP/Shapley content anywhere in the pillar (grep-confirmed). This is a deliberate coverage choice, not a defect — flagging so the reviewer-of-record knows the SHAP check was vacuous.
- **03:137** prints "`(+29.9% vs single)`" for a *reduction* in MSE (improvement is $+29.9\%$ in the "vs single" convention). Consistent across the block; purely cosmetic.
- **index:30** overloads $M$: "ensemble size $B$ (RF) or $M$ (boosting)" and the MDI row reuses $M$ for the number of trees. Harmless but slightly loose.
- **03:158** attributes "sequential bootstrapping, `avgU`" to AFML Ch 6; those live in Ch 4 in AFML's structure. AFML is not in the *verified* corpus, so this is a soft note, not a confirmed error.

## 3. Math verified

Every boxed formula and prose number re-derived and/or re-executed:

- **Tree prediction (9.10–9.11)** $f(x)=\sum_m c_m\mathbb 1(x\in R_m)$, $c_m=\mathrm{ave}(y_i\mid x_i\in R_m)$ ✓.
- **Greedy split (9.13)** $\min_{j,s}[\min_{c_1}\sum_{R_1}(y_i-c_1)^2+\min_{c_2}\sum_{R_2}(y_i-c_2)^2]$ ✓ (matches verified `esl_ch6-10.md:86-87`).
- **SSE fast form** $\sum_R(y_i-\bar y)^2=\sum_R y_i^2-\tfrac1n(\sum_R y_i)^2$ ✓ (algebraically exact).
- **Gini (9.17)** $\sum_k \hat p_{mk}(1-\hat p_{mk})$; binary peak $2p(1-p)=0.5$ at $p=\tfrac12$ ✓.
- **Deviance/cross-entropy (9.17)** $-\sum_k\hat p_{mk}\log\hat p_{mk}$ ✓.
- **Cost-complexity prune (9.16)** $C_\alpha(T)=\sum_m N_mQ_m(T)+\alpha|T|$, weakest-link ✓.
- **Bagging (8.51–8.52)** $\hat f_{\text{bag}}=\tfrac1B\sum_b\hat f^{*b}$; population aggregation never increases MSE ✓ (verified `esl_ch6-10.md:68`).
- **RF variance (15.1)** $\rho\sigma^2+\frac{1-\rho}{B}\sigma^2$ ✓ (verified `esl_ch11-18.md:140`); with $\rho{=}0.657,B{=}100$, floor $=\rho\sigma^2$ dominates ✓.
- **Bootstrap loss** $(1-1/n)^n\to e^{-1}\approx36.8\%$ ✓ (OOB $\approx e^{-1}$) ✓ (verified 15.3.1).
- **RF defaults** classification $m=\lfloor\sqrt p\rfloor$/node 1; regression $m=\lfloor p/3\rfloor$/node 5 ✓ (ESL 15.1).
- **Boosting recursion (10.28/10.2)** $F_m=F_{m-1}+\nu h_m$, $r_{im}=-[\partial L/\partial F]_{F_{m-1}}$ ✓; for $L=\tfrac12(y-F)^2$, $r_{im}=y_i-F_{m-1}(x_i)$ ✓.
- **AdaBoost (10.1)** $\alpha_m=\log\frac{1-\mathrm{err}_m}{\mathrm{err}_m}$, population minimiser = half log-odds ✓ (10.16, verified `esl_ch6-10.md:107`).
- **XGBoost** $\mathcal L^{(t)}\approx\sum_i[g_if_t+\tfrac12h_if_t^2]+\Omega$, $g=\partial_{\hat y}L$, $h=\partial^2_{\hat y}L$ ✓; $\Omega=\gamma|T|+\tfrac12\lambda\sum_j w_j^2$ ✓; $w_j^*=-G_j/(H_j+\lambda)$ ✓ (correct sign); $\text{Gain}=\tfrac12[\frac{G_L^2}{H_L+\lambda}+\frac{G_R^2}{H_R+\lambda}-\frac{(G_L+G_R)^2}{H_L+H_R+\lambda}]-\gamma$ ✓.
- **Shrinkage (10.12.1)** small $\nu$ + early stopping ✓.
- **Overfitting optimism (7.24)** $\approx2d\sigma_\varepsilon^2/N$ ✓.
- **MDI (10.42–43)** $I_\ell^2(T)=\sum_{t=1}^{|T|-1}\hat\imath_t^2\mathbb 1(v(t)=\ell)$, averaged over trees; $\sum_\ell\mathrm{MDI}_\ell=1$ ✓ (verified `esl_ch6-10.md:112`).
- **MDA** $\mathrm{Score}_{\text{OOS}}-\mathrm{Score}_{\text{OOS},\pi_j}$ ✓; SFI one-feature-at-a-time (AFML §8.4.1) ✓.
- **Worked examples re-executed** — hub split $x_1\le1.4769$; page-01 OLS $0.3774$/$0.6469$ vs stump $0.4765$ (−26.3%); page-02 U-curve $0.3008\to0.3463\to0.3680$; page-03 $1.5539\to1.0888$, $\rho\,0.657\to0.621$, OOB $1.1993\to1.1567$; page-04 $0.9888\to0.6733$ (−31.9%); page-05 MDI $0.541/0.459$, leaky $+0.0462$ vs honest $-0.1687$; page-06 MDI/MDA/SFI table, blend $0.7135$ vs best $0.7138$. **All match the documented fences exactly.**

**Not-checkable:** SHAP/Shapley (absent — see Observations).

## 4. Code run / match stats

| File | Block | Runs (exit 0) | Stdout matches doc | Blocks |
|---|---|---|---|---|
| index.md | §3 tree engine | ✓ | ✓ | 1 |
| 01-from-zero-intuition.md | line vs stump | ✓ | ✓ | 1 |
| 02-decision-trees.md | from-scratch CART + depth curve | ✓ | ✓ | 1 |
| 03-bagging-and-random-forests.md | bagging vs RF + OOB | ✓ | ✓ | 1 |
| 04-gradient-boosting.md | from-scratch boosting | ✓ | ✓ | 1 |
| 05-failure-modes-and-practice.md | MDI bias + leaky CV | ✓ | ✓ | 1 |
| 06-advanced-extensions.md | MDI/MDA/SFI + averaging | ✓ | ✓ | 1 |

**Total `python` blocks: 7. Executed: 7. Stdout matches: 7.** (Each page has exactly one `python` block, so no intra-page chaining was needed; every block was still run to completion in a fresh interpreter with numpy 2.5.3 — exit 0, no warnings/tracebacks.)

## 5. Coherence

- **Hub vs sub-pages:** hub lookup table, §4 five signposts, and the reading-route arc all agree numerically and thematically with `01`–`06`. No contradictions found (other than the "stumps" mislabel in §2, issue 3).
- **Prereqs:** hub declares folder-level prereqs (Statistics & Inference) for `02`–`06` and explicitly defers page `01`'s smaller entry bar to itself — page `01` correctly states only "Statistics & Inference (mean, variance, regression)". Back/Continue links form a consistent 01→02→…→06 chain.
- **Links:** 20/20 unique wikilinks resolve (verified against the filesystem). Cross-pillar links to `financial-ml-pitfalls-and-low-snr/*`, `purged-cross-validation-and-backtest-hygiene/*`, `tree-based-factor-ranking-and-purged-cv`, `deep-learning-for-sequential-data`, `regime-classification-hmm-and-gmm` all exist.
- **Citations:** ESL equation numbers spot-checked against `corpus/verified/esl_*.md` — all correct. AFML is not in `corpus/verified/` but the AFML PDFs/epub are present under `corpus/titles/refs/pillar7/`, so "*PDF read in the corpus*" is defensible.

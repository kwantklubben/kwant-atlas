# Audit: `content/pillars/01-quantitative-research/signal-processing-and-kalman/`

**Date:** 2026-09-10 · **Sole reviewer** · **Scope:** 7 files (index + 01–06) · **House rules applied:** wikilinks `[[full/path|Alias]]`, math `$..$`/`$$..$$`, verified against `corpus/verified/*.md` (`tsay_ch10-12.md` Ch 11 is the primary source). `_legacy/` ignored.

## Verdict: **FAIL** — 1 clear formula error (hub Joseph form uses the wrong matrices), 1 convention/labeling error in the hub's steady-state row, and 1 notation clash between the hub's essence box and its own §2 notation. **All 7 code blocks execute cleanly and reproduce their documented output byte-for-byte; every worked example checks out numerically; no dead links; no spelling errors.**

---

## 1. SPELLING / TYPO in prose
- **No issues found.** Hunspell has no English dictionary installed in this environment (silent no-op), so I scanned manually and with targeted regexes for the usual suspects (doubled words, common misspellings, `teh`/`recieve`/`occured`/`paramater`, etc.) across all 7 files — zero hits. Non-ASCII characters are all legitimate (arrows `→`, minus `−`, `Särkkä`). Prose is clean and consistent.

## 2. MATH — every boxed formula & worked example
| File:line | Object | Verdict |
|---|---|---|
| index:33 / 02:32–33 | General linear-Gaussian form (Tsay 11.26–11.27): `s_{t+1}=d_t+T_ts_t+R_tη_t`, `y_t=c_t+Z_ts_t+e_t` | ✅ matches corpus tsay_ch10-12:37 |
| index:37–41 / 03:37–41 | Innovation, `V_t=Z_tΣZ_t'+H_t`, gain `K_t=T_tΣZ_t'V_t⁻¹`, state update, `Σ_{t+1|t}=T_tΣL_t'+R_tQ_tR_t'`, `L_t=T_t−K_tZ_t` (Tsay 11.64) | ✅ matches corpus tsay_ch10-12:38 exactly |
| index:42 / 03:67 / 04:52 | Prediction-error log-likelihood (Tsay 11.25) | ✅ matches corpus |
| index:43 / 01:44 / 03:55 | Scalar local-level (Tsay 11.14) + hand example `P0=1,q=.25,r=1,y=1.5` → `x=0.833333, P=0.555556` | ✅ re-derived: Pp=1.25, K=1.25/2.25=5/9, x=5/6, P=(4/9)(5/4)=5/9 |
| **index:44** | **Steady-state gain row** — see **Error 2** | ❌ convention/labeling error |
| index:45 / 02:55 | Local-level ↔ ARIMA(0,1,1) (Tsay 11.4–11.5): `σ_e²=θσ_a²`, `(1+θ²)σ_a²=2σ_e²+σ_η²`; Alcoa θ=.858, σ_a=.5184 → σ_e=.4802, σ_η=.0736 | ✅ matches corpus tsay_ch10-12:34; numbers reproduce |
| index:46 / 04:21 | Dynamic CAPM (Tsay 11.29), `Z_t=(1, r_{M,t})` | ✅ matches corpus tsay_ch10-12:41 |
| **index:47** | **Joseph form** — see **Error 1** | ❌ wrong matrices |
| index:48 / 06:32–34 | RTS smoother `C_t=Σ_{t|t}T_t'Σ_{t+1|t}⁻¹`, `s_{t|T}=s_{t|t}+C_t(s_{t+1|T}−s_{t+1|t})` | ✅ standard RTS form |
| 02:49–51 | ARMA(1,1) companion state `s_t=(x_t,θa_t)'`, `T=[[φ,1],[0,0]]`, `R=(1,θ)'`, `Z=(1,0)`, `H=0` | ✅ re-derived from `x_t=φx_{t-1}+θa_{t-1}+a_t`; matches code (diff 0.00e0) |
| 03:47 | Bayes route `K=Σ⁻Z'(ZΣ⁻Z'+H)⁻¹`, posterior cov `(I−KZ)Σ⁻` | ✅ |
| 03:136 | Joseph form `Σ=(I−KZ)Σ⁻(I−KZ)'+KHK'` | ✅ **correct** (contrast with index:47) |
| 06:42–44 | SV model + measurement density `p(y|h)=1/√(2π)e^{−h/2}exp(−½y²e^{−h})` | ✅ re-derived from `y=e^{h/2}ε` |
| 06:48–55 | Bootstrap PF weights/estimate/ESS/resample/propagate | ✅ |

**Error 1 — `index.md:47` (Joseph form, wrong matrices).**
Stated: `Σ_{t|t}=(I-K_tH_t)Σ_{t|t-1}(I-K_tH_t)^\top+K_tR_tK_t^\top`.
Under this folder's own notation (index:29 → `Z_t`=observation/design matrix, `H_t`=measurement-noise covariance, `R_t`=process-noise selection), the Joseph form must use `Z_t` and `H_t`:
**Correct:** `Σ_{t|t}=(I-K_tZ_t)\Sigma_{t\mid t-1}(I-K_tZ_t)^\top+K_tH_tK_t^\top`.
The hub has swapped in `H_t` where `Z_t` belongs and `R_t` where `H_t` belongs. Notably `03-the-kalman-filter.md:136` writes the *correct* form, so the hub contradicts its own sub-page. (The written form is the standard Joseph form only under the control-theory convention where `H`=measurement matrix and `R`=measurement noise — the same clash as Error 3.)

**Error 2 — `index.md:44` (steady-state row; Riccati convention).**
Stated: "`Σ_∞` solves the algebraic Riccati equation (scalar: `Σ=r(Σ+q)/(Σ+q+r)`)", `q=.25,r=1 ⇒ Σ_∞=0.390388, K_∞=0.390388`.
- The gain **`K_∞=0.390388` is correct** (verified: a-priori Σ∞=0.640388, K=0.640388/(0.640388+1)=0.390388).
- But the stated scalar equation `Σ=r(Σ+q)/(Σ+q+r)` is the fixed point of the **a-posteriori (filtered)** covariance recursion, not of the a-priori `Σ_{t|t-1}` defined on index:29. Under the page's own a-priori convention the algebraic Riccati is `Σ²−qΣ−qr=0`, whose solution is **`Σ_∞=0.640388`** (not 0.390388); `0.390388` is the filtered variance `Σ_{t|t}`.
- The presentation `Σ_∞=K_∞=0.390388` is also misleading: the two coincide **only because `r=1`** (a-posteriori `=rΣ⁻/(Σ⁻+r)`, gain `=Σ⁻/(Σ⁻+r)`; equal iff `r=1`), not as a general fact. It also contradicts `03-the-kalman-filter.md:128,130`, where `Σ_∞` is correctly reported as the **a-priori** covariance (`0.717891`, gain `0.417891`). A reader who plugs the hub's `Σ_∞=0.390388` into `Σ_{t|t-1}` is off by ~64%.

**Error 3 — `index.md:23` (essence box; notation clash with §2).**
The one-sentence essence writes the gain as `K=P^-H^\top(HP^-H^\top+R)^{-1}`, using the control-theory convention (`H`=measurement matrix, `R`=measurement noise). Line 29 of the same hub and every other formula define `Z_t`=observation matrix, `H_t`=measurement-noise covariance, `R_t`=process-noise selection (Tsay's convention). Mixing the two on one page is exactly what produces Error 1; the box should read `K=\Sigma^-Z^\top(Z\Sigma^-Z^\top+H)^{-1}` to match the rest of the hub.

*(Not counted as errors: `02:92` prints "(Tsay: 0.0735)" beside a computed `0.0736` — pure rounding; `02:120` says `σ_η=0.074` — rounding.)*

## 3. CODE — every ```python block executed
All blocks run with `python3`, exit 0, **output matches the documented fence exactly** (no drift):
| File | Block @L | Result |
|---|---|---|
| index.md | 58 | ✅ exact match (`x_post=0.833333 P_post=0.555556 loglik=-1.824404`; `Sigma_inf=0.390388 K_inf=0.390388`) |
| 01-from-zero-intuition.md | 60 | ✅ exact match (`raw RMSE=1.0324`, `KF RMSE=0.4241`, `58.9%`, `K*=0.1318`) |
| 02-state-space-models.md | 67 | ✅ exact match (round-trip θ=0.5; Alcoa σ_e=0.4802, σ_η=0.0736; `6.5x`; companion diff `0.00e+00`) |
| 03-the-kalman-filter.md | 77 | ✅ exact match (`3.53e-12`; `Sigma_inf=0.717891 K_inf=0.417891`) |
| 04-time-varying-beta.md | 66 | ✅ exact match (`RMSE KF=0.0187`, `OLS=0.1164`, `83.9%`, endpoint `1.2729` vs true `1.0195`) |
| 05-failure-modes-and-practice.md | 63 | ✅ exact match (all five Q rows; `K_500=2.00e-03`, `ratio 56x`, `RMSE 3.5252`) |
| 06-advanced-extensions.md | 63 | ✅ exact match (variance `44.4%`, RMSE `15.2%`; `0.3298`, `corr 0.6278`, `ESS 2995.0`) |

**blocks_run = 7** — all executed, none failed, zero output drift.

## 4. COHERENCE — hub ↔ sub-pages, jargon, links, contradictions
- ✅ **Prereq chain consistent:** hub:11 states folder prereqs (LinAlg, Probability) apply to `02`–`06` while `01` has smaller entry requirements; `01:11` confirms "none beyond high-school algebra". `02`→`03`→`04`→`05`→`06` chain on the sub-pages is linear and matches the hub's reading arc (index:127–131).
- ✅ **Numbers cross-consistent:** hub lookup table matches sub-pages — KF RMSE `0.0187` vs OLS `0.1164` (04); smoother variance `↓44.4%`, RMSE `↓15.2%` (06); Alcoa `σ_e=0.4802, σ_η=0.0736` (02). No contradictions besides Errors 1–3.
- ✅ **Jargon uniform:** `Σ_{t|t-1}` a-priori, `T_t/Z_t/Q_t/H_t/R_t`, standardized innovation `v_t/√V_t`, ESS, Riccati — used consistently across files.
- ✅ **Links:** every real `[[...]]` wikilink in all 7 files resolves to an existing target (0 broken). (The regex flags `[[1.0]]`/`[[se2]]` etc. are numpy literals inside code fences, not wikilinks.) Sibling/cross-pillar links (`statistical-arbitrage-and-pairs-trading`, `fundamental-multi-factor-models`, `backtesting-hygiene`, `regime-classification-hmm-and-gmm`, `cross-sectional-and-time-series-momentum`, the flat `signal-processing-and-kalman-filtering` note) all exist.
- ✅ **Verified-source claims:** Tsay eq/section attributions all match `tsay_ch10-12.md` (11.14, 11.25, 11.26–11.27, 11.29, 11.64, 11.1.6, 11.4.1, 11.4–11.5). The "in the corpus" book claims (Hilpisch, Strimpel, Vidyamurthy) are borne out by the `corpus/titles/` manifest (they are listed there, largely `PAYWALLED_NO_ACCESS`), so not flagging.
- ⚠️ **Minor (not counted):** `04:37` says "Everything below is just the Kalman recursion of page 03 with these matrices", but the `04` code uses the **contemporaneous (filtered)** covariance form `P=(I−KZ)P`, whereas page 03's canonical (11.64) form — and `03:139` explicitly warns against mixing the two — uses `Σ_{t+1|t}=TΣ_{t|t-1}L'+RQR'`. `04` is internally consistent and numerically equivalent, so no numeric error; the phrasing is just imprecise.

---

## Error ledger
1. **[MATH]** `index.md:47` — Joseph form uses `H_t` where `Z_t` belongs and `R_t` where `H_t` belongs. Correct: `Σ_{t|t}=(I-K_tZ_t)Σ_{t|t-1}(I-K_tZ_t)^\top+K_tH_tK_t^\top` (as `03-the-kalman-filter.md:136`).
2. **[MATH]** `index.md:44` — steady-state row: `Σ_∞=0.390388` is the **a-posteriori** variance, not the a-priori `Σ_{t|t-1}` the page defines; the stated scalar Riccati `Σ=r(Σ+q)/(Σ+q+r)` is the filtered-covariance fixed point. A-priori steady state is `Σ²−qΣ−qr=0 ⇒ Σ_∞=0.640388`. `K_∞=0.390388` is correct; `Σ_∞=K_∞` holds only because `r=1`.
3. **[COHERENCE/NOTATION]** `index.md:23` — essence box gain `K=P⁻H'(HP⁻H'+R)⁻¹` clashes with the hub's own §2 notation (`Z`=design, `H`=measurement noise); should read `K=Σ⁻Z'(ZΣ⁻Z'+H)⁻¹`. Root cause shared with Error 1.

**errors_found = 3** · **files_checked = 7** · **blocks_run = 7**

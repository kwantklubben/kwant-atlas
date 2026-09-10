# Audit — `content/pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/`

**Reviewer:** sole, adversarial · **Date:** 2026-09-10
**Files:** 7 (index + 01…06) · **Code blocks:** 7/7 extracted and executed · **Verdict:** PASS WITH FIXES

---

## 1. Verdict

The folder is **structurally sound and correct in its core apparatus**. All seven `python`
blocks run to completion with deterministic seeds and reproduce their documented output
fences **byte-for-byte**. Every headline formula (SNR↔R², IC ceiling, AR(1) effective sample
size, bias–variance / optimism, fractional-difference weights, regime-shift misspecification
term, expected-max selection bias, MinBTL, Deflated Sharpe) re-derives correctly. All 77
wikilinks resolve; no broken link, no malformed LaTeX, no non-running code.

Two defects found, both **label/consistency errors rather than wrong constants**:

1. A **covariance subscript** that contradicts its own right-hand side (and the page's own
   correlation formula) — `02:34`.
2. A **non-sequitur numeric inference** that attaches the Bailey "45 configurations / 5 years"
   figure to a formula that actually yields ~12 — `05:44`.

---

## 2. Issues

| # | file:line | Problem | Fix |
|---|---|---|---|
| 1 | `02-why-finance-is-different.md:34` | **Covariance subscript inconsistent with its own RHS.** Text: "Two labels offset by $j$ share $h-j$ returns, so $\operatorname{Cov}(y_t,\,y_{t+h-j})=\sigma^2(h-j)$". A subscript of $t+h-j$ means an **index offset of $h-j$**, for which the overlap is $j$ returns, so the RHS would be $\sigma^2 j$ — not $\sigma^2(h-j)$. The stated $\sigma^2(h-j)$ matches an offset of $j$ (i.e. $\operatorname{Cov}(y_t,y_{t+j})$) and is what the very next formula $\operatorname{Corr}=1-\lvert t-t'\rvert/h$ demands (offset $j$ ⟹ corr $=1-j/h$; "consecutive labels ($j{=}1$) have correlation $(h-1)/h$" ✓). So the **subscript is the error**, not the coefficient. | Write $\operatorname{Cov}(y_t,\,y_{t+j})=\sigma^2(h-j)$ (offset $j$), or equivalently $\operatorname{Cov}(y_t,y_{t+h-j})=\sigma^2 j$. |
| 2 | `05-failure-modes-and-practice.md:44` | **"…which is exactly why a 5-year backtest can only support $\approx45$ independent configurations" does not follow from the quoted formula.** The page states $y\ge 2\ln N/\mathrm{SR}_{\text{IS}}^2$, which for $\mathrm{SR}_{\text{IS}}{=}1,\ y{=}5$ gives $N\le e^{5/2}\approx12$, **not 45**. The Bailey figure (paper §"Minimum Backtest Length", verified against the source: "if only five years of data are available, no more than forty-five independent model configurations should be tried") comes from the **exact** MinBTL $=(E[\max_N Z])^2/\mathrm{SR}_{\text{IS}}^2$ with $E[\max_N Z]=(1-\gamma)\Phi^{-1}(1-1/N)+\gamma\Phi^{-1}(1-1/(Ne))$: for $N{=}45$, $E[\max]{=}2.235\Rightarrow y{=}5.0$ yr (and $N{=}7\Rightarrow1.92$ yr, matching the paper's "two-year backtest, 7 configs"). The page's own $\sqrt{2\ln N}$ bound gives $7.6$ yr for $N{=}45$ — i.e. it **overstates** the paper's 5 yr, so the two statements are not the same relation. | Either (a) keep the upper-bound formula and write "…supports only $\approx12$ independent configurations", or (b) present the exact MinBTL $=(E[\max_N Z])^2/\mathrm{SR}_{\text{IS}}^2$ (giving 5 yr / 45 configs) and reserve $2\ln N/\mathrm{SR}^2$ for the upper bound, saying so. |

**Nitpicks (not counted as errors):**

- `index.md:28` — "*All numbers in the check column were re-executed and reproduced exactly from the verified code in §3*". The §3 block computes only the IC↔R² and $\mathbb{E}[\max]$ rows; the $N_{\text{eff}}{=}52.6$ row (`index:38`) and the MinBTL $7.6$ row (`index:41`) are **not** produced by §3 (they live in `03`/`05`). Reword to "from the verified code in this folder's §3 of each page".
- `index.md:39`, `05:36,121`, `06:31` — $\sqrt{2\ln N}$ is the paper's **stated upper bound** on $\mathbb{E}[\max_N Z]$, not the expectation itself. The exact value is lower by ~14% at $N{=}1000$ ($3.25$ vs $3.72$) and materially at $N{=}200$ ($2.767$ vs the printed $3.255$). The `≈` keeps it defensible, but the label "expected max" is imprecise; the sibling folder (`01-quantitative-research/backtesting-hygiene`) uses the exact order-statistic form for the same quantity — consider aligning.
- `index.md:89` — the $+0.13$ leakage is `02`'s measured result ($+0.1263$); `05`'s Experiment A measures a *different* leak ($+0.047$), so "see 02/05" is loose.
- `index.md:114` — "Absolute beginner: 01 — no prior knowledge needed" vs `01:11` stating a prerequisite (Statistics & Inference). Minor tension (same pattern accepted in the sibling folder).

---

## 3. Math verified (re-derived independently)

ESL items are anchored by `corpus/verified/esl_ch6-10.md` (eq. 7.9 bias–variance ✓; optimism
$(2d/N)\sigma_\varepsilon^2$ eq. 7.24 ✓; §7.10.2 wrong-vs-right screening **3% vs true 50%** ✓).
The Bailey/LdP items were checked against the primary source text of *Pseudo-Mathematics and
Financial Charlatanism* (Notices AMS 61(5), 2014) — eq. (4)/(5)/(6), the "upper bound
$\sqrt{2\ln N}$" statement, and the "forty-five configurations / five years" figure.

| Formula (location) | Check | Result |
|---|---|---|
| $R^2=\mathrm{SNR}^2/(1+\mathrm{SNR}^2)$; $\mathrm{SNR}{=}0.0501\Rightarrow R^2$ (index:36) | $0.0501^2/(1.00251)$ | ✓ 0.00250 |
| IC ceiling $R^2_{\text{OOS}}\le\mathrm{IC}^2$; IC$=0.05$ (index:37, 03:40–44) | $0.05^2$ | ✓ 0.25% |
| $\mathrm{IC}=\sigma_s/\sqrt{\sigma_s^2+\sigma_\varepsilon^2}\Rightarrow R^2=\mathrm{IC}^2$ (03:40–42) | corr of scaled forecast with $r=s+\varepsilon$ | ✓ |
| $N_{\text{eff}}=T(1-\rho)/(1+\rho)$; $\rho{=}0.9,T{=}1000$ (index:38, 03:23,52) | $1000\cdot0.1/1.9$ | ✓ 52.6 |
| $\operatorname{Var}(\bar x)=\sigma_x^2(1+\rho)/((1-\rho)T)$ (03:46–48) | AR(1) geometric sum | ✓ |
| $\mathbb{E}[\max_N]\approx\sqrt{2\ln N}$; $N{=}1000$ (index:39) | $\sqrt{13.8155}$ | ✓ 3.717 (upper bound; exact $\approx3.25$) |
| bias–variance MSE + optimism $2p\sigma_\varepsilon^2/N$ (01:23,37,43) | ESL 7.9 / 7.24 | ✓ (matches corpus) |
| Overlap $\operatorname{Corr}(y_t,y_{t'})=1-\lvert t-t'\rvert/h$, $j{=}1\Rightarrow(h-1)/h$ (02:34) | $1-1/h$ | ✓ (corr ok; **Cov subscript wrong — issue #1**) |
| Regime-shift term $\sigma_B^2+(\beta_A-\beta_B)^2\mathbb{E}[x_t^2]$ (04:38) | $(y-\hat\beta_A x)^2$, $y=\beta_B x+\varepsilon_B$ | ✓ |
| Fractional weights $w_k=(-1)^k\binom{d}{k}$, $\binom{d}{k}=\prod_{i\le k}(d-i+1)/i$ (04:44, 06:41) | AFML Ch. 5 | ✓ |
| MinBTL $y\ge2\ln N/\mathrm{SR}_{\text{IS}}^2$; $N{=}45,\mathrm{SR}{=}1$ (index:41, 05:42) | $2\ln45$ | ✓ 7.61 (valid **upper bound**; exact $=5.0$ — see issue #2) |
| Selection bias $\mathbb{E}[\max\mathrm{SR}]\approx\sqrt{2\ln N}$ (05:36–38) | — | ✓ |
| **DSR** boxed (06:33) | $\Phi[({\rm SR}-{\rm SR_0})\sqrt{n-1}/\sqrt{1-\gamma_3{\rm SR}+((\gamma_4-1)/4){\rm SR}^2}]$; normal $\Rightarrow\sqrt{1+\tfrac12{\rm SR}^2}$ | ✓ canonical form |
| DSR worked sweep (06 §3) | $n{=}756,\ {\rm SR}{=}1/\sqrt{252},$ `SR*`=$\sqrt{2\ln N}/27.5$ | ✓ 0.958 / 0.405 / 0.153 / 0.097 / 0.024 |
| DSR $\mathrm{SR}_0=\sqrt{2\ln N}/\sqrt n$ (06:35) | per-period rescaling of $\mathbb{E}[\max]$ | ✓ consistent (conservative vs exact $\mathbb{E}[\max]$) |
| §7.10.2 prose "3% vs true 50%" (02:110, 05:34) | ESL source | ✓ (corpus-confirmed) |

**No wrong sign, no wrong constant, no inverted inequality** was found in any boxed formula.

---

## 4. Code stats (diffed stdout vs the following output fence)

| File | Block | Runs | Seed | Output fence |
|---|---|---|---|---|
| `index.md` | IC↔R² + $\mathbb{E}[\max_N]$ table | ✓ rc=0 | none (deterministic) | **exact match** |
| `01-from-zero-intuition.md` | ridge polynomial in/out-of-sample R² | ✓ rc=0 | 7 | **exact match** |
| `02-why-finance-is-different.md` | random 5-fold vs walk-forward on overlapping labels | ✓ rc=0 | 5 | **exact match** |
| `03-the-low-snr-problem.md` | $N_{\text{eff}}$ + AR(1) MC variance + IC ceiling | ✓ rc=0 | 5 | **exact match** |
| `04-non-stationarity-and-samples.md` | regime-shift sign-flip R² | ✓ rc=0 | 13 | **exact match** |
| `05-failure-modes-and-practice.md` | ESL wrong-vs-right CV + 200-strategy selection bias | ✓ rc=0 | 0 / 123 | **exact match** |
| `06-advanced-extensions.md` | Deflated Sharpe sweep | ✓ rc=0 | none (deterministic) | **exact match** |

**7/7 blocks run; 7/7 reproduce their documented stdout exactly** (verified by executing each
fenced `python` block and diffing against the immediately-following output fence). Six blocks
are stdlib-only (`math`, `random`); `05` additionally imports `numpy.random.default_rng`
(available) and pins the global `random` seed for the Sharpe MC. All MC blocks are seed-pinned
and deterministic cross-machine.

---

## 5. Links & coherence

- **Wikilinks: 77 total, 77 resolve** (index 15, 01 4, 02 10, 03 12, 04 10, 05 13, 06 13 — counts
  include the long-form in-folder paths). Zero broken links.
- **Hub ↔ 01 prereq consistent:** `index:12` scopes the folder-level prerequisites to pages
  02–06 and explicitly defers page 01 to its own (strictly smaller) entry requirements; `01:11`
  lists only Statistics & Inference. No conflict (nitpick on `index:114` wording above).
- **Hub structure consistent:** "six sub-pages" ↔ six files 01–06; the §4 five-item failure-mode
  list matches `05`'s five names one-for-one; the §1 route map (SNR ceiling → non-stationarity →
  failure modes → advanced toolkit) matches the page order.
- **Jargon first-use:** SNR and IC defined at `index:18`; $N_{\text{eff}}$, DSR, fractional
  differentiation, purged/embargoed CV, PIT, MinBTL all defined at or before first use. Clean.
- **LaTeX:** no unmatched `$`/`$$` (each `$$` block balanced); no malformed token of the kind
  found in the sibling folder.
- **Spelling/typos in prose:** no misspellings or doubled words found in prose (domain terms —
  SNR, IC, DSR, PBO, IID, AR(1), MinBTL, HMM/GMM — all legitimate).
- **Citations:** Notices AMS 61(5) 2014, JPM 40(5) 2014, J. Comp. Finance 20(4) 2017, RFS 33(5)
  2020, Hamilton Econometrica 57(2) 1989 all check out.

---

## 6. Notes / caveats

- Only the ESL claims have a `corpus/verified/` anchor (`esl_ch6-10.md`). The Bailey/López de
  Prado claims were validated by re-derivation **and** by direct comparison with the primary
  source text of the Notices AMS paper (fetched to confirm the MinBTL "forty-five / five years"
  figure and the $\sqrt{2\ln N}$ upper-bound statement).
- Blocks were executed with `python3` from the repo root; each is self-contained.
- The two fixes are one-line edits and do not touch any rendered number in a code fence.

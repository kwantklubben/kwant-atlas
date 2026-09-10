# Topic Audit — `foundations/econometrics-and-timeseries/`

**Auditor:** Sole reviewer (adversarial, per-topic).
**Date:** 2026-09-10
**Scope:** 7 files (index + 01–06). House style respected: wikilinks, `$..$`/`$$..$$` math, 6-subpage structure, corpus-verified claims.
**Method:** (1) prose spell-scan (pyspellchecker en_US, code/LaTeX stripped), (2) full re-derivation of every boxed/inline formula + numerical simulation where needed, cross-checked against `corpus/verified/tsay_ch1-3/ch4-6/ch7-9/ch10-12.md`, (3) executed all 7 ` ```python ` blocks with stdlib-only Python 3.14 and diffed stdout against the documented output, (4) coherence: wikilink resolution, hub↔subpage prereq chain, sign conventions, internal numeric consistency.

---

## Verdict

**PASS with 4 fixable errors.** No fabrications; math is otherwise well-grounded and every claimed empirical/verified number in the prose and code output reproduces exactly. One genuine formula sign error (ARMA(1,1) variance), one sign-convention mismatch (MA(1) model display vs its ACF), one internal code-vs-table inconsistency in the hub, and one LaTeX-rendering bug (unescaped currency `$`). All 7 code blocks run clean and match their documented output byte-for-byte.

---

## 1. SPELLING / TYPOS

Automated spell-scan of all prose (math, LaTeX, and code fenced blocks stripped) returned **0 genuine misspellings**. The only "unknown" tokens are legitimate domain vocabulary/abbreviations: `cointegrated`, `ehacf`, `eacf`, `pacf`, `EGARCH`, `TGARCH`, `RiskMetrics`, `GARCH-M`, `lognormal`, `Jarque`, `Bera`, `Korajczyk`, `invertibility`, `reparameterization`, `detrending`, `heteroskedasticity`, etc.

No spelling/typo findings.

---

## 2. MATH — formula-by-formula re-derivation

Almost everything checks out against `tsay_ch1-3/4-6/7-9/10-12.md`. Confirmed **correct** (not exhaustive):
- AR(1) mean `φ0/(1−φ1)`, var `σ²/(1−φ1²)`, ACF `ρℓ=φ1^ℓ`; AR(2) `ρℓ=φ1ρℓ−1+φ2ρℓ−2`; cycle `k=2π/cos⁻¹[φ1/(2√(−φ2))]` ✓ (tsay ch1-3 L46–47)
- Wold `ρℓ=Σψiψi+ℓ/Σψi²`, Var `σ_a²Σψi²` ✓
- Ljung–Box `Q=T(T+2)Σρ̂²/(T−ℓ)`, df `m−g` for AR residuals ✓; Jarque–Bera `JB=Ŝ²/(6/T)+(K̂−3)²/(24/T)` ✓
- ADF: `∇x=c+βc x_{t−1}+Σφi∇x_{t−i}+e`, `βc=φ1−1`, DF distribution, criticals `−3.43/−2.86/−2.57` ✓ (tsay ch1-3 L55)
- Forecast-error var `E[Var e_h(ℓ)]=(1+ψ1²+…+ψ_{ℓ−1}²)σ_a²` ✓; RW forecast-error `ℓ σ_a²` ✓; AR(1) half-life `ln(0.5)/ln|φ1|` ✓ (φ1=0.8→3.11 periods ✓)
- 15-day Gauss AR(2)-GARCH VaR `$1,039,191 < $1,114,257=√15·$287,700` → √T rule overstates ~7.2% ✓ (tsay ch7-9 L34,38)
- ARCH(1) uncond kurtosis `3(1−α1²)/(1−3α1²)`, finite 4th moment needs `α1²<1/3` ✓
- GARCH stationarity `Σ_{i≤max(m,s)}(αi+βi)<1`; uncond var `ω/(1−α−β)`; heavy-tails `1−2α²−(α+β)²>0`; multi-step `σ_h²(ℓ)=α0+(α1+β1)σ_h²(ℓ−1)` ✓
- IGARCH uncond var undefined; `σ_h²(ℓ)=σ_h²(1)+(ℓ−1)α0`; RiskMetrics EWMA `(1−β)a²_{t−1}+βσ²_{t−1}` β≈0.94 ✓
- EGARCH g-form `g(ε)=θε+γ[|ε|−E|ε|]`, E|ε|=√(2/π), slopes (θ+γ)/(θ−γ), θ<0 leverage; IBM −2σ vs +2σ ≈37% more ✓ (correctly attributes leverage to **θ** in the g-form — the exact correction from tsay ch1-3 L104)
- TGARCH/GJR `N_{t−i}=1{a_{t−i}<0}` ✓; GARCH-M `r=µ+cσ²_t+a` ✓; GARCH excess kurtosis `6α1²/[1−2α1²−(α1+β1)²]` ✓
- ECM `∇x_t=αβ'x_{t−1}+ΣΦ*∇x+…`, `αβ'=−Φ(1)`, rank cases 0/k/m ✓; Johansen eigen-problem `|λS11−S10S00^{-1}S01|=0`, trace & max `−(T−p)Σln(1−λ̂)` ✓ (tsay ch7-9 L62–63)
- TB3m/TB6m example: VAR(3), trace 83.27 vs CV 19.96, coint vector `tb3m−1.0124·tb6m`, ECM α=(−0.0949,−0.0211) ✓ — exact (tsay ch7-9 L64)
- Pairs trading ECM `[r1,r2]'=[α1,α2]'(w_{t−1}−µ_w)+ε`, opposite signs, `2δ>η`, profit `2δ−η` ✓
- State-space/Kalman: `v,y,Z`, `V=ZΣZ'+H`, `K=TΣZ'V^{-1}`, `L=T−KZ`, `s_{t+1|t}=d+Ts_{t|t−1}+Kv`, `Σ_{t+1|t}=TΣL'+RQR'` ✓ (tsay ch10-12 L36–38)
- Local-level ↔ ARIMA(0,1,1) map `(1+θ²)σ_a²=2σ_e²+ση²`, `θσ_a²=σ_e²` ✓; Alcoa θ̂=0.858, σ̂a=0.5184 → σ̂e=0.4803≫σ̂η=0.0735 ✓ exact (tsay ch10-12 L47)
- Markov switching `1/w_i` durations, US real GNP ≈3.7/11.3 qtrs ✓; MH ratio `r=f(θ*|X)J_t(θ_{t−1}|θ*)/[f(θ_{t−1}|X)J_t(θ*|θ_{t−1})]`, accept min(r,1) ✓; Gibbs `θ̄=(1/(n−m))Σ_{j=m+1}^n θ_j` ✓
- Cisco+Intel portfolio VaR ordering `$57,117 < $57,648 < $58,180` ✓ exact (tsay ch10-12 L18); BEKK param count `k²(m+s)+k(k+1)/2` ✓; DCC `Q_t=(1−θ1−θ2)Q̄+θ1εε'+θ2Q_{t−1}` ✓; multivariate-t as standardized (v−2) form ✓

### ERROR 1 (HIGH, math sign) — `02-stationarity-and-arma.md:43`
**Stated:** ARMA(1,1) variance `(1−2φθ+θ²)σ_a²/(1−φ²)`.
**Corrected:** with the ARMA(1,1) model exactly as the file writes it on the same line — `x_t=φx_{t−1}+a_t+θa_{t−1}` — and consistent with the file's own, Tsay-correct ρ1 formula on the next line (`ρ1=(1+θφ)(φ+θ)/(1+2θφ+θ²)`, which uses the `+θ` convention), the variance is **`(1+2φθ+θ²)σ_a²/(1−φ²)`**.
- Derivations: γ0(1−φ²)=σ_a²(1+2φθ+θ²) from E[x_t²]=φγ1+σ_a²+θ(φ+θ)σ_a² and γ1=φγ0+θσ_a².
- Numerical confirmation (simulation, φ=0.5,θ=0.3): sample var = 1.857σ_a²; `(1+2φθ+θ²)/(1−φ²)=1.853` ✓ vs stated `(1−2φθ+θ²)/(1−φ²)=1.053` ✗.
- Root cause: the file mixes the Tsay-MA/ARMA **`−θ`** convention (which gives the `−2φθ` variance) with the **`+θ`** convention used by the very next ρ1 formula and by the code; the ρ1/code are right, so the variance's minus sign is the error. (`corpus/verified/tsay_ch1-3.md` L51 transcribes the book's `−` form, but the document's own stated model and ρ1 use `+`, so the document self-contradicts regardless.)

### ERROR 2 (LOW–MED, sign-convention display) — `index.md:39` and `02-stationarity-and-arma.md:41`
**Stated:** MA(1) model `x_t=a_t+θ_1 a_{t-1}` **and** `ρ1=−θ_1/(1+θ_1²)`.
The `ρ1=−θ/(1+θ²)` value is the correct textbook (Tsay) result, but it belongs to the **`−θ`** convention `x_t=a_t−θ_1a_{t-1}`. Under the `+θ` model as displayed, `ρ1=+θ/(1+θ²)` (simulation, θ=0.4: model `a_t+0.4a_{t−1}` → ρ1=+0.345, not −0.345). Fix: display the model as `x_t=a_t−θ_1 a_{t-1}`, OR flip the ACF sign — do not state both.
This is the same convention slip as Error 1; the values match Tsay, so it is a display/notation bug rather than a mis-stated result.

---

## 3. CODE — all 7 blocks executed

All blocks were run with stdlib-only Python 3.14 (`python3`), no external packages, matching the pages' own "no numpy/scipy" claim. **All 7 exit 0 and their stdout matches the documented output exactly** (block-by-block):

| Block | Executed output (matches doc) |
|---|---|
| `index` §3 | ADF `−19.117` / RW `−1.905` / LB `18.137` ✓ |
| `01` §3 | ACFs `0.9902 / −0.0095 / 0.0137`, mean `0.659` ✓ |
| `02` §3 | YW `(1.213,−0.605)`, PACF `[0.756,−0.605,0.003,−0.027]`, ρ1 `0.6619/0.6611`, ρ3 `0.1634` ✓ |
| `03` §3 | spurious `R²=0.248` / non-rej `177/200`, ADF `−15.613 / −0.638` ✓ |
| `04` §3 | LM `2817.2`, MLE `(0.0588,0.1178,0.8257)`, uncond var `1.0417`, persist `0.9436` ✓ |
| `05` §3 | β̂ `(1.041,1.995)`, ADF `−17.026`, ECM `−0.434`, indep-RW ADF `−0.831` ✓ |
| `06` §3 | MAE `0.333/0.744`, gain `0.181`, `σe=0.4802/ση=0.0736`, regime agreement `0.911` ✓ |

Prose interpretations following each code block (e.g. 04: "recovers (α,β)≈(0.118,0.826)… persistence 0.944≈0.95… uncond var 1.04≈1.0") are consistent with the actual output.

### ERROR 3 (MED, code-vs-table coherence) — `index.md:42` and `index.md:51`
The hub's §2 "Verified check" column and its own §3 script disagree **on the same page**:
- Index §3 code (seed 1, φ=0.7) prints **RW ADF `−1.905`** and **AR ADF `−19.117`**.
- Table line 42 (Random walk row) claims **RW ADF `−0.64`**.
- Table line 51 (ADF row) claims **AR `−15.6` vs RW `−0.64`**.
- Table line 37 (AR(1) row) claims **`−19.1`** (matches §3 code).

So the table reports three different "ADF on RW / stationary AR(1)" figures; `−0.64` and `−15.6` actually originate from the **03 subpage's** different simulation (seed 9, φ=0.6 → `−0.638`/`−15.613`), not from index §3 code which §3's intro sentence claims "reproduces the key-test column above". The qualitative verdicts (reject / cannot-reject) are all correct, and all values are legitimate outputs, but the table and the reproducing script are internally inconsistent. Fix: align the table numbers with the §3 script's actual output (`−19.1` / `−1.905`) or explicitly note the mixed provenance.

---

## 4. COHERENCE / LINKS / CONVENTIONS

- **Wikilinks:** all **21** outbound links (foundations indices, all 6 subpages, and 10 pillar targets) resolve to existing files. No broken links.
- **Prereq chain:** index:10 correctly states folder-level prereqs (LA + Prob/Measure) apply to 02–06 while 01 declares its own smaller entry; 01→Prob only ✓; 02→01; 03→02; 04→02+03; 05→03+LA; 06→04+05. Chain is monotone and cycle-free. Hub's "Reading route" (beginner 01→02→03→04, then 05→06) matches the subpage prereq graph.
- **Jargon/fixed terms:** consistent `σ_t²=Var(r_t|F_{t−1})`, `a_t` innovations, `ε_t` shocks, `B` backshift. ACF/PACF cut-off story (AR→PACF cuts, MA→ACF cuts) is consistent across 02 and index.
- **3-regime correction applied:** 05:45 and 05:114 carry the corrected threshold-cointegration reading (three regimes, ECM active only in outer bands, "Not '2-regime'"), matching tsay ch7-9 C8-1. No stale 2-regime text remains.
- **EGARCH leverage attribution** is correctly assigned to θ (not γ) in the g-form — matches the correction flagged in tsay ch1-3.
- **Kalman Σ-recursion warning** (06:110 — don't mix the two equivalent forms) matches the verified note; correctly included as a failure mode.
- **No contradictions** beyond Error 3; no leftover TODO/FIXME/markers.
- Math-delimiter audit: all files have balanced `$`/`$$` and braces **except 06:45** (see Error 4).

### ERROR 4 (MED, LaTeX/render) — `06-advanced-extensions.md:45`
Raw text: `Verified example (Cisco+Intel, $1M each, 5%): univariate $57,117$ < time-varying-corr $57,648$ < constant-corr $58,180$.`
The currency **`$1M`** is unescaped, so it opens a KaTeX/`$..$` inline-math span that swallows `1M each, 5%): univariate ` until the next `$` — corrupting rendering of the sentence. The `$57,117$`/`$57,648$`/`$58,180$` currency values are likewise wrapped as math. Contrast with **03:34**, which correctly writes `\$1,039,191` / `\$1,114,257`. Fix: `\$1M`, `\$57,117`, `\$57,648`, `\$58,180`.

---

## Findings summary

| # | Severity | File:line | Type | Issue |
|---|---|---|---|---|
| 1 | HIGH | 02:43 | Math sign | ARMA(1,1) variance `(1−2φθ+θ²)` should be `(1+2φθ+θ²)` under the stated `+θ` model/ρ1; numerically 1.85 vs 1.05 σ² for φ=0.5,θ=0.3 |
| 2 | LOW–MED | index:39, 02:41 | Math/convention | MA(1) written `a_t+θa_{t−1}` but ACF `ρ1=−θ/(1+θ²)` is the `−θ` result; display must match one convention |
| 3 | MED | index:42,51 | Coherence/code | Table's RW ADF `−0.64`/AR `−15.6` contradict the page's own §3 script (`−1.905`/`−19.117`); `−0.64/−15.6` come from the 03 subpage simulation |
| 4 | MED | 06:45 | Render/LaTeX | Unescaped currency `$1M` (+ `$57,117$` etc.) breaks inline-math parsing; should be `\$` |

No spelling, no broken links, no other formula/code issues. Code blocks: 7/7 executed, all match documented output.

*EOF*
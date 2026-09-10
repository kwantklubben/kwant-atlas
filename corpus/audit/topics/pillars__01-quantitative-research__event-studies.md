# Audit: `content/pillars/01-quantitative-research/event-studies/`

**Sole reviewer, adversarial pass.** Folder = 7 files (index hub + 6 sub-pages). Scope: spelling/typos in prose, math (every boxed formula + worked example, cross-checked vs standard theory and `corpus/verified/`), code (every ```python block executed and diffed), coherence (hub↔01 prereqs, jargon, links, contradictions). Ignored `_legacy/`.

**Verdict: FAIL — 2 factual math errors in the hub's "Verified check" table + 2 minor coherence issues. All 7 python blocks reproduce their documented output exactly; all prose/formulas otherwise clean.**

---

## 1. Code verification (7/7 blocks run, all pass)

Blocks extracted from each file and executed under Python 3.11; output diffed against the documented ```` ``` ```` output fences. Every block is seeded, so output is deterministic and byte-matchable.

| File | Block | Result | Diff vs documented |
|---|---|---|---|
| index.md | §3 market-model AR computation (seed 11) | Ran clean | **Exact match** |
| 01-from-zero-intuition.md | §3 mean-adjusted abnormal return (seed 3) | Ran clean | **Exact match** (−0.217 / +2.500 / +2.717) |
| 02-event-study-methodology.md | §3 full market-model pipeline (seed 11) | Ran clean | **Exact match** (239, α=−0.00014, β=1.15870, AR=+3.021%, t=+1.460, CAR(−1,+1)=−1.342%/t=−0.374, CAR(−5,+5)=−3.150%) |
| 03-abnormal-returns-and-car.md | §3 CAR with cross-sectional aggregation (seed 23) | Ran clean | **Exact match** (full 11-day table + CAR(−1,+1)=+1.930%/t=+3.54, CAR(0,+1)=+1.973%/t=+4.43, s=0.315%) |
| 04-statistical-testing.md | §3 cross-correlation SE / variance trap / power (seed 7) | Ran clean | **Exact match** (all SE ratios incl. 1.73@ρ.02/N100; size 4.98% / 16.52%; power 9.2 / 26.6 / 76.2%) |
| 05-failure-modes-and-practice.md | §3 Exp.1 non-synchronous-trading / Scholes–Williams (seed 5) | Ran clean | **Exact match** (TRUE 1.5, OLS +0.873, SW +0.928) |
| 06-advanced-extensions.md | §3 PEAD drift (seed 31) | Ran clean | **Exact match** (+2.90% / −5.98% / spread +8.87%, n=20/17) |

Every documented output line reproduced bit-for-bit (incl. the Monte-Carlo blocks in 04, which are seeded and deterministic). **No code error.**

## 2. Math verification

All boxed formulas and worked examples re-derived; the underlying formulas are correct. **Two transcription errors exist in the hub table only** (see Findings F1–F2).

- **index.md formulas:** market model `R_it=α_i+β_i R_mt+ε_it` ✓; `AR_it=R_it−(α̂_i+β̂_i R_mt)` ✓; mean-adjusted `R_it−(1/L)ΣR_ik` ✓ (BW 1–2); cross-sectional mean `(1/N)ΣAR_it` ✓ (KW eq. 3); `CAR=ΣAR_t` ✓ (KW eq. 4); test stat `J=CAR/√(L·σ²(AR_t))` ✓ (KW eq. 5–6); `BHAR_i=Π(1+R_ik)−Π(1+R_Bk)` ✓ (KW eq. 7); cross-correlation inflation `√(1+(N−1)ρ)` ✓ (KW eq. 10), evaluated at ρ=.02,N=100 → §3/§04 both give **1.73** ✓.
- **01:** return decomposition `R_it=K_it+e_it`, mean-adjusted model, ~239-obs BW window (days −244…−6). All correct.
- **02:** OLS β̂=Cov/Var, α̂=R̄−β̂ R̄_m, prediction-error AR, market-adjusted (α=0,β=1) forcing — all correct.
- **03:** CAR vs BHAR semantics (simple-sum/rebalanced vs compounding/buy-and-hold), BHAR right-skewness/long-horizon cross-correlation — correct.
- **04:** J test st^; cross-correlation SE inflation `√(1+(N−1)ρ)`; ρ=.02,N=100 → **1.73** ✓ (matches table); power approx `P(|Z|>1.96−μ/(σ/√N))` ✓ (standard); variance-double misspecification (5%→16.5%) reproduced exactly in code ✓; "6 firms detect a 10% one-day AR at 100% power" and "200 firms detect 25%-over-5-years <50%" are KW-cited claims (Table 2 / §3.6.4, Jegadeesh–Karceski 2004) — not independently reproduced, but attributed.
- **05:** Scholes–Williams `β̂_SW=(β̂₋₁+β̂₀+β̂₊₁)/(1+2ρ̂_m)` — correct standard formula, and the code's correction runs as documented. Cross-correlation and variance-increase sections consistent with 04.
- **06:** SUE standardization, `AR_i=a+b·SUE_i+u_i` cross-sectional regression (Sefcik–Thompson), drift `∂AR/∂SUE>0`, Carhart four-factor Jensen-alpha regression (`R_pt−R_ft = a_p + b_p(R_mt−R_ft) + s_p SMB + h_p HML + m_p UMD + e_pt`) — all correct.

## 3. Spelling & prose

Full-prose vocabulary audit (prose only, LaTeX/link/code stripped): **zero misspelled or typo'd words.** Grammar and register consistent and clean throughout.

## 4. Coherence

- **Hub↔01 prereqs:** consistent. Hub (index.md:11) states the folder-level entrants (econometrics + statistics) apply to pages 02–06, with page 01 declaring its own smaller entry bar; 01's declared prereqs (econometrics + probability) match that. No contradiction.
- **Cross-page numbers agree EXCEPT the two hub cells flagged below:** β̂=1.1587(0) is stated identically in index/02; AR=+3.021% in index/02; mean-adjusted +2.717% in index/01; ρ-inflation 1.73 in index/04. **The only cross-page discrepancies are index.md:39 and index.md:40 (F1–F2).**
- **Wikilinks:** all in-folder, base, sibling, and forward targets resolve (verified: pillars/04-.../var-and-expected-shortfall, pillars/01-.../backtesting-hygiene-and-deflated-sharpe, momentum/02-cross-sectional-momentum, fundamental-multi-factor-models/index, econometrics-and-timeseries/index, probability-and-measure-theory/index, statistics-and-inference/index). No broken links.
- **Jargon:** consistent and correct (market model, prediction error, CAR/BHAR, non-synchronous trading, cross-sectional dependence, PEAD/SUE, Jensen-alpha/calendar-time).
- **Verified refs:** the folder's "Verified refs/49–52" pointers correspond to `corpus/titles/refs/` (Brown–Warner 1980/85, MacKinlay 1997, Kothari–Warner 2007). `corpus/verified/` contains no event-study paper texts (only the finance/econometrics textbook chapters), so the checks here rest on the formula transcripts + the referenced titles registry; the two failed cells are internal-consistency errors against the folder's own scripts, independent of corpus content.

---

## Findings (4: 2 factual math errors, 2 minor coherence nits)

**F1 (math, hub) — index.md:39, CAR(0,+1) "Verified check" is wrong.**
Stated: `CAR(0,+1) = +1.925%` (Ex. 03). The sub-page 03 §3 script (line 76 output: `CAR(0,+1) = +1.973%`, from AR₀=+1.482% + AR₁=+0.491%) reproduces **+1.973%**. The same page's index.md:29 claims all table numbers "were re-executed and reproduced exactly from the working Python in §3 and the sub-pages," but +1.925% matches neither the §3/03 output (+1.973%) nor the other displayed window CAR(−1,+1)=+1.930%. **Fix: change to `+1.973%`.** *(≈true value format: +1.973%.)*

**F2 (math, hub) — index.md:40, test-statistic "Verified check" t=+4.62 is wrong.**
Stated: `t = +4.62` (Ex. 03). Ex. 03's only printed test statistics are **t(CAR(−1,+1))=+3.54** and **t(CAR(0,+1))=+4.43** (03 §3 output). +4.62 matches neither. (Drift: 4.62 would correspond to ~4.62 but no combined window/t-stat in the folder equals it.) **Fix: change to `+4.43` (CAR(0,+1)) or `+3.54` (CAR(−1,+1)) and label the window.**

**F3 (coherence, minor) — 03-abnormal-returns-and-car.md:96, "the same +1.5% signal that was statistically invisible for one firm in 02."**
02's single-firm experiment injected a **+3%** abnormal return on day 0 (AR=+3.021%, t=+1.460, conveniently below significance); 03's cross-section uses a **+1.5%** mean effect. These are not "the same signal," so the connector sentence slightly mischaracterizes the link to 02. The substantive point (single-firm noise vs N=40 aggregation) is correct. **Fix: reword to "a comparable per-firm signal that was statistically invisible for one firm in 02."**

**F4 (coherence, note) — 05-failure-modes-and-practice.md:92 cites "(Kothari–Warner 1997)".**
This is a real, correct citation — Kothari & Warner (1997), *Measuring Long-Horizon Security Price Performance*, JFE 43(3), 301–339 — not a typo for 2007. However §5's reference list (lines 97–106) lists only the Kothari–Warner **2007** Handbook chapter, so the in-text quote cites a source absent from the page's reference list. **Optional fix: add the 1997 JFE paper to §5, or re-anchor the quote to the 2007 chapter.**

All other "Verified check" cells in the hub table reproduce exactly from the on-page / sub-page scripts. Nothing else requires remediation.
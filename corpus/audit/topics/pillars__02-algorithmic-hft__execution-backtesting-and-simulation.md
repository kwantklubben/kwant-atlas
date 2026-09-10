# Audit — `content/pillars/02-algorithmic-hft/execution-backtesting-and-simulation/`

**Date:** 2026-09-10 · **Reviewer:** sole deep-audit pass (adversarial)
**Scope:** 7 files — `index.md` + `01`..`06` (`_legacy/` ignored).
**Method:** every ```python block extracted to a temp file and run with `python3`
(numpy 2.5.3 / Python 3.14.7) and diffed **byte-for-byte** against its following
output fence; every boxed/display formula re-derived by hand and every worked
example (fill assumptions, latency pick-off, slippage attribution, backtest-vs-live
gap, market-replay bias) recomputed from the code outputs; every `[[wikilink]]`
resolved against `content/**`; prose scanned with a duplicate-word regex, a
space-before-punctuation regex and a manual typo pass (no dictionary available on
host — `hunspell` present but no `en_US` affix/dic installed).

---

## Verdict

**PASS WITH FIXES — ship after one incorrect identity and four mislabelled/unverifiable numbers.**

- **Code: perfect.** All **8** ```python blocks execute cleanly (exit 0) and reproduce their
  documented output **exactly** (byte-for-byte diff). No code errors anywhere.
- **Spelling: clean.** No typos, no doubled words, no spacing defects. Author names
  (Hasbrouck, Almgren, Chriss, Kukanov, Perold, Gould, López de Prado) all correct.
- **Links: all resolve.** The escaped-pipe form `[[.../index\|Alias]]` in `index.md:47` is the
  repo's house convention for wikilinks **inside markdown tables** (also used throughout
  `content/index.md` and `content/diagnostics.md`), not a typo — the target
  `pillars/06-market-making/market-impact-and-depth/index.md` exists.
- **Math:** the core fill/queue/impact machinery is correct and consistent with the code.
  But there is **one genuinely false displayed equation** (`01:50`, the Perold identity),
  **two wrong σ-units claims** (`04:113`, `04:120`), **one mislabelled horizon** (`04:119`),
  and **one "verified" number that no block produces** (`index:38`), plus a cross-page
  unit-convention clash in the Poisson fill-probability formula. Details below.

---

## Issues

| file:line | problem | fix |
| :--- | :--- | :--- |
| `01-from-zero-intuition.md:50` | **FALSE IDENTITY (MATH, major).** The Perold shortfall is printed as `IS = (v−n₁)'π₁ = (n₁−n₀)'(p−π₀) + (v−n₁)'(π₁−π₀)`. The RHS decomposition is correct, but the LHS is **not** equal to it. Counterexample `n₀=0, v=100, n₁=80, p=10.2, π₀=10, π₁=10.5`: LHS `= (100−80)·10.5 = 210`; RHS `= 80·0.2 + 20·0.5 = 26`. The correct left-hand side (paper P&L − actual P&L) is `IS = v(π₁−π₀) − n₁(π₁−p) − n₀(p−π₀)`, which *does* expand to the two RHS terms. The hub `index.md:43` prints the decomposition correctly with **no** bogus LHS — so `01` both is wrong and disagrees with the hub. | Delete `(v−n₁)'π₁=`; keep only the two-term decomposition (or write the correct LHS). |
| `index.md:38` | **Unverifiable "verified" value + unit clash (MATH).** Row "Fill probability by $T$ (Poisson trades)" carries the check *"$x{=}1200\text{ sh}$: closed $0.5306$"*, but **no block in the folder computes a Poisson-tail fill probability at $x=1200$** — the only `x=1200` value anywhere is the *binomial* closed form `closed(1200)=0.0934` (`03` Block A). §3's engine has no such computation, so the "exact run output" claim is unsupported. The formula itself uses bound `k<x`, contradicting `02:49` and `03:42`, which use `k<x/`v̄``. | Either compute it in §3 and cite the real number, or drop the row; reconcile the bound with `02`/`03`. |
| `02-why-execution-backtests-lie.md:49` & `03-the-fill-model.md:42` | **Dimensional inconsistency (MATH).** Both write `𝔽(ξ(T)≥x) = 1 − Σ_{k<x/`v̄`} (μT)^k e^{−μT}/k!` where `ξ(T)~Poisson(μT)` is a **count of trades** (`02:47`: "μ = Poisson trade arrivals") but `x` is in **shares**. The LHS compares a trade-count to a share-count; the RHS bound `x/`v̄`` is the only dimensionally sound one. The hub (`index:38`) instead uses `k<x` with `ξ` as share volume — so the folder states the same law under **two mutually exclusive unit conventions**. Related: `02:51` and `03:45` state the negative-binomial waiting time has "mean `x/μ`", but with trade size `v̄` the mean is `(x/`v̄`)/μ = x/(μ`v̄`)`; `x/μ` is right only if `v̄=1` (or if μ is a share-volume rate, in which case the `x/`v̄`` bound is wrong). | Pick one convention (recommend: `ξ` = cumulative **share** outflow, `μ` = share-volume rate, bound `k<x`, NegBin mean `x/μ`) and apply it on `index`, `02` and `03`. |
| `04-market-replay-vs-monte-carlo.md:113` | **Wrong σ-units (MATH).** "The one recorded path was a lucky draw (**0.36 standard deviations above the mean**) of a distribution with σ=0.45." The run gives mean `0.6384`, sd `0.4511`, replay `1.0000`; the z-score is `(1.0000−0.6384)/0.4511 = 0.80`, not 0.36. The number 0.36 is the raw fill-ratio excess `1.0000−0.6384 = 0.3616`, mis-relabelled as standard deviations. | "**0.80** standard deviations above the mean". |
| `04-market-replay-vs-monte-carlo.md:120` | **Same wrong σ-units (MATH).** "here it landed **0.36σ high** and would have mis-sized the strategy by ~56%." z-score is 0.80σ (see above). The 56% figure is correct (`1/0.6384 − 1 = 56.6%`). | "**0.80σ** high". |
| `04-market-replay-vs-monte-carlo.md:119` | **Mislabelled horizon (MATH/CONSISTENCY).** "the toy replay's P(fill) went 0.3301 → 1.0000 **with a 2× horizon**." Those numbers are `05`'s F3 experiment, whose look-ahead horizon is **4×** (quote lives 150 of 600 events, `05:94`). The *2×* look-ahead experiment is `02`'s, where the causal value is `0.3686`, not 0.3301. So the cited pair and the cited horizon come from two different pages. | Use "4× horizon (150 of 600 events)" and keep 0.3301→1.0000. |
| `index.md:101` & `03-the-fill-model.md:166` | **Overstated precision (MATH prose).** "The closed form and Monte Carlo agree to the third digit" (Cont–Kukanov, block A). The run disagrees at the first–third significant figure: `850.41 vs 848.49`, `609.34 vs 609.51`, `312.85 vs 316.49` (up to ~1.2 %). Only the *binomial* replay-vs-closed comparison (`03` Block A, `03:117`) genuinely agrees to three decimals (`0.9762 vs 0.9761`). | Restrict the "third digit" claim to the binomial replay check; describe Cont–Kukanov as "agree to ~2–3 significant figures / within Monte-Carlo sampling error". |
| `index.md:109` | **Misattribution (COHERENCE, low).** "measured here, the naive rule booked **800** shares where FIFO fills **234** ($3.4×$ overbooking)". The hub's own §3 engine never computes this (its FIFO fractions are for `x=0..1000`, not the `11 500`-share queue); the 800-vs-234 pair comes from `05`'s F1 (`05:117`), and `02:115`'s average FIFO fill ratio is the related `0.2908` (`→ 232.6` shares). | Say "measured on `05` (`≈800` vs `234`)" or point §4 items at the page that actually runs them. |

**Non-issues checked and dismissed (not defects):**

- `index.md:47` `[[.../index\|Market Impact & Depth]]` — the `\|` is required escaping for a pipe inside a markdown table, and is the repo-wide convention (`content/index.md`, `content/diagnostics.md`). Link resolves. ✔
- `index.md:37` optimistic `1.0000` vs FIFO `0.3686` — matches `02` §3 exactly. ✔
- `index.md:39` `Q=1000,L=1000,m=3000 ⇒ 609.34` (MC `609.51`) — matches block 0 output. ✔
- `index.md:40` `x=0⇒0.9762`, `x=1000⇒0.2238` — matches the binomial fractions. ✔
- `index.md:42` pick-off `0.05 ms → 0.0488`, `10 ms → 1.0000` — matches `05` F2. ✔
- `index.md:45` temp. impact `ηX²/T`: `$25 000 → $1 250` — matches `05` F4 (1 d vs 20 d). ✔
- `index.md:46` ln–ln exponent `0.4922`, `R²=0.9401` — matches `06` block output. ✔
- `index.md:48` replay `1.0000` vs MC `0.6384`, CI `[0.6259, 0.6509]` — matches `04`. ✔
- `index.md:49` SE `0.0451` (N=100) / `0.001426` (N=1e5) — matches `04`. ✔
- `01:39–44` `g_exec = α_H − s − 2h`, and the three-regime SR table (`0.224`, `−0.222`, `0.570`) — recomputed from block 1: `0.06−0.02−0.02=0.02 → 0.02/0.0894=0.224`; `0.06−0.04−0.04=−0.02 → −0.222`; `0.06−0.005−0.004=0.051 → 0.570`. ✔
- `02:41–45` first-principles bias-direction table (`any print`↑, `trades-only`↑, `ignore cancels`↓, `look-ahead`↑, `mid fill`↑) — directions all correct, and the code's `1.0000 / 1.0000 / 0.3686 / 1.0000` confirms the "↑" cases. ✔
- `02:55–57` slippage `slip = (p−π₀) − (m_T−π₀) = p − m_T`; a mid fill with no impact ⇒ `m_t − m_T`. Algebra correct. ✔
- `02:120` `$16.00 → $1.86`, "8.6×" — code gives `16.000` and `1.861` (8.6×). ✔
- `03:35` boxed `Filled(x,L,ξ) = (ξ−x)⁺ − (ξ−x−L)⁺` — correct FIFO fill function, and reproduced by the replay engine. ✔
- `03:51–52` `𝔼[(ξ−Q)⁺]=m e^{−Q/m}`, `𝔼[filled]=m(e^{−Q/m}−e^{−(Q+L)/m})` — correct for `ξ~Exp(mean m)`. ✔
- `03:60` trade-through `(∃ trade at p<b) ⇒ fill w.p. 1` — correct price-priority sweep argument. ✔
- `03:70` `edge = ½s − AS − (fees+impact)`. ✔
- `04:36–39,55` MC estimator / `SE=σ/√N` / `N=(σ/ε)²` — correct. ✔
- `04:120` "mis-sized by ~56%" — `1/0.6384−1 = 56.6%`. ✔
- `05:55` `C_temp = ηΣn_k² → ηX²/T`, and "20× more impact if compressed 1 d vs 20 d" — correct. ✔
- `05:57` prose warning "toward more fills, earlier, at better prices" — consistent with all five signposts. ✔
- `06:34–35` Roll signature `γ₀=2c²+σ_u²`, `γ₁=−c²`, `γ_k=0 (k≥2)` — code recovers `c_hat=0.0172` from built-in `0.017`; `g₀=0.003054 ≈ 2c²+σ_u²=0.003078`. ✔
- `06:43` `ΔP≈Yσ(Q/V)^α`, `α≈0.5–0.6` — code recovers `0.4922`. ✔
- `06:51` concave intensities `λ(q)↑, λ″<0` — code's `log(1+q)/log 2` is increasing and concave (`1.000→8.969`). ✔
- Prerequisite coherence: hub `index:11` states folder-level prereqs for `02`–`06` with `01` declaring its own smaller set — matches each page's header (`01`→Market Microstructure; `02`→`01`; `03`→`02`+Queue-03; `04`→`03`+Numerical Methods; `05`→`04`+Low-Latency; `06`→`05`+Queue-06). ✔

---

## Code verification (8/8 blocks, all exit 0, all diff clean)

| block | description | result |
| :--- | :--- | :--- |
| `index.md` | Cont–Kukanov closed form vs MC; binomial FIFO fraction; optimistic-vs-conservative | ✔ exact (850.41/848.49, 609.34/609.51, 312.85/316.49; 0.9762/0.7728/0.4024/0.2238) |
| `01` | same alpha, signal-BT vs exec-BT across three cost regimes | ✔ exact (SR 0.671 vs 0.224 / −0.222 / 0.570) |
| `02` | five fill rules on a simulated level; per-order edge | ✔ exact (1.0000/1.0000/0.3686/1.0000; fill ratio 0.2908; $16.000 vs $1.861, 8.6×) |
| `03` (A) | LOB replay simulator vs binomial closed form, x=0..1200 | ✔ exact (0.9761/0.7715/0.4039/0.2237/0.0938) |
| `03` (B) | Cont–Kukanov + optimistic/conservative + trade-through | ✔ exact (incl. 0.2451/0.0837/0.0107) |
| `04` | one replay day vs MC distribution + counterfactual sweep | ✔ exact (replay 1.0000; MC 0.6384 sd 0.4511; SE 0.045109…0.001426; 0.9822/0.6291/0.1508) |
| `05` | four failures: optimistic fills, latency, look-ahead, self-impact | ✔ exact (800 vs 234 ×3.4; 0.0488→1.0000; 0.3301→1.0000; $25 000/$5 000/$1 250) |
| `06` | three stylized-fact validations (Roll, √-impact, concave intensity) | ✔ exact (c_hat 0.0172; exponent 0.4922, R² 0.9401 vs 0.8491; λ 1.000→8.969) |

---

## Summary

- **Code:** 8/8 blocks reproduce byte-for-byte — no implementation errors.
- **Spelling/links:** clean.
- **Math defects:** 1 false identity (`01:50`), 2 wrong σ-units (`04:113`,`04:120`), 1 mislabelled
  horizon (`04:119`), 1 unverifiable "verified" value (`index:38`), 1 cross-page unit clash
  (`02:49`/`03:42`/`index:38`), plus 2 lower-severity prose/attribution overstatements
  (`index:101`/`03:166`, `index:109`).
- **Overall:** fixes are local and mechanical; nothing in the fill/queue/impact core is wrong.

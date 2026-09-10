# Audit — `pillars/01-quantitative-research/regime-detection/`

**Scope:** 7 files (index.md + 01–06). Solo, adversarial review. Not counting `content/_legacy/`.
**Area:** Markov-switching (Hamilton), SETAR/STAR, HMM (forward–backward/Viterbi/Baum–Welch), regime allocation.
**Verified sources used:** `corpus/verified/tsay_ch4-6.md`, `tsay_ch10-12.md` (no `tsay_ch7-9.md` regime content beyond the S&P basis ECM cross-checked via tsay_ch4-6 §8 ref).

---

## 1. Spelling / typo (prose only, code/LaTeX excluded)

| file:line | Issue | Fix |
|---|---|---|
| `05-failure-modes-and-practice.md:18` | **"estiomable"** — not a word | → "estimable" |

Spellcheck pass (`pyspellchecker`, en_US, fences/LaTeX/wikilinks stripped) returned **one genuine typo** above; all other flagged tokens are technical terms, names or proper nouns (arma, overfit, kalman, teräsvirta split, vol(s), stdlib, economical) — no additional errors.

## 2. Math — formulas & worked examples (boxed/inline)

### 2.1 Verified correct (checked by independent recomputation)
| Where | Claim | Result |
|---|---|---|
| index:33, 02:33 | 2-state transition matrix, rows sum 1; stationary `π0=(1−P11)/(2−P00−P11)` | ✓ (gives π_recession=0.2796) |
| index:34 | `π_exp = 0.720` under Hamilton p=0.9049, q=0.7550 | ✓ 0.7204 |
| index:35 / 02:33 | E[stay in i]=1/(1−Pii); expansion 10.52, recession 4.08 qtr (paper 10.5/4.1) | ✓ 1/0.0951=10.52, 1/0.245=4.08 |
| index:36–38 / 02:43–45 | Hamilton filter predict/update; Gaussian conditional density | ✓ structure matches Hamilton §4.2 |
| index:39 / 02:37 | Sample log-likelihood = Σ ln Σ_j f(·)P[s_t=j|y_{1:t−1}] | ✓ |
| index:40–41 / 04:56–59 | α/β/γ recursions and Viterbi `δ_t(j)=f(y_t|j)max_i[δ_{t−1}(i)P_ij]` | ✓ (Viterbi/backtrace; index table omits γ normalization — *minor*: should read ∝, see 04:50 which is correct) |
| index:42 / 03:22 | SETAR(2;d) form `x_t=φ0^(j)+Σφi^(j)x_{t−i}+a_t^(j)` if `γ_{j−1}≤x_{t−d}<γ_j` | ✓ Tsay Eq. 4.9 |
| index:43 / 03:26 | STAR (logistic) form, F=1/(1+e^−z), mid at ℓ | ✓ Tsay Eq. 4.15 |
| 03:36 | TAR(1) ergodicity `φ1^(1)<1, φ1^(2)<1, φ1^(1)·φ1^(2)<1` | ✓ **verbatim in** `tsay_ch4-6.md:17` |
| 02:57 | Markov-switching GNP contraction ≈3.7qtr, expansion ≈11.3qtr (MCMC/Gibbs) | ✓ `tsay_ch4-6.md:22` (3.69 / 11.31) |
| 02:51–55, 04:61–64 | EM E/M steps; μ,σ updates | ✓ §4 corrected forms identical; **02:55 transition update** `P_ij∝Σ_t γ_t(i)P_ij f(y_{t+1}|j)` is a loose/self-referential restatement of the ξ_t responsibility (04:64 gives the clean `P_ij=Σξ_t/Σγ_t`) — *minor imprecision only; the executed code implements the correct Baum–Welch form.* |
| 05:37 / 05 Exp2 | BIC = −2ln L̂ + K ln T | ✓ recomputed: 2-state −2580.1, 3-state −2543.5, Δloglik +0.925 |
| 05 Exp1 | Label-switching | ✓ both runs → 1309.234, permuted means (0.0108/−0.0133) |
| 06:28 | Mixture variance Var(y)=π1σ1²+π2σ2²+π1π2(μ1−μ2)² | ✓ correct composition variance |

### 2.2 ✗ **Error — index.md hub formula engine (stationary prior fed into Hamilton filter with swapped state labels)**
- Formula (index:34) and code (index:62–63, 76–78) assign the label π0 inconsistently.
  - Lookup table (index:34): `π0=(1−P_11)/(2−P_00−P_11)` = **state-0 (recession) stationary prob = 0.2796**.
  - Code (index:62): `pi0=(1−q)/(2−p−q)` = **0.7204** — this is π_expansion, not π0-as-labeled.
- The filter is then initialised `[pi0, pi1] = [0.7204, 0.2796]` into slots [state0, state1] where state0 = **recession** (μ[0]=−0.004; output maps pr[0]→"P(recession)"). So the prior is fed **swapped**: P(recession)=0.72, P(expansion)=0.28, the reverse of the true stationary (0.28 / 0.72).
- **Effect (recomputed):** documented output `t=1 P(recession)=0.5725` is an artifact of the swapped prior. With the correct prior, t=1 gives P(recession)=0.2813 and P(expansion)=0.7187 — the filter is **expansion-leaning throughout on this 3-point sample**, so the page's pedagogical line (index:90, "the filter shifts from recession-leaning to expansion-leaning") is itself an artifact of the mis-set initial distribution.
- **Fix:** initialise with `[1−pi0, pi0]` i.e. [P(recession),P(expansion)] = [0.2796, 0.7204] and reconcile variable naming with the lookup-table convention (or relabel the table).
- Severity: **moderate** — the printed numbers do reflect the code that ships (no doctoring), but the worked example mis-uses the stationary distribution and its narrative conclusion is wrong on the displayed data.

## 3. Code — every block executed (stdlib only), diff vs documented output fence

| File & block | Runs (exit 0) | Stdout == documented fence |
|---|---|---|
| index.md §3 (Hamilton durations + 2-state filter) | ✓ | ✓ (only trailing-newline diff) |
| 01-from-zero-intuition.md §3 (planted-regime filter, 87.5%) | ✓ | ✓ |
| 02-markov-switching-models.md §3 (Hamilton filter + EM end-to-end) | ✓ | ✓ |
| 03-threshold-models.md §3 Part 1 (SETAR grid search, γ=0.000) | ✓ | ✓ |
| 03-threshold-models.md §3 Part 2 (STAR, c=0.00, SSE 5.863, 1.035×) | ✓ | ✓ |
| 04-hmm.md §3 (forward-backward 88.6% + Viterbi 77.8%) | ✓ | ✓ |
| 05-failure-modes-and-practice.md Exp 1 (label switching) | ✓ | ✓ |
| 05-failure-modes-and-practice.md Exp 2 (overfitting/BIC) | ✓ | ✓ |
| 06-advanced-extensions.md §3 (static vs regime-tactical 60/40) | ✓ | ✓ |

**9/9 blocks run clean (exit 0) and match the documented output fences exactly** (fixed `random.seed` → deterministic). All "Stdlib only" claims are true.

- ✗ **04-hmm.md:108** — a dead/buggy first line of the Viterbi `delt` init (`mu[0]` written as a literal `0`, inconsistent with state-1 handling) is immediately overwritten by line 109, so output is unaffected, but the dead line is incorrect code that should be deleted. (Code quality — minor.)

## 4. Coherence
- **Links:** 21 unique wikilinks, **all resolve** (15 direct `.md`, 6 via `/index.md`). No broken links.
- **Hub vs 01 prereq:** index:11 correctly notes 01 states its own smaller entry requirements, and 01 does list its own (P&MT Bayes + Econometrics stationarity). Minor tension: hub line 122 says 01 = "no prior knowledge needed" while 01 actually lists two prereqs — soft overstatement, not a hard error.
- **Cross-page numeric consistency:** index §4 `loglik 1309.234` (label-switch) and `BIC −2580 vs −2543`, `Δ+0.925` (overfit) exactly match 05 Exp 1/2 outputs; index §2 "filter 889.5 / EM →891.195" match 02 (889.549 / 891.195); smoothed 88.6% & Viterbi 77.8% consistent index↔04; SETAR threshold "0.000" & STAR c "≈0" consistent index↔03. The "verified check" column is trustworthy throughout. ✓
- **Jargon:** SETAR/STAR, HMM, E-step/M-step, forward–backward, Viterbi, Baum–Welch, BIC, MAP, filtered vs smoothed vs decoded, label switching all defined on/near first use. No undefined terms.
- ✗ **01-from-zero-intuition.md:24** — prose says "if it's bull today, there's a **4%** chance of bear tomorrow", but the same page's model (01:63) has P[0][1]=0.05 (**5%**); page 02 uses 5% too. The 4% only matches 06's separate example (P[0][1]=0.04). Fix to 5% for internal consistency. (Minor — coherence.)
- ⚠ **01:51** "versus NBER postwar averages of 4.7 and 14.3 [quarters]" — specific external statistic, **not** verifiable from the verified corpus and not standard textbook NBER postwar figures (recessions ≈4 qtr, expansions ≫14 qtr). Recommend adding a source or re-checking against Hamilton (1989) / NBER. (Unverified claim — advise citation, not flagged as definitively wrong.)

## 5. Summary

**7 files, 9 code blocks. Quality is high:** all math cross-checked against `tsay_ch4-6.md`/`tsay_ch10-12.md` and Hamilton; 9/9 code blocks reproduced exactly; all links resolve; verified corpus claims accurate; internal numeric "verified check" column is consistent across all pages.

**Errors found (4):**
1. `05:18` — typo "estiomable" → "estimable" (spelling).
2. `index.md:34/62–78` — stationary distribution fed into Hamilton filter with **swapped state labels**, making the §3 worked example's prior (and its "recession→expansion shift" narrative) an artifact of the bug (math/coherence, moderate).
3. `01:24` — "4% chance of bear" inconsistent with the page's own 5% transition (coherence, minor).
4. `04:108` — dead, incorrect Viterbi init line; delete (code quality, minor).

**Warnings (non-blocking):** 01:51 NBER "4.7 / 14.3 qtr" statistic needs a source; index:122 "no prior knowledge" vs 01's listed prereqs; index:40 γ_t table omits normalization (∝); 02:55 transition-M-step formula loose (correct in 04).
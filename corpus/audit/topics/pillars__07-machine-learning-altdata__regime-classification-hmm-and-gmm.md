# Audit — `content/pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/`

**Scope:** 7 files (index + 01–06). Adversarial pass: prose spelling, every boxed formula + worked
example, every ```python block executed and diffed against its documented output fence, hub↔sub-page
coherence, link resolution. `content/_legacy/` ignored.

**Verdict:** **PASS WITH MINOR ISSUES** — all math is correct, all code reproduces byte-for-byte,
all links resolve; two numeric prose claims are imprecise (one genuinely wrong).

**Counts:** files_checked = 7 · blocks_run = 9 · errors_found = 2.

---

## 1. Code execution (9/9 blocks ran, 9/9 stdout == documented fence)

Every ```python block was extracted, **chained in file order within one namespace** (required for
`05-failure-modes-and-practice.md`, whose 3 blocks share `sim`/`gauss`/`em_gmm`/`r`/`st`), executed
with stdlib `python3`, and diffed line-for-line against the page's output fence.

| File | blocks | result |
|---|---|---|
| index.md | 1 | MATCH (`final LL = 15.53`) |
| 01-from-zero-intuition.md | 1 | MATCH (`…agreement vs truth = 78.1%`) |
| 02-unsupervised-clustering-gmm.md | 1 | MATCH (LL `1740.73→2968.43`) |
| 03-the-em-algorithm.md | 1 | MATCH (2-D EM `-1078.90→-902.49`) |
| 04-hmm-regimes.md | 1 | MATCH (Viterbi `95.8%`) |
| 05-failure-modes-and-practice.md | 3 (chained) | MATCH (label-switch `2376.866`; BIC; look-ahead `+40.0`) |
| 06-advanced-extensions.md | 1 | MATCH (OOS agreement, MSE table) |

The Experiment 1→2→3 dependency note on `05` (§3 line 47) is accurate: Experiments 2 and 3 do reuse
Experiment 1's namespace and would raise `NameError` standalone. No hidden dependency beyond that.

## 2. Math — boxed formulas

Re-derived every displayed formula. **All correct:**

- **GMM (index §2, 02 §2, 03 §2).** Mixture density, responsibility/Bayes, `N_k=Σγ`, M-step
  `π=N_k/N`, `μ=Σγx/N_k`, `Σ=Σγ(x-μ)(x-μ)ᵀ/N_k` — correct, including the `1/N_k` (not `1/N`)
  normalisation.
- **HMM forward–backward (index §2, 04 §2).** `α₁(j)=π_j𝒩(y₁)`, `α_t(j)=𝒩(y_t)Σ_i α_{t-1}(i)A_ij`,
  `β_T(i)=1`, `β_t(i)=Σ_j A_ij𝒩(y_{t+1})β_{t+1}(j)`, `γ=αβ/Σαβ`, and the `ξ_t(i,j)` two-time
  posterior — all standard and correctly indexed.
- **Baum–Welch M-step.** `π_i=γ₁(i)`, `A_ij=Σ_{t<T}ξ/Σ_{t<T}γ`, Gaussian `μ`,`σ²` re-estimation —
  correct.
- **Viterbi (04 §2).** `δ₁(j)=logπ_j+log𝒩(y₁)`, `δ_t(j)=log𝒩(y_t)+max_i[δ_{t-1}(i)+logA_ij]` with
  back-pointer traceback — correct log-domain recursion.
- **EM / ELBO (03 §2).** Jensen lower bound `ℓ(θ)=log E_q[p(x,z|θ)/q(z)] ≥ E_q[log p(x,z|θ)] −
  E_q[log q(z)]`, the `Q(θ;θ^old)` definition, and the monotonicity chain
  `ℓ(θ^new) ≥ L(q,θ^new) ≥ L(q,θ^old) = ℓ(θ^old)` — correct (log-concavity gives log E[X] ≥ E[log X],
  and it is `p(x)` that the expectation collapses to).
- **BIC (05 §2).** `BIC = −2ℓ_max + m·log T` with `m = 3K−1` for a 1-D GMM (`K−1` weights + `K`
  means + `K` variances) — correct; recomputed numerically against the run: K=1→−4484.31,
  K=2→−4720.32, K=3→−4702.96, K=4→−4683.31, matching the page.
- **Permutation invariance of the mixture likelihood** (label switching) — correctly stated.
- **Supervised / mixture-of-experts (06 §2).** Logistic `σ(wᵀx)`, hard conditional indicator
  predictor, and soft `Σ_k P(z=k|x) f_k(x)` — all correct.

## 3. Errors found

### E1 — [02-unsupervised-clustering-gmm.md:106] wrong constant in prose (moderate)
- **Stated:** "recovers both regime volatilities to within $1.5\%$ of the truth ($0.00794$ vs $0.008$,
  $0.02686$ vs $0.028$)".
- **Correct:** low-vol relative error = `|0.00794−0.008|/0.008 = 0.75%`; high-vol relative error =
  `|0.02686−0.028|/0.028 = 4.07%`. The larger error is **~4.1%**, so "within 1.5%" is false for the
  high-vol component. Suggested fix: "within **~4%** of the truth (0.75% low-vol, 4.1% high-vol)",
  or drop the percentage and say "to within a few percent".

### E2 — [01-from-zero-intuition.md:17] imprecise constant in prose (minor)
- **Stated:** panic "…where volatility is $3\times$ higher."
- **Correct:** the folder's canonical sim (used verbatim in 01/02: `sig=[0.008,0.028]`) has a vol
  ratio of `0.028/0.008 = 3.5×`. Low-severity: `3×` reads as loose rounding; tighten to `3.5×` (or
  "more than 3×") for exactness.

*No other numeric, sign, or indexing discrepancy was found across the boxed formulas, the §2
derivations, or any worked-example claim in prose.*

## 4. Spelling / typos (prose only; code & LaTeX excluded)

Tokenised all prose (frontmatter, code fences, inline code, `$…$`/`$$…$$`, wikilinks stripped) and
run every distinct token against a system wordlist with stem-aware leniency. **No spelling errors**:
the 196 out-of-dictionary tokens are all domain terms, hyphenated compounds, or proper nouns
(Baum–Welch, Viterbi, Rabiner, Dempster, JRSS-B, mixure-of-experts terms, z-vol, etc.). No typos.

## 5. Coherence

- **Hub ↔ 01 prereq:** index §Basic-Prerequisites explicitly says page `01` "states its own, smaller,
  entry requirements"; 01 says "None beyond basic statistics". **Consistent.**
- **Jargon first-use:** Notation block on the hub fixes $x_t, z_t, π_k, μ_k, Σ_k, A_{ij}, γ_t(k),
  N_k$ before reuse. "responsibility" defined at 01 §2 and reused; "ELBO" defined on first use at
  03 §2; "filtered/smoothed" defined at 04 §1. **Consistent.**
- **Links:** all **23 distinct `[[…]]` targets resolve** (file or `index.md` hub) — 0 broken.
- **Cross-page numbers:** the shared simulated-series parameters (`A`, `μ`, `σ`) are consistent
  across 01/02/04 and reused identically in 05's look-ahead experiment. The label-switching LL
  `2376.866`, BIC values, `+40 pt` gap, and `−8.8% / +5.5%` figures agree across hub, sub-pages, and
  the actual runs.
- **Contradictions:** none found. No AIC anywhere (the pages use BIC only) — not an error, just note
  the task's "BIC/AIC" was BIC-only here.

## 6. Recommendation

Ship. Optionally patch the two prose constants (E1 first — it is the only materially wrong claim).

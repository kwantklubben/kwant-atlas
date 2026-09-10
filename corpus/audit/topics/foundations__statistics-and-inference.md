# Audit: `content/foundations/statistics-and-inference/`

**Sole reviewer, adversarial pass.** Folder = 7 files (index hub + 6 sub-pages). Scope: spelling/typos in prose, math (every boxed formula + worked example, cross-checked vs standard theory and `corpus/verified/`), code (every ```python block executed and diffed), coherence (hub↔01 prereqs, jargon, links, contradictions). Ignored `_legacy/`.

**Verdict: PASS with 2 minor issues.** No content or mathematical errors found. All 7 python blocks run cleanly under Python 3 and reproduce their documented output **exactly** (every block is seeded, so output is deterministic and byte-matchable). All boxed formulas and worked examples check out. No spelling/typo errors in prose. The two findings are coherence nits, not factual errors.

---

## 1. Code verification (7/7 blocks run, all pass)

Blocks extracted from each file and executed; output diffed against the documented ```` ``` ```` output blocks.

| File | Block | Result | Diff vs documented |
|---|---|---|---|
| index.md | §3 MSE/CRLB/CLT | Ran clean (seed 11) | **Exact match** |
| 01-from-zero-intuition.md | §3 sampling dist (seed 7) | Ran clean | **Exact match** |
| 02-point-estimation.md | §3 Gamma-MLE/Newton (seed 11) | Ran clean | **Exact match** |
| 03-the-clt-and-sampling.md | §3 SE/χ²/t/Berry–Esseen (seed 19) | Ran clean | **Exact match** |
| 04-confidence-intervals-and-testing.md | §3 t-CI/LRT/multiplicity (seed 23) | Ran clean | **Exact match** |
| 05-bias-variance-and-validation.md | §3 bias–var/CV/AIC–BIC (seed 29) | Ran clean | **Exact match** |
| 06-advanced-extensions.md | §3 bootstrap/.632/best-of-N (seed 31) | Ran clean | **Exact match** |

Every documented output line reproduced bit-for-bit (including the two Monte-Carlo blocks, index.md and 01, which are nonetheless seeded let either run cleanly and deterministically — no unseeded agreement judgement needed).

## 2. Math verification

All boxed formulas and worked examples re-derived; all correct.

- **index.md:** MSE decomposition `E(W−θ)²=Var W+(Bias W)²`; CRLB = `[τ'(θ)]²/nE[(∂log f/∂θ)²]`; observed-info variance `[h'(θ)]²/(−ℓ''(θ̂|x))`; delta method univariate + multivariate; `(n−1)S²/σ² ~ χ²_{n−1}` (mean=n−1=11, Var=2(n−1)=22 ✓); student-t P(|t|>1.96)=0.1217@n=5 ✓; t-CI coverage Normal 0.9504 / Exp 0.9123 ✓; Wilks λ-stat mean 0.9941, 95th pct 3.861 ✓; 20-null FWER 0.647 (theory 0.642) ✓; exp-rate MLE Var 0.03172 ≈ CRLB λ²/n=0.03125 ✓; odds-ratio Var 0.00177 ≈ p/[n(1−p)³]=0.00175 ✓. **All replicate the §3/§02/§03/§04 runs; no errors.**
- **02:** MSE(σ̂²_MLE)=(2n−1)σ⁴/n² < MSE(S²)=2σ⁴/(n−1) — verified algebra (n=10: 0.19 vs 0.2222 σ⁴) and simulation (3.043 vs 3.553). Gamma α̂/B̂ recovered; β̂=α̂/x̄ correct.
- **03:** LLN, CLT, SE=σ_f/√n, Berry–Esseen factor, exact distributions all correct. Rate claim (0.133→0.037 as n goes 1→16, ≈3.6× for 4× n) verified ≈√4=2×? — actual: 0.1333→0.0372 is ≈3.6×, consistent with the √(1/16)−0.25 exponent; prose's "factor ≈3.6 for factor-4 increase" is correct (√4 = 2 would be exact only asymptotically; the observed 3.6 matches printed values).
- **04:** Neyman–Pearson, Karlin–Rubin, LRT/Wilks, FWER bound `≤1−(1−α)^m`, BH step-up `p_(k)≤(k/m)q`, best-of-N `E[max]≈√(2ln N)`. t-cutoff used (2.1448 = t_{14,0.975}, n=15) correct. All correct.
- **05:** bias–variance 3-term decomposition, optimism `2d/n·σ²_ε`, `df=tr(S)`, K-fold CV formula, AIC/BIC. `tr(S)≤p` claim correct. Screening 3%-vs-50% (ESL §7.10.2) claim consistent across index/04/05.
- **06:** bootstrap SE, percentile interval, .632 = 0.368·err + 0.632·OOB, omit-fraction 1−1/e≈0.368, `E[max t_j]≈√(2ln N)`. Panel (D) numbers self-consistent with `√(2lnN)`: N=1000 → E[max]=3.24 (theory 3.72 incl. second-order term) ✓.

No mathematical error found in any boxed formula, derived quantity, or worked example across all 7 files.

## 3. Spelling & prose

Full-prose vocabulary audit (all prose, LaTeX/code stripped): zero misspelled/typo'd words. Grammar and register consistent. Style is consistent British hyphenation (penalised, normalises, maximisation) with minor US forms — not an error.

## 4. Coherence

- **Hub↔01 prereqs:** consistent. Hub states 02–06 need probability + calculus; page 01 explicitly declares its own smaller entry bar (elementary algebra, no probability), matches the hub's parenthetical. No contradiction.
- **Jargon:** consistent C&B-cited terminology; Cramér–Rao, Neyman–Pearson, Karlin–Rubin, Benjamini–Hochberg, Berry–Esseen all spelled/used correctly.
- **Cross-page numbers agree:** MSE-MLE beats-S², t-interval under-coverage 0.912/91%, best-of-20 ≈65%, screening 3%-vs-50%, `√(2ln N)` threshold all stated identically wherever repeated.
- **Wikilinks:** all in-folder, base, sibling, and forward links resolve (checked all 14 targets exist). One style/coherence exception → **FINDING 2** below.

---

## Findings (2, both minor, no factual errors)

**F1 — index.md line 39 (MSE row "Verified check") disagrees with the on-page §3 script.**
Stated: `MSE(S²)=3.579 vs MSE(σ̂²_MLE)=3.055, n=10`. The same page's §3 script (index.md lines 106–107, deterministic seed 11) prints `MSE(S²)=3.5459`, `MSE(σ̂²_MLE)=3.0366`. Line 31 claims all §2 numbers "were re-executed and reproduced exactly by the scripts in §3", but these two figures match neither the §3 output (3.5459/3.0366) nor the 02 sub-page (3.5526/3.0429). All four are the same 40k-sample Monte-Carlo quantity within noise of theory (3.5556/3.0400), so nothing substantive is wrong — but the recorded "verified check" numbers are stale relative to the repo's own reproduceable scripts. **Fix: update the table to 3.546 / 3.037 (or note the replicate).**

**F2 — index.md line 141: `[[foundations/numerical-methods|Numerical Methods]]` omits `/index`.**
Every other folder-level link in this hub (same line: econometrics, ergodicity) uses the `/index` suffix, and the sibling ergodicity hub links it as `[[foundations/numerical-methods/index|Numerical Methods]]`. The bare-folder form is the only sibling link in the graph that omits `/index` and is likely non-resolving in Quartz. **Fix: `[[foundations/numerical-methods/index|Numerical Methods]]`.**

All other "Verified check" cells in the index table reproduce exactly from the on-page scripts.

---

## Files checked
1. `index.md`
2. `01-from-zero-intuition.md`
3. `02-point-estimation.md`
4. `03-the-clt-and-sampling.md`
5. `04-confidence-intervals-and-testing.md`
6. `05-bias-variance-and-validation.md`
7. `06-advanced-extensions.md`
# Audit — `content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/`

**Reviewer:** sole adversarial reviewer (subagent)
**Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). `content/_legacy/` ignored.
**Method:** every boxed formula and worked example re-derived/executed; all 7 ```python blocks run and stdout diffed against the output fences; all wikilinks path-checked; prose spell-checked (hunspell en_US, British-spelling house style accounted for).

**Verdict: PASS WITH MINOR ISSUES.** 2 substantive issues (one wrong formula, one claim that contradicts the page's own code output) plus 6 minor/formatting items. No numeric block failed to reproduce.

---

## (3) CODE — blocks actually run

**7 python blocks run** — one per file. All seven exit 0 and reproduce. Two fences (04, 05) differ from live stdout by a single space of column padding (whitespace only; every numeric token matches after whitespace-normalisation).

| File | Block | Reproduces? |
|---|---|---|
| index.md | sizing engine (f*, c(2−c), S²/2+r) | ✅ exact |
| 01-from-zero-intuition.md | growth landscape + 40k-path sim | ✅ exact |
| 02-the-kelly-formula.md | 3 formulas + f_c bisection | ✅ exact |
| 03-growth-and-optimality.md | c(2−c) law + full/half sim | ✅ exact |
| 04-fractional-kelly-and-ruin.md | half/full/double sim | ⚠️ numeric ✅, fence whitespace off by 1 space |
| 05-failure-modes-and-practice.md | estimation-error + fat-tail | ⚠️ numeric ✅, fence whitespace off by 1 space |
| 06-advanced-extensions.md | multi-asset Kelly / tangency | ✅ exact |

---

## (2) MATH — findings

### E1 — WRONG FORMULA (substantive)
**`03-growth-and-optimality.md:44`**
Stated: `$$g_\infty(cf^*)=\frac{m^2}{s^2}c\left(1-\tfrac c2\right)$$`
Correct: `$$g_\infty(cf^*)=r+\frac{(m-r)^2}{s^2}c\left(1-\tfrac c2\right)$$`

Two defects: the drift term uses `m²` instead of `(m−r)²`, and the additive riskless rate `r` is dropped. Because `f*=(m−r)/s²`, expanding `r+(cf*)(m−r)−½s²(cf*)²` gives `r+(m−r)²/s²·c(1−c/2)`. With the page's own worked numbers (m=0.11, s=0.15, r=0.06) at c=0.5 the stated formula yields **0.201667** vs the actual **0.101667** (2× off) — confirmed numerically and against the page's own fence (`g_inf=+0.101667`). The formula also silently assumes the ratio `c(2−c)` is exact, which holds only when r=0.

### E2 — CLAIM CONTRADICTS THE PAGE'S OWN OUTPUT (substantive)
**`06-advanced-extensions.md:93`**
Stated: "the coupled optimum shifts weight — less into asset 0 ($0.92$), **more into asset 1 ($1.10$)**".
Computed from the block's own inputs (μ=[0.10,0.16], Σ=[[0.04,0.012],[0.012,0.09]], rf=0.05): isolated assets give (1.2500, 1.2222); the coupled optimum is (0.9201, 1.0995). Both weights **decrease** — asset 1 goes 1.2222 → 1.0995. The text should read "**less** into asset 1 (1.10)". The printed table one line above (`isolated 1.2222 vs coupled 1.0995`) directly refutes the "more" claim.

### E3 — IMPRECISE FORMULA (minor, 3 occurrences)
`index.md:82`, `05-failure-modes-and-practice.md:23`, `05-failure-modes-and-practice.md:45`:
Stated: `$g\approx\mu-\tfrac12\sigma^2f^2$`. The linear term is missing its `f` multiplier; the continuous growth rate is `g(f)=r+f(m-r)-\tfrac12 s^2f^2` (elsewhere the folder writes it correctly). Correct shorthand: `g\approx f\mu-\tfrac12\sigma^2f^2` (or `f(m-r)-\tfrac12\sigma^2f^2`).

### Verified-correct (no action)
Discrete `f*=p−q`, `f*=m/(ab)` with `m=bp−aq`, `g(f)=p ln(1+bf)+q ln(1−af)`, `f_c(p=0.55)=0.198668`; continuous `f*=(m−r)/s²=2.2222`, `g_∞(f*)=S²/2+r=0.115556`, `f_c=5.4272` (upper root), `c(2−c)` law (r=0), multi-asset `w*=Σ⁻¹(μ−rf1)`, `g∞(w*)=½·SR²max+rf=0.133478`, tangency normalisation, `ρ=0.2`, `f_hat/f_true=3.5×`, estimation-error numbers (`g(0.14)=−0.00426`), fat-tail `μ/σ²=0.7663` vs exact `0.581`, all 5 hub quick-reference rows, and the full prereq chain (01→02→03→04→05→06). All reproduce.

---

## (1) SPELLING / TYPOS
hunspell (en_US) surfaced only proper nouns, acronyms and British `-ise/-isation` forms (house style). One genuine typo:

### E5 — typo
**`index.md:83`** — "assumes even-money, **win-or-lose-lose-all**" — doubled "lose". Likely "win-or-lose-all" (or "win-or-lose-it-all").

### E8 — terminology inconsistency (minor)
**`02-the-kelly-formula.md:108`** — "because **leverage drag** scales like f²". The quadratic `−½s²f²` term is called "volatility drag" everywhere else (index:17, 01:25, etc.). Probably should be "volatility drag".

---

## (4) COHERENCE — hub vs sub-pages, links, contradictions

### E4 — dangling simulation reference (minor)
**`05-failure-modes-and-practice.md:99`** — claims "(simulated in §4's text to double the ruin rate)". §4 is prose failure-modes only; there is **no** simulation there. The companion assertion at `05:45` ("the Gaussian bet nearly doubles the ruin probability") is likewise unsupported by any code in the folder. Either drop the cross-reference or add the simulation.

### E7 — `c(2−c)` caveat missing where it matters (minor)
`index.md:41` (quick-reference table) and `04-fractional-kelly-and-ruin.md:36` present `g_∞(cf*)/g_∞(f*)=c(2−c)` as a general identity. It is exact only for r=0 (equivalently for the excess-growth `g_∞−r`); `03:47,100` correctly notes that with r>0 half-Kelly keeps ~0.88 (not 0.75) in the folder's own continuous example. The caveat should be carried into the hub table and page 04.

### E6 — output-fence whitespace (formatting)
`04:78-80` and `05:93-94` output fences are mis-aligned with live stdout by one padding space (`mw:10.4f` / `mw:8.4f` rendering). Numeric content identical; re-pad to match.

### Links / structure — clean
- 25 distinct wikilink targets, **all resolve** to existing files.
- All sub-pages carry consistent frontmatter (`title`, `tags`) and the mandated 6-section layout.
- Hub prereq note ("pages 02–06 need Ergodicity + Calculus; 01 states its own smaller prereq") is consistent with page 01's actual prereq line.
- Hub signposts to failure-mode analysis match where the content actually lives (page 05).
- No contradictions found between hub quick-reference table and pages 02–06, except the c(2−c) caveat (E7).

---

## Summary

| Severity | Count | Items |
|---|---|---|
| Substantive | 2 | E1 (wrong growth formula, 03:44), E2 (contradicted weight claim, 06:93) |
| Minor | 6 | E3 (missing `f`, ×3), E4 (dangling ref), E5 (typo), E6 (fence whitespace), E7 (c(2−c) caveat), E8 (terminology) |
| **Total** | **8** | |

Code: 7/7 blocks run, 7/7 reproduce. Links: 25/25 resolve.

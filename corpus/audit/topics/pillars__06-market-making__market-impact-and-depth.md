# Audit — `content/pillars/06-market-making/market-impact-and-depth/`

**Date:** 2026-09-10 · **Reviewer:** sole deep-audit pass (adversarial)
**Scope:** 7 files — `index.md` + `01`..`06` (no `content/_legacy/`).
**Method:** every ```python block extracted and run standalone with `python3` and diffed against its
following output fence; every boxed/display formula and worked example re-derived by hand and
re-executed numerically; generalized-Roll / Kyle claims cross-checked against the verified corpus
(`corpus/verified/hasbrouck_ch6-10.md`, `hasbrouck_ch1-5.md`); all 17 wikilink targets resolved against
`content/**`; prose run through a wordlist diff (hunspell had no dictionary installed — `cracklib`
wordlist + manual pass used instead).

---

## Verdict

**PASS with corrections — 5 findings, all low-to-moderate severity.** No spelling/typos in prose.
All **7 Python blocks run cleanly and reproduce their documented output byte-for-byte** (7/7). Every
boxed formula is correct except one broken LaTeX fragment (`01:41`); one worked example has a **sign
convention error** (`03`); two **coherence** defects (contradictory statements about linear-model bias
in `04`, and an inverted exponent identity in `06`). The reported numeric outputs (Kyle λ=1.0000,
half-information residual 1.9982, square-root slopes 0.5054/0.5000, OFI slope ∝1/depth, Amihud) are all
reproduced exactly.

---

## Code execution (job #2) — 7/7 blocks match

| file | block | stdout vs fence |
| :--- | :--- | :--- |
| `index.md` | kyle_sim | **byte-for-byte match** |
| `01-from-zero-intuition.md` | linear_impact_path | **byte-for-byte match** |
| `02-the-kyle-model.md` | kyle_sim | **byte-for-byte match** |
| `03-temporary-vs-permanent-impact.md` | propagator | **byte-for-byte match** |
| `04-the-square-root-law.md` | book_impact | **byte-for-byte match** |
| `05-failure-modes-and-practice.md` | ofi_regression | **byte-for-byte match** |
| `06-advanced-extensions.md` | impact_path | **byte-for-byte match** |

**Blocks run: 7.** No exceptions, no warnings; every fence is an exact transcript.

---

## Issues

| file:line | problem | stated → correct |
| :--- | :--- | :--- |
| `01:41` | **Malformed LaTeX.** The depth formula has an *empty denominator*: `\frac{\text{signed order flow needed for a \$1 price move}}{}`. Renders as a fraction over a blank denominator. | Written: `\frac{1}{\lambda}= \frac{\text{signed order flow needed for a \$1 price move}}{}`. Correct: drop the trailing `\frac{...}{}` and write `\text{depth}=\dfrac{1}{\lambda}\;\text{is the signed order flow needed for a \$1 price move}`, or `= \frac{1}{\lambda}` with the words as prose. |
| `03:73`, `03:85`, `03:109` | **Sign-convention error in the worked example.** The example is "One **sell** of $X=-10^6$ shares" with "Permanent coefficient $\gamma=-2\times10^{-6}$/share". The code does `m += gamma_perm*q` with `q=X/n`, so $\gamma X = (-2\times10^{-6})(-10^6) = +2$: the price **rises** by \$2 on a *sell*. This contradicts the page's own §1 ("Sell a stock and watch the price settle 20bp **lower**"). Executed: final efficient price = 52.0, i.e. +2.0 from S₀=50 (price **up**). | A sell must give a negative permanent move. Correct: either make $X=+10^6$ (sell magnitude) with $\gamma=-2\times10^{-6}$ → $\gamma X=-2$ (price falls), **or** keep $X=-10^6$ signed and set $\gamma=+2\times10^{-6}$. Every number in the table (permanent 2.0000, peak 7.2106, VWAP 4.4105) then carries the correct (negative) sign. As written the magnitudes are right but the *direction is inverted*. |
| `03:109` | **Formula/label mismatch.** "Permanent impact is constant at 2.0000 … exactly the Almgren–Chriss prediction $\tfrac12\gamma X^2$." The code returns `gamma_perm * X` = \$2/share — that is the **per-share price impact** $\gamma X$, not the **total permanent cost** $\tfrac12\gamma X^2$. With $\gamma=-2\times10^{-6}$, $X=-10^6$: $\tfrac12\gamma X^2 = \tfrac12(-2\times10^{-6})(10^{12}) = -\$1{,}000{,}000$, not 2. | State the identity that actually holds: per-share permanent impact $=\gamma X=\$2$ (or, in total dollars, $\tfrac12\gamma X^2=-\$1\text{M}$). The sentence mixes the two objects. (The parallel statement in failure-mode 1, `03:117`, uses $\tfrac12\gamma X^2$ correctly for the *bookkeeping cost*.) |
| `04:32` **vs** `04:130` | **Self-contradiction on the direction of linear-model bias.** `04:32` (essence box): "a linear-impact assumption **understates** the cost of small orders and **overstates** it for large ones." `04:130` (failure mode 1): "linear models **understate** the cost of large orders (they treat impact as proportional)." The two cannot both hold. | `04:32` is the correct statement (a concave $\sqrt{Q}$ law lies below a linear chord fit at the sample's typical sizes, so the linear model **overstates** large orders and understates small ones). Fix `04:130` to read "…**overstate** the cost of large orders (they treat impact as proportional)". Note `01:113` ("A linear model underestimates (or a naive one overestimates) the cost of very large orders") also leans the wrong way and should be aligned to "overestimates for large orders". |
| `06:37` | **Inverted exponent identity, inconsistent with `04`.** `06:37` writes "matching the order-sign autocorrelation exponent $\gamma=(1-\beta)/2$ **of page 04**". But page 04 (`04:63`) and the hub (`index:60`) give $\beta=(1-\gamma)/2$ (the Bouchaud response-function relation). These are not algebraically equivalent ($\gamma=(1-\beta)/2 \Rightarrow \beta=1-2\gamma$, vs $\beta=(1-\gamma)/2$). | Correct `06:37` to match page 04: $\beta=(1-\gamma)/2$ (equivalently $\gamma=1-2\beta$), not $\gamma=(1-\beta)/2$. |

**Minor / cosmetic (not counted among the 5):** `06:37` wraps inline LaTeX in a code span
(`` `impact decays as a power law $G(\tau)\sim\tau^{-\gamma}$` ``), so the math will not render; drop the
backticks.

---

## Verified correct (spot-checks)

- **Kyle (1985) equilibrium** (`index:39–46`, `02:52–78`): $\beta=\sqrt{\sigma_u^2/\Sigma_0}$,
  $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$, depth $1/\lambda=2\sqrt{\sigma_u^2/\Sigma_0}$,
  $\mathrm{Var}[v\mid y]=\Sigma_0/2$, $\mathbb E[\pi\mid v]=\tfrac{(v-p_0)^2}{2}\sqrt{\sigma_u^2/\Sigma_0}$,
  $\mathbb E[\pi]=\tfrac12\sqrt{\sigma_u^2\Sigma_0}$ — all re-derived and all reproduced by the sim
  ($\lambda_{\text{OLS}}=0.9998$, residual $1.9982$, profit $0.9969$).
- **Generalized Roll** (`index:68`, `03:61`): $\Delta p_t=c(q_t-q_{t-1})+\lambda q_t+u_t$ (eq 8.2),
  spread $=2(c+\lambda)$, $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ — matches
  `hasbrouck_ch6-10.md` lines 61–63 ("**CORRECT**").
- **Almgren–Chriss** (`index:49–52`, `03:35–51`): permanent $g=\gamma v$, temporary
  $h=\epsilon\,\mathrm{sgn}(v)+\tilde\eta v$, $E[x]=\tfrac12\gamma X^2+\epsilon\sum|n_k|+\tilde\eta\sum n_k^2$,
  the $\sinh$ trajectory and $\kappa$ form — correct.
- **Almgren et al. (2005)** (`index:55–56`, `04:52–58`): $I=\gamma\sigma\frac{X}{V}(\frac{\Theta}{V})^{1/4}$,
  $J=\frac I2+\mathrm{sgn}(X)\eta\sigma(\frac{X}{VT})^{3/5}$, $\gamma=0.314$, $\eta=0.142$, permanent
  exponent $1$, temporary $3/5$ — correct.
- **Gatheral no-dynamic-arbitrage** (`index:64`, `04:69`, `06:44`): manipulation $\iff\gamma+\delta<1$,
  i.e. no-arbitrage requires $\gamma+\delta\ge1$; exponential kernel + nonlinear impact excluded — correct
  and consistent across all three files.
- **Diffusive-book derivation** (`04:42–44`): $\rho(\ell)=\rho_0\ell \Rightarrow L=\tfrac12\rho_0\ell^2
  \Rightarrow \ell=\sqrt{2\Delta V/\rho_0}$; the code recovers slope **0.5054** (diffusive) and **1.0000**
  (flat), matching the analytic $\sqrt{2\Delta V}=141.4$ vs simulated 141.
- **Bouchaud–Farmer–Lillo** (`index:60`, `04:63`): $\beta=(1-\gamma)/2$, $\gamma\approx0.5\Rightarrow$
  impact $\sim N^{3/4}$ — internally consistent (the error is the *restatement* in `06:37`).
- **OFI / Amihud** (`index:69–70`, `05:38`, `05:55`): $\lambda_{\mathrm{OFI}}\propto1/\text{depth}$,
  $I=\mathbb E[|r_t|/\$\text{Vol}_t]$ — correct; OFI regression recovers $1/(2\,\text{depth})$ to 5 dp.

---

## Coherence (hub vs sub-pages, jargon, links)

- **Hub ↔ prerequisites:** consistent. Hub declares Probability & Measure + Econometrics as the
  folder-level prereqs for `02`–`06` and explicitly exempts `01`; `01` states only Probability &
  Measure Theory, matching the hub's footnote. Documented house convention, not a defect.
- **Links:** all **17** unique wikilink targets resolve to existing folders/files; no dead links.
- **Jargon:** consistent across the folder (`λ`, `1/λ`, temporary/permanent, OFI, propagator). No
  undefined term introduced in a sub-page without a preceding definition.
- **Contradictions:** the only two are `04:32`↔`04:130` and `06:37`↔`04:63` (reported above). No
  numeric disagreement between the hub's quick-reference table and the sub-pages.

---

## Summary

- **Spelling/typos:** none.
- **Math:** 5 findings — 1 broken LaTeX (`01:41`), 1 sign-convention error (`03`), 1 formula/label
  mismatch (`03:109`), 2 coherence/formula defects (`04:32`↔`04:130`; `06:37`).
- **Code:** 7/7 blocks run, all outputs exact.
- **Coherence:** hub/prereq/links clean; two contradictions listed above.

# Audit — pillars/04-quantitative-risk/model-risk-and-validation

Folder: `content/pillars/04-quantitative-risk/model-risk-and-validation/`
Scope: 7 files (index + 01–06). `_legacy/` absent — nothing ignored.
Role: sole adversarial reviewer.
Date: 2026-09-10

## Summary

- **Files checked:** 7
- **Python blocks run:** 10 (all stdlib, no deps). **10/10 execute clean (exit 0) and stdout matches the documented output fence exactly** (normalised trailing-space/blank-line). No code discrepancy found.
- **Wikilinks:** 18 unique link targets — all resolve to existing files.
- **Math:** 3 errors found (2 distinct root causes, one appearing twice).

---

## 1. Math errors (3)

### 1.1 index.md:55 — green-zone LR/p-value summary row contradicts the table's own code output
- **Stated:** row `0–4 | ≤0.77 | ≥0.38 | … | green | 0.00 | 3.00`.
- **Correct:** the Kupiec LR is *two-sided*; `x=0` and `x=1` fall inside the green zone but give `LR_uc=5.0252 (p=0.0250)` and `LR_uc=1.1765 (p=0.2781)` respectively (confirmed by the block at index.md:80–104, which prints `x=0 LR_uc=5.0252`). So the green zone spans `LR_uc` from `0.0949` to `5.0252` and p from `0.0250` to `0.7580`, not "≤0.77 / ≥0.38". The stated bounds only describe exceptions 2–4.
- **Impact:** the lookup row misleads a reader into thinking zero exceptions is a *strong pass* on the two-sided test, when the POF test actually *rejects* at 5% for `x=0` (over-conservative model).

### 1.2 03-validation-and-backtesting.md:168 — "LR_uc first exceeds the 5% critical value 3.84 at x=7" is false
- **Stated:** "Kupiec test needs roughly ≥7 exceptions to reject at 5% (… LR_uc first exceeds the 5% critical value 3.84 at x=7)."
- **Correct:** `LR_uc` also exceeds `3.8415` at `x=0` (`5.0252`), and at `x=7` (`5.4970`). The *first* exceedance in ascending exception count is `x=0`; the claim "first … at x=7" holds only if one (wrongly) drops the two-sided `x=0` case. (Related to 1.1 — same two-sided Kupiec root cause, separate location.)
- **Note:** the *intended* point — that a materially wrong model (true rate 2%) can still pass, i.e. low power — is correct; only the "first exceeds at x=7" sentence is wrong.

### 1.3 05-failure-modes-and-practice.md:37–38 — sign error in the drift exception-rate closed form
- **Stated:** $\pi_1=\Phi\!\left(\frac{\sigma_0}{\sigma_1}\,z_{1-p}\right)$; then "at $\sigma_1=2\sigma_0$, $\pi_1=\Phi(1.163)=0.878\to$ the expected exception rate is $\approx12\%$".
- **Correct:** the exception (breach) rate is $\pi_1=\Phi\!\left(-\frac{\sigma_0}{\sigma_1}\,z_{1-p}\right)=\Phi(-1.163)=0.122\approx 12\%$. As written, $\Phi(+1.163)=0.878$ is the *coverage* (probability of NOT breaching), not the breach rate — the boxed formula has the wrong sign and the stated `π1=0.878` contradicts the claimed 12% (and the code at 05:89–99 which correctly returns `12/100 = 12.0%`). Fix: negate the argument inside $\Phi$.
- **Impact:** the worked number (12%) is right, but the displayed formula is wrong by a sign — exactly the kind of symbol-level error that defeats a lookup reader.

---

## 2. Math verified correct (no error)

- **Kupiec/Christoffersen/conditional coverage** (index:41–49; 03:32–38): formulae, $LR_{uc}=0.0949\ (p{=}0.7580)$, $LR_{ind}=0.0732$, $LR_{cc}=0.1681\ (p{=}0.9194)$, $\chi^2_1$ tail via `erfc(√(z/2))`, $\chi^2_2$ tail via $e^{-z/2}$ — all reproduce in code.
- **BCBS traffic light** (index:51–63; 03:40): zone boundaries at $x=5$ ($\mathbb P(K\le5\mid99\%)=0.958817$, = BCBS 95.88%) and $x=10$ ($0.999946$); `plus` schedule `{5:0.40,6:0.50,7:0.65,8:0.75,9:0.85}`; `k=3+plus` — all match.
- **Diebold–Mariano / pinball** (03:42–46, 03:124–160): loss differential `DM=-0.0385`; correct reading given.
- **Error-budget quadrature** (02:42–48, 02:116): `0.37524²+0.00532²+0.03989²+0.08888²+0.52719² → total 0.6544 (6.262%)`; vega `37.524`, rho `53.2325`; `base call=10.4506`; all reproduce.
- **VaR quantile SE** (index:128, 05:40): $se=\frac1{f(q)}\sqrt{\frac{\alpha(1-\alpha)}n}=0.2361\sigma$ at $n{=}250$ ≈ stated 0.23σ. OK.
- **Selection-bias / expected max** (05:31–32): $E[\max_{i\le M}\hat t_i]\approx\sqrt{2\ln M}-\frac{\ln\ln M+\ln4\pi}{2\sqrt{2\ln M}}$; Bonferroni $z^\star=\Phi^{-1}(1-\alpha/M)=3.8906$ at $M{=}1000$; `max t=3.6360`; `sqrt(2 ln 1000)=3.7169` — all reproduce.
- **POT / GPD quantile & method-of-moments** (01:42–44): $u+\frac{\hat\beta}{\hat\xi}[(\frac{N}{N_u}(1-\alpha))^{-\hat\xi}-1]$, $\hat\xi=\frac12(1-\bar y^2/s^2)$, $\hat\beta=\frac12\bar y(\bar y^2/s^2+1)$ — standard, correct.
- **BMA/BIC** (06:29–33): $w_i\propto e^{-\frac12\Delta\mathrm{BIC}_i}$; weights `0.7307/0.2093/0.0600`, `BMA=10.6179`, `sd=0.2903` — reproduce.
- **KL divergence (Gaussian)** (06:38): $0.009566$ and $0.101778$ — reproduce.
- **Entropy-robust bound** (06:42, 06:83–85): $E_P[X]+\sqrt{2\varepsilon\operatorname{Var}_P(X)}$ (leading order, exponential-tilting dual) — add-ons `0.6550/2.0713/4.6315` reproduce.
- **Capital link** (04:37–39): $\Delta=(k-3)\mathrm{VaR}$, green 0% → red 33% of the $3\times\mathrm{VaR}$ base — correct.

---

## 3. Code audit

10 Python blocks across the 7 files; **all 10 ran (exit 0) and stdout matched the documented output fence byte-for-byte** (after trailing-space normalisation). No fabricated/documented-vs-actual mismatch.

| File | Blocks | Status |
|---|---|---|
| index.md | 1 | ✓ |
| 01-from-zero-intuition.md | 1 | ✓ |
| 02-sources-of-model-risk.md | 1 | ✓ |
| 03-validation-and-backtesting.md | 2 | ✓ |
| 04-model-risk-management.md | 2 | ✓ |
| 05-failure-modes-and-practice.md | 2 | ✓ |
| 06-advanced-extensions.md | 1 | ✓ |

## 4. Spelling / typos

No spelling/typo issues found in prose (code/LaTeX excluded; code was executed, not spell-checked).

## 5. Coherence

- **Hub vs 01 prereqs:** index.md:11 states pages 02–06 share folder-level prereqs (Statistics & Inference, Probability & Measure Theory) and that 01 declares its own smaller set; 01.md:10 lists Stats & Inference + VaR/ES. Consistent, no contradiction.
- **Jargon first-use:** *effective challenge* defined index:23 and 04:23; *conceptual soundness* defined 03:20; *deflated Sharpe ratio* introduced 05:34 (§2.2) with Bailey & López de Prado before use; *pinball loss* defined 03:43; *PIT histogram* defined 03:48. All introduced before use.
- **Links:** 18 unique targets — all resolve.
- **Internal numbers:** `LR_uc=0.0949` (index:45) = Panel A (03:113); `LR_ind=0.0732` (index:46) = Panel A (03:113); `DM=-0.0385` (05:113) = 03:159. Consistent.
- **Contradiction flagged:** none beyond the three math errors above; the 05 §2.3 closed form (1.3) and its code disagree on formula sign but agree numerically on 12%.

---

## Verdict

**FOUND — 3 math errors (2 distinct root causes: the two-sided Kupiec "green zone" mischaracterisation in index:55 and 03:168; and a sign error in the drift exception-rate formula in 05:37–38).** All 10 code blocks execute and match documented output; all links resolve; no typos. The numeric conclusions of the affected sections are nevertheless correct — the errors are in the displayed formulae/tables, which is precisely what a lookup consumer reads.

# Audit: pillars/03-derivative-pricing/calibration-and-market-practice

**Scope:** 7 files (index + 01–06). **Role:** sole adversarial reviewer. **Date:** 2026-09-10.
**Verified sources cross-checked:** `corpus/verified/gatheral_ch1-5.md`, `bergomi_ch1-5.md`, `bergomi_ch6-10.md`; sibling folder `advanced-volatility-heston-sabr/`. **Ignored:** `_legacy/`.

---

## Summary

- **Code blocks:** 7/7 run clean (rc=0), deterministic (all use `random.seed`), output **exactly** matches every output fence. No code errors.
- **Links:** all wikilinks resolve (dir-only links map to existing `index.md`). No broken links.
- **Math:** 1 real math error (SABR ATM skew, **04**). 1 minor numeric understatement (**05**). 2 minor notation inconsistencies (κ/ξ vs κ/η; χ vs ν).
- **Spelling/typos:** none found.
- **Coherence hub↔01:** consistent; 01 states its own smaller prereqs as the hub promises. No internal contradictions beyond notation.

**Verdict:** ISSUES_FOUND — 1 math error, 3 minor. All code output verified correct.

---

## 1. Spelling / typos

No doubled words; full manual read found no spelling or grammatical errors. Prose is clean and consistent.

---

## 2. MATH — every boxed formula + worked example

### 04-calibrating-stochastic-vol.md

**MATH ERROR — line 36 (also §2 context).**
> "with ATM skew $\partial\sigma_{\text{BS}}/\partial k|_{k=0}=\rho/2$"

For the SABR formula stated (boxed, line 34, $\sigma_{BS}(k)=\sigma_0\frac{y}{f(y)}\big(1+\tfrac14\rho\chi\sigma_0+\frac{2-3\rho^2}{24}\chi^2T+\dots\big)$, $y=-\chi k/\sigma_0$), the ATMF skew is **$\rho\chi/2$**, not $\rho/2$. The skew carries the vol-of-vol factor $\chi$.

- *Stated:* $\rho/2$
- *Correct:* $\rho\chi/2$ (with $\chi$ = SABR vol-of-vol as used in the SDE $d\sigma_t=\chi\sigma_t\,dZ_2$ and the boxed formula).
- *Proof (numerical):* with the code's own truth params $\rho=-0.30$, $\chi=\nu=0.40$, the Hagan ATM skew computed by central difference = **−0.0607**; $\rho\chi/2=-0.06$ ✓, while $\rho/2=-0.15$ ✗ (off by 2.5×).
- *Corroboration:* sibling folder `advanced-volatility-heston-sabr/index.md:47` states the same result correctly as $\rho\nu/2$ (verified numerically there: $\rho\nu/2\cdot0.989=-0.1374$). So 04 contradicts its own cited prerequisite.
- *Impact:* minor in practice (the code fits with the full Hagan formula and recovers the truth), but the prose formula is wrong and self-contradictory.

**Notation inconsistency (χ vs ν, lines 19/32–36 vs code 50–58).** Text/formula use $\chi$ for SABR vol-of-vol; the code and its printed output use `nu` (ν); the sibling H&S folder uses $\nu$ and reserves $\chi$ for the instantaneous vol *level*. Convention clash within the page and vs the prerequisite folder — same parameter, three symbols across the folder boundary.

### 05-failure-modes-and-practice.md

**Minor numeric understatement — line 90.**
> "blows one reconstructed local variance up to $4.3\times10^7$ — six orders of magnitude above the true level"

- *Stated:* "six orders of magnitude"
- *Correct:* ~**nine** orders. $4.34\times10^7$ / true level $(\sim0.024$–$0.048) \approx 9\times10^8$–$1.8\times10^9 \approx 10^{8.9}$–$10^{9.3}$.
- *Impact:* the claim understates the instability (qualitative point stands; not dangerous, but the number is wrong). The code output (max `43406990.52`) is correctly transcribed.

### Formulas verified CORRECT (vs corpus)

| File:line | Formula | Source check |
|---|---|---|
| 03:32 | Dupire local variance $\sigma_{loc}^2(K,T)=\frac{2(\partial_T C+qC+(r-q)K\partial_K C)}{K^2\partial_{KK}C}$ | standard Dupire; consistent w/ Gatheral 1.4 |
| 03:40-41 | Gatheral (1.10) local variance from total variance | **matches** `gatheral_ch1-5.md:31-34` exactly |
| 03:36 | $\sigma^2(K,T,S_0)=\mathbb{E}[v_T\mid S_T=K]$ (Gyöngy) | matches Gatheral 1.12 (`gatheral_ch1-5.md:38`) |
| 03:45 | implied skew = ½ local skew; curvature = ⅓; $\alpha\propto t^{-\gamma}$ decay, equity γ≈½ | **matches** Bergomi 2.48–2.53 (`bergomi_ch1-5.md:164-169`) |
| 04:30 | Heston short skew→$\rho\eta/2$, long→$\rho\eta/(\lambda'T)$; two-expiration recipe | **matches** Gatheral 3.19 (`gatheral_ch1-5.md:87-88`) |
| 04:34 | SABR $\sigma_0\frac{y}{f(y)}(1+\frac14\rho\chi\sigma_0+\frac{2-3\rho^2}{24}\chi^2T)$ | matches H&S folder line 46 (with χ=ν) |
| 05:37 | Bergomi (2.89) $\mathcal S_T=\frac{1}{\hat\sigma_T^2T}\int_0^T\frac{T-t}{T}\langle d\ln S_t\,d\hat\sigma_T(t)\rangle dt$ | **exact match** `bergomi_ch1-5.md:198` |
| 02:40 | bias–variance decomposition | correct (standard) |
| 02:44-46 | ridge $+\lambda\|\theta-\theta_0\|^2$, normal eqs $(X^\top X+\lambda I)^{-1}X^\top y$ | correct |
| 02:36 | BSM vega $=S e^{(b-r)T}n(d_1)\sqrt T$ | correct (Hull) |
| 06:32 | SVI $w(k)=a+b(\rho(k-m)+\sqrt{(k-m)^2+\sigma^2})$, $k=\ln K$ | **matches** Gatheral 3.20 (`gatheral_ch1-5.md:90`) |
| 06:36 | LFM caplet = Black $Cpl=P(0,T_i)\tau_i Bl(K,F_i(0),v_i)$ | consistent w/ BM Ch 6 |
| 02:48 / index:37 | overfitting mechanism, ridge shrinks coefficients | correct |

### Worked examples / code-derived claims

- **index + 01:** single-σ fit: price-RMSE opt σ=0.23904 vs vol-RMSE opt σ=0.26; cross-RMSEs 1.21277/0.04799. Reproduced exactly. Narrative (price-RMSE biased to ATM, sits below) correct.
- **02:** degree-6 extrapolates 1.42 where true smile ~0.35; ridge restores ~0.42. Reproduced. ("true smile ~0.35" is approximate — the input list peaks at 0.335 near k=+0.35 and extrapolates down to ~0.2; loose but not wrong.)
- **03:** LV round-trip closes within ~1–3 vol pts (short maturity), local vol smile-shaped 0.064 (put side) vs 0.027 (ATM). Reproduced exactly. Note text says "deep-OTM/ITM dropped" while table still shows k=±0.30 — minor wording, not an error.
- **04:** free SABR fit recovers truth (α=0.141, β=0.512, ρ=-0.299, ν=0.396 vs 0.15/0.5/-0.3/0.4); freeze β=0.3/0.5/1.0 gives statistically identical RMSE but different ρ; ridge lam=1 pins β=0.6 at no fit cost. All reproduced exactly. This is the correct demonstration of non-identifiability.
- **05:** ~0.4-volpt noise → v_loc max 4.3e7 (see #2 above), 1/19 points negative/absurd. Reproduced.
- **06:** SVI fits SABR slice to total-var RMSE 2.3e-5 with butterfly w''≥0 (no strike arb). Reproduced.

---

## 3. CODE — run + diff vs output fence

All 7 blocks run under `python3`, exit 0. Each seeds RNG → fully deterministic. Diffed stdout vs the trailing fence: **byte-identical** in every case.

| File | Block | Matches fence |
|---|---|---|
| index.md | single-σ dual-objective | ✓ |
| 01 | single-σ dual-objective | ✓ |
| 02 | polynomial overfit vs ridge | ✓ |
| 03 | LV inversion + MC round-trip | ✓ |
| 04 | SABR fit + identification + ridge | ✓ |
| 05 | LV instability with/without noise | ✓ |
| 06 | SVI fit + butterfly check | ✓ |

No nondeterminism issues (all seeded; MC in 03 uses `random.seed(7)`). No code logic errors found.

---

## 4. COHERENCE — hub, jargon, links, contradictions

- **Hub vs 01 prereq:** index states 01 "has its own smaller entry requirements"; 01 declares only "Black–Scholes–Merton Hub, no prior derivatives knowledge" — consistent.
- **Notation inconsistency (κ/ξ vs κ/η) — lines index:40, 02:110, 04 §2 heading "The κ/ξ ridge".** The page family defines Heston vol-of-vol as **η** (04:19 $dv_t=-\lambda(v_t-\bar v)dt+\eta\sqrt{v_t}dZ_2$; 04:38 explicitly "mean-reversion speed λ (or κ) and vol-of-vol η"). Yet the collinear pair is written **κ/ξ** in three places. "ξ" is never defined here and, in Bergomi (cited on the same pages), $\xi_t^T$ denotes the forward-variance *curve* — a different object. Elsewhere in the folder it is correctly **κ/η** (04 failure-mode 1; 05:22; 05 failure-mode 2). Internal contradiction; recommend unify to κ/η (or λ/η).
- **Links:** all resolve. `counterparty-risk-and-xva` and `numerical-methods` are dir-wikilinks that map to existing `index.md`. No dangling links.
- **No other contradictions** across the six sub-pages (failure modes, desk practice, and literature citations are mutually consistent and agree with the verified corpus).

---

## Errors found (summary)

1. **[MATH] 04:36** SABR ATMF skew stated $\rho/2$; correct $\rho\chi/2$ (drops the vol-of-vol factor). Verified numerically (−0.06 vs −0.15).
2. **[MINOR] 05:90** "six orders of magnitude" above true level; actual ~nine orders ($4.3\times10^7$ vs ~0.03).
3. **[MINOR] index:40, 02:110, 04 §2** "κ/ξ" for Heston pair; should be κ/η (ξ undefined/incorrect here; contradicts 04:38, 04-FM1, 05).
4. **[MINOR] 04** SABR vol-of-vol rendered χ in text/formula vs ν in code and in the sibling folder — convention clash.

No spelling errors, no broken links, no code/execution errors.

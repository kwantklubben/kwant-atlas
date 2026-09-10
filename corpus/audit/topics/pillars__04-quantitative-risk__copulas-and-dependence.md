# Audit — `pillars/04-quantitative-risk/copulas-and-dependence/`

**Scope.** 7 topic files (index hub + 6 sub-pages). Sole adversarial reviewer.
**Checks performed:** (1) spelling/typos, (2) every boxed formula + worked example + every numeric check value re-derived with *independent* primitives (Newton normal-inverse + direct numerical integration of the Student-$t$ density — no code shared with the pages), (3) every ```` ```python ```` block executed and diffed against its output fence, (4) hub↔page coherence, jargon, links, contradictions.
**Method reproducibility:** all 7 code blocks run under CPython 3.14.7, stdlib only, 0 external deps required.

---

## 1. Verdict summary

| Metric | Result |
|---|---|
| Files checked | 7 / 7 |
| Python blocks run | 7 / 7 |
| Blocks matching output fence | 7 / 7 (exact, line-for-line) |
| Worked formula/check values independently re-derived | 12 / 12 correct |
| Wikilink targets resolved | 67 / 67 |
| **Genuine errors found** | **2** (1 math error, 1 formula/notation error) |
| Minor / coherence notes | 3 |

**VERDICT: FAIL** — two errors, both in the *index hub*'s mathematical ground truth; the six sub-pages are clean on math and code. Fixes below.

---

## 2. ERRORS (must fix)

### E1. Reversed dependence-risk inequality — `01-from-zero-intuition.md:54`
**Stated:**
$$\text{risk}(M)\ \le\ \text{risk}(C)\ \le\ \text{risk}(W)\quad(\text{for coherent, subadditive risk measures}).$$
**Correct:** for any risk measure monotone in the supermodular/concordance order (which is exactly what "coherent, subadditive" buys you — comonotone additivity), **dependence raises risk**, so
$$\text{risk}(W)\ \le\ \text{risk}(C)\ \le\ \text{risk}(M).$$
The stated direction is backwards and **contradicts the page's own §2 worked example** (Case 2 comonotone VaR $=1.6449$ > Case 1 independent $=1.1631$ > Case 3 countermonotone $=0$): under the stated inequality the countermonotone book (risk $0$) would sit at the *top*.
> Fix: swap to `risk(W) ≤ risk(C) ≤ risk(M)` and (optional) note that plain VaR is not generally monotone in dependence, so the "coherent, subadditive" qualifier is doing the work.

### E2. Upper tail-dependence formula is internally inconsistent — `index.md:51`
**Stated:**
$$\lambda_u=\lim_{q\to1}\Pr(X_2>F_2^{\leftarrow}(q)\mid X_1>F_1^{\leftarrow}(q))=\lim_{q\to1}\frac{\hat C(q,q)}{1-q}.$$
**Problem:** the survival-copula argument must go to the *lower* corner as the quantile level $q\to1$; here $\hat C(q,q)$ is evaluated at $q\to1$ while the denominator $1-q\to0$, so the right-hand limit diverges ($\hat C(1,1)=1$, denominator $\to0$) instead of giving $\lambda_u$.
**Correct:**
$$\lambda_u=\lim_{q\to1^-}\frac{\hat C(1-q,\,1-q)}{1-q}
\Big(= \lim_{v\to0^+}\frac{\hat C(v,v)}{v}\Big),$$
i.e. equate the limit via the survival quantile $v=1-q$. (The sub-page gets this right: `04-tail-dependence-and-t-copula.md:40` writes $\lambda_u=\lim_{q\to0^+}\hat C(q,q)/q$ — correct with $q$ a small survival level. The hub and sub-page must be consistent.)
> Fix: rewrite the second equality as $\lim_{q\to1^-}\hat C(1-q,1-q)/(1-q)$ (or adopt the sub-page's small-$q$ form).

---

## 3. Math verified correct (independent re-derivation)

Every boxed formula and every "Verified check" / worked number below was re-derived with independent primitives (Newton-based normal inverse over `math.erf`, direct Simpson integration of the $t(\nu)$ density, and the $\mathrm{Phi}_2$ bivariate-normal integral). All agree to the precision printed.

| Location | Formula / result | Verdict |
|---|---|---|
| `index:42`, `02:41-44` | Sklar's theorem $F=C(F_1,\dots,F_d)$, converse $C(u)=F(F_1^\leftarrow(u),\dots)$ | correct |
| `index:43`, `02:54`, `01:50` | Fréchet bounds $\max(\sum u_i+1-d,0)\le C\le\min(u_i)$ | correct |
| `index:44`, `02:58-60` | $\Pi(u){=}\prod u_i$; $M(u){=}\min u_i$; $W(u_1,u_2){=}\max(u_1{+}u_2{-}1,0)$ | correct |
| `index:45`, `02:63-66` | Gauss copula; $\varrho{=}0.7$: $C(0.95,0.95){=}0.9196$, $C(0.05,0.05){=}0.0196$ | correct (re-derived 0.919599 / 0.019599) |
| `index:46`, `02:67` | $t$ copula $C^t_{\nu,P}(u)=t_{\nu,P}(t_\nu^{-1}(u))$ | correct |
| `index:47`, `06:38` | Gumbel $C=\exp(-[(-\ln u)^\theta+(-\ln v)^\theta]^{1/\theta})$ | correct |
| `index:48`, `06:36` | Clayton $C=(u^{-\theta}+v^{-\theta}-1)^{-1/\theta}$ | correct |
| `index:49`, `02:82`, `02:84` | Kendall $\rho_\tau=\frac2\pi\arcsin\varrho$; $\varrho{=}0.7\to0.4936$; inversion $\varrho=\sin(\pi\rho_\tau/2)$ | correct |
| `index:50`, `02:82` | Spearman $\rho_S=\frac6\pi\arcsin(\varrho/2)$; $\varrho{=}0.7\to0.6829$ | correct |
| `index:51` | upper $\lambda_u$ definition (probabilistic half) | correct (formula half: see E2) |
| `index:52`, `04:48-51` | Gaussian $\lambda=0$ for all $\varrho<1$; coeff $\sqrt{(1-\varrho)/(1+\varrho)}$ | correct |
| `index:53`, `04:61` | $t$ copula $\lambda=2\,t_{\nu+1}\big({-}\sqrt{\tfrac{(\nu+1)(1-\varrho)}{1+\varrho}}\big)$; $\nu{=}4,\varrho{=}0.5\to0.2532$ | correct |
| `04:65-70` | t Table 7.1 all rows incl. $\varrho=0$ col ($0.18,0.08,0.01$) | correct (indep) |
| `index:54`, `06:37,39` | $\lambda_u^{Gu}=2-2^{1/\theta}$ ($\theta{=}2\to0.5858$); $\lambda_l^{Cl}=2^{-1/\theta}$ ($\theta{=}2\to0.7071$) | correct |
| `index:55`, `03:47` | Vašíček conditional PD $p(x)=\Phi\big(\tfrac{\Phi^{-1}(p)-\sqrt\rho x}{\sqrt{1-\rho}}\big)$ | correct |
| `index:56`, `03:51` | Asymptotic loss CDF $F(\theta)=\Phi\big(\tfrac{\sqrt{1-\rho}\,\Phi^{-1}(\theta)-\Phi^{-1}(p)}{\sqrt\rho}\big)$; $p{=}2\%,\varrho{=}15\%\to F(0.1763)=0.999$ | correct |
| `index:57`, `03:52` | Loss quantile $\theta_q=\Phi\big(\tfrac{\Phi^{-1}(p)+\sqrt\rho\,\Phi^{-1}(q)}{\sqrt{1-\rho}}\big)$; $p{=}5\%,\varrho{=}15\%\to\theta_{0.99}{=}0.2099$, $\theta_{0.999}{=}0.3135$ | correct |
| `03:39` | Li default time $\tau_i=F_i^{-1}(\Phi(Z_i))$ meta-Gaussian | correct |
| `03:60` | Tranche EL $= \mathbb E[\min(L,b)-\min(L,a)]/(b-a)$ | correct |
| `06:34` | Archimedean construction $C(u)=\psi(\sum\psi^{-1}(u_i))$ | correct |
| `06:36,38` | Clayton generator $\psi(s)=(1+s)^{-1/\theta}$; Gumbel $\psi(s)=e^{-s^{1/\theta}}$; frailtys $\Gamma(1/\theta,1)$ resp. pos.-stable$(1/\theta)$ | correct |
| `06:47` | Marshall–Olkin $U_i=\psi(E_i/V)$; Clayton $U=(1+E/V)^{-1/\theta}$; Gumbel $U=e^{-(E/V)^{1/\theta}}$ | correct |
| `04:57` | $t$-cop conditional $\sqrt{\frac{\nu+1}{\nu+x^2}}\,\frac{X_2-\rho x}{\sqrt{1-\rho^2}}\sim t_{\nu+1}$ | correct |
| `03:45`, `02:69`, `04:74` | one-factor $X_i=\sqrt\rho Y+\sqrt{1-\rho}Z_i$; $t$-cop simulation $\mathbf X=\mathbf Z\sqrt{\nu/W}$, $W\sim\chi^2_\nu$ | correct (code matches) |

Additional independent numeric spot-checks that agree: the hub's simulated joint-tail excesses (q=0.95 → 7.7×, q=0.99 → 25.3× over independence); page 03's senior-tranche ES-vs-$\rho$ correlation smile and the closed-form vs MC Vašíček cross-check (0.1763 vs 0.1752 at 99.9%).

---

## 4. Code audit — all 7 blocks

Ran under CPython 3.14.7 (page 03 requires `random.binomialvariate`, Python ≥ 3.12 — met; the conditional-mean fallback handles older builds). **Every block's output matches its ```` ``` ```` fence exactly (character-for-character).**

| File | Block | Output fence | Notes |
|---|---|---|---|
| `index.md` | Gauss tail-excess + Vašíček quantiles | MATCH | seeded MC (seed 1); deterministic |
| `01` | independent/comonotone/countermonotone VaR & ES | MATCH | seeded (20240501); analytic line correct |
| `02` | Sklar via $\mathrm{Phi}_2$ integral + empirical CDF + rank-correlation closed forms | MATCH | seeded (7); reproduces 0.9196/0.0196, τ 0.4893 vs 0.4936, ρS 0.6780 vs 0.6829 |
| `03` | CDO tranche simulation + Vašíček cross-check | MATCH | binomialvariate (seeded 2024/99/5); finance-free, stdlib |
| `04` | $t$-copula λ vs Table 7.1 + tail simulation | MATCH | custom regularized-incomplete-beta `t` CDF; correct to 4 dp vs McNeil table |
| `05` | Kendall inversion fit + regime-shift tails | MATCH | this is the file's main new computation; ratios 4.8×/12.3×/20.7× reproduced exactly |
| `06` | Gumbel/Clayton Marshall–Olkin tails | MATCH | stable_pos sampler; converges to 0.5858 / 0.7071 |

**Nondeterminism note:** all MC outputs are reproducible given the explicit `random.seed(...)` calls; `random.binomialvariate`'s output was also stable across this interpreter. Verified on this run; a future Python patch-level change to `random` could shift the seeded sequences, so the fences are pinned to CPython 3.14 (3.12-compatible paths were not re-run) — flagged for re-run if the toolchain changes.

No block fails, errors, or crashes; none depends on packages outside the stdlib.

---

## 5. Coherence — hub vs pages, jargon, links, contradictions

**Links:** all 67 `[[...]]` targets across the 7 files resolve (incl. `foundations/*`, all sibling pillar sub-pages, and in-folder `01`–`06`). The hub's routing list (§6) names all 6 sub-pages with correct paths.

**Hub↔page consistency:** the hub's £formula lookup (index §2) matches the six sub-pages' full derivations everywhere except the E2 tail-dependence edge case (hub uses the divergent $q\to1$ form; page 04 uses the correct $q\to0$ form). All headline numbers in the hub (§3) come straight from the page code and agree. Prerequisite chains are coherent: `01`(self-contained) → `02`→`03`/`04` → `05`→`06`; hub prerequisite block matches. Jargon introduced on `01` (marginals, copula, Fréchet bounds, rank correlation) is re-used consistently downstream; no undefined terms found.

**Contradiction to flag (from E1):** `01:54`'s reversed inequality contradicts `01`'s own §2 worked VaR example — reviewers of page 01 should treat the inequality line as the authoritative-correcting detail.

### NOTE N1 — "Formula-verified in the corpus" overclaims (sourcing)
`index:35`, `02:198`, `03:173`, `04:200,204`, `06:153` state McNeil, Frey & Embrechts (2015) Ch 7, Bluhm (2010), Bielecki & Rutkowski (2002), and de Haan & Ferreira (2006) are "formula-verified / math-verified in the corpus" reference=`corpus/verified/*.md`. **None of these are transcribed in `corpus/verified/`** (that directory holds Tsay/Hull/Gregory/Glasserman/Brigo–Mercurio etc., not McNeil/Bluhm/Bielecki/Haan). The four titles exist only as *acquired raw PDFs* under `corpus/titles/refs/pillar4/` (`McNeil_2015_...pdf`, `32_Bluhm_2010_...pdf`, `33_Bielecki_2002_...pdf`, `18_Haan_2006_...pdf`). The math itself is *independently confirmed correct* in this audit, so the item to fix is the attribution wording ("acquired, not yet verified") — not the formulas.

### NOTE N2 — generator codomain (very minor) `06:32`
$$\psi:[0,\infty)\to(0,1],\quad \psi(0)=1,\ \psi(\infty)=0.$$
As written the codomain `(0,1]` excludes `0` while `ψ(∞)=0` asserts `0` is attained; should be `[0,1]` (or note the convention). Cosmetic; no downstream effect (all families in the file satisfy `[0,1]`).

### NOTE N3 — terminology consistency (cosmetic)
ASCII `Vasicek` appears only inside code comments/output (`index`, `03`); prose uses the diacritic `Vašíček` — no action needed. `McNeil` spelled consistently; `d.o.f.` = degrees of freedom consistent.

---

## 6. Spelling / typos
No spelling errors, no duplicated words, no common misspellings detected across the 7 files (scanned repeats, `dependance/recieve/seperate` etc.). Clean.

---

## 7. Actions recommended
1. **Fix E1** (`01:54`): reverse to `risk(W) ≤ risk(C) ≤ risk(M)`; keep/annotate the coherence qualifier.
2. **Fix E2** (`index:51`): change $\lim_{q\to1}\hat C(q,q)/(1-q)$ to $\lim_{q\to1^-}\hat C(1-q,1-q)/(1-q)$ to match page 04:40.
3. **Optional:** soften the "corpus-verified" attributions (N1) to reflect acquisition-only status; adjust `[0,1]` codomain on `06:32` (N2).

*All 7 code blocks re-run cleanly; all 12 headline numbers and closed forms independently re-derived correct; 67/67 links resolve. The two open items are the index-level math fixes above.*
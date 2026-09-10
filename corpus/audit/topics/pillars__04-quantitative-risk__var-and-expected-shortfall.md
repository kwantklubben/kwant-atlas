# Audit — `pillars/04-quantitative-risk/var-and-expected-shortfall/`

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages). VaR/ES definitions, coherence axioms, ES subadditivity & closed forms, ES/VaR ratio for the normal (and t), Euler allocation, backtests, Basel FRTB.
**Corpus cross-check:** `corpus/titles/refs/pillar4/Artzner_1999_coherent_measures_of_risk.pdf`, `08_Rockafellar_2000_optimization_of_conditional_value_at_risk.pdf`, `09_Acerbi_2002_on_the_coherence_of_expected_shortfall.pdf`; `corpus/verified/hull_ch19-23.md` (Hull Ch 22 verified digest).
**Method:** (1) spelling/typo scan of prose (code/LaTeX excluded); (2) every boxed formula & worked example re-derived and cross-checked against the source PDFs; (3) every ```python block executed in Python 3 and diffed against its output fence; (4) hub↔sub-page coherence, jargon first-use, wikilink resolution.

---

## VERDICT: **PASS (with minor fixes)** — 6 minor defects, 0 high-severity; all 7 code blocks reproduce their fences exactly; all core math correct.

---

## Summary of findings

| # | Severity | File:line | Type | Issue |
|---|----------|-----------|------|-------|
| 1 | **MINOR** | `02-var-definition-and-flaws.md:41` | MATH (numeric) | "the 1.6% chance of a 2000 payout" — writing 2 A-options pays 2000 with prob $P(S_T>U)=0.008$ (0.8%), not 1.6%. |
| 2 | **MINOR** | `05-failure-modes-and-practice.md:28` | NUMERIC / consistency | "the 99% VaR is the 297th sorted loss" — the code picks `s[int(0.99·300)] = s[297]` = the **298th** order statistic. Off-by-one vs its own code (which ES also draws from). |
| 3 | **TRIVIAL** | `04-expected-shortfall.md:122` | TYPO | "non-elic lack of ES" — truncated word; should read "non-elicitable". |
| 4 | **TRIVIAL** | `04-expected-shortfall.md:47` | QUOTE | Mangled R-U quotation `"$(x)\le \mathrm{CVaR}$… portfolios with low CVaR necessarily have low VaR as well."` — stray broken math fragment; source reads "the α-VaR is never more than the α-CVaR". |
| 5 | **MINOR** | `01:39`, `02:59/85`, `index:50` | CITATION | The two-bond 4%-default / \$100 "koan" is labelled "(Artzner §3.3)". Artzner §3.3's counterexamples are the digital-option construction (0.008/1000) and the Albanese credit example; the 4%/\$100 bond is a simplification, not from the source (softened by "made discrete", but the §3.3 attribution is imprecise). |
| 6 | **TRIVIAL** | `06-advanced-extensions.md:98` | CROSS-REF | Link caption "03 · §4.2" — `03` has no §4.2 subsection; the PH/liquidity point is §4 item 2 / §2.1. |

All **boxed formulas, the coherence scorecard, and every worked example** re-derived correct. **7 of 7** python blocks execute and reproduce their documented output fences **character-for-character**.

---

## FINDING 1 — MINOR · wrong probability in the digital-option narrative (`02-var-definition-and-flaws.md:41`)

**Stated:** "Writing $2A$ alone: the $1\%$ VaR of the net worth is $-2u$ (essentially the premium — **the $1.6\%$ chance of a $2000$ payout** sits inside the $1\%$ quantile only if it is the adverse tail …)"

**Correct:** Writing two A-options each paying 1000 if $S_T>U$ gives a total payout of **2000 with probability $P(S_T>U)=0.008$ = 0.8%**, not 1.6%. (The $1.6\%$ union probability belongs to the *A+B* position, and that carries a single 1000 payout, not 2000 — Artzner: "the positive number $1000-l-u$". Since $0.8\%<1\%$ the 2000-event indeed sits *beyond* the 1% quantile, so the qualitative point stands; only the number is wrong.)

**Source check (Artzner §3.3):** "Choosing $L$ and $U$ such that $P\{S_T<L\}=P\{S_T>U\}=0.008$ … They are $-2\cdot u$ and $-2\cdot l$." ✓ (stated value $0.016$ appears nowhere for the 2A position).

**Fix:** replace "$1.6\%$" with "$0.8\%$" (or drop the parenthetical).

---

## FINDING 2 — MINOR · order-statistic index off by one (`05-failure-modes-and-practice.md:28`)

**Stated:** "with a $300$-observation sample the $99\%$ VaR is the **$297$th** sorted loss: the $298$th, $299$th, $300$th … do not enter."

**Problem:** the page's own code uses `var(s,a) → s[min(len-1, int(a*len))] = s[297]`, which is the **298th** order statistic under 1-based counting. Its ES (`s[-3:]`) then draws the 298th, 299th, 300th — i.e. **VaR itself (298th) is inside the ES tail**, contradicting "the 298th … do not enter". The rank used for the $\partial\mathrm{ES}/\partial(\text{worst loss})=1/k$ demo is therefore inconsistent with the prose by one position. Numerator demo ($(15-3)/3 = 4$) is unaffected.

**Fix:** state "$298$th" and "the $299$th, $300$th do not enter" (or switch the code to `int(a*n)` vs 1-based rank consistently).

---

## FINDING 3 — TRIVIAL · truncated word (`04-expected-shortfall.md:122`)

Reference line reads "— **non-elic** lack of ES (the backtesting caveat)." Should be "non-elicitable".

---

## FINDING 4 — TRIVIAL · mangled quotation (`04-expected-shortfall.md:47`)

The text quotes R-U as: `Rockafellar–Uryasev: "$(x)\le \mathrm{CVaR}$… portfolios with low CVaR necessarily have low VaR as well."` The leading `"$(x)\le \mathrm{CVaR}$"` is a broken fragment. Source (`08_Rockafellar...pdf`): "the α-VaR is never more than the α-CVaR, so portfolios with low CVaR must have low VaR as well." The second half of the quote is verbatim-correct.

---

## FINDING 5 — MINOR · imprecise attribution of the two-bond example

Pages `01:39` ("The subadditivity koan (Artzner §3.3), made discrete"), `02:59` (§3 code relying on the 4%/\$100 bond) and `index:50` ("Artzner §3.3") present two independent bonds each losing \$100 w.p. 4%. That exact construction is **not in Artzner §3.3** (verified: the PDF has no "4%", no "0.04"). Artzner's §3.3 counterexamples are (a) the digital options (`P=0.008`, payout 1000) — faithfully reproduced in `02 §2.2` — and (b) the Albanese credit example (2% spread, 1% default, \$1m, 5% VaR = −\$20,000, $P(\ge2\text{ defaults})>0.18$) — faithfully reproduced in `02 §2.4`. The \$100/4% bond is a valid independent simplification, but attributing its numbers to §3.3 overstates the sourcing. Recommend "a discrete analogue inspired by Artzner §3.3".

---

## FINDING 6 — TRIVIAL · dangling cross-reference (`06-advanced-extensions.md:98`)

Link caption "([[…03-coherent-risk-measures|03 · §4.2]])" cites a §4.2 that does not exist in `03` (its §4 has no subsections; the homogeneity/liquidity point is §4 item 2). Target file resolves; only the section label is wrong.

---

## Verified-correct items (no action)

### Formula engine & lookup (hub §2 table) — ALL CORRECT
- **VaR** $\mathrm{VaR}_\alpha(L)=\inf\{l:\mathbb P(L>l)\le 1-\alpha\}=F_L^{-1}(\alpha)$ (`index:30`, `02:29`, `01:34`) ✓
- **Artzner net-worth form** $\mathrm{VaR}_\alpha(X)=-\inf\{x:\mathbb P(X\le xr)>\alpha\}$ (`index:31`, `02:33`) ✓ — matches Artzner Def. 3.1 verbatim; pinned to right quantile $q^+_\alpha=\inf\{x:\mathbb P(X\le x)>\alpha\}$ (Def. 3.2) ✓
- **ES tail mean / quantile integral / Rockafellar–Uryasev min** (`index:32-34`, `04:29-31`) ✓
- **Discrete-atom ES correction** (`04:35`): $\frac{1}{1-\alpha}(\mathbb E[L\mathbf 1_{L\ge \mathrm{VaR}}]-\mathrm{VaR}(\mathbb P(L\ge \mathrm{VaR})-(1-\alpha)))$ ✓ (matches Acerbi–Tasche tail-mean form)
- **Normal VaR** $\mu+\sigma z_\alpha$ and **Normal ES** $\mu+\sigma\varphi(z_\alpha)/(1-\alpha)$ (`index:35-36`, `01:47`, `04:52`) ✓ — agrees with `corpus/verified/hull_ch19-23.md` eq (22.1) "Normal ES = σ·φ(zα)/(1−α)"
- **Normal ES/VaR @99%** $\varphi(z_\alpha)/((1-\alpha)z_\alpha)=1.145665$ (`index:37`) ✓ (re-derived)
- **N-day √N scaling for VaR and ES** (`index:38`, `04:110`) ✓ (Hull lines 26836–26837, confirmed in the verified digest)
- **FRTB 97.5% ES ≈ 99% VaR** calibration: ES$_{97.5\%}=2.337803$ vs VaR$_{99\%}=2.326348$, ratio $1.004924$ (`index:52`, `04:53`, `06:81-82`) ✓

### Coherence (Artzner §2–§5) — ALL CORRECT
- **Four axioms** (T: $\rho(X+\alpha r)=\rho(X)-\alpha$; S: $\rho(X_1+X_2)\le\rho(X_1)+\rho(X_2)$; PH; M) (`03:29-34`, `index:42-47`) ✓ — Def. 2.4 verbatim
- **M rules out mean–std $\rho=-E[X]+\alpha\sigma$; S rules out semi-variance** (`03:36`) ✓ — Artzner's Remark reproduced exactly
- **Acceptance set** $\mathcal A=\{X:\rho(X)\le0\}$, $\rho_{\mathcal A,r}(X)=\inf\{m: mr+X\in\mathcal A\}$; equivalent axioms $L^+\subseteq\mathcal A$, $\mathcal A\cap L^{--}=\varnothing$, convex, cone (`03:38-42`) ✓
- **Scenario representation** $\rho(X)=\sup\{\mathbb E_P[-X/r]:P\in\mathcal P\}$ (Prop. 4.1) (`03:47`) ✓ verbatim
- **TCE / WCE** (Defs. 5.1/5.2), **TCE ≤ WCE** (Prop. 5.1), **equality under uniform P + distinct discounted outcomes** (Prop. 5.3), **VaR = least coherent measure dominating it** (Prop. 5.2) (`03:52-57`) ✓ all verbatim from source
- **Spectral family** $M_\varphi=\int_0^1\varphi(u)\mathrm{VaR}_u\,du$, $\int\varphi=1$, $\varphi$ non-decreasing; ES as the step $\varphi_{\mathrm{ES}}=\frac{1}{1-\alpha}\mathbf 1_{u>\alpha}$ (`06:27-34`) ✓ (Acerbi 2002)
- **Kusuoka mixture** $\rho=\sup_\mu\int \mathrm{ES}_\alpha\,d\mu$ (`06:37`) ✓
- **Euler** $\rho(L)=\sum_i w_i\,\partial\rho/\partial w_i$ (`06:43`) ✓
- **Subadditivity failure koan**: VaR$_{95\%}$(A)=VaR$_{95\%}$(B)=0, VaR$_{95\%}$(A+B)=100, and $1-0.96^2=7.84\%>5\%$ ✓; ES(A)=ES(B)=80, ES(A+B)=103.2 ≤ 160 ✓ (hand-verified and code-verified)

### Worked numbers — ALL CORRECT
- $z_{0.99}=2.326348$, ES$_{99}=2.665214$, portfolio \$1e6: VaR 2,326,347.9 / ES 2,665,214.2 ✓ (block `index`)
- Bond koan: one-bond VaR 0.0 / ES 80.00; two-bond VaR 100.0 / ES 103.20; 50-bond MC VaR 400.0 / ES 535.8 ✓
- Axiom checks: translation VaR(A+c)=10=VaR(A)+c, ES=90; homogeneity VaR(λA)=0=λ·VaR(A), ES=240 ✓
- MC three-representations: analytic 2.66521, tail-mean 2.66900, quantile-integral 2.66903 ✓
- Estimation error: sd(VaR$_{99}$) = 0.2314 / 0.1181 / 0.0388 at n=250/1000/10000 — matches the text's "≈0.23σ, ≈0.12σ, ≈0.04σ" ✓; ES sd larger at every n ✓
- Tail blindness: worst loss 3→15 leaves VaR unchanged, moves ES by 4 ✓
- Euler allocation: two-asset normal, $\sigma_P=0.019349$, ES$_{99}=0.051570$, contributions sum to ES (diff 1.4e−17) ✓; FRTB ratio 1.004924 ✓

### Code blocks — execution & fence diff
**7 blocks** extracted (one per file) and executed. **All 7 reproduce their documented output fences character-for-character** (after trailing-whitespace trim). Block `01`/`02`/`03`/`05` use seeded RNG (`random.seed(...)`) and are therefore **deterministic**; no nondeterminism observed.

### Coherence, links, jargon
- Structure: exactly index + 6 sub-pages; no stragglers. ✓
- All **61 unique wikilinks resolve** (hub↔sub-pages, foundations/probability-and-measure-theory, foundations/calculus-and-optimization, siblings at 04-quantitative-risk/*, forward to 05-portfolio-optimization/*). ✓
- Hub declares folder-level prereqs (prob&measure + 01) and correctly notes page 01 states its own smaller entry requirements — matches `01:10`. ✓
- Prereq chain 01→02→03→04→05→06 consistent with reading order; no contradictions between hub and sub-pages. ✓
- Jargon first-use: VaR/ES/CVaR/TailVaR/TCE/WCE/FRTB/EVT/FHS all defined at first use. Only nit: "TUFF" (Kupiec) appears only in the `05:110` reference line without expansion, and "OTM" (`01:107`, `index:109`) is used without expansion in-folder (fine if the options pillar owns it). Not counted as errors.
- Spelling: one truncated token (`non-elic`, Finding 3); otherwise clean (British spelling used consistently: *optimise*, *decentralised*, *artefacts*, *idealisation*).

---

## Files checked (7)
1. `index.md`
2. `01-from-zero-intuition.md`
3. `02-var-definition-and-flaws.md`
4. `03-coherent-risk-measures.md`
5. `04-expected-shortfall.md`
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md`

**Blocks run:** 7 · **Errors found:** 6 (all minor/trivial; none blocks correctness of the exposition)

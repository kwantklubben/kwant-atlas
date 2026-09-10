# Audit — pillars/06-market-making/adverse-selection-and-glosten-milgrom/

**Date:** 2026-09-10 · **Auditor:** sole adversarial reviewer · **Files checked:** 7/7

## Verdict

**PASS with minor issues.** All mathematics is correct (every boxed formula and
worked example verified against the corpus and by independent derivation). All 7
Python blocks run and match their documented output fences exactly. Coherence is
strong (hub ↔ sub-pages consistent, jargon first-use mostly correct). Found 4
minor errors: 1 broken wikilink (in-page anchor), 1 wrong acronym expansion,
1 suspicious term, 1 capitalization typo.

---

## 1. Spelling / typos (prose)

| File:line | Issue | Correct |
|---|---|---|
| index.md:74 | `also copeland–Galai's` — lowercase proper noun (elsewhere always "Copeland–Galai") | `Copeland–Galai` |

- 05-failure-modes-and-practice.md:13 "thinner than poison" — odd literal phrasing
  (intended metaphor: thinner than the information cost), not a misspelling; noted,
  not counted as an error.

## 2. Mathematics — every boxed formula + worked example verified

All formulas independently re-derived and cross-checked against
`corpus/verified/hasbrouck_ch1-5.md`, `hasbrouck_ch6-10.md`, `foucault_ch1-3.md`.
**No math errors found.** Confirmations:

- **Buy-arrival law** `P(B|V_H)=(1+π)/2`, `P(B|V_L)=(1−π)/2` — correct (index:48, 03:33).
- **Bayes bid/ask update** `θ±` — correct (index:53, 02:43, 03:38).
- **Zero-profit quotes** `A=E[V|buy]`, `B=E[V|sell]` — correct (index:61, 03:43).
- **GM ask/bid half-spreads** `s_a^t, s_b^t` (index:66–67, 05:39) — derived:
  `θ⁺−θ = πθ(1−θ)/(πθ+(1−π)/2)`, `θ−θ⁻ = πθ(1−θ)/(π(1−θ)+(1−π)/2)`. ✓
- **Symmetric spread** `S = π(V_H−V_L)` at θ=½ (index:71, 03:52) — correct; verified by
  Monte Carlo in code (index/03 outputs, e.g. π=0.25 ⇒ spread=0.50=2·0.25).
- **Hasbrouck δ/µ form** `A−B=4(1−δ)δµ(V_H−V_L)/(1−(1−2δ)²µ²)`, δ=½ ⇒ `(V_H−V_L)µ`
  (index:75, 03:54) — matches corpus hasbrouck_ch1-5.md:101,128. ✓
- **Wealth-transfer identity** `(A−E[V|U,B])Pr(U|B) = −(A−E[V|I,B])Pr(I|B)` (03:58)
  — matches corpus hasbrouck_ch1-5.md:102 (Eq 5.4). ✓
- **P(informed|buy) = 2π/(1+π)** (index:35, 02:37) — correct; π=0.1 ⇒ 0.1818 ✓ (code).
- **Adverse-selection P&L** `E[P&L]=h−π` and `h*=π` (01:43–45) — correct (code matches).
- **Winner's curse** `E[P&L]=h−π(V_H−V_L)/2` (05:33) — correct; π=0.30, h=0.10 ⇒ −0.20 ✓ (code).
- **Kyle lambda** `λ=½√(Σ₀/σ_u²)`, `β=√(σ_u²/Σ₀)`, depth `1/λ` (index:37, 06:33)
  — correct (matches corpus hasbrouck_ch6-10.md:39).
- **Kyle half-impounding** `Var[v|y]=Σ₀/2` (06:35,74) — derived & verified in code: 2.0000 = 4/2 ✓.
- **Kyle informed profit** `Eπ=(v−p₀)²/2·√(σ_u²/Σ₀)` (06:35) — derived: `Eπ=(v−p₀)²/(4λ)`, `1/(4λ)=½√(σ_u²/Σ₀)`. ✓
- **PIN** `αµ/(αµ+2ε)` (index:36, 06:41) — correct; code: (0.3,10,2)⇒0.4286, (0.3,30,2)⇒0.6923 ✓.
- **Spread decomposition** `Δp_t = c(q_t−q_{t-1}) + λq_t + u_t` (index:82, 04:37)
  — derived from `p_t=m_t+cq_t`, `m_t=m_{t-1}+λq_t+u_t`. ✓
- **Moment structure** `γ₀=c²+(c+λ)²+σ_u²`, `γ₁=−c(c+λ)`, `σ_w²=λ²+σ_u²=γ₀+2γ₁`
  (04:41–44) — all correct; OLS recovery verified in code (3/3 exact). ✓
- **ST−LT=c** (04:46) — correct (short-term impact λ+c, long-term λ).

## 3. Code — execution audit

Extracted and ran **every** ```python block in the folder; diffed stdout against the
following output fence (text or plain). Seed-based Monte Carlo reproduces exactly.

| File | Block | Result |
|---|---|---|
| index.md | 1 | MATCH |
| 01-from-zero-intuition.md | 1 | MATCH |
| 02-informed-vs-uninformed.md | 1 | MATCH |
| 03-the-glosten-milgrom-model.md | 1 | MATCH |
| 04-spread-decomposition.md | 1 | MATCH |
| 05-failure-modes-and-practice.md | 1 | MATCH |
| 06-advanced-extensions.md | 1 | MATCH |

**Blocks run: 7 · Blocks matching documented output: 7 · Failures: 0.**

## 4. Coherence, jargon, links

- **Hub ↔ 01 prereq:** consistent. Hub states page 01 carries its own smaller entry
  requirements; 01 requires only Probability & Measure Theory. Hub requires that +
  Bayesian Statistics. ✓
- **Six sub-pages claimed (01–06) and present (index + 6) = 7 files.** ✓
- **72 wikilinks scanned; 71 resolve.** Sibling/forward targets
  (toxic-order-flow-and-vpin, spread-decomposition-and-roll-model,
  avellaneda-stoikov-and-optimal-quoting, limit-order-book-mechanics,
  inventory-management-and-quote-skewing) all exist.
- **Broken link (ERROR):** index.md:88 `[[#the-glosten-milgrom-model|03 · The GM
  Model]]` — in-page anchor `#the-glosten-milgrom-model` matches no heading id on the
  index page (closest heading slugs to `the-glosten-milgrom-model` do not match). The
  alias "03 · The GM Model" indicates it should be the sub-page:
  `[[pillars/06-market-making/adverse-selection-and-glosten-milgrom/03-the-glosten-milgrom-model|03 · The GM Model]]`.
- **Wrong acronym expansion (ERROR):** 02-informed-vs-uninformed.md:91 writes
  "Volume-Synchronized probability of **toxicity** measures". VPIN = Volume-Synchronized
  Probability of **Informed Trading** (López de Prado / Easley–O'Hara). Fix the expansion.
- **Suspicious term (ERROR):** 06-advanced-extensions.md:109 "no-trade unemployment"
  — likely intended "no-trade intervals"/"no trading" (Easley–O'Hara 1992 no-trade
  results). Clarify.
- **Jargon first-use:** GM, adverse selection, PIN, Kyle lambda, VPIN, OFI all
  introduced before reuse; no orphan acronyms. "µ" overloaded (informed-fraction vs
  semi-strong efficient price `µ_t` vs Poisson intensity) but disambiguated in-place
  at each use; acceptable.

## Error summary (counted)

1. index.md:88 — broken in-page anchor link (should target sub-page 03 file).
2. 02-informed-vs-uninformed.md:91 — VPIN acronym expansion wrong ("toxicity" → "Informed Trading").
3. 06-advanced-extensions.md:109 — "no-trade unemployment" unclear/incorrect term.
4. index.md:74 — lowercase "copeland–Galai" capitalization typo.

**errors_found = 4** (1 link, 1 factual/acronym, 1 terminology, 1 typo).
No math errors. No code mismatches.

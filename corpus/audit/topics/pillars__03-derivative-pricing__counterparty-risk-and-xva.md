# Audit: `content/pillars/03-derivative-pricing/counterparty-risk-and-xva/`

**Auditor:** sole adversarial reviewer (subagent)
**Scope:** 7 files (index + 01–06). All wikilinks, code blocks, and boxed formulas verified.
**Repo:** `/home/alfred/local-repos/kwant-atlas` · sources `corpus/verified/gregory_ch1-3.md`, `gregory_ch4-6.md`.
**Ignored:** `content/_legacy/` (none present under this topic).

**Verdict: PASS with corrections** — 3 errors (1 math/sign, 1 code-comment typo, 1 garbled token). All 9 Python blocks run and match their fences; all 61 wikilinks resolve; formulas numerically re-verified against the corpus. Nothing materially mispriced in the narrative.

---

## 1. Spelling / Typos

- Clean overall. Mixed BrE/AmE spellings ("stylised" text vs "stylized" printed in 03's code fence, 04 uses "stylised") — cosmetic, not flagged.
- `03-cva-and-dva.md:137` — **garbled token:** Hull reference reads "CVA & DVA `fnd - CVA + DVA`". The inline-code `` `fnd - CVA + DVA` `` is a stray artifact (likely a truncated "value = clean price − CVA + DVA" or funding-based value formula) and conveys nothing on its own. **ERROR-3 (text/coherence).**

---

## 2. MATH — boxed formulas & worked examples

All transcribed formulas were re-derived/numerically re-computed against the verified corpus. **Identified one real sign error.**

### 2.1 Exposure metrics (index §2; 02 §2.1; 01 §2) — CORRECT
- `EFV=μ`, `PFE(α)=μ+σΦ⁻¹(α)`, `EPE=σφ(z)+μΦ(z)`, `ENE=σφ(z)−μΦ(−z)` (z=μ/σ) match corpus exactly (gregory_ch1-3:98–108).
- Worked checks μ=2,σ=2: EPE 2.17 ✓, ENE 0.17 (positive magnitude; book convention, corpus notes "book states positive magnitude") ✓, PFE(99%)=6.65 ✓. μ=2,σ=4: EPE 2.79 ✓, ENE 0.79 ✓, PFE 11.31 ✓.
- 01 five-scenario Spreadsheet 11.1: EFV 22, PFE 70, EPE 30, ENE −8, EPE+ENE=EFV ✓ (matches corpus line 97).
- Note: ENE is presented as a positive *magnitude* in the index/02 tables while the text asserts ENE≤0; this is inherited from the source book's convention and the code displays `-ENE` (negative), so it is internally consistent. Not flagged.

### 2.2 CVA / DVA (index §2; 03; 01 CVA step) — CORRECT
- Discrete Eq 17.3 `−LGD Σ EPE_i PD(t_{i-1},t_i)` ✓. Hazard λ=s/LGD (Hull 24.2; BM 21.25) ✓. Flat-EPE check: EPE=20, 150bp, LGD 60%, 5y ⇒ CVA=0.6×20×(1−e^(−0.125))=**1.4100** ✓ (index:58, code reproduces exactly).
- Bilateral CVA/DVA with first-to-default survival factors (Eqs 17.8a/b) — code reproduced UCVA −1.40 / UDVA +0.49 / BCVA −0.89, hand-verified ✓. Index "stylised 5y swap ⇒ −0.89" ✓ matches 03.
- Integral form CVA=−LGD∫λ_C D_{r+λ_C} EPE du (Eq 17.2) and DVA integral (17.7c) match corpus lines 162–166 ✓.
- Spread approx formula text (Eq 17.9) `BCVA ≈ −EPĒ·s_C − ENĒ·s_P` matches corpus line 173 ✓.

### 2.3 ⚠ FVA / MVA (04; index §2) — CODE SIGN ERROR in 03, FVA/MVA themselves CORRECT
- FVA=−Σ EFV·FS·Δt (Eq 18.3), FCA=−Σ EPE·FS·Δt, FBA=−Σ ENE·FS·Δt, FVA=FCA+FBA — code reproduces FCA −1.336 / FBA +0.236 / FVA −1.100, hand-verified ✓ (index:66 agrees).
- MVA=−Σ EIM·FS·Δt (Eq 20.1): EIM 100→30 @100bp ⇒ −3.314 ✓ (hand-verified; index:67 agrees).
- **ERROR-1 (MATH, sign):** `03-cva-and-dva.md:110` code and `:118` output. The code computes the spread approximation as
  `-sum(epe)/5*sp_c + sum(ene)/5*sp_p` = −19.8×0.015 + (−10.2)×0.010 = **−0.399 ≈ −0.40**.
  But Eq 17.9 (stated correctly at `03:69`) is `BCVA ≈ −EPĒ·s_C − ENĒ·s_P`. With ENĒ = −10.2, the correct value is
  −0.297 − (−0.102) = **−0.195 ≈ −0.20**.
  The code applied `+ENĒ·s_P` where Eq 17.9 has `−ENĒ·s_P`; since ENE is negative this flips the DVA/own-credit side from a *benefit* (−0.20) into an additional *cost* (−0.40), roughly doubling the magnitude. Output fence reproduces the buggy −0.40. **Stated −0.40, correct −0.195.**

### 2.4 Initial margin / SIMM (02 §2.3–2.4) — CORRECT (one comment typo)
- Var-cov IM = Φ⁻¹(α)√τ σ_P: 99%/10d σ=100 ⇒ **46.34** (book 46.4) ✓; 99%/5d 32.77 ✓; 95%/10d 32.77 ✓; 99% ES(10d) 53.09, multiplier 2.66≈2.67 ✓.
- SIMM two-tenor delta: √(13797²+43427²+2·0.84·13797·43427)=**55,523** (Gregory 55,524; full-tenor 59,540) ✓; gross sum 57,224 ✓. Corpus line 187 confirms 59,540 and 84% correlation ✓.
- Net standardised IM (0.4+0.6·NGR)×gross: 60,000/42,000/24,000 ✓.
- **ERROR-2 (code-comment typo):** `02-exposure-and-margin.md:91` comment claims "exact product **32.67**" for 95% 10-day, but the code's own exact product (and printed value) is **32.77** (Φ⁻¹(0.95)=1.6449 × 0.1992 × 100). "32.67" is a typo for "32.77".

### 2.5 Failure modes & capital (05; 06; index §2) — CORRECT
- WWR "corr +50% roughly doubles EPE, −50% at least halves" matches corpus line 632 ✓; 05 MC experiment reproduces ratio 1.85 (+0.5) and 0.34 (−0.5) — consistent, and the E~N(10,20) unconditional EPE 13.96 at ρ=0 hand-verifies ✓.
- JTD P&L (Eq 21.2): unhedged −26.0, hedged +10.0 — hand-verified ✓.
- BA-CVA reduced form (Eq 13.3) and per-cpty K=SCVA·√(ρ²+(1−ρ²)/n) match corpus lines 243/388 ✓; n=1,2,10,50 → K/n 1.118/0.935/0.758/0.718, converg. to ρ=0.5 ✓.
- SA-CVA per-bucket and across-bucket forms, R=0.01, α=1.4, ρ=50%, 5% floor — all match corpus ✓.
- P&L explain (Table 21.8): 120,960−1,800,820−1,610,770+279,335−214,585 = **−3,225,880** ✓ (hand-summed).
- KVA/MVA trade-off model (MVA=20f, KVA=38.8(1−f)²): min at f=0.75 (17.43 bps) — illustrative toy; corpus (line 866) confirms the *qualitative* result that the optimal IM is below full regulatory. Consistent.

### 2.6 MPoR / netting / CSA (02) — CORRECT
- CSA Eq 7.3, MPoR model Eq 15.3 (Exposure_t = max(V_t − C_{t−MPoR}, 0)), TH+MTA additivity, 5d/10d MPoR, "IM ≡ negative threshold" — all match corpus/standard practice. No errors.

---

## 3. CODE — execution vs output fences

9 Python blocks (index:1, 01:1, 02:1, 03:1, 04:1, 05:3, 06:1). **All 9 executed successfully under python3 and byte-for-byte match their output fences.** Stdlib-only as claimed (math/random only).

Blocks whose printed output was also hand-verified: index CVA engine, 01 scenario metrics, 02 IM/SIMM, 04 FVA/MVA, 06 BA-CVA/P&L — all consistent with the corpus numbers. Exception: 03 spread-approx prints the buggy −0.40 (see ERROR-1); the fence is internally consistent with the code but the code is wrong relative to Eq 17.9.

---

## 4. COHERENCE — hub vs prereqs, jargon, links, contradictions

- **Wikilinks:** all **61** wikilink targets resolve (base = `content/`). Verified programmatically.
- **Hub ↔ sub-pages:** index §1/§6 reading routes map correctly to 01–06; every sub-page's Back/Forward/Index-Hub links are consistent and cycle-correct (01→02→03→04→05→06). Prereq chains (01 requires stoch-calc only; 02→01; 03→02; 04→03; 05→04; 06→05) are self-consistent. No dangling or wrong-direction links.
- **Jargon:** CVA/DVA/FVA/MVA/KVA/ColVA, EE/EPE/ENE/EFV/PFE, MPoR, SIMM, SA-CCR, BA-CVA/SA-CVA, WWR, JTD, IM/VM/CSA — used consistently with definitions given on first use. No unexplained abbreviations.
- **Cross-folder coherence:** index:71 critical caveat (CVA netting-set-level vs trade-additive FVA) agrees with 03:44/03:129; DVA/FBA double-counting warning appears consistently in 04:46-49, 05:22/42, and index:132. No contradiction between hub and 01–06.
- **Pillar 3 vs Pillar 4 partitioning — ADEQUATE.** Pillar 3 scope note (index:13) declares the **pricing/desk view** (xVA enters the price; desk marks & hedges) and routes the risk/regulatory view (capital, netting sets, SA-CCR, WWR-as-risk) to Pillar 4, whose index (04-quantitative-risk/.../index:12) reciprocates ("use this folder to govern, that one to price"). The two scope notes are symmetric and mutually citing. **Caveat (not an error):** Pillar 3 still substantively covers netting & margin (02), WWR (05, 06), CVA capital/BA-CVA/SA-CVA (06), and SA-CCR's 5% floor (06) — i.e. topics the Pillar 3 scope note *delegates* to Pillar 4 — just framed through the pricing lens. Because the "price vs govern" framing is explicit in both hubs and each names the other, the partitioning holds; but a reader could hit near-duplicate WWR/capital content in both folders. Recommend a one-line "this pillar treats X from the desk's pricing angle; risk-management version in Pillar 4" pointer on 06 (already present at 06's scope via index) — minor.
- **Corpus consistency:** Every claimed source number (46.4, 6.65, 1.4100, −21.5, FCA/FBA, 59,540, 55,524, K/n=0.758, P&L −3,225,880, jump %s 83/27) traces to the verified corpus or re-execution. No fabrication detected.

---

## Summary of errors

| # | File:line | Type | Stated | Correct |
|---|-----------|------|--------|---------|
| 1 | `03-cva-and-dva.md:110` (code) & `:118` (output) | **MATH — sign** | Spread-approx = **−0.40** (`-EPĒ·s_C + ENĒ·s_P`) | **−0.195** (Eq 17.9: `-EPĒ·s_C − ENĒ·s_P`, ENE negative ⇒ own-credit benefit added) |
| 2 | `02-exposure-and-margin.md:91` | code-comment typo | "exact product **32.67**" (95% 10-day) | **32.77** |
| 3 | `03-cva-and-dva.md:137` | garbled text token | `` `fnd - CVA + DVA` `` | remove / replace with meaningful phrase (e.g. value = clean − CVA + DVA) |

No run-time errors, no fabricated figures, no broken links, no hub/sub-page contradictions.

**files_checked: 7 · blocks_run: 9 · errors_found: 3**

# Audit: `content/fundamentals-accounting/capital-structure-and-corporate-finance/`

**Date:** 2026-09-10 · **Auditor:** sole reviewer (adversarial) · **Files:** 7 (index hub + 6 sub-pages) · **Blocks run:** 9/9 · **Scope:** spelling, math (MM I/II, tax shield, WACC, levered beta/relevering, EPS dilution), code execution vs. output fences, coherence/links.

## Verdict: **PASS WITH MINOR ISSUES — 1 substantive prose/output contradiction + 5 cosmetic/wording nits**

Every boxed formula and every worked example was independently re-derived. All 9 Python blocks run on the stdlib and reproduce their documented output fences (7 exact; 2 differ only by an omitted leading blank line). All 15 unique wikilink **targets** resolve. No prose spelling or grammar errors found. No wrong formula, sign, or constant found. The MM 1958 fn-12 constants (X=1000, D=4000, r=5%, ρ_k=10%) were verified against the paper text (footnote 12 reads *"suppose X = 1000, D = 4000, r = 5 per cent and p_k = 10 per cent"*).

---

## 1. Spelling / Typos (prose)
- **No errors.** Full read of all 7 files plus an automated scan (`pyspellchecker`, distance 1) over prose with code fences, `$…$`/`$$…$$` LaTeX, and wikilink targets stripped. Remaining flags were all domain terms/abbreviations/possessives (`ceteris`, `paribus`, `dilutive`, `overinvestment`, `unlevered`, `wipeout`, `gotchas`, `lookup`, `creditors'`, `managers'`, `holders'`, `mm's`, `ii's`, `dodd's`) — no genuine misspellings. Doubled-word regex scan clean (hits were only repeated numbers inside output fences).

## 2. Math — formulas & worked examples (all verified)

| Check | Location | Result |
|---|---|---|
| Prop I: V=X/ρ=1000/0.10=10 000; X/V=ρ_k | index:43, 02:31, 02 code | ✓ |
| Prop II: r_E=ρ_k+(ρ_k−r)D/S; fn-12 → 13.33% | index:44, 02:39/51, 02 code | ✓ |
| Prop II ≡ definition r_E=(X−rD)/S at every D (0,2000,4000,6000) | 02 code | ✓ (all match to the cent) |
| WACC-flatness identity: (D/V)r+(S/V)(ρ_k+(ρ_k−r)D/S)=ρ_k | 02:43 | ✓ (algebra expands to ρ_k) |
| Tax: X^τ=(X−rD)(1−T)+rD; V_L=V_U+τD; V_U=X(1−τ)/ρ | index:46, 02:45-49 | ✓ |
| Tax shield τD=0.30·4000=1200; V_L=7000+1200=8200 | index:46/100, 02 code | ✓ |
| WACC(with tax)=ρ(1−τD/V_L)=10%·(1−1200/8200)=8.54% | index:47, 02:47, both codes | ✓ (9.21% / 8.54% / 7.95% at D=2k/4k/6k all reproduce) |
| Arbitrage proof V_2>V_1 ⇒ α(V_2/V_1)X−αrD_2 > α(X−rD_2) | 02:35 | ✓ (difference = αX(V_2/V_1−1)>0) |
| Waterfall: recovery_i=min(C_i, max(0, A−Σ_{k<i}C_k)); equity=max(0, A−Σ senior) | 03:37/41, 03 code | ✓ (5 scenarios reproduce; equity=0 for A≤700) |
| ROE=NI/n; EPS dilution (V+mp)/(n+m)=9.60, transfer 40 | index:50/51, 04:31/43, both codes | ✓ |
| Buyback EPS accretion 140/90=1.556 (+11.1%); forgone-NI-corrected 133/90=1.478 | index:51, 04 code | ✓ |
| Death spiral ΔA=(r_d D−aA)/f, f=0.55; 7-step runaway to A=0 | 05:36, 05 code | ✓ (every step reproduces numerically) |
| FCF agency loss: FCF−FCF·g/ρ=100−30=70 destroyed | 04:37, 05:42, 06 | ✓ |
| Trade-off V_L=V_U+τD−Distress(D); D*=1000, V_L,max=1150 | index:53, 06:31, 06 code | ✓ (convex distress 600(D/2000)², peak reproduced) |
| Myers–Majluf transfer m(V′/(n+m)−p)=10·(11.8909−10)=18.9 > NPV 8 ⇒ refuse | index:52, 05:48, 06:42, 06 code | ✓ |

- Internal consistency across hub ↔ sub-pages: the hub lookup-table northstar values (V=10 000, r_E=13.33%, WACC=10.00%/8.54%, +1200, 8.54%, 40, 1.556, D*=1000, refuse NPV 8) are each reproduced by the owning sub-page. ✓
- No wrong formula, sign, or constant found in any boxed equation.

## 3. Code — execution vs. documented output
- **9 code blocks located, all 9 executed (Python 3), diffed against their output fences.**
  - index.md block0 — **exact match**. 02 block0 — **exact match**. 03 block0 — **exact match**. 04 block0 — **exact match**. 05 block0 — **exact match**. 06 block0 — **exact match**. 01 block0 — **exact match**.
  - 05 block1 & 06 block1 — **mismatch, cosmetic only**: these blocks begin with `print()` (emitting a leading newline) but the documented fence drops the leading blank line. All substantive output lines match. (See Findings #2, #3.)
- One coherent sample company (MM fn-12 firm: X=1000, r=5%, ρ=10%, D=4000, τ=30%) reused consistently across the hub and 02; separate self-contained datasets in 01, 03, 04, 05, 06 are internally consistent. No block throws; no undefined behavior.

## 4. Coherence, jargon, links
- **Hub ↔ 01 prereq:** consistent — hub (index:12) labels `financial-statements-and-accounting` + `core-financial-ratios` as the folder-level prereqs for pages 02–06 and notes page 01 "states its own, smaller, entry requirements" (01:11 lists Financial Statements only). ✓
- **Prereq chains:** 02→01; 03→01+02; 04→02+03; 05→02…04; 06→02+05. Non-cyclic, monotone, sensible. ✓
- **Links:** all 15 unique wikilink targets resolve to existing `.md` files (7 in-folder + 8 cross-folder). ✓
- **Jargon:** consistent and introduced before use (tax shield, home-made leverage, pecking order, residual claim, death spiral, debt overhang). No contradictions between the hub's four-friction framing (index:20-25), 01's first-principles (01:82), and 06's three theories. ✓
- **Northstar values** in the hub table are all traceable to the owning page's code. ✓

## Findings (defects)

| # | Severity | Location | Stated | Correct |
|---|---|---|---|---|
| 1 | **Substantive (content)** | `03-debt-equity-and-seniority.md:85` | "**senior debt is repaid in full in every scenario** (it is protected)" | False for the page's own output: senior claim = 300 but recovers only **250** at A=250 and **100** at A=100 (output lines 81-82). Senior is repaid in full only when A ≥ 300 (scenarios 900/650/480). The table/graph is correct; the prose overstates. Fix: "senior debt is repaid in full whenever assets cover it (A ≥ 300), and is the **last** claim to absorb losses." |
| 2 | Cosmetic | `05-failure-modes-and-practice.md` §3, 2nd output fence (L101-106) | fence starts with `== Agency cost…` | Actual stdout of that block begins with a **blank line** (block starts with `print()`). Add the leading blank line (or drop the leading `print()`). |
| 3 | Cosmetic | `06-advanced-extensions.md` §3, 2nd output fence (L119-128) | fence starts with `== Agency cost…` | Same: actual stdout begins with a blank line. Same fix. |
| 4 | Minor | `05-failure-modes-and-practice.md:60` code comment | `# shock: … equity ~0` | After the −900 shock equity = 1100 − 1200 = **−100** (the program's own output line 80 prints `equity ~ -100`). Comment should read `equity −100`. |
| 5 | Minor (wording) | `02-modigliani-miller.md:35` | "buy $\alpha(V_2/V_1)$ **worth** of firm 1" | Ambiguous; the return formula $\alpha(V_2/V_1)X$ requires buying a **fraction** $\alpha(V_2/V_1)$ of firm 1 (costing $\alpha V_2$, exactly the $\alpha S_2+\alpha D_2$ raised). Reword to "buy a fraction $\alpha V_2/V_1$ of firm 1". |
| 6 | Minor (notation) | `index.md:49` and `03-debt-equity-and-seniority.md:21` | ladder written "senior debt **<** junior debt **<** mezzanine **<** convertible **<** common equity" under the caption "from *most* to *least* protected" | The "<" glyph reads as *less-than*, inverting the intended meaning. Use ">" (greater protection) or a plain arrow "→" to avoid misreading. |

## Errors found: **6** (1 substantive · 2 cosmetic · 3 minor wording/notation)
## Blocks run: 9/9 · Files checked: 7

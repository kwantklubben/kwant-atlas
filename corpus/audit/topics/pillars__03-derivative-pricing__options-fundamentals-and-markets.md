# Audit: pillars/03-derivative-pricing/options-fundamentals-and-markets/

**Reviewer:** sole adversarial reviewer · **Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages) · **Verdict:** PASS (with minor editorial notes)

---

## Summary

- **Code:** all 7 ` ```python ` blocks run and diff **exactly** against their output fences (0 mismatches).
- **Math:** every boxed formula and worked example re-derived independently and cross-checked against `corpus/verified/` (haug_lookup-1, hull_ch1-6, shreve1_ch5-8). All correct.
- **Links:** every wikilink target resolves (folder links resolve to `<folder>/index.md`). All 7 sibling folder targets exist.
- **Coherence:** hub↔sub-page prerequisite chain is consistent (01→02→03→04→05; 06 depends on 02 & 04). No contradictions found.

---

## 1. Spelling / typos

| Severity | File:Line | Finding | Correction |
|---|---|---|---|
| minor | `01-what-is-a-derivative.md:24` | "the buyer's downside is truncated at (premium)" — dangling parenthetical | should read "truncated at **the** premium" |
| minor | `index.md:61` | Check column for the row "American call ≡ European call (no dividends)" cites a **put** tree (European put 0.9600 vs American put 1.3600) | the example correctly illustrates the early-exercise premium for puts, but sits under a call claim — harmless, could be relabelled as a put counter-example |

No other misspellings found in a targeted scan.

---

## 2. Math verification (all correct)

Every claim below was independently recomputed (not just diffed against the code) and confirmed.

### index.md — no-arbitrage skeleton
- Forward price `F0 = 60·e^0.05 = 63.0763` ✓ (matches code).
- Forward value `f = (F0−K)e^(−rT) = 66 − 63·e^(−0.025) = 4.5555` ✓.
- Put–call parity `p = c + X·e^(−rT) − S = 8.5 + 105·e^(−0.05) − 100 = 8.37909` ✓ (matches haug_lookup-1 L371: 8.3791→8.37909).
- Generalized parity `c−p = S·e^((b−r)T) − X·e^(−rT)`; with b=r gives `100 − 105·e^(−0.05) = 0.12091` ✓.
- Lower bounds `c ≥ 0.12091, p ≥ 0`; upper bounds `c ≤ 100, p ≤ 99.8791` ✓.
- Black-76 `F=X=19, T=0.75, r=0.10, σ=0.28 → c = 1.70105` ✓ (matches haug_lookup-1 L69/L371).
- American parity bounds `S0−K ≤ C−P ≤ S0−X·e^(−rT)` ✓ (Hull 11.7).
- Cost-of-carry dictionary b=r / r−q / 0 / r−r_f ✓.

### 01 — forward pricing
- Boxed `F0 = S0·e^(rT)` ✓.
- Forward value `f = (F0−K)e^(−rT) = S0−K·e^(−rT)`; worked `66 − 63·e^(−0.025) = 4.5555` ✓.
- Call net P&L `max(S_T−K,0)−c` ✓. Payoff menu symmetric/truncated correctly.

### 02 — mechanics & payoff diagrams
- Four-position payoff table correct (short call `=min(K−S_T,0)`, short put `=min(S_T−K,0)`) ✓.
- Moneyness classification (ITM/ATM/OTM) correct across the code table ✓.
- BSM ATM `call=10.4506, put=5.5735` ✓ (recomputed).
- OTM/ITM BSM values `X=80 → 24.5888/0.6872`, `X=120 → 3.2475/17.3950` ✓ (recomputed).
- Delta ranges `call∈(0,1), put∈(−1,0)` ✓. Breakeven `K+premium=110.45` ✓.
- Early-exercise: American call = European for non-dividend stock; put ≥ intrinsic — correct.

### 03 — markets & products
- Naked-call margin `max(100c+20%S−100·max(K−S,0), 100c+10%S)`; worked prem=5, S=55, X=50 → $1,600 ✓ (recomputed; Hull Ch 10.7).
- Naked-put margin worked prem=5, S=45, X=50 → $1,500 ✓.
- Rate-futures bp economics: 3-mo $1M → $25.00; 1-mo $5M → $41.67 ✓.
- Index notional 4200×100 = $420,000 ✓.
- Cost-of-carry master formula and Garman–Kohlhagen/Black-76/Merton specialisations correct.

### 04 — no-arbitrage & bounds
- Parity replication `A_T = B_T = max(S_T,K)` ✓.
- Generalized parity specialisations (stock/index/futures/currency) ✓.
- American bounds inequality ✓.
- Dividend-adjusted bounds & parity `c + D + K·e^(−rT) = p + S0` ✓.
- **Worked arbitrage:** sell call (c=10), buy put (p=8), buy stock (S=100), borrow 98 at r=10% for T=0.5; riskless profit = 98·(e^(0.05)−1)+2 = 1.97543 at every S_T ∈ {90,105,120} ✓ (recomputed).
- **Shreve Ex 5.1 tree** (S0=4, u=2, d=½, r=¼, K=5): European put 0.9600, American put 1.3600, early-exercise premium 0.4000 ✓ (matches shreve1_ch5-8 L49: `max{1.36,1}=1.36`).

### 05 — failure modes & hedging
- Basis `b2 = S2−F2`; effective price `F1+b2 = 2.20+0.05 = 2.25` ✓.
- `h* = ρ·σ_S/σ_F = 0.928·0.0263/0.0313 = 0.7798`; `R² = ρ² = 0.8612`; residual `(1−ρ²)σ_S² = 0.000096` ✓ (matches hull_ch1-6 L50: h*=0.78, N*≈37).
- `N* = 0.7798×2,000,000/42,000 = 37.13 → 37` ✓.
- Tailing `37/1.05 = 35.24` ✓. Empirical slope from seeded sim 0.7808 ✓.
- Boxed `h* = ρ σ_S/σ_F`, `N* = h* Q_A/Q_F` ✓.

### 06 — strategies
- Box spread constant payoff `K2−K1 = 10`, value `10·e^(−0.025) = 9.7531` ✓.
- Butterfly/spread/straddle payoff table all recomputed and match ✓.
- Principal-protected note `100·e^(−0.05) + call(10.4506) = 95.1229 + 10.4506 = 105.5735` ✓.
- Covered-call ≡ shifted short-put (via parity) ✓.

---

## 3. Code execution (7/7 match)

| File | Block | Result |
|---|---|---|
| index.md | payoff engine + parity + Black-76 anchor | ✓ MATCH |
| 01-what-is-a-derivative.md | forward/call P&L | ✓ MATCH |
| 02-options-mechanics-and-payoffs.md | BSM + moneyness + diagram | ✓ MATCH |
| 03-markets-and-products.md | margins + bp economics | ✓ MATCH |
| 04-no-arbitrage-and-bounds.md | parity + arbitrage + Shreve tree | ✓ MATCH |
| 05-failure-modes-and-practice.md | min-variance hedge sim | ✓ MATCH |
| 06-advanced-extensions.md | strategy table + box + note | ✓ MATCH |

---

## 4. Coherence & links

- Prereq chain consistent: index(none) → 01(none) → 02(01) → 03(02) → 04(03) → 05(04); 06(02 & 04). No dead-end or circular prereqs.
- All 17 external wikilinks to sibling pillars resolve (folder-style links map to `<folder>/index.md`, all exist).
- In-folder links among 01–06 all resolve. No `content/_legacy/` references.
- Jargon consistent with corpus (carry b, moneyness, CTD, box spread, minimum-variance ratio).
- Index hub lists all 6 sub-pages; each sub-page links back to hub and next/prev. No contradictions between hub and 01.

---

## Verdict: PASS

- **errors_found:** 2 (both minor/editorial — no math, no code, no link defects)
- **blocks_run:** 7 · **files_checked:** 7 · **math errors:** 0 · **code diffs:** 0

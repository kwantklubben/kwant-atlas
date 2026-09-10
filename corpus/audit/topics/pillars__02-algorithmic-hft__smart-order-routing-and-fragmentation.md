# Audit — pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/

**Reviewer role:** sole adversarial reviewer.
**Scope:** 7 files (index.md + 6 sub-pages). `content/_legacy/` ignored per house rules.
**Date:** 2026-09-10

---

## Summary

- **Files checked:** 7 (index, 01–06)
- **Python blocks:** 7 (one per file). All **run clean and byte-identical to their output fences** — no code/output divergence.
- **Wikilinks:** all cross-links resolve (no broken `[[path]]` targets), including the non-`/index` variants (`queue-position-and-fill-probability`, `optimal-execution-and-almgren-chriss/index`).
- **Spelling/typos:** none found (doubled-word scan clean; prose is clean).
- **Errors found:** **2 math errors** (see below). Both are in worked/demonstration math, not in the boxed formula blocks (those check out).

---

## 1. MATH VERIFICATION

### Boxed formulas — all CORRECT
- `index.md:52` — SOR objective LP `min Σqᵢ[pᵢ+fᵢ+φ(Lᵢ)+kθᵢ] s.t. Σqᵢ=Q, 0≤qᵢ≤Sᵢ`. Correct; greedy water-filling solution correct for a separable linear objective.
- `index.md:48` — NBBO `a*=min aᵢ, b*=max bᵢ, S*=a*−b*`. Correct.
- `index.md:49` — HHI fragmentation index and `1/HHI` effective venues. Correct.
- `index.md:58` — `S_cum = S_raw + 2f_t`. Correct.
- `02:32` — NBBO boxed. Correct. Locked/crossed definitions correct.
- `02:35–37` — HHI. Correct.
- `03:32` — SOR objective boxed. Correct.
- `04:38` — `S_cum = S_raw + 2f_t`. Correct.
- `06:34` — latency-aware objective boxed. Correct.
- `06:38` — crossover-latency derivation. Algebra correct.

### Worked examples — all CORRECT (verified by re-execution + recomputation)
- `index.md:67–113` — NBBO 100.00 (C), fee-aware legs [(B,400),(C,100)] avg 100.0120 = $50,006.00; price-only [(C,200),(B,300)] avg 100.0140 = $50,007.00; misroute $1.00 / 0.20 bps. ✓
- `01:52–121` — single-venue fill 800@100.0225 (C), largest venue 800@100.0350 (A), SOR full 1500@100.0193 = $150,029.00, 0.3 bps better. ✓
- `02:57–106` — NBBO B/C, spread 0.0100, mid 100.0050, HHI 0.2850 → 3.51 venues. ✓
- `03:54–111` — fee-aware avg 100.0030 vs fee-blind 100.0075, Δ0.0045/share = $4.50 = 0.45 bps. ✓
- `04:57–118` — X/Z all-in 100.0030 vs 100.0010; split table raw spread 0.0200→0.0242 at constant total 0.0009; make route 99.9879. ✓
- `05:51–110` — trade-through $30.00 / 3.0 cps; pick-off $4.47→$141.42 over 0.05→50 ms (×31.6 ≈ √1000); fee misroute $7.00. ✓
- `06:55–129` — B true cost 100.05657, latency-aware 100.01126, saves $45.31; L* = 0.2243 ms. ✓

### ❌ ERROR 1 — `02-fragmentation-and-nbbo.md:114` (Failure Modes §1)
- **Stated:** "costs 1–2 cents per share in this example — **500+ bps** of round-trip edge on a stock trading near 100.00..."
- **Correct:** 1–2 cents on a ~$100 stock is **1–2 bps per side**, i.e. **~2–4 bps round-trip** (2 cents/share = 2 bps one-way = 4 bps round-trip). "500+ bps" is off by ~100–250×; 500 bps of $100 = $5/share round-trip, inconsistent with the 1–2-cent per-share gap the same sentence quotes.
- **Severity:** High (materially misleading quantitative claim in a failure-modes callout).

### ❌ ERROR 2 — `05-failure-modes-and-practice.md:42` (fee-misrouting formula)
- **Stated:** `Δ_fee = minᵢ(pᵢ+fᵢ) − minᵢpᵢ − (fee of the raw-best venue)`, described as "positive whenever the reorder condition is crossed."
- **Correct:** per-share misrouting = all-in cost of the fee-blind choice minus the fee-aware choice = `minᵢpᵢ + (fee of the raw-best venue) − minᵢ(pᵢ+fᵢ)`. The published form is the **exact negation**.
- **Worked check (own demo data):** cheap-quote (99.996, 0.0150), dear-quote (100.004, 0.0000). True per-share misroute = `(99.996+0.0150) − (100.004+0.0000)` = **+0.007**. Stated formula = `100.0040 − 99.996 − 0.0150` = **−0.007** — negative, contradicting the text's "positive" claim. (The demo's printed $7.00 is itself correct — it is computed by the code path, not this prose formula.)
- **Severity:** Medium (sign/structure error in a displayed equation; the worked number is right so impact is limited, but the formula as written is wrong).

---

## 2. CODE VERIFICATION
All 7 ```python blocks extracted, executed with `python3`, stdout diffed against the adjacent output fence. **7/7 identical**, exit code 0. No fabricated or stale output. Includes the 02 f-string nesting (`{` + `{v}:{s:.0%}`), the 04 `make and (take-make)` quirk (correct), and the 06 `if target > ... else 0` guard — all reproduce exactly.

---

## 3. COHERENCE / JARGON / LINKS
- All 7 files share consistent vocabulary: all-in price, cum-fee spread, `σ√L` latency term, HHI fragmentation, water-filling greedy sweep, trade-through/Reg NMS Rule 611. No jargon drift.
- Folder-level prerequisite discipline held: hub `index.md:11` correctly scopes folder prereqs to pages 02–06 and defers page 01 to its own lighter entry bar; page 01 honors that.
- Cross-page forward/back links (01↔02↔03↔04↔05↔06↔hub) all present and resolving; external topic bridges (market-microstructure, queue-position, market-making, VPIN, Almgren–Chriss, low-latency) all resolve.
- Literature cites internally consistent (Colliard & Foucault numbers 30c/21c/9c round-lot and the SEC 0.30/round-lot 2006 cap are consistent between 04 and 05; O'Hara & Ye 0.29c/7s figures consistent between 02 and 04).
- **Minor exposition nit (not an error):** `06:37–39` "Crossover latency" — prose labels venue `i` "better quote" but then defines `Δ = pᵢ+fᵢ−(pⱼ+fⱼ) > 0` which implies `i` is *worse*, and the equation solves for the *fast* venue's latency (≈6.647 ms in the demo) whereas the demo prints `L*=0.2243 ms`, the *slow* venue's latency threshold. The algebra and demo are each correct — only the index naming/prose is loose and could mislead a reader mapping the formula onto the printed number. Suggest clarifying which venue's latency each side solves for.

---

## Verdict
**CHANGES NEEDED** — 2 math errors (one high-impact bps claim, one wrong-signed formula). Boxed formulas, all 7 code blocks, all other worked examples, links, and prose are verified correct.

### Required fixes
1. `02-fragmentation-and-nbbo.md:114` → change "500+ bps" to "~2–4 bps" (or "1–2 bps per side / 2–4 bps round-trip").
2. `05-failure-modes-and-practice.md:42` → invert to `Δ_fee = minᵢpᵢ + (fee of the raw-best venue) − minᵢ(pᵢ+fᵢ)`.
3. (Optional) `06:37–39` → clarify which venue's latency the crossover solves for.

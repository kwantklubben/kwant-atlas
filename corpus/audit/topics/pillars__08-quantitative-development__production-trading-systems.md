# Audit: Production Trading Systems

**Folder:** `content/pillars/08-quantitative-development/production-trading-systems/`
**Files checked:** 7 (index hub + 6 sub-pages `01`–`06`)
**Blocks run:** 7 (one `python` block per page; each executed with `python3` and diffed against its printed fence)
**Result:** FAIL — 3 defects: one deterministic math off-by-one (token-bucket claim), one broken-LaTeX operator, one nonsensical code comment. All 7 code blocks run and **byte-for-byte match** their fences. All 30 unique wikilinks resolve. No prose misspellings, no cross-page numeric contradictions beyond the token-bucket item.

---

## (1) Spelling / prose typos

No prose misspellings or doubled words found. Scan covered all `*.md` in the folder for common transpositions/doubled tokens — clean. The only spelling-class item is inside a code comment (excluded from this category): **06 line 86** `# … hours to repair/provoke` — `repair/provoke` should be `repair/reprovision` (the page's own line 36 reads "mean time to repair/reprovision"). Flagged under §2 below as a defect since it renders as a nonsense phrase in the fenced code.

---

## (2) Math verification

Every boxed formula/table claim was recomputed by hand and cross-checked against the executed code output. Verified **correct** (exact):

**index.md**
- L44 max order notional: `150 × 200 = 30,000 ≤ 100,000`. ✓
- L45 price collar: `(160.00−150.05)/150.05 = 6.631% > 3% ⇒ REJECT`. ✓ (matches 04 output `6.63%`.)
- L46 gross exposure: `1200·150 + 800·310 + 450·210 = 522,500 > 500,000` ⇒ `104.5%` BREACH. ✓
- L47 net exposure: `180,000 − 248,000 + 94,500 = 26,500` vs `200,000` = `13.2%`. ✓
- L49 daily loss: `14,500 / 25,000 = 58.0%`. ✓
- L50 drawdown: `1 − 1,930,000/2,000,000 = 0.0350` vs `0.0500` = `70.0%`. ✓
- L52 position break `b_i = q_int − q_ext`; TSLA `+50` REAL, AAPL `+200` = pending ⇒ TIMING (matches 05). ✓
- L53 cash residual `r = C_ext − (C_{−1} − ΣP_iq_i − fees + fin) = +0.00` MATCHED. ✓
- L54 availability `A = 720/(720+0.25) = 0.99965290`. ✓
- L55 `A_N = 1−(1−A)^N`, N=2 ⇒ `3799.44 ms/yr`. ✓ (exact: (0.25/720.25)²·8760·3600·1000 = 3799.44.)
- L56 common-cause floor `(1−A)[f+(1−f)(1−A)]`, f=50% ⇒ `1.521 h/yr`. ✓
- L58 canary exposure `Σ w_k h_k`: `(0.01+0.05+0.25)·0.5 = 0.155 h × $50,000 = $7,750` vs big-bang `$100,000`. ✓

**01** — `μ_net = μ − cV/10⁴`; `V* = 10⁴μ/c = 10⁴·0.12/6 = 200`. ✓ Table rows (50→3.00%/9.00%/1.50 … 1200→72.00%/−60.00%/−10.00) all reproduce. ✓ `Y_erased = ℓ/μ_net = 0.30/0.06 = 5.00`. ✓ §2.2 multiplicative-incident log-growth expression is the correct `E[logW] − ½Var` form. ✓

**02** — exposure-hours `E = ∫w dt`; canary `Σ w_k h_k`; abort index `k* = min{k : L·Σ w_jh_j ≥ Θ}`; per-deploy `p·L·E`, annual `p·N·L·E`. ✓ Code: canary cum `250→1,500→7,750` trips Θ=5,000 at t=1.5 h; big-bang `2.00 h·$50,000 = $100,000`; reduction `100,000/7,750 = 12.9×`; expected `0.2·100,000 = 20,000` vs `0.2·7,750 = 1,550`. ✓ Blue-green as `K=1` special case consistent. ✓

**03** — `E[FA] = n·p_k·M`, `p_k = 2(1−Φ(k))`. ✓ Code reproduces the fence exactly: k=2→393.12/metric/day ×100 = 39,312; k=3→2,332.6; k=4→54.7; k=5→0.5; k=6→0.0. ✓ EWMA `σ_z = σ_x√(λ/(2−λ))`, limit `= 20+3√(0.2/1.8) = 21.000`. ✓ Step response `Δ(1−(1−λ)^m)` and `m* = ln(1−(kσ_x/Δ)√(λ/(2−λ)))/ln(1−λ)` algebraically correct. ✓ Percentiles/ack-rate/break-count definitions correct. ✓

**04** — G1–G5 predicates correct, incl. **post-trade** postures in G4/G5 (`|q_i + sgn(side)·q| ≤ q̄_i`, `Σ|q_j+δ_jq|P_j ≤ G_max`). ✓ Token bucket `b_t = min(B, b_{t−1}+RΔt)` correct. ✓ Escalation ladder `α≈0.6/β≈0.4/γ≈2` matches code (`−0.6·cap`, `−0.4·cap`, `−1·cap`, `−2·cap`). ✓ Guard latency `0.25/2.00 µs = 12.5%`. ✓

**05** — `b_i = q_int − q_ext`; TIMING iff `b = P_i` (in-flight), else REAL. ✓ Cash expectation formula. ✓ `ρ` completed/attempted ratio; §2.4 `Δ_risk ~ σ√(D/T_yr)·Q·P` (sqrt-time), 15 min vs 60 min ⇒ `4×` blind-window cut. ✓ Code: AAPL +200 TIMING, MSFT 0 MATCHED, TSLA +50 REAL, cash residual +0.00, net +50 across 1 break. ✓

**06** — `A = MTBF/(MTBF+MTTR)`; nines (0.999→8.8 h, 0.9999→53 min, 0.99999→5.3 min). ✓ `A_N = 1−(1−A)^N`; common-cause `downtime_N ≈ (1−A)[f+(1−f)(1−A)^{N−1}]`. ✓ Quorum `2F+1`/`F+1` votes/tolerate `F`. ✓ Detection `E = τ/2 + h/2`, `τ = kh`; code `1.25 + 1.5 = 2.75 s`. ✓ Code reproduces all fence figures: `3.041 h`, `3799.44 ms`, `1.32 ms`, `0.305 h`, `1.521 h`. ✓ §3 prose `1,440×` (1.521 h ÷ 3.799 s = 1441) and `2×` (3.041/1.521 = 2.0) correct. ✓

### DEFECT A — token-bucket off-by-one (index.md line 51; also 04 line 146 comment)

- **File/line:** `index.md:51` (hub lookup "Rate | Token bucket"), reproduced in `04-risk-guards-and-kill-switches.md:146` code comment `# 3rd order in 0.1s -> bucket empties`.
- **Stated:** "3rd order in 0.1s empties a `B=4, R=4` bucket."
- **Correct:** with `B=R=4` starting at capacity, the first three orders at `t=0, 0.1, 0.1` leave the bucket at **3.0 → 2.4 → 1.40** tokens — the 3rd order is **approved**, not refused. The bucket first drops below the `1`-token approve threshold on the **4th** order (`0.40`), and the **5th** order is the first rejection. Confirmed both analytically and by the page's own executed code, whose fence shows all three orders `APPROVE`.
- **Impact:** medium-low — the ordering/claim intent ("a fast burst consumes the burst allowance and a sustained excess is throttled") is sound, but the specific countable claim is wrong by one and directly contradicts the executed output on the same page.

### DEFECT B — broken LaTeX operator (index.md line 57)

- **File/line:** `index.md:57` — verification cell `$100\times \times 6\text{bps} = 6.00\%$/yr`.
- **Stated:** duplicated operator `\times \times`, rendering as "100× × 6bps".
- **Correct:** single `\times` — `$100\times 6\text{bps} = 6.00\%$/yr`. The numeric result (6.00%/yr) is itself correct; only the rendered expression is malformed.

### DEFECT C — nonsensical word in code comment (06 line 86)

- **File/line:** `06-advanced-extensions.md:86` — `mtbf_h, mttr_h = 720.0, 0.25   # hours between failures, hours to repair/provoke`.
- **Stated:** "repair/provoke" (nonsense; the enumeration's meaning per L36 is "repair/reprovision"). **Correct:** "repair/reprovision". Cosmetic — no numeric or rendering impact beyond the comment text.

### Minor observation (not counted as an error)

- `03-monitoring-and-alerting.md:40` states a 10-second scrape "over a trading day is `n ≈ 8,640`". `86,400/10 = 8,640` is a full **24-hour** day; a ~6.5 h trading session would be ≈ 2,340. The linked code correctly computes `86,400/interval` (a calendar day), so only the word "trading day" is imprecise.

---

## (3) Code execution

All 7 `python` blocks were extracted, executed with `python3` (stdlib only), and diffed against their printed fences. **All 7 are byte-for-byte identical** to the shown output; all exit code 0; no stderr.

| Page | Block line | Result |
|---|---|---|
| index.md | 78 | MATCH |
| 01-from-zero-intuition.md | 68 | MATCH |
| 02-lifecycle-and-deployment.md | 67 | MATCH |
| 03-monitoring-and-alerting.md | 91 | MATCH |
| 04-risk-guards-and-kill-switches.md | 102 | MATCH |
| 05-failure-modes-and-practice.md | 95 | MATCH |
| 06-advanced-extensions.md | 84 | MATCH |

Every block is deterministic computation (no wall-clock/timing blocks; 02 and 04 simulate a clock with an explicit `t`, 03 seeds `random.seed(7)`), so exact match is the required standard and it holds. The one prose-vs-output discrepancy (Defect A, token bucket) is a *documentation* error, not a fence mismatch — the executor's output is self-consistent and correct on its own terms.

---

## (4) Coherence

- **Hub vs 01 prereq:** index L13 states the folder-level prereqs apply to `02`–`06` while `01` states its own smaller entry requirement; 01 L10 gives a single base prereq (`event-driven-backtesting-engines/01-from-zero-intuition`). Consistent.
- **Prereq chain:** 01←(backtesting 01); 02←01; 03←02; 04←03; 05←04; 06←05+concurrency. No cycles.
- **Hub "verified check" table vs sub-pages:** all reproduced values agree (gross 522,500; collar 6.63%; recon TSLA +50 / AAPL +200; availability 0.99965290 / 3799.44 ms / 1.521 h; canary $7,750 vs $100,000; incident drag 6.00%/yr) — **except** the token-bucket cell (Defect A), which is not reproduced by 04's execution.
- **Internal form** consistency: 04's ladder constants (α≈0.6/β≈0.4/γ≈2) match the code; 02 §2.2's false-abort arithmetic `2(1−Φ(k))` matches 03; 05 §2.4's `√D` and its §4 point #4 agree; 06's essence `A_N = 1−(1−A)^N` matches §2.1. No contradictions.
- **Links:** all 30 unique wikilinks resolve to existing targets (incl. the flat page `production-risk-guards-and-kill-switches` correctly referenced without `/index`). House format `[[full/path|Alias]]` used throughout; math delimiters `$…$`/`$$…$$` used correctly except Defect B.
- **Jargon:** "exposure-hours", "fencing token", "RTO/RPO", "common-cause floor", "silent failure", "break vs timing" introduced with definitions where needed; consistent across hub and sub-pages.

---

## Verdict

**FAIL** — 3 defects: (A) deterministic off-by-one in the hub token-bucket claim (index.md:51, echoed at 04:146), (B) malformed LaTeX `\times \times` (index.md:57), (C) nonsense word in a code comment (06:86). All 7 code blocks execute and match their fences byte-for-byte; all wikilinks resolve; no prose spelling errors and no other math errors found.

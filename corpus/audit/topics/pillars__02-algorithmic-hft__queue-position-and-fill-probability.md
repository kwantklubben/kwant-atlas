# Audit — content/pillars/02-algorithmic-hft/queue-position-and-fill-probability/

**Role:** sole adversarial reviewer.
**Scope:** 7 files (`index.md`, `01`–`06`). `content/_legacy/` ignored.
**Method:** (1) spelling/typo scan; (2) hand-verification of every boxed formula + worked example; (3) executed **all 7** ```python blocks in a fresh interpreter (numpy 2.5.3 in a throwaway venv) and diffed stdout against the output fence, each run twice for determinism; (4) coherence pass (hub↔01 prereq, jargon, wikilinks, cross-page contradictions).

**Verdict: PASS-WITH-NITS.** No formula is wrong; every boxed equation, closed form, and worked numeric example reproduces. All 7 output fences match their code except one cosmetic blank line. Findings are notation-coherence and prose-overstatement issues, not math errors.

---

## 1. Spelling / typos

None found. Name/prose scan clean (the only regex hit, "Thierry", is a person's name).

Style nit (not an error): the term is hyphenated inconsistently — `04` frontmatter tag uses `birth-death-process` and the title "Birth-Death" (ASCII hyphen) while the body uses `birth–death` (en dash) throughout. Cosmetic.

---

## 2. MATH — every boxed formula + worked example verified

All checks below were re-derived by hand and/or reproduced by the code.

### index.md
| Location | Claim | Verdict |
|---|---|---|
| §2 (idx:35) | `Filled(x,L,ξ)=(ξ−x)⁺−(ξ−x−L)⁺` | correct (CK fill function) |
| §2 table (idx:44) | cancel-ahead prob `x/Q`; 25/200 → 0.125 | 25/200 = 0.125 ✓ |
| §2 table (idx:46) | `NegBin(x,p)`, mean `x/μ`; q=10,p=0.05 → 200 ticks | 10/0.05 = 200 ✓ |
| §2 table (idx:47) | P(Bin(T,p)≥x); x=10,T=300 closed 0.9350 / MC 0.9336 | reproduced by block ✓ |
| §2 table (idx:48) | `dx/dt=−(μ+θx)`, `x(t)=(x₀+μ/θ)e^{−θt}−μ/θ`; t*=9.116 s | ODE solution verified (d/dt ⇒ −θx−μ = −(μ+θx) ✓); t*=50·ln(1.2)=9.116 ✓ |
| §2 table (idx:49) | cancel-only `x₀e^{−θt}`, halving 34.66 s | ln2/0.02 = 34.66 ✓ |
| §2 table (idx:50) | mid-up prob exact 0.2322 / MC 0.2324 at (10,5) | reproduced ✓ |
| §2 table (idx:51) | `ΔP=β·OFI/depth`; slope 0.005007 vs 1/200=0.005, R²=0.896 | reproduced ✓ |
| §2 table (idx:52) | E[ΔM|filled]<0; −$0.0119 vs +$0.0166 | reproduced ✓ |

### 01-from-zero-intuition.md
- `01:39` boxed `P(filled by T)=P(Bin(T,p)≥x)=Σ_{k=x}^T C(T,k)p^k(1−p)^{T−k}` — correct.
- `01:43` `E[time to fill]=x/μ` — correct (mean of NegBin(x,p)=x/p).
- `01:49` cancel-ahead `=x/Q` — correct.
- `01:55` `E[ΔM_T|filled]<0`, `E[ΔM_T|not filled]>0` — correct, and reproduced by the block.
- Worked example text (`01:121`): "position 10 … fill about half the time" (block: 0.5468) ✓; "filled orders … 2.38 ticks below … unfilled … 2.87 above" (block: −2.377 / +2.873) ✓.

### 02-the-order-queue.md
- `02:33` `Filled=(ξ−x)⁺−(ξ−x−L)⁺`; `02:35` unit-size ⇒ `1{ξ≥x}` — correct.
- `02:41` pro-rata `Fill_i=V·q_i/Σ_j q_j` — correct.
- `02:55` boxed `dx/dt=−(μ+θx)` ⇒ `x(t)=(x₀+μ/θ)e^{−θt}−μ/θ` — correct.
- `02:59` `t*=(1/θ)ln(1+θx₀/μ)` — correct (t*=9.116 s for x₀=50, μ=5, θ=0.02).
- `02:61` cancel-only `x₀e^{−θt}`, halving 34.66 s — correct.
- Block reproduces the whole fence (see §3 below for the one cosmetic diff). Mean-field table (8 s → x=5.64, MC P(fill)=0.1983) consistent with ODE.

### 03-fill-probability-models.md
- `03:29-30` NegBin pmf `P(τ_x=k)=C(k−1,x−1)p^x(1−p)^{k−x}` — correct.
- `03:32` `E=x/p`, `Var=x(1−p)/p²` — correct.
- `03:36` boxed `P(τ_x≤T)=P(Bin(T,p)≥x)=I_p(x,T−x+1)` — correct (standard regularised-incomplete-beta identity).
- `03:38` relative dispersion `sd/mean=√((1−p)/x)` — correct: `√(x(1−p))/p ÷ (x/p) = √((1−p)/x)`.
- `03:44` effective outflow `p+pc·x/Q` — correct.
- `03:52` boxed CK `E[filled]=∫[(ξ−Q)⁺−(ξ−Q−L)⁺]dF(ξ)` — correct (see notation note E1).
- `03:58` hazard definition — correct.
- Worked examples: closed-form vs MC agree to <0.003 (max diff 0.0025 at q=10) ✓; cancels lift P(fill) 0.0091→0.8989 at pc=0.10 (≈ hundredfold) ✓.
- NOTE: `03`'s block prints MC(q=10)=**0.9325** while `index.md:47` prints MC(q=10)=**0.9336** — **not a contradiction**: the two blocks iterate over different `q` tuples with the same seed 5, so the RNG stream diverges before q=10. Both fences match their own code.

### 04-queue-reactive-models.md
- `04:31` per-order cancel hazard θi (death rate `μ+θi`) — correct.
- `04:48-49` `P(up)=P(σ_A<σ_B)`, `P(down)=P(σ_B<σ_A)` — correct.
- `04:51` symmetric book ⇒ ½ by exchangeability; a>b ⇒ P(up)<½ — correct reasoning.
- Block: exact vs MC (5,5)=0.5000/0.5001, (10,5)=0.2322/0.2324, (5,10)=0.7678/0.7663, (15,8)=0.2349/0.2337 — all reproduced deterministically. Economics consistent (thin ask ⇒ up).
- `04:33` prose claim — see finding **E2** below.

### 05-failure-modes-and-practice.md
- `05:34` true-fill (ξ≥x) vs naive-fill — correct.
- `05:42` `P(picked off)≈1−e^{−ρℓ}`, `E[loss/fill]=P·Δp·size` — correct for small ℓ.
- `05:50` `E[ΔM_T|filled]=−AS<0` — correct.
- `05:54` `edge=½s − AS − fees/impact` — correct.
- `05:62` `x_new=fQ` — correct.
- Block: naive 1.0000 vs true 0.7939 (26% relative inflation) ✓; pick-off 0.0247→0.9933 ✓; refresh 500/2,500/4,500 ✓; E[P&L|filled]=−0.0119 / unfilled=+0.0166 ✓.

### 06-advanced-extensions.md
- `06:34` CK fill function — correct (notation note E1).
- `06:38-39` exponential-outflow closed form `E[(ξ−Q)⁺]=m·e^{−Q/m}`, `E[filled]=m(e^{−Q/m}−e^{−(Q+L)/m})` — correct; I re-derived analytically and it matches the MC rows exactly (Q=0→850.4, 500→719.7, 1000→608.8, 2000→436.4, 3000→312.5).
- `06:45` overbooking total `A(X,ξ)=M+Σ_k[(ξ_k−Q_k)⁺−(ξ_k−Q_k−L_k)⁺]` — correct.
- `06:57` OFI definition (signed bid-size change − signed ask-size change) — correct stylisation of CKS (2014).
- `06:61` boxed `ΔP_k=β·OFI_k/depth_k+ε_k` — correct.
- `06:100` concave proxy `λ(q)=log₂(1+q)`: 1→1.000, 5→2.585, 20→4.392, 100→6.658, 500→8.969 — all reproduced; increasing & concave ✓.
- Block reproduces OFI slope 0.005007 vs theory 0.005000, R²=0.896 ✓; overbooking non-execution 27.975%→7.355%→1.804%→0.470% ✓.

---

## 3. CODE — every ```python block executed

7 python blocks, one per file. All executed in a fresh subprocess; `random.seed(...)` set in every block.

| File | rc | deterministic | fence match |
|---|---|---|---|
| index.md | 0 | yes | ✅ identical |
| 01-from-zero-intuition.md | 0 | yes | ✅ identical |
| 02-the-order-queue.md | 0 | yes | ⚠️ **one blank line** (see E5) |
| 03-fill-probability-models.md | 0 | yes | ✅ identical |
| 04-queue-reactive-models.md | 0 | yes | ✅ identical |
| 05-failure-modes-and-practice.md | 0 | yes | ✅ identical |
| 06-advanced-extensions.md | 0 | yes | ✅ identical |

**Nondeterminism:** none observed — all 7 blocks produce byte-identical output across repeated runs (all RNG seeded; `np.linalg.solve` deterministic). Blocks in 04 and 06 require **numpy**; the other five are stdlib-only.

---

## 4. COHERENCE

- **Hub ↔ prereqs.** `index:11` declares folder prereqs = Probability Theory + Market Microstructure for pages 02–06, and states page 01 has "its own, smaller, entry requirements". `01:11` lists only Probability Theory. ✅ consistent, and the hub flags the deviation explicitly.
- **Wikilinks.** All 17 distinct wikilink targets resolve to files/folders in `content/`. No dangling links. ✅
- **Cross-page structure.** §1–§6 section scheme consistent across all 7 files; "Back / Forward / Base" bridges agree (index only lists all six sub-pages; `04`→`05`→`06` forward chain unbroken; every page links back to the hub). ✅
- **Sibling signposting** matches the folder's stated scope vs `optimal-execution-and-almgren-chriss` and `market-impact-and-depth`. ✅
- **Contradiction scan:** the only real issue is the **Q-notation clash** (E1). The `03` vs `index` MC(0.9325 vs 0.9336) difference is benign (different RNG consumption), not a contradiction.

---

## 5. Findings (ranked)

**E1 — Notation clash: `Q` means two different things. (medium, coherence)**
`index:31` defines `x` = orders ahead **and** `Q` = total depth at the price. But the CK fill function is written with `Q` as the queue *ahead* in three places: `03:50/52` ("for queue Q ahead"), `06:32/34` ("for queue Q ahead"), `06:45` (`Q_k` = "queues Q_k ahead"), and `index:108`. The hub's own boxed version of the same function (`index:35`) uses `x`. So the same symbol denotes "queue ahead" in the CK sections and "total depth" in the uniform-cancel sections (`01:49`, `02:23`, `03:44`, `05:62`). *Fix:* use `x` (or a distinct `Q_ahead`) consistently in the CK statements, or rename total depth.

**E2 — `04:33` stationary mean misstated. (low–medium, math prose)**
*Stated:* "the queue is **mean-reverting around μ/θ** in the cancel-dominated regime." *Correct:* for the CTST birth–death queue (birth λ, death μ+θi) the stationary mean solves λ=μ+θE[i] ⇒ `E[i]=(λ−μ)/θ`, not μ/θ. `μ/θ` is the floor of the *no-birth* trade+cancel process (`dx/dt=−(μ+θx)` in `02:48`). The prose conflates the two regimes.

**E3 — "agree to three decimals" overstated. (low)**
`04:124` ("agree to three decimals") and `index:60` ("matches simulation to 3 decimals"): of the four (a,b) rows, two fail at the third decimal — (5,10): exact 0.7678 vs MC 0.7663 (Δ0.0015), (15,8): 0.2349 vs 0.2337 (Δ0.0012). Agreement is to **two decimals** (within ~0.002). *Fix:* say "to ~2 decimals / within 0.002".

**E4 — `05:136` "roughly linearly in latency" contradicts its own model. (low)**
The code models `P=1−e^{−ρℓ}` (ρ=1/2 per ms), which is linear only for small ℓ — as `05:44` itself states. Over the quoted 0.05→10 ms range the loss is 0.025→0.993: a 200× latency increase yields only a ~40× loss (clearly saturating), so "roughly linearly" is wrong *for that range*. *Fix:* say "near-linear at low latency, saturating at high latency", or quote a small-ℓ range.

**E5 — `02` output fence has an extra blank line. (cosmetic)**
`02:110-111`: the fence shows a blank line between the `t*=9.116 s` line and the table header that the code does not print (the two `print` calls are adjacent). All **numeric** output matches exactly. Cosmetic only.

**E6 (nit) — `index:60` "Runs on numpy (and stdlib) only."**
The index's own block is stdlib-only (`random`, `math.comb`); numpy is needed only by pages 04 and 06. The sentence is about the folder but reads as if the shown block needs numpy.

---

## Summary

- **7 files, 7 python blocks executed, 0 math errors.**
- Every boxed formula (fill condition, NegBin curve, `I_p` identity, mean-field ODE + solution, `t*`, cancel-only decay, mid-move race, CK fill function, exponential closed form, overbooking total, OFI law) verified correct by hand and/or execution.
- All output fences match code except one blank line (E5). No nondeterminism.
- 6 findings, all notation/coherence/overstatement; none alter a number.

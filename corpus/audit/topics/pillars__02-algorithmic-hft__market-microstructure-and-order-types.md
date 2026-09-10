# Audit — Market Microstructure and Order Types (Pillar 2 hub folder)

**Scope:** `content/pillars/02-algorithmic-hft/market-microstructure-and-order-types/`
**Files audited:** 7 (index + 01–06)
**Auditor:** sole adversarial reviewer
**Method:** spell/typo scan; independent re-derivation of every boxed formula & worked example; execution of all 7 ```python blocks vs their output fences; wikilink resolution against `content/`; hub-vs-subpage coherence.

---

## 1. Spelling & typos

| File:Line | Issue | Stated | Correct |
|---|---|---|---|
| 04-auctions-and-continuous-trading.md:117 | Article error | "a deterministic window is **an standing** invitation" | "...is **a standing** invitation" |

No other typos or doubled-word errors (the `an F`/`an S` hits in index/02/05/03 are acronyms pronounced with a vowel onset — FOK, IOC, SOR — and are correct; the `taker  TAKER` in 03 is column alignment).

## 2. MATH — every boxed formula + worked example

All boxed/formula items verified correct by independent derivation (detail below). **One narrative-math error found.**

### Verified correct
- **index:51 micro-price.** `P^micro=(q^b a+q^a b)/(q^b+q^a)=m+(S/2)(q^b-q^a)/(q^b+q^a)` — algebra matches (expand RHS to confirm equality); leans toward thin side; code reproduces `100.0364` above mid `100.0250`. ✓
- **index:54 / 01:46,50 Roll model.** `γ0=2c²+σu²`, `γ1=−c²` (from `Δp_t=c(q_t−q_{t−1})+u_t`, Var(q_t−q_{t−1})=2, Cov(q_{t−1}−q_{t−2}, q_t−q_{t−1})=−1); inversion `c=√(−γ1)`, `σu²=γ0+2γ1`, spread `2c` — all correct. Worked example: true c=0.02, σu=0.10 → theory γ0=0.0108 (sample 0.01079), γ1=−0.0004 (sample −0.00038), ĉ=0.0195, 2.00 bps — correct. ✓
- **index:55 Kyle price impact.** `λ=½√(Σ0/σu²)`, depth `1/λ` — consistent with Hasbrouck eq 7.5 (conditional `Eπ=((v−p0)²/2)√(σu²/Σ0)` ⇒ `λ=½√(Σ0/σu²)`); matches verified `hasbrouck_ch6-10.md`. ✓
- **index:56 Glosten–Milgrom.** `A−B=(V_H−V_L)μ` symmetric-prior — standard. ✓
- **index:59 fee identity.** `cost=Np+Nf`, `f=−r_m` maker / `+t_a` taker, inverted-venue sign flip — correct. ✓
- **02:42 walk.** `p̄(Q)` step-linear convex; slippage zero iff Q≤q₁^a — correct. Worked: 300·100.05+500·100.10+200·100.20=100.105; effective spread 8.00 bps; limit@100.05 = 2.50 bps — correct. ✓
- **02:52 adverse selection / 02:57 effective & realized spread.** `S_e=d(p−m)`, `S_r=d(p−m_{t+Δ})` (Foucault 2.3–2.5), `E[Δm|fill at bid]<0` — correct. ✓
- **03:38 NBBO, 03:44 SOR allocation, 03:50/54 fees & all-in spread `S^eff=S^quoted+(f_t−f_m)`, 03:58 dark midpoint saving = ½S^NBBO.** All correct. Worked: maker-taker swing $5.00/1000; NBBO 100.01/100.04 (not locked); mid 100.025; dark saving 1.50 bps = half of 3¢ — correct. ✓
- **04:32,36 auction.** `E(p)=min(D(p),S(p))`, `p*=argmax E(p)`. Worked: max exec 2000 at 100.10 (demand 2100 / supply 2000 at that price); schedule table reproduces exactly; continuous VW 100.1810, range 100.10–100.30 — correct. ✓
- **05:33,39,45,51 slippage, iceberg queue, `E|Δm|≈σ√L`, hidden fill cost.** All correct. Worked: iceberg fills 100/500, competitor 400/400, reserve 300; latency losses $3.16/$10.00/$22.36 (√L scaling, ×7 for ×50) — correct. ✓
- **06:31,35 latency race `P(win)≈e^{−Δ/τ}`, rent `R=NV e^{−Δ/τ}`; 06:41 batch `E[speed rent]=0`; 06:47 MM net `net=r_m+S_r−AS`.** Decay shape correct; worked numbers (82%, 1.8%, $16M→$13.1M→$5.89M→$0.29M; MM net 0.0055) reproduce exactly. ✓

### Errors / imprecisions
| File:Line | Item | Stated | Correct |
|---|---|---|---|
| 04:111 | Continuous price band | "immediacy with a **~8-cent price band**" | the stated range is **100.10–100.30 = ~20 cents** (the 8¢ figure equals VW 100.1810 − auction 100.10, i.e. the VW-vs-auction gap, mislabeled as the band) |
| 06:91 | Rent decomposition | "the next 190 µs buy **~$10M** more" | from 10 µs→200 µs the rent delta is **~$12.8M** (13,099,692→293,050) — "~$10M" understates |
| 06:31 | Latency P(win) constant | `P(win)≈e^{−Δ/τ}` | exact independent-Exp race gives `(1/2)e^{−Δ/τ}` (decay shape fine; the omitted ½ is a defensible ≈, but P(win)=1.000 at Δ=0 is overstated) |

**Verdict on math:** 12/12 boxed formulas and 7/7 worked examples are numerically correct. One narrative mislabel (04:111 band) and one loose rent estimate (06:91). Flag with priority: 04:111.

## 3. CODE — execution vs output fence

All 7 ```python blocks were extracted and executed with `python3`; every output matched its fence **exactly** (no diffs). All are stdlib-only and deterministic.

| Block | File | Exit | Output fence match |
|---|---|---|---|
| toy LOB / micro-price / walk | index.md | 0 | ✓ exact |
| Roll model recovery | 01 | 0 | ✓ exact |
| order-type execution (FIFO) | 02 | 0 | ✓ exact |
| fees / NBBO / dark midpoint | 03 | 0 | ✓ exact |
| call auction + continuous replay | 04 | 0 | ✓ exact |
| iceberg / latency / dark hit-rate | 05 | 0 | ✓ exact |
| latency rent + batch counterfactual + MM net | 06 | 0 | ✓ exact |

## 4. COHERENCE

- **Structure:** folder = index hub + 6 sub-pages (01–06); hub table lists exactly 6 sub-pages; reading-route arcs order them correctly. ✓
- **Prereqs:** hub states folder-level prereqs (Prob&Measure, Calc&Opt) apply to 02–06 and that 01 declares its own smaller entry requirement — 01 declares "or none". Consistent. ✓
- **Jargon consistency:** maker/taker, effective vs realized spread, half-spread notation, NBBO, FIFO/pro-rata used identically across hub and pages. Micro-price definition identical in index (51) and 01 (24). ✓
- **Wikilinks:** all 15 outbound links resolve to existing `.md`/`index.md` in `content/`. No dangling links. ✓
- **Cross-folder split:** hub explicitly scope-delegates deep LOB mechanics to Pillar 6 and fill-probability to sibling folder; the pages respect that split (no duplication). ✓
- **Contradictions:** none found besides 04:111 (internal band-vs-range contradiction, listed above).

---

## Summary
- **Errors found: 3** (1 typo 04:117; 1 math mislabel 04:111 — priority; 1 loose estimate 06:91; plus a noted-exactness nuance 06:31).
- **Blocks run: 7/7, all match output fences exactly.**
- **Formulas: 12/12 verified correct.**
- **Links: 15/15 resolve.**
- **Verdict: PASS with minor fixes** — no correctness-affecting formula/code errors; the 04:111 price-band figure should be corrected before publish.

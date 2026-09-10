# Audit: foundations/stochastic-calculus/

**Auditor:** sole reviewer · **Date:** 2026-09-10
**Scope:** `content/foundations/stochastic-calculus/` — 7 files (index hub + 6 sub-pages).
**Sources cross-checked:** `corpus/verified/shreve1_*`, `shreve2_*`, `bjork_*`, `glasserman_*`.

## Verdict

**PASS with minor issues.** All mathematics is correct, every boxed formula and worked example re-derives cleanly, the Vasicek/CIR parameter-role mix-up flagged by a prior audit is **now resolved** (roles are consistent across prose, formulas, and code). All 7 code blocks run to completion and each reproduces its documented output fence **exactly**. Issues found are prose/typos, one code time-step inconsistency, one self-looping link, and two minor coherence nits. No math errors.

---

## Issues table

| file:line | problem | fix |
|---|---|---|
| `02-brownian-motion-and-martingales.md:90` | "Gerascope the step variance" — **typo/nonsense word** in prose. | Reword, e.g. "Mismatch the step variance" / "Mis-scale the step variance". |
| `03-ito-integral-and-doeblin.md:93` | "Is Your $\Delta$ predictable (adapted)" — mid-sentence capital "Your", awkward phrasing inside a failure-mode bullet. | Lowercase "your"; smooth the sentence (e.g. "Ensure $\Delta$ is predictable (adapted) — if it looks into the future…"). |
| `04-sdes-and-simulation.md:96` | **Code inconsistency (Milstein):** drift/diffusion use loop step `T/n` (=0.025) but the Milstein correction `0.25*s*s*dtl*(dw*dw - dtl)` uses `dtl` (=1/12 ≈ 0.0833). The `dtl` variable is a leftover from the Vasicek step above. The correction's variance scale and subtracted term are ~3.3× too large. Block still runs and its fence matches, but the term is mathematically off. | Replace with `0.25*s*s*(dw*dw - T/n)` using the same `T/n` as the drift. |
| `04-sdes-and-simulation.md:103–108` (fence) & §3(d) | §3 header claims "(d) shows Euler-CIR *can* go negative while Milstein stays nonnegative" — but the Feller condition here is satisfied (`2κθ=0.12 ≫ σ²=0.0004`), so **both** Euler and Milstein stay positive in the output (0.0457 vs 0.0404). The claimed demonstration is not actually shown. | Either lower the Feller condition (raise σ / drop κ·θ) so Euler visibly crosses below zero, or soften the prose claim to "illustrates the CIR scheme". |
| `index.md:135` | **Self-looping wikilink:** `[[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma (legacy page)]]` in the hub's own "Connected Graph Bridges / Foundational base" resolves to the *current* `index.md` itself, mislabeled "legacy page". | Remove the self-reference or point it at the real legacy target if one exists under a distinct path. |
| `index.md:12` vs `01-from-zero-intuition.md:10`, `index.md:139` | Coherence: hub note claims page 01 "states its own, smaller, entry requirements," and the reading route bills 01 as "no prior knowledge" — but `01` lists the **same** prerequisite (`Probability & Measure Theory`) as the folder level. Slight contradiction in the audience arc. | Either drop the prereq line on 01 (true "from zero") or soften the "smaller requirements / no prior knowledge" claims. |

---

## Math verified (all correct)

- **QV of BM** `[W,W](T)=T ⇒ (dW)²=dt`, increment variance `2Δt²`, LLN collapse. ✔
- **Exponential martingale** `Z(t)=e^{σW−½σ²t}`; first-passage Laplace `E e^{−ατ_m}=e^{−m√(2α)}`, `E τ_m=∞`; reflection principle. ✔
- **Itô integral** isometry `E[I²]=∫ E[Δ²]du`, QV `[I,I](t)=∫Δ²du`, martingale property. ✔
- **Itô–Doeblin** `df=f_t dt+f_x dX+½f_xx(dX)²`, `(dX)²=Δ²dt`; product rule. ✔
- **GBM** `S(t)=S₀e^{σW+(μ−½σ²)t}`, `E[S]=S₀e^{μt}`; `∫W dW=½W(T)²−½T`. ✔
- **Vasicek** (reversion `κ`, mean `θ`): mean `e^{−κt}R₀+θ(1−e^{−κt})`, variance `σ²/(2κ)(1−e^{−2κt})→σ²/(2κ)`; exact transition; **can go negative**. ✔
- **CIR**: expectation identical to Vasicek; variance→`θσ²/(2κ)`; **Feller `2κθ≥σ²`**; noncentral-χ² params `d=4κθ/σ²`, `c=σ²(1−e^{−κΔt})/(4κ)`, `λ=R_t e^{−κΔt}/c`. ✔
- **Vasicek/CIR parameter-role consistency:** re-verified — prose, formulas, and code all treat `κ`(alpha) as reversion speed and `θ`(b) as long-run mean. **Prior mix-up is resolved.** ✔
- **Girsanov** RN derivative `Z(t)=exp{−∫Θ dW −½∫Θ²du}`, market price of risk `Θ=(μ−r)/σ`, `d(DS)=σDS dW̃`. ✔
- **Martingale Representation** `M(t)=M(0)+∫Γ dW`; **Feynman–Kac** `F_t+μF_x+½σ²F_xx−rF=0`. ✔
- **FTAP / MPR system** `α_i−R=Σ σ_ij Θ_j`; completeness classification table; Björk meta-theorem `M vs R`. ✔
- Worked numerical checks (index §3, 04, 05, 06): MC vs BSM closed form `10.43/10.45`, discounted-stock martingale `=100.00`, hedge P&L `≈0.015` — all within Monte-Carlo noise. ✔

## Code stats

- Blocks found: **7** (one per file: index, 01, 02, 03, 04, 05, 06). All stdlib; no multiprocessing needed.
- Blocks run: **7** — all exit 0.
- **All 7 reproduce their documented output fences exactly** (checked line-by-line).
- 1 code defect found (`04:96` Milstein `dtl` vs `T/n`, see table) — runs but term is scaled wrong.

## Links

- 17 unique wikilink targets checked; **all resolve** (`black-scholes-merton/02,03,05`, `no-arbitrage-and-binomial`, `interest-rate-and-term-structure`, `advanced-volatility-heston-sabr`, `econometrics-and-timeseries`, `probability-and-measure-theory` all exist).
- 1 self-loop: `index.md:135` links to its own `index` (see table).
- In-folder chain 01→02→03→04→05→06 and hub↔subpage cross-links are coherent and resolve.

---

**Summary:** No math or factual errors. 6 minor issues (2 prose typos/awkwardness, 1 code time-step bug, 1 non-demonstrated demo claim, 1 self-looping link, 1 prereq-coherence nit). Vasicek/CIR parameter-role consistency confirmed fixed.

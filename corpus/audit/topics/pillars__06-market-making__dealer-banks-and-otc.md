# Audit — `content/pillars/06-market-making/dealer-banks-and-otc/`

Reviewer: adversarial, sole. Date: 2026-09-10. Scope: the 7 files in the folder. `content/_legacy/` ignored (does not exist in repo).

## Verdict: **FAIL**

Concrete mathematical errors in the formula-lookup hub and the model page — the folder's own (verified, matching) computational engine contradicts the boxed/prose formulas and its own quoted check values. Every code block runs and reproduces its documented output exactly (7/7), and every wikilink resolves (0 broken), but the math is not reliably "re-derived and verified exactly" as claimed.

Files checked: 7. Blocks run: 7 (all matched documented output). Broken links: 0.

---

## 1. Code audit — all 7 blocks run, all 7 match documented output ✓

| File | Block | Result |
|---|---|---|
| index.md §3 | DGP equilibrium engine | **match** (stdlib) |
| 01 §3 | OTC search allocation sim | **match** (numpy) |
| 02 §3 | CCP netting network | **match** (numpy) |
| 03 §3 | DGP equilibrium engine | **match** (stdlib) |
| 04 §3 | impact/reversal path | **match** (numpy) |
| 05 §3 | contagion cascade | **match** (numpy) |
| 06 §3 | netting vs clearing trade-off | **match** (numpy) |

No stdout diffs anywhere. The index/03 blocks are stdlib-only and ran under bare Python; the numpy blocks ran under the project py3.14 (site-packages numpy 2.5.3). Numbers reproduced exactly: e.g. index `A=18.315906 B=18.140204 P=18.206093 spread=0.175702`; 03 spread identity `0.1706099929 = 0.1706099929`; 06 `bilateral=49.72 vs cleared=7.00` at 2× shock.

## 2. Math audit — flagged errors

**E1 — index.md:40 — monopolist-spread formula does not match its own check value (wrong formula / dropped terms).**
Stated: `A-B = δ/(r+λu+λd+ρ(1-z))`, with check value `=0.219628 at ρ=0`.
For the stated parameters (`r=0.05, λu=1.0, λd=0.1, δ=1`), the formula at `ρ=0` gives `δ/(0.05+1.0+0.1)=1/1.15=0.869565`, **not `0.219628`**. The value `0.219628` comes from the full denominator `D = r+λd+2λμlo(1-q)+λu+2λμhn q+ρ(1-z)` (verified: `1/0.219628=4.553`), i.e. the formula shown omits the two `2λμ` search-mass terms that are present in the page's own `D` (line 38) and in its own code. Formula and quoted verification are mutually inconsistent.

**E2 — index.md:44 (related to E1) — heterogeneous-investor spread formula.**
Stated `A-B = zδ/(r+λu+λd+ρ(1-z))` (attributed to eq 19). At the page's parameters it gives `0.8/1.15=0.6957`, which is not the model spread the page's own code produces for any λ (max ≈0.397). Same dropped `2λμ·` terms. Unless eq (19) refers to a genuinely different (non-dealer) equilibrium, this is inconsistent with the rest of the lookup; the page does not flag any regime switch.

**E3 — 03:74 — monopolist spread is claimed "independent of the investor search intensity λ"; the folder's own code contradicts this.**
Page 03 states the z=1 spread "becomes `A-B=δ/(r+λu+λd+ρ(1-z))`, which is **independent of the investor search intensity λ**." Running the folder's own `dgp_prices` at `z=1, ρ=0` gives a spread that varies strongly with λ:
`λ=5 → 0.49647`, `λ=26 → 0.219628`, `λ=100 → 0.078510`, `λ=1000 → 0.009012`.
The claim is refuted by the very engine the folder marks "reproduced exactly." (The "increasing in ρ" half of the claim *is* reproduced.) E1/E3 are the same conceptual defect surfacing at two locations.

**E4 — 05:34 — search-failure limiting price is wrong.**
Stated: `P ≥ (1−δ)/r` and `lim_{λ,ρ→0} P = (1−δ)/r` ("the low-type holding value").
The folder's own closed form gives `lim P = 1/r − (δ/r)·[(1−q)r+λd]/(r+λd+λu)` — never `(1−δ)/r` for positive parameters (equality would require `−qr = λu`). Numerically (standard params, δ=1, r=0.05): the limit is **17.826**, not `(1−δ)/r = 0`. Verified by evaluating `P(λ,ρ)` down to `λ=1e-4, ρ=1e-5 → 17.826`. The inequality `P≥(1−δ)/r` happens to hold in the traded region but the stated *equality limit* is incorrect.

**E5 (minor, coherence) — 01:48 `H−L = δ/r` vs the equilibrium value.**
Page 01 derives `H−L=δ/r` (the frictionless bound) and page 01:60/index:39 both write `A−B = z(H−L)`. In the model the equilibrium gains are `H−L = δ/D` (follows from `A−B=z(H−L)` and `A−B=δz/D`), not `δ/r`. E.g. at the standard parameters `z(H−L)=0.1757` while `z·(δ/r)=16`. The "fundamental surplus = δ/r" is only the frictionless upper bound; the pages use it as an equality without noting the friction gap. Mild overstatement in a "from zero" page, but the cross-page mixing of `H−L` is inconsistent.

## 3. Prose / spelling / coherence

- **Spelling:** no misspellings found in prose. One diacritic inconsistency: the model author is spelled `Gârleanu` everywhere except the page-03 title ("Duffie–Garleanu–Pedersen", 03:2). Cosmetic.
- **Jargon first-use:** `RFQ` is expanded on first use (01:109 "RFQ (request-for-quote) platforms" and again 02:19). Types `lo/hn/ho/ln` are defined in the hub notation block (index:29). `D` common denominator defined (index:38). `M` (interdealer price) defined (01:56, 02:21). Adequate.
- **Robustness descriptions:** (03 Title, index, 01 :30/32/111 Stoll 1978) — consistent.
- **Coherence hub vs 01:** hub:11 says page 01 "states its own, smaller, entry requirements," but 01's only stated prerequisite (Inventory Mgmt & Quote Skewing, 01:10) equals the folder default; and 01:16 claims "no prior knowledge of dealer banks needed" while still listing Inventory Mgmt. Minor tension, not an error of substance.
- **Rendering:** 06:19 uses `(\S05)` — a literal backslash escape; the section symbol `§05` should be plain (this is prose in a bullet, not LaTeX/code). Cosmetic.

## 4. Link resolution

All wikilinks across the 7 files resolve to existing pages (verified against the full `content/` tree, 0 broken). This includes the deep sibling links into `adverse-selection-and-glosten-milgrom/03-*` and `inventory-management-and-quote-skewing/03-*`, and foundation links (`foundations/ergodicity-and-statistical-mechanics/index`, etc.).

## 5. Priority summary for fixes

1. (E1/E2) Fix the `δ/(r+λu+λd+ρ(1-z))` lookup formulas on index:40 and index:44 — either add the `2λμlo(1-q)+2λμhn q` denominator terms or relabel them as a distinct regime; make the formula equal its own check value 0.219628.
2. (E3) Correct/delete the "independent of λ" claim at 03:74.
3. (E4) Replace the wrong limit `lim P=(1−δ)/r` at 05:34 with the true closed-form limit (or drop the equality limit claim).
4. (Optional) 03:2 accent; 06:19 `\S05`; clarify `H−L=δ/r` as an upper bound on 01.
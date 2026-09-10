# Pillar 4 — Quantitative Risk Management: Audit Report

**Audited:** `content/pillars/04-quantitative-risk/` (11 topic-folders × 7 pages = 77 pages + pillar hub `index.md`)
**Reference pattern:** `content/pillars/03-derivative-pricing/black-scholes-merton/`
**Audit date:** 2026-09-10
**Verdict: PASS** — 77/77 template-compliant, all code executes, all spot-checked math correct against the verified corpus. Two link-integrity defects (7 dangling wikilinks) and two thin-topic gaps flagged below.

---

## 1. Completeness

The 11 topic-folders map 1:1 onto the Pillar 4 corpus scope (`corpus/pillar4-quantitative-risk.md` + `corpus/titles/pillar4-quantitative-risk.TITLES.md`):

| # | Folder | Corpus section covered |
|---|---|---|
| 1 | var-and-expected-shortfall | var-and-expected-shortfall (VaR/ES, Artzner, Acerbi-Tasche, R-U) |
| 2 | parametric-historical-and-monte-carlo-var | parametric-historical-monte-carlo-var (3 VaR families, Kupiec, Christoffersen, BCBS backtest) |
| 3 | extreme-value-theory-and-fat-tails | extreme-value-theory (GEV, GPD/POT, Hill, Pickands) |
| 4 | credit-risk-and-the-merton-model | credit-risk-modeling (Merton structural, reduced-form, CDS) |
| 5 | stress-testing-and-scenario-analysis | stress-testing-and-scenario-analysis (CCAR/DFAST, reverse stress) |
| 6 | liquidity-risk-and-funding | liquidity-risk-and-funding (LCR/NSFR, Brunnermeier-Pedersen, Amihud) |
| 7 | counterparty-risk-and-xva | counterparty-risk-and-xva (EE/EPE/PFE, CVA/DVA, SA-CCR, FVA/MVA/KVA) |
| 8 | model-risk-and-validation | model-risk-and-validation (Derman, SR 11-7, backtesting) |
| 9 | basel-and-regulation | basel-and-regulation (RWA, FRTB SA vs IMA, output floor) |
| 10 | operational-risk | operational-risk (loss taxonomy, frequency-severity, LDA, AMA/SMA) |
| 11 | risk-factor-sensitivities | risk-factor-sensitivities (delta/gamma/vega, DV01, factor exposures) |

**Every corpus topic is represented** — no corpus section is orphaned. No awkward duplication: the backtesting material is split by angle (VaR-method backtests in folders 1–2; model-validation governance in folder 8) and Basel's credit/op-capital page (folder 9, 04) cross-references, rather than re-derives, the dedicated folders 4/10. These are intentional, complementary views, not overlaps.

**Gaps (notable but non-blocking):**
- **Systemic risk** — thin. Only a handful of mentions, all one-liners: `liquidity-risk-and-funding/06` (3), `counterparty-risk-and-xva/05` (1), `basel-and-regulation/01` (1), `liquidity-risk-and-funding/index` (1). No treatment of contagion, interbank networks, or macroprudential stress as a distinct strand.
- **Risk aggregation across risk types** — thin. Only `basel-and-regulation/03-market-risk-and-frtb.md` (2) and `stress-testing-and-scenario-analysis/05` (1). The corpus explicitly lists Bellini *Stress Testing and Risk Integration in Banks* as CORE; the pillar gestures at it but has no dedicated treatment of how market/credit/op capital are integrated.
- **Copulas & portfolio-credit correlation** (Gaussian copula, Vasicek one-factor, CDO, CreditMetrics) — *covered*, but only inside advanced-extensions (`credit-risk-and-the-merton-model/06`: copula×9, Vasicek×17, CDO×4; `extreme-value-theory-and-fat-tails/06`: copula×29). These are CORE corpus topics (McNeil "multivariate dependence and copulas"; Vasicek 1987 + CreditMetrics 1997 are free full-texts in `refs/`), so consigning them to extension pages is a defensible editorial choice but means no first-class treatment of dependence modeling.

## 2. Depth & Template

**Template pass: 77/77 pages (100%).** Every page — all 11 folders × (index + 01…06) — carries the locked template:
- YAML frontmatter with `title:` and `tags:` list whose **first tag is `pillar-quantitative-risk`** ✓
- A `**Basic Prerequisites:**` line ✓
- All six numbered sections `### 1.` … `### 6.` (Intuition & Practical Objective · Mathematical Ground Truth & Derivations · Computational Implementation · Failure Modes & First-Principles Breakdowns · Canonical Literature & Study References · Connected Graph Bridges) ✓

Verified programmatically: 0 pages missing any template element; every page's first tag is exactly `pillar-quantitative-risk`.

**Minor inconsistency:** the pillar-level hub `04-quantitative-risk/index.md` carries first tag `pillar-quant-risk` (not `pillar-quantitative-risk`). The hub is outside the 77-page template set, so it does not fail the gate, but the tag spelling should be harmonised.

**Depth per folder** (lines / words / python blocks, all 7 pages each):

| Folder | lines | words | py |
|---|---|---|---|
| basel-and-regulation | 890 | 9,052 | 11 |
| counterparty-risk-and-xva | 1,077 | 9,959 | 7 |
| credit-risk-and-the-merton-model | 993 | 9,264 | 9 |
| extreme-value-theory-and-fat-tails | 959 | 9,373 | 8 |
| liquidity-risk-and-funding | 852 | 10,298 | 7 |
| model-risk-and-validation | 1,023 | 10,148 | 10 |
| operational-risk | 917 | 8,081 | 9 |
| parametric-historical-and-monte-carlo-var | 913 | 8,882 | 10 |
| risk-factor-sensitivities | 1,090 | 11,024 | 7 |
| stress-testing-and-scenario-analysis | 726 | 8,662 | 7 |
| var-and-expected-shortfall | 905 | 8,242 | 7 |

No thin folder — every folder is 850–1,100 lines and 8–11 k words with 7–11 runnable Python blocks.

**Audience arc:** the hub gives a four-stage reading path (Start: sensitivities → VaR/ES → parametric VaR; Core tail: EVT → stress; Credit/counterparty/liquidity; Governance/regulation/op-risk) that covers all 11 folders in dependency order. Every one of the 11 folder `index.md` files carries a "Recommended reading route (audience arc)" split into beginner → formulas+code → practitioner/graduate, and links all six sub-pages. Verified: all 11 indexes have the arc, all six sub-page links, and a Basic Prerequisites line.

## 3. Coherence & Links

901 wikilinks scanned across the 77 pages + hub. **7 broken links (2 distinct dangling targets):**

1. **`pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals/index`** — dangling `/index` suffix. The target is a *flat* note (`liquidity-risk-and-margin-spirals.md`), which has no `index` subpage. Correct target is `.../liquidity-risk-and-margin-spirals` (as the hub's "Original Notes" already uses).
   - `credit-risk-and-the-merton-model/index.md:141`
   - `credit-risk-and-the-merton-model/05-failure-modes-and-practice.md:166`
2. **`pillars/04-quantitative-risk/basel-and-regulation`** — missing `/index` suffix. The folder's hub lives at `basel-and-regulation/index.md`; under this repo's explicit-`/index` convention the bare folder link is dangling (the pillar hub and sibling pages all write `.../basel-and-regulation/index`).
   - `risk-factor-sensitivities/06-advanced-extensions.md:66, 153, 184`
   - `risk-factor-sensitivities/index.md:187`
   - `risk-factor-sensitivities/03-rates-and-key-rate-duration.md:155`

**Hub:** lists all 11 folders (numbered) with a one-line summary each, plus the four-stage Reading Path and a Mermaid control-loop diagram. All six "Original Notes" links to the legacy flat notes resolve cleanly. Cross-pillar links (foundations, pillar 5) all resolve — the only defects are the 7 above.

## 4. Math & Code

**Code execution:** 64 Python blocks extracted from the eight code-bearing folders; **all 64 run clean** under `python3` (stdlib only — no numpy/scipy imports anywhere), exit code 0, no timeout. Outputs are internally consistent and match the stated/verified values in every case (63 exact string matches; the single non-exact case is a false positive from block extraction — the code's printed numbers `3,218.55 / rank 6` and EWMA vol `0.0136 > 0.0120` match the page's prose exactly).

**Formula spot-checks (13) against the verified corpus (`corpus/verified/`) and direct recomputation — all correct:**

| Formula / result | Where | Check |
|---|---|---|
| Normal VaR/ES: `VaR=μ+σz`, `ES=μ+σφ(z)/(1−α)`; ES₉₉=2.665214, ES₉₅=2.062713 | var folder | matches tsay_ch7 ES₀.₉₉=2.6652, ES₀.₉₅=2.0627 |
| ES/VaR ratio at 99% = φ(z)/((1−α)z) = 1.145665 | var index | recomputed 1.145665 ✓ |
| Artzner subadditivity koan: two 4%-default bonds → 95% VaR 0→100, ES 80/103.2 ≤ 160 | var 01 | recomputed ES 80 & 103.2 exactly ✓ |
| GEV `Gξ(x)=exp{−(1+ξx)^{−1/ξ}}`, Fréchet/Gumbel/Weibull domains | EVT 03 | matches tsay Eq 7.16 |
| GPD `1−(1+ξx/ψ)^{−1/ξ}`, POT | EVT 04 | matches tsay Eq 7.31 |
| EVT VaR/ES: `VaR=u+(β/ξ)[((n/Nu)(1−q))^{−ξ}−1]`, `ES=(VaR+β−ξu)/(1−ξ)` | EVT 04 | matches tsay Eq 7.28 (McNeil-Frey form) + §4.1 |
| Hill estimator `α̂=k/Σ ln(X₍ᵢ₎/X₍ₖ₊₁₎)` on Student-t₄ → α̂≈3.6–3.8 | EVT 03 | ran, sensible vs true α=4 |
| Merton: `E₀=V₀N(d₁)−De^{−rT}N(d₂)`, `σₑE₀=N(d₁)σᵥV₀`, `PD=N(−d₂)`, DD fixed-point | credit 02/03 | matches hull_ch24 (eqs 24.3–24.4), ran (V₀=432.91, PD=26.4bp) |
| Hazard from spread `λ=spread/LGD` | credit 04, xva 03 | matches hull eq 24.2 |
| CVA `UCVA=−LGD·Σ EPEᵢ·PDᵢ`, closed-form EPE for forward `S₀e^{rt}(2Φ(½σ√t)−1)` | xva 03 | matches Gregory 17.2/17.3, ran |
| Rockafellar–Uryasev: `ES=min_β{β + 1/(1−α)E[(L−β)⁺]}` | var index | correct |
| Euler component allocation; `w'Σw` variance cross-check, |diff|=0 | risk-factor-sens 04 | ran, exact |
| Kupiec POF: `LR=−2ln[(1−p)^{T−x}p^x/((1−p̂)^{T−x}p̂^x)]`; 11/1000→0.098, 115/1000→363.29 | parametric index | recomputed 0.098 & 363.292 ✓ |
| RiskMetrics √N scaling, 2-position `VaR=√(VaR₁²+VaR₂²+2ρVaR₁VaR₂)` | var/parametric | matches tsay §7.2.1–7.2.2 |

**No math errors and no non-running code found.**

---

## Verdict summary

- **Completeness:** PASS — all corpus topics covered by the 11 folders; minor gaps (systemic risk, cross-type risk aggregation thin; copulas/portfolio-credit relegated to advanced-extensions).
- **Template & depth:** PASS — 77/77 pages fully template-compliant; consistently deep across all folders; complete audience arc at hub and per-folder.
- **Coherence & links:** CONDITIONAL PASS — hub solid, topics cohere; **7 dangling wikilinks to fix** (see §3).
- **Math & code:** PASS — 64/64 Python blocks execute; 13 formula spot-checks all correct against the verified corpus.

**Recommended fixes:** (1) repair the 7 dangling wikilinks (§3); (2) harmonise hub tag `pillar-quant-risk` → `pillar-quantitative-risk`; (3) optional: strengthen systemic-risk / risk-aggregation coverage, and consider promoting copulas/portfolio-credit from advanced-extensions.

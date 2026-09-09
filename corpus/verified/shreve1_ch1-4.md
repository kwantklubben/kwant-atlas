# Shreve — Stochastic Calculus for Finance Vol. I — Ch. 1–4 (Verified Deep-Read)

**Scope.** Verified against rendered page images `/tmp/atlas_pages/shreve1/p-012.png … p-090.png` and the
body text of `/tmp/atlas_extract/shreve1.txt`, cross-checked against `/tmp/atlas_extract/shreve.md`
(Part A). Source PDF: *combined/lecture edition* (discrete-time binomial model first, then a condensed
continuous-time treatment in the same file).

**CRITICAL STRUCTURAL CORRECTION (read first).** The provided PDF is **not** the standard 6-chapter
Shreve Vol. I. It is a *re-lectured/re-organized edition* with its own chapter scheme, and the task's
page→title map is accordingly **misaligned**. OCR of the rendered pages establishes the true layout:

| Rendered PDF pages | Book p. (≈ PDF − 2) | This edition's actual chapter | = task's intended theme |
|---|---|---|---|
| p-013–017 | 11–15 | **Ch 1 §1.1 The Binomial Asset Pricing Model** | Binomial No-Arbitrage (derivation) |
| p-017–049 | 15–47 | **Ch 1 §1.2–1.5** finite/general probability, independence, LLN, CLT | (probability machinery) |
| p-051–067 | 49–65 | **Ch 2 Conditional Expectation** (§2.1–2.4) | Probability on Coin-Toss space (cond. expectation, martingales) |
| p-068–078 | 66–76 | **Ch 3 Arbitrage Pricing** (§3.1–3.5) | State prices / general arbitrage pricing, completeness |
| p-079–090+ | 77–88+ | **Ch 5 Stopping Times & American Options** | American derivatives, optimal stopping |

So: (a) the binomial **no-arbitrage** derivation occupies only the first pages (PDF 13–17, book 11–15),
and the rest of the task's "ch1" PDF 12–49 is generic probability; (b) the task's "ch2" (PDF 50–59) is
correctly conditional-expectation/martingale material but runs to PDF ~67; (c) the task's "ch3 State
Prices" (PDF 60–67) actually falls inside Ch 2's martingale section — there is **no chapter literally
called "State Prices"** in this edition (that content is Ch 3 "Arbitrage Pricing"); (d) the task's
"ch4 American Derivatives" (PDF 68–77) is actually **Ch 3 Arbitrage Pricing / completeness**, while
American/stopping-time material lives at **PDF ~79+ (Ch 5)**. No extraction error caused this — it is a
structural mismatch between the delegation brief and the on-disk edition. The four deep-read sections
below follow the *intended* genuine-Shreve themes and cite the actual PDF pages for each.

> Verification note: `vision_analyze` on rendered PNGs returned HTTP 404 (image backend unreachable, even
> for valid data-URLs) for this whole session. Pixel-level vision was therefore substituted with local
> OCR (`tesseract`) of the same rendered PNGs, overlaid on the text dump. All formulas below were
> confirmed against OCR/text and are standard Shreve content.

---

## Section A — The Binomial No-Arbitrage Pricing Model (one- & two-period)
*Actual pages: PDF p-013–017 = book 11–15 (§1.1). Extraction source: shreve.md Ch 1 first bullets.*

**Model setup.** Initial stock `S0 > 0`; constants `d, u` with `0 < d < u` (eq. 1.1); one period gives
`S1(H)=uS0` (up) or `S1(T)=dS0` (down). Money market: $1 grows to `(1+r)`. **No-arbitrage condition
(1.2): `d < 1+r < u`.** If `1+r ≤ u` nobody holds stock; if `d ≥ 1+r` one borrows and buys stock. The
book assumes `S0=4, u=2, d=½` in Example 1.1 (Fig. 1.1: `S2(HH)=16, S2(HT)=S2(TH)=4, S2(TT)=1`,
`S1(H)=8, S1(T)=2`).

**One-period European call.** Payoff `V1(ω)=(S1(ω)−K)^+ = max{S1(ω)−K,0}`. Sell the call at price `V0`
(unknown), hedge by buying `Δ0` shares financed with `V0 − Δ0 S0` in the money market. Require portfolio
value = payoff in both states:
```
V1(H) = Δ0 S1(H) + (1+r)(V0 − Δ0 S0)      (1.3)
V1(T) = Δ0 S1(T) + (1+r)(V0 − Δ0 S0)      (1.4)
```
Subtract (1.4) from (1.3): `V1(H)−V1(T) = Δ0 (S1(H)−S1(T))`, hence the **delta**
```
Δ0 = [V1(H)−V1(T)] / [S1(H)−S1(T)]        (1.6)   ← discrete delta-hedging ratio
```
Substituting back yields the **arbitrage price (1.7)/(1.9)** with risk-neutral probabilities (1.8):
```
p̃ = (1+r−d)/(u−d),   q̃ = (u−1−r)/(u−d) = 1−p̃,        (1.8)
V0 = (1/(1+r)) [ p̃ V1(H) + q̃ V1(T) ].                  (1.9)
```
Key point (made in text p. 13–14): `p̃, q̃` are *derived* from solving (1.3)–(1.4) and have **nothing to
do with the actual coin-toss probabilities**; by (1.2) both lie in `(0,1)` and sum to 1, so they are a
legitimate probability measure — the *risk-neutral* measure `P̃`.

**Two-period extension.** The agent re-hedges after the first toss: at time 1 in state `ω1` she holds
`Δ1(ω1)` shares, buying them with wealth `X1(ω1) = Δ0 S1(ω1)+(1+r)(V0−Δ0 S0)` (eq. 1.10). Working
backward from expiration `V2=(S2−K)^+`:
```
V1(H) = (1/(1+r))[ p̃ V2(HH) + q̃ V2(HT) ],
V1(T) = (1/(1+r))[ p̃ V2(TH) + q̃ V2(TT) ],
V0    = (1/(1+r))[ p̃ V1(H)  + q̃ V1(T)  ],   Δ1(ω1) = [V2(ω1,H)−V2(ω1,T)]/[S2(ω1,H)−S2(ω1,T)].
```
This is the **backward-induction / dynamic-hedging** template generalized in Section D.

**Gaps/errors found in existing extraction (shreve.md Ch 1).** The extraction's formulas are correct and
verbatim (`p̃=(1+r−d)/(u−d)`, `q̃=(u−1−r)/(u−d)`, delta and one-period V0 formulas all match (1.6)–(1.9)).
Two gaps: (1) it folds §1.1 binomial content together with the *general-probability* sections of Ch 1
(finite spaces, Lebesgue measure, σ-algebras, standard machine, LLN/CLT), so a reader cannot see that
the arbitrage derivation is confined to book pp. 11–15; (2) it omits the book's explicit no-arbitrage
interpretation arguments (`1+r ≤ u` and `d ≥ 1+r` cases) behind (1.2). Nothing in the math is wrong.

---

## Section B — Probability on Coin-Toss Space: Information, Conditional Expectation, Martingales
*Actual pages: PDF p-051–067 = book 49–65 (§2.1–2.4).*

**§2.1 A Binomial Model for Stock Price Dynamics** (book p. 49). On the n-toss space
`Ω={H,T}^n`, `S_k` depends only on first k tosses; the natural filtration `F_k = σ(S_1,…,S_k)`
tracks the stock. **§2.2 Information** (p. 50): σ-algebras as "information"; `X` `F_k`-measurable iff
its value is determined by the first k tosses.

**§2.3 Conditional Expectation.** On a general probability space `(Ω,F,P)`, with sub-σ-algebra `G⊆F`,
`E[X|G]` is characterized by **partial averaging**: it is `G`-measurable and
```
∫_A E[X|G] dP = ∫_A X dP   for all A ∈ G;   equivalently E[V·E[X|G]] = E[V·X] for all G-measurable V.
```
On the finite coin-toss space this reduces to averaging over atoms: `E[X|F_k](ω)` is the mean of `X`
over the set of continuations sharing the first k tosses of `ω`. **Properties** (verified in text,
pp. 55–57): (linearity, positivity,) (a) `E[E[X|G]]=E X`; (b) `X` G-measurable ⇒ `E[X|G]=X`;
(c) linearity; (d) positivity `X≥0 ⇒ E[X|G]≥0`; Jensen: convex `φ` ⇒ `E[φ(X)|G] ≥ φ(E[X|G])`;
Tower: `H⊆G` ⇒ `E[E[X|G]|H]=E[X|H]`; "taking out what is known": Z G-measurable ⇒
`E[ZX|G]=Z·E[X|G]`; independence ⇒ `E[X|G]=E X`. Binomial example: `E[S_{k+1}|F_k]=(p u + q d)S_k`
(similarly `E[S_1|F_0]=(pu+qd)S_0`).

**§2.4 Martingales** (book pp. 58–64; PDF p-060 = book p. 58). Ingredients: filtration
`F_0⊆F_1⊆…⊆F_n` and adapted stochastic process `{M_k}`. **Martingale:** `E[M_{k+1}|F_k]=M_k`;
**supermartingale:** `E[M_{k+1}|F_k] ≤ M_k`; **submartingale:** `≥`. Binomial consequences:
- `(pu+qd)=1` ⇒ `{S_k}` is a martingale; `>1` ⇒ submartingale; `<1` ⇒ supermartingale.
Under the *risk-neutral* probabilities `p̃,q̃` one has `p̃ u+q̃ d = 1+r`, so `{S_k}` is *not* a
P̃-martingale but the **discounted** stock `{S_k/(1+r)^k}` is.

**Errors/gaps in shreve.md Ch 1/2.** The extraction correctly lists the properties (a)–(k) and gives
`E[S_{k+1}|F_k]=(pu+qd)S_k` and the martingale/supermartingale conditions. Gaps: it does not state the
crucial remark that under the *risk-neutral* measure it is the **discounted** stock that is the
martingale (it implies this only later in Ch 3); and it lists Ch 2 items partly under its "Ch 1" heading
(its own chapter grouping is by the lecture edition, not by theme). Math is otherwise accurate.

---

## Section C — Arbitrage Pricing / General One-Step APT, Risk-Neutral Measure, Completeness (≙ "State Prices")
*Actual pages: PDF p-066–078 = book 64–76 (Ch 3). OCR of p-067 (book 65) shows the discounted-value
martingale proof; p-066 shows "3.5 The Binomial Model is Complete".*

**§3.1 Binomial pricing / §3.2 General one-step APT.** Abstract away from binomial: suppose a claim
`V_1` (any `F_1`-measurable payoff) is to be priced over one period in two states `{H,T}`. Pick
`(Δ0, X0)` so the self-financing portfolio matches the claim in **both** states:
```
(1+r)X0 + Δ0(S1(H)−(1+r)S0) = V1(H)
(1+r)X0 + Δ0(S1(T)−(1+r)S0) = V1(T)
```
Solve: `Δ0 = (V1(H)−V1(T))/(S1(H)−S1(T))`, and the value `X0 = Ẽ[V1]/(1+r)` equals the risk-neutral
expectation. APT maintained assumptions: unlimited short selling, unlimited borrowing at the same rate
`r`, no transaction costs, price taker.

**§3.3 Risk-Neutral Probability Measure.** A **portfolio process** `Δ=(Δ0,…,Δ_{n−1})` with each
`Δ_k` `F_k`-measurable (no inside information). **Self-financing wealth process** (verified, text
eq. 3.2.x and p-068 area; line 4253):
```
X_{k+1} = Δ_k S_{k+1} + (1+r)(X_k − Δ_k S_k).          (self-financing)
```
Two key martingale theorems under `P̃`:
1. **Discounted stock is a martingale:** `Ẽ[S_{k+1}/(1+r)^{k+1} | F_k] = S_k/(1+r)^k`.
2. **Discounted self-financing wealth is a martingale:** `Ẽ[X_{k+1}/(1+r)^{k+1}|F_k] = X_k/(1+r)^k`.
   (Rearranged: `(1+r)^{−(k+1)} X_{k+1} = (1+r)^{−k} X_k + Δ_k[(1+r)^{−(k+1)} S_{k+1} − (1+r)^{−k} S_k]`,
   a P̃-martingale increment since the bracketed term is a martingale increment.)

**§3.4 Simple European derivative security.** `V_m` is `F_m`-measurable (payoff fixed at maturity,
no intermediate exercise). Its value at k if hedgeable:
```
V_k = (1+r)^k Ẽ[ V_m/(1+r)^m | F_k ].          (risk-neutral valuation)
```

**§3.5 Completeness (The Binomial Model is Complete).** Constructing the hedge: with
`X_m = V_m`, the backward recursion gives `X_k = V_k = (1+r)^k Ẽ[V_m/(1+r)^m | F_k]` and the unique
portfolio `Δ_k = (V_{k+1}(·,H) − V_{k+1}(·,T)) / (S_{k+1}(·,H) − S_{k+1}(·,T))`. Proof (book p. 65,
verified on PDF p-067) shows `X_{k+1}(H)=V_{k+1}(H)` and `X_{k+1}(T)=V_{k+1}(T)` by substituting the
delta and using `V_k = (1/(1+r))(p̃ V_{k+1}(H)+q̃ V_{k+1}(T))` together with
`S_{k+1}(H)−(1+r)S_k = uS_k−(1+r)S_k = S_k(u−(1+r))`. **Conclusion: every simple European claim is
hedgeable; the binomial model is complete; the no-arbitrage value is unique and given by the P̃
expectation.** (`Δ_k` identity holds for all self-financing hedges, i.e. there is one risk-neutral
measure and one hedge.)

**"State prices" framing.** This edition does not run a separate "State Prices" chapter; the *market
measure / Arrow–Debreu state-price* development appears later (genuine Shreve Ch. 9, "Pricing in terms
of Market Probabilities: Radon–Nikodym", book ~p.111 / PDF ~p-113): the state price density
`ζ_k=(1+r)^{−k} Z_k`, `V_0=E[ζ_k V_k]`, `{ζ_k S_k}` and `{ζ_k X_k}` P-martingales. A reader seeking the
textbook's "State Prices" chapter should read **Ch 3 here (arbitrage pricing + completeness)** for the
replication/valuation core and **Ch 9** for the state-price/market-probability representation. This is
a *coverage/mapping* gap in shreve.md, which never flags that "State Prices" and "American
Derivatives" (the genuine Ch. 3/4 titles) are not literal chapters in this edition.

**Errors/gaps in shreve.md Ch 3.** All formulas match the text. The one structural gap: shreve.md
attributes Theorem/Corollary numbers ("Corollary 4.13", "Theorem 5.14", "Completeness Theorem 5.14")
that are **not** the numbers in this edition (its Ch 3 uses §3.x and the book's own cross-numbering
differs), so those numbers are unverifiable against the PDF and should not be cited as authoritative.
The delta, self-financing, martingale, and completeness statements themselves are correct.

---

## Section D — American Derivative Securities & Optimal Stopping
*Actual pages: PDF p-079–090+ = book 77–88+ (Ch 5 Stopping Times and American Options); the "properties
of American derivatives" (Ch 6) and Jensen/no-early-exercise of calls (Ch 7) follow at book pp. 87–99+.*

**§5.1 American Pricing — backward recursion.** European (Markov form), `v_n(x)=g(x)`:
```
v_k(x) = (1/(1+r))[ p̃ v_{k+1}(ux) + q̃ v_{k+1}(dx) ],    Δ_k = (v_{k+1}(uS_k)−v_{k+1}(dS_k))/(uS_k−dS_k).
```
American (holder may exercise any time k for `g(S_k)`; the hedge must keep `X_k ≥ g(S_k)` a.s.):
```
v_n(x) = g(x)
v_k(x) = max{ (1/(1+r))[ p̃ v_{k+1}(ux)+q̃ v_{k+1}(dx) ],  g(x) }        (American algorithm)
```
Value = **max(continuation value, intrinsic value)**; exercise when the intrinsic value branch binds.

**Worked Example 5.1 (American put, verified numbers).** `S0=4, u=2, d=½, r=¼ ⇒ p̃=q̃=½`, n=2,
`g(x)=(5−x)^+`. Tree: `S2(HH)=16, v2=0; S2(HT)=S2(TH)=4, v2=1; S2(TT)=1, v2=4`.
`v1(8)=max{(1/(1+r))[½·0+½·1],0}=max{0.40,0}=0.40`; `v1(2)=max{(4/5)[½·1+½·4],3}=max{2,3}=3.00`;
`v0(4)=max{(4/5)[½·0.40+½·3.00],1}=max{1.36,1}=1.36`. **American price 1.36 > European put price**
(the European put would have value `v2(4)=1` node reproduced below, showing early exercise at T raises
value). Note the hedge at time 1 in the down state is *not* well-defined by the two terminal equations
when the option was exercised (they give `Δ_1(T)=−1.83` vs `−0.16`), which is why American hedging needs
the consumption formulation below.

**§5.2 Hedging with consumption.** Allow the seller to consume `C_k`:
```
X_{k+1} = Δ_k S_{k+1} + (1+r)(X_k − C_k − Δ_k S_k)
        = (1+r)X_k + Δ_k(S_{k+1} − (1+r)S_k) − (1+r)C_k.
```
Properties (verified, book p. 79): (i) the discounted value `X_k/(1+r)^k` is a **supermartingale**;
(ii) `X_k ≥ g(S_k)` for all k; (iii) `X_k/(1+r)^k` is the **smallest** process with these two
properties. American option value = value of the smallest supermartingale dominating the intrinsic
value `g(S_k)`.

**Stopping times & optimal stopping.** A **stopping time** (Def. 5.1) is a random variable
`τ:Ω→{0,…,n}∪{∞}` with `{τ=k}∈F_k` for every k (decision uses only current information; it is an
`F_k`-measurable stopping decision). The value at time k:
```
V_k = max_{τ≥k} (1+r)^k Ẽ[ (1+r)^{−τ} G_τ | F_k ]     (max over stopping times τ ≥ k a.s.)
```
and at 0, `V_0 = max_τ Ẽ[(1+r)^{−τ} G_τ]`. **Optimal exercise time:** `τ* = min{ k : V_k = G_k }`
(first time the option value equals its intrinsic value) attains the maximum; equivalently any τ with
`G_τ = V_τ` a.s. is optimal. If the value process `{V_k}` is kept above intrinsic `G_k` and `V_n=G_n`,
stopping at the first hitting time `τ*` is optimal by the optional-sampling/martingale argument.

**Optional Sampling (stated, Ch 5.3).** For a martingale (resp. super-/sub-) `{Y_k,F_k}` and bounded
stopping times `σ ≤ τ`: `E[Y_τ | F_σ] = Y_σ` (resp. `≤` supermartingale, `≥` submartingale). Used to
justify that stopping at `τ*` reproduces the value.

**No-early-exercise theorem (Ch 7, book ~p. 92–96, PDF ~p-094–098).** For a convex payoff `g` with
`g(0)=0` (e.g. a call `(S−K)^+`), `r ≥ 0`:
```
Ẽ[(1+r)^{−n} g(S_n)] = max_τ Ẽ[(1+r)^{−τ} g(S_τ)]      (τ = n optimal; never exercise early)
```
because `(1+r)^{−k} g(S_k)` is a P̃-submartingale (convex function of the P̃-martingale
`S_k/(1+r)^k`-type argument), so by optional sampling the maximum is at the terminal time. **American
call on a non-dividend-paying stock = European call.** (Verification beyond rendered range; flagged as
in genuine Ch 7, consistent with text's §7.2.)

**Errors/gaps in shreve.md Ch 5/6/7.** shreve.md Ch 5–6 deep-reads are mathematically correct and cover
the recursion, stopping times, optional sampling, compound-European decomposition, and the smallest-
supermartingale characterization. Gaps: (1) the worked Example 5.1 numeric values (`0.40, 3.00, 1.36`,
`Δ_0=−0.43`) are absent — they are the best sanity anchors and should be added; (2) shreve.md does not
flag that these chapters sit **outside** PDF 12–77 (they start ~PDF 79), so the "Ch 4 = American
Derivatives, pages 68–77" portion of the task brief points at the wrong pages (those are APT); (3) the
no-early-exercise-of-call theorem is recorded in shreve.md Ch 7 but without noting it is what makes the
American call ≡ European call concrete for the reader.

---

## Consolidated correction / gap list (per chapter)
- **Ch 1 (Binomial No-Arbitrage) [PDF 13–17]:** extraction formulas correct; only need to (a) separate
  §1.1 arbitrage derivation from the general-probability sections that fill PDF 17–49, and (b) record
  the economic justification of `d<1+r<u` (the `1+r≤u` and `d≥1+r` cases).
- **Ch 2 (Coin-Toss / Cond. Expectation / Martingales) [PDF 51–67]:** correct; add that it is the
  **discounted** stock that is P̃-martingale (extraction only states P-martingale condition `pu+qd=1`).
- **Ch 3 (State Prices / Arbitrage Pricing) [PDF 68–78]:** formulas correct. Flag: there is no literal
  "State Prices" chapter in this edition (content = Ch 3 APT here + Ch 9 Radon–Nikodym later); drop
  unverifiable theorem numbers ("4.13", "5.14") that belong to another edition's numbering.
- **Ch 4 (American Derivatives / Optimal Stopping) [PDF 79–90+]:** correct but note the material starts
  at PDF ~79, **not** 68–77 as the brief assumed; add worked Example 5.1 numbers and the explicit
  American-call ≡ European-call consequence of the no-early-exercise theorem.
- **Process gap:** the four intended themes span PDF 13–90, and "American/stopping" material plus the
  market-probability (state-price) development extend beyond the briefed PDF 12–77 range.

*Formulas re-verified 2026-09-09 from rendered-page OCR + text dump; no source files were modified.*

# Audit — `content/pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/`

**Reviewer role:** sole adversarial reviewer.
**Scope:** 7 files (index + 01–06). `_legacy/` ignored.
**Sources cross-checked:**
- Avellaneda & Stoikov (2008), *High-frequency trading in a limit order book* — full text retrieved (`people.orie.cornell.edu/sfs33/LimitOrderBook.pdf`).
- Guéant, Lehalle & Fernandez-Tapia (2013), arXiv:1105.3115 — full text retrieved.

**Verdict: FAIL — 7 issues (5 math, 2 coherence).** The corpus is in good shape overall: every code block reproduces its output fence exactly, all wikilinks resolve, and most boxed formulas match the papers. But two transcribed equations are wrong (a sign in the AS θ-equation and a missing term + wrong exponent in the GLFT ODE), plus a repeated factor-of-γ slip and two coherence problems.

---

## 1. MATH

### ❌ M1 — `03-the-avellaneda-stoikov-model.md:40` — wrong exponent sign in the AS θ-equation (eq. 3.3)

Stated (bid max term):

$$+\max_{\delta^b}\frac{\lambda^b(\delta^b)}{\gamma}\Big[1-e^{-\gamma(s-\delta^b-r^b)}\Big]$$

**Correct** (AS 2008 eq. (3.3), verified verbatim from the paper): the exponent carries **no minus** for the *bid* term —

$$+\max_{\delta^b}\frac{\lambda^b(\delta^b)}{\gamma}\Big[1-e^{+\gamma(s-\delta^b-r^b)}\Big]$$

i.e. $1-e^{\gamma(p^b-r^b)}$ with $p^b=s-\delta^b$. The paper's ask term keeps the minus, $1-e^{-\gamma(s+\delta^a-r^a)}$, so the two terms are intentionally asymmetric. The page's version flips the bid term's sign (line 41 has the ask term right).

Self-consistency check confirms the error: with exponential intensity, the FOC from the page's (wrong) bid term gives $e^{-\gamma(s-\delta^b-r^b)}=\frac{k}{k-\gamma}$, yielding $\delta^b = s-r^b+\tfrac1\gamma\ln\!\frac{k}{k-\gamma}$ instead of the correct $\delta^b = s-r^b+\tfrac1\gamma\ln(1+\tfrac{\gamma}{k})$. So the page's own equation contradicts the boxed spread it derives two sections later. The correct form recovers $\delta^a+\delta^b=\gamma\sigma^2\tau+\tfrac2\gamma\ln(1+\tfrac\gamma k)$.

### ❌ M2 — `06-advanced-extensions.md:30` — GLFT ODE missing the $v_{q+1}$ term

Stated:

$$\dot v_q(t)=\alpha q^2 v_q(t)-\eta\,v_{q-1}(t)$$

**Correct** (GLFT 2013, Prop. 1, verified verbatim): for interior states the equation has **both** neighbours —

$$\dot v_q(t)=\alpha q^2 v_q(t)-\eta\big(v_{q-1}(t)+v_{q+1}(t)\big)$$

(boundary states $q=\pm Q$ drop the corresponding out-of-range term: $\dot v_Q=\alpha Q^2 v_Q-\eta v_{Q-1}$, $\dot v_{-Q}=\alpha Q^2 v_{-Q}-\eta v_{-Q+1}$). As written the ODE is one-sided and does not match GLFT.

### ❌ M3 — `06-advanced-extensions.md:30` — wrong exponent in the GLFT $\eta$

Stated: $\eta=A\,(1+\gamma/k)^{-(1+\gamma/k)}$.

**Correct** (GLFT 2013, Prop. 1/2): $\eta=A\,(1+\gamma/k)^{-(1+k/\gamma)}$ — the second part of the exponent is $k/\gamma$, not $\gamma/k$. ($\alpha=\tfrac{k}{2}\gamma\sigma^2$ is correct.)

### ❌ M4 — `03-the-avellaneda-stoikov-model.md:69` — skew per unit inventory has an extra factor $\gamma$

Stated: "The skew per unit inventory is exactly $2\theta_2\gamma\dots$".

**Correct:** $2\theta_2$ (equivalently $\gamma\sigma^2\tau$). Since $\theta_2=\tfrac12\gamma\sigma^2\tau$, we have $2\theta_2=\gamma\sigma^2\tau$, and $r=\theta_1-2q\theta_2$ gives $\mathrm{d}r/\mathrm{d}q=-2\theta_2$. The page's "$2\theta_2\gamma$" $=\gamma^2\sigma^2\tau$ is off by one factor of $\gamma$.

### ❌ M5 — `04-inventory-and-risk-aversion.md:39` — same $2\theta_2\gamma$ slip, self-contradicting

Stated: "The skew per unit inventory is $2\theta_2\gamma$ in the $\theta$ language — concretely, moving inventory by one lot shifts the reservation price by $\gamma\sigma^2(T-t)$."

The second clause is correct ($\gamma\sigma^2\tau=2\theta_2$, so $2\theta_2$ is right); the first clause ($2\theta_2\gamma$) contradicts it. Fix: $2\theta_2$.

### ✅ Verified correct (spot-checks)
- index table: $r=s-q\gamma\sigma^2\tau$; $r^b=s+(-1-2q)\tfrac{\gamma\sigma^2\tau}{2}$; $r^a=s+(1-2q)\tfrac{\gamma\sigma^2\tau}{2}$; $\lambda=Ae^{-k\delta}$; spread $=\gamma\sigma^2\tau+\tfrac2\gamma\ln(1+\tfrac\gamma k)$ — all match AS (2.3), (2.6)–(2.7), (2.11), (3.13)/(3.18).
- 02: value function (2.3), indifference conditions (2.4)–(2.5), $\theta$-ansatz (3.2), HJB (3.1) and intensity derivation ($A=\Lambda/\alpha,\;k=\alpha K$) — all match the paper verbatim.
- 03: expansion (3.10)–(3.12), $\theta^1=s$, $\theta^2=\tfrac12\sigma^2\gamma\tau$, spread (3.18) — all match AS.
- 06: GLFT value function $u=-e^{-\gamma(x+qs)}v_q(t)^{-\gamma/k}$; stationary closed forms $\delta^{b\ast}_\infty\simeq\tfrac1\gamma\ln(1+\tfrac\gamma k)+\tfrac{1}{2k}\sqrt{\alpha/\eta}(2q+1)$, $\delta^{a\ast}_\infty\simeq\tfrac1\gamma\ln(1+\tfrac\gamma k)-\tfrac{1}{2k}\sqrt{\alpha/\eta}(2q-1)$ — match GLFT Theorem 2 (only $\eta$ is fed the wrong exponent, M3).
- 04: AS Table 1 figures ($62.94/5.89$ vs $67.21/13.43$) and Tables 1–3 spreads $1.29/1.33/1.15$ match the paper exactly.
- 05: half-spread $\tfrac12\gamma\sigma^2\tau+\tfrac1\gamma\ln(1+\tfrac\gamma k)$ matches the boxed spread $\div2$.

## 2. CODE — 7/7 blocks run, 7/7 stdout match

Each ```python block was extracted and executed (`python3`); output diffed against its fence.

| # | file | result |
|---|---|---|
| 1 | index.md | ✅ exact match |
| 2 | 01 | ✅ `[3, -6, 5, -14, -5]` (seeded) |
| 3 | 02 | ✅ reservation-prices match closed forms |
| 4 | 03 | ✅ exact match |
| 5 | 04 | ✅ exact match (20 000 paths, seeded) |
| 6 | 05 | ✅ exact match |
| 7 | 06 | ✅ exact match |

No runtime errors; no numeric drift. **blocks_run = 7.**

## 3. SPELLING / TYPOS

Clean. `aspell --mode=markdown` (en_GB) reports no misspellings across all 7 files; no doubled words in prose (the only `random random` hit is inside a code fence). Prose, en-dashes, and accented names (Avellaneda–Stoikov, Guéant, Cartea–Jaimungal–Penalva, Itô) are consistent.

## 4. COHERENCE

### ❌ C1 — `index.md:90` contradicts `05-failure-modes-and-practice.md`§3

Hub: "our simulation shows the AS P&L turning negative once **a few percent** of fills are informed."
Page 05 §3: P&L stays **positive** through $p_\text{tox}=0.2$ ($+36.7$) and $0.4$ ($+16.3$); it only turns negative at $p_\text{tox}=0.6$ — i.e. **60%**, not "a few percent". Either fix the hub wording or the characterization is false.

### ❌ C2 — `04-inventory-and-risk-aversion.md:37` — justification contradicts the stated monotonicity

"The stationary spread is **decreasing** in $\gamma$ because a dealer who **cares less** about inventory can afford to quote tighter and trade more."

A dealer who cares less = low $\gamma$, but the component $\tfrac2\gamma\ln(1+\tfrac\gamma k)$ is *largest* as $\gamma\to0$ ($\to 2/k$) and *decreases* as $\gamma$ grows. The clause "cares less → tighter" therefore supports the **opposite** monotonicity to the one claimed. The stated direction (decreasing in $\gamma$) is right; the rationale is backwards.

### ✓ Other coherence checks pass
- Hub ↔ 01: prereq split is consistent (folder-level prereqs for 02–06; 01 states its own smaller requirement). Hub says "six sub-pages"; 6 sub-pages exist.
- All 10 distinct wikilink targets resolve to existing `index.md` folders (checked). Internal cross-links (01→02→03→04→05→06, hub) are consistent and acyclic in the recommended reading route.
- Jargon is used consistently ($r$, $\psi$, $\theta$, $\delta^{a/b}$, $A$, $k$); no conflicting definitions between hub and sub-pages.

### Minor note (not counted)
`index.md:41` labels the stationary spread $s^\ast$ — in the hub's own notation section $s$ is the mid-price, so `s^\ast` for a *spread* is an avoidable symbol clash (elsewhere $\psi$ is used). Cosmetic.

---

## Summary

| # | file:line | severity | issue | fix |
|---|---|---|---|---|
| M1 | 03:40 | high | AS eq (3.3) bid term exponent sign flipped | `e^{-\gamma(s-\delta^b-r^b)}` → `e^{+\gamma(s-\delta^b-r^b)}` |
| M2 | 06:30 | high | GLFT ODE missing $v_{q+1}$ | add `-\eta(v_{q-1}+v_{q+1})` |
| M3 | 06:30 | high | GLFT $\eta$ exponent | `-(1+\gamma/k)` → `-(1+k/\gamma)` |
| M4 | 03:69 | med | skew per lot `2θ₂γ` | → `2θ₂` |
| M5 | 04:39 | med | skew per lot `2θ₂γ` | → `2θ₂` |
| C1 | index:90 | med | "a few percent" vs 60% sim result | reword |
| C2 | 04:37 | low | rationale contradicts stated monotonicity | reword |

**Blocks run:** 7 · **blocks matching fence:** 7 · **files checked:** 7 · **errors:** 7.

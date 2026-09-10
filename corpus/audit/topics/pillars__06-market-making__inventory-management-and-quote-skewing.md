# Audit Report — `content/pillars/06-market-making/inventory-management-and-quote-skewing/`

Scope: 7 files (index.md + 01..06). Sole adversarial reviewer. Audited spelling/typos (prose only, code/LaTeX excluded), every boxed formula and worked numeric example, every ` ```python ` block (run + stdout-diff), and cross-page coherence (prereqs, jargon, wikilinks, contradictions).

## 1. Verdict

**ACCEPT_WITH_FIXES.** All 7 code blocks run (exit 0) and their stdout matches the adjacent output fence **byte-for-byte (7/7)**; all 22 unique wikilinks resolve. Prose is clean except one frontmatter-tag typo. The core math — reservation price, skew-per-share, reservation ask/bid, inventory-risk CE cost, P&L std, cost-anchored half-markup, Almgren–Chriss trajectory, multi-asset reservation price — re-derives correctly and matches the code. Two **substantive math errors** and several minor notation/imprecision issues remain:

1. **06:58 (HIGH)** — the Guéant–Lehalle–Fernandez-Tapia linear-ODE system is written wrong **twice**: it drops the $v_{q+1}$ neighbour term and the $\eta$ exponent has $\gamma/k$ where it must be $k/\gamma$.
2. **02:55 / 02:100 (MEDIUM)** — the optimal inventory $I^\ast=\mu/(\gamma\sigma^2\tau)$ carries a spurious $\tau$ (should be $\mu/(\gamma\sigma^2)$ under the folder's own $\mu$-as-rate convention, which its own 05 code uses).
3. **03:64 (MEDIUM)** — symbol collision: the fill-intensity prefactor and the markup share the symbol $A$, so the prose formula "revenue $=Ae^{-kA}(A-c)$" does **not** maximize at $c+1/k$ as written.
4. **05:32 (LOW)** — the two-sided first-passage constant is the *one-sided* value ($2\Phi$); for $\max|q_t|$ it should be $4\Phi$.
5. **05:42 (LOW)** — "$z_\beta\sqrt{Q}\,\sigma_q$" is dimensionally inconsistent.
6. **02:39 (LOW, notation)** — CE identity mixes a zero-mean RHS with a level-priced LHS ($I S_T$).
7. **06:9 (LOW, typo)** — tag `almgen-chriss` → `almgren-chriss`.

## 2. Issues table

| File:Line | Problem (stated) | Correct | Severity |
|---|---|---|---|
| 06:58 | $\dot v_q(t)=\alpha q^2 v_q(t)-\eta\,v_{q-1}(t)$ | GLFT (arXiv:1105.3115) system is $\dot v_q(t)=\alpha q^2 v_q(t)-\eta\,(v_{q-1}(t)+v_{q+1}(t))$. The write-up omits the $v_{q+1}$ term, breaking the $\ell^2$ structure (the source rewrites it as $\alpha q^2 v_q-\eta(v_{q+1}-2v_q+v_{q-1})-2\eta v_q$). Add $+v_{q+1}(t)$. | **HIGH (math)** |
| 06:58 | $\eta=A\big(1+\tfrac{\gamma}{k}\big)^{-(1+\gamma/k)}$ | GLFT: $\eta=A\big(1+\tfrac{\gamma}{k}\big)^{-(1+k/\gamma)}$. The exponent's fractional part is $k/\gamma$, **not** $\gamma/k$. (Cross-checked against the source text and the hftbacktest reference implementation, where $c_2=\sqrt{\gamma/(2A\delta k)\,((1+\xi\delta/k)^{k/(\xi\delta)+1})}$ ⇒ exponent $1+k/\gamma$.) With $\gamma{=}0.1,k{=}1.5,A{=}140$: stated $\eta=130.69$, correct $\eta=49.85$ — a 2.6× error. | **HIGH (math)** |
| 02:55, 02:100 | $I^\ast=\dfrac{\mu}{\gamma\sigma^2\tau}$ | With $\mu$ a drift **rate** (the folder's own convention — see the 05:77 code `S += mu*dt`), $\mathbb E[W]=\text{spread}+I\mu\tau$ and $\mathrm{Var}=I^2\sigma^2\tau$, so $\partial_I\!\big[I\mu\tau-\tfrac\gamma2 I^2\sigma^2\tau\big]=0 \Rightarrow I^\ast=\dfrac{\mu}{\gamma\sigma^2}$. The $\tau$ cancels; the stated formula has an extra $\tau$. (Only convention-consistent if $\mu$ were defined as the *total* expected move over $\tau$, which it is not.) | **MEDIUM (math)** |
| 03:64 | "fill arrivals $\pi(A)=Ae^{-kA}$ … expected revenue per sell at ask markup $A$ is $Ae^{-kA}(A-c)$; maximizing gives $A^\ast=c+\tfrac1k$" | Symbol collision: the first $A$ is the intensity **prefactor** ($=140$ in the code, a constant), the $A$ in $e^{-kA}$ and $(A-c)$ is the **markup**. Read literally with one symbol, $Ae^{-kA}(A-c)$ maximizes at $A\approx1.36$ (verified numerically), **not** $c+1/k=0.7167$. The code is correct because it uses distinct names (`A` vs `g`); the prose should write $\pi(\delta)=\lambda_0 e^{-k\delta}$ and revenue $\lambda_0 e^{-k\delta}(\delta-c)$. The endpoint $A^\ast=c+1/k$ is right for the code objective. | **MEDIUM (notation)** |
| 05:32 | $\mathbb P\!\big(\max_{0\le t\le T}|q_t|\ge Q\big)\approx 2\,\Phi\!\big(-\tfrac{Q}{\sigma_q\sqrt T}\big)$ | $2\Phi(-Q/(\sigma_q\sqrt T))$ is the **one-sided** reflection result $\mathbb P(\max_{[0,T]}q_t\ge Q)$. For the two-sided $|q_t|$ the leading constant is $4$: $4\Phi(-Q/(\sigma_q\sqrt T))$ (union of two rare, near-disjoint events). Monte-Carlo check ($\sigma_q{=}2,Q{=}3,T{=}1$, 200k paths): 0.248 ≈ $4\Phi{=}0.267$, while $2\Phi{=}0.134$ is ~2× low. | Low (math) |
| 05:42 | "inventory-risk VaR $\approx z_\beta\sqrt{Q}\,\sigma_q$" | Dimensionally inconsistent: $\sqrt{Q}\,\sigma_q$ mixes shares$^{1/2}$ with a variance. Scaling should be linear in the limit ($\approx z_\beta Q\,\sigma_S\sqrt{\tau}$ for price risk) or $z_\beta\sigma_q$ if it is inventory-dispersion VaR. Fix the exponent/expectation to match the intended quantity. | Low (math) |
| 02:39 | $\mathbb E[-e^{-\gamma I S_T}]=-e^{-\gamma(0-\frac\gamma2 I^2\sigma^2\tau)}$ | LHS uses the **level** $I S_T$ (mean $I\bar S$), RHS assumes a **zero-mean** P&L. Either write $\mathbb E[-e^{-\gamma I(S_T-\bar S)}]$ or restore the mean in the exponent. Page 03:52 states the consistent form $\bar S I-\tfrac12\gamma\sigma^2I^2\tau$, so the two pages disagree in notation. | Low (notation) |
| 06:9 | frontmatter tag `- almgen-chriss` | misspelling of **Almgren**; should be `almgren-chriss` (page body spells it correctly). | Low (typo) |

## 3. Math verified (correct)

Every boxed formula / worked number re-derived by hand and/or re-executed. All of the following are **correct**:

- **Reservation price** $r(I)=\bar S-\gamma\sigma^2I\tau$ (02:43, 03:54, 04:19, index:33, 01:51): $\bar S{=}100,\gamma{=}.1,\sigma{=}2,\tau{=}1,I{=}4$ ⇒ $98.40$ ✓. Slope $-\gamma\sigma^2\tau=-0.4$ ✓.
- **Skew per share** $\gamma\sigma^2\tau=0.400$ ✓ (index:34).
- **Reservation ask/bid** $r^a=\bar S+(1-2I)\tfrac{\gamma\sigma^2\tau}{2}$, $r^b=\bar S+(-1-2I)\tfrac{\gamma\sigma^2\tau}{2}$ (03:58, index:35-36): centered on $r(I)$ with half-width $\tfrac12\gamma\sigma^2\tau$ ⇒ $98.60/98.20$ at $I{=}4$ ✓; difference $=\gamma\sigma^2\tau$ ✓ (index:37, quadratic in $\sigma$: 0.1/0.4/1.6 ✓).
- **Inventory-risk CE cost** $\tfrac12\gamma\sigma^2I^2\tau$ (index:38, 02:45): $I{=}40$ ⇒ $320$ ✓; marginal cost $\gamma\sigma^2(I+\tfrac12)\tau$ from discrete increment (02:22) ✓; $\partial_I(\tfrac12\gamma\sigma^2I^2\tau)=\gamma\sigma^2I\tau$ ✓ (02:47).
- **P&L std** $|I|\sigma\sqrt\tau$ (index:39, 02:33): $I{=}40$ ⇒ $80$ ✓; code reproduces 20.02/40.04/80.09 ✓.
- **Cost-anchored half-markup** $a^\ast=c+\tfrac1k$ (index:41, 03:66): $c{=}.05,k{=}1.5$ ⇒ $0.7167$ ✓; code's grid/argmax agrees to 4 dp ✓.
- **Inventory-controlled quotes** bid $=r-a^\ast$, ask $=r+a^\ast$ (index:40, 03:70): $I{=}4$ ⇒ $97.68/99.12$ ✓; the "both quotes below mid when long" claim ✓.
- **Linear skew** $\Delta s=-\alpha(I-I_{\text{target}})$, $\alpha=\gamma\sigma^2\tau$ (04:23,04:37,04:45,index:42) ✓; 04's $\alpha{=}0.40$ = $\gamma\sigma^2\tau$ at its own params ✓.
- **A–S half-spread** in the code, $\text{half}=\tfrac12\big(\gamma\sigma^2\tau+\tfrac2\gamma\ln(1+\gamma/k)\big)$ (01:71, 04:73, 05:62) = $\tfrac12\gamma\sigma^2\tau+\tfrac1\gamma\ln(1+\gamma/k)$ ✓ matches A–S.
- **Almgren–Chriss** (06:34): $x_t=X\sinh(\kappa(T-t))/\sinh(\kappa T)$, $\kappa=\sqrt{\lambda\sigma^2/\eta}$ ✓. Executed: $\kappa{=}0.6$, half-life $\ln2/\kappa{=}1.155$ yr ✓, speed $t{=}0$ $=X\kappa\coth(\kappa T)=1113.6$/yr ✓, $t{=}T$ $=X\kappa/\sinh(\kappa T)=942.5$/yr ✓; monotone claims (↑$\lambda$ or ↑$\sigma^2$ ⇒ ↑$\kappa$; ↑$\eta$ ⇒ ↓$\kappa$) ✓.
- **Multi-asset reservation price** $r_i=\bar S_i-\gamma\,\mathbf e_i^\top\Sigma\,\mathbf q\,\tau$ (06:50) ✓ correct generalization of the scalar skew.
- **Adverse-selection break-even** $a^\ast=c+\tfrac1k\ge p_{\text{tox}}J$ (06:42) — coherent heuristic ✓.
- **Mean-variance objective / proxy** $\mathbb E[W]-\tfrac\gamma2\mathrm{Var}(W)$ (02:53, 04:55) ✓.
- **Numeric prose claims** all match the code: 01/04 symmetric std $8.97$, max $48$; skew cuts std $3.0\times$ / inv std $2.8\times$; 04 over-skew mean $51.46$; 05 breach $91.8\%\!\to\!0.22\%$; 06 mean P&L $53.5\!\to\!28.6\!\to\!3.6$.

## 4. Code run / match stats

| File | Block | Runs (exit 0) | Stdout matches doc |
|---|---|---|---|
| index.md | §3 quote engine | ✓ | ✓ |
| 01-from-zero-intuition.md | symmetric-vs-skew paths | ✓ | ✓ |
| 02-the-inventory-problem.md | fixed-position P&L/CE | ✓ | ✓ |
| 03-ho-stoll-model.md | r(I)+interior a* | ✓ | ✓ |
| 04-quote-skewing.md | 4-strategy headline | ✓ | ✓ |
| 05-failure-modes-and-practice.md | trending breach sweep | ✓ | ✓ |
| 06-advanced-extensions.md | A–C path + toxic flow | ✓ | ✓ |

**7/7 blocks run successfully (NumPy only); 7/7 stdout match the documented fences exactly.** All blocks are deterministic (`np.random.default_rng(<fixed seed>)`, `PCG64`) — no timing/nondeterminism or multiprocessing. The 01 and 04 blocks share the same `run('symmetric')` engine/seed and produce identical symmetric stats (std 8.973, max 48) — coherent.

## 5. Links & coherence

- **22 unique wikilinks, all resolve** (file-exact or `folder/index.md`). No broken links. Forward links to `optimal-execution-and-almgren-chriss`, `execution-algorithms-vwap-twap-pov`, `var-and-expected-shortfall`, `liquidity-risk-and-margin-spirals`, `adverse-selection-and-glosten-milgrom`, `toxic-order-flow-and-vpin`, `spread-decomposition-and-roll-model` and the four A–S sub-pages all land.
- **Prerequisites:** index.md names folder-level prereqs (A–S **and** Probability & Stochastic Control) for pages 02–06, with 01 self-scoped. Each sub-page states its own smaller chain (02: 01+Prob; 03: 02+Stoch Calc; 04: 03+A–S:04; 05: 04; 06: 04+05). 04/05/06 don't restate the folder-level prereqs — same benign framing tension the sibling audit noted; internally consistent, no hard error.
- **Jargon:** reservation price, inventory risk, CE cost, quote skewing, cost-anchored half-markup, fill elasticity $k$, Ornstein–Uhlenbeck reversion, bang-bang, GLFT linear-ODE, Almgren–Chriss $\kappa$, VPIN/toxicity all defined on first use. No undefined terms.
- **Contradictions:** none beyond the issues above. The "skew ≠ adverse-selection defence" message is consistent across index §4, 01 f.m.3, 03 f.m.4, 04 f.m.5, 05 f.m.5, 06 f.m.2. Numeric "verified check" cells on index.md agree with the sub-page code outputs.
- **House style:** wikilinks `[[full/path|Alias]]` ✓; math in `$…$`/`$$…$$` ✓; hub + 6 sub-pages ✓. Minor: index:11 & 112 alias "Probability & Stochastic Control" points at `foundations/probability-and-measure-theory`; index:93 says "our simulation" for the 92% breach number that is actually computed on page 05 (cosmetic).

## 6. Recommended fixes

1. **06:58** — write $\dot v_q(t)=\alpha q^2 v_q(t)-\eta\big(v_{q-1}(t)+v_{q+1}(t)\big)$ and $\eta=A\big(1+\tfrac{\gamma}{k}\big)^{-(1+k/\gamma)}$.
2. **02:55 / 02:100** — change $I^\ast=\tfrac{\mu}{\gamma\sigma^2\tau}$ to $I^\ast=\tfrac{\mu}{\gamma\sigma^2}$.
3. **03:64** — rename the intensity prefactor (e.g. $\lambda_0 e^{-k\delta}$) so the markup $A$ is unambiguous; the result $A^\ast=c+1/k$ then follows.
4. **05:32** — use $4\,\Phi(-Q/(\sigma_q\sqrt T))$ for the two-sided $\max|q_t|$ (or relabel the bound as one-sided).
5. **05:42** — restore a dimensionally consistent VaR expression.
6. **02:39** — make LHS/RHS both zero-mean (or both include $I\bar S$).
7. **06:9** — fix tag to `almgren-chriss`.

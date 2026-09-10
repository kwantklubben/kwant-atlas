# Audit — pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising

Folder: `content/pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/`
Scope: 7 files (index + 01–06). `_legacy/` absent — nothing ignored.
Role: sole adversarial reviewer.
Date: 2026-09-10

## Summary

- **Files checked:** 7
- **Python blocks run:** 9 (all stdlib, `numpy` only). **9/9 execute clean (exit 0) and stdout matches the documented output fence byte-for-byte** (after trailing-space/blank-line normalisation). No code discrepancy found.
- **Wikilinks:** 15 unique targets — all resolve to existing files.
- **Math:** 1 error found (minor — a wrong limiting constant in a worked derivation).

---

## 1. Math errors (1)

### 1.1 01-from-zero-intuition.md:46 (and prose at 48) — wrong limit for observations-per-parameter at N≈T
- **Stated:** `$$\frac{NT}{N(N+1)/2}=\frac{2T}{N+1}\xrightarrow[\ N\approx T\ ]{}\ 1 .$$` followed by "When N is comparable to T, there is *one* observation per parameter."
- **Correct:** substituting N=T gives $\frac{2T}{N+1}=\frac{2N}{N+1}\approx 2$ (verified numerically: N=T=500 → 1.996). The arrow should point to **2**, and the prose should say **two** observations per parameter. (The "one observation per parameter" regime is actually $q=N/T\approx\tfrac12$, not $q\approx1$.)
- **Impact:** minor. The surrounding message — parameter count $N(N+1)/2$ explodes vs $NT$ data points — is correct; only the limiting constant at the $N\approx T$ boundary is off by 2×.

---

## 2. Math verified correct (no error)

- **Sample covariance / MP law** (index:30–39; 02:39–47): $S=\tfrac1T X^\top X$; $f(\lambda)=\frac{1}{2\pi\sigma^2 q\lambda}\sqrt{(\lambda_+-\lambda)(\lambda-\lambda_-)}$; edges $\lambda_\pm=\sigma^2(1\pm\sqrt q)^2$. Edges re-checked: q=0.5 → λ₊=2.9142, q=0.1 → λ₊=1.7325, q=1 → [0,4]. All correct.
- **Condition-number blow-up** (02:53): $\kappa(S)\approx\frac{(1+\sqrt q)^2}{(1-\sqrt q)^2}\to\infty$ as q→1. Correct; N=490,T=500 → 2.05×10⁴ confirmed by code (`cond=20517.46`).
- **Linear shrinkage intensity** (index:35; 03:43–53): $\delta^*=\frac{\pi-\rho}{\gamma}\cdot\tfrac1T$, clipped to [0,1]; $\pi=\sum_{ij}\tfrac1T\sum_t(x_{it}x_{jt}-s_{ij})^2$; $\rho=\sum_i\pi_{ii}$ (identity target); $\gamma=\|F-S\|_F^2$. Identity-target N=8,T=16 → δ*=0.3734 (code confirms). Correct.
- **Well-conditioned / bias-variance form** (index:41; 03:61–67): $\delta^*=\frac{\beta^2}{\alpha^2+\beta^2}$ with $\alpha^2=\|\Sigma-\mu I\|_F^2$, $\beta^2=\mathbb{E}\|S-\Sigma\|_F^2$, $\delta^2=\alpha^2+\beta^2=\mathbb{E}\|S-\mu I\|_F^2$. The cross term $\mathbb{E}\langle S-\Sigma,\Sigma-\mu I\rangle=0$ since $\mathbb{E}[S]=\Sigma$, so $\delta^2=\alpha^2+\beta^2$ holds. **PRIAL = δ\*** verified by closed-form minimization (min risk $=\alpha^2\beta^2/\delta^2$ ⇒ PRIAL $=1-\alpha^2/\delta^2=\beta^2/\delta^2=\delta^*$). Correct.
- **RMT constant-residual denoising** (index:42; 04:43–47): $\lambda_i^{\rm den}=\lambda_i$ for signal, $\bar\lambda_{\rm noise}=\frac{1}{N-K}\sum_{i>K}\lambda_i$ otherwise; bulk-average $\approx1$ via $\operatorname{tr}=N$. Correct; N=200,T=500 → λ₊=2.6649, K=3 confirmed.
- **Nonlinear (oracle) shrinkage** (index:45; 06:31–37): $d_i=\frac{\lambda_i}{|1-c-c\lambda_i\breve m_F(\lambda_i)|^2}$, $c=N/T$; MP equation $m_F(z)=-[z-c\int\frac{\tau}{1+\tau m_F(z)}\,dH(\tau)]^{-1}$. Standard LW 2012 oracle. Correct; Experiment 1 reproduces (top-4 sample [22.02,14.47,11.17,2.77] → nonlinear [20.58,14.51,10.46,1.59]).
- **Factor covariance** (index:46; 06:47–49): $\hat\Sigma=B\Lambda B^\top+\Psi$, $\Psi=\operatorname{diag}$; κ 3323→161 at N=100,T=150 confirmed by code.
- **All worked numeric claims** cross-checked against code output: EXP A (01: in-sample 0.0216 vs true 0.1752, 1/N 0.0959), EXP B (02: κ 2.05×10⁴), EXP D (04: Frobenius −25%, variance −42%, κ 277→44), EXP E (05: κ≈6×10¹⁸, pinv var 4.79 vs 1/N 0.013), 05 Exp 2 ranking table (T=50/100/300/1000), 06 Exp 1/2. All match.
- **Bias–variance decomposition** (01:52), min-variance weight $w=\Sigma^{-1}\mathbf 1/(\mathbf 1^\top\Sigma^{-1}\mathbf 1)$ (01:36), rank deficiency $\operatorname{rank}(S)\le\min(N,T-1)$ (05:30), MLE-vs-unbiased $T/(T-1)$ scaling (02:104), overfitting inequality (05:48) — all correct.

---

## 3. Code audit

9 Python blocks across the 7 files; **all 9 ran (exit 0) and stdout matched the documented output fence byte-for-byte** (after trailing-space normalisation). No fabricated or mismatched outputs.

| File | Blocks | Status |
|---|---|---|
| index.md | 1 | ✓ |
| 01-from-zero-intuition.md | 1 | ✓ |
| 02-the-sample-covariance-problem.md | 1 | ✓ |
| 03-linear-shrinkage.md | 1 | ✓ |
| 04-random-matrix-theory-denoising.md | 1 | ✓ |
| 05-failure-modes-and-practice.md | 2 | ✓ |
| 06-advanced-extensions.md | 2 | ✓ |

Actual count of blocks run: **9**. All require only `numpy`; no external deps.

---

## 4. Coherence & links

- **Hub↔subpage sequencing** consistent: 01→02→03→04→05→06; each page's "Basic Prerequisites" names exactly the prior page(s) and matches the hub's routing. Hub correctly states 01 has its own smaller entry requirements ("none") while 02–06 inherit the folder-level prerequisites.
- **EXP labels** (hub §2/§4: EXP A–E) map cleanly to pages: A=01, B=02, C=03, D=04, E=05. Minor style note: hub uses "EXP A–E" while pages 05/06 use "Experiment 1/2" — not a contradiction, just a naming convention difference.
- **All 15 wikilink targets resolve** (6 sub-pages, 5 sibling folders under `05-portfolio-optimization/`, 2 foundations, hub). One regex false positive (`[[20.0,15.0,10.0]]` inside 06's Python code) is not a link.
- **Jargon consistent:** "bulk", "noise band", "λ₊", "error maximization", "constant residual" used consistently across hub and pages.
- **Minor notation advisory:** the hub lookup table reuses the symbol $\kappa$ for the LW intensity numerator ($\kappa=(\pi-\rho)/\gamma$) in the same table where $\kappa(S)$ means the condition number. Both are locally defined, so it is not an error, but a reader could momentarily conflate the two.
- **Cross-references correct:** page 03's forward links, 04/05/06 bridge sections, and the Black–Litterman / HRP / MPT sibling links all point at existing folders.

---

## 5. Verdict

**PASS (1 minor math error).** The folder is high-quality and internally consistent: all 9 code blocks reproduce their documented output exactly, all formulas are standard and correctly transcribed, all links resolve, and the hub/subpage structure is coherent. The single defect is a wrong limiting constant ($\to 1$ should be $\to 2$) in the observations-per-parameter derivation at 01:46/01:48.

# Audit: pillars/06-market-making/spread-decomposition-and-roll-model

**Auditor:** sole adversarial reviewer (subagent)
**Date:** 2026-09-10
**Scope:** 7 files (index.md + 01–06). `_legacy` excluded.
**Sources used:** `corpus/verified/hasbrouck_ch1-5.md`, `hasbrouck_ch6-10.md`, `hasbrouck_ch11-15.md`; primary PDFs `corpus/titles/refs/03_hasbrouck_2007_…pdf`, `26_Stoll_1989_…pdf`, `25Huang1997_…pdf`.
**Verdict:** **NEEDS REVISION.** Code is clean (all 11 blocks reproduce their fences exactly), but there is one blocking formula error carried across pages (`S_q = 2c` vs the correct `2(c+λ)`), a formula↔code timing mismatch in the generalized-Roll implementation, and several moderate math/labeling inconsistencies.

---

## 1. Coverage

| File | Checked | Py blocks | Runs | Output = fence |
|---|---|---|---|---|
| index.md | ✓ | 3 | ✓ | MATCH |
| 01-from-zero-intuition.md | ✓ | 1 | ✓ | MATCH |
| 02-quoted-effective-realized.md | ✓ | 1 | ✓ | MATCH |
| 03-the-roll-model.md | ✓ | 1 | ✓ | MATCH |
| 04-spread-decomposition.md | ✓ | 1 | ✓ | MATCH |
| 05-failure-modes-and-practice.md | ✓ | 3 | ✓ | MATCH |
| 06-advanced-extensions.md | ✓ | 1 | ✓ | MATCH |

- **blocks_run = 11**, all exit 0, every fenced output reproduced **byte-for-byte** (combined 3-line fence in index.md also matches the concatenation of its 3 blocks).
- **Spelling/typos:** hunspell (`en_US` + domain dict) over extracted prose → only legitimate domain terms / proper nouns / LaTeX residue flagged (Beveridge, Demsetz, Cholesky, stationarity, autocorrelated, intraday, illiquid, timestamps, `\mathrm`, `\varepsilon`, `zig-zag`). **No genuine typos.**

---

## 2. Math verification (boxed formulas + worked examples)

### Verified CORRECT
- **03 §2.2 / index §2:** Roll model $m_t=m_{t-1}+u_t$, $p_t=m_t+q_tc$; $\gamma_0=2c^2+\sigma_u^2$, $\gamma_1=-c^2$, $\gamma_k=0\ (k\ge2)$; $c=\sqrt{-\gamma_1}$, $S=2\sqrt{-\gamma_1}$, $\sigma_u^2=\gamma_0+2\gamma_1$. Matches Hasbrouck Eqs 3.3–3.5.
- **03 §2.4 MA(1) inversion** $\theta=(\gamma_0-\sqrt{\gamma_0^2-4\gamma_1^2})/(2\gamma_1)$ with $|\theta|<1$: correct invertible root for $\gamma_1<0$ (roots are reciprocal; this picks $|\theta|<1$). Numerically consistent with 06's output ($\theta=-0.6902$).
- **50 §2.3 / index §2:** Stoll reversal params `(π=½, δ=0)` order-processing, `(π=½, δ=½)` adverse-info, `(π>½, δ=½)` inventory; reversal size $=(1-\delta)S$. **Exact match** to Stoll (1989) Fig. 2.
- **04 §2.1 Glosten–Harris** $m_t=m_{t-1}+u_t+q_t(\lambda_0+\lambda_1V_t)$, $p_t=m_t+q_t(c_0+c_1V_t)$, differenced to the permanent + transitory pieces. Matches Hasbrouck Ch 9 / verified corpus.
- **04 §2.4 Huang–Stoll eq (5)** $\Delta p_t=\tfrac{S}{2}(q_t-q_{t-1})+\lambda\tfrac{S}{2}q_{t-1}+e_t$ with $\lambda=\alpha+\beta$. **Confirmed verbatim against the Huang–Stoll (1997) PDF** (p. 1000, "Combining Equations (3) and (4)"), including the q_{t-1} timing and the "order-processing vs adverse-selection+inventory" reading.
- **06 §2.2 B–N:** $\sigma_w^2=(1+\theta)^2\sigma_\varepsilon^2$ (= book Eq 8.10); **06 §2.3 variance ratio** (book Eq 8.14) and the $M>N\Rightarrow V<1$ direction; **06 §2.4 MRR/Ch 9** $q_t=v_t+\beta v_{t-1}$, $w_t=u_t+\lambda v_t$, $\Delta p_t$ (Eq 9.6), $\sigma_w^2=\sigma_u^2+\lambda^2\sigma_v^2$, relative share $\approx R^2$. All match the verified corpus.
- **04 §2.2 / index §2 generalized Roll** $\Delta p_t=c(q_t-q_{t-1})+\lambda q_t+u_t$, $\gamma_0=c^2+(c+\lambda)^2+\sigma_u^2$, $\gamma_1=-c(c+\lambda)$, $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$. Matches Hasbrouck Eq 8.2–8.3 (chain-rule verified).
- **05 §2 Ex 4.3** $\gamma_1=-c(c+\rho\sigma_u)$ → upward bias. **Exact match** to Hasbrouck Ex 4.3.
- **02 §2 realized** $S_r=2\lambda$ and effective $S_e=2c$: correct under the generalized-Roll timing used.
- index §3 "the numbers in the check column were re-executed and reproduced exactly" — **true**.

### Errors / findings

**E1 (MATH — blocking) — 02-quoted-effective-realized.md:32 (and index.md:39)**
- Stated: "**Quoted:** $S_q=2c$ — the full bid-ask width" (in the *generalized* Roll section, where λ>0).
- **Wrong.** Hasbrouck Ch 8: bid$=m_{t-1}-(c+\lambda)+u_t$, ask$=m_{t-1}+(c+\lambda)+u_t$, "**The spread is $2(c+\lambda)$**." The floor at 02:32 conflates quoted with effective (both written $2c$). This directly contradicts **04:51 / 04:112** ("total quoted spread $2(c+\lambda)$") and **index.md:42** ("total $S=2(c+\lambda)$"). Correct: $S_q=2(c+\lambda)$.
- Consequence: the coded "$S_q$ check $=0.0400$" (index:39) is just the printed `2*c`, whereas the model's quoted spread at $c{=}0.02,\lambda{=}0.01$ is $0.06$.

**E2 (MATH/coherence — major) — 02:38, 02:40**
- Stated: "$S_q-S_r=2(c-\lambda)$" and "with $\lambda>0$ the ordering $S_q\ge S_e\ge S_r$ holds".
- With the **correct** $S_q=2(c+\lambda)$: $S_q-S_r=2(c+\lambda)-2\lambda=\mathbf{2c}$, not $2(c-\lambda)$ (the stated form only follows from the erroneous $S_q=2c$). The ordering claim is also too strong: $S_e\ge S_r$ needs $c\ge\lambda$, and under 02's own $S_q=S_e=2c$ the strict $S_q\ge S_e$ fails at $\lambda{=}0$. Cascade of E1.

**E3 (formula ↔ code mismatch — moderate) — index.md:57 + index §3 block-3; 04:50 + 04 §3**
- The **boxed** generalized-Roll equation (index:57, 04:50, ≡ Hasbrouck Eq 8.2) puts adverse selection on the **contemporaneous** direction: $\Delta p_t=c(q_t-q_{t-1})+\lambda q_t+u_t$.
- The "computational implementation" (index §3 block 3; 04 §3 `simulate_gh`) applies impact *after* the print (`m += lam*q`), so it generates $\Delta p_t=c(q_t-q_{t-1})+\lambda q_{\mathbf{t-1}}+u_t$ and regresses on `X2 = qs[i-1]`. The index code comment even writes `…+lam*q_{t-1}+u`.
- The two are different models: the code's DGP has $\gamma_1=c(\lambda-c)$, **not** the boxed $\gamma_1=-c(c+\lambda)$. (The regression still recovers $c,\lambda$ because its regressors match its own DGP — and it matches Huang–Stoll eq (5) — but it is **not** the boxed generalized Roll.) 04:83 text ("Simulate the generalized-Roll process, then run … $\lambda q_t$") is therefore inaccurate about its own code.

**E4 (MATH — moderate) — 06-advanced-extensions.md:49 vs 06:51**
- 06:49 states "$\sigma_s^2=\theta^2\sigma_\varepsilon^2$ **(pricing-error variance)**"; 06:51 states "in the pure Roll case … $\sigma_s^2=c^2$". Both cannot hold.
- Per Hasbrouck §8.5–8.6: $\mathrm{Var}(p_t-m_t)=c^2$ is the pricing-error variance, while $\theta^2\sigma_\varepsilon^2$ is the **lower bound** on it (attained only when $\sigma_u^2=0$), and in the original Roll model $\sigma_s^2=-\gamma_1=-\theta\sigma_\varepsilon^2>\theta^2\sigma_\varepsilon^2$.
- The page's own code shows the gap: `perr = θ²σε² = 0.000436` vs $c^2=0.000625$ (~30% apart) — yet 06:114 calls it "approximates the bounce $c^2$". The same symbol $\sigma_s^2$ is assigned two different values.

**E5 (experiment fidelity — moderate) — 05:36–38 vs 05:66–78**
- 05:36 states the (correct, Ex 4.2) result $\gamma_1=-c^2(1-2\rho)$ — derived under Ex 4.2's assumption $\mathrm{Corr}(q_t,q_{t-k})=0$ for $k>1$ — and adds "(For $\rho>\tfrac12$ it would even flip positive.)"
- Experiment 1 (05:66–72) instead simulates a **Markov** chain ($P(\text{stay})=0.8\Rightarrow\rho=0.6$) whose autocovariance is *geometric* ($\rho_k=\rho^k$), for which $\gamma_1=-c^2(1-\rho)^2=-0.000064$ — matching the printed `-0.0000630`, but **not** the stated formula (which at $\rho=0.6$ gives $+0.00008$, i.e. an undefined estimator). So the demo does not instantiate the model it cites, and the page's own output refutes its "$\rho>½$ flips positive" parenthetical.

**E6 (arithmetic — low) — 03-the-roll-model.md:58**
- Stated: "$\hat\gamma_1=-0.0000294$ … giving $c=\$0.017$, spread$=\$0.034$." But $2\sqrt{0.0000294}=\$0.0108\ne\$0.034$. The value consistent with $c=\$0.017$ (and with the book) is $\hat\gamma_1\approx-0.00029$ — the displayed figure carries an extra zero (off by $\sqrt{10}\approx3.16$). Faithful to the source text, but arithmetically self-inconsistent.

**E7 (labeling — low) — 02:38 / 02 §3 output / index.md:108**
- "adverse-selection loss $=S_e-S_r=2(c-\lambda)$". $S_e-S_r$ is the **effective−realized (price-impact)** residual per the identity $S_e=S_r+\text{impact}$; it equals zero when $c=\lambda$, **not** when $\lambda$ (adverse selection) is zero. Calling it "adverse-selection loss" is loose. (Numerically 0.0200 only because the chosen $c{:}\lambda=2{:}1$ makes $2(c-\lambda)=2\lambda$.)

---

## 3. Code verification
All 11 Python blocks ran on the standard library, exit 0, and matched their fenced output **exactly**:

- index.md blocks 1–3 → combined fence: `gamma1=-0.0006227 spread=0.04991`; `quoted=0.0400 effective=0.0400 realized=0.0200 impact/2=0.0100`; `c=0.0200 lambda=0.0150 spread=0.0700`. **MATCH.**
- 01 → `-0.0006227 / 0.04991`. **MATCH.**
- 02 → `0.0400 / 0.0400 / 0.0200 / 0.0200`. **MATCH.**
- 03 → `gamma0=0.0013456 … 0.01976 … sigma_u^2=0.00010`. **MATCH.**
- 04 → `0.0200 / 0.0150 / 0.0350 / 0.0700 / 42.8%`. **MATCH.**
- 05 → `-0.0000630/0.01588`; `-0.0004540/0.04261`; `0.000445 → NaN`. **MATCH (all 3).**
- 06 → `theta=-0.6902, sw2=0.000088, perr=0.000436, V(10,1)=0.1630`. **MATCH.**

No stdout/stderr divergence, no missing or stale fences. Note (E5): 05-block-8's output is self-consistent but realises a *different* order-flow model than the text cites; note (E3): 04/index block-3's outputs are right for its own DGP.

---

## 4. Coherence / links / jargon

- **Wikilinks:** all 17 unique targets resolve to real files (no dangling links). ✓
- **Hub ↔ 01 prereq:** index.md:12 explicitly scopes its prerequisites to pages 02–06 and defers page 01's lighter entry requirement to 01 itself — 01:11 states exactly that (econometrics only). **Consistent.** ✓
- **Prereq chain** (03→04→05→06, all +econometrics) is coherent. ✓
- **Contradiction:** the quoted-spread definition is inconsistent across the folder (E1/E2): 02 & index:39 say $2c$; 04 & index:42 say $2(c+\lambda)$; the source says $2(c+\lambda)$.
- **Jargon (minor):** "MRR" (04:141) is used without expansion (Madhavan–Richardson–Roomans); the index table (index:43) abbreviates "OP / AI / Inv" without gloss in the table itself. Cosmetic.
- **Terminology (minor):** index:37/40 defines the effective spread against the effective price $m_t$; the literature convention is the quote *midpoint*. Not wrong in this model but worth a footnote.

---

## 5. Summary of required fixes
1. **02:32 (blocking):** change $S_q=2c$ → $S_q=2(c+\lambda)$; recheck index:39's "quoted" check value and the 02 §1/§2 ordering claims (E1, E2).
2. **04:38/02:38:** replace $S_q-S_r=2(c-\lambda)$ with $2c$ (given correct $S_q$), and relabel/qualify "adverse-selection loss" (E2, E7).
3. **index:57 / 04:50 vs code:** either align the boxed generalized-Roll equation with the code's $q_{t-1}$ timing or fix `simulate_gh` (and its regressor) to use $q_t$; state that the regression is the Huang–Stoll/Glosten–Harris form (E3).
4. **06:49/51:** distinguish the B–N transitory variance / lower bound $\theta^2\sigma_\varepsilon^2$ from the structural pricing-error variance $\sigma_s^2=c^2$ (E4).
5. **03:58:** fix the extra zero in $\hat\gamma_1$ ($-0.00029$, not $-0.0000294$) so the implied $c=\$0.017$ / spread $=\$0.034$ is arithmetically consistent (E6).
6. **05 Experiment 1:** either simulate the Ex 4.2 lag-1-only order flow, or relabel the demo and drop the "$\rho>\tfrac12$ flips positive" claim (E5).

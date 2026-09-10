# Audit — `content/pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/`

**Scope:** 7 files (index + 01–06). Adversarial pass: prose spelling, every boxed formula + worked
example (MDP formalism, Bellman equations, Q-learning/SARSA, DP value iteration, policy gradient,
exploration/exploitation, reward shaping, off-policy corrections), every ```python block executed and
diffed against its documented output fence, hub↔sub-page coherence, link resolution. `content/_legacy/`
ignored.

**Verdict:** **PASS (clean).** All mathematics is correct, all 7 code blocks reproduce their output
fences byte-for-byte, no prose typos, all 71 distinct wikilink targets resolve. Two minor non-math
defects: one wrong citation author and one legacy link target.

**Counts:** files_checked = 7 · blocks_run = 7 · errors_found = 2.

---

## 1. Code execution (7/7 blocks ran, 7/7 stdout == documented fence)

Each page carries exactly **one** ```python block; there is no multi-block page in this folder, so no
cross-block namespace chaining was required (contrary to the task note — verified: every file has 1
python block and 1 output fence). Every block was extracted, executed with stdlib `python3`, and the
stdout compared line-for-line to the page's fence. **All 7 match exactly.**

| File | blocks | result |
|---|---|---|
| index.md | 1 | MATCH — value iteration `V* = (0, 7.0000, 12.3000, 16.0700)`, greedy `[0,1,1,1]` |
| 01-from-zero-intuition.md | 1 | MATCH — contextual MDP: `Q(trade)=+0.096/+0.360/−0.364`, policy `trade/hold/trade` |
| 02-the-mdp-framing.md | 1 | MATCH — `Q*` table; Bellman residual `0.00e+00` |
| 03-value-based-rl.md | 1 | MATCH — tabular Q-learning `max|V_Q−V*| = 0.0000`, greedy `[0,1,1,1]` |
| 04-policy-gradient-and-actor-critic.md | 1 | MATCH — REINFORCE policy `[0,1,1,1]`; softmax `0.999` on sell-1 at x=3 |
| 05-failure-modes-and-practice.md | 1 | MATCH — EXP1 net `9.0000` vs `16.0700`; EXP2 stale loss `0.5200` |
| 06-advanced-extensions.md | 1 | MATCH — RL schedule `[6,4,0,0,0]` = oracle; shortfall `3.3040` vs TWAP `6.7999` |

Seeds are fixed (`random.seed(0/1/3/42)` in 01/03/04/06; 02/index/05 are deterministic), so all
results are reproducible. No `NameError`/stderr on any block.

## 2. Math — boxed formulas and worked examples

Independently re-derived every displayed formula and re-computed every numeric claim. **All correct:**

- **Bellman optimality (02:43, boxed).** `V*(s)=max_a[R(s,a)+γΣ_{s'}P(s'|s,a)V*(s')]` — correct.
  The companion `Q*(s,a)=R+γΣ P max_{a'}Q*` (02:45) and greedy `π*=argmax_a Q*` also correct.
- **Bellman expectation (index:36, 02:39).** `V^π(s)=Σ_a π(a|s)[R(s,a)+γΣ_{s'}P V^π(s')]` — correct.
- **TD(0) (index:39, 03:31).** `V(S_t)←V(S_t)+α[R_{t+1}+γV(S_{t+1})−V(S_t)]` — correct, and the TD
  error `δ_t=R_{t+1}+γV(S_{t+1})−V(S_t)` (03:29) is the same object.
- **Q-learning (index:40, 03:39 boxed).** `Q(S_t,A_t)←Q+α[R_{t+1}+γ max_a Q(S_{t+1},a)−Q]` —
  correct off-policy max backup.
- **SARSA (index:41).** `…+γ Q(S_{t+1},A_{t+1})…` (on-policy, actual next action) — correct.
- **Policy-gradient theorem (index:42, 04:35).** `∇_θJ=E_π[Σ_t ∇_θ log π_θ(A_t|S_t) G_t]` — correct
  (episodic form), consistent with the single-step form in the hub table.
- **Softmax policy (index:43).** `π_θ(a|s)=e^{θ_{s,a}/τ}/Σ_{a'}e^{θ_{s,a'}/τ}` — correct.
- **REINFORCE / likelihood ratio (04:37–39).** `∇π=π∇logπ`; `θ←θ+α∇logπ(A_t|S_t)G_t` — correct ascent
  sign. Baseline-unbiasedness `Σ_a π(a|s)∇logπ(a|s)=0` (04:45) and advantage `A_t=G_t−V(S_t)` (04:49)
  correct. Actor–critic updates (04:54–55) correct two-time-scale pair. PPO `L^CLIP=min(r A,
  clip(r,1−ε,1+ε)A)`, `r=π_θ/π_θold` (04:56) — correct. Natural gradient `F^{-1}∇J` (04:61) — correct.
- **DQN loss (03:53).** `E[(r+γ max_{a'}Q(s',a';θ⁻)−Q(s,a;θ))²]` — correct.
- **Maximization bias (03:45).** `E[max_a Q]≥max_a E[Q]` (Jensen, max convex) — correct.
- **Contraction (02:49).** `‖TV−TU‖_∞ ≤ γ‖V−U‖_∞`, Banach unique fixed point — correct; the γ=1 caveat
  (02:131) is accurate.
- **Almgren–Chriss (06:39).** `x_t=X_0 sinh(κ(T−t))/sinh(κT)`, `κ≈√(λσ²/η)` with η the temporary-impact
  coefficient — correct textbook form; the λ↑/η↑ monotonicity claim is consistent.
- **Sim-to-real bound (05:43).** `|J_{P*}(π)−J_{P_sim}(π)| ≲ γ/(1−γ)² ‖P*−P_sim‖_∞ R_max` — correct
  simulation-lemma form (steep `(1−γ)²` amplification).

**Worked examples re-derived by hand and by independent code:**

- **Liquidation MDP (index §3, 03 §3, 05 EXP1).** `r(x,a)=aP−ka²−hx`, `P=10,k=2,h=1,γ=0.9,N=3`.
  Solving the fixed point gives `V*=(0, 7, 12.3, 16.07)`; verified exactly. Greedy `[0,1,1,1]`.
- **Reward hacking (05 EXP1).** Gross policy `[0,1,2,3]` nets `9.0000`; correct policy nets `16.0700`;
  cost `7.0700`. The claimed **"44% haircut"** = `7.07/16.07 = 44.0%` — correct.
- **Non-stationarity (05 EXP2).** Stale policy `23.1300` vs oracle `23.6500`, loss `0.5200` — matches
  the hub's "loses 0.52" (index:90). Correct.
- **Execution RL (06 §3).** RL schedule `[6,4,0,0,0]` == DP oracle; IS `3.3040` == oracle; TWAP
  `6.7999`; advantage `3.4959` = `51.4%` of shortfall → "saves over half" is true. Correct.
- **Stochastic MDP (02 §3).** Bellman optimality residual printed `0.00e+00`, matching the hub's
  "`0.00×10^0`" (index:45). Q*(11,·)>Q*(9,·) holds for every (x,a) in the table. Correct.
- **Contextual MDP (01 §3).** Learned Q ≈ edge−cost for all three states; policy matches exact
  optimum. Correct.

*No wrong formula, sign, constant, or indexing was found anywhere.*

## 3. Errors found

### E1 — [06-advanced-extensions.md:157] wrong citation author (minor)
- **Stated:** "**Ning, Baruch & Jaimungal (and Ning, Lin & Jaimungal)**: reinforcement-learning
  execution / market-making".
- **Correct:** the co-authors of the Ning–Jaimungal line are **Franco Ho Ting Lin** (variously styled
  *Lin* / *Ling*) — e.g. "Ning, B., Lin, F.H.T., Jaimungal, S., *Double Deep Q-Learning for Optimal
  Execution* (arXiv:1812.06600, 2018)" and "Ning, B., Ling, F.H.T., Jaimungal, S., *Market Making via
  Reinforcement Learning* (AAMAS 2018)". There is no co-author named **Baruch**; the hub (index:100)
  correctly writes "Ning, Lin & Jaimungal". Fix: replace `Baruch` with `Lin` (or `Ling`).

### E2 — legacy wikilink target instead of canonical hub folder (minor)
- **Locations:** `index.md:111`, `index.md:119`, `03-value-based-rl.md:11`, `03-value-based-rl.md:136`,
  `04-policy-gradient-and-actor-critic.md:146`.
- **Stated:** links resolve to the flat legacy page
  `pillars/07-machine-learning-altdata/deep-learning-for-sequential-data` (86-line standalone file).
- **Correct:** the canonical topic is the **folder hub** `…/deep-learning-for-sequences/index.md`
  (144 lines, `index-hub` tag, 01–06 sub-pages), which is what the repo uses predominantly
  (46 references vs 14). The link resolves (so not broken), but the alias at `index.md:119` literally
  reads "Deep Learning for Sequences" while pointing at `…-sequential-data` — an internal mismatch.
  House style is folder = `index.md` hub, so these five links should target
  `…/deep-learning-for-sequences/index`.

## 4. Spelling / typos (prose only; code & LaTeX excluded)

Tokenised all prose (frontmatter, code fences, inline code, `$…$`/`$$…$$`, wikilink targets stripped)
and ran it through the `en_US` hunspell dictionary. **No spelling errors and no doubled words**: every
out-of-dictionary token is a proper noun, acronym, or technical term (MDP, SARSA, DQN, PPO, TRPO, GAE,
A2C, Almgren, Chriss, Bertsekas, Nevmyvaka, Kearns, Jaimungal, Schulman, Puterman, López, Qlib,
softmax, stationarity, misspecification, resettable, suboptimal, …). British spellings (`behaviour`,
`modelling`) and `namable` are consistent with the rest of the corpus. Zero typos.

## 5. Coherence

- **Hub ↔ 01 prereq:** index:11 states the folder-level prerequisites and explicitly notes "page `01`
  states its own, smaller, entry requirements"; 01:10 requires only Probability Theory
  (conditional expectation). **Consistent.**
- **Notation / jargon:** the hub's Quick-Reference block (index:29) fixes `S,A,R,γ,τ,θ,π_θ,V^π,Q^π,V*`,
  and the same symbols are reused unambiguously in 02–06. "Advantage", "recall/behaviour policy",
  "deadly triad", "maximization bias", "implementation shortfall" are each defined on first use.
  **Consistent.**
- **Links:** all **71 distinct `[[…]]` targets resolve** (file or `folder/index.md`) — 0 broken.
  The only defect is the target-choice issue in E2.
- **Cross-page numbers agree across hub and sub-pages:** `V*=(0,7,12.3,16.07)` and greedy `[0,1,1,1]`
  (index §2/§3 ↔ 03 ↔ 04 ↔ 05); `9.00` vs `16.07` "7.07 loss" (index:88 ↔ 05 EXP1); `0.52` stale-policy
  loss (index:90 ↔ 05 EXP2); Bellman residual `0.00e+00` (index:45 ↔ 02 §3). **No contradictions.**
- **Minor terminology wobble (not counted):** the sample-inefficiency figure `10^5–10^7` is called
  "transitions" in 03:116 but "episodes" in index:91 and 05:128. Units differ but the magnitude claim
  is consistent; low severity.
- **Shared-MDP reuse** between 03 §3, 04 §3 and 05 EXP1 (same `P,k,h,γ,N` and same `reward()` helper)
  is stated explicitly and the numbers are identical — the intra-folder simulation is coherent.

## 6. Recommendation

Ship. Optionally patch E1 (wrong author name — the one clear factual defect) and repoint the five
`deep-learning-for-sequential-data` links at `deep-learning-for-sequences/index` (E2) to match the
canonical hub. No math, code, or spelling corrections are needed.

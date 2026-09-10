# Audit — `pillars/06-market-making/limit-order-book-mechanics/`

**Scope.** 7 topic files (index hub + 6 sub-pages: `01-from-zero-intuition`, `02-limit-vs-market-orders`, `03-the-limit-order-book`, `04-matching-and-priority`, `05-failure-modes-and-practice`, `06-advanced-extensions`). Sole adversarial reviewer.
**Checks performed:** (1) spelling/typos in prose (code & LaTeX excluded); (2) every boxed formula + worked example + every "Verified check" value independently re-derived (hand algebra + an independent numeric script that shares no code with the pages); (3) every ```` ```python ```` block executed and stdout diffed against its output fence; (4) hub↔page coherence, prerequisite chain, jargon first-use, wikilink resolution, cross-page contradictions.
**Reference sources:** `corpus/verified/hasbrouck_ch1-5.md`, `corpus/verified/foucault_ch1-3.md`, `corpus/verified/foucault_ch4-6.md`, `corpus/pillar6-market-making.md`.
**Method reproducibility:** all 7 code blocks run under CPython 3.x, stdlib only, 0 external deps. Wikilinks resolved by file existence under `content/`.

---

## 1. Verdict summary

| Metric | Result |
|---|---|
| Files checked | 7 / 7 |
| Python blocks run | 7 / 7 |
| Blocks matching output fence | 7 / 7 (exact, line-for-line) |
| Formula/check values independently re-derived | all reproduced, **except the 2 hub-table rows in E2/E3** |
| Wikilink targets resolved | 94 / 94 |
| **Genuine errors found** | **6** (2 math wrong-value, 1 math sign, 1 spelling, 2 source/coherence) |
| Minor / nit notes | 5 |

**VERDICT: FAIL** — the six sub-pages are clean on math, code, and derivation; all six defects are concentrated in the **index hub** (4) plus two sub-pages (one spelling, one source number). No code defect anywhere.

---

## 2. ERRORS (must fix)

### E1. Hub "Verified check" column is not what the hub's §3 code computes — `index.md:33`
**Stated:** "the numbers in the check column were **re-executed and reproduced exactly** from the code in §3."
**Problem:** the §3 script emits only `best bid/ask`, `spread`, `mid`, `total resting depth`, `top-2 L2`, and `OFI`. It computes **none** of: queue position, market-order VWAP, effective half-spread, microprice, toxic-fill break-even, or expected wait. 5 of the 11 check rows are unsupported by §3 code; 2 of them (E2, E3) are also wrong for the hub's own book.
> Fix: either add the missing computations to §3, or reword to "…reproduced from the code on the sub-pages" and cite which page.

### E2. Market-order VWAP check value belongs to a different book — `index.md:44`
**Stated:** `Market-order VWAP … 100.002 at Q=250` (formula `\bar p(Q)=\frac1Q\sum_k q_k p_k` "over the swept levels").
**Problem:** the hub's own book has best ask **100.01** (asks `{100.01:200, 100.02:400}`). A 250-lot market buy there VWAPs at **100.012**, not 100.002 (independently re-derived: `(200·100.01 + 50·100.02)/250 = 100.012`). The value 100.002 is correct only for **page 02's** book (`best ask 100.00`, `(200·100.00+50·100.01)/250`). Additionally the hub's displayed formula omits the partial-level term (`min(q_k, max(0, Q−Q_{k-1}))`) that page 02 has, so it *cannot* produce a half-level fill like `Q=250`.
**Correct (hub book):** `100.012 at Q=250`; and adopt page 02's exact `\bar p(Q)=\frac1Q\sum_k \min(q_k,\max(0,Q-Q_{k-1}))\,p_k`.

### E3. Effective half-spread check is infeasible in the hub's book — `index.md:45`
**Stated:** `Se = 0.013 at Q=1000`.
**Problem:** the hub book holds only **600 lots** of total ask depth (200+400), so a `Q=1000` market buy cannot exist there; and `0.013` is the *slippage* figure from page 02's book, with an implied midquote $m=100.00$ that is also page-02's, not the hub's ($m=100.005$). `Se = d(p−m)` for the hub book would use $m=100.005$.
> Fix: mark this row as a page-02 example, or recompute against the hub book (e.g. a `Q` within its 600-lot depth).

### E4. Queue-reactive up-tick probability contradicts its own stated monotonicity — `06-advanced-extensions.md:59`
**Stated:**
$$P(\text{up-tick}\mid q^b,q^a)=\Phi\!\left(\frac{q^b-\bar q^b}{\theta^b}\right)\cdot\Psi\!\left(\frac{q^a-\bar q^a}{\theta^a}\right),$$
with the prose "**rising with bid-heavy and ask-light queues**."
**Problem:** with $\Phi,\Psi$ the usual increasing (CDF-like) factors, the ask term $\Psi\big((q^a-\bar q^a)/\theta^a\big)$ **increases** in $q^a$ — i.e. it *falls* when asks are light. So the displayed formula **decreases** with ask-light queues, the opposite of the claim. Numeric check ($\bar q=500,\ \theta=200,\ q^b=800,\ q^a=300$): as written $P=0.148$; flipping the ask-term sign to $( \bar q^a-q^a)/\theta^a$ gives $P=0.785$ — the "ask-light ⇒ higher up-tick" direction the text promises.
**Correct:** either flip the ask argument to $\Psi\!\big((\bar q^a-q^a)/\theta^a\big)$, or state that $\Psi$ is decreasing (and define $\Phi,\Psi$).

### E5. Hasbrouck IBM/Island stub value contradicts the verified corpus — `02-limit-vs-market-orders.md:62`
**Stated:** "bids at \$112.50, \$110.00, \$108.00, and a **\$.63** stub — … printing a stair-step of prices."
**Corpus (`hasbrouck_ch1-5.md:35`, verified):** "IBM/Island ECN example: \$112.50, \$110.00, \$108.00, **\$2.63** bids." The page's "\$.63" matches no value in the source record — a dropped digit (the corpus' own "\$2.63" as a *fourth bid price* is itself questionable, so reconcile against Hasbrouck (2007) p. ~10 rather than trusting either blindly).
> Fix: verify the fourth level against the primary text and make page and corpus agree.

### E6. Typo — `06-advanced-extensions.md:23`
**Stated:** `| **Makidian / queueing** | Markov chain in queue sizes …`
**Correct:** **Markovian** / queueing. ("Makidian" is not a word; the same row's description already says "Markov chain".)

---

## 3. Math verified correct (independent re-derivation)

Every boxed formula and every worked number below was re-derived independently (hand algebra + a from-scratch script); all agree with the pages to the printed precision.

| Location | Formula / result | Verdict |
|---|---|---|
| `index:39-43` | $b_t=\max\{\text{bids}\}$, $a_t=\min\{\text{asks}\}$; $s=a-b$; $m=\tfrac12(a+b)$; depth $D_t(p)=\sum\mathbf1\{p_i=p\}q_i$ | correct (100.00 / 100.01 / 0.01 / 100.0050 / 1400) |
| `index:43` | queue position $Q_0=\sum\mathbf1\{t_i<t_0\}q_i = 300$ | correct |
| `index:46-48` | `OFI`$=I^b-I^a=-50$; microprice $m^\text{micro}=(q^b a+q^a b)/(q^b+q^a)\in[b,a]$; toxic EV $h-\pi J$, $\pi^\star=h/J=0.20$ | correct |
| `index:49` | $\mathbb E[T]\approx(Q_0+s)/\mu = 10.5$ s at $Q_0{=}1000$ | correct (μ=100, s=50) |
| `index:51-55` | price-time key $(-p_i,t_i)/(p_j,t_j)$; pro-rata split $x q_i/\sum q_j$ | correct |
| `01:37,41` | batch auction $\text{Demand}(P)=\sum_{p_i\ge P}q_i$, $\text{Supply}(P)=\sum_{p_j\le P}q_j$, $P^\star=\arg\max\min(D,S)$ | correct — table & clearing $P^\star{=}100.05$, $V^\star{=}800$ reproduced exactly |
| `02:34` | walk VWAP $\bar p(Q)=\frac1Q\sum_k\min(q_k,\max(0,Q-Q_{k-1}))p_k$ | correct — all six rows (100.000/100.002/100.006/100.013/100.0315) reproduced |
| `02:40-44` | $Se=d(p-m)$; $Se=\tfrac12 s$ single-tick at ask; $\Delta m_t=\lambda q_t+\varepsilon_t$, depth $1/\lambda$ | correct (FPR eqs 2.3 / 2.8, confirmed in `foucault_ch1-3.md`) |
| `02:48` | $\mathbb E[\pi_\text{fill}]=h-\pi J$, $h=\tfrac12 s$, negative past $\pi^\star=h/J$ | correct |
| `03:32-40` | L3 state map; depth functions on tick grid $\delta\mathbb Z$; $b_t,a_t,s_t,m_t$ | correct |
| `03:54-57` | imbalance $I_t=(q^b-q^a)/(q^b+q^a)\in[-1,1]$; microprice leans away from the heavy side | correct |
| `04:32` | key $(\text{buy})=(-p_i,t_i)$, $(\text{sell})=(p_j,t_j)$; maker's (older) price prevails | correct (matches Hasbrouck §2.1) |
| `04:38-43` | engine loop; "crosses" $p^\star\!\le\! L$ buy / $p^\star\!\ge\! L$ sell; remainder rests at $L$ | correct |
| `04:47` | pro-rata `fill`$_i=\min(q_i, xq_i/\sum q_j)$ | correct |
| `04:53-57` | $\text{filled}(t)=\min(s,\max(0,E_t-Q_0))$; $P(E_t\ge Q_0{+}s)=1-\sum_{k=0}^{Q_0+s-1}e^{-\mu t}(\mu t)^k/k!$ | correct |
| `04:63`, `05:45` | $P(\text{adverse before fill})\approx\nu/(\nu+\mu/Q_0)\to1$ as $Q_0\uparrow$ | correct |
| `05:34-39` | $\pi_\text{fill}=\{h,\ h-J\}$, $\mathbb E=h-\pi J$, $\pi^\star=h/J$ | correct (break-even π=0.20; all rows reproduced) |
| `05:49` | $\mathbb E[T]\approx(Q_0+s)/\mu$ | correct |
| `05:55-59` | $P(\text{picked off})=1-e^{-\mu_\text{mo}\delta}$; $\text{Loss}=\lambda(1-e^{-\mu_\text{mo}\delta})(J-h)\approx\lambda\mu_\text{mo}\delta(J-h)$ | correct — all three latency rows (0.0200/0.1951/1.5739) reproduced |
| `06:35-38` | Markov-chain event jumps $Q_i\pm\eta$, market order depletes best levels | correct |
| `06:45-53` | OFI per-event $I^b_t,I^a_t$ (three-branch cases) and $\Delta m_t=\beta\,\text{OFI}_t+\varepsilon_t$, slope $\propto 1/$depth; microprice | correct (three-branch signs match the §3 code exactly) |
| `06:65` | Hawkes $\lambda(t)=\mu+\sum_{t_i<t}\phi(t-t_i)$, $\phi\ge0$, branching ratio $n=\int_0^\infty\phi<1$ | correct |

---

## 4. Code

All **7** ```` ```python ```` blocks execute with `rc=0` and reproduce their output fences **exactly, line-for-line** (including the seeded number-cruncher on page 06: `events kept = 23051`, `mean spread = 0.0428`, shallow β = 2.2594e-03 / R² 0.6231, deep β = 1.6781e-03 / R² 0.3795). No stdout/assert/stderr discrepancies.

| File | Block (line) | ran | matches fence |
|---|---|---|---|
| `index.md` | 63 | ✅ | ✅ |
| `01-from-zero-intuition.md` | 57 | ✅ | ✅ |
| `02-limit-vs-market-orders.md` | 70 | ✅ | ✅ |
| `03-the-limit-order-book.md` | 76 | ✅ | ✅ |
| `04-matching-and-priority.md` | 73 | ✅ | ✅ |
| `05-failure-modes-and-practice.md` | 69 | ✅ | ✅ |
| `06-advanced-extensions.md` | 75 | ✅ | ✅ |

Note: the page-05 Monte-Carlo values (`+0.00501`, `-0.00250`) are seed-dependent (`random.seed(7)`) and reproduced identically.

---

## 5. Coherence / links / jargon

- **Wikilinks:** 94 / 94 resolve (folder-path links such as `[[pillars/06-market-making/limit-order-book-mechanics|…]]` resolve to that folder's `index.md`; consistent with the repo-wide convention). No broken targets.
- **Hub ↔ page-01 prerequisite:** coherent — `index.md:12` scopes the folder-level prereqs to pages 02–06 and explicitly carves out page 01 ("states its own, smaller, entry requirements"), which `01:11` gives as "none". No contradiction.
- **Sub-page chain:** 02→03→04→05→06 prerequisites are consistent; 06 correctly requires `04` and `05`.
- **Cross-page consistency of shared quantities:** `h=0.01, J=0.05, π*=0.20`, `μ=100`, `Q_0` queue-race formula, and the toxic-fill identity agree across hub / 02 / 04 / 05. No contradictions found.
- **Source fidelity of citations:** Cont–Stoikov–Talreja (2010) OR 58(3) 549–563, Cont–Kukanov–Stoikov (2014) JFE 12(1) 47–88, Gould et al. (2013) QF 13(11), Bouchaud–Mézard–Potters (2002) QF 2(4) 251–256, Smith et al. (2003) QF 3(6) 481–514, Parlour (1998) RFS 11(4), Foucault–Kadan–Kandel (2005) RFS 18(4), Rosu (2009) RFS 22(11), Huang–Lehalle–Rosenbaum (2015) JSM, Menkveld–Zoican (2017), Hasbrouck §1.2 "depth/breadth/resiliency", Hasbrouck §2.1 I/O, FPR eqs 2.3/2.8 and Fig 3.8–3.9 — **all match** `corpus/` records. (Only E5's IBM stub number is off.)

### Minor / nit notes (not counted as errors)
1. `index.md:48` and `05:139` write the toxic-fill identity as $\mathbb E[\pi]=h-\pi J$, using the symbol $\pi$ for **both** the informed probability and the payoff (page 05's box at `05:35` correctly uses $\pi_\text{fill}$). Consider $\mathbb E[\pi_\text{fill}]$ for consistency.
2. Mixed spelling convention: `01:39` "maximizes" (−ize) against the folder's otherwise British forms ("summarised", "formalise", "optimisation", "modelled", "artefacts", "behaviour"). Pick one.
3. `index.md:135`, `03:170`, `03:191`, `04:190`, `05:163`, `06:51,189` describe this hub as a separate "**Sibling data page** … Limit Order Book Mechanics & L3 Data" — but the link target *is* this folder's `index.md`, whose own frontmatter title is "Limit Order Book Mechanics: Topic Hub & Formula Lookup". A reader is sent back to the page they are on; align the alias/title (or point to a genuinely distinct page).
4. Jargon first-use: `03:170` uses **OFI** without defining it on page 03 (defined only in the hub and page 06); `05:41,143` use **VPIN**/**OFI** without in-page expansion. Cheap one-clause definitions would fix it.
5. `03:38` renders the inline escape `e.g.\ $δ=$0.01$` — the stray `\ ` is a LaTeX artifact in the prose.

---

## 6. Fix list (priority order)

1. `index.md:44` → VWAP check `100.002` is wrong for the hub book (should be `100.012`); adopt page 02's partial-level formula. **(E2)**
2. `index.md:45` → `Se=0.013 at Q=1000` infeasible in the hub book; relabel or recompute. **(E3)**
3. `06:59` → flip the ask term sign (or define Ψ) so the formula matches "rising with bid-heavy and ask-light queues". **(E4)**
4. `02:62` → reconcile `$.63` vs corpus `$2.63` against Hasbrouck (2007). **(E5)**
5. `06:23` → "Makidian" → "Markovian". **(E6)**
6. `index.md:33` → correct the "reproduced exactly from the code in §3" claim. **(E1)**

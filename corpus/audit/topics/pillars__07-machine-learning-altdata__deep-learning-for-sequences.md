# Audit Report — `content/pillars/07-machine-learning-altdata/deep-learning-for-sequences/`

Scope: 7 files (`index.md` + `01`..`06`). Sole adversarial reviewer. Audited spelling/typos (prose only; code & LaTeX excluded), every boxed formula and worked numeric example (RNN/LSTM/GRU gates, sequence-to-vector / seq2seq, temporal CNN, attention, positional encoding, walk-forward training, early stopping, effective-sample overfitting), every ` ```python ` block (run in a fresh interpreter, chained per page where a page has several; stdout byte-diffed against the trailing output fence), and cross-page coherence (prereqs, jargon, wikilinks, contradictions).

Environment: `python3` at `/home/alfred/.local/share/mise/installs/python/latest/bin/python3`, numpy 2.5.3. (Note: the Hermes interpreter lacks numpy — the first pass failed with `ModuleNotFoundError`; all figures below are from the numpy-equipped interpreter.)

## 1. Verdict

**ACCEPT_WITH_FIXES.** The folder is in good shape. All **7/7** `python` blocks execute (exit 0) and every byte of stdout matches its documented output fence exactly; all **20** unique wikilinks resolve to real files/`index.md`; no spelling/typo, doubled-word, or malformed-sentence issues were found in prose (pyspellchecker scan over fence-stripped, math-stripped prose returned only acronyms, British spellings, and author surnames — zero true typos). Every boxed formula is correct: vanilla-RNN state, BPTT Jacobian chain, exploding-gradient bound, LSTM gate set + additive cell update + CEC gradient, scaled dot-product attention + causal mask + multi-head, linear-AE loss, Eckart–Young / Baldi–Hornik, TCN dilated-causal conv, TCN receptive field, GRU gate set, and the seq2seq attention context.

Two real defects remain, both prose numeric claims, plus one low-severity notation nit:

1. **`02:158` (MEDIUM, wrong stated constant).** "The vanilla RNN at $W{=}0.9$ loses **ten orders of magnitude** between $T{=}10$ ($8.6\times10^{-4}$) and $T{=}20$ ($8.7\times10^{-11}$)." The actual drop is a factor of $9.9\times10^{6}$, i.e. **~7 orders of magnitude** (`log10(8.638e-4/8.660e-11) = 6.999`). "Ten" is wrong; should be "seven" (the numbers themselves are correct).
2. **`index:40` (LOW, horizon-mismatched comparator / hub↔02 contradiction).** The CEC row reads "$f{=}0.99,T{=}50\Rightarrow 0.605$ (vs $8.7\times10^{-11}$ RNN)". `8.660e-11` is the RNN value at **$T{=}20$**, while the LSTM figure is at **$T{=}50$** — at the matching $T{=}50$ the RNN gradient is $5.4\times10^{-27}$. The parenthetical therefore implies a ~10-order gap while `02:158` states the same comparison as **26 orders** (correct: $0.605/5.429\times10^{-27}=1.1\times10^{26}$). Fix the comparator to $5.4\times10^{-27}$ (or label it "$T{=}20$ RNN").
3. **`04:42` (LOW, notation).** The Baldi–Hornik theorem states $\mathcal L^\star=\sum_{j>k}\sigma_j^2$, but §2.1 defines $\mathcal L(E,D)=\tfrac1n\sum_i\|x_i-DEx_i\|_2^2$ with a $1/n$ prefactor. The consistent statement is $\mathcal L^\star=\tfrac1n\sum_{j>k}\sigma_j^2$ (the code's `pca_mse` additionally divides by $d$, i.e. it reports a per-entry MSE — the numbers agree, only the formula's normalisation is loose).

No wrong signs, inverted directions, or incorrect constants were found in any boxed formula or any other worked example.

## 2. Issues table

| File:Line | Problem (stated) | Correct | Severity |
|---|---|---|---|
| 02:158 | "loses **ten orders of magnitude** between $T{=}10$ ($8.6\times10^{-4}$) and $T{=}20$ ($8.7\times10^{-11}$)" | $\log_{10}(8.638\times10^{-4}/8.660\times10^{-11})=6.999\Rightarrow$ **seven** orders of magnitude. | **MEDIUM** (wrong constant in prose) |
| index:40 | CEC row: "$f{=}0.99,T{=}50\Rightarrow 0.605$ (vs $8.7\times10^{-11}$ RNN)" | $8.7\times10^{-11}$ is the RNN at $T{=}20$; the LSTM figure is $T{=}50$. At $T{=}50$ the RNN is $5.4\times10^{-27}$, giving the "26 orders" quoted in 02:158. Use the matched-$T$ value. | **LOW** (numeric / coherence) |
| 04:42 | Theorem: $\mathcal L^\star=\sum_{j>k}\sigma_j^2$ | With $\mathcal L$ defined (§2.1) as a $1/n$-averaged loss, $\mathcal L^\star=\tfrac1n\sum_{j>k}\sigma_j^2$. | **LOW** (notation) |

No spelling typos, no doubled words, no broken sentences found in prose (code fences and LaTeX excluded). pyspellchecker flagged only acronyms (`rnn`, `lstm`, `gru`, `tcn`, `bptt`, `cec`, `svd`, `snr`, `afml`, `ieee`, `tsp`…), British spellings (`factorisation`, `generalises`, `optimisation`, `minimise`, `penalise`, `centred`, `summarises`, `maximising`, `parallelisable`…), and prominent author surnames (`Bengio`, `Schmidhuber`, `Kolter`, `Koltun`, `Zohren`, `Polson`, `Witte`, `Hornik`, `Xiu`, `Tibshirani`, `López`, `KyungHyun`, `Sercan`, `Ashish`, `Sepp`, `Ruey`).

### Observations (not counted as errors)

- **Sequence-to-vector**: the brief lists it; the folder covers the sequence families (RNN many-to-one, seq2seq encoder–decoder, vector-to-vector autoencoder) without using the exact term "sequence-to-vector". Coverage is adequate — flagging so the reviewer-of-record knows the exact-phrase check was vacuous.
- **TCN receptive field vs Bai et al.**: the boxed $R=(K-1)(2^L-1)+1$ is *correct for this folder's construction* (one dilated causal conv per layer, dilations $1,2,4$; $K{=}2,L{=}3\Rightarrow 8$, code-verified). The Bai/Kolter/Koltun reference TCN stacks two convs per residual block, which would give $2(K-1)(2^L-1)+1$; the page is internally consistent (text and code match), so this is a convention note, not a defect.
- **`index:40`** otherwise correct: the LSTM figure $0.605$ matches the code ($6.050\times10^{-1}$).
- The AFML "no deep-learning chapter / Ch. 19 = Microstructural Features" caveat is repeated on the hub, p.03, p.04 and p.05 — deliberate anti-mis-citation guardrail, consistent across pages.

## 3. Math verified

Every boxed formula and prose number was re-derived and/or re-executed (numpy 2.5.3):

- **Vanilla RNN** $h_t=\tanh(Wh_{t-1}+Ux_t+b)$ ✓; **output** $\hat y_t=\operatorname{softmax}(Vh_t+b_y)$ ✓.
- **BPTT Jacobian (02.2.2 / hub)** $\partial h_T/\partial h_k=\prod_{t=k+1}^T\operatorname{diag}(1-h_t^2)W$ ✓ (since $\tanh'(a_t)=1-h_t^2$).
- **Exploding bound** $\|\partial h_T/\partial h_0\|\le\|W\|^T$, $\|W\|>1$ explodes ✓.
- **Gradient decay** — code reproduces hub's headline $W{=}0.9,T{=}20\Rightarrow8.660\times10^{-11}$ ✓; $T{=}50\Rightarrow5.429\times10^{-27}$ ✓.
- **LSTM gates** $f,i,o\in(0,1)$ via $\sigma$; $\tilde C_t=\tanh(W_ch_{t-1}+U_cx_t+b_c)$; $C_t=f_t\odot C_{t-1}+i_t\odot\tilde C_t$; $h_t=o_t\odot\tanh(C_t)$ ✓ (hand-worked step $t{=}0$: $f{=}\sigma(0.2){=}0.550$, $i{=}\sigma(-0.3){=}0.426$, $g{=}\tanh(0.2){=}0.197$, $C_0{=}0.0840$, $h_0{=}0.0461$ — matches fence).
- **CEC gradient** $\partial C_T/\partial C_t=\prod_{s}f_s$; $f{=}0.99,T{=}50\Rightarrow0.605$ ✓ ($6.050\times10^{-1}$); $26$ orders vs $5.429\times10^{-27}$ RNN ✓.
- **Scaled dot-product attention** $\operatorname{Attn}(Q,K,V)=\operatorname{softmax}(QK^\top/\sqrt{d_k}+M)V$ ✓; $q\cdot k$ has variance $d_k$, std $\sqrt{d_k}$ ✓.
- **Causal mask** $M_{ij}=-\infty$ for $j>i$, $0$ else ✓; code proves $\operatorname{triu}(W,1)=0$ exactly, rows sum to 1, position 0 attends only to itself ✓.
- **Scaling argument** — code: stdev $1.45\to8.96\to15.73$ at $d_k{=}4/64/256$; unscaled entropy $1.776\to0.158$; scaled $1.979\to1.753$; $\ln 8=2.079$ ✓.
- **Multi-head** $\operatorname{Concat}(\text{head}_1,\dots,\text{head}_h)W^O$, $\text{head}_m=\operatorname{Attn}(QW^Q_m,KW^K_m,VW^V_m)$ ✓; post-norm residual block $\operatorname{LayerNorm}(x+\text{MultiHead}(x))$ ✓; positional encodings needed for permutation-invariance ✓.
- **Linear-AE loss** $\mathcal L=\tfrac1n\sum_i\|x_i-DEx_i\|_2^2$ ✓; **Eckart–Young** $\hat X_k=U_k\Sigma_kV_k^\top$, $E=V_k^\top,D=V_k$ ✓; **Baldi–Hornik** linear AE $=$ top-$k$ PCA subspace ✓ (code: AE MSE $0.1714=$ PCA MSE, gap $-0.000\%$, $\cos$(principal angles)$=[1,1,1]$, rank-3 PCA captures $99.6\%$).
- **Sparse-AE** $L=\|x-Dz\|_2^2+\lambda\|z\|_1$ ✓.
- **TCN dilated causal conv** $(F*_d x)(t)=\sum_{k=0}^{K-1}f_k\,x_{t-dk}$ ✓; **receptive field** $R=(K-1)(2^L-1)+1$, $K{=}2,L{=}3\Rightarrow8$ ✓ (code-verified; causality proven by perturbing input[15] → only output[15] moves).
- **GRU** $z_t=\sigma(W_zh_{t-1}+U_zx_t)$, $r_t=\sigma(W_rh_{t-1}+U_rx_t)$, $\tilde h_t=\tanh(W(r_t\odot h_{t-1})+Ux_t)$, $h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t$ ✓; "2 gates vs LSTM's 3" ✓.
- **Seq2seq attention** $c_i=\sum_t\alpha_{it}h_t$, $\alpha_{it}=\operatorname{softmax}_t(\operatorname{score}(s_{i-1},h_t))$ ✓.
- **Effective sample size** $N_{\text{eff}}\approx N(1-\rho)/(1+\rho)$ ✓ correct AR(1) form; $\rho{=}0.1,N{=}2500\Rightarrow2045.45\approx2045$ ✓.
- **Generalisation gap** $\sim\sqrt{p/N}$ ✓.
- **Worked examples re-executed** — hub (RNN/LSTM/attention/TCN probe); 01: autocorr $+0.527\to+0.003$, run length $5.00\to2.02$, accuracy $0.797\to0.505$; 02: LSTM forward table + gradient/LSTM-path tables; 03: causal weight matrix + entropy-vs-$d_k$; 04: AE MSE $0.1714$, gap $-0.000\%$, $99.6\%$ variance, angles $[1,1,1]$; 05: noise $R^2$ blow-up ($p{=}40$: train $1.000$, OOS $-834.3$), ridge $\lambda$ sweep, AR(2) in-regime $+0.757$ / out-regime $-0.680$; 06: TCN output ramp + RF $8$ + GRU table. **All match the documented fences exactly.**

**Not-checkable:** none — every listed item was exercised. ESL eq. numbers on 04/05 were not cross-checked against `corpus/verified/esl_*.md` (not required for the deep-learning folder; flagged for awareness).

## 4. Code run / match stats

| File | Block | Runs (exit 0) | Stdout matches doc | Blocks |
|---|---|---|---|---|
| index.md | §3 architecture probe (RNN/LSTM/attention/TCN) | ✓ | ✓ | 1 |
| 01-from-zero-intuition.md | shuffle-destroys-order (stdlib) | ✓ | ✓ | 1 |
| 02-rnns-and-lstms.md | LSTM forward + vanishing gradient | ✓ | ✓ | 1 |
| 03-attention-and-transformers.md | causal attention + $\sqrt{d_k}$ scaling | ✓ | ✓ | 1 |
| 04-autoencoders-for-factors.md | linear AE vs PCA | ✓ | ✓ | 1 |
| 05-failure-modes-and-practice.md | overfitting / ridge / non-stationarity | ✓ | ✓ | 1 |
| 06-advanced-extensions.md | causal dilated conv + GRU | ✓ | ✓ | 1 |

**Total `python` blocks: 7. Executed: 7. Stdout matches: 7.** Each page has exactly one `python` block, so no intra-page chaining was needed; every block was still run to completion in a fresh interpreter (exit 0, no warnings/tracebacks).

## 5. Coherence

- **Hub vs sub-pages:** hub lookup table, §4 four signposts, §5 references and §6 reading route all agree numerically and thematically with `01`–`06`. The only numeric disagreement is the CEC-comparator mismatch in §2 (issue 2: hub implies ~10 orders, page 02 states 26). §2 headline $0.605$ and $8.66\times10^{-11}$ values agree with §3 code and with page 02.
- **Prereqs:** hub declares folder-level prereqs (Calculus & Optimization, Financial ML Pitfalls; classical ancestor = Kalman) and explicitly defers page `01`'s smaller entry bar to itself — page `01` correctly states only "Financial ML Pitfalls & Low SNR". Per-page prereqs form a consistent DAG: 02←01; 03←02; 04←01(+Feature Eng.); 05←02,04; 06←02,03. Back/Continue links form a clean 01→02→…→06 chain.
- **Jargon:** RNN/LSTM/GRU/TCN/BPTT/CEC/seq2seq/DeepAR/TFT/DeepLOB are all defined at first use; the CEC ("constant-error-carousel") is defined on 02 and reused correctly. No undefined jargon found.
- **Links:** 20/20 unique wikilinks resolve (verified against the filesystem). Cross-pillar targets `financial-ml-pitfalls-and-low-snr/*`, `purged-cross-validation-and-backtest-hygiene/*`, `tree-based-factor-ranking-and-purged-cv`, `financial-nlp-and-transcripts/*`, `regime-classification-hmm-and-gmm/*`, `deep-learning-for-sequential-data`, the `foundations/*` and `pillars/01`/`02`/`06` targets all exist.
- **Contradictions:** none beyond issue 2. The non-stationarity figure $+0.76/-0.68$ is consistent between 01, 05. The $10^6$–$10^9$ large-$N$ regime is consistent between hub and 05's decision table.
- **Citations:** Deep Learning Ch. 10/14, Vaswani 2017, Hochreiter & Schmidhuber 1997, Cho 2014, Bai/Kolter/Koltun 2018, Salinas 2020 (DeepAR), Lim 2021 (TFT), Zhang/Zohren/Roberts 2019 (DeepLOB), Gu/Kelly/Xiu 2020, Bailey & López de Prado 2014, Baldi & Hornik 1989, Eckart & Young 1936, Hinton & Salakhutdinov 2006 — all real and correctly attributed; the repeated AFML "no DL chapter" correction is accurate.

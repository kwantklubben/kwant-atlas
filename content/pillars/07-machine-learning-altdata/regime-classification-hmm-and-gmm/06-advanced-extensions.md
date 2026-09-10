---
title: "06 — Advanced Extensions: Regime-Conditional ML & Supervised Regime Labeling"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - regime-conditional-ml
  - supervised-learning
  - mixture-of-experts
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM]], [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM]], and [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Regimes are rarely the end goal — they are the **condition** under which a trading model should behave differently. This page is the launchpad for *using* regimes in ML pipelines, in three escalating moves:

1. **Supervised regime labeling.** If you have a regime *proxy* (a VIX threshold, an NBER flag, a drawdown rule), you don't need clustering — train a **classifier** (logistic, tree) to predict the regime from features, and the regime becomes a target column in a standard supervised pipeline (ties to [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]]).
2. **Regime-conditional models.** Fit a **separate** prediction model per regime ($\hat f_0,\hat f_1$) instead of one global model. When the regime's relationship to the features truly differs, the conditional model dominates.
3. **Soft regime weighting (mixture-of-experts).** Because the regime call is uncertain (and label error is the killer from [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]), the robust move is to blend the per-regime predictions by the regime *posterior probability*: $\hat y=\sum_k P(z{=}k\mid x)\hat f_k(x)$. This is exactly how an HMM's filtered probability is used downstream, and it inherits all the machinery of [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|EM]].

> **The one-sentence essence.** "A regime is the *context* of a prediction; regime-conditional ML fits one model per regime and blends them by the regime probability — and the blending must be *soft*, because hard regime switches are where label error bites."

---

### 2. Mathematical Ground Truth & Derivations

**Supervised labeling.** With a proxy label $z_t\in\{0,1\}$ and features $x_t$, logistic regression models
$$\mathbb{P}(z_t{=}1\mid x_t)=\sigma(w^{\!\top}x_t)=\frac{1}{1+e^{-w^{\!\top}x_t}},$$
fit by maximum likelihood (gradient ascent on the cross-entropy). The fitted probabilities $\hat p_t$ are the regime membership used downstream. (This is the ESL Ch 4 linear-classifier view; the tree/boosted version is [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting]].)

**Regime-conditional forecast.** Split the training data by regime, fit $\hat f_0$ on $\{(x_t,y_t):z_t{=}0\}$ and $\hat f_1$ on $\{z_t{=}1\}$, then predict
$$\hat y_t^{\text{cond}}=\mathbb{1}[z_t{=}0]\,\hat f_0(x_t)+\mathbb{1}[z_t{=}1]\,\hat f_1(x_t).$$
If the two regimes have *opposite* relationships (momentum in calm, mean-reversion in stress), a single pooled $\hat f$ averages them toward zero — a **biased** predictor in both regimes — while the conditional model nails each.

**Soft mixture (regime-weighted).** Replace the hard indicator with the regime posterior:
$$\hat y_t^{\text{soft}}=\mathbb{P}(z_t{=}0\mid x_t)\,\hat f_0(x_t)+\mathbb{P}(z_t{=}1\mid x_t)\,\hat f_1(x_t).$$
This is the finite-mixture / mixture-of-experts predictor (ESL Ch 14; Jacobs et al. 1991), and it is robust to label error: a mislabeled hard switch applies the *wrong sign* model, whereas the soft weight merely down-weights the less-certain expert. This is the same logic that makes the HMM's **filtered** probability ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]) the correct object to feed a live strategy rather than a hard decoded state.

---

### 3. Computational Implementation — label, then condition, then blend

Two regimes with genuinely opposite dynamics (calm: positive drift + momentum; stress: negative drift + mean-reversion). Pipeline: (1) train a **logistic labeler** on features → OOS regime calls; (2) fit **global**, **per-regime (hard)**, and **soft-mixture** forecasters; (3) compare OOS MSE. Stdlib only.

```python
import math, random

def sim(T=2000, seed=6):
    random.seed(seed)
    A=[[0.95,0.05],[0.10,0.90]]            # ~67% calm days
    st=[0]*T; r=[0.0]*T; s=0
    for t in range(T):
        s = 0 if random.random()<A[s][0] else 1
        st[t]=s; prev = r[t-1] if t>0 else 0.0
        r[t] = (+0.004+0.6*prev+random.gauss(0,0.002)) if s==0 \
          else (-0.004-0.6*prev+random.gauss(0,0.003))
    return st,r

def rolling(x,w):
    out=[]
    for t in range(len(x)):
        win=x[max(0,t-w+1):t+1]; m=sum(win)/len(win)
        out.append(math.sqrt(sum((v-m)**2 for v in win)/len(win)))
    return out

st,r=sim(); T=len(st)
vol20=rolling(r,20); vol5=rolling(r,5)
def feats(t):
    prev=r[t-1] if t>0 else 0.0
    return [1.0, prev, abs(prev), vol20[t], vol5[t]]

def logreg(X,y,iters=2000,lr=0.3,seed=1):
    rnd=random.Random(seed); w=[rnd.gauss(0,0.05) for _ in range(len(X[0]))]
    for _ in range(iters):
        for xi,ti in zip(X,y):
            p=1/(1+math.exp(-sum(wi*xi[i] for i,wi in enumerate(w))))
            for i in range(len(w)): w[i]+=lr*(ti-p)*xi[i]
    return w
def prob(w,X): return [1/(1+math.exp(-sum(wi*xi[i] for i,wi in enumerate(w)))) for xi in X]

tr=1000
X=[feats(t) for t in range(1,T)]; y=st[1:]         # target = regime at t+1
w=logreg(X[:tr],y[:tr]); probs=prob(w,X[tr:])
pred=[1 if p>0.5 else 0 for p in probs]
agree=sum(1 for a,b in zip(pred,y[tr:]) if a==b)/len(y[tr:])
print(f"supervised logistic regime labeler: OOS regime agreement = {100*agree:.1f}%")

def ols(Xr,yv):
    p=len(Xr[0]); n=len(Xr); G=[[0.0]*p for _ in range(p)]; b=[0.0]*p
    for xi,yi in zip(Xr,yv):
        for i in range(p):
            for j in range(p): G[i][j]+=xi[i]*xi[j]
            b[i]+=xi[i]*yi
    for i in range(p): G[i][i]+=1e-6
    A=[row[:] for row in G]; bb=b[:]
    for c in range(p):
        for rr in range(c+1,p):
            f=A[rr][c]/A[c][c]
            for cc in range(c,p): A[rr][cc]-=f*A[c][cc]
            bb[rr]-=f*bb[c]
    coef=[0.0]*p
    for rr in range(p-1,-1,-1):
        coef[rr]=(bb[rr]-sum(A[rr][c]*coef[c] for c in range(rr+1,p)))/A[rr][rr]
    return coef
def pv(coef,Xr): return [sum(c*xi[i] for i,c in enumerate(coef)) for xi in Xr]
def mse(ys,pr): return sum((a-b)**2 for a,b in zip(ys,pr))/len(ys)

Xa=[feats(t) for t in range(1,tr)]; ya=[r[t+1] for t in range(1,tr)]
wG=ols(Xa,ya)
w0=ols([feats(t) for t in range(1,tr) if st[t+1]==0],[r[t+1] for t in range(1,tr) if st[t+1]==0])
w1=ols([feats(t) for t in range(1,tr) if st[t+1]==1],[r[t+1] for t in range(1,tr) if st[t+1]==1])
ts=list(range(tr,T-1)); y_tgt=[r[t+1] for t in ts]; X_te=[feats(t) for t in ts]
mse_glob=mse(y_tgt,pv(wG,X_te))
reg_pred=[1 if p>0.5 else 0 for p in probs]
mse_rc=mse(y_tgt,[sum(c*feats(t)[i] for i,c in enumerate((w1 if reg_pred[k]==1 else w0))) for k,t in enumerate(ts)])
pred_soft=[(1-probs[k])*sum(c*feats(t)[i] for i,c in enumerate(w0))+probs[k]*sum(c*feats(t)[i] for i,c in enumerate(w1)) for k,t in enumerate(ts)]
mse_soft=mse(y_tgt,pred_soft)
mse_or=mse(y_tgt,[sum(c*feats(t)[i] for i,c in enumerate((w1 if st[t+1]==1 else w0))) for t in ts])

print(f"\nregime-conditional forecast of next-day return (OOS {len(ts)} rows)")
print(f"  global (single) model          MSE = {mse_glob:.6e}")
print(f"  conditional + PREDICTED regime MSE = {mse_rc:.6e}   improvement {(mse_glob-mse_rc)/mse_glob*100:+.1f}%")
print(f"  SOFT regime-weighted (mixture) MSE = {mse_soft:.6e}   improvement {(mse_glob-mse_soft)/mse_glob*100:+.1f}%")
print(f"  conditional + TRUE regime      MSE = {mse_or:.6e}   (oracle upper bound, improvement {(mse_glob-mse_or)/mse_glob*100:+.1f}%)")
```
```
supervised logistic regime labeler: OOS regime agreement = 85.4%

regime-conditional forecast of next-day return (OOS 999 rows)
  global (single) model          MSE = 2.981821e-05
  conditional + PREDICTED regime MSE = 3.242955e-05   improvement -8.8%
  SOFT regime-weighted (mixture) MSE = 2.819108e-05   improvement +5.5%
  conditional + TRUE regime      MSE = 1.198914e-05   (oracle upper bound, improvement +59.8%)
```

The table is the whole lesson of the folder, in four rows. **Global** is the naive single-model baseline. **Oracle** (true regime, an upper bound) improves $59.8\%$ — there is a *huge* regime-conditional edge to capture. But a **hard** switch on the *predicted* regime *loses* ($-8.8\%$): with opposite-sign regime models, the ~15% of mislabeled days apply the wrong sign and destroy the gain. The **soft mixture** — weighting the two per-regime models by the classifier's posterior — captures a *positive* $+5.5\%$ improvement robustly, because it never commits to a wrong hard label. **That is why real regime-conditional ML blends softly (mixture-of-experts / filtered probability) instead of switching hard.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Hard regime-switching loses to label error** (measured above: $-8.8\%$ vs soft $+5.5\%$). The regime call is *uncertain*; hard $0/1$ switches apply the wrong sign on mislabeled days. *Fix:* soft posterior weighting.
2. **The supervised label is only as good as its proxy.** If your "regime" label (VIX threshold, drawdown rule) does not align with the *model-relevant* regime, you are conditioning on noise. Validate that the label separates the outcome, not just that it classifies.
3. **Look-ahead again.** If the regime label or the labeler's *features* use future data (e.g. a label built from a full-sample drawdown), the conditional edge is phantom ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]). Train the labeler on PIT features and evaluate OOS.
4. **Per-regime overfitting.** Splitting the data by regime *shrinks* each training set; with few stress days, $\hat f_1$ overfits. *Fix:* shrinkage/regularization per regime (ESL Ch 18) or a shared feature backbone.

---

### 5. Canonical Literature & Study References

- **Jacobs, Jordan, Nowlan & Hinton**, "Adaptive Mixtures of Local Experts," *Neural Computation* 3(1):79–87, 1991 — the mixture-of-experts architecture the soft regime-weighted predictor is an instance of.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* — Ch 4 (logistic regression / linear classifiers for the labeler), Ch 14 (mixtures and soft assignment). *Corpus verified.*
- **Ang & Timmermann**, "Regime Changes and Financial Markets," *ARFE* 4, 2012 — the survey connecting estimated regimes to portfolio choice; the allocation-side payoff of regime-conditional modeling.
- **López de Prado**, *Advances in Financial Machine Learning* — Ch 3/10 (meta-labeling: a secondary model on top of a primary signal — the same "condition on a secondary latent factor" idea), Ch 7 (honest CV). See [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting]] and [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]].

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/ml-for-portfolio/index|ML for Portfolio Construction]] (regime-conditional allocation) · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequential Data]]
- Sibling disciplines: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]] (the supervised labeler) · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged & Embargoed CV]] (honest OOS) · [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|Regime Detection · Advanced Extensions]]

---
title: "06 — Advanced Extensions: Fama–French Factor Models, Combining Factors, and the Factor-Model Regression"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - fama-french
  - factor-models
  - combining-factors
---

**Basic Prerequisites:** [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] and [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

The single-factor pages built the axis; this page builds the **model**. The objective is the question every quantamental portfolio asks: *once I have value, profitability, investment, and quality factors, how do I combine them, and how do I know a portfolio's return is really "alpha" and not just exposure to known factors?* Two instruments answer it:

- **The Fama–French factor construction** — how SMB, HML, RMW, and CMA are literally built (2×3 double-sorts, portfolio arithmetic) from the same accounting data this folder has used all along.
- **The factor regression** — the test that decomposes any portfolio's return into a market loading, a value loading, a profitability loading, etc., plus a residual $\alpha$. If $\alpha\approx0$, the portfolio is just the known factors in disguise; if $\alpha$ is large and stable, you have something new.

The through-line: **a factor model turns "this strategy made money" into "this strategy is long value, short growth, and that's where the return came from."** It is the machine that both *combines* factors and *audits* them — which is why [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] and this page sit side by side.

---

### 2. Mathematical Ground Truth & Derivations

**The Fama–French 2×3 construction (1993; extended 2015).** Independent sorts: two size groups (small/big, split at the NYSE median market cap) and three groups on each of B/M, operating profitability, and investment (30th/70th percentile breakpoints). The intersections give six value-weighted portfolios; each factor is the *average of small and big versions* of a long-short:

$$\text{SMB} = \tfrac{1}{3}\big[\text{avg(S/L,S/M,S/H)} - \text{avg(B/L,B/M,B/H)}\big],$$

$$\text{HML} = \tfrac{1}{2}\big[\text{(S/H + B/H)} - \text{(S/L + B/L)}\big],$$

and analogously $\text{RMW}$ (robust minus weak profitability) and $\text{CMA}$ (conservative minus aggressive investment). Because each factor averages small and big portfolios, SMB/HML/RMW/CMA are **roughly size-neutral** — that neutrality is part of their definition.

**The factor-model regression (Fama–MacBeth; Fama–French 2015).** A portfolio's excess return is regressed on the factor excess returns:

$$R_{it} - R_{ft} = \alpha_i + \beta_i(R_{Mt}-R_{ft}) + s_i\,\text{SMB}_t + h_i\,\text{HML}_t + r_i\,\text{RMW}_t + c_i\,\text{CMA}_t + e_{it}.$$

The intercept $\alpha_i$ is the *abnormal return* unexplained by the factors. The five-factor model (Fama–French 2015) is **rejected** by the strict GRS test — it fails on small stocks that invest a lot despite low profitability — but for applied purposes it gives an acceptable description of average returns. HML averages about **0.38%/month** in the 2×3 construction; RMW and CMA add positive premiums on top.

**Combining factors — composite scores.** The simplest combination that the evidence supports (and that [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] motivated) is a rank-sum: rank the universe on each factor and average the ranks:

$$\text{Composite} = \frac{1}{K}\sum_{j=1}^{K} \text{rank}_j(\text{firm}),$$

so a firm cheap *and* profitable *and* high-quality scores best. Greenblatt's magic formula and Piotroski's F-score are both instances; a factor model tells you how much of that composite's return is incremental.

---

### 3. Computational Implementation — build the 2×3 factors and run the regression, stdlib only

Two halves. First it constructs **SMB and HML** from a 20-stock cross-section using the genuine 2×3 algorithm (size median, B/M 30/70 breakpoints). Then it builds a 48-month time series for the six cells, forms the market and HML factors, and runs an **OLS regression** (via the normal equations) of a value portfolio's return on [market, HML] — showing the portfolio is fully "explained" by the factors, with ~zero alpha.

```python
import statistics as st, random
random.seed(11)
stocks=[]
for i in range(20):                       # name, size(mc), B/M, realized return
    size=random.uniform(500,20000); bm=random.uniform(0.1,1.4)
    ret=0.04+0.05*bm-0.0004*(size/1000.0)+random.gauss(0,0.01)
    stocks.append([chr(65+i),size,bm,ret])
# --- Fama-French 2x3: Size median, B/M 30/70 breakpoints ---
size_med=st.median([s[1] for s in stocks])
bms=sorted([s[2] for s in stocks]); n=len(bms)
lo_bm=bms[n//3-1]; hi_bm=bms[2*n//3-1]
def cell(s): return ('S' if s[1]<size_med else 'B') + \
                   ('L' if s[2]<=lo_bm else ('H' if s[2]>=hi_bm else 'M'))
C={k:[] for k in ['SL','SM','SH','BL','BM','BH']}
for s in stocks: C[cell(s)].append(s)
avg=lambda c: st.mean([x[3] for x in c]) if c else 0.0
SMB=st.mean([avg(C['SL']),avg(C['SM']),avg(C['SH'])])-st.mean([avg(C['BL']),avg(C['BM']),avg(C['BH'])])
HML=st.mean([avg(C['SH']),avg(C['BH'])])-st.mean([avg(C['SL']),avg(C['BL'])])
print("2x3 portfolio sizes:", "  ".join(f"{k}:{len(C[k])}" for k in ['SL','SM','SH','BL','BM','BH']))
print(f"Market = {st.mean([s[3] for s in stocks])*100:.2f}%   SMB = {SMB*100:+.2f}%   HML = {HML*100:+.2f}%")
# --- OLS (stdlib) of the value portfolio on [market, HML], 48 months ---
def ts(base,T=48): return [base/12+random.gauss(0,0.02) for _ in range(T)]
SL,SH,BL,BH=[ts(avg(C[k])) for k in ('SL','SH','BL','BH')]
mkt=[st.mean([SL[t],SH[t],BL[t],BH[t]]) for t in range(48)]
hml=[(SH[t]+BH[t])/2-(SL[t]+BL[t])/2 for t in range(48)]
p=[(SH[t]+BH[t])/2 for t in range(48)]            # value portfolio = long high-B/M
def ols(y,Xs):
    X=[[1.0]+list(r) for r in zip(*Xs)]; k=len(X[0]); m=len(X)
    XtX=[[sum(X[i][a]*X[i][b] for i in range(m)) for b in range(k)] for a in range(k)]
    Xty=[sum(X[i][a]*y[i] for i in range(m)) for a in range(k)]
    A=[r[:] for r in XtX]; b=Xty[:]
    for c in range(k):
        pv=max(range(c,k),key=lambda r:abs(A[r][c])); A[c],A[pv]=A[pv],A[c]; b[c],b[pv]=b[pv],b[c]
        for r in range(c+1,k):
            f=A[r][c]/A[c][c]
            for cc in range(c,k): A[r][cc]-=f*A[c][cc]
            b[r]-=f*b[c]
    x=[0.0]*k
    for r in range(k-1,-1,-1): x[r]=(b[r]-sum(A[r][cc]*x[cc] for cc in range(r+1,k)))/A[r][r]
    return x
a,bb,hh=ols(p,[mkt,hml])
print(f"Value portfolio: R_p = {a*100:+.2f}% + {bb:.2f}*MKT + {hh:.2f}*HML")
print(f"(alpha~0 => the known factors explain the value return; HML loading={hh:.2f} is the value exposure)")
```

```text
2x3 portfolio sizes: SL:4  SM:3  SH:3  BL:2  BM:3  BH:5
Market = 7.26%   SMB = +0.05%   HML = +3.53%
Value portfolio: R_p = -0.00% + 1.00*MKT + 0.50*HML
(alpha~0 => the known factors explain the value return; HML loading=0.50 is the value exposure)
```

*The output is the whole point of a factor model.* HML is +3.53% (value pays); SMB is ≈0 (this cross-section has no size premium). The regression then decomposes the value portfolio: a market loading of **1.00**, a value (HML) loading of **0.50** — it is half value-factor — and an **alpha of −0.00%**. The strategy's return is *fully* attributable to the known factors; it has no hidden edge to claim. That is exactly what a factor model is for: **converting "it made money" into "it is long value," and flagging as alpha only what survives after the known factors are removed.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The 2×3 breakpoints are a modeling choice with real consequences.** NYSE-median size and 30/70 B/M breakpoints are arbitrary (Fama–French 2015 test 2×2 and 2×2×2×2 variants); HML, RMW, and CMA averages differ across constructions. Quote the construction, or the factor is not comparable.
2. **Factors built without controls are confounded.** HML built from a B/M-only 2×3 is *not* neutral to profitability and investment — the regression slopes then don't isolate clean exposures (Fama–French's own caveat). Interpreting the HML *slope* as "pure value" requires controls.
3. **Alpha is a residual, and residuals are the hard part.** $\alpha\approx0$ means "explained," not "no return"; a large $\alpha$ can be a new factor, luck, or a data artifact. Distinguish them with out-of-sample tests and multiple-testing discipline ([[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **The model is rejected by the strict test.** The five-factor model fails the GRS test on small high-investment/low-profitability stocks. It is "acceptable for applied purposes," not the truth — the q-factor model (Hou, Xue & Zhang) and others compete to digest the same anomalies.
5. **Composite ranks hide factor-specific risk.** Averaging ranks on value *and* profitability bundles two exposures; the model regression is what lets you see how much of the composite is each — don't skip it.

---

### 5. Canonical Literature & Study References

- **Fama & French**: "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) — the three-factor model and the SMB/HML construction.
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) — adds RMW and CMA; *the 2×3 construction and the ~0.38%/month average HML return verified against the corpus paper.*
- **Hou, Xue & Zhang**: "Digesting Anomalies: An Investment Approach" (*RFS*, 2015) — the q-factor model (investment + ROE) as the production-theory competitor.
- **Green, Hand & Zhang**: "The Characteristics That Provide Independent Information…" (*RFS*, 2017) — how many factors genuinely matter; the parsimonious 10-signal model.
- **Fama & French**: "Choosing Factors" (*JFE*, 2018) — the selection discipline for what counts as a real factor.
- **Gray & Carlisle**: *Quantitative Value* — the published, transparent combination of value, quality, and earnings-quality signals into a backtested quantamental screen.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Factor-model layer: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]] (Barra/FF model construction, the professional layer) · [[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene & Deflated Sharpe]] (how to audit the alpha)
- Portfolio layer: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (turning factor tilts into an optimized portfolio)
- Screening: [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] · [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|Screening · Advanced Extensions]]

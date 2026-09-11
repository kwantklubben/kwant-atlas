---
title: "F.3.5 Martingales"
tags:
  - foundations
  - probability-and-measure-theory
  - martingales
  - risk-neutral-measure
  - radon-nikodym
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]].

---

### 1. Intuition & Practical Objective

A martingale is **a fair game**: given everything you know at time $s$, the expected value of the future state is the present value, $\mathbb E[M_t\mid\mathcal F_s]=M_s$. It is the mathematical backbone of no-arbitrage pricing because "prices under the risk-neutral measure are martingales" *is* modern pricing (Glasserman eq. 1.39). Crucially, "fair" means fair in *conditional expectation* — a martingale can be enormously volatile (Brownian motion, a discounted price) and still be fair.

The practical objective: understand the *three linked faces* — (1) the martingale/supermartingale/submartingale hierarchy and the discounted-stock martingale under the risk-neutral measure; (2) the **exponential martingale** $e^{\sigma W-\frac12\sigma^2t}$; (3) the **change of measure** (Radon–Nikodym) that moves you from the physical measure $\mathbb P$ to the pricing measure $\widetilde{\mathbb P}$ without changing which events are impossible. This is the discrete skeleton of Girsanov's theorem in continuous time ([[foundations/stochastic-calculus/index|Stochastic Calculus]]).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Martingales, super-, sub- (Shreve I §2.4)
With filtration $\mathcal F_0\subseteq\cdots\subseteq\mathcal F_n$ and adapted integrable $\{M_k\}$:
$$
\text{martingale: }\mathbb E[M_{k+1}\mid\mathcal F_k]=M_k;\quad \text{super-}: \le;\quad \text{sub-}: \ge.
$$
Binomial consequences (Shreve I §2.4): if $\mathbb E[S_{k+1}\mid\mathcal F_k]=(pu+qd)S_k$, then $(pu+qd)=1$ ⇒ martingale, $>1$ ⇒ submartingale, $<1$ ⇒ supermartingale.

#### 2.2 The discounted stock is the risk-neutral martingale (Shreve I §3.3; Glasserman §1.2)
Under the risk-neutral measure $\widetilde{\mathbb P}$, the **discounted** stock and every discounted self-financing wealth process are martingales (Shreve I §3.3, verified):
$$
\widetilde{\mathbb E}\Big[\tfrac{S_{k+1}}{(1+r)^{k+1}}\;\Big|\;\mathcal F_k\Big]=\frac{S_k}{(1+r)^k},
$$
equivalently $\widetilde{\mathbb E}[S_{k+1}\mid\mathcal F_k]=(1+r)S_k$. This is the cornerstone pricing equation in continuous time, $V(0)=\widetilde{\mathbb E}[e^{-rT}V(T)]$ (Glasserman eq. 1.39). Pricing under $\mathbb P$ would depend on the drift $\mu$; under $\widetilde{\mathbb P}$ it depends only on $r$ and $\sigma$.

#### 2.3 Exponential martingale (Shreve II Thm 3.6.1; Shreve I Thm 9.41)
$$
Z(t)=e^{\sigma W(t)-\frac12\sigma^2t}\ \Rightarrow\ \mathbb E[Z(t)\mid\mathcal F(s)]=Z(s).
$$
*Proof:* factor $Z(s)$, condition on the independent increment $W(t)-W(s)$, use its MGF $\mathbb E e^{\sigma\Delta W}=e^{\frac12\sigma^2(t-s)}$ to cancel the correction. This process is the seed of the change of measure — and of Girsanov ([[foundations/stochastic-calculus/05-girsanov-and-risk-neutral|Stochastic Calculus 05 · Girsanov]]).

#### 2.4 Change of measure = Radon–Nikodym (Shreve II Thm 1.6.1; Shreve I Ch 9)
Let $Z\ge0$ a.s. with $\mathbb E Z=1$; define $\widetilde{\mathbb P}(A)=\int_A Z\,d\mathbb P$. Then $\widetilde{\mathbb P}$ is a probability measure, $\widetilde{\mathbb P}\ll\mathbb P$, and if $Z>0$ a.s. the measures are **equivalent** (mutually absolutely continuous). Change of expectation:
$$
\widetilde{\mathbb E}X=\mathbb E[XZ],\qquad \mathbb E Y=\widetilde{\mathbb E}[Y/Z].
$$
On the finite market (Shreve I Ex 9.1) with physical $p=\frac13,q=\frac23$ and risk-neutral $\widetilde p=\widetilde q=\frac12$, the density is $Z(\omega)=\widetilde{\mathbb P}(\omega)/\mathbb P(\omega)$ with $Z(HH)=\frac94, Z(HT)=Z(TH)=\frac98, Z(TT)=\frac9{16}$, and $Z_k=\mathbb E[Z\mid\mathcal F_k]$ is a $\mathbb P$-martingale. The state-price density is $\zeta_k=(1+r)^{-k}Z_k$ (Shreve I Ch 9).

#### 2.5 The normal-recentering preview of Girsanov (Shreve II Ex 1.6.x)
If $X$ is standard normal under $\mathbb P$ and $Z=\exp\{-\theta X-\frac12\theta^2\}$ ($\theta$ constant), then under $\widetilde{\mathbb P}$ the shifted variable $Y=X+\theta$ is standard normal (completing the square: $e^{-\theta x-\theta^2/2}\varphi(x)=\varphi(x+\theta)$). This is exactly the discrete/finite version of the Girsanov drift shift — verified verbatim on Shreve II pp. 57–58.

---

### 3. Computational Implementation — verify the martingale & the change of measure

Check the random-walk martingale property, the risk-neutral discounted-stock relation, the exponential martingale mean, and the normal-recentering change of measure. Stdlib only.

```python
import math, random
random.seed(19)
# (1) martingale property of a zero-mean random walk
npaths,steps=30000,200
dt=1.0/steps
paths=[]
for _ in range(npaths):
    M=[0.0]
    for i in range(steps): M.append(M[-1]+random.gauss(0,math.sqrt(dt)))
    paths.append(M)
s,t=80,199
groups={}
for p in paths:
    ms=round(p[s],1)
    g=groups.setdefault(ms,[0,0.0]); g[0]+=1; g[1]+=p[t]
maxdev=max(abs(ms-g[1]/g[0]) for ms,g in groups.items() if g[0]>=50)
print("martingale: max|E[M_t|F_s]-M_s|=%.4f (theory 0)" % maxdev)
# (2) risk-neutral: E~[S_{k+1}|F_k]=(1+r)S_k  (discounted stock martingale)
r,u,d=0.25,2.0,0.5
pt=(1+r-d)/(u-d); S0=4.0
Enext=pt*u*S0+(1-pt)*d*S0
print("risk-neutral: E~[S_{k+1}|S_k]=%.4f vs (1+r)S_k=%.4f" % (Enext,(1+r)*S0))
# (3) exponential martingale E[e^{sig W - .5 sig^2 t}]=1
sig=0.7
zs=[math.exp(sig*random.gauss(0,1)-0.5*sig*sig) for _ in range(300000)]
print("exponential martingale E[Z]=%.4f (theory 1.0)" % (sum(zs)/len(zs)))
# (4) RN change of measure: X~N(0,1) under P, Z=exp{-th X -.5 th^2}, Y=X+th ~N(0,1) under P~
th=0.8
X=[random.gauss(0,1) for _ in range(400000)]
Z=[math.exp(-th*x-0.5*th*th) for x in X]
EY=sum((x+th)*z for x,z in zip(X,Z))/len(X)
print("RN recenter: E~[Y]=E[(X+th)Z]=%.4f (theory 0)" % EY)
print("  E[Z]=%.4f (theory 1.0)" % (sum(Z)/len(Z)))
```
```
martingale: max|E[M_t|F_s]-M_s|=0.1337 (theory 0)
risk-neutral: E~[S_{k+1}|S_k]=5.0000 vs (1+r)S_k=5.0000
exponential martingale E[Z]=1.0005 (theory 1.0)
RN recenter: E~[Y]=E[(X+th)Z]=-0.0005 (theory 0)
  E[Z]=1.0020 (theory 1.0)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Zero drift" ≠ "stays put."** A martingale can have enormous variance — BM, discounted prices. The property says only that the *conditional mean* of the future is the present, never that the path is flat. Treating "martingale" as "predictable at the level" misreads the definition.
2. **Discounting under the wrong measure.** Pricing needs expectation under $\widetilde{\mathbb P}$ (drift $r$), *not* $\mathbb P$ (drift $\mu$). A $\mathbb P$-expectation of $e^{-rT}V_T$ depends on the unhedgeable drift — the exact mispricing that a change of measure fixes (Shreve I Ch 12; Glasserman §1.2).
3. **Forgetting it is the *discounted* stock that is a martingale.** Under $\widetilde{\mathbb P}$, $S_k/(1+r)^k$ is the martingale, not $S_k$ itself — unless $r=0$. Dropping the discount breaks the pricing equation.
4. **Equivalent measures share the "impossible."** $\widetilde{\mathbb P}$ and $\mathbb P$ are equivalent ($Z>0$) so they agree on which events have probability zero; a model where $\mathbb P$ lets a price hit zero while $\widetilde{\mathbb P}$ forces $S_t>0$ violates absolute continuity and the RN density blows up.
5. **Optional sampling needs bounded stopping times.** $\mathbb E[Y_\tau\mid\mathcal F_\sigma]=Y_\sigma$ for martingales holds for bounded $\sigma\le\tau$ (Shreve I §5.3); stopping at the wrong (unbounded) time and asserting constancy of expectation silently fails.

---

### 5. Canonical Literature & Study References

- **Shreve**, *Stochastic Calculus for Finance II*, Ch 1 §1.6 (change of measure, RN Thm 1.6.1, normal-recentering Ex), Ch 3 (martingale Thm 3.3.4, exponential martingale Thm 3.6.1).
- **Shreve**, *Stochastic Calculus for Finance I*, §2.4 (martingale/super/sub), §3.3 (discounted-stock martingale), Ch 9 (Radon–Nikodym, state-price density $\zeta_k=(1+r)^{-k}Z_k$, Ex 9.1), Ch 12 (market price of risk, CMG), §5.3 (optional sampling).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §1.2 (risk-neutral measure via Radon–Nikodym, cornerstone eq. 1.39, Girsanov drift).

---

### 6. Connected Graph Bridges

- Back: [[foundations/probability-and-measure-theory/04-conditional-expectation|04 · Conditional Expectation]] · [[foundations/probability-and-measure-theory/index|Index Hub]]
- Forward: [[foundations/probability-and-measure-theory/06-advanced-extensions|06 · Advanced Extensions]] (RN derivative, convergence theorems) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (Girsanov, exponential martingale, FTA)
- Applications: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (risk-neutral valuation) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] (the discrete discounted-stock martingale)

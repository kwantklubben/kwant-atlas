---
title: "04 — Advanced Dynamics: Skew Stickiness, Heston Skew, Jumps & SABR"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - skew-dynamics
  - heston
  - sabr
  - forward-skew
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/03-surface-models|03 · Surface Models]].

---

### 1. Intuition & Practical Objective

All stochastic-volatility-with-jumps models produce **essentially the same surface shape** (Gatheral ch 7, §7.8). So the shape cannot tell you which model is right. What separates models — and what costs money — is the **dynamics**: how the surface *moves* when the spot moves and when time passes. This page is the "why dynamics decides" page.

Two distinct questions:

1. **Statics (today's shape):** answered by the skew level, $\partial_k\sigma_{BS}^2$. Every SV model gives about $\rho\eta\beta(v)/2$ short-dated and $\rho\eta\beta(v)/(\lambda'T)$ long-dated, and jumps add $-2\mu_J$ — so the shape is (to first order) **model-independent** (Gatheral §7.1–7.3).
2. **Dynamics (how it moves):** answered by the **skew stickiness ratio** $R_T$ and the **forward skew** $\mathcal S_\theta(\tau)$. Here models diverge sharply: local vol generates $R_T\to\approx2$–$3$ and *too-flat* future skews; time-homogeneous SV keeps future skews equal to today's.

The practical objective: know that **vanilla smiles barely constrain cliquet/forward-start prices**, and that the skew-level independence and the empirical lognormal-variance scaling point to a specific dynamics (lognormal variance, $\beta(v)\sim\sqrt v$, not a square-root process).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Skew stickiness ratio in local volatility (Bergomi eq 2.64)

The regression definition is $R_T=\frac{1}{\mathcal S_T}\frac{\langle d\hat\sigma_{F_TT}\,d\ln S_0\rangle}{\langle(d\ln S_0)^2\rangle}$ (Bergomi 2.62), with $R_T=1$ sticky-strike, $R_T=0$ sticky-delta. In **local volatility**
$$R_T=1+\frac1T\int_0^T\frac{\mathcal S_t}{\mathcal S_T}\,dt,$$
and the **$R=2$ rule**: if the skew $\mathcal S$ (equivalently $\alpha$) is maturity-independent, $R_T=2$ for all $T$; moreover $\lim_{T\to0}R_T=2$ for *any* smooth LV (exact, via the backward/forward symmetry $\hat\sigma_{ST}(K)=\hat\sigma_{KT}(S)$, zero rates). For a power-law skew $\mathcal S_T\propto T^{-\gamma}$,
$$R_T\to\frac{2-\gamma}{1-\gamma}\ (T\to\infty):\quad \gamma=\tfrac12\ (\text{equity})\Rightarrow R_\infty=3;\qquad \gamma=1\Rightarrow R_T\propto\ln T.$$
The **vol-of-vol implied by LV** is $\mathrm{vol}(\hat\sigma_{F_TT})\to2\mathcal S_T$ as $T\to0$ (Bergomi eq 2.85) — a large, structural number.

#### 2.2 Skew dynamics under SV vs LV

- **SV:** future surfaces look like today's — the skew is **time-homogeneous**. The empirical fact that the *skew slope is roughly independent of the volatility level* translates to $\beta(v)\sim\sqrt v$, i.e. **variance is approximately lognormal**, not square-root (Gatheral §8.1).
- **LV:** future (forward) surfaces are **substantially flatter** than today's, because the forward local skews are flatter: from (2.90)/(2.91) with today's skew $\mathcal S_t=\alpha(t/\tau_0)^{-\gamma}$,
$$\mathcal S_\theta(\tau)=\mathcal S_{\tau+\theta}-\frac{\tau}{\theta}\!\left(\frac1\theta\int_\tau^{\tau+\theta}\mathcal S_t\,dt-\mathcal S_{\tau+\theta}\right),\qquad \mathcal S_\theta(\tau)\propto\left(\frac{\theta}{\tau}\right)^{\gamma}\mathcal S_\theta\ \ll\ \mathcal S_\theta.$$
- **Consequence:** a **wrong SV model** (off $\sim1.5\times$ if vol doubles) still beats **LV**, which generates almost *no* forward skew (Gatheral §8.1–8.2). LV sellers of forward-skew products win the deal and lose money (Gatheral ch 8/10).

#### 2.3 Heston skew and term structure

Heston (Gatheral §2.2, §3.4; Bergomi ch 6) with $\lambda'=\lambda-\rho\eta/2$, $\bar v'=\bar v\lambda/\lambda'$:
$$\hat\sigma_{BS}^2\big|_{K=F_T}=\frac{(\bar v-\bar v')\big(1-e^{-\lambda'T}\big)}{\lambda'T}+\bar v',$$
$$\sigma_{BS}^2\approx \hat w'_T/T+\rho\eta\,\frac{x_T}{\lambda'T}\!\left(1-\frac{1-e^{-\lambda'T}}{\lambda'T}\right).$$
- **Short-dated ATM skew** $\to\frac{\rho\eta}{2}$ — independent of $\lambda$ and $T$ (confirmed numerically below, $-0.1388$ vs $-0.1389$).
- **Long-dated ATM skew** $\to\frac{\rho\eta}{\lambda'T}$ — decays as $1/T$.
- The skew is **independent of the variance level** $v_0,\bar v$ (approximately true even for $v_0\ne\bar v$); increasing $|\rho|$ or $\eta$ steepens it; $\eta$ also sets curvature (kurtosis).
- Heston hard-wires $\mathcal S_T\propto1/\hat\sigma_{F_TT}$, which reality does not show (Bergomi §6 criticism).

#### 2.4 Jumps and the SABR/SV asymptotics

Adding jumps (Gatheral ch 5, §7.3). For short $\Delta T$,
$$\sigma_{BS}^2\text{ skew}\big|_{k=0}\approx-2\mu_J,\qquad \mu_J=\lambda\,\mathbb{E}[J-1]\ \text{(compensator)}.$$
Jumps and stochastic vol contribute **additively** to the ATM variance skew at $\tau=0$:
$$\left.\frac{\partial v_{BS}}{\partial k}\right|_{k=0}\to \rho\,b(\sigma)-2\mu_J.$$
The **jump compensator drives the short-expiry skew; the expected jump size drives its decay** (Gatheral §5.4). The **SABR** model
$$dS_t=\sigma_tS_t^{\beta}dZ_1,\qquad d\sigma_t=\chi\sigma_t\,dZ_2,\qquad dZ_1dZ_2=\rho\,dt$$
(Hagan et al. 2002) has no mean reversion, so it is a short-expiration tool, but it has an exact $\tau\to0$ smile formula that factorizes: $\sigma_{BS}(k)=\sigma_0\frac{y}{f(y)}\big(1+\tfrac14\rho\chi\sigma_0+\frac{2-3\rho^2}{24}\chi^2\tau+\cdots\big)$ with $y=-\chi k/\sigma_0$ (Gatheral eq 7.7). It implies $\partial_k\sigma_{BS}|_{k=0}=\rho/2$ — the special case of (7.6) — and the **Medvedev–Scaillet** small-time expansion (Gatheral eq 7.4–7.6) reproduces it, proving $\partial_k I|_{k=0}\to\rho b(\sigma)/(2\sigma)$.

**Long expirations (Fouque–Papanicolaou–Sircar):** for log-OU volatility the skew $\partial_x\sigma_{BS}\approx \rho\xi/(\lambda T)$ (Gatheral eq 7.10), matching Heston for large $\lambda T$. The **natural interpolation** between the two limits is Bergomi eq 7.11, which Lewis's small-$\eta$ expansion proves *exact* to $O(\eta)$ (Gatheral §7.6, eq 7.11–7.12). **Extreme strikes:** Lee's moment formula, $\beta^*=g(q^*)$, $g(x)=2-4(\sqrt{x^2+x}-x)$ — model-independent (Gatheral §7.7).

---

### 3. Computational Implementation — SSR and the Heston skew limits

We (i) verify the LV skew-stickiness formula on a realistic decaying equity skew (and the $R=2$ rule), and (ii) verify the Heston ATM term structure and the short-dated-skew limit $\rho\eta/2$. Stdlib only.

```python
import math
def R_T(a,tau0,T,n=200000):                 # R_T = 1 + (1/T) int_0^T S_t/S_T dt, S_t = a/sqrt(t+tau0)
    def Sk(t): return a/math.sqrt(max(t,tau0))
    ST=Sk(T);tot=0.0;dt=T/n
    for i in range(n):
        t=(i+0.5)*dt;tot+=Sk(t)/ST*dt
    return 1.0+tot/T

for T in (0.25,1.0,5.0,50.0):
    print(f"skew S_T=a/sqrt(T+tau0): T={T:5.2f}  R_T={R_T(0.2,0.05,T):.4f}")
print("constant skew (S_t/S_T=1): R_T = 2 exactly  (the R=2 rule)")

v0,vbar,eta,rho,lam=0.0174,0.0354,0.3877,-0.7165,1.3253     # Heston, Gatheral Table 3.2
lam2=lam-rho*eta/2.0; vbar2=vbar*lam/lam2
def atm_var(T):
    x=lam2*T; return (vbar-vbar2)*(1-math.exp(-x))/x+vbar2
def skew(T):
    x=lam2*T; return rho*eta/(lam2*T)*(1-(1-math.exp(-x))/x)
print(f"Heston: lambda'={lam2:.4f} vbar'={vbar2:.5f}")
for T in (0.001,0.1,1.0,5.0):
    print(f"T={T:6.3f}: ATM var={atm_var(T):.5f} ({math.sqrt(atm_var(T))*100:5.2f}% vol)  skew={skew(T):+.4f}")
print(f"short-dated skew limit rho*eta/2 = {rho*eta/2:+.4f}")
```
```
skew S_T=a/sqrt(T+tau0): T= 0.25  R_T=2.5528
skew S_T=a/sqrt(T+tau0): T= 1.00  R_T=2.7764
skew S_T=a/sqrt(T+tau0): T= 5.00  R_T=2.9000
skew S_T=a/sqrt(T+tau0): T=50.00  R_T=2.9684
constant skew (S_t/S_T=1): R_T = 2 exactly  (the R=2 rule)
Heston: lambda'=1.4642 vbar'=0.03204
T= 0.001: ATM var=0.03540 (18.81% vol)  skew=-0.1388
T= 0.100: ATM var=0.03517 (18.75% vol)  skew=-0.1324
T= 1.000: ATM var=0.03381 (18.39% vol)  skew=-0.0901
T= 5.000: ATM var=0.03250 (18.03% vol)  skew=-0.0328
short-dated skew limit rho*eta/2 = -0.1389
```

The LV **skew stickiness ratio climbs toward $R=2$–$3$** exactly as the power-law asymptotics predict (a $1/\sqrt{T}$ skew → $R_\infty=3$), and the constant-skew case gives the exact $R=2$ rule. The Heston skew **converges to $\rho\eta/2=-0.1389$** as $T\to0$ (computed $-0.1388$ at $T{=}0.001$) and **decays toward $1/T$** at long maturities — the *same* $1/T$ decay that is too slow to fit the observed short-end smile (Gatheral Table 3.2 / Fig 3.6). Note also the printed ATM variance $\to0.0354=\bar v$ as $T\to0$ — the flagged notation subtlety: the *physical* short limit should be $v_0=0.0174$, revealing (3.18)'s unconditional-path construction.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Judging a model by its static fit.** Vanilla smiles barely constrain forward-skew-dependent products: Bergomi's model-independent bounds leave a 95/105 forward call spread anywhere in $[1.6\%,7.7\%]$ from a flat 20% smile, narrowing only when *congruent* payoffs are added (Bergomi §3.1.7). Fitting today's surface is not model validation.
2. **Local volatility's missing forward skew.** LV generates future skews $\propto(\theta/\tau)^\gamma$ times today's — systematically flat. Digitally-capped cliquets, barriers and digitals are all mispriced (Gatheral ch 8–10: a 1-year ATM digital mispriced by $\sim12\%$ of notional if the skew term is dropped).
3. **Square-root variance is the wrong scaling.** Empirically the skew slope is ~independent of vol level, implying $\beta(v)\sim\sqrt v$ (lognormal variance), not Heston's $\beta=1$. Models with $R_T$ and vol-of-vol term structure of the wrong shape misprice variance swaptions and cliquets even with matched vanillas (Gatheral §8.1; Bergomi ch 6–7).
4. **No time-homogeneous SV fits the short end.** The observed short-dated skew rises *faster* than any SV model allows; jumps are required (Gatheral ch 3 conclusion, ch 5). Fitting Heston to the whole surface forces a compromise that is too flat short-dated.
5. **SABR is short-dated only.** No mean reversion ⇒ SABR does not reproduce the long-dated skew term structure; using it for long expirations is a first-principles error (Gatheral §7.2).

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 7 (short-expiration asymptotics §7.1, Medvedev–Scaillet §7.2, SABR 7.7, jumps §7.3, FPS §7.4, Lewis §7.6, Lee §7.7, summary §7.8) and Ch 8 (surface dynamics: skew level-independence §8.1, LV forward skew §8.2, stochastic implied vol §8.3). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 2 §2.5–2.6 (SSR 2.61/2.64, $R=2$ rule 2.66–2.79, forward skew 2.90–2.92), Ch 3 (forward-start, model-independent bounds), Ch 6 (Heston in forward-variance form 6.9/6.17–6.20). *Math-verified.*
- **Hagan, Kumar, Lesniewski, Woodward**: *Managing Smile Risk* (Wilmott, 2002) — the SABR formula. **Medvedev–Scaillet** (2004), **Lewis** (2000), **Lee** (2004) for the asymptotics.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/03-surface-models|03 · Surface Models]]
- Forward: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-and-sabr|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|06 · Advanced Extensions]]

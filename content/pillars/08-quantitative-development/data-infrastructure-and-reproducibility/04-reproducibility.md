---
title: "8.6.4 Reproducibility"
tags:
  - pillar-quant-dev
  - data-infrastructure-and-reproducibility
  - reproducibility
  - determinism
  - environment-management
  - lockfiles
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/03-data-versioning-and-lineage|03 · Data Versioning & Lineage]] and [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/02-data-pipelines|02 · Data Pipelines]].

---

### 1. Intuition & Practical Objective

**Reproducibility is a contract on inputs, not outputs.** You do not *try* to reproduce a number; you pin three inputs - **data version, code commit, environment lockfile** - and the output reproduces as a matter of course. If any of the three changes, you are computing something different, and the honest thing is to treat it as a new result, not a buggy echo of the old one.

This page makes the discipline concrete. Two things must both hold:

1. **Determinism of the code** - given fixed inputs, the algorithm itself must return the same bytes every time. The two classic enemies are *unseeded randomness* and *floating-point reduction order*.
2. **Pinning of the environment** - the exact dependency versions, Python version, and container/image must be captured so that "the same code" is literally the same binary environment on day 1 and day 1000. This is the job of `uv`/`conda-lock`/Poetry lockfiles and Docker images.

> **The one-line job:** *make `O = f(D, C, E)` hold with all three inputs frozen, so a rerun anywhere, anytime, reproduces the original bytes - and make any divergence fail loudly instead of silently.*

---

### 2. Mathematical Ground Truth & Derivations

**Floating-point reduction is order-dependent.** A double keeps ~16 significant digits. Summing a list in different orders can give different answers because intermediate roundings differ. The canonical absorption example:
$$
s = 10^{16} + 1 - 10^{16}.
$$
In forward order, $10^{16}+1 = 10^{16}$ (the $1$ is absorbed, since the ulp of $10^{16}$ is $2$), then $10^{16}-10^{16}=0$ - the result is $0$. Regrouping the *same* three terms so the $1$ is added last lets it survive:
$$
\underbrace{(10^{16}+1)-10^{16}}_{\text{absorbed}\ \to\ 0} = 0 \quad\text{vs}\quad \underbrace{(10^{16}-10^{16})}_{0}+1 = 1
$$
More precisely, *any* summation $\sum_i x_i$ computed in two different orders can differ by the magnitude of the absorbed low-order terms. A parallel framework that reorders a reduction (map-reduce, GPU block reductions) can therefore change a result. **The fix is not "more precision" but *pinning the order*** - the same aggregation sequence, recorded and reused.

**Reproducibility = frozen inputs.** Formally, output $O$ is a function of the input triple $(D,C,E)$. The reproducible set is the set of *equivalent reruns*:
$$
O^{(1)} = O^{(2)} \iff (D_1,C_1,E_1) = (D_2,C_2,E_2)
$$
up to the algorithm's own determinism. This is why a lockfile (pinning $E$) and a data version hash (pinning $D$) and a git commit (pinning $C$) are not nice-to-haves - they *are* the definition of reproducibility.

---

### 3. Computational Implementation - determinism vs reduction order

Two demonstrations in one stdlib script. **A.** The same seeded computation, run twice, is bit-identical (proven by hashing the result). **B.** A parallel reduction assembled in two orders changes the answer - the FP-order failure you must pin against.




**B. Floating-point reduction order changes the answer** (a threaded map-reduce whose aggregation is reordered - the failure mode to pin):




Part A is the reproducibility you *want*; part B is the silent divergence you must *prevent*. In a real pipeline, shards could be summed in whatever order threads finish - unless the reduction order is fixed. The whole point of pinning $E$ and $C$ is that B cannot sneak in between "the run that worked" and "the run that proves it."

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Unseeded randomness.** `random.random()` without `Random(seed)` yields a different stream every run - part A of §3 silently fails the moment the seed is dropped. Seed everything, always.
2. **Unpinned environments.** A dependency bump (a new numpy/scipy/duckdb) can change rounding, sorting, or even a function's semantics. Without a lockfile, "same code" is an illusion - this is **config drift** (see [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/05-failure-modes-and-practice|05]]).
3. **Parallel reduction order.** As §3B shows, a reordered sum can give $1.0$ vs $0.0$. A framework that reduces nondeterministically breaks reproducibility even with all inputs fixed.
4. **Pinning only part of the triple.** Freezing data but not code, or code but not the environment, leaves a hole. All three legs of $(D,C,E)$ must be pinned for the guarantee to hold.

---

### 5. Canonical Literature & Study References

- **Astral `uv` / Poetry / conda-lock / Docker** - official docs - the *tools* that pin $E$ (dependency + environment reproducibility), the practical baseline. **Priority M.**
- **López de Prado** - *Advances in Financial Machine Learning*, Ch 1 - reproducibility discipline and the cost of leakage/overfitting when inputs drift.
- **McKinney** - *Python for Data Analysis*, 3rd ed. - the Python-stack foundation this reproducibility layer manages.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/03-data-versioning-and-lineage|03 · Data Versioning & Lineage]] · [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/05-failure-modes-and-practice|05 · Failure Modes & Practice]] (what breaks when any leg of the triangle is dropped)
- Consumer: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] (reproducible backtests are the downstream payoff)

---
title: "8.1.4 numba & JIT"
tags:
  - pillar-quant-dev
  - python-quant-stack
  - numba
  - jit
  - nopython-mode
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization|02 · NumPy Vectorization]] and Python function/loop basics.

---

### 1. Intuition & Practical Objective

Sometimes you genuinely need a loop — an iterative optimizer, a path-dependent simulation, a recurrence that broadcasting cannot express. The practical objective of this page: **when you must loop, `numba.njit` compiles that Python function (loops and all) down to native machine code on first call, giving compiled-C speed for code you write in Python.** It is the escape hatch that closes the one gap vectorization leaves open.

Three ideas:

1. **`@njit` compiles *your* Python to machine code.** On the first call, Numba (via LLVM) type-infers your function's arguments and generates a compiled version; subsequent calls skip compilation entirely. A pure-Python loop that takes hundreds of milliseconds drops to single-digit milliseconds — the verified benchmark below shows **~165×** for a dot-product loop.
2. **`nopython=True` (the default for `njit`) forbids Python objects.** It compiles only when every variable is a supported NumPy/primitive type (ints, floats, arrays). If you need `dict`, `str` manipulation, or dynamic Python objects, it falls back to *object mode* (slow) or refuses — this constraint is the price of the speed.
3. **It scales to real vectorized backtesting.** The `vectorbt` engine in this stack is itself numpy/numba-accelerated ([[pillars/08-quantitative-development/python-quant-stack/06-advanced-extensions|06]]); knowing Numba lets you write your own fast loops for custom strategies and indicators.

**Why it matters for quant.** Not everything is array math. Options Greeks via Monte Carlo, pathwise VaR, custom risk-adjusted signals, or nested optimizers all contain loops. Numba turns the "Python is too slow for these" wall into a footnote — at the cost of respecting its strict typing and of paying a one-time compile per function signature.

---

### 2. Mathematical Ground Truth & Derivations

**What JIT actually removes.** Consider the dot product over $N$ elements,

$$
s = \sum_{i=1}^{N} x_i\, y_i .
$$

A pure-Python loop pays per element the interpreter overhead $c_{\text{py}}$ (bytecode dispatch, boxing, attribute lookup). Numba removes *all* of it: after type inference it emits the equivalent of a compiled `for` loop with raw pointer loads and fused multiply-add — each element ~$c_C$. Hence

$$
\text{speedup} = \frac{N\,c_{\text{py}}}{N\,c_C} \approx \frac{c_{\text{py}}}{c_C},
$$

the same ratio as vectorization ([[pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization|02]]), because *both* remove the same per-element Python overhead — one by batching, one by compiling the loop itself. Numba's advantage is generality: it handles loops broadcasting can't express.

**The GIL link.** A compiled Numba function releases the GIL while it runs (if `nogil=True`), so it is one of the few ways to get real thread parallelism out of CPU-bound Python (see [[pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice|05]]).

**First-call compilation cost.** The first call pays a compile (type inference + LLVM), often ~0.1–1 s per signature, amortized over the many warm calls that follow. Always warm the function on a tiny input before timing or before hot loops.

---

### 3. Computational Implementation — the JIT speedup, reproduced

The dot product three ways: pure-Python loop, `np.dot`, and a `numba.njit` loop. Numba matches NumPy and crushes the Python loop; the first-call compile is excluded by a warm-up call.

```python
import timeit, numpy as np, numba
np.random.seed(0)
n = 2_000_000
x = np.random.randn(n); y = np.random.randn(n)

def py_dot(x, y):                      # pure-Python loop
    s = 0.0
    for i in range(len(x)):
        s += x[i]*y[i]
    return s

@numba.njit
def nb_dot(x, y):                      # same loop, JIT-compiled
    s = 0.0
    for i in range(len(x)):
        s += x[i]*y[i]
    return s

nb_dot(x[:10], y[:10])                 # WARM-UP: compile once, exclude from timing

py_t = min(timeit.repeat(lambda: py_dot(x, y), number=1, repeat=3))
np_t = min(timeit.repeat(lambda: np.dot(x, y), number=1, repeat=5))
nb_t = min(timeit.repeat(lambda: nb_dot(x, y), number=1, repeat=5))
print(f"n = {n:,}")
print(f"pure-Python loop: {py_t*1000:9.1f} ms")
print(f"numpy   np.dot:   {np_t*1000:9.3f} ms")
print(f"numba   njit loop:{nb_t*1000:9.3f} ms  (first-call compile excluded)")
print(f"numba vs Python:  {py_t/nb_t:8.1f}x   numba vs numpy: {np_t/nb_t:.2f}x")
py_r = py_dot(x, y); np_r = np.dot(x, y); nb_r = nb_dot(x, y)
print(f"all three agree: {abs(py_r-np_r)<1e-9 and abs(np_r-nb_r)<1e-9}")
```
```
n = 2,000,000
pure-Python loop:     324.2 ms
numpy   np.dot:       0.687 ms
numba   njit loop:    1.956 ms  (first-call compile excluded)
numba vs Python:     165.7x   numba vs numpy: 0.35x
all three agree: True
```

Numba's compiled loop lands within ~2–3× of BLAS `np.dot` (0.35× = `np.dot` is ~3× faster here) while beating the interpreted loop ~165× — and, unlike `np.dot`, it compiles *any* loop body you write, not just a fixed kernel. A Monte Carlo simulator or a pathwise loop sees the same kind of gain.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **`nopython` mode is strict.** Passing a Python `dict`, `str`, `object`, or an unsupported type makes Numba refuse (or silently fall to slow *object mode*). Constrain your data to NumPy arrays and primitives — the typed subset — and your code compiles; anything else is a red flag to refactor.
2. **First-call compile latency is real.** Timing Numba without a warm-up call measures LLVM compile time, not loop speed — a classic benchmark trap (I excluded it above deliberately).
3. **Type-inference changes can be silent.** A function that compiles for `int` input may behave differently for `float`; Numba caches a separate compiled version per signature, so mixed input types multiply compile time and can hide bugs.
4. **The GIL is only released with `nogil=True`.** A `@njit` function that touches Python objects cannot run threads in parallel. Pure-array `nogil=True` functions can — that is the correct route to thread parallelism ([[pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice|05]]).

---

### 5. Canonical Literature & Study References

- **QuantEcon — Numba chapter**, *Python Programming for Economics and Finance* (quantecon.org) — the free tutorial that brings numeric Python loops to compiled speed, economics-flavored and directly applicable to quant simulation loops.
- **Numba official docs** (numba.pydata.org) — JIT decorators, `nopython` mode, supported types, `nogil`, and caching; the authoritative reference.
- **Gorelick & Ozsvald**, *High Performance Python* (2nd ed., 2020) — ch. 4 (Cython/Numba): when to compile vs vectorize, profiling to find the loop worth compiling.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/python-quant-stack/03-pandas-pitfalls|03 · pandas Pitfalls]] · [[pillars/08-quantitative-development/python-quant-stack/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/08-quantitative-development/python-quant-stack/06-advanced-extensions|06 · Advanced Extensions]] (vectorbt's numba-accelerated engine)
- Base: [[foundations/numerical-methods/index|Numerical Methods]] (the numeric algorithms these loops implement)

#!/usr/bin/env python3
"""Strict whole-corpus fence check (v2).

For every non-_legacy markdown page: parse ``` fences line-based; execute each
python block in a namespace SHARED with earlier python blocks on the same page
(so chained pages work), but capturing ONLY the current block's stdout; then
byte-compare to the IMMEDIATELY FOLLOWING fence (lang '' or 'text').

Each block runs in a subprocess with a hard timeout, so a spinning or
network-blocked block cannot hang the pass.

In the subprocess, earlier blocks are re-executed with stdout suppressed, so
their prints never contaminate the comparison. That was the bug in v1.
"""
import glob, json, subprocess, sys

SKIP = {  # page -> python-block indices deliberately not executed
    # network stub, explicitly labelled "not executed here"
    "content/fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl.md": {1},
    # multiprocessing demo: correct as a file, not under a piped -c harness
    "content/pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice.md": {0},
}

RUNNER = r'''
import io, contextlib, sys
_g = {}
_quiet = io.StringIO()
for _c in _prior:
    with contextlib.redirect_stdout(_quiet):
        exec(_c, _g)
_buf = io.StringIO()
try:
    with contextlib.redirect_stdout(_buf):
        exec(_target, _g)
except Exception as _e:
    sys.stderr.write("TRACEBACK: %s: %s\n" % (type(_e).__name__, _e))
    sys.exit(3)
sys.stdout.write(_buf.getvalue())
'''


def fences(s):
    lines = s.split("\n"); out = []; i = 0
    while i < len(lines):
        if lines[i].startswith("```"):
            lang = lines[i][3:].strip(); j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            if j < len(lines):
                out.append((lang, "\n".join(lines[i + 1:j])))
                i = j + 1
                continue
        i += 1
    return out


def run_block(prior, target, timeout=90):
    import json as _j
    payload = _j.dumps({"prior": prior, "target": target})
    prog = ("import json,sys\n"
            "_p=json.loads(sys.stdin.read())\n_prior=_p['prior']\n_target=_p['target']\n"
            + RUNNER)
    try:
        r = subprocess.run([sys.executable, "-c", prog], input=payload,
                           capture_output=True, text=True, timeout=timeout, cwd="/tmp")
    except subprocess.TimeoutExpired:
        return "", "", "TIMEOUT(%ds)" % timeout
    return r.stdout, r.stderr, None


problems = []
npages = nblocks = nskip = 0
for f in sorted(glob.glob("content/**/*.md", recursive=True)):
    if "/_legacy/" in f:
        continue
    fl = fences(open(f).read())
    if not any(l == "python" for l, _ in fl):
        continue
    npages += 1
    prior, pi = [], 0
    for k, (lang, c) in enumerate(fl):
        if lang != "python":
            continue
        nxt = fl[k + 1] if k + 1 < len(fl) else None
        if pi in SKIP.get(f, set()):
            nskip += 1
            prior.append(c)
            pi += 1
            continue
        nblocks += 1
        out, err, terr = run_block(prior, c)
        prior.append(c)
        if terr:
            problems.append((f, pi, terr))
        elif "TRACEBACK" in err:
            problems.append((f, pi, "RUN " + err.strip().split("\n")[-1][:60]))
        elif nxt is None or nxt[0] not in ("", "text"):
            problems.append((f, pi, "NO FENCE"))
        elif out.rstrip() != nxt[1].rstrip():
            problems.append((f, pi, "MISMATCH"))
        pi += 1
    print("checked %s" % f, flush=True)

print("=" * 60)
print("pages=%d python_blocks=%d skipped=%d problems=%d" % (npages, nblocks, nskip, len(problems)))
for f, k, e in problems:
    print("  %-14s | %s blk %d" % (e, f, k))
with open("/tmp/fence_problems.json", "w") as fh:
    json.dump(problems, fh, indent=1)

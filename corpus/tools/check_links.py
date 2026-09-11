#!/usr/bin/env python3
"""Resolve every wikilink in content/ and fail on dangling targets.

Used as a CI gate. Design notes:

* Both alias forms are stripped: `[[path|Alias]]` and the escaped `[[path\\|Alias]]` used
  inside markdown tables. A naive `[[path|` replace silently misses the latter.
* `_legacy/` is skipped -- it is archive material, excluded from the published site.
* Known false positives are filtered: numpy fancy-indexing (`x[[1.0, 0.0, -1.0]]`) parses as
  a wikilink, as do similar numeric/expression spans. A target is only treated as a real
  link if it looks like a content path or a bare slug.
* Exit 0 when clean, 1 with a list otherwise.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = os.path.join(ROOT, "content")

LINK_RE = re.compile(r"\[\[([^\]\n]+?)\]\]")
AREAS = ("foundations/", "pillars/", "fundamentals-accounting/", "corpus/")
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """Remove fenced blocks and inline code before looking for wikilinks.

    `[[...]]` inside a code block is not a link: numpy fancy-indexing (`x[[1.0, 0.0, -1.0]]`)
    and array literals (`np.array([[se2]])`) otherwise parse as wikilinks and produce
    false positives. This was the single largest source of noise in link checking.
    """
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))


def targets() -> set[str]:
    """Every addressable page: <relpath-without-.md>, plus the bare dir form for an index.md."""
    out = set()
    for root, dirs, files in os.walk(CONTENT):
        if "_legacy" in root.split(os.sep):
            continue
        for f in files:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, f), CONTENT).replace(os.sep, "/")
            out.add(rel[:-3])
            if rel.endswith("/index.md"):
                out.add(rel[: -len("/index.md")])
    return out


def looks_like_path(t: str) -> bool:
    """Filter out numeric/expression spans that merely look like wikilinks."""
    if not t or any(c in t for c in ",()[]+"):
        return False
    if any(ch.isspace() for ch in t):
        return False
    if t.startswith("#") or "://" in t:
        return False
    if t in AREAS or any(t.startswith(a) for a in AREAS):
        return True
    # a bare slug (no slash) is also addressable, e.g. [[glossary]] / [[diagnostics]]
    return "/" not in t and t.replace("-", "").replace("_", "").isalnum()


def main() -> int:
    known = targets()
    bad: list[tuple[str, str]] = []
    total = 0
    for root, dirs, files in os.walk(CONTENT):
        if "_legacy" in root.split(os.sep):
            continue
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            src = os.path.relpath(p, ROOT)
            for m in LINK_RE.finditer(strip_code(open(p, encoding="utf-8").read())):
                raw = m.group(1)
                t = raw.split("\\|")[0].split("|")[0].strip().strip("/")
                if t.endswith(".md"):
                    t = t[:-3]
                if t.endswith("/index"):
                    t = t[: -len("/index")]
                if not looks_like_path(t):
                    continue
                total += 1
                if t not in known:
                    bad.append((src, t))

    print(f"wikilinks checked: {total}")
    if bad:
        print(f"UNRESOLVED: {len(bad)}")
        for src, t in bad:
            print(f"  {src} -> {t}")
        return 1
    print("all resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())

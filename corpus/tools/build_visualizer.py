#!/usr/bin/env python3
"""Generate the D3 graph data in content/visualizer.html from the content tree.

WHY THIS EXISTS
---------------
The node `path` fields and the `links` array used to be hand-maintained inside
visualizer.html, and that drifted silently twice:

  1. Retiring a legacy flat note left four nodes pointing at deleted slugs -- live 404s.
  2. Graph *edges* reference node IDs while click-through uses a separate `path` field.
     A "0 dangling edges" check therefore passed while four nodes still 404'd.

DESIGN -- derive what is mechanical, validate what is editorial
---------------------------------------------------------------
* DERIVED from the content tree on every run: each node's click-through `path`, its
  `group`, and whether its target still exists. A renamed or deleted folder becomes a
  loud error instead of a 404.
* CURATED but VALIDATED: which edges to draw is a graph-design choice, so the 255 edges
  live in visualizer_meta.json (`links`). Both endpoints are checked against the live
  node set, so a retired node id fails the build rather than dangling.
* Also reported: content-tree topics with no metadata entry, and isolated nodes.

(Automatically deriving edges from the markdown was tried and rejected: hubs list so many
cross-references that it yields ~1040 edges, an unreadable hairball. The curated 255 is a
deliberate design decision, not laziness.)

USAGE
-----
    python3 corpus/tools/build_visualizer.py            # rewrite visualizer.html
    python3 corpus/tools/build_visualizer.py --check    # exit 1 if it would change

Exits non-zero on: a metadata target that no longer exists, a topic-folder with no
metadata entry, a duplicate node id, or an edge endpoint that is not a live node.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = os.path.join(ROOT, "content")
HTML = os.path.join(CONTENT, "visualizer.html")
META = os.path.join(ROOT, "corpus", "tools", "visualizer_meta.json")

GROUP_RE = re.compile(r"^pillars/0(\d)-")

# Folders that have an index.md but deliberately no node in the graph.
# `foundations` is an area hub page with no F-HUB node (the 9 F-* topics hang off the
# pillars instead). It is a graph-design choice, not an oversight -- keep it listed here
# so a genuinely-new unmapped topic still fails loudly.
NO_NODE = {"foundations"}


def norm(target: str) -> str:
    t = target.strip().strip("/")
    if t.endswith("/index"):
        t = t[: -len("/index")]
    if t.endswith(".md"):
        t = t[:-3]
    return t


def group_of(target: str) -> str:
    if target.startswith("foundations"):
        return "foundations"
    if target.startswith("fundamentals-accounting"):
        return "fundamentals-accounting"
    m = GROUP_RE.match(target)
    if m:
        return "p" + m.group(1)
    raise SystemExit(f"cannot derive group for {target!r}")


def resolves(target: str) -> bool:
    """Live if it is a page (.md) or a folder with an index.md."""
    return os.path.isfile(os.path.join(CONTENT, target + ".md")) or os.path.isfile(
        os.path.join(CONTENT, target, "index.md")
    )


def url_for(target: str) -> str:
    """The URL quartz serves for this target."""
    if os.path.isfile(os.path.join(CONTENT, target + ".md")):
        return "/" + target
    return "/" + target + "/"


def discover_topic_folders() -> set[str]:
    found = set()
    for root, dirs, files in os.walk(CONTENT):
        if "_legacy" in root.split(os.sep):
            continue
        if "index.md" in files:
            rel = os.path.relpath(root, CONTENT)
            if rel != ".":
                found.add(rel.replace(os.sep, "/"))
    return found


def build() -> tuple[list[dict], list[dict]]:
    meta = json.load(open(META, encoding="utf-8"))
    targets, raw_links = meta["targets"], meta.get("links", [])

    bad = [t for t in targets if not resolves(t)]
    if bad:
        raise SystemExit(
            "metadata targets that no longer exist on disk "
            "(repoint them, or retire the node):\n  " + "\n  ".join(bad)
        )

    unmapped = sorted(f for f in discover_topic_folders() if f not in targets and f not in NO_NODE)
    if unmapped:
        raise SystemExit(
            "topic-folders with no metadata entry (add them to visualizer_meta.json):\n  "
            + "\n  ".join(unmapped)
        )

    ids = [v["id"] for v in targets.values()]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit("duplicate node ids: " + ", ".join(sorted(dupes)))

    nodes = [
        {
            "id": v["id"],
            "title": v["title"],
            "group": group_of(target),
            "path": url_for(target),
            "math": v["math"],
            "code": v["code"],
            "intuition": v["intuition"],
            "failure": v["failure"],
        }
        for target, v in sorted(targets.items(), key=lambda kv: (group_of(kv[0]), kv[1]["title"]))
    ]

    idset = {n["id"] for n in nodes}
    seen, links = set(), []
    for entry in raw_links:
        src, dst, typ = entry
        for endpoint in (src, dst):
            if endpoint not in idset:
                raise SystemExit(
                    f"edge {src!r} -> {dst!r} references unknown node {endpoint!r}; "
                    "if that node was retired, repoint or drop the edge in visualizer_meta.json"
                )
        if (src, dst) in seen:
            raise SystemExit(f"duplicate edge {src!r} -> {dst!r}")
        seen.add((src, dst))
        links.append({"source": src, "target": dst, "type": typ})

    touched = {e["source"] for e in links} | {e["target"] for e in links}
    isolated = sorted(idset - touched)
    if isolated:
        print("note: nodes with no edge: " + ", ".join(isolated), file=sys.stderr)

    return nodes, links


def render(nodes: list[dict], links: list[dict]) -> list[str]:
    n = json.dumps(nodes, ensure_ascii=False, separators=(", ", ": "))
    l = json.dumps(links, ensure_ascii=False, separators=(", ", ": "))
    return ["      nodes: " + n + ",", "      links: " + l + ","]


def replace_block(html: str, new_lines: list[str]) -> str:
    """Swap the nodes:/links: lines in place. Line-based on purpose: a regex over
    ~30 KB of JSON is exactly the fragile structured-text edit that caused the bugs
    this generator exists to prevent."""
    lines = html.split("\n")
    i = next((k for k, ln in enumerate(lines) if ln.lstrip().startswith("nodes: [")), None)
    if i is None:
        raise SystemExit("could not find the `nodes: [` line in visualizer.html")
    j = next((k for k in range(i, len(lines)) if lines[k].lstrip().startswith("links: [")), None)
    if j is None:
        raise SystemExit("could not find the `links: [` line in visualizer.html")
    end = next((k for k in range(j, len(lines)) if lines[k].rstrip().endswith("],")), None)
    if end is None:
        raise SystemExit("could not find the end of the `links: [` array")
    return "\n".join(lines[:i] + new_lines + lines[end + 1:])


def main() -> int:
    check = "--check" in sys.argv
    nodes, links = build()
    html = open(HTML, encoding="utf-8").read()
    updated = replace_block(html, render(nodes, links))
    if updated == html:
        print(f"visualizer up to date ({len(nodes)} nodes, {len(links)} links)")
        return 0
    if check:
        print("visualizer is STALE -- run: python3 corpus/tools/build_visualizer.py")
        return 1
    open(HTML, "w", encoding="utf-8").write(updated)
    print(f"rewrote visualizer.html: {len(nodes)} nodes, {len(links)} links")
    return 0


if __name__ == "__main__":
    sys.exit(main())

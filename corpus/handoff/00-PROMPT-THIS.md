# Alfred — inform the agent where the paid sources are

> Paste the block below into Hermes when resuming the Kwant-Atlas build.
> Before pasting: tell the agent where the delivered paid sources are (a local path or Google Drive location).
> This block is self-contained — the agent re-reads all context from the handoff files on disk.

---

```markdown
Continue the Kwant-Atlas project for the Kwant Klubben (quant finance club).

CONTEXT FIRST — read and internalize these before doing anything:
1. /home/alfred/local-repos/kwant-atlas/corpus/handoff/01-VISION-AND-STRUCTURE.md
2. /home/alfred/local-repos/kwant-atlas/corpus/handoff/02-PROJECT-STATE-AND-FILEMAP.md
3. /home/alfred/local-repos/kwant-atlas/corpus/handoff/03-BUILD-METHOD-AND-TEMPLATE.md
4. /home/alfred/local-repos/kwant-atlas/corpus/handoff/04-NEXT-SESSION-BRIEF.md
5. /home/alfred/local-repos/kwant-atlas/corpus/handoff/05-EXECUTION-REALITY-AND-SCALE.md
6. /home/alfred/local-repos/kwant-atlas/corpus/handoff/06-ENVIRONMENT-AND-TOOLING.md
Also read corpus + titles under /home/alfred/local-repos/kwant-atlas/corpus/ and the
verified deep-reads under /home/alfred/local-repos/kwant-atlas/corpus/verified/.
Read 06-ENVIRONMENT first — it documents the installed tools, the flaky vision backend
fallback (text layer + analytic re-derivation, never trust raw pdftotext math), and the
critical warning NOT to git-clean/reset (corpus/ is untracked and holds the handover).

CRITICAL — KNOW THE MIGRATION GAP (doc 02 §5, doc 05):
The current content/ is the OLD DRAFT, NOT the target structure. It has 8 pillars ×
(hub + 6 flat topic notes) = 65 files. The folder-per-topic structure (topic = folder
with index.md hub + sub-pages carrying intro→advanced depth) does NOT exist yet ANYWHERE.
Building the Atlas is a MIGRATION + MAJOR EXPANSION, and a single pillar to full depth is
THOUSANDS of lines — a long, multi-session effort. Read doc 05 for the working method:
one pillar at a time (Pillar 3 first), one topic-folder at a time, sources-first, verified
files authoritative for formulas, worked runnable code mandatory, correctness over volume,
work in defensible chunks, use subagents per precise topic-folder spec + one central
lockstep pass. Do NOT try to build everything at once.

WHAT THE ATLAS IS (the heart of the project — hold this in mind at all times):
It is a first-principles knowledge graph of quantitative finance for the club,
built so people of ANY background (CS, math, econ, none) can enter any topic
from zero. It deliberately MARRIES three equally-important jobs — none may be dropped:
  (1) FIND + UNDERSTAND QUICKLY  — the best lookup guide in the club: it condenses the
      important books and many fields into one clear, correct, findable spot.
  (2) FOLLOW A PATH AND BUILD    — from bare bones you can traverse the knowledge in a
      sensible order and build a real quant project, discovering related areas.
  (3) DEBUG FROM FIRST PRINCIPLES — when you're building and it breaks, walk
      symptom → first-principles root cause → fix, through the same knowledge.
A graph alone gives overview but isn't useful when studying or debugging; study paths
alone don't let you jump to an answer; a lookup alone doesn't teach you to build.
The Atlas must do all three from the SAME source of truth. That marriage is the point.

It must serve the full audience arc at once:
  • BEGINNERS (from zero, any background) — intuition first, so they understand WHY.
  • INTERMEDIATES (implementing) — working, correct math AND code.
  • EXPERTS / FRONTIER — depth approaching (near) Wall-Street implementation.
So each topic carries: intuition → mathematical ground truth → working code → advanced sections.
A member goes from "never priced an option" to "understands HJM no-arbitrage" and beyond.

CONTENT MODEL (locked): folder-per-topic. Each topic = a folder with an index.md hub
(overview + lookup tables + links into its sub-pages) + sub-pages carrying intro-to-advanced
depth with worked math/code. The sub-pages are the topic's OWN internal structure, NOT a
detached graded lesson track (we rejected graded tracks as too much complexity).
Navigation is by strong lists and indexes — the graph is only an overview assist.
One source of truth, public repo, members clone + PR.

STRUCTURE: 8 operational pillars (P1 quant research · P2 algorithmic/HFT · P3 derivative
pricing · P4 risk · P5 portfolio · P6 market making · P7 ML/alt data · P8 quant dev) +
a shared foundations math toolbox + a cross-cutting Fundamentals & Accounting area.

THE PLAN THIS SESSION:
1. Verify the paid sources I've delivered (I'll tell you where they are).
2. Run the verified deep-read pipeline (handoff doc 03 §2) on the new sources.
3. Build PILLAR 3 (Derivative Pricing) to full depth FIRST as the flagship model —
   folder-per-topic, 6-section template, intuition→math→code→advanced, updating
   visualizer.html + index.md diagnostic matrix + pillar hub + README in lockstep.
4. Review Pillar 3 with me, then scale the pattern to the other pillars + foundations + fundamentals.

WORKFLOW: use a git branch, verify, merge to main, delete orphan branches.
Before doing ANY work: confirm you've read the handoff docs and restate in your own words
(1) the three married jobs of the Atlas, (2) the audience arc it must serve, (3) the
folder-per-topic content model and why we chose it, (4) that the current content/ is the
OLD draft and the folder-per-topic depth does NOT exist yet (the migration gap), and
(5) the scale reality — one pillar at a time, thousands of lines each, correctness over
volume, Pillar 3 first. Then start with source verification.
```

# Kwant-Atlas — Environment & Tooling (handoff 2026-09-09)

> The toolchain this project relies on, what's confirmed installed, and the known quirks. A fresh agent must read this before running the deep-read pipeline or building, so it doesn't rediscover (or worse, trust) broken assumptions.

---

## 1. Confirmed CLI tools (present on this machine, verified 2026-09-09)

| Tool | Path | Used for |
|---|---|---|
| `pdftotext` | /usr/bin/pdftotext | PDF → text layer for reading |
| `pdftoppm` | /usr/bin/pdftoppm | PDF → page PNGs (for vision / math-aware read) |
| `pdfinfo` | /usr/bin/pdfinfo | page counts, metadata |
| `tesseract` | /usr/bin/tesseract | OCR (only needed for PDFs with no Unicode text layer, e.g. Type-3 fonts) |
| `curl` | /usr/bin/curl | downloading sources (`-L` + browser user-agent to avoid bot-blocks) |
| `git` | /usr/bin/git | version control |
| `node` / `npm` / `npx` | mise-managed, v26.8.1 / 11.19.0 | Quartz build (`npx quartz build`) |
| `python3` | mise-managed | scripting |
| `uv` | ~/.local/bin/uv | Python package/venv management |
| `mise` | /usr/bin/mise | runtime version manager (node, python) |

**NOT installed:** `pandoc`, `wget`. For docx/xlsx reading, prefer Python (`python-docx`, `openpyxl`) or `unzip` + XML — don't assume pandoc.

---

## 2. Python libraries — ⚠️ NOT stably installed

**Critical honest gotcha:** the execute_code/agent Python environment used this session had `PIL` available, but **`numpy`, `pandas`, `openpyxl`, `python-docx`, `scipy`, `statsmodels`, `pypdf` were NOT present** in a stable, known venv. Subagents that read `.docx`/`.xlsx` (the notes, screening workbooks) installed what they needed **on-the-fly** during the session, and those installs are **not guaranteed to persist** for a fresh session.

**Action for the next session:**
- Before relying on any Python lib (openpyxl, python-docx, numpy, pandas), check `import <lib>` and install as needed, e.g. with `uv pip install <lib>` (or `pip install` into the active interpreter).
- The safe pattern: the deep-read pipeline is **CLI-driven** (`pdftotext`/`pdftoppm` are installed), so math extraction doesn't depend on Python libs. Python libs are only needed for `.docx`/`.xlsx` source reading.

---

## 3. The vision backend — ⚠️ unreliable (critical known quirk)

The `vision_analyze` tool for reading rendered page PNGs was **flaky all session**: it returned **intermittent HTTP 404s** on local file paths and data-URLs. This is NOT a bug in the pipeline; it's an external backend.

**The fallback that works (and was used successfully all session):**
1. `pdftotext` gives a text layer. For many books this is faithful and page-aligned.
2. When a formula is contested or the text layer is corrupted (dropped Greek letters, collapsed exponents, lost ½ factors), **re-derive the formula analytically** and cross-check against canonical results.
3. Retry `vision_analyze` periodically — it often recovers.
4. **Never copy a formula from a raw text dump into the Atlas without this cross-check.** The `corpus/verified/*.md` files are the authoritative, already-cross-checked source.

**Important:** the verified per-chapter files (`corpus/verified/`) already did this cross-checking for the 11 textbooks. A fresh agent building from those does NOT need to re-run vision — only new sources being deep-read need it, and should use the same fallback discipline.

---

## 4. Quartz build

- Repo: `~/local-repos/kwant-atlas/` — Quartz v4 (this is a fork; many `upstream/*` remotes exist — see §6 of this doc).
- `package.json` and `node_modules/` are present.
- Build with `npx quartz build`. Preview with `npx quartz preview`.
- **Broken-wikilink check:** Quartz surfaces unresolved `[[links]]` — run a build after adding content to catch them.
- `visualizer.html` node/link data is **hardcoded** — new notes won't appear in the D3 graph until their node JSON + edges are added (see `03-BUILD-METHOD` §5).
- **YAML frontmatter titles must be plain ASCII — no backslashes.** A title containing LaTeX like `$\gamma$` produces `unknown escape sequence` and **aborts the whole quartz build** (error is on the file, but the site won't emit at all). Write `Gamma` in the title, keep the math for the body. If a build fails, grep frontmatter titles for `\`: `grep -rn '^title:.*\\\\' content/`.
- **Numeric-literal table rows are not wikilinks.** `[[1.0,0.0,-1.0]]` in a numpy code fence is matched by naive `[[...]]` link-checkers — ignore those false positives when auditing dangling links; strip a trailing `\` (from `\|` table escapes) before resolving.

---

## 5. Source-reading conventions established this session

- **Rendering math-dense books:** `pdftoppm -png -r 120 <pdf> <prefix>` → numbered `p-001.png`... pages. Watch the printed-vs-PDF page offset (it varied per book — verify with a page-header read).
- **Clean filenames for downloads:** `AuthorYear_ShortTitle.pdf` in `~/kwant-atlas-sources/free/<domain>/`.
- **Verify downloads:** check `file <pdf>` says PDF and size > 5KB (or >100KB for books); retry alternate source on HTML-error/too-small.

---

## 6. Git layout — know before you branch

- The repo has many `remotes/upstream/*` branches (Quartz v4/v5, feature branches) plus `origin/main`.
- **Local branch:** `main`, tracking `origin/main`.
- **Only `content/Inbox.md` and `corpus/` are untracked** (not yet committed) — this entire handover lives in `corpus/`. **Do not `git clean` or hard-reset**; you will lose the handover and all research.
- Workflow per user: create a feature branch for build work, verify, merge to `main`, delete orphan branches.

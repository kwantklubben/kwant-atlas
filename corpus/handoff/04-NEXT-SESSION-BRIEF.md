# Kwant-Atlas — Next-Session Brief (for the session that picks this back up)

> Read `01-VISION-AND-STRUCTURE.md`, `02-PROJECT-STATE-AND-FILEMAP.md`, `03-BUILD-METHOD-AND-TEMPLATE.md` first. This is the runbook for what to do when we resume.

---

## Context to re-establish immediately
This session (2026-09-09) was spent: cleaning the user's Google Drive Investing folder → extracting + math-verifying its 11 textbooks into 43 verified per-chapter files → researching the full corpus wishlist for the Atlas (8 pillars + foundations + fundamentals) → downloading the ~252 free sources → building the Atlas vision/structure. The user will now **deliver the ~304 paid sources** we're missing.

---

## First actions when we resume

### 1. Receive the user's sources
- The user said they'll get the **304 missing (code 3) books/papers**.
- Ask where they are (Google Drive folder? a local dir? zipped?). **Verify they arrived** and take inventory (count, integrity, which titles).

### 2. Stage + deep-read (Pillar 3 first, per Option A)
- The **flagship is Pillar 3 (Derivative Pricing)** — build it to full depth first as the model.
- For each newly-delivered paid source, run the **verified deep-read pipeline** (see `03-BUILD-METHOD` §2): pdftotext + pdftoppm, one subagent per chapter-group, produce corrected per-chapter `.md` in the verified set.
- **Pillar 3 priority sources** (the gaps beyond what's already verified): Gatheral *Volatility Surface*, Bergomi *Stochastic Volatility Modeling*, Andersen-Piterbarg *Interest Rate Modeling*, Gregory *xVA Challenge*, Haug *Option Pricing Formulas*, Natenberg *Option Volatility & Pricing*, Duffy *Finite Difference Methods*.
- Cross-check the delivered set against `corpus/titles/pillar3-derivative-pricing.TITLES.md` to confirm coverage of the 37 paid items.

### 3. Build Pillar 3 (folder-per-topic)
- Use `03-BUILD-METHOD` §3/§4/§5: the 6-section template, folder-per-topic structure, and lockstep maintenance.
- Write topic folders from the **verified** material (verified files win over raw text).
- Update visualizer.html + index.md diagnostic matrix + pillar hub + README **in lockstep**.
- `npx quartz build`, check broken links, spot-check formulas.

### 4. Review together → then scale
- Review Pillar 3 with the user. Confirm the depth/navigation pattern feels right.
- Then replicate the pattern across the other pillars + foundations + fundamentals (each is a mini-course).

---

## Important notes / gotchas

- **Branch workflow** (user preference): work on a branch → verify → merge to main → delete orphan branches.
- **`visualizer.html` nodes are hardcoded** — new pages are invisible in the graph unless their node JSON + edges are added. This is the #1 thing that silently goes stale.
- **Verified files are authoritative** for formulas; raw `pdftotext` mangles math (Greek, exponents, ½ factors). Re-derive/cross-check before copying into the Atlas.
- **Copyright:** copyrighted books stay out of the public repo — reference by title/chapter; host actual PDFs in the club's private Google Drive (kwant-cowork) if needed.
- **The Investing Google Drive folder** is slated for deletion once knowledge is extracted; the verified files + corpus are the preserved knowledge (also copy verified/ into the repo so it survives folder deletion).

---

## Suggested starting prompt for next session
"Continue the Kwant-Atlas build. The user delivered the paid sources. Re-establish from the handoff docs in `corpus/handoff/`, verify the delivered sources, run the deep-read on the Pillar 3 set, and build Pillar 3 to full depth as the flagship. Then we review and scale."

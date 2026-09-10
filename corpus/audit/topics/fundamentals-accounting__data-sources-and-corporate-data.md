# Audit — `content/fundamentals-accounting/data-sources-and-corporate-data/`

**Auditor:** sole reviewer (adversarial) · **Date:** 2026-09-10
**Scope:** 7 files (index + 01–06) · **Files checked:** 7 · **Python blocks run:** 7 (all matched) · **Network stubs skipped:** 1

---

## Verdict

**PASS WITH MINOR FIXES.** The folder is internally well-built: all seven runnable
Python blocks execute cleanly and reproduce their documented output fences
*exactly* (byte-for-byte after whitespace trim); every wikilink resolves; no
spelling/typo errors were found in prose; the EDGAR endpoint patterns, the ≤10
req/s rate limit, the Ken-French 3/5/6-factor/1926 claims, and the data-access
notes all check out against `corpus/titles/refs/fundamentals/Data_SEC_EDGAR_access.txt`,
`Data_KenFrench_DataLibrary_access.txt`, and `Data_XBRL_Taxonomies_access.txt`.

The defects found are localized: one numerical inconsistency in the hub's own
provenance formula, one code-comment/behaviour mismatch, and a cluster of
stale (pre-Sept-2024) Schedule 13D/13G deadline claims in page 04.

---

## (3) CODE — every block run, diffed vs documented fence

Extracted each fenced ```python block, executed with `python3`, and diffed stdout
against the adjacent plain fence. Result: **7/7 exact matches.**

| File | Block | rc | Result |
|---|---|---|---|
| index.md | SOURCES registry audit | 0 | ✅ match ($66,500; 8 free/5 paid; 9/13 PIT; buckets [0,1,30,45,365]) |
| 01 | layers + look-ahead leak | 0 | ✅ match (36.36% / 30.43% / 5.93 pp) |
| 02 | companyfacts → canonical mapper | 0 | ✅ match (10.50% margin, 47.10% equity/assets) |
| 02 | live fetch stub | — | ⏭ skipped (requires network; correctly flagged as such in-file) |
| 03 | three-provider EBITDA reconciliation | 0 | ✅ match (median 210, spread 5.7%, EV/EBITDA 9.60) |
| 04 | Form 4 flow + cluster + 13-F | 0 | ✅ match (+$100,500; CLUSTER BUY; 55.0%) |
| 05 | three biases quantified | 0 | ✅ match (+6.25% / −15.00% / 21.25 pp; 8.3 min) |
| 06 | company-tracker panel | 0 | ✅ match (10.68/10.43/10.45%; CAGRs 6.20/3.15/3.90%) |

All printed numbers were also re-derived by hand where non-trivial (median EV/EBITDA,
CAGR ladder, HHI/ownership, cluster-window arithmetic) — none disagree with the fence.

---

## (1) SPELLING / TYPOGRAPHY

**No genuine misspellings found.** A dictionary sweep (cracklib-small + domain
allowlist) over prose with code/LaTeX/inline-code/wikilinks stripped returned only
compound jargon, company names, and acronyms (`Sharadar`, `Compustat`, `EDGAR`,
`point-in-time`, `as-reported`, …). No corrections required.

---

## (2) MATH / TECHNICAL-FACT ERRORS

### E1 — Hub provenance formula contradicts its own registry *(index.md:35 vs :114)*
- **Stated** (index.md:35): `lag ∈ {0, 1, 45, 90, 365} days (by source)`.
- **Actual** (registry, index.md:65–80; emitted output index.md:114): staleness
  buckets are `[0, 1, 30, 45, 365]`.
- **Correct:** `90` never occurs in any source; `30` (Ken French) is omitted from the
  formula. The two sets should be identical. **Severity: medium (self-contradiction).**

### E2 — Schedule 13G deadlines are stated under the pre-Sept-2024 regime *(04:23, 04:38)*
- **Stated:** "**13-G annually**" (04:23) and table row `13-G | passive >5% holder | …
  | 45 days after quarter end` (04:38).
- **Correct (current rules, effective 2024-09-30):** a **passive** investor's initial
  Schedule 13G is due **within 5 business days** of crossing 5% (Rule 13d-1(c)); the
  **45-days-after-quarter-end** deadline applies to **Qualified Institutional Investors**
  (Rule 13d-1(b)), and *all* 13G amendments are now due **quarterly** (45 days after
  quarter end) — not annually. Verified against SEC Regulation 13D-G guidance and the
  2024 rule amendments.
- **Severity: medium (stale factual claim in a datestamped corpus).**

### E3 — "10 for passive-ish" on the Schedule 13-D row is muddled *(04:37)*
- **Stated:** `13-D … 5 business days (10 for passive-ish)`.
- **Correct:** Schedule **13D** is due within **5 business days** (no passive variant —
  the "passive" form is **13G**). The "10" figure is the **pre-2024** 13D deadline
  (10 calendar days) / the old passive-13G window. The parenthetical conflates rule
  families and eras. **Severity: low–medium.**

### E4 — Code comment contradicts actual filter behaviour *(05:61)*
- **Stated:** `returns = {"A":0.12,"B":0.08,"C":-0.15,"D":-1.00,"E":0.20}  # D,E delisted`.
- **Actual:** `survivors = {k:v for … if v > -1.0}` drops **only D** (−1.00); **E**
  (return +0.20) stays in the survivor set and drives the printed +6.25%.
- **Correct/impact:** the comment "D,E delisted" is wrong, and it **does not change the
  printed output** — the documented fence (+6.25 / −15.00 / 21.25 pp) is produced, so
  the block still reproduces. But a reader "fixing" the filter to also drop E would get
  a different, undocumented number. Comment/label should be corrected. **Severity: low.**

### E5 — Restatement-gap sentence appears internally inverted *(05:42)*
- **Stated:** "…a database that keeps only `x_r` systematically understates the good news
  available at the time **and overstates the quality of firms that later turned out to
  have problems.**"
- **Concern:** the first clause is correct (downside restatements lose contemporaneous
  good news). The second clause's direction does not follow: keeping the *lower*
  restated value makes a problem firm look *worse*, not higher-quality. The clause reads
  as inverted/confusing. **Severity: low (wording; flag for author review, confidence medium).**

### E6 — "XBRL taxonomies" counted as a point-in-time dataset *(index.md:42; registry)*
- The registry marks `XBRL taxonomies` as `pit: True, lag: 0` and lists it under
  *"free AND point-in-time (the zero-cost honest stack)"* (index.md:102–107).
- A taxonomy is a **reference schema**, not a timestamped data series — it has no
  as-of semantics. Counting it inflates the headline "9/13 point-in-time" and the
  "honest stack" list. **Severity: low (category slip).**

---

## Minor notes (not counted as errors)

- **index.md:41** lists `Form 4, 13-F` inside the EDGAR row's "US filings + XBRL facts"
  phrase. Those ownership forms are XML filer documents, not XBRL financial facts in
  `companyfacts`. Readable, but imprecise.
- Cost figures are consistently marked approximate (`~$500`, `$$$$$`, registry `500/12000/24000`)
  and are internally consistent between prose and code; Bloomberg (~$24k) and FactSet
  (~$12k) are within the plausible industry range, so no correction is asserted.

---

## (4) COHERENCE

- **Hub ↔ 01 prerequisite consistency: OK.** index.md:11 states the folder-level
  prerequisites (Financial Statements & Accounting + Core Financial Ratios) apply to
  pages 02–06, and that page 01 "states its own, smaller, entry requirements" —
  page 01:10 indeed lists only *Financial Statements & Accounting*. Consistent.
- **Structure: OK.** index + 6 sub-pages (01–06), matching the "six sub-pages" claim
  (index.md:19, :146) and the reading route (index.md:148–152).
- **Links: OK.** All 18 distinct wikilink targets resolve to existing files. The `\|`
  escapes seen inside table cells (01:29, 03:116, 06:126–130) are the repo-wide
  convention for a pipe inside a Markdown table — confirmed used across many other
  topic folders; **not** a defect.
- **Cross-page references:** the forward/back "Connected Graph Bridges" form a
  consistent chain (01→02→03→04→05→06); every "measured in §3 / formalized in 05"
  pointer resolves to the intended page.
- **Data-access-note references** (`Data_SEC_EDGAR_access.txt`,
  `Data_KenFrench_DataLibrary_access.txt`) exist under
  `corpus/titles/refs/fundamentals/` and corroborate the endpoint patterns, the
  10-req/s guidance, and the 1926/3-5-6-factor claims.

---

## Summary of required fixes

| # | Location | Fix |
|---|---|---|
| E1 | index.md:35 | Change `{0, 1, 45, 90, 365}` → `{0, 1, 30, 45, 365}` (match registry/output). |
| E2 | 04:23, 04:38 | Update 13G deadlines to post-2024 rules (passive: 5 business days; QII: 45 days after QE; amendments quarterly). |
| E3 | 04:37 | Drop or correct "(10 for passive-ish)" on the 13-D row. |
| E4 | 05:61 | Fix "D,E delisted" comment (only D is filtered) or adjust the filter + fence. |
| E5 | 05:42 | Reword the second clause of the restatement-gap sentence. |
| E6 | index.md:42 | Don't classify "XBRL taxonomies" as PIT / remove from "zero-cost honest stack". |

**errors_found: 6** (E1–E6) · **files_checked: 7** · **blocks_run: 7** · verdict: **pass-with-minor-fixes**

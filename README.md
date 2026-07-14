# PUI — Purāṇic Index

_Created: 05-04-2026 · Last updated: 05-07-2026_

Corrections and issue-tracking repository for the Cologne Digital Sanskrit
Lexicons digitisation of Vettam Mani's *Purāṇic Index* (1951) — a
comprehensive encyclopaedia of Epic and Purāṇic literature. The digitised
text has 12,987 tokens flagged as possible diacritic/encoding errors out of
a much larger corpus; this repo is where those get found, reviewed, and
turned into corrections against the canonical source.

---

## Why this repo exists

The primary source text lives in
[`csl-orig/v02/pui/pui.txt`](https://github.com/sanskrit-lexicon/csl-orig) in
the sibling `csl-orig` repository — that file is never edited directly (see
the org-wide [correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)).
Instead, this repo holds:

- **Detection scripts** that scan `pui.txt` for likely digitisation errors
  (mis-transliterated diacritics, improbable n-grams from OCR noise).
- **Per-issue folders** (`issues/issueN/`) with the scan output, the
  change files derived from it, and the audit trail.
- **Issue tracking** against the taxonomy shared by every Sanskrit Lexicon
  dictionary repo (see [Labels](#labels) below).

Corrections never land in `csl-orig` directly from here — they're queued,
validated, and delivered in the monthly consolidated PR (`/cologne-batch-pr`).

---

## How it works

```mermaid
flowchart LR
  S["Print scan PDF"] -->|OCR / keyboarding| R["raw pui.txt"]
  R --> O["csl-orig/v02/pui/pui.txt"]
  O -->|updateByLine.py + change files| C["corrected pui.txt"]
  C --> O
  O -->|generate_dict.sh| X["pui.xml"]
  X --> A["csl-app web display"]
```

1. A detection script scans `pui.txt` and writes flagged candidates to a
   `.tsv` under `issues/issueN/`.
2. A human/agent reviews the candidates and decides which are genuine
   errors vs. legitimate proper nouns (Sanskrit names correctly carry
   diacritics — the point of [`issue1`](https://github.com/sanskrit-lexicon/PUI/issues/1)
   was separating "real English words that slipped past OCR" from "real
   Sanskrit names", not flagging every diacritic).
3. Confirmed corrections become a change file, applied via
   [`updateByLine.py`](https://github.com/sanskrit-lexicon/csl-pywork), and
   queued for the next `csl-orig` batch PR.

---

## Usage: reproduce the issue-1 diacritic scan

[`issues/issue1/analyze_diacritics.py`](issues/issue1/analyze_diacritics.py)
is the actual script that produced
[`issues/issue1/non_english_sorted.tsv`](issues/issue1/non_english_sorted.tsv)
(12,987 flagged tokens). As committed it needs two things not present in a
fresh checkout: a hardcoded absolute path to `pui.txt` on the original
author's machine, and a live download of the `dwyl/english-words` word list
over the network — so it is not directly runnable without editing the path
and having network access.

The output `.tsv` it produced **is** committed and small enough to inspect
directly — this is the runnable, verified part:

```python
import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('issues/issue1/non_english_sorted.tsv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))

print('total flagged tokens:', len(rows))
for row in rows[:5]:
    print(row['word'], row['count'])
```

Executed against this repo's checked-in data (05-07-2026):

```
total flagged tokens: 12987
Kṛṣṇa 1093
Manu 568
Brahmā 512
Śiva 502
Hari 448
```

The top hits are correctly-diacritised Sanskrit proper names (expected —
the script's job was to separate these from genuine OCR noise), which is
why issue #1 split the review into "≥6 occurrences" (high-confidence,
closed) and "≤5 occurrences" (long tail, still open as
[#4](https://github.com/sanskrit-lexicon/PUI/issues/4)).

To re-run the scan itself from scratch: edit the two hardcoded paths at the
top and bottom of `analyze_diacritics.py` to point at your local
`csl-orig/v02/pui/pui.txt` checkout and a writable output path, ensure
network access to GitHub raw content, then run:

```sh
python issues/issue1/analyze_diacritics.py
```

### issue3 — improbable n-grams

[`issues/issue3/issue3.py`](issues/issue3/issue3.py) similarly scans for
improbable letter sequences (OCR noise patterns like broken word-splits:
`tions`, `dence`) and wrote
[`issues/issue3/improbable_words.tsv`](issues/issue3/improbable_words.tsv)
(171 rows), each tagged with a pattern code (e.g. `1_mn_kg`, `2_m_tdlv`)
describing which OCR-noise heuristic flagged it.

---

## Contents

| Path | Purpose |
|---|---|
| [`issues/`](issues/) | Per-issue correction workflows (`issue1/`, `issue3/`, …) |
| [`CITATION.cff`](CITATION.cff) | Machine-readable citation metadata (CFF 1.2.0) |
| [`CLAUDE.md`](CLAUDE.md) | Developer guidance for Claude Code agents |

---

## Timeline

| Period | Activity |
|---|---|
| April 2026 | Repository created; initial encoding corrections for IAST diacritics (#1, #3) |
| April–May 2026 | Minor encoding corrections per issues #1 and #4; improbable-ngram review (#3) |
| May 2026 | CLAUDE.md added; CITATION.cff enriched with author and year |

---

## Projects & Milestones

| Milestone | Open | Closed | Total |
|---|---|---|---|
| Dictionary to Book | 0 | 0 | 0 |
| Digitization Quality | 1 | 2 | 3 |
| Structured Data | 1 | 0 | 1 |
| Major Enhancements | 0 | 0 | 0 |

### Solved issues

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| [#1](https://github.com/sanskrit-lexicon/PUI/issues/1) | Modern IAST for PUI >= 6 occurrences | `encoding` | minor | Digitization Quality |
| [#3](https://github.com/sanskrit-lexicon/PUI/issues/3) | Improbable ngrams | `text-correction` | minor | Digitization Quality |

### Open issues

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| [#2](https://github.com/sanskrit-lexicon/PUI/issues/2) | Questions for resolution | `question` | minor | Structured Data |
| [#4](https://github.com/sanskrit-lexicon/PUI/issues/4) | Modern IAST PUI <= 5 occurrences | `encoding` | minor | Digitization Quality |

---

## Labels

### Type labels

| Label | Description |
|---|---|
| `link-target` | Click-through from `<ls>` abbreviation to scanned PDF page |
| `link-splitting` | Split combined source references into per-page links |
| `markup` | Normalise XML tag content |
| `text-correction` | Corrections to headwords or definitions |
| `content-enhancement` | New material or display upgrades |
| `encoding` | SLP1/IAST transcoding and character normalisation |
| `scan-quality` | Replace blurry or missing scan pages |
| `bug` | Broken links, XML errors, broken downloads |
| `question` | Scholarly questions requiring research |

### Severity labels

| Label | Description |
|---|---|
| `minor` | Targeted fix — a handful of lines |
| `medium` | Standard work unit — one index or batch |
| `hard` | Large effort spanning many files |

---

## Encoding

- UTF-8 NFC throughout.
- Sanskrit text in SLP1 transliteration, wrapped in `{#…#}`.
- Display layer uses IAST (ISO 15919) and Devanagari, generated via `transcoder/`.
- Round-trip verified for the vast majority of entries; exceptions tracked under issue label `encoding`.

---

## Source

- **Author**: Mani, Vettam
- **Title**: *The Purāṇic Encyclopaedia: A Comprehensive Work with Special Reference to the Epic and Purāṇic Literature*
- **Publisher**: Delhi: Motilal Banarsidass
- **Year(s)**: 1951 (reprint 1975)
- **Scans**: available via Cologne Digital Sanskrit Lexicon mirrors
- **First digitisation**: Cologne Digital Sanskrit Lexicon project

---

## Contributors

- [Dr. Dhaval Patel](https://github.com/drdhaval2785)
- [Mārcis Gasūns](https://github.com/gasyoun)

---

_Dr. Mārcis Gasūns_

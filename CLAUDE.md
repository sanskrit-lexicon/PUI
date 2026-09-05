_Created: 15-05-2026 · Last updated: 05-09-2026_

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PUI** is the corrections repository for the Cologne digitization of V. R. Ramachandra Dikshitar's *The Purāṇa Index* (University of Madras, 3 vols, 1951–1955). The canonical source lives in `csl-orig/v02/pui/pui.txt`.

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/PUI/issues).

## Architecture

| Directory | Purpose |
|---|---|
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |

### Issue correction pattern (`issues/issueNNN/`)

Each issue folder follows the standard workflow:
1. Copy current `pui.txt` to a local `temp_pui_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_pui_1.txt`, `temp_pui_2.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit the corrected file to `csl-orig`, then sync to Cologne
5. Commit issue documentation back here

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh pui ../../PUIScan/2020
sh xmlchk_xampp.sh pui
```

## Dependencies

- **Python 3**
- **pui.txt** — in `$BASE/cologne/csl-orig/v02/pui/pui.txt`

---

## GitHub Issue Conventions

All issues follow the org-wide Sanskrit Lexicon taxonomy.

### Milestones

| Number | Title | Types |
|---|---|---|
| 1 | Dictionary to Book | `link-target`, `link-splitting` |
| 2 | Digitization Quality | `scan-quality`, `encoding`, `bug`, `text-correction` |
| 3 | Structured Data | `markup`, `question` |
| 4 | Major Enhancements | `content-enhancement` |

### Type labels (color `#0075ca`)

| Label | When to use |
|---|---|
| `link-target` | Click-through from `<ls>` abbreviation to scanned PDF page |
| `link-splitting` | Splitting combined source references into per-page links |
| `markup` | Normalising XML tags (`<ls>`, `<lex>`, `<ab>`, etc.) |
| `text-correction` | Corrections to headwords, definitions, Sanskrit text |
| `content-enhancement` | New material or display upgrades beyond correction |
| `encoding` | SLP1/AS/IAST transcoding, character rendering, normalisation |
| `scan-quality` | Blurry, skewed, or missing scan page replacements |
| `bug` | Broken links, XML errors, broken downloads |
| `question` | Scholarly or editorial questions requiring research |

### Severity labels

| Label | Color | When to use |
|---|---|---|
| `minor` | `#e4e669` | Targeted fix — a handful of lines or one file |
| `medium` | `#fbca04` | Standard work unit — one index, a batch of corrections |
| `hard` | `#d93f0b` | Large effort spanning many sources or files |

---

## Data format

PUI source files use the standard Cologne lightweight XML markup:

| Tag | Role | Example |
|---|---|---|
| `<L>NNNN` | Entry begin, with print line number | `<L>12345` |
| `<LEND>` | Entry end | |
| `<k1>headword` | Primary headword in SLP1 | `<k1>rAma` |
| `<k2>variant` | Secondary spelling | `<k2>rAma` |
| `<e>N` | Edition or entry marker | `<e>1` |
| `<lex>code` | Lexical category marker | `<lex>m.` |
| `<ls>source` | Literary source citation | `<ls>Bhāgavata P.` |
| `<ab>tag` | Italicised abbreviation | `<ab>m.</ab>` |
| `{#text#}` | Sanskrit text in SLP1 transliteration | `{#rAmaH#}` |
| `{%text%}` | Italicised display text | `{%see also%}` |

### Annotated example entry

```
<L>1<pc>001,1<k1>A<k2>A
A<lex>ind.</lex> a prefix of various meanings—
  negation: {%not%}, {%without%};
  approach: {%towards%};
  {%see%} <ls>Sk. 1.1.14.</ls>
<LEND>
```

- `<L>1` — entry number 1 in the print edition
- `<pc>001,1` — page 001, column 1
- `<k1>A` — primary headword `A` (SLP1 for the vowel ā)
- `<lex>ind.</lex>` — lexical class: indeclinable
- `{%not%}` — italicised English gloss
- `<ls>Sk. 1.1.14.</ls>` — citation to Siddha-kaumudī 1.1.14

_Dr. Mārcis Gasūns_

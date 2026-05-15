# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PUI** is the corrections repository for the Cologne digitization of M.A. Macdonell's *Puraṇic Index*. The canonical source lives in `csl-orig/v02/pui/pui.txt`.

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

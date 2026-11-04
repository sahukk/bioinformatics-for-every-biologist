# Chapter 3 — code and tests

| File | Purpose |
| --- | --- |
| `gc_content_spreadsheet.xlsx` | Step B: base counts for tulsi rbcL (MF468180.2) and three test cases, with the correct formula and the "brackets missing" formula |
| `gc_content.py`, `gc_content_naive.py`, `test_known.fasta` | Earlier Python version of Step B, now reserved for Chapter 10 (see notes/ch10-material-from-ch03.md) |

## Test record (spreadsheet)
- 2026-09-30, LibreOffice 26.8.0.3, macOS:
  - Correct `=(B3+B4)/(B2+B3+B4+B5)*100` → tulsi 43.07; tests 50, 100, 0.
  - Without brackets `=(B3+B4)/B2+B3+B4+B5*100` → tulsi 20921.47; tests 206, #DIV/0!, 500.
- Excel: not yet tested.

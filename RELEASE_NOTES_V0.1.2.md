# Release Notes — v0.1.2 (publication candidate, not final)

Date: 2026-11-11 · Predecessor: v0.1.1 (externally reviewed, not final; archive SHA-256 `e333c87928364fc8fa21ed93c74af1e2d7a25de45f78b781582bebb5d6ea627a`).

This version addresses the five required corrections of the independent Kimi AI review of v0.1.1
(verdict: PASS WITH CORRECTIONS / READY WITH MINOR EDITS; archived in `review/`). AI reviews are not scientific peer review.

## Required corrections

| # | Correction | v0.1.2 status |
|---|---|---|
| 1 | Zeta asymptotic domain `n>m>2`; `polygon_limit()` guard | DONE — manuscript states `n>m>2` (and `p>2` for `G_N`); `polygon_limit()` raises `ValueError` for `m<=2` or invalid `A/B`, `n<=m`. Reference value unchanged. |
| 2 | Scan-qualify the `N=4` minimum | DONE — abstract, polygon section, Figure 2 caption, conclusion, README, and `summary_results.json` now say "unique minimum within the computed N=3..1000 scan"; no global theorem claimed. |
| 3 | Remove `.pytest_cache/`, `__pycache__/`, `.pyc`; regenerate manifest | DONE — removed; `.gitignore` added; manifest regenerated; a test asserts none are listed. |
| 4 | `source_index` propagation + asymmetric regression test | DONE — `geometry_equilibrium(..., source_index=0)` added and passed to both `geometry_factor()` calls; used in `normalization_rescale_identity()` and `spherical_nearest_bounds()`. Tests on a non-vertex-transitive centroid-centered set and a co-spherical centrally symmetric set compare every source against a vertex-permutation oracle. Source-0 outputs are numerically unchanged. |
| 5 | Real GitHub URL in `CITATION.cff` | DONE — `repository-code` set to the author-supplied URL `https://github.com/eit-orbitos/EIT-LJ-Geometry` (2026-11-11); strict-xfail marker removed and the test now asserts the exact URL. Repository existence/contents not verified by this package. |

## Recommended precision edits also applied
- Large-N limit described as a nearest-neighbor-rescaled local infinite-chain limit with curvature-weighted radial projections (not a unit-projection chain sum `2ζ(p)`, not a continuum-circle integral).
- Conclusion now scopes the 1.3 exclusion to the reference parameters and the nearest-neighbor co-spherical class.
- `requirements.txt` pinned (Python 3.13.5, NumPy 2.2.5, Matplotlib 3.10.8, mpmath 1.3.0, pytest 9.0.2).

## Not changed (recommended, nonblocking, still open)
- Uncited Shannon (1948) entry remains in the bibliography. *(Post-release note: removed on `main` after the v0.1.2 tag; see `CHANGELOG.md`. The tagged/archived v0.1.2 still contains it.)*
- Full PolyForm / CC license texts not added (URL-based notices unchanged).
- Separate asymptotics for `m<2` and `m=2` not derived.

## Output changes vs v0.1.1
- All four CSV files: byte-identical.
- `summary_results.json`: only `version`, the large-N `interpretation` string, and a new `N_min_scope` string differ; all numbers identical.
- Figures 1–4 and 6: byte-identical. `figure_05_research_architecture.png` and `graphical_abstract.png`: version label / limit label text only.
- PDF recompiled from the edited LaTeX (pdfTeX 1.40.26, 12 pages); the v0.1.1 PDF is not duplicated in this tree.

## Tests
39 tests: 39 passed (correction 5 completed; its former strict expected failure now passes). The original nine tests are unchanged and pass.

## Status
Released as GitHub v0.1.2 and archived on Zenodo. Version DOI: 10.5281/zenodo.24149914; concept DOI: 10.5281/zenodo.24149913. No experimental validation of EIT/H-space or new physics is claimed; 0.9 and 1.3 remain heuristic.

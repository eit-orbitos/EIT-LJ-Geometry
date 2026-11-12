# Release Notes — v0.1.1

Status: **review-corrected candidate**

This release preserves the v0.1.0 numerical results while correcting interpretation and packaging issues identified by an independent Tasklet AI review.

## Nine mandatory corrections

1. Reclassified the two cuboid normalization conventions as an exact change of length unit, not distinct physical predictions.
2. Reclassified the deformed cuboid root as a constrained radial equilibrium; added full-vector tangential-residual calculation.
3. Replaced “continuum circle” language with the correct nearest-neighbor-rescaled infinite-chain interpretation.
4. Added the analytic large-N formula `R_inf=[(A/B) zeta(n-1)/zeta(m-1)]^(1/(n-m))`.
5. Added the co-spherical nearest-neighbor bound `R_ref/rho_max <= R_G <= R_ref`, proving `1.3` unreachable in that class for the reference model.
6. Removed the unsupported claim that the complete scan scope is historically documented as predeclared before all exploratory comparisons.
7. Added `scripts/build_all.py` so all committed CSV/JSON files and figures are reproducibly generated.
8. Removed caches, compiled Python files, LaTeX auxiliary files, and duplicate PDFs; clarified that P2-SMOOTH is out of scope.
9. Changed release licensing to PolyForm Noncommercial 1.0.0 for code and CC BY-NC-SA 4.0 for paper/figures/docs, conservatively aligning with the related project line.

## Additional verification

- Historical Jones DOIs and the 2024 Schwerdtfeger-Wales review DOI were externally rechecked during v0.1.1 preparation.
- Original v0.1.0 remains unchanged as a provenance snapshot.

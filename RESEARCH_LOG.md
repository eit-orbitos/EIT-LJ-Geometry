# Research Log — v0.1.2

1. Defined generalized force balance and reference LJ-derived equilibrium.
2. Introduced radial geometry factor and geometry-dependent radial root.
3. Established simplex cancellation for equal normalized pair distances.
4. Scanned regular polygons and Platonic solids.
5. Audited the heuristic 0.9/1.3 window; no derivation was accepted.
6. Added controlled cube-to-cuboid deformation.
7. Independent AI review of v0.1.0 reported PASS WITH CORRECTIONS.
8. v0.1.1 corrected normalization interpretation: alternate `d_ref` values are exact length-unit rescalings.
9. v0.1.1 corrected cuboid interpretation: radial root is not full vector equilibrium for `delta != 1`.
10. Derived the polygon large-N limit `[(A/B) zeta(n-1)/zeta(m-1)]^(1/(n-m))`.
11. Proved the co-spherical nearest-neighbor bound `R_ref/rho_max <= R_G <= R_ref`.
12. Added deterministic `scripts/build_all.py` to regenerate all data and figures.
13. Removed build caches, `.pyc`, LaTeX auxiliaries, and duplicate PDFs from the release archive.
14. Clarified that P2-SMOOTH is outside the scope of this geometry package.
15. Aligned licensing conservatively with the related project line: PolyForm Noncommercial for code; CC BY-NC-SA for paper/figures/docs.
16. Independent Kimi AI review of v0.1.1 reported PASS WITH CORRECTIONS / READY WITH MINOR EDITS (archived in `review/`).
17. Correction to entry 13: the v0.1.1 archive in fact still contained `.pytest_cache/`, two `__pycache__/` directories, and `.pyc` files. They are removed in v0.1.2; entry 13 is retained unchanged as historical record.
18. v0.1.2 restricted the large-N zeta formula to `n>m>2`; `polygon_limit()` now rejects `m<=2`.
19. v0.1.2 scan-qualified the `N=4` polygon minimum ("unique minimum within the computed N=3..1000 scan"); no global theorem is claimed.
20. v0.1.2 fixed `source_index` propagation in `geometry_equilibrium()`, `normalization_rescale_identity()`, and `spherical_nearest_bounds()`; added asymmetric-geometry regression tests. Source-0 outputs are numerically unchanged.
21. v0.1.2 clarified that the large-N local-chain limit uses curvature-weighted radial projections, and scoped the 1.3 exclusion to the stated co-spherical nearest-neighbor class.

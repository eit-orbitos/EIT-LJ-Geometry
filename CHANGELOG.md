# Changelog

## Post-release maintenance (main, after v0.1.2 tag)
- `PUBLICATION_PLAN.md`: current status updated to released/archived; the pre-release "publication candidate — not final, not released" text kept only as superseded history.
- Bibliography: uncited Shannon (1948) entry removed from `paper/references.bib` and from the manual `thebibliography`; the manual `thebibliography` in `paper/manuscript.tex` is documented as the canonical rendered source. PDF recompiled (only the uncited reference is gone).
- `scripts/build_all.py`: removed a no-op `for ...: pass` loop in the Figure 5 section (outputs byte-identical).
- `CITATION.cff`: added `license` (PolyForm-Noncommercial-1.0.0, CC-BY-NC-SA-4.0) and a `preferred-citation` for the Zenodo preprint; validated with cffconvert.
- `MANIFEST.sha256` regenerated last. No numerical result changed; the `v0.1.2` tag and the Zenodo archive are unchanged.

## Post-release metadata (after v0.1.2 tag)
Added Zenodo DOIs to `CITATION.cff` and `README.md` (version DOI 10.5281/zenodo.24149914; concept DOI 10.5281/zenodo.24149913), plus a DOI regression test; `MANIFEST.sha256` regenerated. No code, data, figure, or manuscript change. The `v0.1.2` tag (commit `fc98ea3`) is unchanged and is what Zenodo archived; that tagged copy does not contain the DOI.

## v0.1.2 — 2026-11-11
Publication candidate (not final). Addresses the five required corrections of the independent Kimi v0.1.1 review. See `RELEASE_NOTES_V0.1.2.md`.

## v0.1.1 — 2026-10-28
Review-corrected release candidate. See `RELEASE_NOTES_V0.1.1.md`.

## v0.1.0 — 2026-10-28
Initial reproducible research package.

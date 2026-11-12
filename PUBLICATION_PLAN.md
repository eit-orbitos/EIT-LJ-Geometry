# Publication Plan — v0.1.2

## Before GitHub/Zenodo

1. Run `python scripts/build_all.py` from a clean checkout.
2. Run `pytest -q` and archive the output.
3. Compile the LaTeX manuscript and visually inspect the PDF.
4. Recompute `MANIFEST.sha256` after all edits.
5. Obtain at least one additional independent review if possible.
6. Verify repository visibility, author metadata, and final release tag.
7. Upload the exact release archive to Zenodo and record the DOI in the repository only after Zenodo publication.

## Licensing

- Code: PolyForm Noncommercial 1.0.0
- Manuscript/figures/documentation: CC BY-NC-SA 4.0

Because the archive contains mixed licensing, the Zenodo description should state both licenses explicitly rather than implying one license applies to every file.

## Claim discipline

Do not publish claims such as “new gravity proven,” “EIT experimentally validated,” “Yang-Mills solved,” or “0.9/1.3 derived.” The current work supports a mathematical/computational geometry model and explicit negative results/limitations only.

## v0.1.2 status (2026-11-11)

- Status: **publication candidate — not final, not released**. Requires a short differential review of v0.1.1 → v0.1.2 before any GitHub release or Zenodo deposit.
- DONE (2026-11-11): `CITATION.cff` `repository-code` set to the author-supplied URL `https://github.com/eit-orbitos/EIT-LJ-Geometry`; `MANIFEST.sha256` regenerated; the former strict-xfail marker on `test_citation_repository_url_completed` removed. Uploading to GitHub is not authorized by this change.

## Release record (2026-11-11 local / 2026-11-12 UTC)

- Differential review v0.1.1 → v0.1.2: PASS for publication candidate (AI review, not peer review; it did not cover binaries, MANIFEST, or the new regression-test contents).
- Repository made public by the author; GitHub release `v0.1.2 — publication candidate` published by the author on tag `v0.1.2` → commit `fc98ea3`.
- Zenodo archived the release: version DOI 10.5281/zenodo.24149914; concept DOI 10.5281/zenodo.24149913. Zenodo shows the publication date as 2026-11-12 (UTC); `CITATION.cff` keeps the author-selected `date-released: 2026-11-11`.
- Status remains **publication candidate**: not frozen, no scientific or experimental validation claimed. Zenodo license metadata should be checked by the author against the mixed licensing.

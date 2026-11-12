# Publication Plan — v0.1.2

## Current status (post-release maintenance on `main`)

- GitHub release: `v0.1.2` (tag `v0.1.2` → commit `fc98ea3d35f99548d882f76e7135398038a0eb11`; the tag is not moved).
- Zenodo version DOI: 10.5281/zenodo.24149914 · concept DOI: 10.5281/zenodo.24149913.
- Zenodo archived the tagged `v0.1.2` snapshot. DOI metadata and documentation corrections were added afterwards on `main`; they do not modify the archived tagged scientific content.
- Nature of the release: a theoretical/computational preprint. No experimental validation of EIT/H-space, new gravity, Yang-Mills, or new physics is claimed; 0.9 and 1.3 remain heuristic operational thresholds.
- Not frozen. AI reviews archived in `review/` are not scientific peer review.

## Pre-release checklist (historical, completed before the v0.1.2 release)

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

## Historical pre-release status (superseded)

On 2026-11-11, before release, the status read "publication candidate — not final, not released", pending a short differential review of v0.1.1 → v0.1.2. This status is superseded: v0.1.2 was subsequently released on GitHub and archived on Zenodo after differential AI review. See the release record below.

- DONE (2026-11-11): `CITATION.cff` `repository-code` set to the author-supplied URL `https://github.com/eit-orbitos/EIT-LJ-Geometry`; `MANIFEST.sha256` regenerated; the former strict-xfail marker on `test_citation_repository_url_completed` removed.

## Release record (2026-11-11 local / 2026-11-12 UTC)

- Differential review v0.1.1 → v0.1.2: PASS for publication candidate (AI review, not peer review; it did not cover binaries, MANIFEST, or the new regression-test contents).
- Repository made public by the author; GitHub release `v0.1.2 — publication candidate` published by the author on tag `v0.1.2` → commit `fc98ea3d35f99548d882f76e7135398038a0eb11`.
- Zenodo archived the tagged release snapshot: version DOI 10.5281/zenodo.24149914; concept DOI 10.5281/zenodo.24149913. Zenodo shows the publication date as 2026-11-12 (UTC); `CITATION.cff` keeps the author-selected `date-released: 2026-11-11`.
- Zenodo record license metadata currently lists CC BY-NC-SA 4.0 only; the code in the archive is under PolyForm Noncommercial 1.0.0 (see `LICENSE_CODE`). The author may add this to the Zenodo record.
- Post-release on `main`: DOI metadata (commit `5b0ede6`), release-notes status (commit `fde1c3e`), and a maintenance pass (status text, bibliography cleanup, dead-code removal, manifest regeneration). None of these change numerical results or the archived tagged content.

# Geometry-Dependent Equilibria in Generalized Lennard-Jones-Type Power-Law Systems

Version **0.1.2** — 11 November 2026 · released on GitHub (tag `v0.1.2`) and archived on Zenodo ([10.5281/zenodo.24149914](https://doi.org/10.5281/zenodo.24149914)). A theoretical/computational preprint; not frozen and not experimentally validated.

This repository is a reproducible theoretical/computational study of constrained radial equilibria for the generalized force

`F(r) = A/r^n - B/r^m`, with `A>0`, `B>0`, `n>m>0`.

For the reference case `A/B=2`, `n=13`, `m=7`, the two-body equilibrium is `R_EQ = 2^(1/6)`.

## Main results

- A geometry factor `G_G(p)` gives the constrained radial equilibrium
  `R_G = [(A/B) G_G(n)/G_G(m)]^(1/(n-m))`.
- Regular simplices cancel the geometry ratio exactly.
- For the reference `(13,7)` pair, regular polygons have a unique minimum at `N=4` **within the computed `N=3..1000` scan**. No global theorem for all `N>=3` is claimed.
- The nearest-neighbor-rescaled large-`N` polygon limit is analytic:
  `R_inf = [2 zeta(12)/zeta(6)]^(1/6) = 1.1192958791...`.
  Valid for `n>m>2` (the zeta asymptotic requires `p>2`; `polygon_limit()` rejects `m<=2`).
  This is a nearest-neighbor-rescaled local infinite-chain limit with curvature-weighted radial projections,
  not a conventional unit-projection chain sum and not a fixed-radius continuum-circle integral.
- For co-spherical configurations under nearest-neighbor normalization:
  `R_ref/rho_max <= R_G <= R_ref`.
  Therefore, for the reference parameters, `1.3` is analytically excluded within this co-spherical nearest-neighbor class only — not for every geometry, normalization, or model choice.
- A deformed cuboid generally has a nonzero tangential force residual. Its reported scalar root is a **constrained radial equilibrium**, not a full vector equilibrium.
- The two cuboid reference-length conventions in v0.1.0 are exactly related by
  `R_fixed = R_nearest * d_fixed/d_nn`; they are different length units, not independent physical predictions.
- `0.9` and `1.3` remain **heuristic operational thresholds**, not derived constants.

## Reproduce everything

```bash
python scripts/build_all.py
pytest -q -p no:cacheprovider
```

`build_all.py` regenerates all committed CSV/JSON outputs and all figures.

## Experiments

1. **Geometry spectrum** — regular polygons `N=3..1000` and five Platonic solids.
2. **Controlled cuboid deformation** — radial root, full-vector residual, and exact normalization-rescaling audit.

## Release structure

- `paper/` — v0.1.2 manuscript PDF and LaTeX source
- `src/` — core mathematics
- `experiments/` — two focused experiment scripts
- `scripts/build_all.py` — full deterministic output/figure builder
- `tests/` — regression suite
- `data/` — regenerated CSV/JSON outputs
- `figures/` — regenerated figures and graphical abstract
- `review/` — independent-review prompts, archived AI review summary, and the archived Kimi v0.1.1 independent review
- `MANIFEST.sha256` — release checksum manifest

## Scope

This is an internal mathematical/computational model. It does **not** experimentally validate EIT/H-space physics, prove a new force law, solve Yang-Mills, or derive the heuristic interval `[0.9,1.3]`.

The earlier exploratory label **P2-SMOOTH a=b=2** belongs to a separate energy-partition sandbox and is **not part of this geometry-equilibrium release**.

## Citation and DOI

- Version DOI (v0.1.2): [10.5281/zenodo.24149914](https://doi.org/10.5281/zenodo.24149914)
- Concept DOI (all versions, resolves to latest): [10.5281/zenodo.24149913](https://doi.org/10.5281/zenodo.24149913)

The Zenodo archive was created from GitHub release tag `v0.1.2` (commit `fc98ea3`). DOI metadata and later documentation/maintenance corrections were added afterwards on `main`; they do not modify the archived tagged scientific content. See `CITATION.cff` and `CHANGELOG.md`.

## Licensing

- Code: **PolyForm Noncommercial 1.0.0**
- Manuscript, figures, and documentation: **CC BY-NC-SA 4.0**

This licensing choice (unchanged since v0.1.1) is deliberately aligned conservatively with the previously reported licensing of the related `eit-orbitos` line. It can be changed only by an explicit later relicensing decision.

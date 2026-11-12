# Reproducibility Protocol — v0.1.2

## Clean rebuild

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/build_all.py
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider
```

The build script regenerates:

- `data/polygon_spectrum_N3_1000.csv`
- `data/platonic_geometry_spectrum.csv`
- `data/cuboid_normalization_sensitivity.csv`
- `data/cuboid_deformation_delta_0p2_5.csv`
- `data/summary_results.json`
- all PNG files under `figures/`

## Core conventions

- Reference pair: `A/B=2`, `n=13`, `m=7`.
- Primary geometry comparison: nearest-neighbor length units.
- The cuboid scalar root is a constrained radial equilibrium; full-vector residuals are checked separately.
- Fixed-edge and nearest-neighbor cuboid coordinates satisfy the exact identity
  `R_fixed = R_nearest * d_fixed / d_nn`.
- The heuristic thresholds `0.9` and `1.3` are never treated as derived outputs.

## Environment

v0.1.2 was built with Python 3.13.5, NumPy 2.2.5, Matplotlib 3.10.8, mpmath 1.3.0, pytest 9.0.2 (pinned in `requirements.txt`). Data products are expected to be byte-identical across environments; PNG files are byte-identical only with the pinned Matplotlib (an independent v0.1.1 review found pixel-identical but not byte-identical PNGs with Matplotlib 3.10.3).

## Precision

The standard release uses NumPy float64. The main results are stable at higher precision. Float32 may obscure the very small large-N rise of the polygon sequence even though the `N=4` minimum remains identifiable.

## Provenance rule

A numerical match to a heuristic threshold is not a derivation unless the criterion is independently motivated before comparison. Version 0.1.1 removes the unsupported historical claim that every scan choice can be proven to have been fixed before all exploratory comparisons.

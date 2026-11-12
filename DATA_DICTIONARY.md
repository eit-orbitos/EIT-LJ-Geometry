# Data Dictionary — v0.1.2

## polygon_spectrum_N3_1000.csv
- `N`: number of polygon vertices
- `G13`, `G7`: radial geometry factors
- `Q`: `G13/G7`
- `R_EQ`: constrained radial equilibrium in nearest-neighbor units

## platonic_geometry_spectrum.csv
- `geometry`, `N_vertices`
- `G13`, `G7`, `Q`, `R_EQ`

## cuboid_deformation_delta_0p2_5.csv
409-row deterministic scan: 401 log-spaced points on `[0.2,5]` plus the anchors `0.25,0.5,0.75,1.25,1.5,2,3,4`.
- `delta`: cuboid z half-axis relative to x/y half-axis=1
- `G13`, `G7`, `Q`, `R_EQ`: nearest-neighbor-unit constrained radial outputs

## cuboid_normalization_sensitivity.csv
601 log-spaced `delta` values.
- `*_nearest`: nearest-neighbor units
- `*_fixed_edge`: fixed reference `d_ref=2`
- `d_nn`: actual nearest-neighbor distance
- `R_fixed_predicted`: `R_nearest * 2/d_nn`
- `identity_abs_error`: numerical error in the exact rescaling identity

## summary_results.json
Machine-readable release summary including:
- polygon minimum
- analytic large-N zeta limit
- cuboid radial minimum
- cuboid tangential residual (with common LJ prefactor 24)
- co-spherical nearest-neighbor bound examples
- threshold provenance

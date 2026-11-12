# External Review Prompts

These prompts are prepared for optional independent review. No review is claimed until an external system actually returns a report.

## Mathematics reviewer prompt
Independently audit the manuscript and code. Re-derive every equilibrium formula from first principles, verify the geometry-factor construction, and search for counterexamples. Do not assume the reported numerical results are correct. Pay special attention to normalization dependence and the claim of simplex cancellation. Classify each result as rigorous, numerical, conjectural, heuristic, or unsupported.

## Computational reviewer prompt
Run the code independently in a clean environment. Reproduce both experiments, compare CSV outputs, verify regression tests, inspect numerical stability for large N, and test alternate sampling densities. Report any discrepancy with exact inputs and outputs.

## Methods/research-integrity reviewer prompt
Audit provenance and claims. Check that derived quantities, trial parameters, and heuristic thresholds are never conflated. Flag any language implying experimental validation or established new physics. Recommend revisions required for a responsible public preprint.

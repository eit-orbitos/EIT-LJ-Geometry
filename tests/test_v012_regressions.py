"""v0.1.2 regression tests for the five required corrections of the v0.1.1 review."""
import csv, sys
from pathlib import Path
import numpy as np
import pytest
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from eit_geometry import *  # noqa: E402,F403


# ---------- Correction 1: zeta domain n>m>2 ----------
@pytest.mark.parametrize("n,m", [(4, 2), (4, 1), (3, 2.0), (13, 0.5), (2.5, 2.0)])
def test_polygon_limit_rejects_m_le_2(n, m):
    with pytest.raises(ValueError):
        polygon_limit(n, m)


@pytest.mark.parametrize("n,m,ab", [(2, 3, 2.0), (7, 7, 2.0), (13, 7, 0.0), (13, 7, -1.0)])
def test_polygon_limit_rejects_invalid_parameters(n, m, ab):
    with pytest.raises(ValueError):
        polygon_limit(n, m, ab)


def test_polygon_limit_reference_high_precision():
    mp.mp.dps = 50
    exact = (2 * mp.zeta(12) / mp.zeta(6)) ** (mp.mpf(1) / 6)
    assert abs(polygon_limit() - float(exact)) < 1e-14
    assert mp.nstr(exact, 16) == '1.119295879072896'


def test_polygon_limit_valid_nonreference_is_real_and_finite():
    v = polygon_limit(5, 3)
    assert isinstance(v, float) and np.isfinite(v)
    mp.mp.dps = 30
    assert abs(v - float((2 * mp.zeta(4) / mp.zeta(2)) ** 0.5)) < 1e-13


# ---------- Correction 2: N=4 minimum is scan-qualified ----------
def test_polygon_scan_unique_minimum_N4_within_3_to_1000():
    rows = list(csv.DictReader(open(ROOT / 'data' / 'polygon_spectrum_N3_1000.csv')))
    N = np.array([int(r['N']) for r in rows]); R = np.array([float(r['R_EQ']) for r in rows])
    assert N[0] == 3 and N[-1] == 1000 and len(N) == 998
    assert N[int(np.argmin(R))] == 4 and np.sum(R == R.min()) == 1
    assert np.all(np.diff(R[N >= 4]) > 0)  # sampled monotone rise only; not a global theorem


def test_wording_scan_qualified_in_manuscript_and_readme():
    tex = (ROOT / 'paper' / 'manuscript.tex').read_text()
    readme = (ROOT / 'README.md').read_text()
    assert 'n>m>2' in tex and 'within the computed' in tex.lower()
    assert 'within the computed `N=3..1000` scan' in readme


# ---------- Correction 3: no build artifacts in the release tree ----------
def test_no_build_artifacts_listed_in_manifest():
    man = (ROOT / 'MANIFEST.sha256').read_text()
    for bad in ('.pytest_cache', '__pycache__', '.pyc'):
        assert bad not in man


# ---------- Correction 4: source_index propagation ----------
def _asymmetric_centered():
    """Centroid-centered, non-vertex-transitive configuration (stretched octahedron)."""
    return np.array([(1.0, 0, 0), (-1.0, 0, 0), (0, 1.7, 0), (0, -1.7, 0), (0, 0, 2.6), (0, 0, -2.6)])


def _cospherical_asymmetric():
    """Centrally symmetric (centroid = sphere center), co-spherical, non-vertex-transitive."""
    u = np.array([[1.0, 0, 0], [0.6, 0.8, 0], [0.1, 0.3, 0.9]])
    u = u / np.linalg.norm(u, axis=1)[:, None]
    return np.vstack([u, -u])


def _move_to_front(V, s):
    idx = [s] + [j for j in range(len(V)) if j != s]
    return V[idx]


def test_geometry_equilibrium_source_index_matches_permutation():
    V = _asymmetric_centered()
    vals = []
    for s in range(len(V)):
        a = geometry_equilibrium(V, source_index=s)
        b = geometry_equilibrium(_move_to_front(V, s))
        assert abs(a['R_EQ'] - b['R_EQ']) < 1e-14 and abs(a['Q'] - b['Q']) < 1e-14
        vals.append(a['R_EQ'])
    assert max(vals) - min(vals) > 1e-3  # sources genuinely differ, so propagation is exercised


@pytest.mark.parametrize("s", range(6))
def test_normalization_identity_nonzero_source(s):
    V = _asymmetric_centered()
    out = normalization_rescale_identity(V, 2.0, source_index=s)
    assert out['abs_error'] < 1e-12
    ref = normalization_rescale_identity(_move_to_front(V, s), 2.0)
    assert abs(out['R_nearest'] - ref['R_nearest']) < 1e-14


@pytest.mark.parametrize("s", range(6))
def test_spherical_bounds_nonzero_source(s):
    V = _cospherical_asymmetric()
    b = spherical_nearest_bounds(V, source_index=s)
    assert b['satisfies']
    assert abs(b['actual'] - geometry_equilibrium(V, source_index=s)['R_EQ']) < 1e-14


def test_source0_reference_outputs_unchanged():
    assert abs(geometry_equilibrium(cube_vertices())['R_EQ'] - 1.1015673696491965) < 1e-15
    assert abs(geometry_equilibrium(regular_polygon_vertices(4))['R_EQ'] - 1.1126198391757889) < 1e-13
    V = cuboid_vertices(0.8513399225207845)
    R = geometry_equilibrium(V)['R_EQ']
    assert abs(R - 1.047252079231908) < 1e-13
    res = vector_force_residual(V, R, common_prefactor=24.0)
    assert abs(res['tangential_norm'] - 9.2437093441292742) < 1e-9


# ---------- Correction 5: release metadata ----------
def test_citation_version_matches():
    cff = (ROOT / 'CITATION.cff').read_text()
    assert 'version: 0.1.2' in cff


def test_citation_repository_url_completed():
    cff = (ROOT / 'CITATION.cff').read_text()
    assert 'REPLACE_WITH_GITHUB_URL' not in cff
    assert 'repository-code: "https://github.com/eit-orbitos/EIT-LJ-Geometry"' in cff

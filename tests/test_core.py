import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from eit_geometry import *


def test_reference_equilibrium():
    assert abs(equilibrium_radius()-2**(1/6)) < 1e-12


def test_triangle_simplex_cancellation():
    out=geometry_equilibrium(regular_polygon_vertices(3))
    assert abs(out['Q']-1) < 1e-12


def test_tetrahedron_simplex_cancellation():
    out=geometry_equilibrium(tetrahedron_vertices())
    assert abs(out['Q']-1) < 1e-12


def test_cube_value():
    out=geometry_equilibrium(cube_vertices())
    assert abs(out['R_EQ']-1.1015673696491965) < 1e-12


def test_heuristic_thresholds_are_declared():
    assert HEURISTIC_R_LOW == 0.9 and HEURISTIC_R_HIGH == 1.3


def test_polygon_closed_limit():
    assert abs(polygon_limit()-1.1192958790728956) < 5e-12


def test_normalization_rescaling_identity():
    for d in (0.25,0.5,0.807,1.0,2.0,4.0):
        out=normalization_rescale_identity(cuboid_vertices(d),2.0)
        assert out['abs_error'] < 1e-12


def test_cuboid_radial_not_vector_equilibrium():
    d=0.8513399225207845
    V=cuboid_vertices(d)
    R=geometry_equilibrium(V)['R_EQ']
    res=vector_force_residual(V,R,common_prefactor=24.0)
    assert abs(res['radial_component']) < 1e-10
    assert 9.0 < res['tangential_norm'] < 9.5


def test_spherical_bound_cube_and_cuboid():
    for V in (cube_vertices(),cuboid_vertices(0.8513399225207845),dodecahedron_vertices()):
        b=spherical_nearest_bounds(V)
        assert b['satisfies']
        assert b['actual'] <= b['upper'] + 1e-12

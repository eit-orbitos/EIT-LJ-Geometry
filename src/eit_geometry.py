"""Core mathematics for geometry-dependent generalized Lennard-Jones-type equilibria.

Research status: theoretical/computational sandbox. No claim of experimental validation.
Version: 0.1.2
"""
from __future__ import annotations
import math
from typing import Sequence
import numpy as np

DEFAULT_N = 13.0
DEFAULT_M = 7.0
DEFAULT_A_OVER_B = 2.0
R_EQ_REFERENCE = DEFAULT_A_OVER_B ** (1.0/(DEFAULT_N-DEFAULT_M))
HEURISTIC_R_LOW = 0.9
HEURISTIC_R_HIGH = 1.3


def equilibrium_radius(A_over_B: float = DEFAULT_A_OVER_B, n: float = DEFAULT_N, m: float = DEFAULT_M) -> float:
    if not (A_over_B > 0 and n > m > 0):
        raise ValueError("Require A/B>0 and n>m>0")
    return A_over_B ** (1.0/(n-m))


def lj_potential(r: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
    if r <= 0:
        raise ValueError("r must be > 0")
    s6=(sigma/r)**6
    return 4*epsilon*(s6*s6-s6)


def lj_force(r: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
    if r <= 0:
        raise ValueError("r must be > 0")
    return 24*epsilon*(2*sigma**12*r**-13 - sigma**6*r**-7)


def lj_curvature(r: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
    if r <= 0:
        raise ValueError("r must be > 0")
    return 24*epsilon*(-7*sigma**6*r**-8 + 26*sigma**12*r**-14)


def _reference_distance(V: np.ndarray, source_index: int, normalization: str,
                        reference_distance: float | None) -> float:
    src=V[source_index]
    ds=[np.linalg.norm(V[j]-src) for j in range(len(V)) if j != source_index]
    if normalization == "nearest":
        return float(min(ds))
    if normalization == "fixed":
        if reference_distance is None or reference_distance <= 0:
            raise ValueError("fixed normalization requires positive reference_distance")
        return float(reference_distance)
    raise ValueError("normalization must be 'nearest' or 'fixed'")


def geometry_factor(vertices: Sequence[Sequence[float]], p: float, source_index: int = 0,
                    normalization: str = "nearest", reference_distance: float | None = None) -> float:
    """Radial projection factor.

    normalization='nearest' uses the nearest-neighbor distance as d_ref.
    normalization='fixed' uses reference_distance.

    The value depends on the chosen length unit through d_ref. Equilibrium radii
    computed with different d_ref conventions transform by the same length-unit
    rescaling; see normalization_rescale_identity().
    """
    if p <= 0:
        raise ValueError("p must be > 0")
    V=np.asarray(vertices,dtype=float)
    if V.ndim != 2 or len(V) < 2:
        raise ValueError("Need NxD vertex array")
    src=V[source_index]
    centroid=V.mean(axis=0)
    inward=centroid-src
    ni=np.linalg.norm(inward)
    if ni == 0:
        raise ValueError("source vertex cannot coincide with centroid")
    inward=inward/ni
    dref=_reference_distance(V,source_index,normalization,reference_distance)
    total=0.0
    for j in range(len(V)):
        if j == source_index:
            continue
        dv=V[j]-src
        dist=np.linalg.norm(dv)
        direction=dv/dist
        projection=float(np.dot(direction,inward))
        total += projection / ((dist/dref)**p)
    return total


def geometry_equilibrium(vertices: Sequence[Sequence[float]], n: float = DEFAULT_N, m: float = DEFAULT_M,
                         A_over_B: float = DEFAULT_A_OVER_B, normalization: str = "nearest",
                         reference_distance: float | None = None,
                         source_index: int = 0) -> dict:
    """Constrained radial equilibrium for the declared geometry.

    source_index selects the source vertex (default 0; v0.1.2 adds explicit
    propagation to both geometry_factor calls).

    This zeros only the inward radial component of the net pair-force sum. For
    deformed, non-radially-symmetric shapes (e.g. a cuboid with delta != 1),
    tangential components can remain nonzero, so this is not necessarily a full
    vector-force equilibrium.
    """
    gn=geometry_factor(vertices,n,source_index=source_index,normalization=normalization,reference_distance=reference_distance)
    gm=geometry_factor(vertices,m,source_index=source_index,normalization=normalization,reference_distance=reference_distance)
    if gn <= 0 or gm <= 0:
        raise ValueError("Geometry factors must be positive")
    q=gn/gm
    req=(A_over_B*q)**(1.0/(n-m))
    return {"G_n":gn,"G_m":gm,"Q":q,"R_EQ":req}


def normalization_rescale_identity(vertices: Sequence[Sequence[float]], fixed_reference: float,
                                   n: float = DEFAULT_N, m: float = DEFAULT_M,
                                   A_over_B: float = DEFAULT_A_OVER_B,
                                   source_index: int = 0) -> dict:
    """Verify exact change-of-length-unit identity between two d_ref choices.

    For the same geometry, if R_near uses d_nn and R_fixed uses d_fixed, then
        R_fixed = R_near * d_fixed / d_nn.
    Thus the two values are coordinate representations in different reference
    length units, not independent physical predictions.
    """
    V=np.asarray(vertices,dtype=float)
    src=V[source_index]
    dnn=min(np.linalg.norm(V[j]-src) for j in range(len(V)) if j != source_index)
    near=geometry_equilibrium(V,n,m,A_over_B,"nearest",source_index=source_index)['R_EQ']
    fixed=geometry_equilibrium(V,n,m,A_over_B,"fixed",fixed_reference,source_index=source_index)['R_EQ']
    predicted=near*fixed_reference/dnn
    return {"d_nn":float(dnn),"R_nearest":near,"R_fixed":fixed,
            "R_fixed_predicted":predicted,"abs_error":abs(fixed-predicted)}


def vector_force_residual(vertices: Sequence[Sequence[float]], R: float,
                          A_over_B: float = DEFAULT_A_OVER_B,
                          n: float = DEFAULT_N, m: float = DEFAULT_M,
                          source_index: int = 0, normalization: str = "nearest",
                          reference_distance: float | None = None,
                          common_prefactor: float = 1.0) -> dict:
    """Full vector-force residual at a declared radial equilibrium.

    Pair magnitudes are common_prefactor * [A/r^n - B/r^m], with B=1 and
    A=A_over_B, and pair separations r = R * rho_ij. A common prefactor does not
    change the radial equilibrium; common_prefactor=24 matches normalized LJ
    force scaling for the (13,7) reference pair.
    """
    if R <= 0 or common_prefactor <= 0:
        raise ValueError("R and common_prefactor must be positive")
    V=np.asarray(vertices,dtype=float)
    src=V[source_index]
    centroid=V.mean(axis=0)
    inward=centroid-src
    inward=inward/np.linalg.norm(inward)
    dref=_reference_distance(V,source_index,normalization,reference_distance)
    net=np.zeros(V.shape[1],dtype=float)
    for j in range(len(V)):
        if j == source_index:
            continue
        dv=V[j]-src
        dist=np.linalg.norm(dv)
        u=dv/dist
        rho=dist/dref
        mag=common_prefactor*(A_over_B/(R*rho)**n - 1.0/(R*rho)**m)
        net += mag*u
    radial=float(np.dot(net,inward))
    tangential=net-radial*inward
    return {"net_vector":net,"net_norm":float(np.linalg.norm(net)),
            "radial_component":radial,"tangential_norm":float(np.linalg.norm(tangential))}


def regular_polygon_vertices(N: int, radius: float = 1.0) -> np.ndarray:
    if N < 3:
        raise ValueError("N >= 3")
    return np.array([(radius*math.cos(2*math.pi*k/N),radius*math.sin(2*math.pi*k/N),0.0) for k in range(N)])


def polygon_limit(n: float = DEFAULT_N, m: float = DEFAULT_M,
                  A_over_B: float = DEFAULT_A_OVER_B) -> float:
    """Large-N regular-polygon limit under nearest-neighbor normalization.

    Valid domain: A/B > 0 and n > m > 2. For p > 2 the fixed-k end sums
    converge and G_N(p) ~ 2*pi/N * zeta(p-1), so
      R_inf = [(A/B) zeta(n-1)/zeta(m-1)]^(1/(n-m)).
    For p <= 2 this endpoint-dominated asymptotic does not hold (zeta(1)
    diverges at p = 2), so m <= 2 raises ValueError instead of returning a
    truncated-harmonic or complex value.

    Interpretation: nearest-neighbor-rescaled local infinite-chain limit with
    curvature-weighted radial projections (each fixed-k projection vanishes as
    pi*k/N). It is neither the conventional unit-projection chain sum (which
    would give 2*zeta(p)) nor a finite-radius continuum-circle force integral.
    """
    if not (A_over_B > 0 and n > m > 2):
        raise ValueError("polygon_limit requires A/B>0 and n>m>2 "
                         "(zeta asymptotic G_N(p) ~ 2*pi*zeta(p-1)/N needs p>2)")
    try:
        import mpmath as mp
        zeta_n=float(mp.zeta(n-1))
        zeta_m=float(mp.zeta(m-1))
    except Exception:
        # For the reference integer exponents, use rapidly convergent sums.
        def zeta(s: float) -> float:
            return sum(k**(-s) for k in range(1,1_000_000))
        zeta_n=zeta(n-1); zeta_m=zeta(m-1)
    return (A_over_B*zeta_n/zeta_m)**(1.0/(n-m))


def spherical_nearest_bounds(vertices: Sequence[Sequence[float]],
                             n: float = DEFAULT_N, m: float = DEFAULT_M,
                             A_over_B: float = DEFAULT_A_OVER_B,
                             source_index: int = 0, tol: float = 1e-10) -> dict:
    """Bounds for co-spherical configurations with nearest-neighbor normalization.

    If all vertices lie on one sphere centered at the centroid and radial
    projections are nonnegative, rho_j in [1,rho_max] implies
      rho_max^(-(n-m)) <= G(n)/G(m) <= 1,
    hence
      R_ref/rho_max <= R_G <= R_ref.
    """
    if not n > m > 0:
        raise ValueError("Require n>m>0")
    V=np.asarray(vertices,dtype=float)
    centroid=V.mean(axis=0)
    radii=np.linalg.norm(V-centroid,axis=1)
    if np.max(np.abs(radii-radii[0])) > tol*max(1.0,float(radii[0])):
        raise ValueError("configuration is not co-spherical about its centroid")
    src=V[source_index]
    inward=(centroid-src)/np.linalg.norm(centroid-src)
    ds=[]; projections=[]
    for j in range(len(V)):
        if j==source_index:
            continue
        dv=V[j]-src; dist=np.linalg.norm(dv)
        ds.append(dist); projections.append(float(np.dot(dv/dist,inward)))
    if min(projections) < -tol:
        raise ValueError("negative radial projection violates bound assumptions")
    dnn=min(ds); rho_max=max(ds)/dnn
    ref=equilibrium_radius(A_over_B,n,m)
    lower=ref/rho_max; upper=ref
    actual=geometry_equilibrium(V,n,m,A_over_B,"nearest",source_index=source_index)['R_EQ']
    return {"rho_max":float(rho_max),"lower":lower,"actual":actual,"upper":upper,
            "satisfies":bool(lower-tol <= actual <= upper+tol)}


def cuboid_vertices(delta: float, xy_half: float = 1.0) -> np.ndarray:
    if delta <= 0 or xy_half <= 0:
        raise ValueError("positive dimensions required")
    return np.array([(x,y,z) for x in (-xy_half,xy_half) for y in (-xy_half,xy_half) for z in (-delta,delta)],dtype=float)


def tetrahedron_vertices() -> np.ndarray:
    return np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)],dtype=float)


def cube_vertices() -> np.ndarray:
    return cuboid_vertices(1.0)


def octahedron_vertices() -> np.ndarray:
    return np.array([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)],dtype=float)


def icosahedron_vertices() -> np.ndarray:
    phi=(1+math.sqrt(5))/2
    pts=[]
    for a in (-1.0,1.0):
        for b in (-phi,phi):
            pts.extend([(0,a,b),(a,b,0),(b,0,a)])
    return np.unique(np.round(np.array(pts),12),axis=0)


def dodecahedron_vertices() -> np.ndarray:
    phi=(1+math.sqrt(5))/2; inv=1/phi
    pts=[]
    for x in (-1.,1.):
        for y in (-1.,1.):
            for z in (-1.,1.):
                pts.append((x,y,z))
    for a,b,c in [(0,inv,phi),(inv,phi,0),(phi,0,inv)]:
        for sa in (-1.,1.):
            for sb in (-1.,1.):
                for sc in (-1.,1.):
                    pts.append((sa*a,sb*b,sc*c))
    return np.unique(np.round(np.array(pts),12),axis=0)


def heuristic_state(R: float) -> str:
    if R < HEURISTIC_R_LOW:
        return "FREEZE"
    if R <= HEURISTIC_R_HIGH:
        return "ACTIVE"
    return "RELEASE"

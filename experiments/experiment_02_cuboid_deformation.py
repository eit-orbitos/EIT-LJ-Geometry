"""Experiment 2: constrained radial cuboid equilibrium and normalization identity.
For the complete release build, run scripts/build_all.py.
"""
from pathlib import Path
import csv, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from eit_geometry import *
deltas=np.geomspace(0.2,5.0,601); rows=[]
for d in deltas:
    V=cuboid_vertices(float(d))
    near=geometry_equilibrium(V,normalization='nearest')
    fixed=geometry_equilibrium(V,normalization='fixed',reference_distance=2.0)
    ident=normalization_rescale_identity(V,2.0)
    rows.append([d,near['G_n'],near['G_m'],near['Q'],near['R_EQ'],fixed['G_n'],fixed['G_m'],fixed['Q'],fixed['R_EQ'],ident['d_nn'],ident['R_fixed_predicted'],ident['abs_error']])
with open(ROOT/'data/cuboid_normalization_sensitivity.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['delta','G13_nearest','G7_nearest','Q_nearest','R_EQ_nearest','G13_fixed_edge','G7_fixed_edge','Q_fixed_edge','R_EQ_fixed_edge','d_nn','R_fixed_predicted','identity_abs_error']); w.writerows(rows)
a=np.asarray(rows,float); imin=np.argmin(a[:,4]); d=float(a[imin,0]); R=float(a[imin,4])
res=vector_force_residual(cuboid_vertices(d),R,common_prefactor=24.0)
print('nearest-unit radial minimum:',d,R)
print('normalization identity max error:',max(r[-1] for r in rows))
print('full-vector tangential residual (LJ prefactor 24):',res['tangential_norm'])

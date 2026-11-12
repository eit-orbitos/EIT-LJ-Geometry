"""Experiment 1: regenerate polygon and Platonic-solid data.
For the complete release build (data + figures + summary), run scripts/build_all.py.
"""
from pathlib import Path
import csv, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from eit_geometry import *
rows=[]
for N in range(3,1001):
    out=geometry_equilibrium(regular_polygon_vertices(N))
    rows.append((N,out['G_n'],out['G_m'],out['Q'],out['R_EQ']))
with open(ROOT/'data/polygon_spectrum_N3_1000.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['N','G13','G7','Q','R_EQ']); w.writerows(rows)
geometries={'tetrahedron':tetrahedron_vertices(),'cube':cube_vertices(),'octahedron':octahedron_vertices(),'icosahedron':icosahedron_vertices(),'dodecahedron':dodecahedron_vertices()}
with open(ROOT/'data/platonic_geometry_spectrum.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['geometry','N_vertices','G13','G7','Q','R_EQ'])
    for name,V in geometries.items():
        o=geometry_equilibrium(V); w.writerow([name,len(V),o['G_n'],o['G_m'],o['Q'],o['R_EQ']])
a=np.asarray(rows,float); i=np.argmin(a[:,4])
print('polygon minimum:',int(a[i,0]),a[i,4])
print('N=1000:',a[-1,4])
print('closed large-N limit:',polygon_limit())

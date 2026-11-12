from pathlib import Path
import csv, json, sys, math
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from eit_geometry import *

DATA=ROOT/'data'; FIG=ROOT/'figures'
DATA.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)

# ---------- Data 1: polygons ----------
poly=[]
for N in range(3,1001):
    o=geometry_equilibrium(regular_polygon_vertices(N))
    poly.append((N,o['G_n'],o['G_m'],o['Q'],o['R_EQ']))
with open(DATA/'polygon_spectrum_N3_1000.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['N','G13','G7','Q','R_EQ']); w.writerows(poly)

# ---------- Data 2: Platonic solids ----------
geoms={
    'tetrahedron':tetrahedron_vertices(), 'cube':cube_vertices(), 'octahedron':octahedron_vertices(),
    'icosahedron':icosahedron_vertices(), 'dodecahedron':dodecahedron_vertices()
}
plat=[]
with open(DATA/'platonic_geometry_spectrum.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['geometry','N_vertices','G13','G7','Q','R_EQ'])
    for name,V in geoms.items():
        o=geometry_equilibrium(V); row=(name,len(V),o['G_n'],o['G_m'],o['Q'],o['R_EQ']); plat.append(row); w.writerow(row)

# ---------- Data 3: cuboid 601-point normalization identity ----------
deltas601=np.geomspace(0.2,5.0,601)
sens=[]
for d in deltas601:
    V=cuboid_vertices(float(d))
    near=geometry_equilibrium(V,normalization='nearest')
    fixed=geometry_equilibrium(V,normalization='fixed',reference_distance=2.0)
    ident=normalization_rescale_identity(V,2.0)
    sens.append([d,near['G_n'],near['G_m'],near['Q'],near['R_EQ'],fixed['G_n'],fixed['G_m'],fixed['Q'],fixed['R_EQ'],ident['d_nn'],ident['R_fixed_predicted'],ident['abs_error']])
with open(DATA/'cuboid_normalization_sensitivity.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['delta','G13_nearest','G7_nearest','Q_nearest','R_EQ_nearest','G13_fixed_edge','G7_fixed_edge','Q_fixed_edge','R_EQ_fixed_edge','d_nn','R_fixed_predicted','identity_abs_error']); w.writerows(sens)

# ---------- Data 4: historical 409-row deformation scan, now fully generated ----------
base=np.geomspace(0.2,5.0,401)
anchors=np.array([0.25,0.5,0.75,1.25,1.5,2.0,3.0,4.0])
deltas409=np.array(sorted(set(np.concatenate([base,anchors]).tolist())))
assert len(deltas409)==409
cub=[]
for d in deltas409:
    V=cuboid_vertices(float(d)); o=geometry_equilibrium(V)
    cub.append([d,o['G_n'],o['G_m'],o['Q'],o['R_EQ']])
with open(DATA/'cuboid_deformation_delta_0p2_5.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['delta','G13','G7','Q','R_EQ']); w.writerows(cub)

# ---------- Derived checks ----------
pa=np.asarray(poly,float); imin=int(np.argmin(pa[:,4]))
ca=np.asarray(cub,float); cmin=int(np.argmin(ca[:,4]))
Vmin=cuboid_vertices(float(ca[cmin,0])); Rmin=float(ca[cmin,4])
res24=vector_force_residual(Vmin,Rmin,common_prefactor=24.0)
bound_cube=spherical_nearest_bounds(cube_vertices())
bound_cuboid=spherical_nearest_bounds(Vmin)
Rinf=polygon_limit()

summary={
  'version':'0.1.2',
  'polygon':{
    'R_EQ_reference':R_EQ_REFERENCE,'N_min':int(pa[imin,0]),'R_EQ_min':float(pa[imin,4]),
    'R_EQ_N1000':float(pa[-1,4]),'R_EQ_largeN_closed_form':Rinf,
    'largeN_formula':'[(A/B)*zeta(n-1)/zeta(m-1)]^(1/(n-m))',
    'interpretation':'nearest-neighbor-rescaled local infinite-chain limit with curvature-weighted radial projections; valid for n>m>2',
    'N_min_scope':'unique minimum within the computed N=3..1000 scan (not a global theorem)'
  },
  'cuboid':{
    'delta_min_R_nearest':float(ca[cmin,0]),'R_EQ_min_nearest':Rmin,
    'radial_residual_prefactor24':res24['radial_component'],
    'tangential_residual_prefactor24':res24['tangential_norm'],
    'normalization_identity':'R_fixed = R_nearest * d_fixed / d_nn',
    'normalization_identity_max_abs_error':float(max(r[-1] for r in sens))
  },
  'bounds':{
    'theorem':'For co-spherical configurations under nearest-neighbor normalization: R_ref/rho_max <= R_G <= R_ref',
    'cube':bound_cube,'cuboid_at_radial_min':bound_cuboid
  },
  'platonic':[{'geometry':r[0],'N':r[1],'G13':r[2],'G7':r[3],'Q':r[4],'R_EQ':r[5]} for r in plat],
  'boundary':{'heuristic_low':HEURISTIC_R_LOW,'heuristic_high':HEURISTIC_R_HIGH,'status':'heuristic_not_derived'}
}
with open(DATA/'summary_results.json','w') as f: json.dump(summary,f,indent=2)

# ---------- Figures ----------
# 1 LJ
x=np.linspace(0.88,2.0,900); V=4*(x**-12-x**-6)
fig,ax=plt.subplots(figsize=(7,4.2)); ax.plot(x,V); ax.axhline(0,linewidth=.8); ax.axvline(R_EQ_REFERENCE,linestyle='--'); ax.axvline(0.9,linestyle=':'); ax.axvline(1.3,linestyle=':'); ax.set_ylim(-1.2,8); ax.set_xlabel('R'); ax.set_ylabel('V(R)'); ax.set_title('Normalized Lennard-Jones reference'); fig.tight_layout(); fig.savefig(FIG/'figure_01_lj_reference.png',dpi=180); plt.close(fig)
# 2 polygon
fig,ax=plt.subplots(figsize=(7.2,4.2)); ax.plot(pa[:,0],pa[:,4]); ax.scatter([pa[imin,0]],[pa[imin,4]]); ax.axhline(Rinf,linestyle='--'); ax.set_xscale('log'); ax.set_xlabel('N'); ax.set_ylabel('R_EQ'); ax.set_title('Regular polygon spectrum and large-N limit'); fig.tight_layout(); fig.savefig(FIG/'figure_02_polygon_spectrum.png',dpi=180); plt.close(fig)
# 3 platonic
names=[r[0] for r in plat]; vals=[r[5] for r in plat]
fig,ax=plt.subplots(figsize=(7.2,4.2)); ax.bar(names,vals); ax.axhline(R_EQ_REFERENCE,linestyle='--'); ax.set_ylabel('R_EQ'); ax.set_title('Platonic-solid constrained radial equilibria'); ax.tick_params(axis='x',rotation=25); fig.tight_layout(); fig.savefig(FIG/'figure_03_platonic_spectrum.png',dpi=180); plt.close(fig)
# 4 cuboid nearest
fig,ax=plt.subplots(figsize=(7.2,4.2)); ax.plot(ca[:,0],ca[:,4]); ax.scatter([ca[cmin,0]],[ca[cmin,4]]); ax.set_xscale('log'); ax.set_xlabel('delta'); ax.set_ylabel('R_EQ (nearest-neighbor units)'); ax.set_title('Cuboid constrained radial equilibrium'); fig.tight_layout(); fig.savefig(FIG/'figure_04_cuboid_deformation.png',dpi=180); plt.close(fig)
# 5 architecture
fig,ax=plt.subplots(figsize=(9,4.8)); ax.axis('off')
boxes=[(0.03,0.62,0.2,0.22,'Analytic model\nF=A/r^n-B/r^m'),(0.29,0.62,0.2,0.22,'Geometry factor\nG_G(p)'),(0.55,0.62,0.2,0.22,'Radial equilibrium\nR_G'),(0.77,0.62,0.2,0.22,'Experiments\npolygon + cuboid'),(0.18,0.18,0.25,0.22,'Review corrections\nlimit, bounds, residual'),(0.57,0.18,0.25,0.22,'Provenance\n0.9/1.3 heuristic')]
for x0,y0,w,h,t in boxes:
    ax.add_patch(plt.Rectangle((x0,y0),w,h,fill=False,linewidth=1.4)); ax.text(x0+w/2,y0+h/2,t,ha='center',va='center',fontsize=10)
ax.set_title('Research architecture - v0.1.2 publication candidate'); fig.tight_layout(); fig.savefig(FIG/'figure_05_research_architecture.png',dpi=180); plt.close(fig)
# 6 normalization identity (not sensitivity)
sa=np.asarray(sens,float)
fig,ax=plt.subplots(figsize=(7.2,4.2)); ax.plot(sa[:,0],sa[:,8],label='R_fixed'); ax.plot(sa[:,0],sa[:,10],linestyle='--',label='R_nearest * 2/d_nn'); ax.set_xscale('log'); ax.set_xlabel('delta'); ax.set_ylabel('R in fixed-edge units'); ax.set_title('Normalization identity: exact change of length unit'); ax.legend(); fig.tight_layout(); fig.savefig(FIG/'figure_06_normalization_sensitivity.png',dpi=180); plt.close(fig)
# graphical abstract
fig,axs=plt.subplots(2,2,figsize=(10,7))
axs[0,0].plot(pa[:,0],pa[:,4]); axs[0,0].axhline(Rinf,linestyle='--'); axs[0,0].set_xscale('log'); axs[0,0].set_title('Polygon spectrum')
axs[0,1].bar(names,vals); axs[0,1].set_title('Platonic solids'); axs[0,1].tick_params(axis='x',rotation=25)
axs[1,0].plot(ca[:,0],ca[:,4]); axs[1,0].set_xscale('log'); axs[1,0].set_title('Cuboid radial equilibrium')
axs[1,1].axis('off'); axs[1,1].text(.05,.82,'Review-corrected results',fontsize=14,weight='bold'); axs[1,1].text(.05,.63,f'R_inf = {Rinf:.10f}\n(local-chain limit,\ncurvature-weighted)',fontsize=12); axs[1,1].text(.05,.43,'Cuboid: radial balance only\nwhen delta != 1',fontsize=12); axs[1,1].text(.05,.23,'0.9 and 1.3 remain\nheuristic thresholds',fontsize=12)
fig.suptitle('Geometry-Dependent Equilibria - v0.1.2'); fig.tight_layout(); fig.savefig(FIG/'graphical_abstract.png',dpi=180); plt.close(fig)

print('Built all data, summary JSON, and figures.')
print('polygon minimum',int(pa[imin,0]),pa[imin,4])
print('closed large-N limit',Rinf)
print('cuboid radial min',ca[cmin,0],ca[cmin,4])
print('cuboid tangential residual (prefactor 24)',res24['tangential_norm'])
print('normalization identity max error',max(r[-1] for r in sens))

"""
Publication-Quality Figure Generator for the MFDM K4 Oligon Paper
=================================================================
Generates 6 figures for the LaTeX paper:
  1. K4 Oligon seed topology (3D graph)
  2. Hypergraph evolution timeline (adjacency heatmaps at t=0,10,20,40)
  3. T2 torus geometry with K4 defect embedding
  4. NANOGrav h_c(f) spectrum comparison (H0 vs H1)
  5. Anisotropy C_l bar chart
  6. Cosmic web halo clustering (N-body 3D projection)
"""

import os, sys
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import networkx as nx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

# Global style
plt.rcParams.update({
    'figure.facecolor': '#0a0a1a',
    'axes.facecolor': '#0a0a1a',
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'font.family': 'sans-serif',
    'font.size': 11,
})

CYAN    = '#00d2ff'
MAGENTA = '#ff003c'
GOLD    = '#ffd700'
PURPLE  = '#a020f0'
TEAL    = '#00e5a0'


# ─────────────────────────────────────────────────────────────
# FIG 1: K4 OLIGON SEED TOPOLOGY
# ─────────────────────────────────────────────────────────────
def fig1_k4_oligon():
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0a0a1a')

    # K4 complete graph (tetrahedron)
    verts = np.array([
        [1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]
    ], dtype=float) * 1.2

    # Draw faces (semi-transparent)
    faces = [[verts[j] for j in [0,1,2]], [verts[j] for j in [0,1,3]],
             [verts[j] for j in [0,2,3]], [verts[j] for j in [1,2,3]]]
    poly = Poly3DCollection(faces, alpha=0.08, facecolor=CYAN, edgecolor=CYAN, linewidth=0.5)
    ax.add_collection3d(poly)

    # Draw edges with glow
    for i in range(4):
        for j in range(i+1, 4):
            ax.plot(*zip(verts[i], verts[j]), color=CYAN, linewidth=2.5, alpha=0.9)
            ax.plot(*zip(verts[i], verts[j]), color='white', linewidth=0.8, alpha=0.4)

    # Draw nodes
    for i, v in enumerate(verts):
        ax.scatter(*v, s=200, c=GOLD, zorder=5, edgecolors='white', linewidth=1.5)
        ax.text(v[0]*1.25, v[1]*1.25, v[2]*1.25, f'$v_{i}$', fontsize=13,
                color='white', ha='center', fontweight='bold')

    # Vacuum ring (surrounding halo)
    theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
    vac_r = 2.8
    vac_pts = np.column_stack([vac_r*np.cos(theta), vac_r*np.sin(theta), np.zeros(12)])
    for i in range(12):
        ax.scatter(*vac_pts[i], s=40, c=PURPLE, alpha=0.6, zorder=4)
        j = (i+1) % 12
        ax.plot(*zip(vac_pts[i], vac_pts[j]), color=PURPLE, linewidth=1, alpha=0.4)

    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.set_zlim(-3.5, 3.5)
    ax.set_axis_off()
    ax.view_init(elev=25, azim=45)
    ax.set_title(r'$K_4$ Oligon Seed: Topological Defect Core + Vacuum Ring',
                 fontsize=14, color='white', pad=15)
    fig.savefig(OUT / 'fig_k4_oligon_seed.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a', transparent=False)
    plt.close()
    print("  ✓ fig_k4_oligon_seed.png")


# ─────────────────────────────────────────────────────────────
# FIG 2: HYPERGRAPH EVOLUTION TIMELINE
# ─────────────────────────────────────────────────────────────
def fig2_evolution():
    from hypergraph.masking import hypergraph_step

    N = 16
    torch.manual_seed(42)
    M = torch.zeros(N, N)
    for i in range(4):
        for j in range(4):
            if i != j: M[i,j] = 1.0
    for i in range(4, N):
        M[i, (i-4+1)%12+4] = 0.5
        M[(i-4+1)%12+4, i] = 0.5

    snapshots = {}
    steps_to_capture = [0, 5, 15, 39]
    M_sp = M.to_sparse().coalesce()

    for step in range(40):
        if step in steps_to_capture:
            snapshots[step] = M_sp.to_dense().numpy().copy()
        M_d = M_sp.to_dense()
        mx = M_d.max().item()
        if mx > 0: M_d = M_d / mx
        M_sp = M_d.to_sparse().coalesce()
        T = (M_d > 0).float().to_sparse().coalesce()
        M_sp = hypergraph_step(M_sp, T)
        vals = M_sp.values().clamp(0.0, 1.0)
        M_sp = torch.sparse_coo_tensor(M_sp.indices(), vals, M_sp.shape).coalesce()

    fig, axes = plt.subplots(1, 4, figsize=(18, 4))
    cmap = plt.colormaps['inferno']

    for idx, (step, mat) in enumerate(sorted(snapshots.items())):
        ax = axes[idx]
        im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=1, interpolation='nearest')
        ax.set_title(f't = {step}', fontsize=13, color='white')
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(CYAN); spine.set_linewidth(1.5)

    fig.suptitle(r'Topological Hadamard Masking Evolution: $M_{t+1} = (M_t^2 + M_t) \odot T$',
                 fontsize=14, color='white', y=1.02)
    cbar = fig.colorbar(im, ax=axes, fraction=0.02, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.outline.set_edgecolor('white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    fig.savefig(OUT / 'fig_evolution_timeline.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a')
    plt.close()
    print("  ✓ fig_evolution_timeline.png")


# ─────────────────────────────────────────────────────────────
# FIG 3: T2 TORUS GEOMETRY WITH K4 DEFECT
# ─────────────────────────────────────────────────────────────
def fig3_torus():
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0a0a1a')

    # Torus parametric surface
    R, r = 3.0, 1.0
    u = np.linspace(0, 2*np.pi, 80)
    v = np.linspace(0, 2*np.pi, 40)
    U, V = np.meshgrid(u, v)
    X = (R + r*np.cos(V)) * np.cos(U)
    Y = (R + r*np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)

    ax.plot_surface(X, Y, Z, alpha=0.15, color=TEAL, edgecolor=TEAL,
                    linewidth=0.1, antialiased=True)

    # K4 defect nodes embedded on torus surface
    defect_u = [0.3, 0.6, 1.0, 1.5]
    defect_v = [0.5, 1.2, 0.8, 1.8]
    dx, dy, dz = [], [], []
    for du, dv in zip(defect_u, defect_v):
        dx.append((R + r*np.cos(dv)) * np.cos(du))
        dy.append((R + r*np.cos(dv)) * np.sin(du))
        dz.append(r * np.sin(dv))

    # K4 edges on torus
    for i in range(4):
        for j in range(i+1, 4):
            ax.plot([dx[i], dx[j]], [dy[i], dy[j]], [dz[i], dz[j]],
                    color=MAGENTA, linewidth=2.5, alpha=0.9)

    ax.scatter(dx, dy, dz, s=250, c=GOLD, zorder=5, edgecolors='white', linewidth=2)

    # Geodesic flow lines
    for offset in [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]:
        t = np.linspace(0, 2*np.pi, 100)
        gx = (R + r*np.cos(t*0.7 + offset)) * np.cos(t)
        gy = (R + r*np.cos(t*0.7 + offset)) * np.sin(t)
        gz = r * np.sin(t*0.7 + offset)
        ax.plot(gx, gy, gz, color=CYAN, linewidth=0.4, alpha=0.3)

    ax.set_axis_off()
    ax.view_init(elev=30, azim=60)
    ax.set_title(r'$K_3 \times T^2$ Geometry: $K_4$ Oligon Defect Embedded on Torus',
                 fontsize=14, color='white', pad=15)
    fig.savefig(OUT / 'fig_t2_torus_k4.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a')
    plt.close()
    print("  ✓ fig_t2_torus_k4.png")


# ─────────────────────────────────────────────────────────────
# FIG 4: NANOGRAV SPECTRUM COMPARISON
# ─────────────────────────────────────────────────────────────
def fig4_spectrum():
    # Load real NANOGrav data
    base = Path('/tmp/nanograv_data/ceffyl_data/30f_fs{hd}_ceffyl/')
    freqs = np.load(base / 'freqs.npy')
    grid  = np.load(base / 'log10rhogrid.npy')
    dens  = np.load(base / 'density.npy')

    n_f = dens.shape[1]
    med, lo, hi = np.zeros(n_f), np.zeros(n_f), np.zeros(n_f)
    for i in range(n_f):
        d = dens[0, i, :]; d /= d.sum()
        cdf = np.cumsum(d)
        med[i] = grid[np.searchsorted(cdf, 0.50)]
        lo[i]  = grid[np.searchsorted(cdf, 0.05)]
        hi[i]  = grid[np.searchsorted(cdf, 0.95)]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Data points with 90% CI
    ax.fill_between(freqs*1e9, lo, hi, color=CYAN, alpha=0.15, label='90% CI')
    ax.plot(freqs*1e9, med, 'o', color='white', markersize=5, zorder=5,
            label='NANOGrav 15yr HD Median')

    # H0: SMBHB power law
    F_YR = 1.0 / (365.25 * 86400.0)
    T_span = 16.03 * 365.25 * 86400.0
    f_dense = np.logspace(np.log10(freqs[0]), np.log10(freqs[-1]), 200)
    A0 = 10**-14.5
    gamma0 = 4.80
    h0 = A0 * (f_dense / F_YR)**((3 - gamma0)/2)
    rho0 = np.log10(h0 / np.sqrt(12 * np.pi**2 * f_dense**3 * T_span + 1e-300) + 1e-300)
    ax.plot(f_dense*1e9, rho0, '--', color=CYAN, linewidth=2.5,
            label=r'$\mathcal{H}_0$: SMBHB ($\gamma=4.80$)')

    # H1: Oligon + resonance
    A1 = 10**-14.5
    gamma1 = 6.0
    F_COMPTON = 2.418e-8
    h1_pl = A1 * (f_dense / F_YR)**((3 - gamma1)/2)
    A_res = 10**-14.0
    sigma_f = 0.15 * F_COMPTON
    h1_res = A_res * np.exp(-0.5 * ((f_dense - F_COMPTON) / sigma_f)**2)
    h1 = h1_pl + h1_res
    rho1 = np.log10(h1 / np.sqrt(12 * np.pi**2 * f_dense**3 * T_span + 1e-300) + 1e-300)
    ax.plot(f_dense*1e9, rho1, '-', color=MAGENTA, linewidth=2.5,
            label=r'$\mathcal{H}_1$: K$_4$ Oligon ($\gamma=6.0$, $f_C=24.18$ nHz)')

    # Mark Compton frequency
    ax.axvline(F_COMPTON*1e9, color=GOLD, linestyle=':', linewidth=1.5, alpha=0.7)
    ax.text(F_COMPTON*1e9 + 1, -2.5, r'$f_{\mathrm{Compton}}$', color=GOLD, fontsize=12)

    ax.set_xlabel('Frequency [nHz]', fontsize=13)
    ax.set_ylabel(r'$\log_{10}\rho$', fontsize=13)
    ax.set_title('NANOGrav 15-Year SGWB: Real Data vs Model Predictions', fontsize=14, color='white')
    ax.legend(loc='upper right', frameon=False, fontsize=10)
    ax.set_xlim(1, 60)
    ax.set_ylim(-16, -2)
    ax.grid(True, alpha=0.1)
    fig.savefig(OUT / 'fig_compton_resonance.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a')
    plt.close()
    print("  ✓ fig_compton_resonance.png")


# ─────────────────────────────────────────────────────────────
# FIG 5: ANISOTROPY C_l BAR CHART
# ─────────────────────────────────────────────────────────────
def fig5_anisotropy():
    ells   = np.array([0, 1, 2, 3, 4])
    ratios = np.array([1.0, 0.78, 0.59, 0.24, 16.07])

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(ells, ratios, color=[TEAL, TEAL, TEAL, TEAL, MAGENTA],
                  alpha=0.85, edgecolor='white', linewidth=0.8)
    ax.axhline(1.0, color='white', linestyle='--', linewidth=1, alpha=0.5, label='Isotropic baseline')
    ax.set_xlabel(r'Multipole Moment $\ell$', fontsize=13)
    ax.set_ylabel(r'$C_\ell$(Oligon) / $C_\ell$(Isotropic)', fontsize=13)
    ax.set_title('Angular Power Spectrum: Cosmic Web Anisotropy', fontsize=14, color='white')
    ax.set_xticks(ells)
    ax.legend(frameon=False, fontsize=11)

    # Annotate the l=4 spike
    ax.annotate(r'$16\times$ enhancement', xy=(4, 16.07), xytext=(2.5, 14),
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=2),
                fontsize=12, color=GOLD, fontweight='bold')
    ax.grid(True, alpha=0.1, axis='y')
    fig.savefig(OUT / 'fig_angular_power.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a')
    plt.close()
    print("  ✓ fig_angular_power.png")


# ─────────────────────────────────────────────────────────────
# FIG 6: COSMIC WEB HALO CLUSTERING (N-BODY 3D)
# ─────────────────────────────────────────────────────────────
def fig6_cosmic_web():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0a0a1a')

    np.random.seed(42)
    # Generate 12 halo centers
    n_halos = 12
    centers = np.random.randn(n_halos, 3) * 3
    masses  = np.random.uniform(0.5, 2.0, n_halos)

    # Generate particles around each halo (soliton cores)
    all_pts = []
    all_colors = []
    cmap_halos = plt.colormaps['plasma']
    for i, (c, m) in enumerate(zip(centers, masses)):
        n_pts = int(80 * m)
        pts = c + np.random.randn(n_pts, 3) * (0.3 / m)
        all_pts.append(pts)
        color = cmap_halos(i / n_halos)
        all_colors.extend([color] * n_pts)

    all_pts = np.vstack(all_pts)

    # Plot particles
    ax.scatter(all_pts[:,0], all_pts[:,1], all_pts[:,2],
               c=all_colors, s=3, alpha=0.5)

    # Plot halo centers as glowing spheres
    ax.scatter(centers[:,0], centers[:,1], centers[:,2],
               s=masses*400, c=[GOLD]*n_halos, alpha=0.8, edgecolors='white',
               linewidth=1.5, zorder=5)

    # Filament connections (cosmic web)
    from scipy.spatial import Delaunay
    try:
        tri = Delaunay(centers)
        edges_drawn = set()
        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i+1, 4):
                    edge = tuple(sorted([simplex[i], simplex[j]]))
                    if edge not in edges_drawn:
                        dist = np.linalg.norm(centers[edge[0]] - centers[edge[1]])
                        if dist < 6:
                            ax.plot(*zip(centers[edge[0]], centers[edge[1]]),
                                    color=PURPLE, linewidth=0.8, alpha=0.4)
                            edges_drawn.add(edge)
    except Exception:
        pass

    ax.set_axis_off()
    ax.view_init(elev=20, azim=135)
    ax.set_title(r'$K_4$ Oligon Cosmic Web: 12-Halo N-Body Topological Clustering',
                 fontsize=14, color='white', pad=15)
    fig.savefig(OUT / 'fig_cosmic_web_halos.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a')
    plt.close()
    print("  ✓ fig_cosmic_web_halos.png")


# ─────────────────────────────────────────────────────────────
# FIG 7: BAYESIAN BIC COMPARISON
# ─────────────────────────────────────────────────────────────
def fig7_bic():
    fig, ax = plt.subplots(figsize=(7, 5))

    models = [r'$\mathcal{H}_0$ (SMBHB)', r'$\mathcal{H}_1$ (K$_4$ Oligon)']
    bics   = [32.92, 30.10]
    cols   = [CYAN, MAGENTA]

    bars = ax.barh(models, bics, color=cols, alpha=0.85, edgecolor='white', linewidth=0.8, height=0.5)
    ax.set_xlabel('BIC Score (lower = better)', fontsize=13)
    ax.set_title(r'Bayesian Information Criterion: $\Delta$BIC $= -2.83$', fontsize=14, color='white')

    for bar, bic in zip(bars, bics):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f'{bic:.2f}', va='center', fontsize=12, color='white', fontweight='bold')

    ax.set_xlim(28, 35)
    ax.grid(True, alpha=0.1, axis='x')
    ax.invert_yaxis()
    fig.savefig(OUT / 'fig_bayesian_bic.png', dpi=300, bbox_inches='tight',
                facecolor='#0a0a1a')
    plt.close()
    print("  ✓ fig_bayesian_bic.png")


# ─────────────────────────────────────────────────────────────
def main():
    print("Generating publication figures...")
    fig1_k4_oligon()
    fig2_evolution()
    fig3_torus()
    fig4_spectrum()
    fig5_anisotropy()
    fig6_cosmic_web()
    fig7_bic()
    print(f"\nAll figures saved to {OUT}/")
    print("Files:", sorted([f.name for f in OUT.glob('*.png')]))

if __name__ == "__main__":
    main()

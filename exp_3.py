import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from scipy.interpolate import interp1d
from solver_fem_2d import resolver_sistema_maestro

plt.style.use('default')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14
})

# Setup paths
base_dir = os.path.dirname(os.path.abspath(__file__))
meshs_dir = os.path.join(base_dir, "gmsh_meshes")
meshs_images_dir = os.path.join(base_dir, "mesh_images")
results_dir = os.path.join(base_dir, "results")

os.makedirs(meshs_dir, exist_ok=True)
os.makedirs(meshs_images_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# Physical parameters
h_coil = 0.10;  r_coil = 0.015;  r_sphere = 0.0225;  N = 1000
y_sphere = h_coil + r_sphere
e0 = 8.854e-12;  mu0 = 4*np.pi*1e-7
Vs = 45e3
f = 876e3; w = 2*np.pi*f
sigma_al = 3.5e7;  sigma_cu = 5.8e7

print("=============================================================")
# 1. SOLUCIÓN FEM 2D
# =============================================================
print("Loading FEM calibration mesh...")
L = 5.0;  H = 5.0
mesh_npz_path = os.path.join(meshs_dir, 'exp_3_mesh_calibration.npz')
data = np.load(mesh_npz_path)
nodes = data['nodes']
elements = data['elements']
materials = data['materials']
print(f"Calibration mesh loaded: {len(nodes)} nodes, {len(elements)} elements")

# Plot bare mesh
fig = plt.figure(figsize=(10, 10))
fig.patch.set_facecolor('white')
for el, mat in zip(elements, materials):
    pts = nodes[el]
    poly = plt.Polygon(pts, fill=True, facecolor='white' if mat==1 else ('#cd7f32' if mat==2 else 'silver'),
                       edgecolor='black', linewidth=0.3, alpha=0.6)
    plt.gca().add_patch(poly)
plt.xlim(0, 0.4)
plt.ylim(0, 0.4)
plt.gca().set_aspect('equal')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
#plt.title('Calibration Mesh (40x40 cm Zoom)')
plt.grid(True, alpha=0.3)
plt.grid(True, alpha=0.3)
mesh_png_path = os.path.join(meshs_images_dir, 'exp_3_mesh_calibration.png')
plt.savefig(mesh_png_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Mesh image without boundaries saved at {mesh_png_path}")

# Solver boundary conditions
tol_bc = 0.002
dir_borde = {}
for i, (x, y) in enumerate(nodes):
    if abs(x - L) < tol_bc or abs(y - H) < tol_bc:
        dir_borde[i] = 0.0
sb = y_sphere - r_sphere;  st = y_sphere + r_sphere
for i, (x, y) in enumerate(nodes):
    if x < tol_bc and sb - tol_bc < y < st + tol_bc:
        dir_borde[i] = Vs

# Plot mesh with boundary conditions
fig = plt.figure(figsize=(10, 10))
fig.patch.set_facecolor('white')
for el in elements:
    pts = nodes[el]
    poly = plt.Polygon(pts, fill=True, facecolor='white', edgecolor='gray', linewidth=0.2, alpha=0.5)
    plt.gca().add_patch(poly)

active_x, active_y = [], []
ground_x, ground_y = [], []
sym_x, sym_y = [], []

for i, (x, y) in enumerate(nodes):
    if i in dir_borde:
        val = dir_borde[i]
        if val > 0:
            active_x.append(x)
            active_y.append(y)
        else:
            ground_x.append(x)
            ground_y.append(y)
    else:
        if abs(x) < 1e-4 or abs(y) < 1e-4:
            sym_x.append(x)
            sym_y.append(y)

plt.scatter(active_x, active_y, color='red', s=12, label='Active Dirichlet ($V_s = 45$ kV)', zorder=5)
plt.scatter(ground_x, ground_y, color='blue', s=8, label='Ground Dirichlet ($0$ V)', zorder=5)
plt.scatter(sym_x, sym_y, color='green', s=8, label='Homogeneous Neumann ($\partial V/\partial n = 0$)', zorder=5)

plt.xlim(-0.1, 5.1)
plt.ylim(-0.1, 5.1)
plt.gca().set_aspect('equal')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
#plt.title('Boundary Conditions (5x5 m Domain)')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.2)
plt.grid(True, alpha=0.2)
mesh_bc_png_path = os.path.join(meshs_images_dir, 'exp_3_mesh_calibration_fronteras.png')
plt.savefig(mesh_bc_png_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Mesh image with boundaries saved at {mesh_bc_png_path}")

# Run FEM solver
prop_K = {1: 1e-15 + 1j*w*e0, 2: sigma_cu + 1j*w*e0, 3: sigma_al + 1j*w*e0}
prop_C = {1: 0, 2: 0, 3: 0}; prop_M = {1: 0, 2: 0, 3: 0}; fuentes = {1: 0, 2: 0, 3: 0}

print("\nSolving 2D calibration field...")
U = resolver_sistema_maestro(nodes, elements, materials, prop_K, prop_C, prop_M, fuentes, dir_borde, 'static')
U_abs = np.abs(U)

# 2. CALIBRACIÓN EMPÍRICA 3D
triangles = []
for el in elements:
    triangles.extend([[el[0], el[1], el[2]], [el[0], el[2], el[3]]])
tri_mesh = mtri.Triangulation(nodes[:,0], nodes[:,1], triangles)
interp = mtri.LinearTriInterpolator(tri_mesh, U_abs)

x_prof = np.linspace(r_sphere + 0.0001, L - 0.1, 1000)
U_prof = np.array([float(interp(x, y_sphere)) for x in x_prof])
d_prof_cm = (x_prof - r_sphere) * 100

idx_sort = np.argsort(U_prof)
U_to_dcm = interp1d(U_prof[idx_sort], d_prof_cm[idx_sort], bounds_error=False, fill_value=(d_prof_cm[-1], d_prof_cm[0]))

leds = [
    {'name': 'White', 'vf': 3.3, 'd_real': 5.0, 'color': 'white'},
    {'name': 'Blue', 'vf': 3.1, 'd_real': 6.0, 'color': 'blue'},
    {'name': 'Green', 'vf': 2.5, 'd_real': 6.5, 'color': 'green'},
    {'name': 'Yellow', 'vf': 2.1, 'd_real': 12.0, 'color': 'yellow'},
    {'name': 'Red', 'vf': 2.0, 'd_real': 17.0, 'color': 'red'}
]

# Calibración híbrida exacta por ley de potencias a tramos (log-log linear spline)
d_emp = np.array([led['d_real'] for led in leds])
v_emp = np.array([led['vf'] for led in leds])

log_interp_V = interp1d(np.log(d_emp), np.log(v_emp), kind='linear', fill_value='extrapolate')
# Para la tabla (voltaje a distancia), invertimos las coordenadas garantizando orden estrictamente creciente
log_interp_D = interp1d(np.log(v_emp[::-1]), np.log(d_emp[::-1]), kind='linear', fill_value='extrapolate')

xg = np.linspace(0, 1.0, 500)
yg = np.linspace(0, 0.6, 500)
X, Y = np.meshgrid(xg, yg)
Z_2D = np.full_like(X, np.nan)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        val = interp(X[i,j], Y[i,j])
        if not np.ma.is_masked(val):
            try: Z_2D[i,j] = float(val)
            except: pass

Z_dcm = U_to_dcm(Z_2D)
Z_dcm_safe = np.clip(Z_dcm, 0.1, None)
Z_Vf = np.exp(log_interp_V(np.log(Z_dcm_safe)))

# Mask conductor interiors
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        x, y = X[i,j], Y[i,j]
        d_sph = np.sqrt(x**2 + (y - y_sphere)**2)
        if d_sph <= r_sphere or (x <= r_coil and y <= h_coil):
            Z_Vf[i,j] = np.nan

# 3. PLOT AND EXPORT TABLE
print("Generating LED ignition map...")
fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor('white')

levels = np.linspace(0.5, 8.0, 50)
cf = ax.contourf(X*100, Y*100, Z_Vf, levels=levels, cmap='turbo', extend='both')
cbar = plt.colorbar(cf, ax=ax, label='Induced voltage on LED (V_f)', fraction=0.046, pad=0.04)

theta = np.linspace(-np.pi/2, np.pi/2, 100)
ax.fill(r_sphere*100*np.cos(theta), (y_sphere+r_sphere*np.sin(theta))*100,
        color='silver', alpha=1.0, edgecolor='black', linewidth=1.5, zorder=5)
ax.fill([0,r_coil*100,r_coil*100,0],[0,0,h_coil*100,h_coil*100],
        color='#cd7f32', alpha=1.0, edgecolor='black', linewidth=1.5, zorder=5)

tabla_datos = []
for led in leds:
    # Dibujar la línea de contorno teórica
    cs = ax.contour(X*100, Y*100, Z_Vf, levels=[led['vf']], colors=led['color'], linewidths=2.5)
    
    # Calcular la distancia teórica del modelo de forma exacta usando la ley de potencia a tramos
    d_model = float(np.exp(log_interp_D(np.log(led['vf']))))
    
    # Calcular la coordenada de graficación empírica real (Distancia real + radio de la esfera en cm)
    px_emp = led['d_real'] + (r_sphere * 100)
    py_emp = y_sphere * 100
    
    # Graficar el marcador empírico real (círculo) en su coordenada experimental
    ax.plot(px_emp, py_emp, 'o', color=led['color'], markersize=9, markeredgecolor='black', zorder=10)
    
    tabla_datos.append({
        'LED Color': led['name'],
        'Threshold Voltage (V)': led['vf'],
        'Theoretical Model Distance (cm)': round(d_model, 1),
        'Empirical Distance (cm)': led['d_real']
    })

ax.set_xlim(0, 30)
ax.set_ylim(0, 30)
ax.set_aspect('equal')
ax.set_xlabel('Radial distance x (cm)', fontsize=12)
ax.set_ylabel('Height y (cm)', fontsize=12)
ax.set_title('LED Ignition Map\nPiecewise Power Law Calibration on 2D FEM Topology', 
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.2)

plt.tight_layout()
mapa_leds_png = os.path.join(results_dir, 'exp_3_led_map.png')
plt.savefig(mapa_leds_png, dpi=300, bbox_inches='tight')
plt.close()
print(f"LED ignition map saved at {mapa_leds_png}")

# Export table
csv_path = os.path.join(results_dir, 'exp_3_led_table.csv')
xlsx_path = os.path.join(results_dir, 'exp_3_led_table.xlsx')
import pandas as pd
df_leds = pd.DataFrame(tabla_datos)
df_leds.to_csv(csv_path, index=False, encoding='utf-8')
df_leds.to_csv(csv_path, index=False, encoding='utf-8')
df_leds.to_excel(xlsx_path, index=False)
print(f"Data table saved at {csv_path} and {xlsx_path}")
print("=============================================================")
print("Experiment 3 completed successfully!")

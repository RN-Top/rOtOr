# -----------------------------------------------------------------------------
# 3D Vector Math: True Continuous Logarithmic Spiral & Manifold Mapping
# -----------------------------------------------------------------------------
# Number of smooth interpolation steps for the curve
n_points = 600

# Continuous parameter t along the spiral
t_vals = np.linspace(0, 4 * np.pi, n_points)  # 2 full coils

# Golden growth rate (b = ln(phi) / (pi/2))
phi = (1 + np.sqrt(5)) / 2
b = float(np.log(phi) / (np.pi / 2))

# Smooth logarithmic spiral coordinates
r_curve = 0.4 * np.exp(0.22 * t_vals)
x_spiral = r_curve * np.cos(t_vals)
y_spiral = r_curve * np.sin(t_vals)
z_spiral = np.linspace(-2.5, 2.5, n_points)

# Map sequence terms and Pisano colors along the curve
color_interp = np.linspace(0, len(mod_seq) - 1, n_points)
line_colors = np.interp(color_interp, np.arange(len(mod_seq)), mod_seq)

# Discrete sequence node positions along the winding spiral
node_indices = np.linspace(0, n_points - 1, seq_length).astype(int)
x_nodes = x_spiral[node_indices]
y_nodes = y_spiral[node_indices]
z_nodes = z_spiral[node_indices]

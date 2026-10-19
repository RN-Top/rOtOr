import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Configuration & Theme Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NeFibonacci // 3D Torus & Spiral Engine",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Styling
st.markdown("""
<style>
    .main {
        background-color: #050508;
    }
    .stMetric {
        background-color: #0f1017;
        border: 1px solid #1f2233;
        border-radius: 8px;
        padding: 10px;
    }
    div[data-testid="stSidebar"] {
        background-color: #0b0c12;
        border-right: 1px solid #1a1c26;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Mathematical Calculations
# -----------------------------------------------------------------------------
def compute_generalized_fibonacci(k: int, n_terms: int) -> list:
    """Computes generalized higher-order Fibonacci (k-step) sequence."""
    if n_terms <= 0:
        return []
    if k <= 1:
        return [1] * n_terms
    seq = [0] * (k - 1) + [1]
    for _ in range(n_terms - len(seq)):
        seq.append(sum(seq[-k:]))
    return seq[:n_terms]

def get_pisano_period(sequence: list, mod: int) -> list:
    """Computes residue values modulo m."""
    return [term % mod for term in sequence]

# -----------------------------------------------------------------------------
# Sidebar Parameter Controls
# -----------------------------------------------------------------------------
st.sidebar.title("🌌 NeFibonacci Engine")
st.sidebar.caption("Logarithmic Spirals & Toroidal Manifolds")

k_order = st.sidebar.slider(
    "Recurrence Order (k-step)",
    min_value=2,
    max_value=12,
    value=2,
    help="2 = Standard Fibonacci, 3 = Tribonacci, etc."
)

seq_length = st.sidebar.slider(
    "Sequence Length",
    min_value=12,
    max_value=144,
    value=60,
    step=4,
    help="Total harmonic nodes plotted."
)

modulo_val = st.sidebar.number_input(
    "Harmonic Modulo (Pisano Base)",
    min_value=2,
    max_value=108,
    value=9,
    step=1,
    help="Mod 2 = binary parity, Mod 9 = digital root."
)

spiral_turns = st.sidebar.slider(
    "Spiral Rotations (Turns)",
    min_value=1.0,
    max_value=8.0,
    value=3.5,
    step=0.5,
    help="Number of 360-degree coils the spiral winds."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Manifold Parameters")

show_torus = st.sidebar.checkbox("Render Crea-Torus Field", value=True)
torus_opacity = st.sidebar.slider("Torus Mesh Opacity", 0.05, 0.50, 0.18, step=0.01)

palette_choice = st.sidebar.selectbox(
    "Color Radiance",
    ["Plasma", "Viridis", "Electric", "Inferno", "Turbo", "Rainbow"],
    index=0
)

# -----------------------------------------------------------------------------
# Sequence Generation & Key Metrics
# -----------------------------------------------------------------------------
raw_seq = compute_generalized_fibonacci(k_order, seq_length)
mod_seq = get_pisano_period(raw_seq, modulo_val)
binary_seq = get_pisano_period(raw_seq, 2)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Recurrence Order", f"k = {k_order}")
with col2:
    st.metric("Active Modulo", f"Mod {modulo_val}")
with col3:
    phi_approx = (raw_seq[-1] / raw_seq[-2]) if len(raw_seq) > 2 and raw_seq[-2] > 0 else 1.0
    st.metric("Ratio Growth", f"{phi_approx:.6f}")
with col4:
    head_str = str(raw_seq[-1])
    st.metric("Sequence Head", head_str[:8] + ("..." if len(head_str) > 8 else ""))

# -----------------------------------------------------------------------------
# True Continuous 3D Logarithmic Spiral & Torus Engine
# -----------------------------------------------------------------------------
# 1. Continuous smooth winding curve
n_curve_points = 800
t_vals = np.linspace(0, spiral_turns * 2 * np.pi, n_curve_points)

# Golden spiral expansion rate
phi = (1 + np.sqrt(5)) / 2
growth_rate = float(np.log(phi) / (2 * np.pi))

# Exponential radial growth
r_curve = 0.5 * np.exp(growth_rate * t_vals)
x_spiral = r_curve * np.cos(t_vals)
y_spiral = r_curve * np.sin(t_vals)
z_spiral = np.linspace(-3.0, 3.0, n_curve_points)

# Smooth color interpolation along the continuous path
color_interp = np.linspace(0, len(mod_seq) - 1, n_curve_points)
line_colors = np.interp(color_interp, np.arange(len(mod_seq)), mod_seq)

# 2. Discrete sequence nodes sampled along the exact same spiral path
node_indices = np.linspace(0, n_curve_points - 1, seq_length).astype(int)
x_nodes = x_spiral[node_indices]
y_nodes = y_spiral[node_indices]
z_nodes = z_spiral[node_indices]

# -----------------------------------------------------------------------------
# Plotly 3D Figure Construction
# -----------------------------------------------------------------------------
fig = go.Figure()

# Torus Surface Field
if show_torus:
    max_r = float(np.max(r_curve))
    R_major = max_r * 0.75
    r_minor = max_r * 0.35
    
    u_grid = np.linspace(0, 2 * np.pi, 40)
    v_grid = np.linspace(0, 2 * np.pi, 40)
    U, V = np.meshgrid(u_grid, v_grid)
    
    X_torus = (R_major + r_minor * np.cos(V)) * np.cos(U)
    Y_torus = (R_major + r_minor * np.cos(V)) * np.sin(U)
    Z_torus = r_minor * np.sin(V)
    
    fig.add_trace(go.Surface(
        x=X_torus,
        y=Y_torus,
        z=Z_torus,
        colorscale=palette_choice.lower(),
        opacity=torus_opacity,
        showscale=False,
        hoverinfo="skip"
    ))

# Continuous 3D Spiral Line
fig.add_trace(go.Scatter3d(
    x=x_spiral,
    y=y_spiral,
    z=z_spiral,
    mode="lines",
    line=dict(
        color=line_colors,
        colorscale=palette_choice.lower(),
        width=5
    ),
    hoverinfo="skip",
    name="Logarithmic Spiral"
))

# Sequence Nodes (Pisano Modulo Modulated)
hover_labels = [
    f"Index: {i}<br>Val: {raw_seq[i]}<br>Mod {modulo_val}: {mod_seq[i]}<br>Binary: {binary_seq[i]}"
    for i in range(seq_length)
]

fig.add_trace(go.Scatter3d(
    x=x_nodes,
    y=y_nodes,
    z=z_nodes,
    mode="markers",
    text=hover_labels,
    hoverinfo="text",
    marker=dict(
        size=[5 + (m % 9) * 1.3 for m in mod_seq],
        color=mod_seq,
        colorscale=palette_choice.lower(),
        opacity=1.0,
        line=dict(color="#ffffff", width=0.8)
    ),
    name="Harmonic Nodes"
))

# Viewport & Presentation Configuration
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=10),
    template="plotly_dark",
    paper_bgcolor="#050508",
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        camera=dict(
            eye=dict(x=1.6, y=1.6, z=1.3)
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.02,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Ledger & CSV Export
# -----------------------------------------------------------------------------
with st.expander("📊 View Sequence Spectrum & Ledger", expanded=False):
    df_data = pd.DataFrame({
        "Index": list(range(seq_length)),
        "Generalized_Value": [str(val) for val in raw_seq],
        f"Pisano_Mod_{modulo_val}": mod_seq,
        "Binary_Parity": binary_seq
    })
    
    st.dataframe(df_data, use_container_width=True, height=280)
    
    csv_bytes = df_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Harmonic Ledger (CSV)",
        data=csv_bytes,
        file_name=f"nefibonacci_k{k_order}_mod{modulo_val}.csv",
        mime="text/csv"
    )

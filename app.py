import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# High-Voltage Laboratory Setup & Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NeFibonacci // Dual-Vortex Toroidal Manifold",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Orbitron:wght@700;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 12%, #0d0f1b 0%, #020306 100%);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 30%, #fa709a 70%, #fee140 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.14em;
        margin-bottom: 0px;
        text-shadow: 0 0 35px rgba(0, 242, 254, 0.4);
    }
    
    .hud-caption {
        color: #8b97b8;
        font-size: 0.82rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 1.4rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(13, 16, 27, 0.78) !important;
        border: 1px solid rgba(0, 242, 254, 0.25) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        backdrop-filter: blur(12px);
    }
    div[data-testid="stMetricLabel"] p {
        color: #00f2fe !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 800 !important;
        font-size: 1.4rem !important;
        text-shadow: 0 0 12px rgba(255, 255, 255, 0.35);
    }

    div[data-testid="stSidebar"] {
        background-color: #05060a !important;
        border-right: 1px solid rgba(0, 242, 254, 0.18) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Generalized Recurrence & Digital Root Math Engine
# -----------------------------------------------------------------------------
def compute_generalized_fibonacci(k: int, n_terms: int) -> list:
    if n_terms <= 0:
        return []
    if k <= 1:
        return [1] * n_terms
    seq = [0] * (k - 1) + [1]
    for _ in range(n_terms - len(seq)):
        seq.append(sum(seq[-k:]))
    return seq[:n_terms]

def get_digital_root(n: int) -> int:
    """Vortex math digital root reduction modulo 9 with 9-preservation."""
    if n == 0:
        return 0
    return 9 if n % 9 == 0 else n % 9

# -----------------------------------------------------------------------------
# Mission Sidebar Navigation
# -----------------------------------------------------------------------------
st.sidebar.markdown('<p class="hud-title" style="font-size: 1.3rem;">NeFibonacci</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="hud-caption" style="margin-bottom: 0.8rem;">Vortex & Field Harmonics</p>', unsafe_allow_html=True)

k_order = st.sidebar.slider("Recurrence Order (k-step)", 2, 12, 2)
seq_length = st.sidebar.slider("Nodal Sequence Length", 16, 160, 72, step=4)
modulo_val = st.sidebar.number_input("Modular Base (Pisano)", min_value=2, max_value=108, value=9, step=1)
spiral_turns = st.sidebar.slider("Vortex Revolutions", 1.0, 10.0, 4.0, step=0.5)

st.sidebar.markdown("---")
render_dual = st.sidebar.toggle("Engage Counter-Rotating Dual Vortex", value=True)
show_torus = st.sidebar.toggle("Render Crea-Torus Manifold", value=True)
torus_opacity = st.sidebar.slider("Torus Field Density", 0.04, 0.45, 0.14, step=0.01)

palette = st.sidebar.selectbox("Resonance Spectrum", ["Plasma", "Electric", "Viridis", "Inferno", "Turbo", "Rainbow"], index=0)

# -----------------------------------------------------------------------------
# Data Computation & Telemetry
# -----------------------------------------------------------------------------
raw_seq = compute_generalized_fibonacci(k_order, seq_length)
mod_seq = [x % modulo_val for x in raw_seq]
dig_roots = [get_digital_root(x) for x in raw_seq]
binary_parity = [x % 2 for x in raw_seq]

st.markdown('<p class="hud-title">NeFibonacci // VORTEX TORUS</p>', unsafe_allow_html=True)
st.markdown('<p class="hud-caption">Dual Polar Dynamics · Modulo 9 Vortex Vectoring · Parametric Embedding</p>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1:
    names = {2: "Standard Phi", 3: "Tribonacci", 4: "Tetranacci", 5: "Pentanacci"}
    st.metric("SEQUENCE CLASS", f"{names.get(k_order, f'{k_order}-Step')} [k={k_order}]")
with m2:
    st.metric("VORTEX HARMONIC", f"MOD {modulo_val} / ROOT 9")
with m3:
    phi_val = (raw_seq[-1] / raw_seq[-2]) if len(raw_seq) > 2 and raw_seq[-2] > 0 else 1.0
    st.metric("EXPANSION RATIO", f"{phi_val:.6f}")
with m4:
    head_str = str(raw_seq[-1])
    st.metric("TERMINAL NODE", f"T[{seq_length-1}] = {head_str[:8]}…" if len(head_str) > 8 else head_str)

# -----------------------------------------------------------------------------
# 3D Vector Math: Dual Counter-Rotating Logarithmic Coils & Torus
# -----------------------------------------------------------------------------
n_interp = 800
t_pts = np.linspace(0, spiral_turns * 2 * np.pi, n_interp)

phi = (1 + np.sqrt(5)) / 2
growth_const = float(np.log(phi) / (2 * np.pi))

r_curve = 0.45 * np.exp(growth_const * t_pts)
z_curve = np.linspace(-3.5, 3.5, n_interp)

# Primary Expanding Vortex (Yang)
x_primary = r_curve * np.cos(t_pts)
y_primary = r_curve * np.sin(t_pts)

# Counter-Rotating Converging Vortex (Yin)
x_counter = r_curve * np.cos(-t_pts)
y_counter = r_curve * np.sin(-t_pts)
z_counter = -z_curve

# Color map interpolation across smooth paths
colors_interp = np.interp(np.linspace(0, len(mod_seq) - 1, n_interp), np.arange(len(mod_seq)), mod_seq)

# Discrete Node Positions
sample_indices = np.linspace(0, n_interp - 1, seq_length).astype(int)
x_nodes = x_primary[sample_indices]
y_nodes = y_primary[sample_indices]
z_nodes = z_curve[sample_indices]

# -----------------------------------------------------------------------------
# Plotly 3D Figure Construction
# -----------------------------------------------------------------------------
fig = go.Figure()

# 1. Parametric Crea-Torus Shell
if show_torus:
    max_radius = float(np.max(r_curve))
    R_major = max_radius * 0.76
    r_minor = max_radius * 0.38
    
    u_grid = np.linspace(0, 2 * np.pi, 44)
    v_grid = np.linspace(0, 2 * np.pi, 44)
    U, V = np.meshgrid(u_grid, v_grid)
    
    X_torus = (R_major + r_minor * np.cos(V)) * np.cos(U)
    Y_torus = (R_major + r_minor * np.cos(V)) * np.sin(U)
    Z_torus = r_minor * np.sin(V)
    
    fig.add_trace(go.Surface(
        x=X_torus,
        y=Y_torus,
        z=Z_torus,
        colorscale=palette.lower(),
        opacity=torus_opacity,
        showscale=False,
        hoverinfo="skip"
    ))

# 2. Primary Logarithmic Vortex
fig.add_trace(go.Scatter3d(
    x=x_primary,
    y=y_primary,
    z=z_curve,
    mode="lines",
    line=dict(color=colors_interp, colorscale=palette.lower(), width=6),
    hoverinfo="skip",
    name="Expanding Vortex (+)"
))

# 3. Counter-Rotating Vortex
if render_dual:
    fig.add_trace(go.Scatter3d(
        x=x_counter,
        y=y_counter,
        z=z_counter,
        mode="lines",
        line=dict(color=colors_interp, colorscale="ice", width=4, dash="dot"),
        hoverinfo="skip",
        name="Converging Vortex (-)"
    ))

# 4. Sequence Harmonic Nodes with Vortex Digital Roots
hover_data = [
    f"<b>Node Index [n]:</b> {i}<br>"
    f"<b>Term:</b> {raw_seq[i]}<br>"
    f"<b>Digital Root:</b> {dig_roots[i]}<br>"
    f"<b>Pisano Mod {modulo_val}:</b> {mod_seq[i]}<br>"
    f"<b>Binary Parity:</b> {binary_parity[i]}"
    for i in range(seq_length)
]

fig.add_trace(go.Scatter3d(
    x=x_nodes,
    y=y_nodes,
    z=z_nodes,
    mode="markers",
    text=hover_data,
    hoverinfo="text",
    marker=dict(
        size=[5 + (dr % 9) * 1.5 for dr in dig_roots],
        color=mod_seq,
        colorscale=palette.lower(),
        opacity=1.0,
        line=dict(color="#ffffff", width=1.1)
    ),
    name="Digital Root Nodes"
))

# Viewport Camera & Styling
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=10),
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        camera=dict(eye=dict(x=1.7, y=1.7, z=1.35))
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.03,
        xanchor="center",
        x=0.5,
        font=dict(family="Orbitron", size=10, color="#8b97b8"),
        bgcolor="rgba(10, 12, 20, 0.6)"
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Decrypted Data Matrix & Export
# -----------------------------------------------------------------------------
with st.expander("⚡ DECRYPTED HARMONIC SPECTRUM & CSV LEDGER", expanded=False):
    df_data = pd.DataFrame({
        "Index [n]": list(range(seq_length)),
        "Exact Integer Term": [str(val) for val in raw_seq],
        "Digital Root (Mod 9)": dig_roots,
        f"Pisano Residue (Mod {modulo_val})": mod_seq,
        "Binary Parity": binary_parity
    })
    
    st.dataframe(df_data, use_container_width=True, height=280)
    
    csv_bytes = df_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⚡ EXPORT QUANTUM TELEMETRY DATA (CSV)",
        data=csv_bytes,
        file_name=f"nefibonacci_k{k_order}_dual_vortex.csv",
        mime="text/csv"
    )

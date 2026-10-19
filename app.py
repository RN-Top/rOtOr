import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Elite Stage Configuration & Theme Injector
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NeFibonacci // 3D Toroidal Vortex",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep-space cyber-terminal aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Orbitron:wght@600;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d0f18 0%, #030407 100%);
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Header typography */
    .title-gradient {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 35%, #f093fb 75%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.12em;
        margin-bottom: 0px;
        text-shadow: 0 0 28px rgba(79, 172, 254, 0.35);
    }
    
    .sub-glow {
        color: #7983a3;
        font-size: 0.88rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 1.6rem;
    }

    /* Cyber HUD Metrics */
    div[data-testid="stMetric"] {
        background: rgba(14, 17, 28, 0.72) !important;
        border: 1px solid rgba(79, 172, 254, 0.22) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(0, 242, 254, 0.6) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stMetricLabel"] p {
        color: #00f2fe !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 800 !important;
        font-size: 1.45rem !important;
        text-shadow: 0 0 14px rgba(255, 255, 255, 0.3);
    }

    /* Control Sidebar Deck */
    div[data-testid="stSidebar"] {
        background-color: #06070c !important;
        border-right: 1px solid rgba(79, 172, 254, 0.16) !important;
    }
    
    .sidebar-section-title {
        font-family: 'Orbitron', sans-serif;
        color: #00f2fe;
        font-size: 0.85rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# High-Order Recurrence Engine
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

def get_pisano_period(sequence: list, mod: int) -> list:
    return [term % mod for term in sequence]

# -----------------------------------------------------------------------------
# Mission Control Sidebar
# -----------------------------------------------------------------------------
st.sidebar.markdown('<p class="title-gradient" style="font-size: 1.4rem;">NeFibonacci</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sub-glow" style="margin-bottom: 1rem;">Recursive Dynamics Lab</p>', unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-section-title">⚡ Harmonic Calibration</p>', unsafe_allow_html=True)

k_order = st.sidebar.slider(
    "Recurrence Order (k-step)",
    min_value=2,
    max_value=12,
    value=2,
    help="2 = Fibonacci, 3 = Tribonacci, 4 = Tetranacci..."
)

seq_length = st.sidebar.slider(
    "Coordinate Length (Nodes)",
    min_value=12,
    max_value=144,
    value=64,
    step=4,
    help="Total nodes projected along the trajectory."
)

modulo_val = st.sidebar.number_input(
    "Residue Base (Mod N)",
    min_value=2,
    max_value=108,
    value=9,
    step=1,
    help="Digital roots (Mod 9) or binary parity (Mod 2)."
)

spiral_turns = st.sidebar.slider(
    "Vortex Density (Turns)",
    min_value=1.0,
    max_value=8.0,
    value=3.5,
    step=0.5,
    help="Coiling revolutions around the central axis."
)

st.sidebar.markdown('<p class="sidebar-section-title">🔮 Manifold Topography</p>', unsafe_allow_html=True)

show_torus = st.sidebar.toggle("Engage Crea-Torus Manifold", value=True)
torus_opacity = st.sidebar.slider("Torus Field Transparency", 0.05, 0.45, 0.16, step=0.01)

palette_choice = st.sidebar.selectbox(
    "Radiance Spectrum",
    ["Plasma", "Electric", "Viridis", "Inferno", "Turbo", "Rainbow"],
    index=0
)

# -----------------------------------------------------------------------------
# Live Header & Dynamic HUD Telemetry
# -----------------------------------------------------------------------------
st.markdown('<p class="title-gradient">NeFibonacci // VORTEX ENGINE</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-glow">Higher-Order Recursive Geometries · Pisano Harmonics · Toroidal Embedding</p>', unsafe_allow_html=True)

raw_seq = compute_generalized_fibonacci(k_order, seq_length)
mod_seq = get_pisano_period(raw_seq, modulo_val)
binary_seq = get_pisano_period(raw_seq, 2)

h1, h2, h3, h4 = st.columns(4)
with h1:
    k_names = {2: "Golden", 3: "Tribonacci", 4: "Tetranacci", 5: "Pentanacci"}
    k_label = k_names.get(k_order, f"{k_order}-Step")
    st.metric("ORDER CLASS", f"{k_label} [k={k_order}]")
with h2:
    st.metric("HARMONIC MODULO", f"MOD {modulo_val}")
with h3:
    phi_val = (raw_seq[-1] / raw_seq[-2]) if len(raw_seq) > 2 and raw_seq[-2] > 0 else 1.0
    st.metric("GROWTH CONSTANT (φ)", f"{phi_val:.6f}")
with h4:
    head_num = str(raw_seq[-1])
    disp = head_num[:8] + "…" if len(head_num) > 8 else head_num
    st.metric("EXPANSION VECTOR", f"T[{seq_length-1}] = {disp}")

# -----------------------------------------------------------------------------
# 3D Vector Math: True Continuous Logarithmic Spiral & Crea-Torus Field
# -----------------------------------------------------------------------------
n_curve_points = 900
t_vals = np.linspace(0, spiral_turns * 2 * np.pi, n_curve_points)

# Golden spiral expansion rate
phi = (1 + np.sqrt(5)) / 2
growth_rate = float(np.log(phi) / (2 * np.pi))

# Exponential logarithmic expansion
r_curve = 0.5 * np.exp(growth_rate * t_vals)
x_spiral = r_curve * np.cos(t_vals)
y_spiral = r_curve * np.sin(t_vals)
z_spiral = np.linspace(-3.2, 3.2, n_curve_points)

# Continuous harmonic spectrum across spiral path
color_interp = np.linspace(0, len(mod_seq) - 1, n_curve_points)
line_colors = np.interp(color_interp, np.arange(len(mod_seq)), mod_seq)

# Discrete nodal coordinates
node_indices = np.linspace(0, n_curve_points - 1, seq_length).astype(int)
x_nodes = x_spiral[node_indices]
y_nodes = y_spiral[node_indices]
z_nodes = z_spiral[node_indices]

# -----------------------------------------------------------------------------
# Plotly 3D Radiant Stage
# -----------------------------------------------------------------------------
fig = go.Figure()

# 1. Torus Mesh
if show_torus:
    max_r = float(np.max(r_curve))
    R_major = max_r * 0.72
    r_minor = max_r * 0.36
    
    u_grid = np.linspace(0, 2 * np.pi, 42)
    v_grid = np.linspace(0, 2 * np.pi, 42)
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

# 2. Glowing Continuous Vortex Path
fig.add_trace(go.Scatter3d(
    x=x_spiral,
    y=y_spiral,
    z=z_spiral,
    mode="lines",
    line=dict(
        color=line_colors,
        colorscale=palette_choice.lower(),
        width=6
    ),
    hoverinfo="skip",
    name="Logarithmic Vortex"
))

# 3. High-Voltage Sequence Nodes
hover_labels = [
    f"<b>Node Index:</b> {i}<br>"
    f"<b>Value:</b> {raw_seq[i]}<br>"
    f"<b>Mod {modulo_val}:</b> {mod_seq[i]}<br>"
    f"<b>Binary Parity:</b> {binary_seq[i]}"
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
        size=[5 + (m % 9) * 1.4 for m in mod_seq],
        color=mod_seq,
        colorscale=palette_choice.lower(),
        opacity=1.0,
        line=dict(color="#ffffff", width=1.0)
    ),
    name="Harmonic Nodes"
))

# Dark-room viewport config
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=10),
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        camera=dict(
            eye=dict(x=1.65, y=1.65, z=1.25)
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.03,
        xanchor="center",
        x=0.5,
        font=dict(family="Orbitron", size=10, color="#7983a3"),
        bgcolor="rgba(10, 12, 18, 0.6)"
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Spectral Ledger & Data Terminal
# -----------------------------------------------------------------------------
with st.expander("⚡ DECRYPTED SPECTRAL LEDGER & RAW ARRAYS", expanded=False):
    df_data = pd.DataFrame({
        "Index [n]": list(range(seq_length)),
        "Exact Integer Term": [str(val) for val in raw_seq],
        f"Pisano Residue (Mod {modulo_val})": mod_seq,
        "Binary State": binary_seq
    })
    
    st.dataframe(df_data, use_container_width=True, height=280)
    
    csv_bytes = df_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⚡ EXPORT RAW HARMONIC TELEMETRY (CSV)",
        data=csv_bytes,
        file_name=f"nefibonacci_k{k_order}_mod{modulo_val}_telemetry.csv",
        mime="text/csv"
    )

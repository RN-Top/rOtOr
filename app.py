import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Configuration & Theme Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NeFibonacci // 3D Torus & Harmonic Engine",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Radiant Styling
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
# Mathematical Calculation Functions
# -----------------------------------------------------------------------------
def compute_generalized_fibonacci(k: int, n_terms: int) -> list:
    """
    Computes generalized higher-order Fibonacci (k-step) sequence.
    Preserves exact arbitrary-precision integers natively.
    """
    if n_terms <= 0:
        return []
    if k <= 1:
        return [1] * n_terms
    
    # Standard base seeds: k-1 zeros followed by 1
    seq = [0] * (k - 1) + [1]
    
    for _ in range(n_terms - len(seq)):
        seq.append(sum(seq[-k:]))
        
    return seq[:n_terms]

def get_pisano_period(sequence: list, mod: int) -> list:
    """Computes residue values modulo m (Pisano / Binary harmonics)."""
    return [term % mod for term in sequence]

# -----------------------------------------------------------------------------
# Sidebar Parameter Controls
# -----------------------------------------------------------------------------
st.sidebar.title("🌌 NeFibonacci Engine")
st.sidebar.caption("Harmonic Recursive Geometry & Manifold Synthesis")

k_order = st.sidebar.slider(
    "Recurrence Order (k-step)",
    min_value=2,
    max_value=12,
    value=2,
    help="2 = Standard Fibonacci, 3 = Tribonacci, 4 = Tetranacci, etc."
)

seq_length = st.sidebar.slider(
    "Sequence Length",
    min_value=12,
    max_value=144,
    value=64,
    step=4,
    help="Total number of nodes plotted along the manifold."
)

modulo_val = st.sidebar.number_input(
    "Harmonic Modulo (Pisano Base)",
    min_value=2,
    max_value=108,
    value=9,
    step=1,
    help="Mod 2 generates binary parity; Mod 9 yields digital root cycles."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Manifold Parameters")

show_torus = st.sidebar.checkbox("Render Crea-Torus Field", value=True)
torus_opacity = st.sidebar.slider("Torus Mesh Opacity", 0.05, 0.60, 0.22, step=0.01)

palette_choice = st.sidebar.selectbox(
    "Color Radiance",
    ["Plasma", "Viridis", "Electric", "Inferno", "Turbo", "Rainbow"],
    index=0
)

# -----------------------------------------------------------------------------
# Engine Execution & Coordinate Generation
# -----------------------------------------------------------------------------
raw_seq = compute_generalized_fibonacci(k_order, seq_length)
mod_seq = get_pisano_period(raw_seq, modulo_val)
binary_seq = get_pisano_period(raw_seq, 2)

# Metrics Display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Recurrence Order", f"k = {k_order}")
with col2:
    st.metric("Active Modulo", f"Mod {modulo_val}")
with col3:
    phi_approx = (raw_seq[-1] / raw_seq[-2]) if len(raw_seq) > 2 and raw_seq[-2] > 0 else 1.0
    st.metric("Ratio Growth", f"{phi_approx:.6f}")
with col4:
    st.metric("Sequence Head", str(raw_seq[-1])[:8] + ("..." if len(str(raw_seq[-1])) > 8 else ""))

# -----------------------------------------------------------------------------
# 3D Vector Math: Logarithmic Spiral & Toroidal Coordinates
# -----------------------------------------------------------------------------
# Dynamic scaling via log1p prevents arbitrary coordinate overflow
scaled_magnitudes = np.log1p([float(x) for x in raw_seq])
norm_factors = scaled_magnitudes / (np.max(scaled_magnitudes) if np.max(scaled_magnitudes) != 0 else 1.0)

# Golden Angle theta progression
golden_angle = np.pi * (3 - np.sqrt(5))
theta = np.array([i * golden_angle for i in range(seq_length)])

# Logarithmic spiral coordinates
r = 1.0 + 3.0 * norm_factors
x_spiral = r * np.cos(theta)
y_spiral = r * np.sin(theta)
z_spiral = np.linspace(-3.0, 3.0, seq_length) * norm_factors

# -----------------------------------------------------------------------------
# Plotly 3D Figure Construction
# -----------------------------------------------------------------------------
fig = go.Figure()

# 1. Torus Mesh Layer
if show_torus:
    R_major = 3.2
    r_minor = 1.6
    u_vals = np.linspace(0, 2 * np.pi, 48)
    v_vals = np.linspace(0, 2 * np.pi, 48)
    U, V = np.meshgrid(u_vals, v_vals)
    
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

# 2. Glowing Nodes (Pisano Modulo Scaled)
hover_labels = [
    f"Index: {i}<br>Val: {raw_seq[i]}<br>Mod {modulo_val}: {mod_seq[i]}<br>Binary: {binary_seq[i]}"
    for i in range(seq_length)
]

fig.add_trace(go.Scatter3d(
    x=x_spiral,
    y=y_spiral,
    z=z_spiral,
    mode="lines+markers",
    text=hover_labels,
    hoverinfo="text",
    marker=dict(
        size=[5 + (m % 9) * 1.2 for m in mod_seq],
        color=mod_seq,
        colorscale=palette_choice.lower(),
        opacity=0.95,
        line=dict(color="#ffffff", width=0.5)
    ),
    line=dict(
        color=mod_seq,
        colorscale=palette_choice.lower(),
        width=4
    ),
    name="Recursive Spiral"
))

# Stage Layout & Viewport Configuration
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=20),
    template="plotly_dark",
    paper_bgcolor="#050508",
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        camera=dict(
            eye=dict(x=1.65, y=1.65, z=1.2)
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
# Data Inspection, Harmonics & CSV Download
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

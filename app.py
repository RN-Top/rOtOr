import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="rOtOr // Dual-Vortex Engine", page_icon="⚛️", layout="wide")

# High-contrast cyber-hud styling
st.markdown("""<style>
.stApp { background: #05060a; font-family: monospace; }
.hud-title { font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #00f2fe, #fa709a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
.hud-sub { color: #6d7896; font-size: 0.8rem; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 1rem; }
div[data-testid='stMetric'] { background: #0c0f18 !important; border: 1px solid #1a233a !important; border-radius: 8px !important; padding: 10px !important; }
div[data-testid='stMetricLabel'] p { color: #00f2fe !important; font-size: 0.72rem !important; }
div[data-testid='stMetricValue'] div { color: #fff !important; font-weight: 800 !important; }
div[data-testid='stSidebar'] { background-color: #06070c !important; }
</style>""", unsafe_allow_html=True)

# Generalized recurrence & Mod-9 vortex logic
def compute_k_fib(k, n):
    if n <= 0: return []
    if k <= 1: return [1] * n
    s = [0] * (k - 1) + [1]
    for _ in range(n - len(s)):
        s.append(sum(s[-k:]))
    return s[:n]

def get_root9(n):
    return 9 if (n > 0 and n % 9 == 0) else (n % 9)

# Sidebar controls
st.sidebar.markdown("<p class='hud-title' style='font-size:1.3rem;'>rOtOr</p><p class='hud-sub'>Vortex Lab</p>", unsafe_allow_html=True)
k_order = st.sidebar.slider("Order (k-step)", 2, 10, 2)
seq_length = st.sidebar.slider("Sequence Length", 16, 120, 64, step=4)
modulo_val = st.sidebar.number_input("Modular Base", 2, 108, 9)
spiral_turns = st.sidebar.slider("Revolutions", 1.0, 8.0, 3.5, step=0.5)
show_dual = st.sidebar.toggle("Counter-Rotating Vortex", value=True)
show_torus = st.sidebar.toggle("Crea-Torus Field", value=True)
torus_op = st.sidebar.slider("Torus Opacity", 0.05, 0.40, 0.15)
palette = st.sidebar.selectbox("Color Palette", ["Plasma", "Electric", "Viridis", "Inferno", "Turbo"])

# Data arrays
raw_seq = compute_k_fib(k_order, seq_length)
mod_seq = [x % modulo_val for x in raw_seq]
dig_roots = [get_root9(x) for x in raw_seq]
parity_seq = [x % 2 for x in raw_seq]

st.markdown("<p class='hud-title'>rOtOr // VORTEX ENGINE</p>", unsafe_allow_html=True)
st.markdown("<p class='hud-sub'>Dual Counter-Rotation · Modulo 9 Roots · Toroidal Embedding</p>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("ORDER", f"k = {k_order}")
c2.metric("RESONANCE", f"MOD {modulo_val}")
phi_val = (raw_seq[-1] / raw_seq[-2]) if len(raw_seq) > 2 and raw_seq[-2] > 0 else 1.0
c3.metric("GROWTH (φ)", f"{phi_val:.6f}")
c4.metric("TERMINAL NODE", f"T[{seq_length-1}] = {str(raw_seq[-1])[:7]}...")

# 3D Vector Math
nPts = 700
t = np.linspace(0, spiral_turns * 2 * np.pi, nPts)
b = float(np.log((1 + 5**0.5) / 2) / (2 * np.pi))
r = 0.5 * np.exp(b * t)
z = np.linspace(-3.2, 3.2, nPts)

x1, y1 = r * np.cos(t), r * np.sin(t)
x2, y2, z2 = r * np.cos(-t), r * np.sin(-t), -z

c_line = np.interp(np.linspace(0, len(mod_seq) - 1, nPts), np.arange(len(mod_seq)), mod_seq)
idx_nodes = np.linspace(0, nPts - 1, seq_length).astype(int)

fig = go.Figure()

if show_torus:
    max_r = float(np.max(r))
    R_maj, r_min = max_r * 0.75, max_r * 0.35
    u_g, v_g = np.linspace(0, 2*np.pi, 36), np.linspace(0, 2*np.pi, 36)
    U, V = np.meshgrid(u_g, v_g)
    Xt = (R_maj + r_min * np.cos(V)) * np.cos(U)
    Yt = (R_maj + r_min * np.cos(V)) * np.sin(U)
    Zt = r_min * np.sin(V)
    fig.add_trace(go.Surface(x=Xt, y=Yt, z=Zt, colorscale=palette.lower(), opacity=torus_op, showscale=False, hoverinfo="skip"))

# Primary vortex
fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z, mode="lines", line=dict(color=c_line, colorscale=palette.lower(), width=6), name="Expanding (+)"))

# Dual counter vortex
if show_dual:
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z2, mode="lines", line=dict(color=c_line, colorscale="ice", width=4, dash="dot"), name="Converging (-)"))

# Discrete nodes
h_text = [f"n: {i}<br>Val: {raw_seq[i]}<br>Mod: {mod_seq[i]}<br>Root9: {dig_roots[i]}<br>Parity: {parity_seq[i]}" for i in range(seq_length)]
fig.add_trace(go.Scatter3d(
    x=x1[idx_nodes], y=y1[idx_nodes], z=z[idx_nodes],
    mode="markers", text=h_text, hoverinfo="text",
    marker=dict(size=[5 + (dr % 9) * 1.3 for dr in dig_roots], color=mod_seq, colorscale=palette.lower(), opacity=1.0, line=dict(color="#fff", width=1)),
    name="Nodes"
))

fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=10), template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), camera=dict(eye=dict(x=1.7, y=1.7, z=1.3))),
    legend=dict(orientation="h", y=0.02, x=0.5, xanchor="center")
)

st.plotly_chart(fig, use_container_width=True)

# Ledger & export
with st.expander("⚡ DECRYPTED SPECTRAL LEDGER", expanded=False):
    df = pd.DataFrame({"n": range(seq_length), "Term": [str(x) for x in raw_seq], "Mod": mod_seq, "Root9": dig_roots, "Parity": parity_seq})
    st.dataframe(df, use_container_width=True, height=260)
    st.download_button("Export Telemetry (CSV)", data=df.to_csv(index=False).encode(), file_name=f"rOtOr_k{k_order}.csv", mime="text/csv")

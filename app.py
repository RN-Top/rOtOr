import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
st.set_page_config(
page_title="NeFibonacci",
page_icon="🌌",
layout="wide",
initial_sidebar_state="expanded"
)
Dark radiant theme styling
st.markdown("""
<style>
.stApp {
background: radial-gradient(circle at 50% 20%, #15002b 0%, #080811 70%, #000000 100%);
color: #f3f4f6;
}
.metric-card {
background: rgba(255, 255, 255, 0.04);
border: 1px solid rgba(168, 85, 247, 0.25);
border-radius: 12px;
padding: 16px;
margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)
st.title("🌌 NeFibonacci")
st.caption("Generalized N-step Fibonacci Engine & Radiant 3D Visualizer")
Sidebar parameter controls
with st.sidebar:
st.header("Parameters")
order = st.slider("Order (k-step recurrence)", min_value=2, max_value=6, value=2,
help="2 = Classical Fibonacci, 3 = Tribonacci, 4 = Tetranacci")
length = st.slider("Sequence Length", min_value=10, max_value=120, value=35)
modulo_val = st.number_input("Pisano / Modulo Cycle", min_value=2, max_value=32, value=9)
colorscale = st.selectbox("Color Theme", ["Plasma", "Viridis", "Turbo", "Electric", "Inferno"])
st.markdown("---")
show_raw = st.checkbox("Show Data Table", value=False)
def calculate_ne_fibonacci(k: int, n: int) -> list:
"""Computes generalized k-step Fibonacci sequence."""
if n <= 0:
return []
if k < 2:
return [0] * n
seq = [0] * n
if n > 1:
seq[1] = 1
for i in range(2, min(k, n)):
seq[i] = 2  (i - 1)
for i in range(k, n):
seq[i] = sum(seq[i - k:i])
return seq
Calculate sequence
values = calculate_ne_fibonacci(order, length)
indices = list(range(length))
df = pd.DataFrame({"Index": indices, "Value": values})
df["Binary_Parity"] = df["Value"] % 2
df["Mod_Cycle"] = df["Value"] % modulo_val
Layout columns
col_left, col_right = st.columns([1, 2])
with col_left:
st.markdown("### Sequence Overview")
st.markdown(f"""
<div class="metric-card">
<strong>Current Order:</strong> {order}-step

<strong>Length:</strong> {length} terms

<strong>Max Value:</strong> {df['Value'].iloc[-1]:,}

<strong>Parity Distribution (0/1):</strong> {sum(df['Binary_Parity'] == 0)} / {sum(df['Binary_Parity'] == 1)}
</div>
""", unsafe_allow_html=True)
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
label="Download Sequence CSV",
data=csv_data,
file_name=f"ne_fibonacci_order_{order}len{length}.csv",
mime="text/csv"
)
if show_raw:
st.dataframe(df, use_container_width=True)
with col_right:
# Parametric 3D mapping
t = np.linspace(0, 4 * np.pi * (order / 2), length)
# Scaled logarithmic growth to prevent extreme out-of-bounds distortion
log_scale = np.log1p(df["Value"])
x = log_scale * np.cos(t)
y = log_scale * np.sin(t)
z = np.array(indices)
fig = go.Figure()
# 3D Radiant path trace
fig.add_trace(go.Scatter3d(
x=x, y=y, z=z,
mode="lines+markers",
line=dict(
color=df["Mod_Cycle"],
colorscale=colorscale,
width=6
),
marker=dict(
size=6,
color=df["Mod_Cycle"],
colorscale=colorscale,
opacity=0.9
),
text=[f"Index: {i}
Val: {v:,}
Mod {modulo_val}: {m}" for i, v, m in zip(indices, values, df["Mod_Cycle"])],
hoverinfo="text",
name="NeFibonacci Curve"
))
fig.update_layout(
template="plotly_dark",
margin=dict(l=0, r=0, b=0, t=20),
scene=dict(
xaxis=dict(showbackground=False, showgrid=True, gridcolor="#27272a", zerolinecolor="#3f3f46"),
yaxis=dict(showbackground=False, showgrid=True, gridcolor="#27272a", zerolinecolor="#3f3f46"),
zaxis=dict(showbackground=False, showgrid=True, gridcolor="#27272a", zerolinecolor="#3f3f46", title="Index (Step)"),
camera=dict(eye=dict(x=1.6, y=1.6, z=1.2))
),
paper_bgcolor="rgba(0,0,0,0)",
plot_bgcolor="rgba(0,0,0,0)",
height=620
)
st.plotly_chart(fig, use_container_width=True)
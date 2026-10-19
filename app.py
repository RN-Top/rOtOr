import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="NeFibonacci",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom Aesthetic Styles
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% 15%, #180033 0%, #0a0b12 65%, #020205 100%);
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .metric-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(192, 132, 252, 0.2);
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #e879f9;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header
st.title("✨ NeFibonacci")
st.markdown("*Generalized N-step Fibonacci Engine & Radiant 3D Visualizer*")

# 4. Sidebar Controls
with st.sidebar:
    st.header("⚙️ Sequence Settings")
    order = st.slider(
        "Recurrence Order (k)",
        min_value=2,
        max_value=6,
        value=2,
        help="2 = Classical Fibonacci, 3 = Tribonacci, 4 = Tetranacci"
    )
    length = st.slider(
        "Sequence Length",
        min_value=8,
        max_value=100,
        value=32
    )
    modulo_val = st.number_input(
        "Pisano / Modulo Cycle",
        min_value=2,
        max_value=32,
        value=9,
        step=1
    )
    colorscale = st.selectbox(
        "Color Radiance",
        ["Plasma", "Turbo", "Viridis", "Electric", "Inferno", "Magenta"]
    )
    st.markdown("---")
    show_table = st.checkbox("Show Data Table", value=False)

# 5. Core Mathematical Generator
def compute_generalized_fibonacci(k: int, n: int) -> list:
    """Computes generalized k-step Fibonacci sequence safely."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    seq = [0] * n
    seq[1] = 1
    
    # Initialize initial base states up to order k
    for i in range(2, min(k, n)):
        seq[i] = 2 ** (i - 1)
        
    # Generalized recursive sliding sum
    for i in range(k, n):
        seq[i] = sum(seq[i - k:i])
        
    return seq

# Generate sequence data
raw_vals = compute_generalized_fibonacci(order, length)
indices = list(range(length))

df = pd.DataFrame({
    "Index": indices,
    "Value": raw_vals
})

df["Binary_Parity"] = df["Value"] % 2
df["Mod_Cycle"] = df["Value"] % modulo_val

# 6. Primary Display Layout
col_stats, col_viz = st.columns([1, 2])

with col_stats:
    st.subheader("Sequence Metrics")
    
    latest_val = df["Value"].iloc[-1]
    str_val = f"{latest_val:,}" if latest_val < 10**15 else f"{latest_val:.3e}"
    
    st.markdown(f"""
    <div class="metric-container">
        <div><strong>Recurrence:</strong> {order}-step</div>
        <div><strong>Total Terms:</strong> {length}</div>
        <div><strong>Final Term:</strong> <span class="metric-value">{str_val}</span></div>
        <div><strong>Binary Parity:</strong> {int((df['Binary_Parity'] == 0).sum())} Even / {int((df['Binary_Parity'] == 1).sum())} Odd</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Export CSV Option
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Data (CSV)",
        data=csv_bytes,
        file_name=f"nefibonacci_k{order}_n{length}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    if show_table:
        st.dataframe(df, use_container_width=True, height=300)

with col_viz:
    st.subheader("Radiant 3D Spiral")
    
    # Logarithmic scaling to keep high orders within visual bounds
    scaled_radii = np.log1p(df["Value"].astype(float).values)
    
    # Golden-ratio based angular evolution
    phi = (1 + np.sqrt(5)) / 2
    theta = np.linspace(0, 2 * np.pi * phi * (order / 1.5), length)
    
    x_coords = scaled_radii * np.cos(theta)
    y_coords = scaled_radii * np.sin(theta)
    z_coords = np.array(indices)
    
    # Construct 3D plot
    fig = go.Figure()
    
    # 3D line & marker trace
    fig.add_trace(go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode="lines+markers",
        line=dict(
            color=df["Mod_Cycle"],
            colorscale=colorscale,
            width=7
        ),
        marker=dict(
            size=6,
            color=df["Mod_Cycle"],
            colorscale=colorscale,
            opacity=0.9
        ),
        text=[
            f"Step: {i}<br>Val: {v:,}<br>Mod {modulo_val}: {m}<br>Parity: {b}"
            for i, v, m, b in zip(df["Index"], df["Value"], df["Mod_Cycle"], df["Binary_Parity"])
        ],
        hoverinfo="text",
        name="NeFibonacci"
    ))
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=10),
        height=580,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(showbackground=False, gridcolor="#27272a", zerolinecolor="#3f3f46", title="X"),
            yaxis=dict(showbackground=False, gridcolor="#27272a", zerolinecolor="#3f3f46", title="Y"),
            zaxis=dict(showbackground=False, gridcolor="#27272a", zerolinecolor="#3f3f46", title="Index (Z)"),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Configuration & Cyber Aesthetic
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="rOtOr // Dual-Vortex Toroidal Manifold",
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
        font-size: 2.2rem;
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

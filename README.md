# NeFibonacci 🌌

An interactive mathematical engine and 3D manifold visualizer built in Python and Streamlit. **NeFibonacci** computes generalized higher-order Fibonacci recurrences, maps their modular harmonic residue cycles (Pisano periods and binary parity pulses), and renders them in an interactive 3D coordinate space embedded within a parametric toroidal field (Crea-Torus).

---

## ⚡ Core Features

- **Generalized $k$-Step Recurrence**: Explore Fibonacci ($k=2$), Tribonacci ($k=3$), Tetranacci ($k=4$), and beyond with arbitrary-precision integer calculation.
- **Harmonic Modulo Reductions**:
  - **Binary Parity (Mod 2)**: Visualizes fundamental on/off bit sequences along the growth spiral.
  - **Digital Roots (Mod 9)**: Unlocks repeating Pisano harmonic patterns.
- **Radiant 3D Manifold Visualizer**:
  - Real-time Plotly WebGL engine with dark-field rendering.
  - Interactive multi-touch 3D rotation, pan, and zoom designed for desktop and mobile.
  - Parametric **Crea-Torus** surface overlay with adjustable mesh opacity.
  - Dynamic radiance colormaps (`Plasma`, `Viridis`, `Electric`, `Inferno`, `Turbo`, `Rainbow`).
- **Harmonic Ledger & CSV Export**: Inspect index terms, modulo residues, and growth ratios, or export full calculation datasets directly to CSV.

---

## 📐 Mathematical Formulation

### Generalized Fibonacci ($k$-Order)
Given an order $k \ge 2$, the sequence is defined recursively as:

$$F_n^{(k)} = \sum_{j=1}^{k} F_{n-j}^{(k)}$$

with seed values:

$$F_0^{(k)} = 0, \quad \dots, \quad F_{k-2}^{(k)} = 0, \quad F_{k-1}^{(k)} = 1$$

### Toroidal Manifold Coordinates
The parametric Crea-Torus envelope is computed across angular coordinates $u, v \in [0, 2\pi]$:

$$x = (R + r \cos v) \cos u$$
$$y = (R + r \cos v) \sin u$$
$$z = r \sin v$$

Where $R = 3.2$ represents the major radius and $r = 1.6$ represents the minor tube radius.

---

## 🚀 Local Installation & Execution

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/neFibonacci.git](https://github.com/your-username/neFibonacci.git)
   cd neFibonacci

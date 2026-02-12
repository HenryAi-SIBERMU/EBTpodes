import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.utils.data_loader import load_national_data, load_provincial_data, format_number, calculate_growth_color
from src.components.sidebar import render_sidebar

# --- Page Config ---
st.set_page_config(
    page_title="Analisis Tren EBT (2021-2024) — CELIOS",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

render_sidebar()

# --- Load Data ---
df_nas = load_national_data()
df_prov = load_provincial_data()

st.title("📉 Analisis Tren & Pertumbuhan EBT (2021 vs 2024)")
st.markdown("""
Halaman ini menganalisis **laju pertumbuhan (Growth Rate)** dari berbagai indikator EBT dan akses energi.
Data dibandingkan antara **PODES 2021** dan **PODES 2024**.
""")

# --- Define Metrics ---
# Mapping readable name -> (col_prefix, label)
METRICS = {
    "PJU Tenaga Surya": ("R502a_pju_surya", "Unit Desa"),
    "Energi Surya (RT)": ("R501c_keluarga_surya", "Keluarga"),
    "Bioenergi (Biogas)": ("R503a6_bioenergi", "Unit/Keluarga"),
    "Energi Air (Sungai/Mikrohidro)": ("R510_air", "Unit Desa"),
    "Keluarga Tanpa Listrik": ("R501b_tanpa_listrik", "Keluarga"),
    "Keluarga Non-PLN": ("R501a2_non_pln", "Keluarga"),
    "Pencemaran Air": ("R514_polusi_air", "Desa Terdampak"),
}

# --- SECTION 1: NATIONAL OVERVIEW (KPI CARDS) ---
st.subheader("1. Overview Tren Nasional")

if not df_nas.empty:
    cols = st.columns(len(METRICS))
    # Filter columns to max 4 per row for layout
    col_batches = [list(METRICS.items())[i:i+4] for i in range(0, len(METRICS), 4)]
    
    for batch in col_batches:
        cols = st.columns(4)
        for i, (label, (prefix, unit)) in enumerate(batch):
            with cols[i]:
                # Get data
                col_2024 = f"{prefix}_2024"
                col_growth = f"{prefix}_growth"
                
                if col_2024 in df_nas.columns and col_growth in df_nas.columns:
                    val_2024 = df_nas[col_2024].iloc[0]
                    growth = df_nas[col_growth].iloc[0]
                else:
                    val_2024 = 0
                    growth = 0
                
                # Wrapper for styling using metrics
                st.metric(
                    label=label,
                    value=f"{format_number(val_2024)}",
                    delta=f"{growth}%",
                    delta_color="normal" if "Tanpa Listrik" not in label and "Pencemaran" not in label and "Non-PLN" not in label else "inverse"
                )
else:
    st.error("Data Nasional tidak ditemukan.")

st.divider()

# --- SECTION 2: PROVINCIAL DEEP DIVE (SLOPE/DIVERGING BAR) ---
st.subheader("2. Deep Dive: Pertumbuhan per Provinsi")

# Selector
target_metric_label = st.selectbox("Pilih Indikator untuk Analisis Provinsi:", list(METRICS.keys()))
target_prefix = METRICS[target_metric_label][0]
unit_label = METRICS[target_metric_label][1]

# Prepare Data
col_growth_prov = f"{target_prefix}_growth"
col_val_prov_2024 = f"{target_prefix}_2024"

if col_growth_prov in df_prov.columns:
    df_chart = df_prov[["Provinsi", col_growth_prov, col_val_prov_2024]].copy()
    
    # Sort by Growth
    df_chart = df_chart.sort_values(col_growth_prov, ascending=True) # Ascending for BarH (bottom to top)
    
    # Classification logic for coloring
    def categorize_growth(x):
        if x > 20: return "Booming (>20%)"
        if x > 5: return "Growing (5-20%)"
        if x >= -5: return "Stagnant (-5 to 5%)"
        if x >= -20: return "Declining (-20 to -5%)"
        return "Collapsing (<-20%)"
    
    df_chart["Category"] = df_chart[col_growth_prov].apply(categorize_growth)
    
    # Color map
    color_map = {
        "Booming (>20%)": "#1a936f", # Green
        "Growing (5-20%)": "#88d498", # Light Green
        "Stagnant (-5 to 5%)": "#f3e1b6", # Neutral
        "Declining (-20 to -5%)": "#f4a261", # Orange
        "Collapsing (<-20%)": "#e76f51" # Red
    }

    # Handle Inverse Logic for "Bad" metrics (Tanpa Listrik, Polusi)
    is_inverse = target_metric_label in ["Keluarga Tanpa Listrik", "Keluarga Non-PLN", "Pencemaran Air"]
    if is_inverse:
        # Swap colors for visual intuition: Decrease (Negative) is GOOD (Green)
        color_map = {
            "Booming (>20%)": "#e76f51", # Red (Bad increase)
            "Growing (5-20%)": "#f4a261",
            "Stagnant (-5 to 5%)": "#f3e1b6",
            "Declining (-20 to -5%)": "#88d498",
            "Collapsing (<-20%)": "#1a936f" # Green (Good decrease)
        }

    # Plot
    fig = px.bar(
        df_chart,
        x=col_growth_prov,
        y="Provinsi",
        color="Category",
        color_discrete_map=color_map,
        orientation='h',
        text=col_growth_prov,
        hover_data={col_val_prov_2024: True, col_growth_prov: True, "Category": False},
        title=f"Laju Pertumbuhan {target_metric_label} (2021-2024)",
        height=800
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(xaxis_title="Growth Rate (%)", yaxis_title="")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown(f"### 💡 Insight: {target_metric_label}")
        
        # Calculate Stats
        top_grower = df_chart.iloc[-1]
        btm_grower = df_chart.iloc[0]
        
        avg_growth = df_chart[col_growth_prov].mean()
        
        st.info(f"""
        **Rata-rata Nasional (Provinsi):** {avg_growth:.2f}%
        
        🚀 **Pertumbuhan Tertinggi:**
        **{top_grower['Provinsi']}** ({top_grower[col_growth_prov]}%)
        
        📉 **Penurunan Terdalam:**
        **{btm_grower['Provinsi']}** ({btm_grower[col_growth_prov]}%)
        """)
        
        # Add context based on logic
        if is_inverse:
            st.warning("⚠️ **Catatan:** Untuk indikator ini, nilai Negatif (-) berarti **BAIK** (Pengurangan masalah), sedangkan Positif (+) berarti **BURUK** (Masalah bertambah).")
        else:
            st.success("✅ **Catatan:** Nilai Positif (+) menunjukkan **Kemajuan/Adopsi**, Negatif (-) menunjukkan **Penurunan/Disupsi**.")

else:
    st.warning(f"Data pertumbuhan untuk {target_metric_label} tidak tersedia di dataset provinsi.")

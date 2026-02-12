import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
import sys, os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.utils.data_loader import load_provincial_data, format_number

# --- Page Config ---
st.set_page_config(
    page_title="Eksplorasi Data — CELIOS EBT",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

render_sidebar()

# --- Load Data ---
df = load_provincial_data()

st.title("📊 Eksplorasi Data & Validasi Statistik")
st.markdown("""
<div style="background-color:#1E1E1E; padding:15px; border-radius:10px; border-left: 5px solid #2196F3; margin-bottom: 20px;">
    <strong>Fitur Analisis Statistik:</strong><br>
    Halaman ini difokuskan untuk <b>pengujian hipotesis (Correlation)</b> dan eksplorasi data mentah. 
    Untuk Analisis Tren (Kenaikan/Penurunan), silakan lihat di <b>Page 3 (Gap Potensi)</b>.
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.error("Data provinsi tidak ditemukan. Silakan cek pipeline data.")
    st.stop()

# Mapping for Correlation (Using Percentage Columns to normalize)
VARS_CORR = {
    "Desa Tambang (%)": "tambang_2024_pct",
    "Pencemaran Air (%)": "R514_polusi_air_2024_pct",
    "Program EBT (%)": "R1504a_program_ebt_2024_pct",
    "Tanpa Listrik (%)": "R501b_tanpa_listrik_2024_pct",
    "Surya RT (%)": "R501c_keluarga_surya_2024_pct",
    "Realisasi Air (%)": "R510_air_2024_pct",
    "Infrastruktur Energi (%)": "R1503a_infra_2024_pct"
}

# --- TABS ---
# Removed Trend Tab
tab1, tab2 = st.tabs(["🔗 Uji Korelasi & Hipotesis", "📋 Data Mentah"])

# ==============================================================================
# TAB 1: CORRELATION ANALYSIS (Formerly Tab 2)
# ==============================================================================
with tab1:
    st.markdown("### 🔗 Uji Korelasi Spearman Rank (Non-Parametrik)")
    st.info("Metode Spearman dipilih karena data tidak terdistribusi normal dan berbentuk ranking/persentase. Nilai p-value < 0.05 menunjukkan korelasi signifikan.")
    
    # 1. Hypothesis Testing Cards (Fixed List from Strategy)
    st.subheader("1. Pengujian Hipotesis Utama")
    
    hypotheses = [
        {
            "id": 1,
            "name": "🚨 Dampak Ekstraktif (Tambang vs Polusi)",
            "x": "Desa Tambang (%)", "y": "Pencemaran Air (%)",
            "exp": "Positif (+)", 
            "citation": "Setiawan et al. (2022); Arifin (2020)",
            "desc": "Menguji fakta lapangan: apakah desa tambang identik dengan kerusakan ekologis (pencemaran air)?"
        },
        {
            "id": 2,
            "name": "📉 Resource Curse: Paradoks Tambang",
            "x": "Desa Tambang (%)", "y": "Program EBT (%)",
            "exp": "Negatif (-)", 
            "citation": "Resosudarmo et al. (2014)",
            "desc": "Menguji tesis 'Paradox of Plenty': apakah dominasi ekonomi kotor menghambat transisi energi hijau?"
        },
        {
            "id": 3,
            "name": "☀️ Harapan Miskin Energi (Surya vs Tanpa Listrik)",
            "x": "Tanpa Listrik (%)", "y": "Surya RT (%)",
            "exp": "Positif (+)", 
            "citation": "IESR (2019); Blum et al. (2013)",
            "desc": "Membuktikan peran vital energi surya bagi rakyat miskin yang diabaikan jaringan listrik pusat (PLN)."
        },
        {
            "id": 4,
            "name": "🏛️ Efektivitas Intervensi Negara",
            "x": "Program EBT (%)", "y": "Realisasi Air (%)",
            "exp": "Positif (+)", 
            "citation": "-",
            "desc": "Mengukur apakah retorika program pemerintah benar-benar menetes menjadi realisasi fisik di lapangan."
        }
    ]
    
    cols_hyp = st.columns(2)
    
    for i, h in enumerate(hypotheses):
        col_idx = i % 2
        with cols_hyp[col_idx]:
            # Calculate Correlation
            x_col = VARS_CORR[h["x"]]
            y_col = VARS_CORR[h["y"]]
            
            # Drop NA for calculation
            clean_df = df[[x_col, y_col]].dropna()
            
            if not clean_df.empty:
                coef, p_val = stats.spearmanr(clean_df[x_col], clean_df[y_col])
                
                # Determine Result
                is_significant = p_val < 0.05
                direction = "Positif" if coef > 0 else "Negatif"
                match_exp = (direction[0] == h["exp"][0]) # Check logic P vs P or N vs N
                
                border_color = "#4CAF50" if is_significant else "#757575"
                sig_label = "✅ Signifikan" if is_significant else "❌ Tidak Signifikan"
                
                st.markdown(f"""
                <div style="border:1px solid #333; padding:15px; border-radius:10px; margin-bottom:15px; background-color: #262730;">
                    <h4 style="margin:0; color:#DDD;">{h['name']}</h4>
                    <p style="font-size:0.9em; color:#AAA; margin-bottom:10px;">{h['desc']}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:1.5em; font-weight:bold; color:{border_color};">r = {coef:.2f}</div>
                            <div style="font-size:0.8em;">p-value = {p_val:.4f}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="background:{border_color}; color:white; padding:4px 8px; border-radius:4px; font-size:0.8em;">{sig_label}</span><br>
                            <span style="font-size:0.8em; color:#AAA;">Hipotesis: {h['exp']}</span>
                        </div>
                    </div>
                    <div style="margin-top:10px; font-size:0.8em; color:#888; border-top:1px solid #444; padding-top:5px;">
                        📚 Ref: {h['citation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 2. Exploratory Heatmap & Scatter
    st.markdown("---")
    st.subheader("2. Eksplorasi Matriks Korelasi Full")
    
    # Select columns
    corr_cols_names = list(VARS_CORR.keys())
    corr_cols_keys = list(VARS_CORR.values())
    
    corr_df = df[corr_cols_keys].rename(columns={v: k for k, v in VARS_CORR.items()}).dropna()
    
    # Heatmap
    corr_matrix = corr_df.corr(method='spearman')
    
    fig_corr = px.imshow(
        corr_matrix, 
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        range_color=[-1, 1],
        title="Matriks Korelasi Spearman"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Interactive Scatter
    st.subheader("3. Scatter Plot Interaktif")
    sc1, sc2 = st.columns(2)
    x_axis = sc1.selectbox("Sumbu X", corr_cols_names, index=0)
    y_axis = sc2.selectbox("Sumbu Y", corr_cols_names, index=1)
    
    fig_scatter = px.scatter(
        df, 
        x=VARS_CORR[x_axis], 
        y=VARS_CORR[y_axis], 
        hover_name="Provinsi",
        trendline="ols", # Just for visual lines, stats above is Spearman
        labels={VARS_CORR[x_axis]: x_axis, VARS_CORR[y_axis]: y_axis},
        title=f"Hubungan: {x_axis} vs {y_axis}"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ==============================================================================
# TAB 2: RAW DATA (Formerly Tab 3)
# ==============================================================================
with tab2:
    st.subheader("Data Mentah (Agregat Provinsi)")
    st.dataframe(df, use_container_width=True)
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CSV",
        csv,
        "data_ebt_provinsi_celios.csv",
        "text/csv",
        key='download-csv'
    )

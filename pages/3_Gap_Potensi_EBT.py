import streamlit as st
import pandas as pd
import altair as alt
import sys, os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.components.sidebar import render_sidebar
from src.utils.data_loader import load_provincial_data, format_number

# --- Page Config ---
st.set_page_config(
    page_title="Analisis Gap Potensi EBT — CELIOS",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

# --- Sidebar ---
render_sidebar()

# --- Load Data ---
df = load_provincial_data()

# --- Main Content ---
# --- Main Content ---
st.markdown("""
<style>
.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0px;
}
.sub-title {
    font-size: 1.1rem;
    color: #66BB6A;
    font-weight: 500;
    margin-top: -15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Gap Potensi vs Realisasi</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Analisis disparitas antara ketersediaan sumber daya alam dan realisasi pemanfaatan EBT</p>', unsafe_allow_html=True)

if df.empty:
    st.error("Data provinsi tidak ditemukan. Pastikan pipeline pemrosesan data sudah dijalankan.")
    st.stop()

# --- Methodology Section ---
with st.expander("ℹ️ Metodologi: Analisis Gap & Inefisiensi", expanded=False):
    st.markdown("""
    **Metode Analisis:**
    Analisis ini menggunakan **Gap Ratio** dan **Ranking Efisiensi** untuk mengukur disparitas pemanfaatan energi terbarukan di tingkat provinsi.
    
    1.  **Formula Gap**: Menghitung selisih antara total desa yang memiliki potensi sumber daya alam dengan desa yang telah memiliki infrastruktur (Realisasi).
        *   `Gap = Potensi - Realisasi`
    
    2.  **Formula Efisiensi**: Mengukur persentase desa yang memanfaatkan potensi EBT yang ada.
        *   `Efisiensi = (Realisasi / Potensi) x 100%`
    
    3.  **Ranking**: Provinsi diurutkan berdasarkan rasio efisiensi terendah ke tertinggi.
        *   Provinsi dengan **ranking terendah (Gap terbesar)** diutamakan karena memiliki potensi besar yang "terbuang" sia-sia.
    """)

# --- 3.1 Control Panel ---
st.markdown("---")
col_ctrl1, col_ctrl2 = st.columns([1, 2])

with col_ctrl1:
    st.subheader("⚙️ Konfigurasi")
    energy_type = st.selectbox(
        "Pilih Jenis Energi:",
        ["Energi Air (Hydro)", "Energi Surya (Solar)"],
        index=0
    )

# --- Logic Calculation ---
# 1. Define Columns & Labels based on Selection
if energy_type == "Energi Air (Hydro)":
    # Priority: R511 (Table 2 Specific) > R1403g (General Asset)
    col_potensi = "R511_potensi_air_2024" if "R511_potensi_air_2024" in df.columns else "R1403g_potensi_air_2024"
    col_realisasi = "R510_air_2024"
    
    label_potensi = "Jumlah Desa Memiliki Potensi Sumber Daya Air"
    label_realisasi = "Jumlah Desa Memiliki Pembangkit Listrik (PLTA/Mikro/Pico)"
    
    color_range = ["#CFD8DC", "#4CAF50"] # Grey (Gap) vs Green (Realized)
    highlight_color = "#4CAF50"
    
elif energy_type == "Energi Surya (Solar)":
    # Solar Potential = Theoretical Maximum (Total Desa)
    col_realisasi = "R502a_pju_surya_2024"
    col_total = "R502a_pju_surya_2024_total"
    col_potensi = "potensi_surya_calc"
    
    # Calculate Potential assuming all villages have solar potential
    df[col_potensi] = df[col_total]
    
    label_potensi = "Total Desa (Potensi Teoritis)"
    label_realisasi = "Jumlah Desa Memiliki PJU Tenaga Surya"
    
    color_range = ["#FFE0B2", "#FB8C00"] # Light Orange (Gap) vs Deep Orange (Realized)
    highlight_color = "#FB8C00"

# 2. Data Preparation
# Convert to numeric to avoid errors
df[col_potensi] = pd.to_numeric(df[col_potensi], errors='coerce').fillna(0)
df[col_realisasi] = pd.to_numeric(df[col_realisasi], errors='coerce').fillna(0)

# Calculate Gap
# Gap = Potensi - Realisasi
df["Gap_Value"] = df[col_potensi] - df[col_realisasi]
df["Gap_Value"] = df["Gap_Value"].clip(lower=0) # Ensure non-negative

# Calculate Utilization Ratio
df["Util_Ratio"] = (df[col_realisasi] / df[col_potensi].replace(0, 1)) * 100

# Sort for Visualization (Show Biggest Gap/Unused Potential first)
df_sorted = df.sort_values("Gap_Value", ascending=False).head(10).reset_index(drop=True)

# 3. National Summary Stats
total_potensi = df[col_potensi].sum()
total_realisasi = df[col_realisasi].sum()
national_ratio = (total_realisasi / total_potensi * 100) if total_potensi > 0 else 0

with col_ctrl2:
    st.markdown("##### Ringkasan Nasional")
    m1, m2, m3 = st.columns(3)
    
    # CSS for Cards
    st.markdown("""
    <style>
    .metric-card {
        background: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        height: 100%;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #AAA;
    }
    .metric-unit {
        font-size: 0.75rem;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Potensi</div>
            <div class="metric-value" style="color: #E0E0E0;">{format_number(total_potensi)}</div>
            <div class="metric-unit">Desa</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Realisasi</div>
            <div class="metric-value" style="color: {highlight_color};">{format_number(total_realisasi)}</div>
            <div class="metric-unit">Desa</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card" style="border-bottom: 2px solid {highlight_color};">
            <div class="metric-label">Rasio Pemanfaatan</div>
            <div class="metric-value" style="color: #FFC107;">{national_ratio:.2f}%</div>
            <div class="metric-unit">Efficiency Rate</div>
        </div>
        """, unsafe_allow_html=True)

# --- 3.1 Visualization (Butterfly/Diverging Bar) ---
st.markdown("---")
st.subheader(f"3.1 Top 10 Provinsi dengan Disparitas Terbesar")
st.caption("Grafik menunjukkan besarnya **Potensi yang Belum Dimanfaatkan** (Kiri/Abu-abu) dibandingkan **Realisasi** (Kanan/Berwarna).")

# Prepare Data for Altair
viz_df = df_sorted[["Provinsi", "Gap_Value", col_realisasi, "Util_Ratio"]].copy()
viz_df = viz_df.rename(columns={"Gap_Value": "Belum Dimanfaatkan", col_realisasi: "Sudah Dimanfaatkan"})

# Melt
viz_melted = viz_df.melt(id_vars=["Provinsi", "Util_Ratio"], value_vars=["Belum Dimanfaatkan", "Sudah Dimanfaatkan"], var_name="Status", value_name="Jumlah")

# Calculate Display Value (Negative for Gap to align Left)
viz_melted["Display_Value"] = viz_melted.apply(lambda x: -x["Jumlah"] if x["Status"] == "Belum Dimanfaatkan" else x["Jumlah"], axis=1)

# Base Chart
base = alt.Chart(viz_melted).encode(
    y=alt.Y("Provinsi", sort=None, axis=alt.Axis(title=None, labelFontWeight='bold')),
    x=alt.X("Display_Value", title="Jumlah Desa", axis=alt.Axis(format="s")), # 's' for SI units (k, M)
    color=alt.Color("Status", scale=alt.Scale(domain=["Belum Dimanfaatkan", "Sudah Dimanfaatkan"], range=color_range), legend=alt.Legend(orient="top")),
    tooltip=["Provinsi", "Status", alt.Tooltip("Jumlah", format=",d")]
)

# Bars
bars = base.mark_bar().properties(height=400)

# Text Labels (Numbers inside bars)
text = base.mark_text(
    align='center',
    baseline='middle',
    dx=alt.expr("datum.Display_Value > 0 ? 20 : -20"), # Offset text slightly
    color='white'
).encode(
    text=alt.Text("Jumlah", format=",") # Show raw number
)

st.altair_chart(bars + text, use_container_width=True)

# --- Detail Data View (Default Expanded) ---
with st.expander("📂 Lihat Data Lengkap (Semua Provinsi)", expanded=True):
    # Show standardized table
    table_df = df[["Provinsi", col_potensi, col_realisasi, "Util_Ratio", "Gap_Value"]].sort_values("Util_Ratio")
    
    st.dataframe(
        table_df.style.format({
            col_potensi: "{:,.0f}",
            col_realisasi: "{:,.0f}",
            "Util_Ratio": "{:.2f}%",
            "Gap_Value": "{:,.0f}"
        }).background_gradient(subset=["Util_Ratio"], cmap="RdYlGn"),
        use_container_width=True
    )
    st.caption("*Data diurutkan berdasarkan Rasio Pemanfaatan terendah (Paling Kiri/Merah di gradien).*")

# --- 3.2 Linear Trendline Analysis (Advanced) ---
st.markdown("---")
st.subheader("3.2 Analisis Regresi: Efisiensi Pemanfaatan")
st.caption("Scatter plot ini menunjukkan provinsi yang **Under-perform** (Bawah Garis) vs **Over-perform** (Atas Garis) relatif terhadap potensi yang dimiliki.")

# Province Abbreviation Mapping (Decluttering)
prov_abbr = {
    "ACEH": "Aceh", "SUMATERA UTARA": "Sumut", "SUMATERA BARAT": "Sumbar", "RIAU": "Riau", "JAMBI": "Jambi",
    "SUMATERA SELATAN": "Sumsel", "BENGKULU": "Bengkulu", "LAMPUNG": "Lampung", "KEP. BANGKA BELITUNG": "Babel", "KEP. RIAU": "Kepri",
    "DKI JAKARTA": "DKI", "JAWA BARAT": "Jabar", "JAWA TENGAH": "Jateng", "DI YOGYAKARTA": "DIY", "JAWA TIMUR": "Jatim", "BANTEN": "Banten",
    "BALI": "Bali", "NUSA TENGGARA BARAT": "NTB", "NUSA TENGGARA TIMUR": "NTT",
    "KALIMANTAN BARAT": "Kalbar", "KALIMANTAN TENGAH": "Kalteng", "KALIMANTAN SELATAN": "Kalsel", "KALIMANTAN TIMUR": "Kaltim", "KALIMANTAN UTARA": "Kaltara",
    "SULAWESI UTARA": "Sulut", "SULAWESI TENGAH": "Sulteng", "SULAWESI SELATAN": "Sulsel", "SULAWESI TENGGARA": "Sultra", "GORONTALO": "Gorontalo", "SULAWESI BARAT": "Sulbar",
    "MALUKU": "Maluku", "MALUKU UTARA": "Malut", "PAPUA BARAT": "Pabar", "PAPUA": "Papua",
    "PAPUA SELATAN": "Papsel", "PAPUA TENGAH": "Papteng", "PAPUA PEGUNUNGAN": "Pappeg", "PAPUA BARAT DAYA": "Pabardya"
}
df["Provinsi_Abbr"] = df["Provinsi"].map(prov_abbr).fillna(df["Provinsi"])

# Scatter Plot with Regression Line
# We use symlog scale for X-axis because potential varies greatly (thousands vs tens) and to handle 0 values
# Categorization for colors
# Shorter labels to prevent legend collision
df["Status_Efisiensi"] = df["Util_Ratio"].apply(lambda x: "Efisien" if x >= national_ratio else "Inefisien")
color_scale = alt.Scale(domain=["Efisien", "Inefisien"], range=["#4CAF50", "#FF5252"])

# 1. Base Chart
base_chart = alt.Chart(df).encode(
    # Use zero=False to remove the "0 to 150" gap if data starts higher
    x=alt.X(col_potensi, title="Total Potensi (Log Scale)", scale=alt.Scale(type="symlog", zero=False)),
    y=alt.Y(col_realisasi, title="Total Realisasi (Log Scale)", scale=alt.Scale(type="symlog", zero=False)) 
)

# 2. Scatter Points
scatter_points = base_chart.mark_circle(size=120, opacity=0.8).encode(
    color=alt.Color("Status_Efisiensi", scale=color_scale, legend=alt.Legend(title="Kinerja", orient="right")),
    tooltip=["Provinsi", "Status_Efisiensi", alt.Tooltip(col_potensi, format=","), alt.Tooltip(col_realisasi, format=",")]
)

# 3. National Average Line (Threshold)
# Create a line that represents the National Average Ratio (y = k * x)
# Use dense points to ensure line renders correctly in Symlog scale (which might curve)
import numpy as np

max_pot = df[col_potensi].max()
min_pot = df[col_potensi].min()
if min_pot <= 0: min_pot = 1 # Avoid log(0) issues for line start

# Generate dense X points (log-spaced)
x_vals = np.geomspace(min_pot, max_pot, num=100)
# Calculate Y based on National Ratio (y = x * ratio)
y_vals = x_vals * (national_ratio / 100)

line_data = pd.DataFrame({
    col_potensi: x_vals,
    col_realisasi: y_vals,
    "Label": ["Rata-rata Nasional"] * len(x_vals)
})

threshold_line = alt.Chart(line_data).mark_line(color="#FFC107", strokeDash=[5,5], size=2).encode(
    x=alt.X(col_potensi),
    y=alt.Y(col_realisasi)
)

# 4. Text Labels (Short Names)
text_labels = base_chart.mark_text(
    align='left',
    baseline='middle',
    dx=8,
    fontSize=10,
    color='white'
).encode(
    text='Provinsi_Abbr'
)

# Combined Chart
final_scatter = (scatter_points + threshold_line + text_labels).properties(height=500).interactive()

# Add Annotation for Context
st.altair_chart(final_scatter, use_container_width=True)

st.info("ℹ️ **Cara Membaca:** Garis putus-putus kuning adalah 'Garis Rata-rata Nasional'. Provinsi di **bawah garis** berarti efisiensinya di bawah rata-rata nasional (Inefisien/Merah). Provinsi di **atas garis** berarti efisiensinya di atas rata-rata nasional (Efisien/Hijau).")

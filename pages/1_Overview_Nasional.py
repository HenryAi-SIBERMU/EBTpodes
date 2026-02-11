import streamlit as st
import pandas as pd
import altair as alt
import sys, os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.utils.data_loader import load_national_data, load_provincial_data, format_number, calculate_growth_color
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="Overview Nasional — CELIOS EBT", page_icon="🏠", layout="wide")
render_sidebar()

# --- Load Data ---
df_nasional = load_national_data()
df_prov = load_provincial_data()

# --- Styles ---
st.markdown("""
<style>
.metric-card {
    background: #1E1E1E;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #4CAF50;
}
.metric-label {
    font-size: 0.9rem;
    color: #AAA;
    margin-bottom: 5px;
}
.metric-delta {
    font-size: 0.8rem;
    font-weight: 600;
}
.delta-pos { color: #4CAF50; }
.delta-neg { color: #f44336; }
</style>
""", unsafe_allow_html=True)

st.title("Overview Nasional & Tren Energi Terbarukan")
st.markdown('<p style="font-size: 1.1rem; color: #66BB6A; font-weight: 500; margin-top: -15px;">Statistik Deskriptif & Analisis Tren (2021 vs 2024)</p>', unsafe_allow_html=True)

if df_nasional.empty:
    st.error("Data Nasional tidak ditemukan. Pastikan proses pipeline data berhasil.")
    st.stop()

# --- KPIs Calculation ---
# Helper to get value
def get_val(suffix, year="2024"):
    col = f"{suffix}_{year}"
    if col in df_nasional.columns:
        return df_nasional.iloc[0][col]
    return 0

def get_growth(suffix):
    col = f"{suffix}_growth"
    if col in df_nasional.columns:
        return df_nasional.iloc[0][col]
    return 0

# KPI 1: Keluarga Tanpa Listrik (R501b)
kpi1_val = get_val("R501b_tanpa_listrik")
kpi1_growth = get_growth("R501b_tanpa_listrik")

# KPI 2: Desa PJU Surya (R502a)
kpi2_val = get_val("R502a_pju_surya")
kpi2_growth = get_growth("R502a_pju_surya")

# KPI 3: Program EBT (R1504a)
# Note: Data is "Ada Program". We can show % coverage or Count.
kpi3_val = get_val("R1504a_program_ebt")
kpi3_growth = get_growth("R1504a_program_ebt") 
# Calc Pct manually for clearer display? Or use _pct col?
kpi3_pct = get_val("R1504a_program_ebt", "2024_pct") # Returns float

# KPI 4: Gap Potensi Air (R511 vs R510)
potensi_air = get_val("R511_potensi_air", "2024")
realisasi_air = get_val("R510_air", "2024")
gap_ratio = (realisasi_air / potensi_air * 100) if potensi_air > 0 else 0

# --- KPI Display ---
col1, col2, col3, col4 = st.columns(4)

def render_kpi(col, label, value, growth, unit="", is_inverse=False):
    with col:
        # Handle extreme growth values or N/A
        if abs(growth) > 1000 or growth == 0:
            growth_text = "Data Baseline 2021 Terbatas"
            growth_color = "metric-label"
            arrow = "ℹ️"
        else:
            growth_color = "delta-pos" if (growth > 0 and not is_inverse) or (growth < 0 and is_inverse) else "delta-neg"
            arrow = "▲" if growth > 0 else "▼"
            growth_text = f"{arrow} {abs(growth):.1f}% (YoY)"

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{format_number(value)} {unit}</div>
            <div class="metric-delta {growth_color}">{growth_text}</div>
        </div>
        """, unsafe_allow_html=True)

render_kpi(col1, "Keluarga Tanpa Listrik", kpi1_val, kpi1_growth, is_inverse=True)
render_kpi(col2, "Desa PJU Surya", kpi2_val, kpi2_growth)
render_kpi(col3, "Desa Ada Program EBT", kpi3_val, kpi3_growth)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Rasio Pemanfaatan Air</div>
        <div class="metric-value">{gap_ratio:.2f}%</div>
        <div class="metric-delta delta-neg">{format_number(realisasi_air)} dari {format_number(potensi_air)} Potensi</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Classify Growth ---
def classify_growth(growth):
    if growth > 20: return "Booming"
    if 5 <= growth <= 20: return "Growing"
    if -5 < growth < 5: return "Stagnant"
    if -20 <= growth <= -5: return "Declining"
    if growth < -20: return "Collapsing"
    return "Unknown"

# --- Chart: 2021 vs 2024 Comparison (Dumbbell Plot) ---
st.subheader("1.1 Perbandingan Adopsi EBT (2021 vs 2024)")

indicators = [
    {"label": "PJU Surya (R502a)", "suffix": "R502a_pju_surya"},
    {"label": "Keluarga Surya (R501c)", "suffix": "R501c_keluarga_surya"},
    {"label": "Biogas (R503a6)", "suffix": "R503a6_bioenergi"},
    {"label": "Pemanfaatan Air (R510)", "suffix": "R510_air"},
    {"label": "Program EBT (R1504a)", "suffix": "R1504a_program_ebt"},
    {"label": "Infrastruktur Energi (R1503a)", "suffix": "R1503a_infra"},
    {"label": "Mata Air (R1403g)", "suffix": "R1403g_potensi_air"},
    {"label": "Non PLN (R501a2)", "suffix": "R501a2_non_pln"},
    {"label": "Tanpa Listrik (R501b)", "suffix": "R501b_tanpa_listrik"},
    {"label": "Polusi Air (R514)", "suffix": "R514_polusi_air"},
]

# --- Chart Data Preparation with Category Split ---
def prepare_chart_data(df):
    chart_data = []
    
    # Define Categories
    household_keys = [
        'R501a2_non_pln', 
        'R501b_tanpa_listrik', 
        'R501c_keluarga_surya', 
        'R503a6_biogas' # Brief says "Keluarga"
    ]
    
    
    # Iterate all indicators and check filtering inside loop
    for item in indicators:
        key = item['suffix']
        label = item['label']
        col_24 = f"{key}_2024"
        col_21 = f"{key}_2021"

        if col_24 in df.columns and col_21 in df.columns:
            val21 = df[col_21].values[0]
            val24 = df[col_24].values[0]
            
            # Category
            category = "Skala Rumah Tangga (Unit: KK)" if key in household_keys else "Skala Wilayah / Desa (Unit: Desa)"

            chart_data.append({"Dimensi": label, "Tahun": "2021", "Jumlah": val21, "Category": category})
            chart_data.append({"Dimensi": label, "Tahun": "2024", "Jumlah": val24, "Category": category})

    return pd.DataFrame(chart_data)

df_chart = prepare_chart_data(df_nasional)

if not df_chart.empty:
    # --- Chart 1: Skala Rumah Tangga ---
    st.subheader("1. Adopsi EBT Skala Rumah Tangga (Keluarga)")
    chart_kk = alt.Chart(df_chart[df_chart['Category'] == "Skala Rumah Tangga (Unit: KK)"]).mark_bar().encode(
        x=alt.X('Jumlah', title='Jumlah Keluarga', axis=alt.Axis(format=',d')),
        y=alt.Y('Dimensi', sort='-x', title=''),
        color=alt.Color('Tahun', scale=alt.Scale(domain=['2021', '2024'], range=['#90CAF9', '#4CAF50']), legend=alt.Legend(title="Tahun")),
        yOffset='Tahun',
        tooltip=['Dimensi', 'Tahun', alt.Tooltip('Jumlah', format=',d')]
    ).properties(height=300).interactive()
    st.altair_chart(chart_kk, use_container_width=True)

    # --- Chart 2: Skala Wilayah / Desa ---
    st.subheader("2. Adopsi EBT Skala Wilayah (Desa)")
    chart_desa = alt.Chart(df_chart[df_chart['Category'] == "Skala Wilayah / Desa (Unit: Desa)"]).mark_bar().encode(
        x=alt.X('Jumlah', title='Jumlah Desa', axis=alt.Axis(format=',d')),
        y=alt.Y('Dimensi', sort='-x', title=''),
        color=alt.Color('Tahun', scale=alt.Scale(domain=['2021', '2024'], range=['#90CAF9', '#4CAF50']), legend=None),
        yOffset='Tahun',
        tooltip=['Dimensi', 'Tahun', alt.Tooltip('Jumlah', format=',d')]
    ).properties(height=400).interactive()
    st.altair_chart(chart_desa, use_container_width=True)

    # --- Section: Analisis Kritis (Keadilan Energi & Dampak Lingkungan) ---
    st.markdown("---")
    st.subheader("1.2 Analisis Kritis: Keadilan & Kedaulatan Energi")
    st.info("Bagian ini menyoroti ketimpangan energi dan risiko lingkungan yang sering terabaikan dalam narasi transisi energi arus utama.")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Provinsi dengan Kerentanan Energi Tertinggi")
        # Top 5 by Families Without Electricity
        if not df_prov.empty and 'R501b_tanpa_listrik_2024' in df_prov.columns:
            top_vulnerable = df_prov.sort_values('R501b_tanpa_listrik_2024', ascending=False).head(5)
            # Shorten labels if necessary or use code
            chart_pov = alt.Chart(top_vulnerable).mark_bar(color='#E57373', cornerRadiusEnd=5).encode(
                x=alt.X('R501b_tanpa_listrik_2024', title='Keluarga Tanpa Listrik (2024)'),
                y=alt.Y('Provinsi', sort='-x', title=''),
                tooltip=['Provinsi', alt.Tooltip('R501b_tanpa_listrik_2024', format=',d')]
            ).properties(height=300)
            st.altair_chart(chart_pov, use_container_width=True)
            st.caption("Fokus pada daerah tertinggal merupakan prioritas utama dalam upaya pemerataan energi.")

    with c2:
        st.subheader("Tren Kerentanan: Pencemaran Air Desa")
        # Pollution Trend (R514)
        if not df_nasional.empty and 'R514_polusi_air_2021' in df_nasional.columns:
            pollution_data = pd.DataFrame({
                'Tahun': ['2021', '2024'],
                'Jumlah': [get_val('R514_polusi_air', '2021'), get_val('R514_polusi_air', '2024')]
            })
            chart_pol = alt.Chart(pollution_data).mark_bar(size=60).encode(
                x=alt.X('Tahun', title=''),
                y=alt.Y('Jumlah', title='Jumlah Desa Tercemar'),
                color=alt.Color('Tahun', scale=alt.Scale(domain=['2021', '2024'], range=['#AAA', '#FF7043']), legend=None)
            ).properties(height=300)
            st.altair_chart(chart_pol, use_container_width=True)
            st.caption("Peningkatan pencemaran air di perdesaan menjadi sinyal bahaya bagi aktivitas yang mengabaikan daya dukung lingkungan.")

    st.markdown("---")
    st.subheader("Kedaulatan Energi: Potensi Mikrohidro yang Terabaikan")
    col_gap1, col_gap2 = st.columns([2, 1])

    with col_gap1:
        # Potential vs Realized Chart
        gap_data = pd.DataFrame([
            {"Label": "Realisasi Pemanfaatan", "Value": realisasi_air, "Color": "#4CAF50"},
            {"Label": "Potensi Terbuang", "Value": potensi_air - realisasi_air, "Color": "#333"}
        ])
        chart_sovereignty = alt.Chart(gap_data).mark_arc(innerRadius=60).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Label", type="nominal", scale=alt.Scale(domain=["Realisasi Pemanfaatan", "Potensi Terbuang"], range=["#4CAF50", "#333"])),
            tooltip=["Label", "Value"]
        ).properties(height=350)
        st.altair_chart(chart_sovereignty, use_container_width=True)

    with col_gap2:
        st.write("### Kesenjangan Kedaulatan")
        st.metric("Potensi Belum Terpakai", f"{format_number(potensi_air - realisasi_air)} Desa")
        st.markdown(f"""
        Rasio pemanfaatan energi air yang hanya sebesar **{gap_ratio:.2f}%** menunjukkan bahwa akses energi berbasis komunitas (lokal) masih jauh dari optimal.
        
        Transisi energi harus lebih didorong ke arah **desentralistik** yang memberdayakan potensi perdesaan, bukan hanya skala industri besar.
        """)

# --- Detailed Data Table ---
with st.expander("Lihat Data Detail (Tabel)"):
    st.dataframe(df_nasional.T, use_container_width=True)

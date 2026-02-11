import streamlit as st
import os

st.set_page_config(
    page_title="CELIOS — EBT Dashboard",
    page_icon=os.path.join(os.path.dirname(__file__), "refrensi", "Celios China-Indonesia Energy Transition.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #43A047, #66BB6A, #81C784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.2;
}

.sub-title {
    font-size: 1.1rem;
    color: #9E9E9E;
    font-weight: 300;
    margin-top: 0;
    margin-bottom: 2rem;
}

.org-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.stat-card {
    background: linear-gradient(135deg, #1A1F2B, #232B3B);
    border: 1px solid #2E7D3233;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    border-color: #43A047;
}
.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    color: #66BB6A;
    margin: 8px 0;
}
.stat-label {
    font-size: 0.85rem;
    color: #9E9E9E;
    font-weight: 400;
}
.stat-delta-up { color: #EF5350; font-size: 0.8rem; }
.stat-delta-down { color: #66BB6A; font-size: 0.8rem; }

.nav-card {
    background: linear-gradient(135deg, #1A1F2B, #232B3B);
    border: 1px solid #ffffff11;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.nav-card:hover { border-color: #43A047; }
.nav-icon { font-size: 1.6rem; margin-bottom: 8px; }
.nav-title { font-size: 1rem; font-weight: 600; color: #E0E0E0; }
.nav-desc { font-size: 0.8rem; color: #757575; margin-top: 4px; }

.footer {
    text-align: center;
    color: #616161;
    font-size: 0.75rem;
    margin-top: 4rem;
    padding: 2rem 0;
    border-top: 1px solid #ffffff0a;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar & Data Access ---
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.data_loader import load_national_data, load_provincial_data, format_number
from src.components.sidebar import render_sidebar
import pandas as pd
import altair as alt

render_sidebar()

# --- Load Data ---
df_nasional = load_national_data()
df_prov = load_provincial_data()

# --- Helpers ---
def get_val(suffix, year="2024"):
    col = f"{suffix}_{year}"
    if not df_nasional.empty and col in df_nasional.columns:
        return df_nasional.iloc[0][col]
    return 0

def get_growth(suffix):
    col = f"{suffix}_growth"
    if not df_nasional.empty and col in df_nasional.columns:
        return df_nasional.iloc[0][col]
    return 0

# Calculated Metrics for Phase 1
kpi1_val = get_val("R501b_tanpa_listrik")
kpi1_growth = get_growth("R501b_tanpa_listrik")

kpi2_val = get_val("R502a_pju_surya")
kpi2_growth = get_growth("R502a_pju_surya")

kpi3_val = get_val("R1504a_program_ebt")
kpi3_growth = get_growth("R1504a_program_ebt")
kpi3_pct = get_val("R1504a_program_ebt", "2024_pct") # Note: if exists

potensi_air = get_val("R511_potensi_air", "2024")
realisasi_air = get_val("R510_air", "2024")
gap_ratio = (realisasi_air / potensi_air * 100) if potensi_air > 0 else 0

# --- Header ---
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Energi Terbarukan Indonesia</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Dashboard Analisis Data PODES 2024 vs 2021 — 84.276 Desa, 38 Provinsi, 10 Dimensi EBT<br><span style="font-size:0.9em; opacity:0.8; font-weight:400;">Riset 3 Narasi Strategis: Desa Tambang, Gap Potensi-Realisasi, & Ketimpangan Energi. <a href="Dokumentasi_Riset" target="_self" style="color:#66BB6A; text-decoration:none;">Klik</a></span></div>', unsafe_allow_html=True)

# --- Phase 1: Overview Nasional ---
st.markdown("---")
st.header("Overview Nasional & Tren Energi Terbarukan")
st.markdown('<p style="font-size: 1rem; color: #66BB6A; font-weight: 500; margin-top: -15px;">Statistik Deskriptif & Analisis Tren (2021 vs 2024)</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    growth_text = f"▼ {abs(kpi1_growth):.1f}% (YoY)" if abs(kpi1_growth) < 1000 else "Data Baseline 2021 Terbatas"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Keluarga Tanpa Listrik</div>
        <div class="stat-number">{format_number(kpi1_val)}</div>
        <div class="stat-delta-down" style="color: {'#EF5350' if kpi1_growth > 0 else '#66BB6A'}">
            {growth_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    growth_text = f"▲ {abs(kpi2_growth):.1f}% (YoY)" if abs(kpi2_growth) < 1000 else "Data Baseline 2021 Terbatas"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Desa PJU Surya</div>
        <div class="stat-number">{format_number(kpi2_val)}</div>
        <div class="stat-delta-up">
            {growth_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    growth_text = f"▲ {abs(kpi3_growth):.1f}% (YoY)" if abs(kpi3_growth) < 1000 else "Data Baseline 2021 Terbatas"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Desa Ada Program EBT</div>
        <div class="stat-number">{format_number(kpi3_val)}</div>
        <div class="stat-delta-up">
            {growth_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Rasio Pemanfaatan Air</div>
        <div class="stat-number">{gap_ratio:.2f}%</div>
        <div class="stat-delta-down" style="color: #EF5350;">{format_number(realisasi_air)} dari {format_number(potensi_air)} Potensi</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Analysis: Trends & Comparison ---
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

def prepare_chart_data(df, indicators_list):
    chart_data = []
    household_keys = ['R501a2_non_pln', 'R501b_tanpa_listrik', 'R501c_keluarga_surya', 'R503a6_biogas']
    
    for item in indicators_list:
        key = item['suffix']
        label = item['label']
        col_24, col_21 = f"{key}_2024", f"{key}_2021"

        if col_24 in df.columns and col_21 in df.columns:
            val21, val24 = df[col_21].values[0], df[col_24].values[0]
            category = "Keluarga (Unit: KK)" if key in household_keys else "Wilayah (Unit: Desa)"
            chart_data.append({"Dimensi": label, "Tahun": "2021", "Jumlah": val21, "Category": category})
            chart_data.append({"Dimensi": label, "Tahun": "2024", "Jumlah": val24, "Category": category})
    return pd.DataFrame(chart_data)

df_chart = prepare_chart_data(df_nasional, indicators)

if not df_chart.empty:
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown("##### 🏠 Skala Rumah Tangga")
        c_kk = alt.Chart(df_chart[df_chart['Category'] == "Keluarga (Unit: KK)"]).mark_bar().encode(
            x=alt.X('Jumlah', axis=alt.Axis(format=',d')),
            y=alt.Y('Dimensi', sort='-x', title=''),
            color=alt.Color('Tahun', scale=alt.Scale(domain=['2021', '2024'], range=['#90CAF9', '#4CAF50'])),
            yOffset='Tahun',
            tooltip=['Dimensi', 'Tahun', alt.Tooltip('Jumlah', format=',d')]
        ).properties(height=250)
        st.altair_chart(c_kk, use_container_width=True)

    with chart_right:
        st.markdown("##### 📍 Skala Desa/Wilayah")
        c_desa = alt.Chart(df_chart[df_chart['Category'] == "Wilayah (Unit: Desa)"]).mark_bar().encode(
            x=alt.X('Jumlah', axis=alt.Axis(format=',d')),
            y=alt.Y('Dimensi', sort='-x', title=''),
            color=alt.Color('Tahun', scale=alt.Scale(domain=['2021', '2024'], range=['#90CAF9', '#4CAF50']), legend=None),
            yOffset='Tahun',
            tooltip=['Dimensi', 'Tahun', alt.Tooltip('Jumlah', format=',d')]
        ).properties(height=250)
        st.altair_chart(c_desa, use_container_width=True)

# --- Section: Keadilan Energi & Kedaulatan ---
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("1.2 Analisis Kritis: Keadilan & Kedaulatan Energi")
st.info("Visualisasi ini menyoroti ketimpangan akses dan potensi lokal yang sering terabaikan.")

c_crit1, c_crit2 = st.columns([1.5, 1])

with c_crit1:
    st.markdown("##### ⚠️ Kerentanan Energi per Provinsi")
    if not df_prov.empty and 'R501b_tanpa_listrik_2024' in df_prov.columns:
        top_pov = df_prov.sort_values('R501b_tanpa_listrik_2024', ascending=False).head(5)
        c_pov = alt.Chart(top_pov).mark_bar(color='#E57373', cornerRadiusEnd=4).encode(
            x=alt.X('R501b_tanpa_listrik_2024', title='Keluarga Tanpa Listrik (2024)'),
            y=alt.Y('Provinsi', sort='-x', title=''),
            tooltip=['Provinsi', alt.Tooltip('R501b_tanpa_listrik_2024', format=',d')]
        ).properties(height=250)
        st.altair_chart(c_pov, use_container_width=True)
    st.caption("Fokus pada daerah tertinggal merupakan prioritas dalam upaya pemerataan hak energi.")

with c_crit2:
    st.markdown("##### 💧 Kesenjangan Potensi Mikrohidro")
    gap_data = pd.DataFrame([
        {"Label": "Realisasi", "Value": realisasi_air},
        {"Label": "Potensi Terbuang", "Value": potensi_air - realisasi_air}
    ])
    c_gap = alt.Chart(gap_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Label", scale=alt.Scale(domain=["Realisasi", "Potensi Terbuang"], range=["#66BB6A", "#333"])),
        tooltip=["Label", "Value"]
    ).properties(height=200)
    st.altair_chart(c_gap, use_container_width=True)
    st.markdown(f"""
    Rasio pemanfaatan: **{gap_ratio:.2f}%**<br>
    <span style="font-size:0.85rem; color:#9E9E9E;">Transisi harus berbasis <b>desentralistik</b> dan memberdayakan potensi komunitas lokal.</span>
    """, unsafe_allow_html=True)

st.caption("⚠️ Hasil olah data lain sedang dalam proses")

# --- Divider ---
st.markdown("---")

# --- Navigation Cards ---
st.markdown("### Navigasi Dashboard")
st.markdown("")

analysis_items = [
    {"title": "Overview Nasional", "desc": "KPI, tren 2021→2024, ringkasan 10 dimensi", "method": "Descriptive Stats & Rate of Change (YoY)", "status": "✅ Akses Halaman", "url": "Overview_Nasional"},
    {"title": "Desa Tambang × EBT", "desc": "Crosstab desa tambang vs 10 dimensi energi terbarukan", "method": "Chi-Square Test & Cross-Tabulation", "status": "✅ Akses Halaman", "url": "Desa_Tambang"},
    {"title": "Gap Potensi EBT", "desc": "Potensi vs realisasi per provinsi, tren menurun", "method": "Gap Ratio & Efficiency Ranking", "status": "✅ Akses Halaman", "url": "Gap_Potensi_EBT"},
    {"title": "Ketimpangan Energi", "desc": "Indeks Kerentanan Energi (IKE) per provinsi", "method": "Composite Index (Weighted Sum + Min-Max)", "status": "✅ Akses Halaman", "url": "Ketimpangan_Energi"},
    {"title": "Analisis Bibliometric", "desc": "Pemetaan literatur riset EBT global", "method": "LLM-assisted Text Mining", "status": "✅ Akses Halaman", "url": "Bibliometric_Discovery"},
]

resource_items = [
    {"title": "Eksplorasi Data", "desc": "Filter interaktif, tabel, download CSV", "status": "✅ Akses Halaman", "url": "Eksplorasi_Data"},
    {"title": "Dokumentasi Riset", "desc": "Report insight, strategi narasi, metodologi", "status": "✅ Akses Halaman", "url": "Dokumentasi_Riset"},
    {"title": "Validasi Metode", "desc": "Harvesting referensi riset", "status": "✅ Akses Halaman", "url": "Validasi_Metode"},
]

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    st.markdown("##### 📂 Analisis")
    for item in analysis_items:
        st.markdown(f"""
        <a href="{item['url']}" target="_self" style="text-decoration: none; color: inherit; display: block;">
            <div class="nav-card">
                <div class="nav-title">{item['title']}</div>
                <div class="nav-desc">{item['desc']}</div>
                <div style="margin-top:8px; font-size:0.8rem; color:#66BB6A; background:#2E7D3222; display:inline-block; padding:2px 8px; border-radius:4px;">📐 {item['method']}</div>
                <div style="margin-top:8px; font-size:0.75rem; color:#E0E0E0;">{item['status']} ➔</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("##### 📚 Resources")
    for item in resource_items:
        st.markdown(f"""
        <a href="{item['url']}" target="_self" style="text-decoration: none; color: inherit; display: block;">
            <div class="nav-card">
                <div class="nav-title">{item['title']}</div>
                <div class="nav-desc">{item['desc']}</div>
                <div style="margin-top:8px; font-size:0.75rem; color:#E0E0E0;">{item['status']} ➔</div>
            </div>
        </a>
        """, unsafe_allow_html=True)



# --- Footer ---
st.markdown("""
<div class="footer">
    CELIOS EBT Dashboard — Sumber data: PODES (Potensi Desa) BPS 2024 & 2021<br>
    Disusun untuk kepentingan riset dan advokasi publik
</div>
""", unsafe_allow_html=True)

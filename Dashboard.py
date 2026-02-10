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

# --- Sidebar ---
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.components.sidebar import render_sidebar
render_sidebar()

# --- Header ---
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Energi Terbarukan Indonesia</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Dashboard Analisis Data PODES 2024 vs 2021 — 84.276 Desa, 38 Provinsi, 10 Dimensi EBT<br><span style="font-size:0.9em; opacity:0.8; font-weight:400;">Riset 3 Narasi Strategis: Desa Tambang, Gap Potensi-Realisasi, & Ketimpangan Energi. <a href="Dokumentasi_Riset" target="_self" style="color:#66BB6A; text-decoration:none;">Klik</a></span></div>', unsafe_allow_html=True)

# --- KPI Cards ---
st.markdown("### Overview Nasional")
st.markdown('<p style="font-size: 0.9em; margin-bottom: 20px;">Metode: <b>Statistik Deskriptif (Total) & Analisis Tren (YoY Growth)</b></p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Keluarga Tanpa Listrik</div>
        <div class="stat-number">658.782</div>
        <div class="stat-delta-down">▼ 33,56% dari 2021</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Desa dengan PJU Surya</div>
        <div class="stat-number">30.476</div>
        <div class="stat-delta-down">▲ 23,06% dari 2021</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Desa Punya Program EBT</div>
        <div class="stat-number">5,37%</div>
        <div class="stat-delta-up">94,63% belum punya</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Gap Potensi Air vs Realisasi</div>
        <div class="stat-number">0,86%</div>
        <div class="stat-delta-up">120.546 potensi → 1.039 realisasi</div>
    </div>
    """, unsafe_allow_html=True)

st.caption("⚠️ Hasil olah data lain sedang dalam proses")
st.markdown("<br>", unsafe_allow_html=True)

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
]

resource_items = [
    {"title": "Eksplorasi Data", "desc": "Filter interaktif, tabel, download CSV", "status": "✅ Akses Halaman", "url": "Eksplorasi_Data"},
    {"title": "Dokumentasi Riset", "desc": "Report insight, strategi narasi, metodologi", "status": "✅ Akses Halaman", "url": "Dokumentasi_Riset"},
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

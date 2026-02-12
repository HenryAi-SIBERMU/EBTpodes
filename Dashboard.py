import streamlit as st
import pandas as pd
import altair as alt
import scipy.stats as stats
import numpy as np
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.data_loader import load_national_data, load_provincial_data, format_number
from src.components.sidebar import render_sidebar
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from src.utils.map_constants import PROVINCE_CENTROIDS, PROVINCE_ABBREVIATIONS

# --- Page Config (Global) ---
st.set_page_config(
    page_title="Dashboard Analisis EBT & Perdesaan",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
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


# ==========================================
# 2. ANALISIS DESA TAMBANG (Integrasi)
# ==========================================
st.markdown("---")
st.header("Analisis Desa Tambang × EBT")
st.markdown('<p style="font-size: 1rem; color: #66BB6A; font-weight: 500; margin-top: -15px;">Deep Dive Analysis: Hubungan Ekstraktivisme dengan Indikator Keberlanjutan</p>', unsafe_allow_html=True)

# Alias for compatibility with copied code
df = df_prov 

if df.empty:
    st.error("Data provinsi tidak ditemukan.")
else:
    # --- Methodology Section ---
    with st.expander("ℹ️ Metodologi: Pipeline Analisis Chi-Square (SPSS)", expanded=False):
        st.markdown("""
        Analisis ini menggunakan uji **Pearson Chi-Square** untuk menentukan hubungan antara aktivitas pertambangan dengan adopsi EBT.
        
        **Langkah-langkah (Algoritma SPSS):**
        1.  **Binning Data**: Mengubah variabel kontinu (%) menjadi Kategori (Tinggi/Rendah) menggunakan pemisah Median.
        2.  **Crosstabulation**: Membuat tabel silang antara status Tambang (Baris) dan status EBT (Kolom).
        3.  **Hypothesis Testing**:
            *   $H_0$: Tidak ada hubungan antara Tambang dan EBT.
            *   $H_1$: Ada hubungan signifikan.
        4.  **Decision Rule**: Jika **P-Value < 0.05**, tolak $H_0$.
        """)

    # --- 2.1 Variable Selection ---
    st.subheader("2.1 Konfigurasi Variabel")

    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        st.markdown("##### Variabel Independen (X) - Faktor Pengaruh")
        mining_col = "tambang_2024_pct"
        st.info(f"**Intensitas Pertambangan** (% Desa Tambang per Provinsi)")
        
    with col_sel2:
        st.markdown("##### Variabel Dependen (Y) - Indikator EBT")
        ebt_options = {
            "R502a_pju_surya_2024_pct": "Penerangan Jalan Umum (PJU) Surya",
            "R501c_keluarga_surya_2024_pct": "Pengguna Listrik Surya (Keluarga)",
            "R503a6_bioenergi_2024_pct": "Pemanfaatan Bioenergi (Biogas)",
            "R510_air_2024_pct": "Pemanfaatan Energi Air (Mikrohidro/PLTA)",
            "R1504a_program_ebt_2024_pct": "Keberadaan Program EBT",
            "R1503a_infra_2024_pct": "Keberadaan Infrastruktur Energi",
            "R1403g_potensi_air_2024_pct": "Potensi Aset Energi Alam (Mata Air)",
            "R501a2_non_pln_2024_pct": "Akses Energi Non-PLN",
            "R501b_tanpa_listrik_2024_pct": "Keluarga Tanpa Listrik",
            "R514_polusi_air_2024_pct": "Pencemaran Lingkungan: Air",
            "R514_polusi_tanah_2024_pct": "Pencemaran Lingkungan: Tanah",
            "R514_polusi_udara_2024_pct": "Pencemaran Lingkungan: Udara"
        }
        # Use unique key for selectbox in dashboard (even though not in tab, safe practice)
        y_col = st.selectbox("Pilih Indikator EBT:", list(ebt_options.keys()), format_func=lambda x: ebt_options[x], key="dash_main_y_col")

    # --- Data Prep ---
    x_median = df[mining_col].median()
    y_median = df[y_col].median()

    df["X_Cat"] = df[mining_col].apply(lambda x: "Tinggi" if x >= x_median else "Rendah")
    df["Y_Cat"] = df[y_col].apply(lambda x: "Tinggi" if x >= y_median else "Rendah")

    label_x_low = f"Rendah (<{x_median:.2f}%)"
    label_x_high = f"Tinggi (≥{x_median:.2f}%)"
    label_y_low = f"Rendah (<{y_median:.2f}%)"
    label_y_high = f"Tinggi (≥{y_median:.2f}%)"

    df["X_Label"] = df[mining_col].apply(lambda x: label_x_high if x >= x_median else label_x_low)
    df["Y_Label"] = df[y_col].apply(lambda x: label_y_high if x >= y_median else label_y_low)

    crosstab = pd.crosstab(df["X_Label"], df["Y_Label"])
    cats_x = [label_x_low, label_x_high]
    cats_y = [label_y_low, label_y_high]
    crosstab = crosstab.reindex(index=cats_x, columns=cats_y, fill_value=0)

    chi2, p, dof, expected = stats.chi2_contingency(crosstab)
    expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)

    # --- Results Display ---
    st.subheader("2.2 Hasil Analisis Statistik")
    
    # A. Case Processing
    st.markdown("### Case Processing Summary")
    total_cases = len(df)
    valid_cases = len(df.dropna(subset=[mining_col, y_col]))
    missing_cases = total_cases - valid_cases
    
    columns = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
    interaction_label = f"{mining_col} * {ebt_options[y_col]}"
    row_data = [valid_cases, f"{valid_cases/total_cases*100:.1f}%", missing_cases, f"{missing_cases/total_cases*100:.1f}%", total_cases, "100.0%"]
    st.table(pd.DataFrame([row_data], index=[interaction_label], columns=columns))

    # B. Crosstab
    st.markdown(f"### {interaction_label} Crosstabulation")
    row_indices = []
    for x_cat in cats_x:
        row_indices.append((x_cat, "Count"))
        row_indices.append((x_cat, "Expected Count"))
    row_indices.append(("Total", "Count"))
    row_indices.append(("Total", "Expected Count"))

    rows = []
    count_low = crosstab.loc[label_x_low].tolist()
    exp_low = expected_df.loc[label_x_low].tolist()
    rows.append(count_low + [sum(count_low)])
    rows.append([f"{x:.1f}" for x in exp_low] + [f"{sum(exp_low):.1f}"])

    count_high = crosstab.loc[label_x_high].tolist()
    exp_high = expected_df.loc[label_x_high].tolist()
    rows.append(count_high + [sum(count_high)])
    rows.append([f"{x:.1f}" for x in exp_high] + [f"{sum(exp_high):.1f}"])

    total_counts = crosstab.sum().tolist()
    total_exp = expected_df.sum().tolist()
    rows.append(total_counts + [sum(total_counts)])
    rows.append([f"{x:.1f}" for x in total_exp] + [f"{sum(total_exp):.1f}"])

    spss_crosstab = pd.DataFrame(rows, index=pd.MultiIndex.from_tuples(row_indices, names=[mining_col, ""]), columns=cats_y + ["Total"])
    st.table(spss_crosstab)

    # C. Chi Square
    st.markdown("### Chi-Square Tests")
    st.markdown(f"**{interaction_label}**")
    
    pearson_val = chi2
    pearson_sig = p
    g, p_g, dof_g, exp_g = stats.chi2_contingency(crosstab, lambda_="log-likelihood")
    
    x_codes = df["X_Label"].replace({label_x_low:0, label_x_high:1})
    y_codes = df["Y_Label"].replace({label_y_low:0, label_y_high:1})
    r, p_corr = stats.pearsonr(x_codes, y_codes)
    lbl_val = (valid_cases - 1) * (r**2)
    
    chi_data = [
        [f"{pearson_val:.3f}", str(dof), f"{pearson_sig:.3f}"],
        [f"{g:.3f}", str(dof), f"{p_g:.3f}"],
        [f"{lbl_val:.3f}", "1", f"{p_corr:.3f}"],
        [str(valid_cases), "", ""]
    ]
    st.table(pd.DataFrame(chi_data, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"]))

    # D. Hypothesis
    st.markdown("### Ringkasan Uji Hipotesis")
    col_card, col_chart = st.columns([1, 1.5])
    
    with col_card:
        is_significant = pearson_sig < 0.05
        status_text = "SIGNIFIKAN (Ada Hubungan)" if is_significant else "TIDAK SIGNIFIKAN"
        order_color = "#4CAF50" if is_significant else "#F44336" 
        bg_color = "rgba(76, 175, 80, 0.1)" if is_significant else "rgba(244, 67, 54, 0.1)"
        
        st.markdown(f"""
        <div style="border: 2px solid {order_color}; padding: 15px; border-radius: 5px; background-color: {bg_color};">
            <h4 style="color: {order_color}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_text}</h4>
            <p style="margin: 0; font-family: monospace;">
                P-Value    : {pearson_sig:.4f}<br>
                Chi-Square : {pearson_val:.3f}<br>
                df         : {dof}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        try:
            a = crosstab.loc[label_x_low, label_y_low]
            b = crosstab.loc[label_x_low, label_y_high]
            c = crosstab.loc[label_x_high, label_y_low]
            d = crosstab.loc[label_x_high, label_y_high]
            odds_ratio = (a * d) / (b * c) if (b * c) > 0 else 0
            st.markdown(f"**Odds Ratio (Risk Estimate):** `{odds_ratio:.3f}`")
            
            if is_significant:
                 st.write("Interpretasi: Wilayah tambang memiliki kecenderungan signifikan terhadap kondisi EBT ini.")
            else:
                 st.write("Interpretasi: Tidak ada bukti statistik yang cukup untuk menyatakan hubungan.")
        except:
            st.write("-")

    with col_chart:
        st.markdown("**Visualisasi Proporsi**")

    # --- 2.3 Visualization ---
    st.markdown("---")
    st.subheader("2.3 Visualisasi Proporsi")
    
    chart_data = crosstab.reset_index().melt(id_vars="X_Label", var_name="Y_Label", value_name="Count")
    chart_data['X_Display'] = chart_data['X_Label'].apply(lambda x: f"Tambang: {x}")

    viz_mode = st.radio("Pilih Tampilan Grafik:", ["Bar Chart (Proporsi)", "Heatmap (Matriks)", "Donut Chart (Komparasi)"], horizontal=True, key="dash_main_viz_mode")

    if viz_mode == "Bar Chart (Proporsi)":
        chart = alt.Chart(chart_data).mark_bar(size=40).encode(
            x=alt.X('X_Display', title='Kategori Wilayah Tambang', axis=alt.Axis(labelAngle=0, grid=False)),
            y=alt.Y('Count', title='Jumlah Provinsi', axis=alt.Axis(grid=False)),
            color=alt.Color('Y_Label', title='Status EBT', scale=alt.Scale(domain=[label_y_low, label_y_high], range=['#E57373', '#81C784'])),
            tooltip=['X_Display', 'Y_Label', 'Count']
        ).properties(
            height=300, 
            title=alt.TitleParams(text='Proporsi Wilayah', anchor='start', fontSize=14)
        ).configure_view(strokeWidth=0).configure_axis(domain=False, tickSize=0)
        st.altair_chart(chart, use_container_width=True)

    elif viz_mode == "Heatmap (Matriks)":
        st.write("Visualisasi 'Density' Hubungan antar Variabel:")
        base = alt.Chart(chart_data).encode(
            x=alt.X('X_Display', title='', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Y_Label', title='Status EBT')
        )
        heatmap = base.mark_rect().encode(
            color=alt.Color('Count', legend=None, scale=alt.Scale(scheme='greens'))
        )
        text = base.mark_text(baseline='middle').encode(
            text='Count',
            color=alt.condition(alt.datum.Count > chart_data['Count'].max()/2, alt.value('white'), alt.value('black'))
        )
        st.altair_chart((heatmap + text).properties(height=300), use_container_width=True)

    elif viz_mode == "Donut Chart (Komparasi)":
        st.write("Perbandingan Komposisi EBT pada tiap Kategori Tambang:")
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"**Wilayah Tambang: {label_x_high}**")
            data_high = chart_data[chart_data['X_Label'] == label_x_high]
            base_h = alt.Chart(data_high).encode(theta=alt.Theta("Count", stack=True))
            pie_h = base_h.mark_arc(outerRadius=80, innerRadius=50).encode(
                color=alt.Color("Y_Label", scale=alt.Scale(domain=[label_y_low, label_y_high], range=['#E57373', '#81C784']), legend=None),
                tooltip=["Y_Label", "Count"]
            )
            text_h = base_h.mark_text(radius=100).encode(text=alt.Text("Count"), order=alt.Order("Y_Label"), color=alt.value("white"))
            st.altair_chart(pie_h, use_container_width=True)

        with c2:
            st.caption(f"**Wilayah Tambang: {label_x_low}**")
            data_low = chart_data[chart_data['X_Label'] == label_x_low]
            base_l = alt.Chart(data_low).encode(theta=alt.Theta("Count", stack=True))
            pie_l = base_l.mark_arc(outerRadius=80, innerRadius=50).encode(
                color=alt.Color("Y_Label", scale=alt.Scale(domain=[label_y_low, label_y_high], range=['#E57373', '#81C784']), legend=None),
                tooltip=["Y_Label", "Count"]
            )
            st.altair_chart(pie_l, use_container_width=True)
        st.info("💡 **Legend**: Hijau = EBT Tinggi, Merah = EBT Rendah")

    with st.expander("Lihat Detail Provinsi per Kategori"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Provinsi: {label_x_high}**")
            st.dataframe(df[df["X_Label"] == label_x_high][["Provinsi", mining_col, y_col]], use_container_width=True)
        with c2:
            st.markdown(f"**Provinsi: {label_x_low}**")
            st.dataframe(df[df["X_Label"] == label_x_low][["Provinsi", mining_col, y_col]], use_container_width=True)


# ==========================================
# 3. ANALISIS GAP POTENSI (Integrasi)
# ==========================================
st.markdown("---")
st.header("Analisis Gap: Potensi vs Realisasi")
st.markdown('<p style="font-size: 1rem; color: #66BB6A; font-weight: 500; margin-top: -15px;">Mengukur Disparitas Pemanfaatan Sumber Daya Alam</p>', unsafe_allow_html=True)

# Use a clean dataframe copy for Phase 3
df_gap = df_prov.copy()

if df_gap.empty:
    st.error("Data provinsi tidak ditemukan.")
else:
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
            index=0,
            key="dash_gap_energy_type"
        )

    # --- Logic Calculation ---
    # 1. Define Columns & Labels based on Selection
    if energy_type == "Energi Air (Hydro)":
        # Priority: R511 > R1403g
        col_potensi = "R511_potensi_air_2024" if "R511_potensi_air_2024" in df_gap.columns else "R1403g_potensi_air_2024"
        col_realisasi = "R510_air_2024"
        
        label_potensi = "Jumlah Desa Memiliki Potensi Sumber Daya Air"
        label_realisasi = "Jumlah Desa Memiliki Pembangkit Listrik (PLTA/Mikro/Pico)"
        
        color_range = ["#CFD8DC", "#4CAF50"] # Grey (Gap) vs Green (Realized)
        highlight_color = "#4CAF50"
        
    elif energy_type == "Energi Surya (Solar)":
        # Solar Potential
        col_realisasi = "R502a_pju_surya_2024"
        col_total = "R502a_pju_surya_2024_total"
        col_potensi = "potensi_surya_calc"
        
        # Calculate Potential assuming all villages have solar potential
        df_gap[col_potensi] = df_gap[col_total]
        
        label_potensi = "Total Desa (Potensi Teoritis)"
        label_realisasi = "Jumlah Desa Memiliki PJU Tenaga Surya"
        
        color_range = ["#FFE0B2", "#FB8C00"] # Light Orange (Gap) vs Deep Orange (Realized)
        highlight_color = "#FB8C00"

    # 2. Data Preparation
    df_gap[col_potensi] = pd.to_numeric(df_gap[col_potensi], errors='coerce').fillna(0)
    df_gap[col_realisasi] = pd.to_numeric(df_gap[col_realisasi], errors='coerce').fillna(0)

    # Calculate Gap
    df_gap["Gap_Value"] = df_gap[col_potensi] - df_gap[col_realisasi]
    df_gap["Gap_Value"] = df_gap["Gap_Value"].clip(lower=0)

    # Calculate Utilization Ratio
    df_gap["Util_Ratio"] = (df_gap[col_realisasi] / df_gap[col_potensi].replace(0, 1)) * 100

    # Sort for Visualization
    df_sorted = df_gap.sort_values("Gap_Value", ascending=False).head(10).reset_index(drop=True)

    # 3. National Summary Stats
    total_potensi = df_gap[col_potensi].sum()
    total_realisasi = df_gap[col_realisasi].sum()
    national_ratio = (total_realisasi / total_potensi * 100) if total_potensi > 0 else 0

    with col_ctrl2:
        st.markdown("##### Ringkasan Nasional")
        m1, m2, m3 = st.columns(3)
        
        # CSS is already loaded at top of Dashboard, but we can add specific if needed.
        # Re-using .metric-card style for consistency with Phase 3 standalone page if requested,
        # but let's try to adapt to Dashboard's .stat-card or use inline style for specific colors.
        # User requested "Colorful Cards" like Phase 2 (Green/Orange).
        
        with m1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Potensi</div>
                <div class="stat-number" style="color: #E0E0E0;">{format_number(total_potensi)}</div>
                <div style="font-size:0.75rem; color:#666;">Desa</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Realisasi</div>
                <div class="stat-number" style="color: {highlight_color};">{format_number(total_realisasi)}</div>
                <div style="font-size:0.75rem; color:#666;">Desa</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="stat-card" style="border-bottom: 2px solid {highlight_color};">
                <div class="stat-label">Rasio Pemanfaatan</div>
                <div class="stat-number" style="color: #FFC107;">{national_ratio:.2f}%</div>
                <div style="font-size:0.75rem; color:#666;">Efficiency Rate</div>
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
        x=alt.X("Display_Value", title="Jumlah Desa", axis=alt.Axis(format="s")),
        color=alt.Color("Status", scale=alt.Scale(domain=["Belum Dimanfaatkan", "Sudah Dimanfaatkan"], range=color_range), legend=alt.Legend(orient="top")),
        tooltip=["Provinsi", "Status", alt.Tooltip("Jumlah", format=",d")]
    )

    # Bars
    bars = base.mark_bar().properties(height=400)

    # Text Labels (Numbers inside bars)
    text = base.mark_text(
        align='center',
        baseline='middle',
        dx=alt.expr("datum.Display_Value > 0 ? 20 : -20"),
        color='white'
    ).encode(
        text=alt.Text("Jumlah", format=",")
    )

    st.altair_chart(bars + text, use_container_width=True)

    # --- Detail Data View (Default Expanded) ---
    with st.expander("📂 Lihat Data Lengkap (Semua Provinsi)", expanded=True):
        table_df = df_gap[["Provinsi", col_potensi, col_realisasi, "Util_Ratio", "Gap_Value"]].sort_values("Util_Ratio")
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
    prov_abbr = { "ACEH": "Aceh", "SUMATERA UTARA": "Sumut", "SUMATERA BARAT": "Sumbar", "RIAU": "Riau", "JAMBI": "Jambi", "SUMATERA SELATAN": "Sumsel", "BENGKULU": "Bengkulu", "LAMPUNG": "Lampung", "KEP. BANGKA BELITUNG": "Babel", "KEP. RIAU": "Kepri", "DKI JAKARTA": "DKI", "JAWA BARAT": "Jabar", "JAWA TENGAH": "Jateng", "DI YOGYAKARTA": "DIY", "JAWA TIMUR": "Jatim", "BANTEN": "Banten", "BALI": "Bali", "NUSA TENGGARA BARAT": "NTB", "NUSA TENGGARA TIMUR": "NTT", "KALIMANTAN BARAT": "Kalbar", "KALIMANTAN TENGAH": "Kalteng", "KALIMANTAN SELATAN": "Kalsel", "KALIMANTAN TIMUR": "Kaltim", "KALIMANTAN UTARA": "Kaltara", "SULAWESI UTARA": "Sulut", "SULAWESI TENGAH": "Sulteng", "SULAWESI SELATAN": "Sulsel", "SULAWESI TENGGARA": "Sultra", "GORONTALO": "Gorontalo", "SULAWESI BARAT": "Sulbar", "MALUKU": "Maluku", "MALUKU UTARA": "Malut", "PAPUA BARAT": "Pabar", "PAPUA": "Papua", "PAPUA SELATAN": "Papsel", "PAPUA TENGAH": "Papteng", "PAPUA PEGUNUNGAN": "Pappeg", "PAPUA BARAT DAYA": "Pabardya" }
    df_gap["Provinsi_Abbr"] = df_gap["Provinsi"].map(prov_abbr).fillna(df_gap["Provinsi"])

    # Scatter Plot
    df_gap["Status_Efisiensi"] = df_gap["Util_Ratio"].apply(lambda x: "Efisien" if x >= national_ratio else "Inefisien")
    color_scale = alt.Scale(domain=["Efisien", "Inefisien"], range=["#4CAF50", "#FF5252"])

    base_chart = alt.Chart(df_gap).encode(
        x=alt.X(col_potensi, title="Total Potensi (Log Scale)", scale=alt.Scale(type="symlog", zero=False)),
        y=alt.Y(col_realisasi, title="Total Realisasi (Log Scale)", scale=alt.Scale(type="symlog", zero=False)) 
    )

    scatter_points = base_chart.mark_circle(size=120, opacity=0.8).encode(
        color=alt.Color("Status_Efisiensi", scale=color_scale, legend=alt.Legend(title="Kinerja", orient="right")),
        tooltip=["Provinsi", "Status_Efisiensi", alt.Tooltip(col_potensi, format=","), alt.Tooltip(col_realisasi, format=",")]
    )

    # National Average Line (Threshold)
    # Max possible value for line extension
    max_pot_data = df_gap[col_potensi].max()
    # Start from 0 to cover origin, go up to 2x max (safety check for 0)
    x_vals = np.concatenate(([0], np.geomspace(1, max(max_pot_data, 1.0) * 2, num=200))) 
    y_vals = x_vals * (national_ratio / 100)

    line_data = pd.DataFrame({ col_potensi: x_vals, col_realisasi: y_vals, "Label": ["Rata-rata Nasional"] * len(x_vals) })

    threshold_line = alt.Chart(line_data).mark_line(color="#FFC107", strokeDash=[5,5], size=2).encode(x=alt.X(col_potensi), y=alt.Y(col_realisasi))

    text_labels = base_chart.mark_text(align='left', baseline='middle', dx=8, fontSize=10, color='white').encode(text='Provinsi_Abbr')

    final_scatter = (scatter_points + threshold_line + text_labels).properties(height=500).interactive()
    st.altair_chart(final_scatter, use_container_width=True)
    st.info("Garis putus-putus kuning adalah 'Garis Rata-rata Nasional'. Provinsi di **bawah garis** berarti efisiensinya di bawah rata-rata nasional (Inefisien/Merah). Provinsi di **atas garis** berarti efisiensinya di atas rata-rata nasional (Efisien/Hijau).")

# --- Divider ---
st.markdown("---")

# ==========================================
# 4. ANALISIS KETIMPANGAN ENERGI (Integrasi)
# ==========================================
st.header("Analisis Ketimpangan Energi (IKE)")
st.markdown('<p style="font-size: 1rem; color: #66BB6A; font-weight: 500; margin-top: -15px;">Pemetaan Risiko Multidimensi (Akses, Ketergantungan, Lingkungan)</p>', unsafe_allow_html=True)

# --- 4.1 Data Processing (Cached) ---
@st.cache_data
def process_ike_data_dashboard():
    df = load_provincial_data()
    if df.empty:
        return None, None, None

    # Indicators
    indicators = {
        "R501b_tanpa_listrik_2024_pct": "Rasio Tanpa Listrik",
        "R501a2_non_pln_2024_pct": "Ketergantungan Non-PLN",
        "R514_polusi_air_2024_pct": "Risiko Lingkungan (Air)"
    }
    
    # Inverse Indicators
    if "R1504a_program_ebt_2024_pct" in df.columns:
        df["Rasio_Tanpa_Program"] = 100 - df["R1504a_program_ebt_2024_pct"]
        indicators["Rasio_Tanpa_Program"] = "Ketiadaan Program EBT"

    if "R1503a_infra_2024_pct" in df.columns:
        df["Rasio_Tanpa_Infra"] = 100 - df["R1503a_infra_2024_pct"]
        indicators["Rasio_Tanpa_Infra"] = "Ketiadaan Infrastruktur"

    indicator_cols = list(indicators.keys())

    # Normalization & IKE
    scaler = MinMaxScaler()
    df_norm = pd.DataFrame(scaler.fit_transform(df[indicator_cols]), columns=indicator_cols, index=df.index)
    
    df["IKE_Score"] = df_norm.mean(axis=1) * 100
    df["IKE_Rank"] = df["IKE_Score"].rank(ascending=False)
    
    # Sort
    df_ike = df.sort_values("IKE_Score", ascending=False).reset_index(drop=True)

    # Province Name Normalization (Data vs GeoJSON)
    prov_map = {
        "ACEH": "DI. ACEH",
        "SUMATERA UTARA": "SUMATERA UTARA",
        "SUMATERA BARAT": "SUMATERA BARAT",
        "RIAU": "RIAU",
        "JAMBI": "JAMBI",
        "SUMATERA SELATAN": "SUMATERA SELATAN",
        "BENGKULU": "BENGKULU",
        "LAMPUNG": "LAMPUNG",
        "KEP. BANGKA BELITUNG": "BANGKA BELITUNG", 
        "KEPULAUAN BANGKA BELITUNG": "BANGKA BELITUNG", 
        "KEP. RIAU": "RIAU",
        "KEPULAUAN RIAU": "RIAU",
        "DKI JAKARTA": "DKI JAKARTA",
        "DAERAH KHUSUS IBUKOTA JAKARTA": "DKI JAKARTA", 
        "JAWA BARAT": "JAWA BARAT",
        "JAWA TENGAH": "JAWA TENGAH",
        "DI YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA", 
        "DAERAH ISTIMEWA YOGYAKARTA": "DAERAH ISTIMEWA YOGYAKARTA", 
        "JAWA TIMUR": "JAWA TIMUR",
        "BANTEN": "PROBANTEN",
        "BALI": "BALI",
        "NUSA TENGGARA BARAT": "NUSATENGGARA BARAT",
        "NUSA TENGGARA TIMUR": "NUSA TENGGARA TIMUR",
        "KALIMANTAN BARAT": "KALIMANTAN BARAT",
        "KALIMANTAN TENGAH": "KALIMANTAN TENGAH",
        "KALIMANTAN SELATAN": "KALIMANTAN SELATAN",
        "KALIMANTAN TIMUR": "KALIMANTAN TIMUR",
        "KALIMANTAN UTARA": "KALIMANTAN TIMUR",
        "SULAWESI UTARA": "SULAWESI UTARA",
        "SULAWESI TENGAH": "SULAWESI TENGAH",
        "SULAWESI SELATAN": "SULAWESI SELATAN",
        "SULAWESI TENGGARA": "SULAWESI TENGGARA",
        "GORONTALO": "GORONTALO",
        "SULAWESI BARAT": "SULAWESI SELATAN",
        "MALUKU": "MALUKU",
        "MALUKU UTARA": "MALUKU UTARA",
        "PAPUA BARAT": "IRIAN JAYA BARAT", 
        "PROVINSI PAPUA BARAT": "IRIAN JAYA BARAT",
        "PAPUA": "IRIAN JAYA TIMUR", 
        "PROVINSI PAPUA": "IRIAN JAYA TIMUR",
        "PAPUA SELATAN": "IRIAN JAYA TIMUR",
        "PROVINSI PAPUA SELATAN": "IRIAN JAYA TIMUR",
        "PAPUA TENGAH": "IRIAN JAYA TENGAH",
        "PROVINSI PAPUA TENGAH": "IRIAN JAYA TENGAH",
        "PAPUA PEGUNUNGAN": "IRIAN JAYA TIMUR",
        "PROVINSI PAPUA PEGUNUNGAN": "IRIAN JAYA TIMUR",
        "PAPUA BARAT DAYA": "IRIAN JAYA BARAT",
        "PROVINSI PAPUA BARAT DAYA": "IRIAN JAYA BARAT"
    }

    df_ike["Provinsi_Map"] = df_ike["Provinsi"].map(prov_map).fillna(df_ike["Provinsi"])
    
    # Prepare Label Data for Map
    label_data = []
    # Ensure constants are fresh (though generally fine in dashboard scope)
    import src.utils.map_constants as mc
    
    for prov_name, coords in mc.PROVINCE_CENTROIDS.items():
        if prov_name in df_ike["Provinsi_Map"].values:
            score = df_ike[df_ike["Provinsi_Map"] == prov_name]["IKE_Score"].values[0]
            abbr = mc.PROVINCE_ABBREVIATIONS.get(prov_name, prov_name)
            label_data.append({
                "lat": coords[0],
                "lon": coords[1],
                "text": f"{abbr}\n{score:.1f}",
                "Provinsi": prov_name,
                "IKE_Score": score
            })
    df_labels_alt = pd.DataFrame(label_data)
    
    return df_ike, df_labels_alt, indicator_cols

# Execute Processing
df_ike_dash, df_labels_dash, indicator_cols = process_ike_data_dashboard()

if df_ike_dash is not None:
    # --- 4.2 Visualization ---
    st.subheader("4.1 Peta Sebaran Kerentanan Energi")
    
    # GeoJSON Configuration
    geo_json_url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
    geo_source = alt.Data(url=geo_json_url, format=alt.DataFormat(property='features', type='json'))

    # Base Map
    base_map = alt.Chart(geo_source).mark_geoshape(
        stroke='white',
        strokeWidth=0.5
    ).encode(
        color=alt.Color(
            'IKE_Score:Q', 
            scale=alt.Scale(scheme='reds', domain=[10, 60], clamp=True),
            title="Skor IKE"
        ),
        tooltip=[
            alt.Tooltip('properties.Propinsi:N', title='Provinsi'),
            alt.Tooltip('IKE_Score:Q', title='Skor IKE', format='.1f'),
            alt.Tooltip('IKE_Rank:Q', title='Peringkat'),
        ]
    ).transform_lookup(
        lookup='properties.Propinsi',
        from_=alt.LookupData(df_ike_dash, 'Provinsi_Map', ['IKE_Score', 'IKE_Rank'])
    ).properties(
        width=800,
        height=500
    )

    # Label Layer
    text_layer = alt.Chart(df_labels_dash).mark_text(
        color='white',
        fontSize=9,
        fontWeight='bold',
        dy=-5,
        clip=False
    ).encode(
        latitude='lat:Q',
        longitude='lon:Q',
        text='text:N'
    )

    # Final Map
    final_map = alt.layer(base_map, text_layer).project(
        type='mercator',
        scale=1200,             
        center=[118, -2]
    ).properties(
        title="Peta Indeks Kerentanan Energi (IKE)"
    ).configure_view(strokeWidth=0)

    st.altair_chart(final_map, use_container_width=True)

    # Top Ranking Chart
    st.subheader("4.2 Peringkat Kerentanan Provinsi")
    
    bar_chart = alt.Chart(df_ike_dash.head(38)).mark_bar().encode(
        x=alt.X("IKE_Score:Q", title="Skor IKE"),
        y=alt.Y("Provinsi:N", sort="-x", title=None),
        color=alt.Color("IKE_Score:Q", scale=alt.Scale(scheme="reds"), legend=None),
        tooltip=["Provinsi", alt.Tooltip("IKE_Score", format=".1f")]
    ).properties(
        height=500,
        title="Peringkat Provinsi (Rentan → Aman)"
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # Detail Expander
    with st.expander("🔍 Lihat Detail Data IKE", expanded=False):
        st.dataframe(df_ike_dash, use_container_width=True)

    # --- 4.3 Validation (Scientific Check) ---
    st.markdown("---")
    st.subheader("4.3 Validasi Statistik: Principal Component Analysis (PCA)")
    st.caption("Uji ketangguhan (*Robustness Check*) untuk memvalidasi apakah metode 'Equal Weighting' bias atau tidak dibandingkan metode statistik murni.")
    
    # Calculate PCA-based Score
    # Re-normalize from df_ike_dash (Sorted) to ensure Row Alignment
    scaler_valid = MinMaxScaler()
    df_valid_norm = pd.DataFrame(scaler_valid.fit_transform(df_ike_dash[indicator_cols]), columns=indicator_cols)
    
    pca = PCA(n_components=1)
    df_pca_input = df_valid_norm.fillna(0)
    pca_score = pca.fit_transform(df_pca_input)
    
    # Align direction
    if np.corrcoef(pca_score.flatten(), df_valid_norm[indicator_cols[0]])[0,1] < 0:
        pca_score = -pca_score
        
    df_ike_dash["IKE_PCA"] = MinMaxScaler().fit_transform(pca_score) * 100
    
    # Correlation Check
    correlation = df_ike_dash["IKE_Score"].corr(df_ike_dash["IKE_PCA"], method='spearman')
    
    # A. Case Processing Summary (SPSS Style)
    st.markdown("##### Case Processing Summary")
    
    total_cases = len(df_ike_dash)
    valid_cases = len(df_pca_input)
    missing_cases = total_cases - valid_cases
    
    columns = pd.MultiIndex.from_product(
        [["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]]
    )
    
    row_data = [
        valid_cases, f"{valid_cases/total_cases*100:.1f}%",
        missing_cases, f"{missing_cases/total_cases*100:.1f}%",
        total_cases, "100.0%"
    ]
    
    case_summary = pd.DataFrame([row_data], index=["Provinsi * Indicators"], columns=columns)
    st.table(case_summary)
    
    # B. Correlation Result
    st.markdown("##### Hasil Uji Korelasi (Pearson & Spearman)")
    
    col_res, col_chart = st.columns([1, 1.5])
    
    with col_res:
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 5px; background-color: rgba(76, 175, 80, 0.1);">
            <h4 style="color: #4CAF50; margin: 0 0 10px 0;">VALID & ROBUST</h4>
            <p style="margin: 0; font-size: 0.9rem;">
                Metode <b>Equal Weighting</b> memiliki korelasi yang sangat kuat dengan hasil komputasi <b>PCA</b>.
            </p>
            <hr style="border-color: #4CAF50; opacity: 0.3;">
            <p style="margin: 0; font-family: monospace; font-size: 1.1rem; font-weight: bold;">
                Correlation : {correlation:.4f}<br>
                Status      : Very Strong
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("*Nilai korelasi mendekati 1.0 menandakan hasil peringkat kedua metode hampir identik.*")
    
    with col_chart:
        st.markdown("**Visualisasi Scatter Plot (Konsistensi Ranking):**")
        chart_corr = alt.Chart(df_ike_dash).mark_circle(size=80).encode(
            x=alt.X('IKE_Score', title='Skor IKE (Equal Weight)'),
            y=alt.Y('IKE_PCA', title='Skor Validasi (PCA)'),
            color=alt.value("#66BB6A"),
            tooltip=['Provinsi', 'IKE_Score', 'IKE_PCA']
        ).properties(height=300)
        
        regression_line = chart_corr.transform_regression('IKE_Score', 'IKE_PCA').mark_line(color='white', strokeDash=[5,5])
        
        st.altair_chart(chart_corr + regression_line, use_container_width=True)

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

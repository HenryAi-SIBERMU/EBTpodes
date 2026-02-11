import streamlit as st
import pandas as pd
import altair as alt
import scipy.stats as stats
from src.components.sidebar import render_sidebar
from src.utils.data_loader import load_provincial_data, format_number

# --- Page Config ---
st.set_page_config(
    page_title="Analisis Desa Tambang — CELIOS",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)

# --- Sidebar ---
render_sidebar()

# --- Load Data ---
df = load_provincial_data()

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

st.markdown('<h1 class="main-title">Desa Tambang × EBT</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Crosstab desa tambang vs 10 dimensi energi terbarukan</p>', unsafe_allow_html=True)

if df.empty:
    st.error("Data provinsi tidak ditemukan.")
    st.stop()

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

# --- 2.1 Variable Selection (was 1.) ---
st.subheader("2.1 Konfigurasi Variabel")

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    st.markdown("##### Variabel Independen (X) - Faktor Pengaruh")
    # Hardcoded to Mining as per page theme
    mining_col = "tambang_2024_pct"
    st.info(f"**Intensitas Pertambangan** (% Desa Tambang per Provinsi)")
    
with col_sel2:
    # ... existing code ...
    st.markdown("##### Variabel Dependen (Y) - Indikator EBT")
    ebt_options = {
        # --- Akses & Penggunaan EBT ---
        "R502a_pju_surya_2024_pct": "Penerangan Jalan Umum (PJU) Surya",
        "R501c_keluarga_surya_2024_pct": "Pengguna Listrik Surya (Keluarga)",
        "R503a6_bioenergi_2024_pct": "Pemanfaatan Bioenergi (Biogas)",
        "R510_air_2024_pct": "Pemanfaatan Energi Air (Mikrohidro/PLTA)",
        
        # --- Infrastruktur & Program ---
        "R1504a_program_ebt_2024_pct": "Keberadaan Program EBT",
        "R1503a_infra_2024_pct": "Keberadaan Infrastruktur Energi",
        "R1403g_potensi_air_2024_pct": "Potensi Aset Energi Alam (Mata Air)",
        
        # --- Keadilan & Akses Dasar ---
        "R501a2_non_pln_2024_pct": "Akses Energi Non-PLN",
        "R501b_tanpa_listrik_2024_pct": "Keluarga Tanpa Listrik",
        
        # --- Dampak Lingkungan ---
        "R514_polusi_air_2024_pct": "Pencemaran Lingkungan: Air",
        "R514_polusi_tanah_2024_pct": "Pencemaran Lingkungan: Tanah",
        "R514_polusi_udara_2024_pct": "Pencemaran Lingkungan: Udara"
    }
    y_col = st.selectbox("Pilih Indikator EBT:", list(ebt_options.keys()), format_func=lambda x: ebt_options[x])

# --- 2. Data Preparation (Binning) ---
# Calculate Medians for Split
x_median = df[mining_col].median()
y_median = df[y_col].median()

# Create Categorical Columns
df["X_Cat"] = df[mining_col].apply(lambda x: "Tinggi" if x >= x_median else "Rendah")
df["Y_Cat"] = df[y_col].apply(lambda x: "Tinggi" if x >= y_median else "Rendah")

# --- 3. SPSS-Style Output Generation ---

# Helper to format labels with range
def get_label_with_threshold(val, median):
    return f"Tinggi (>{median:.1f}%)" if val >= median else f"Rendah (<{median:.1f}%)"

# Rename Categories for Clarity
label_x_low = f"Rendah (<{x_median:.2f}%)"
label_x_high = f"Tinggi (≥{x_median:.2f}%)"
label_y_low = f"Rendah (<{y_median:.2f}%)"
label_y_high = f"Tinggi (≥{y_median:.2f}%)"

df["X_Label"] = df[mining_col].apply(lambda x: label_x_high if x >= x_median else label_x_low)
df["Y_Label"] = df[y_col].apply(lambda x: label_y_high if x >= y_median else label_y_low)

# Create Crosstab (Base)
crosstab = pd.crosstab(df["X_Label"], df["Y_Label"])
# Ensure specific order
cats_x = [label_x_low, label_x_high]
cats_y = [label_y_low, label_y_high]
crosstab = crosstab.reindex(index=cats_x, columns=cats_y, fill_value=0)

# Calculate Expected
chi2, p, dof, expected = stats.chi2_contingency(crosstab)
expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)

# ... (Calculations continue unchanged) ...

# --- RESULTS DISPLAY ---
# --- 2.2 Statistical Analysis (was 2.) ---
st.subheader("2.2 Hasil Analisis Statistik")

# A. Case Processing Summary
# ... (rest of the code) ...

# A. Case Processing Summary
st.markdown("### Case Processing Summary")

total_cases = len(df)
valid_cases = len(df.dropna(subset=[mining_col, y_col]))
missing_cases = total_cases - valid_cases

# Construct MultiIndex Columns for SPSS structure: Cases -> [Valid, Missing, Total] -> [N, Percent]
columns = pd.MultiIndex.from_product(
    [["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]]
)

# Row Data
interaction_label = f"{mining_col} * {ebt_options[y_col]}"
row_data = [
    valid_cases, f"{valid_cases/total_cases*100:.1f}%",
    missing_cases, f"{missing_cases/total_cases*100:.1f}%",
    total_cases, "100.0%"
]

case_summary = pd.DataFrame([row_data], index=[interaction_label], columns=columns)
st.table(case_summary)

# B. Crosstabulation
st.markdown(f"### {interaction_label} Crosstabulation")

# Construct the Nested DataFrame for st.table
row_indices = []

for x_cat in cats_x:
    row_indices.append((x_cat, "Count"))
    row_indices.append((x_cat, "Expected Count"))

row_indices.append(("Total", "Count"))
row_indices.append(("Total", "Expected Count"))

# Build Data Rows
rows = []
# 1. Low Row
count_low = crosstab.loc[label_x_low].tolist()
exp_low = expected_df.loc[label_x_low].tolist()
rows.append(count_low + [sum(count_low)])        # Count
rows.append([f"{x:.1f}" for x in exp_low] + [f"{sum(exp_low):.1f}"]) # Exp

# 2. High Row
count_high = crosstab.loc[label_x_high].tolist()
exp_high = expected_df.loc[label_x_high].tolist()
rows.append(count_high + [sum(count_high)])       # Count
rows.append([f"{x:.1f}" for x in exp_high] + [f"{sum(exp_high):.1f}"]) # Exp

# 3. Total Row
total_counts = crosstab.sum().tolist()
total_exp = expected_df.sum().tolist()
rows.append(total_counts + [sum(total_counts)])   # Count
rows.append([f"{x:.1f}" for x in total_exp] + [f"{sum(total_exp):.1f}"]) # Exp

# Create MultiIndex DataFrame
multi_index = pd.MultiIndex.from_tuples(row_indices, names=[mining_col, ""])
spss_crosstab = pd.DataFrame(rows, index=multi_index, columns=cats_y + ["Total"])

st.table(spss_crosstab)

# C. Chi-Square Tests
st.markdown("### Chi-Square Tests")

# 1. Pearson
pearson_val = chi2
pearson_sig = p

# 2. Likelihood Ratio
g, p_g, dof_g, exp_g = stats.chi2_contingency(crosstab, lambda_="log-likelihood")
like_val = g
like_sig = p_g

# 3. Linear-by-Linear
x_codes = df["X_Label"].replace({label_x_low:0, label_x_high:1})
y_codes = df["Y_Label"].replace({label_y_low:0, label_y_high:1})
r, p_corr = stats.pearsonr(x_codes, y_codes)
n = valid_cases
lbl_val = (n - 1) * (r**2)
lbl_sig = p_corr

# Use the same row labels as SPSS (often just the test names, but the user wants the interaction label context)
# SPSS usually puts the interaction label in the title or a separate row, but let's stick to the test names as row indices for clarity 
# unless the user specifically wants the interaction label *in* the table. 
# Based on screenshot, "Personality * Preference * City" is in the Case Processing Summary. 
# In Chi-Square Tests, it usually lists the variable names if split, or just the test names. 
# The user said "berlaku juga ini di cchi square tests". Let's add it to the table caption or a row if possible, 
# but standard SPSS Chi-Square table has test names as rows. 
# Let's add the interaction label as a clear sub-header or caption to the table to meet the requirement "sebelum N... ada indikator".

st.markdown(f"**{interaction_label}**") 

chi_data = [
    [f"{pearson_val:.3f}", str(dof), f"{pearson_sig:.3f}"],
    [f"{like_val:.3f}", str(dof), f"{like_sig:.3f}"],
    [f"{lbl_val:.3f}", "1", f"{lbl_sig:.3f}"],
    [str(n), "", ""]
]

chi_df = pd.DataFrame(chi_data, 
                      index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"],
                      columns=["Value", "df", "Asymp. Sig. (2-sided)"])
st.table(chi_df)

# D. Hypothesis & Risk Summary (Card NO ICONS)
st.markdown("### Ringkasan Uji Hipotesis")

col_card, col_chart = st.columns([1, 1.5])

with col_card:
    is_significant = pearson_sig < 0.05
    status_text = "SIGNIFIKAN (Ada Hubungan)" if is_significant else "TIDAK SIGNIFIKAN"
    order_color = "#4CAF50" if is_significant else "#F44336" 
    bg_color = "rgba(76, 175, 80, 0.1)" if is_significant else "rgba(244, 67, 54, 0.1)"
    
    # Removed emoji/icon as requested ("jangan pakai ikon ikon")
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

    # Risk Estimate
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




# --- 2.3 Visualization (was 3.) ---
st.markdown("---")
st.subheader("2.3 Visualisasi Proporsi")

# Prepare data for chart
# Stacked Bar: X-Axis = Mining Category, Color = EBT Category, Value = Count
chart_data = crosstab.reset_index().melt(id_vars="X_Label", var_name="Y_Label", value_name="Count")
chart_data['X_Display'] = chart_data['X_Label'].apply(lambda x: f"Tambang: {x}")

viz_mode = st.radio("Pilih Tampilan Grafik:", ["Bar Chart (Proporsi)", "Heatmap (Matriks)", "Donut Chart (Komparasi)"], horizontal=True)

if viz_mode == "Bar Chart (Proporsi)":
    chart = alt.Chart(chart_data).mark_bar(size=40).encode(  # Slimmer bars
        x=alt.X('X_Display', title='Kategori Wilayah Tambang', axis=alt.Axis(labelAngle=0, grid=False)), # No grid
        y=alt.Y('Count', title='Jumlah Provinsi', axis=alt.Axis(grid=False)), # No grid
        # Use the actual labels for color domain
        color=alt.Color('Y_Label', title='Status EBT', scale=alt.Scale(domain=[label_y_low, label_y_high], range=['#E57373', '#81C784'])),
        tooltip=['X_Display', 'Y_Label', 'Count']
    ).properties(
        height=300, # Slightly shorter
        title=alt.TitleParams(text='Proporsi Wilayah', anchor='start', fontSize=14)
    ).configure_view(
        strokeWidth=0 # Remove border
    ).configure_axis(
        domain=False, # Remove axis lines
        tickSize=0    # Remove ticks
    )
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
        color=alt.condition(
            alt.datum.Count > chart_data['Count'].max()/2,
            alt.value('white'),
            alt.value('black')
        )
    )
    st.altair_chart((heatmap + text).properties(height=300), use_container_width=True)

elif viz_mode == "Donut Chart (Komparasi)":
    st.write("Perbandingan Komposisi EBT pada tiap Kategori Tambang:")
    
    # Donut requires pie transform which is tricky in Altair simplified view, let's use facet or hconcat
    # We will make 2 charts side-by-side manually
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.caption(f"**Wilayah Tambang: {label_x_high}**")
        data_high = chart_data[chart_data['X_Label'] == label_x_high]
        base = alt.Chart(data_high).encode(
            theta=alt.Theta("Count", stack=True)
        )
        pie = base.mark_arc(outerRadius=80, innerRadius=50).encode(
            color=alt.Color("Y_Label", scale=alt.Scale(domain=[label_y_low, label_y_high], range=['#E57373', '#81C784']), legend=None),
            tooltip=["Y_Label", "Count"]
        )
        text = base.mark_text(radius=100).encode(
            text=alt.Text("Count"),
            order=alt.Order("Y_Label"),
            color=alt.value("white")  # simple text
        )
        st.altair_chart(pie, use_container_width=True)

    with c2:
        st.caption(f"**Wilayah Tambang: {label_x_low}**")
        data_low = chart_data[chart_data['X_Label'] == label_x_low]
        base = alt.Chart(data_low).encode(
            theta=alt.Theta("Count", stack=True)
        )
        pie = base.mark_arc(outerRadius=80, innerRadius=50).encode(
            color=alt.Color("Y_Label", scale=alt.Scale(domain=[label_y_low, label_y_high], range=['#E57373', '#81C784']), legend=None),
            tooltip=["Y_Label", "Count"]
        )
        st.altair_chart(pie, use_container_width=True)
    
    st.info("💡 **Legend**: Hijau = EBT Tinggi, Merah = EBT Rendah")

# --- List Provinsi ---
with st.expander("Lihat Detail Provinsi per Kategori"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Provinsi: {label_x_high}**")
        st.dataframe(df[df["X_Label"] == label_x_high][["Provinsi", mining_col, y_col]], use_container_width=True)
    with c2:
        st.markdown(f"**Provinsi: {label_x_low}**")
        st.dataframe(df[df["X_Label"] == label_x_low][["Provinsi", mining_col, y_col]], use_container_width=True)


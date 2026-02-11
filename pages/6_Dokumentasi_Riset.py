import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Dokumentasi Riset — CELIOS EBT",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide"
)
render_sidebar()

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.page-header {
    font-size: 2rem;
    font-weight: 700;
    color: #E0E0E0;
    margin-bottom: 0.3rem;
}
.page-sub {
    font-size: 0.95rem;
    color: #757575;
    margin-bottom: 2rem;
}

.doc-selector {
    background: #1A1F2B;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 1.5rem;
    border: 1px solid #ffffff11;
}

.doc-content {
    background: #1A1F2B;
    border-radius: 12px;
    padding: 32px;
    border: 1px solid #ffffff11;
    line-height: 1.7;
}

.doc-meta {
    display: flex;
    gap: 16px;
    margin-bottom: 1rem;
}
.meta-chip {
    background: #2E7D3222;
    color: #66BB6A;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 500;
}

/* Table styling */
.doc-content table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}
.doc-content th {
    background: #232B3B;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 0.85rem;
    border-bottom: 2px solid #2E7D32;
}
.doc-content td {
    padding: 8px 14px;
    border-bottom: 1px solid #ffffff0a;
    font-size: 0.85rem;
}

.download-section {
    margin-top: 1.5rem;
    padding: 16px 20px;
    background: #1A1F2B;
    border-radius: 12px;
    border: 1px solid #ffffff11;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="page-header">📑 Dokumentasi Riset</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Preview dan download dokumen riset EBT — pilih dokumen dari sidebar untuk membaca</div>', unsafe_allow_html=True)

# --- Get docs directory ---
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

# --- List available docs ---
docs_map = {
    "📄 Laporan Insight Data EBT (PODES 2024 vs 2021)": {
        "file": "report_insight_data_EBT_PODES.md",
        "desc": "Laporan lengkap 10 dimensi energi terbarukan + temuan kritis + rencana analisis lanjutan",
        "tags": ["Data Report", "10 Dimensi", "38 Provinsi"]
    },
    "📄 Strategi Narasi & Arah Analisis": {
        "file": "strategi_narasi_EBT.md",
        "desc": "3 narasi besar, metode analisis per narasi, dan rencana struktur Streamlit",
        "tags": ["Strategy", "3 Narasi", "Research Design"]
    },

}

# --- Sidebar document selector ---
with st.sidebar:
    st.markdown("### 📂 Pilih Dokumen")
    selected_doc = st.radio(
        "Dokumen:",
        list(docs_map.keys()),
        label_visibility="collapsed"
    )
    
    # st.markdown("---")
    # st.markdown("### 📋 Daftar Dokumen")
    # for name, info in docs_map.items():
    #     icon = "✅" if name == selected_doc else "📄"
    #     st.markdown(f"{icon} {info['file']}")

# --- Load and render selected doc ---
doc_info = docs_map[selected_doc]
doc_path = os.path.join(DOCS_DIR, doc_info["file"])

# Meta tags
tags_html = " ".join([f'<span class="meta-chip">{tag}</span>' for tag in doc_info["tags"]])
st.markdown(f'<div class="doc-meta">{tags_html}</div>', unsafe_allow_html=True)
st.markdown(f"*{doc_info['desc']}*")

st.markdown("---")

# Read and render markdown
if os.path.exists(doc_path):
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Hide internal planning sections in dashboard view (keep MD file intact)
    if "## Struktur Output Streamlit" in content:
        content = content.split("## Struktur Output Streamlit")[0]
    
    st.markdown(content, unsafe_allow_html=True)
    
    # Download button
    st.markdown("---")
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        st.download_button(
            label=f"⬇️ Download {doc_info['file']}",
            data=content,
            file_name=doc_info["file"],
            mime="text/markdown",
            use_container_width=True,
        )
else:
    st.error(f"File tidak ditemukan: `{doc_path}`")
    st.info("Pastikan file .md sudah ada di folder `docs/`")

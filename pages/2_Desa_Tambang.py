import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar

st.set_page_config(page_title="Desa Tambang — CELIOS EBT", page_icon="🏭", layout="wide")
render_sidebar()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.coming-soon { text-align: center; padding: 80px 20px; }
.coming-soon h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #43A047, #66BB6A); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.coming-soon p { color: #757575; font-size: 1.1rem; }
</style>
<div class="coming-soon">
    <h1>🏭 Desa Tambang × EBT</h1>
    <p>Crosstab desa tambang vs 10 dimensi energi terbarukan</p>
    <p style="margin-top:2rem; font-size:0.9rem; color:#424242;">⏳ Halaman ini sedang dalam pengembangan</p>
</div>
""", unsafe_allow_html=True)

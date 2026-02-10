"""Shared sidebar component — imported by all pages for consistent logo & title."""
import streamlit as st
import os
def render_sidebar():
    """Render CELIOS logo and title in sidebar. Call this in every page."""
    # Path: src/components/sidebar.py -> src/components -> src -> root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    logo_path = os.path.join(base_dir, "refrensi", "Celios China-Indonesia Energy Transition.png")
    
    # Remove CSS hacks that were pushing nav down, since we are building custom nav now
    st.markdown("""
    <style>
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #66BB6A;
        text-align: center;
        padding-bottom: 20px;
        margin-bottom: 0px;
        border-bottom: 1px solid #ffffff11;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch") # Full width using new API (replaces use_container_width)
        else:
            st.warning(f"Logo not found at: {logo_path}")
            
        st.markdown('<div class="sidebar-title">Celios - Riset EBT</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Custom Navigation
        st.page_link("Dashboard.py", label="Dashboard", icon="🏠")
        
        st.markdown("### Analisis")
        st.page_link("pages/1_Overview_Nasional.py", label="Overview Nasional", icon=None)
        st.page_link("pages/2_Desa_Tambang.py", label="Desa Tambang", icon=None)
        st.page_link("pages/3_Gap_Potensi_EBT.py", label="Gap Potensi EBT", icon=None)
        st.page_link("pages/4_Ketimpangan_Energi.py", label="Ketimpangan Energi", icon=None)
        
        st.markdown("### Resources")
        st.page_link("pages/5_Eksplorasi_Data.py", label="Eksplorasi Data", icon=None)
        st.page_link("pages/6_Dokumentasi_Riset.py", label="Dokumentasi Riset", icon=None)

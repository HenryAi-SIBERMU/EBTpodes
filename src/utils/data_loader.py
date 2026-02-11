import pandas as pd
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROV_PATH = os.path.join(BASE_DIR, "data", "processed", "provinsi_agregat.csv")
NASIONAL_PATH = os.path.join(BASE_DIR, "data", "processed", "nasional_summary.csv")

@st.cache_data
def load_provincial_data():
    """Loads the provincial aggregate data."""
    if not os.path.exists(PROV_PATH):
        st.error(f"File not found: {PROV_PATH}")
        return pd.DataFrame()
    return pd.read_csv(PROV_PATH)

@st.cache_data
def load_national_data():
    """Loads the national summary data."""
    if not os.path.exists(NASIONAL_PATH):
        st.error(f"File not found: {NASIONAL_PATH}")
        return pd.DataFrame()
    return pd.read_csv(NASIONAL_PATH)

def format_number(num):
    """Formats number with thousands separator (dot)."""
    if pd.isna(num):
        return "-"
    return f"{int(num):,}".replace(",", ".")

def calculate_growth_color(growth_rate):
    """Returns 'normal' (green) for positive growth, 'inverse' (red) for negative."""
    # Assuming growth is good for Adoption.
    if growth_rate > 0:
        return "normal"
    return "inverse"

import pandas as pd
import streamlit as st
import os

def get_data_path(filename):
    """Try to find the data file in multiple location candidates."""
    # Candidate 1: Absolute path based on this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path1 = os.path.join(base_dir, "data", "processed", filename)
    
    # Candidate 2: Relative path from CWD (usually repo root in Streamlit Cloud)
    path2 = os.path.join("data", "processed", filename)
    
    # Candidate 3: Absolute path from CWD
    path3 = os.path.abspath(path2)
    
    for p in [path1, path2, path3]:
        if os.path.exists(p):
            return p
    return None

@st.cache_data
def load_provincial_data():
    """Loads the provincial aggregate data."""
    path = get_data_path("provinsi_agregat.csv")
    if not path:
        st.error(f"File not found: data/processed/provinsi_agregat.csv")
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def load_national_data():
    """Loads the national summary data."""
    path = get_data_path("nasional_summary.csv")
    if not path:
        st.error(f"File not found: data/processed/nasional_summary.csv")
        return pd.DataFrame()
    return pd.read_csv(path)

def format_number(num):
    """Formats number with thousands separator (dot)."""
    if pd.isna(num) or num == "-":
        return "-"
    try:
        return f"{int(float(num)):,}".replace(",", ".")
    except:
        return str(num)

def calculate_growth_color(growth_rate):
    """Returns 'normal' (green) for positive growth, 'inverse' (red) for negative."""
    if growth_rate > 0:
        return "normal"
    return "inverse"

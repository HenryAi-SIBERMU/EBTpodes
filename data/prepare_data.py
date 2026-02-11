import pandas as pd
import os
import re

# Configuration
BASE_DIR = os.getcwd()
RAW_EXCEL_PATH = os.path.join(BASE_DIR, "refrensi", "Data", "Rawdata", "Energi Terbarukan(AutoRecovered).xlsx")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def clean_province_name(name):
    """Normalize province names (remove excess spaces, uppercasing)."""
    if pd.isna(name): return None
    return str(name).strip().upper()

def parse_sheet_standard(df, sheet_name, value_col_name):
    """
    Parse standard BPS summary sheet.
    Assumes "Nama Provinsi" is at Row 9 (Index 8) or nearby, and data starts after.
    Target Value is usually in Column 3 or 4.
    """
    # Find the row with "Nama Provinsi"
    header_row_idx = -1
    for i in range(15):
        row_vals = df.iloc[i].astype(str).values
        if any("Nama Provinsi" in s for s in row_vals):
            header_row_idx = i
            break
    
    if header_row_idx == -1:
        print(f"Warning: Could not find header in {sheet_name}")
        return pd.DataFrame()

    # Extract Data (Skip header rows)
    # Usually data starts 2 rows after "Nama Provinsi" (because of stacked headers)
    data_start = header_row_idx + 2 
    
    # We want "Nama Provinsi" and "2024 Ada" (or similar)
    # Column mapping is tricky. Let's look at the "Ada" column under "2024".
    # Based on inspection:
    # Row 8: Nama Provinsi | 2024 | ...
    # Row 9: NaN | Ada | Tidak Ada ...
    
    # So "Ada" 2024 is likely Column 2 (Index 2) if Prov is Column 1.
    # Let's dynamically find "Ada" column under "2024"
    
    # Simply: Column 0 or 1 is Province. Column 2 or 3 is Value.
    # In 'Energi Surya-1': Prov is Col 1. 'Ada' (2024) is Col 3.
    
    # Hardcoding based on inspection for now, can be improved.
    # Col 1: Name
    # Col 3: 2024 Ada (Count)
    # Col 4: 2024 % 
    # Col 5: 2021 Total? No.
    
    slice_df = df.iloc[data_start:].copy()
    
    # Identify clean columns
    # Based on inspection of 'Energi Surya-1':
    # Col 1: Name (ACEH)
    # Col 2: 2024 Ada
    # Col 3: 2024 Tidak Ada
    # Col 4: 2024 Total
    # Col 5: 2021 Ada
    # Col 6: 2021 Tidak Ada
    # Col 7: 2021 Total
    
    try:
        # Check if sheet has enough columns
        if slice_df.shape[1] > 7:
            subset = slice_df.iloc[:, [1, 2, 3, 4, 5, 6, 7]].copy()
            subset.columns = ["Provinsi", 
                              f"{value_col_name}_2024", f"{value_col_name}_2024_no", f"{value_col_name}_2024_total",
                              f"{value_col_name}_2021", f"{value_col_name}_2021_no", f"{value_col_name}_2021_total"]
        else:
            # Fallback if 2021 is missing
            print(f"Warning: Sheet {sheet_name} has fewer columns {slice_df.shape[1]}. Extracting 2024 only.")
            subset = slice_df.iloc[:, [1, 2, 4]].copy()
            subset.columns = ["Provinsi", f"{value_col_name}_2024", f"{value_col_name}_2024_total"]
            # Add dummy 'no' column
            subset[f"{value_col_name}_2024_no"] = subset[f"{value_col_name}_2024_total"] - subset[f"{value_col_name}_2024"]
            subset[f"{value_col_name}_2021"] = 0
            subset[f"{value_col_name}_2021_no"] = 0
            subset[f"{value_col_name}_2021_total"] = 0
            
    except Exception as e:
        print(f"Error slicing {sheet_name}: {e}")
        return pd.DataFrame()
    
    # Cleaning
    subset["Provinsi"] = subset["Provinsi"].astype(str).str.strip().str.upper()
    
    # Drop NaNs/Empty
    subset = subset.dropna(subset=["Provinsi"])
    subset = subset[subset["Provinsi"] != "NAN"]
    subset = subset[subset["Provinsi"] != ""]

    # Separate National Data (In Excel it is named "TOTAL")
    nasional_df = subset[subset["Provinsi"] == "TOTAL"].copy()
    if not nasional_df.empty:
        # Rename TOTAL to NASIONAL for consistency
        nasional_df["Provinsi"] = "NASIONAL"
    else:
        # Fallback check
        nasional_df = subset[subset["Provinsi"] == "NASIONAL"].copy()

    # Filter out National/Total from main subset
    subset = subset[subset["Provinsi"] != "TOTAL"]
    subset = subset[subset["Provinsi"] != "NASIONAL"]
    subset = subset[subset["Provinsi"] != "PROVINSI"] 
    subset = subset[subset["Provinsi"] != "NASIONAL"] # double check
    
    # Convert numeric
    for col in subset.columns:
        if col != "Provinsi":
            subset[col] = pd.to_numeric(subset[col], errors='coerce').fillna(0)
    
    # Handle National Data Numeric Conversion
    if not nasional_df.empty:
        for col in nasional_df.columns:
            if col != "Provinsi":
                nasional_df[col] = pd.to_numeric(nasional_df[col], errors='coerce').fillna(0)

    # Calculate Percentage 2024 (Provincial)
    subset[f"{value_col_name}_2024_pct"] = (subset[f"{value_col_name}_2024"] / subset[f"{value_col_name}_2024_total"].replace(0, 1)) * 100
    subset[f"{value_col_name}_2024_pct"] = subset[f"{value_col_name}_2024_pct"].round(2)

    # Calculate Percentage 2021 (Provincial)
    if f"{value_col_name}_2021" in subset.columns:
        subset[f"{value_col_name}_2021_pct"] = (subset[f"{value_col_name}_2021"] / subset[f"{value_col_name}_2021_total"].replace(0, 1)) * 100
        subset[f"{value_col_name}_2021_pct"] = subset[f"{value_col_name}_2021_pct"].round(2)
        
    return subset, nasional_df

def main():
    if not os.path.exists(RAW_EXCEL_PATH):
        print(f"File not found: {RAW_EXCEL_PATH}")
        return
    
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    print("Loading Excel file...")
    xls = pd.ExcelFile(RAW_EXCEL_PATH)
    
    # Define Sheets and Indicators to extract
    # Map: Sheet Name -> Column Name to create (Prefix with PODES Code)
    tasks = {
        "Energi Surya-1": "R502a_pju_surya",     # Penerangan jalan
        "Energi Surya-2": "R501c_keluarga_surya", # Keluarga pengguna
        "Bioenergi": "R503a6_bioenergi",          # R503a.6 -> R503a6
        "Energi Air": "R510_air",               # R510-R512 -> R510 (simplified) or R510_R512
        "Desa Tambang": "tambang",               # No code in image for Tambang? Or check image again.
                                                 # Image says "10 Kerusakan lingkungan" is R514.
                                                 # Tambang galian C is often associated, but usually R... something else.
                                                 # User image doesn't show Tambang explicitly in list? 
                                                 # Oh wait, Item 1-10.
                                                 # Item 5 Kebijakan, 6 Infra, 7 Aset, 8 Akses, 9 Akses, 10 Kerusakan.
                                                 # Where is Tambang? 
                                                 # Maybe "Desa Tambang" sheet is extra? User asked "Kamu ambil dari mana".
                                                 # I will leave Tambang without code or find one.
                                                 # Actually, "Galian C" is typically separate. I'll keep "tambang" for now.
        "Akses Energi-1": "R501a2_non_pln",      # R501a.2
        "Infrastruktur Energi": "R1503a_infra",  # R1503a
        "Aset Energi Alam": "R1403g_potensi_air", # R1403g
        "Kerusakan Lingkungan": "R514_polusi_air", # R514
        "Kebijakan & Program": "R1504a_program_ebt", # R1504a
        "Akses Energi-2": "R501b_tanpa_listrik"  # R501b (Akses Energi?)
    }
    
    final_df = None
    final_nasional_df = None
    
    for sheet, col_name in tasks.items():
        if sheet in xls.sheet_names:
            print(f"Processing {sheet} -> {col_name}...")
            df_raw = pd.read_excel(xls, sheet_name=sheet, header=None)
            df_clean, df_nasional = parse_sheet_standard(df_raw, sheet, col_name)
            
            # Merge Provincial
            if final_df is None:
                final_df = df_clean
            else:
                final_df = pd.merge(final_df, df_clean, on="Provinsi", how="outer")
            
            # Merge National
            if not df_nasional.empty:
                if final_nasional_df is None:
                    final_nasional_df = df_nasional
                else:
                    final_nasional_df = pd.merge(final_nasional_df, df_nasional, on="Provinsi", how="outer")

            # Special Case: "Energi Air" has a second table (Potensi)
            if sheet == "Energi Air":
                print("Processing Energi Air Table 2 (Potensi) -> R511_potensi_air...")
                # Slice columns 11-18 (Indices: 11, 12, 13, 14, 15(pct), 16, 17, 18, 19(pct))
                # We need [11, 12, 13, 14, 16, 17, 18]
                # Re-using parse_sheet_standard but passing parsed slice? No, parse_sheet takes raw df.
                
                # Create a synthetic raw dataframe for parse_sheet_standard
                # It expects Col 1 as Prov. So we shift cols.
                # slice_df = df_raw.iloc[:, [11, 12, 13, 14, 15, 16, 17, 18]] (8 columns matches standard)
                # parse_sheet_standard expects: Prov, 24, No, Total, Pct, 21, No, Total
                
                try:
                    df_table2 = df_raw.iloc[:, [11, 12, 13, 14, 15, 16, 17, 18]].copy()
                    # Reset index or cols to 0..7
                    df_table2.columns = range(df_table2.shape[1])
                    # Insert dummy col 0 to match standard offset (since parse uses iloc[:,1:])
                    df_table2.insert(0, 'dummy', float('nan'))
                    df_table2.columns = range(df_table2.shape[1]) # re-index 0..8
                    
                    df_clean_2, df_nasional_2 = parse_sheet_standard(df_table2, "Energi Air Potensi", "R511_potensi_air")
                    
                    if final_df is not None:
                        final_df = pd.merge(final_df, df_clean_2, on="Provinsi", how="outer")
                    if final_nasional_df is not None and not df_nasional_2.empty:
                         # Rename Total matches
                         if df_nasional_2.iloc[0]["Provinsi"] == "TOTAL": df_nasional_2.iloc[0, df_nasional_2.columns.get_loc("Provinsi")] = "NASIONAL"
                         final_nasional_df = pd.merge(final_nasional_df, df_nasional_2, on="Provinsi", how="outer")

                except Exception as e:
                    print(f"Error extracting Energi Air Table 2: {e}")
        else:
            print(f"Warning: Sheet {sheet} not found.")

    # Fill NaNs
    final_df = final_df.fillna(0)
    if final_nasional_df is not None:
        final_nasional_df = final_nasional_df.fillna(0)
    
    # --- PHASE 4: IKE Calculation --- (Provincial Only)
    print("Calculating IKE Index & Growth Rates (Provincial)...")
    
    # 0. Growth Rate Calculation (Provincial)
    for col_key in tasks.values():
        val_2024 = f"{col_key}_2024"
        val_2021 = f"{col_key}_2021"
        
        if val_2024 in final_df.columns and val_2021 in final_df.columns:
            growth_col = f"{col_key}_growth"
            final_df[growth_col] = (
                (final_df[val_2024] - final_df[val_2021]) / 
                final_df[val_2021].replace(0, 1) 
            ) * 100
            final_df[growth_col] = final_df[growth_col].round(2)

    # 0b. Growth Rate Calculation (National)
    if final_nasional_df is not None:
        print("Calculating Growth Rates (National)...")
        for col_key in tasks.values():
            val_2024 = f"{col_key}_2024"
            val_2021 = f"{col_key}_2021"
            
            if val_2024 in final_nasional_df.columns and val_2021 in final_nasional_df.columns:
                growth_col = f"{col_key}_growth"
                final_nasional_df[growth_col] = (
                    (final_nasional_df[val_2024] - final_nasional_df[val_2021]) / 
                    final_nasional_df[val_2021].replace(0, 1) 
                ) * 100
                final_nasional_df[growth_col] = final_nasional_df[growth_col].round(2)
        
        # Save National CSV
        nasional_csv_path = os.path.join(PROCESSED_DIR, "nasional_summary.csv")
        final_nasional_df.to_csv(nasional_csv_path, index=False)
        print(f"Saved National Index to {nasional_csv_path}")

    # 1. Define Risk Components (Higher = More Vulnerable)
    # Convert 'Asset' (Ada) to 'Risk' (Tidak Ada) where needed
    
    # % Keluarga Tanpa Listrik (Direct Risk)
    col_tanpa_listrik = "R501b_tanpa_listrik_2024_pct"
    final_df["risk_no_electricity"] = final_df[col_tanpa_listrik] if col_tanpa_listrik in final_df.columns else 0
    
    # % Keluarga Non-PLN (Direct Risk)
    col_non_pln = "R501a2_non_pln_2024_pct"
    final_df["risk_non_pln"] = final_df[col_non_pln] if col_non_pln in final_df.columns else 0
    
    # % Desa Tanpa Program EBT (Inverse: 100 - Ada Program)
    col_program = "R1504a_program_ebt_2024_pct"
    if col_program in final_df.columns:
        final_df[col_program] = pd.to_numeric(final_df[col_program], errors='coerce').fillna(0)
        final_df["risk_no_program"] = 100 - final_df[col_program]
    else:
        final_df["risk_no_program"] = 100 

    # % Desa Tanpa Infrastruktur (Inverse: 100 - Ada Infra)
    col_infra = "R1503a_infra_2024_pct"
    if col_infra in final_df.columns:
        final_df[col_infra] = pd.to_numeric(final_df[col_infra], errors='coerce').fillna(0)
        final_df["risk_no_infra"] = 100 - final_df[col_infra]
    else:
        final_df["risk_no_infra"] = 100

    # % Desa Pencemaran Air (Direct Risk)
    col_polusi = "R514_polusi_air_2024_pct"
    final_df["risk_pollution"] = final_df[col_polusi] if col_polusi in final_df.columns else 0
    
    # 2. Normalize (Min-Max Scalling)
    risk_cols = ["risk_no_electricity", "risk_non_pln", "risk_no_program", "risk_no_infra", "risk_pollution"]
    
    # Handle case where columns might be missing if sheet failed to load
    for col in risk_cols:
        if col not in final_df.columns:
            final_df[col] = 0
            
    norm_cols = []
    for col in risk_cols:
        min_val = final_df[col].min()
        max_val = final_df[col].max()
        if max_val - min_val == 0:
            final_df[f"{col}_norm"] = 0
        else:
            final_df[f"{col}_norm"] = (final_df[col] - min_val) / (max_val - min_val)
        norm_cols.append(f"{col}_norm")
        
    # 3. Calculate IKE Score (Average of Normalized Risks * 100)
    final_df["ike_score"] = final_df[norm_cols].mean(axis=1) * 100
    final_df["ike_score"] = final_df["ike_score"].round(2)
    
    # Save
    out_path = os.path.join(PROCESSED_DIR, "provinsi_agregat.csv")
    final_df.to_csv(out_path, index=False)
    print(f"✅ Saved consolidated data to {out_path}")
    print(final_df[["Provinsi", "ike_score"]].head())

if __name__ == "__main__":
    main()

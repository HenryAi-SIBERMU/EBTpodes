import pandas as pd
import os

BASE_DIR = os.getcwd()
RAW_EXCEL_PATH = os.path.join(BASE_DIR, "refrensi", "Data", "Rawdata", "Energi Terbarukan(AutoRecovered).xlsx")

xls = pd.ExcelFile(RAW_EXCEL_PATH)
df = pd.read_excel(xls, sheet_name="Energi Air", header=None)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df.iloc[:15, :])

# Check for "Potensi" keyword in row 6-10?
# Or check columns that have data
print("\n--- Non-Null Counts ---")
print(df.count())

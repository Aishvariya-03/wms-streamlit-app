import pandas as pd
import os

# Define all file paths (change if you're in a different folder)
files = {
    'Amazon': 'Amazon.csv',
    'Flipkart': 'Flipkart.csv',
    'Flipkart-GL': 'Gl FK.csv',
    'Meesho': 'Meesho.csv',
    'Other': 'Orders_2025-01-26_2025-02-01_2025-02-04_12_12-12_17_528114.csv'
}

combined = []

for platform, filepath in files.items():
    try:
        df = pd.read_csv(filepath)
    except Exception:
        df = pd.read_csv(filepath, encoding='latin-1')  # in case of encoding issue

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Try to auto-detect SKU/MSKU and quantity
    sku_col = next((col for col in df.columns if 'msku' in col or 'sku' in col), None)
    qty_col = next((col for col in df.columns if 'quantity' in col or 'qty' in col), None)
    date_col = next((col for col in df.columns if 'date' in col), None)

    temp = pd.DataFrame()
    temp['msku'] = df[sku_col].astype(str).str.strip().str.lower() if sku_col else None
    temp['quantity'] = df[qty_col].astype(int) if qty_col else 1
    temp['date'] = pd.to_datetime(df[date_col], errors='coerce') if date_col else pd.NaT
    temp['marketplace'] = platform

    combined.append(temp)

# Combine all into one DataFrame
final_df = pd.concat(combined, ignore_index=True)

# Drop blank or invalid rows
final_df = final_df.dropna(subset=['msku'])

# Save to CSV
final_df.to_csv("all_sales.csv", index=False)
print("✅ all_sales.csv created successfully.")

# app.py
import streamlit as st
import pandas as pd
from mapping_utils import load_clean_excel, map_and_subtract

st.set_page_config(page_title="WMS Automation", layout="wide")
st.title("📦 Warehouse Management System – Auto SKU Mapper & Inventory Updater")
st.markdown("---")

# Upload inputs
sales_files = st.file_uploader("🧾 Upload Multiple Sales Files (.csv or .xlsx)", type=['csv', 'xlsx'], accept_multiple_files=True)
wms_file = st.file_uploader("🗃️ Upload WMS-04-02.xlsx", type=['xlsx'])

if sales_files and wms_file:
    # Load WMS Excel sheets
    inventory_df = load_clean_excel(wms_file, sheet_name=2)   # Sheet 3 = Inventory
    combo_df = load_clean_excel(wms_file, sheet_name=3)       # Sheet 4 = Combo Breakdown
    mapping_df = load_clean_excel(wms_file, sheet_name=4)     # Sheet 5 = SKU → MSKU

    st.write("🧾 Combo Sheet Columns:", combo_df.columns.tolist())

    all_sales = []

    for file in sales_files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        df['source'] = file.name
        all_sales.append(df)

    sales_df = pd.concat(all_sales, ignore_index=True)

    st.subheader("🔍 Sales Data Preview")
    st.dataframe(sales_df.head())

    st.subheader("📦 Inventory Before")
    st.dataframe(inventory_df.head())

    # Mapping + Subtraction
    updated_df, missing_df, logs = map_and_subtract(sales_df, mapping_df, combo_df, inventory_df)

    st.write("🧾 Detected Sales Columns:", sales_df.columns.tolist())

    st.subheader("✅ Updated Inventory")
    st.dataframe(updated_df[['msku', 'updated_qty']].head(15))

    # Download button
    csv = updated_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Updated Inventory", csv, "updated_inventory.csv", "text/csv")

    # Show missing MSKUs if any
    if not missing_df.empty:
        st.subheader("⚠️ Unmapped SKUs or Missing from Inventory")
        st.dataframe(missing_df)

    # Logs
    if logs:
        st.subheader("📋 Logs")
        for log in logs:
            if "⚠️" in log:
                st.warning(log)
            elif "❌" in log:
                st.error(log)
            else:
                st.info(log)

else:
    st.info("Please upload both a sales report and WMS Excel file to begin.")

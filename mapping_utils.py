import pandas as pd

def load_clean_excel(path_or_buffer, sheet_name):
    df = pd.read_excel(path_or_buffer, sheet_name=sheet_name, header=None)
    for i in range(len(df)):
        if df.iloc[i].astype(str).str.contains("sku", case=False).any():
            df.columns = df.iloc[i]
            return df.iloc[i + 1:].reset_index(drop=True)
    return df


def detect_column(df, possible_keywords):
    for col in df.columns:
        if any(keyword in col.lower() for keyword in possible_keywords):
            return col
    return None


def map_and_subtract(sales_df, mapping_df, combo_df, inventory_df):
    logs = []

    # Standardize columns
    sales_df.columns = sales_df.columns.str.strip().str.lower()
    mapping_df.columns = mapping_df.columns.str.strip().str.lower()
    combo_df.columns = combo_df.columns.str.strip().str.lower()
    inventory_df.columns = inventory_df.columns.str.strip().str.lower()

    # Auto-detect columns
    sku_col = detect_column(sales_df, ['msku', 'sku', 'product id', 'fsn', 'item code'])
    qty_col = detect_column(sales_df, ['quantity', 'qty', 'order qty', 'order quantity'])

    if not sku_col:
        raise ValueError(f"❌ Could not detect SKU column in sales file. Columns found: {sales_df.columns.tolist()}")

    logs.append(f"🔍 Detected SKU column: '{sku_col}'")

    sales_df['msku'] = sales_df[sku_col].astype(str).str.strip().str.lower()

    if qty_col:
        sales_df['quantity'] = sales_df[qty_col]
        logs.append(f"📦 Detected Quantity column: '{qty_col}'")
    else:
        logs.append("⚠️ Quantity column not found. Defaulting all quantities to 1.")
        sales_df['quantity'] = 1

    mapping_df['sku'] = mapping_df['sku'].astype(str).str.strip().str.lower()
    mapping_df['msku'] = mapping_df['msku'].astype(str).str.strip().str.lower()

    # Clean combo sheet
    combo_df = combo_df.loc[:, ~combo_df.columns.isna()]
    combo_df.columns = [str(col).strip() for col in combo_df.columns]

    if "Combo " in combo_df.columns:
        combo_df = combo_df.rename(columns={"Combo ": "combo"})
    elif "Combo" in combo_df.columns:
        combo_df = combo_df.rename(columns={"Combo": "combo"})

    combo_long = pd.melt(
        combo_df,
        id_vars=["combo"],
        value_vars=[col for col in combo_df.columns if col.lower().startswith("sku")],
        var_name="sku_num",
        value_name="msku"
    ).dropna()

    combo_long['combo'] = combo_long['combo'].astype(str).str.strip().str.lower()
    combo_long['msku'] = combo_long['msku'].astype(str).str.strip().str.lower()

    inventory_df['msku'] = inventory_df['msku'].astype(str).str.strip().str.lower()

    outbound = {}
    warned = set()

    for idx, row in sales_df.iterrows():
        sku = row['msku'].strip().lower() if pd.notna(row['msku']) else None
        qty = abs(int(row['quantity'])) if pd.notna(row['quantity']) else 1

        if not sku:
            continue

        if sku in combo_long['combo'].values:
            parts = combo_long[combo_long['combo'] == sku]['msku'].tolist()
            logs.append(f"🔄 Combo SKU '{sku}' split into: {parts}")
            for part in parts:
                outbound[part] = outbound.get(part, 0) + qty
        else:
            mapped = mapping_df[mapping_df['sku'] == sku]['msku']
            if mapped.empty:
                logs.append(f"⚠️ SKU '{sku}' not found in mapping — used as-is.")
            else:
                logs.append(f"🔗 SKU '{sku}' mapped to MSKU '{mapped.values[0]}'")
            msku = mapped.values[0] if not mapped.empty else sku
            outbound[msku] = outbound.get(msku, 0) + qty


    logs.append(f"📦 Outbound Summary: {len(outbound)} SKUs processed")

    # Update inventory
    updated_inventory = inventory_df.copy()
    warehouse_cols = [col for col in updated_inventory.columns if col.lower() not in ['product name', 'msku', 'opening stock', 'buffer stock']]
    updated_inventory['total_qty'] = updated_inventory[warehouse_cols].sum(axis=1)
    updated_inventory['updated_qty'] = updated_inventory['total_qty']

    missing = []
    for msku, sold_qty in outbound.items():
        if msku in updated_inventory['msku'].values:
            updated_inventory.loc[updated_inventory['msku'] == msku, 'updated_qty'] -= sold_qty
        else:
            missing.append(msku)
            logs.append(f"❌ Missing in inventory: {msku} (sold {sold_qty})")

    return updated_inventory, pd.DataFrame({'MSKU': missing}), logs

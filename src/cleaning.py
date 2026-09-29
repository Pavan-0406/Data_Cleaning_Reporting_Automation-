
from pathlib import Path
import pandas as pd
import numpy as np

NA_VALUES = ["", " ", "N/A", "NA", "n/a", "null", "NULL", "-", "#N/A"]

def load_raw_data(path):
    return pd.read_csv(path, na_values=NA_VALUES, keep_default_na=True)

def normalize_headers(df):
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df

def normalize_text(df):
    df = df.copy()
    text_cols = ["customer_id","product","category","region","channel","customer_name"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
            df[col] = df[col].replace(r"^\s*$", pd.NA, regex=True)
    for col in ["category","region","channel"]:
        if col in df.columns:
            df[col] = df[col].str.title()
    return df

def coerce_types(df):
    df = df.copy()
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for col in ["quantity","unit_price","discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def audit_data(df):
    rows = []
    for col in df.columns:
        rows.append({
            "Column": col,
            "Data Type": str(df[col].dtype),
            "Missing Count": int(df[col].isna().sum()),
            "Missing %": round(float(df[col].isna().mean()*100), 2),
            "Unique Values": int(df[col].nunique(dropna=True)),
        })
    return pd.DataFrame(rows)

def clean_data(df):
    df = df.copy()
    original_rows = len(df)
    issues = []

    duplicate_mask = df.duplicated(keep="first")
    duplicate_count = int(duplicate_mask.sum())
    if duplicate_count:
        tmp = df.loc[duplicate_mask].copy()
        tmp["Issue Type"] = "Duplicate row"
        issues.append(tmp)
        df = df.loc[~duplicate_mask].copy()

    # Required field checks
    if "order_id" in df.columns:
        missing_order = df["order_id"].isna()
        if missing_order.any():
            tmp = df.loc[missing_order].copy()
            tmp["Issue Type"] = "Missing Order ID"
            issues.append(tmp)
            df = df.loc[~missing_order].copy()

    # Missing values: numeric -> median, categorical -> mode/label
    if "unit_price" in df.columns:
        df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
    if "quantity" in df.columns:
        df["quantity"] = df["quantity"].fillna(df["quantity"].median()).round().astype(int)
    if "discount" in df.columns:
        df["discount"] = df["discount"].fillna(0)
    for col, fallback in [("customer_name","Unknown Customer"), ("region","Unassigned"),
                          ("channel","Unknown"), ("category","Uncategorized")]:
        if col in df.columns:
            mode = df[col].mode(dropna=True)
            df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else fallback)

    # Date gaps: use median date
    if "order_date" in df.columns:
        med = df["order_date"].dropna().sort_values()
        fill_date = med.iloc[len(med)//2] if len(med) else pd.Timestamp("2026-01-01")
        df["order_date"] = df["order_date"].fillna(fill_date)

    # Invalid numeric values: remove impossible transactions
    invalid_qty = df["quantity"] <= 0
    if invalid_qty.any():
        tmp = df.loc[invalid_qty].copy()
        tmp["Issue Type"] = "Invalid quantity (<= 0)"
        issues.append(tmp)
        df = df.loc[~invalid_qty].copy()

    invalid_price = df["unit_price"] <= 0
    if invalid_price.any():
        tmp = df.loc[invalid_price].copy()
        tmp["Issue Type"] = "Invalid unit price (<= 0)"
        issues.append(tmp)
        df = df.loc[~invalid_price].copy()

    # Standardize IDs
    if "customer_id" in df.columns:
        df["customer_id"] = df["customer_id"].str.upper().str.replace(r"\s+", "", regex=True)

    # Business metric
    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["discount_amount"] = df["gross_sales"] * df["discount"]
    df["net_sales"] = df["gross_sales"] - df["discount_amount"]

    # Friendly output types
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date

    issue_df = pd.concat(issues, ignore_index=True) if issues else pd.DataFrame(columns=list(df.columns)+["Issue Type"])
    summary = {
        "Raw Rows": original_rows,
        "Clean Rows": len(df),
        "Rows Removed": original_rows - len(df),
        "Duplicate Rows": duplicate_count,
        "Missing Values Handled": int(df.isna().sum().sum()),
        "Data Quality Score %": round((len(df)/original_rows)*100, 2),
    }
    return df, issue_df, summary

def run_pipeline(input_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = load_raw_data(input_path)
    raw_audit = audit_data(raw)
    df = normalize_headers(raw)
    df = normalize_text(df)
    df = coerce_types(df)
    cleaned, issues, summary = clean_data(df)
    cleaned.to_csv(output_dir/"cleaned_sales_data.csv", index=False)
    issues.to_csv(output_dir/"data_issues.csv", index=False)
    raw_audit.to_csv(output_dir/"data_quality_audit.csv", index=False)
    return cleaned, issues, raw_audit, summary

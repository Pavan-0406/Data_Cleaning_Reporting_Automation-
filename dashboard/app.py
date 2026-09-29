
import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "cleaned_sales_data.csv"

st.set_page_config(page_title="Data Quality & Reporting Hub", page_icon="📊", layout="wide")

st.markdown("""
<style>
.main {background-color:#f7f9fc;}
.block-container {padding-top: 2rem;}
.metric-card {padding: 1rem; border-radius: 12px; background: white; box-shadow: 0 2px 10px rgba(0,0,0,.06);}
</style>
""", unsafe_allow_html=True)

st.title("📊 Data Cleaning & Reporting Automation")
st.caption("Automated data quality, cleaning and business reporting dashboard")

if not DATA.exists():
    st.error("Cleaned dataset not found. Run `python src/main.py` first.")
    st.stop()

df = pd.read_csv(DATA, parse_dates=["order_date"])
df["order_date"] = pd.to_datetime(df["order_date"])

with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["region"].dropna().unique()), default=sorted(df["region"].dropna().unique()))
    categories = st.multiselect("Category", sorted(df["category"].dropna().unique()), default=sorted(df["category"].dropna().unique()))
    channels = st.multiselect("Channel", sorted(df["channel"].dropna().unique()), default=sorted(df["channel"].dropna().unique()))

filtered = df[df["region"].isin(regions) & df["category"].isin(categories) & df["channel"].isin(channels)].copy()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Net Sales", f"₹{filtered['net_sales'].sum():,.0f}")
c2.metric("Orders", f"{filtered['order_id'].nunique():,}")
c3.metric("Units Sold", f"{filtered['quantity'].sum():,.0f}")
c4.metric("Avg Order Value", f"₹{filtered['net_sales'].mean():,.0f}")

st.divider()

left, right = st.columns(2)
with left:
    monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["net_sales"].sum()
    fig = px.line(monthly, x="month", y="net_sales", markers=True, title="Monthly Net Sales")
    fig.update_layout(xaxis_title="", yaxis_title="Net Sales (₹)")
    st.plotly_chart(fig, use_container_width=True)

with right:
    cat = filtered.groupby("category", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False)
    fig = px.bar(cat, x="category", y="net_sales", title="Sales by Category", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Net Sales (₹)")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    reg = filtered.groupby("region", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False)
    fig = px.bar(reg, x="region", y="net_sales", title="Sales by Region", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

with right:
    top = filtered.groupby("product", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False).head(10)
    fig = px.bar(top.sort_values("net_sales"), x="net_sales", y="product", orientation="h", title="Top 10 Products")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Cleaned Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)

st.download_button(
    "⬇️ Download Cleaned CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="cleaned_sales_data.csv",
    mime="text/csv"
)

import streamlit as st
import pandas as pd

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
import os

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "main_data.csv")

df = pd.read_csv(file_path)

df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.title("Menu Dashboard")

min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date]
)

df = df[
    (df["order_purchase_timestamp"] >= pd.to_datetime(date_range[0])) &
    (df["order_purchase_timestamp"] <= pd.to_datetime(date_range[1]))
]

product_list = df["product_id"].unique()

selected_product = st.sidebar.multiselect(
    "Filter Produk",
    product_list
)

if selected_product:
    df = df[df["product_id"].isin(selected_product)]

# ======================
# TITLE
# ======================
st.title("WELCOME! E-Commerce Dashboard")
st.caption("Analisis sederhana penjualan & produk")

st.divider()

# ======================
# KPI SECTION (RAPI)
# ======================
col1, col2, col3, col4 = st.columns(4)

revenue = df["total_price"].sum()
orders = df["order_id"].nunique()
customers = df["customer_id"].nunique()
avg_order = revenue / orders if orders else 0

col1.metric("💰 Revenue", f"{revenue:,.0f}")
col2.metric("🧾 Orders", f"{orders:,}")
col3.metric("👤 Customers", f"{customers:,}")
col4.metric("📦 Avg Order", f"{avg_order:,.0f}")

st.divider()

# ======================
# TOP 20% CUSTOMER
# ======================

customer_revenue = df.groupby('customer_id')['total_price'].sum().sort_values(ascending=False)

top_20 = int(len(customer_revenue) * 0.2)

top_customers = customer_revenue.head(top_20)

contribution = top_customers.sum() / customer_revenue.sum() * 100

st.subheader("💰 Kontribusi 20% Pelanggan")

st.metric("Persentase Revenue", f"{contribution:.2f}%")
st.bar_chart(top_customers.head(10))

# ======================
# CHART SECTION
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sales Trend")

    monthly = df.groupby(
        df["order_purchase_timestamp"].dt.to_period("M")
    )["total_price"].sum()

    monthly.index = monthly.index.astype(str)

    st.line_chart(monthly)

with col2:
    st.subheader("🛒 Top Produk")

    top_products = df.groupby("product_id")["total_price"] \
        .sum() \
        .sort_values(ascending=False) \
        .head(7)

    st.bar_chart(top_products)

st.divider()

# ======================
# DATA SECTION (EXPANDER BIAR RAPI)
# ======================
with st.expander("📋 Lihat Data Mentah"):
    st.dataframe(df, use_container_width=True)

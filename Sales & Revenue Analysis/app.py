import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Sales & Revenue Dashboard", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")

# Load dataset
data = pd.read_csv("superstore_dataset.csv")

# Convert date column
data["order_date"] = pd.to_datetime(data["order_date"])

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=data["region"].unique(),
    default=data["region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=data["category"].unique(),
    default=data["category"].unique()
)

segment = st.sidebar.multiselect(
    "Select Segment",
    options=data["segment"].unique(),
    default=data["segment"].unique()
)

# Filter dataset
filtered_data = data[
    (data["region"].isin(region)) &
    (data["category"].isin(category)) &
    (data["segment"].isin(segment))
]

# -----------------------------
# KPI METRICS
# -----------------------------
total_sales = filtered_data["sales"].sum()
total_profit = filtered_data["profit"].sum()
total_quantity = filtered_data["quantity"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Quantity Sold", int(total_quantity))

st.markdown("---")

# -----------------------------
# SALES BY CATEGORY
# -----------------------------
sales_category = filtered_data.groupby("category")["sales"].sum().reset_index()

fig1 = px.bar(
    sales_category,
    x="category",
    y="sales",
    color="category",
    title="Sales by Category"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# SALES BY REGION
# -----------------------------
sales_region = filtered_data.groupby("region")["sales"].sum().reset_index()

fig2 = px.pie(
    sales_region,
    names="region",
    values="sales",
    title="Sales by Region"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TOP PRODUCTS
# -----------------------------
top_products = (
    filtered_data.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="sales",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# SALES TREND
# -----------------------------
sales_trend = (
    filtered_data.groupby("order_date")["sales"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    sales_trend,
    x="order_date",
    y="sales",
    title="Sales Trend Over Time"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# SALES BY STATE
# -----------------------------
sales_state = filtered_data.groupby("state")["sales"].sum().reset_index()

fig5 = px.bar(
    sales_state.sort_values(by="sales", ascending=False).head(10),
    x="state",
    y="sales",
    title="Top States by Sales"
)

st.plotly_chart(fig5, use_container_width=True)
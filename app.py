import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Deals Dashboard", layout="wide")
st.title("📊 Complete Deals Dashboard")

# --- Load CSV directly from repo ---
try:
    df = pd.read_csv("Complete Deals Data.csv", encoding='latin1')
except FileNotFoundError:
    st.error("CSV file not found. Make sure 'Complete Deals Data.csv' exists in the repo.")
    st.stop()

# --- Data Cleaning ---
df['status'] = df['status'].astype(str)
df['Pipeline Name'] = df['Pipeline Name'].astype(str)
df['Value(AUD)'] = pd.to_numeric(df['Value(AUD)'], errors='coerce')

# --- Filter: Pipeline Name ---
st.markdown("### 🛠️ Filter by Pipeline Name")
unique_pipelines = df['Pipeline Name'].dropna().unique().tolist()

selected_pipelines = st.multiselect(
    "Select Pipeline(s)",
    options=unique_pipelines,
    default=unique_pipelines
)

# --- Filter Data ---
filtered_df = df[df['Pipeline Name'].isin(selected_pipelines)]

# --- Chart 1: Deal Count by Status ---
count_chart = (
    filtered_df.groupby("status")["Deals ID"]
    .count()
    .reset_index()
    .rename(columns={"Deals ID": "Deal Count"})
    .sort_values("Deal Count", ascending=True)
)

fig_count = px.bar(
    count_chart,
    x="Deal Count",
    y="status",
    orientation='h',
    title="Number of Deals by Status"
)

# --- Chart 2: Value(AUD) by Status ---
value_chart = (
    filtered_df.groupby("status")["Value(AUD)"]
    .sum()
    .reset_index()
    .rename(columns={"Value(AUD)": "Total Value (AUD)"})
    .sort_values("Total Value (AUD)", ascending=True)
)

fig_value = px.bar(
    value_chart,
    x="Total Value (AUD)",
    y="status",
    orientation='h',
    title="Total Value (AUD) by Status"
)

# --- Mobile-friendly horizontal chart layout ---
st.markdown(
    """
    <style>
    .scroll-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding-bottom: 10px;
    }
    .chart-box {
        min-width: 400px;
        flex-shrink: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Filter stays on top, then horizontally scrollable chart row
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.plotly_chart(fig_count, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.plotly_chart(fig_value, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

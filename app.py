import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Deals Dashboard", layout="wide")
st.title("🎯 Deals Insights - Step 1")

# Upload CSV
uploaded_file = st.file_uploader("Upload 'Complete Deals Data.csv'", type="csv")

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file, encoding='latin1')

    # Clean up
    df['status'] = df['status'].astype(str)
    df['Pipeline Name'] = df['Pipeline Name'].astype(str)
    df['Value(AUD)'] = pd.to_numeric(df['Value(AUD)'], errors='coerce')

    # --- Horizontal Pipeline Filter ---
    st.markdown("### 🛠️ Filter by Pipeline Name")
    unique_pipelines = df['Pipeline Name'].dropna().unique().tolist()
    selected_pipelines = st.multiselect(
        "",
        options=unique_pipelines,
        default=unique_pipelines,
        format_func=lambda x: f"  {x}  ",  # Padding for rounded look
        label_visibility="collapsed"
    )

    # Filter data based on pipeline selection
    filtered_df = df[df['Pipeline Name'].isin(selected_pipelines)]

    # --- Chart 1: Count of Deals ID by Status ---
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

    # --- Chart 2: Sum of AUD by Status ---
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

    # Display side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_count, use_container_width=True)
    with col2:
        st.plotly_chart(fig_value, use_container_width=True)

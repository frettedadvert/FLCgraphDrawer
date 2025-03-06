import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit App Title
st.title("📊 FLC-Interactive Data Visualizer")

# Upload dataset
uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

    st.write("### Dataset Preview")
    st.write(df.head())  # Show first few rows

    # Dropdowns for selecting X and Y axes
    x_axis = st.selectbox("📌 Select X-axis (e.g., Datum)", df.columns)
    y_axis_options = st.multiselect("📌 Select Y-axis (Multiple Allowed)", df.columns)

    # Multi-filter selection
    filter_columns = st.multiselect("🔍 Select columns to filter by (e.g., Heim, Teilgericht)", df.columns)

    # Create filter inputs dynamically
    filters = {}
    for col in filter_columns:
        unique_values = df[col].dropna().unique().tolist()
        selected_values = st.multiselect(f"Select values for {col}", unique_values)
        if selected_values:
            filters[col] = selected_values

    # Apply multiple filters
    for col, values in filters.items():
        df = df[df[col].astype(str).isin(values)]

    # Draw graph if selections are made
    if x_axis and y_axis_options:
        # Use color grouping based on the first selected filter column
        color_column = filter_columns[0] if filter_columns else None

        for y in y_axis_options:
            fig = px.line(df, x=x_axis, y=y, color=color_column, title=f"📈 {', '.join(y_axis_options)} over {x_axis}")

            # Show the graph
            st.plotly_chart(fig)

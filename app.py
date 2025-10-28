

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="StabiTrack", layout="wide")

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
    <style>
        /* Whole page background and font */
        body {
            background: radial-gradient(circle at top left, #03303f, #011820, #000c13);
            color: #266CA9;
            font-family: 'Inter', sans-serif;
        }

        .main {
            background: radial-gradient(circle at top left, #002733, #00141c 70%);
            color: #bffcff;
        }

        /* Sidebar style */
        [data-testid="stSidebar"] {
            background: radial-gradient(circle at top left, #011b24, #022b38, #031f2a);
            color: #b8f3f6;
            border-right: 1px solid rgba(0, 255, 255, 0.08);
            box-shadow: inset -4px 0 20px rgba(0, 255, 255, 0.05);
        }

        [data-testid="stSidebar"] h2 {
            color: #00eaff;
            font-weight: 700;
            font-size: 1.4rem;
            text-shadow: 0 0 8px rgba(0, 238, 255, 0.4);
        }

        /* Header */
        .title {
            font-size: 46px !important;
            font-weight: 800 !important;
            color: #5ef3ff;
            text-align: left;
            text-shadow: 0 0 18px rgba(0, 255, 255, 0.35);
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }

        .subtitle {
            text-align: left;
            font-size: 18px;
            color: #9beaff;
            font-weight: 400;
            margin-bottom: 35px;
            letter-spacing: 0.3px;
        }

        /* Metric cards */
        .metric-card {
            background: linear-gradient(145deg, #01232d, #02313f);
            padding: 28px;
            border-radius: 18px;
            text-align: center;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.07);
            border: 1px solid rgba(0, 255, 255, 0.12);
            transition: all 0.3s ease-in-out;
        }

        .metric-card:hover {
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.25);
            transform: translateY(-2px);
        }

        .metric-card h1 {
            color: #6ff9ff;
            font-size: 38px;
            font-weight: 800;
            text-shadow: 0 0 15px rgba(111, 249, 255, 0.35);
            margin-bottom: 6px;
        }

        .metric-card p {
            color: #9feaff;
            font-size: 15px;
            letter-spacing: 0.4px;
            margin-top: 0;
        }

        .metric-card h3 {
            color: #9feaff;
            font-size: 17px;
            font-weight: 500;
            margin-top: 4px;
            letter-spacing: 0.3px;
        }

        /* Section headers */
        h3 {
            color: #6ff9ff !important;
            text-shadow: 0 0 14px rgba(111, 249, 255, 0.35);
            font-weight: 600 !important;
            letter-spacing: 0.4px;
        }

        /* Data table styling */
        .stDataFrame {
            background-color: rgba(2, 35, 45, 0.7) !important;
            color: #bdf8ff !important;
            border-radius: 12px !important;
            border: 1px solid rgba(0, 255, 255, 0.08);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.05);
        }

        /* Plot background */
        .plotly-graph-div {
            background: radial-gradient(circle at center, rgba(0, 36, 46, 0.9), rgba(1, 18, 26, 1)) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(0, 255, 255, 0.06);
            box-shadow: 0 0 18px rgba(0, 255, 255, 0.07);
        }

        /* Divider line */
        hr {
            border: 0.6px solid rgba(0, 255, 255, 0.12);
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- LOAD DATA ----------------------
DATA_PATH = "data/labeled_data.csv"
df = pd.read_csv(DATA_PATH)

required_cols = ["Mine", "Ndvi", "Slope", "Rainfall", "Label", "Year", "FoS"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column in CSV: {col}")
        st.stop()

# ---------------------- SIDEBAR FILTERS ----------------------
st.sidebar.header("🔹 Filters")
selected_mine = st.sidebar.selectbox("Select Mine", sorted(df["Mine"].unique()))
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()), int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)
filtered = df[(df["Mine"] == selected_mine) &
              (df["Year"].between(year_range[0], year_range[1]))]

# ---------------------- HEADER ----------------------
st.markdown("<h1 class='title'>StabiTrack</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Interactive visualization of slope stability parameters across mines</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------- METRIC CARDS ----------------------
col1, col2, col3 = st.columns(3)
years_analyzed = filtered["Year"].nunique()
avg_fos = filtered["FoS"].mean()
avg_slope = filtered["Slope"].mean()

with col1:
    st.markdown(f"<div class='metric-card'><h1>{years_analyzed}</h1><h3>Years Analyzed</h3></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h1>{avg_fos:.2f}</h1><h3>Average FoS</h3></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h1>{avg_slope:.2f}</h1><h3>Average Slope</h3></div>", unsafe_allow_html=True)

# ---------------------- TREND GRAPHS ----------------------
st.markdown("### FoS & NDVI Trends")

col4, col5 = st.columns(2)

# FoS Trend
with col4:
    fig_fos = px.line(filtered, x="Year", y="FoS", title="FoS Trend Over Years",
                      markers=True, color_discrete_sequence=["#00eaff"])
    fig_fos.update_traces(line=dict(width=3))
    fig_fos.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#bffcff"),
        title_font=dict(size=20, color="#00f5ff"),
    )
    st.plotly_chart(fig_fos, use_container_width=True)

# NDVI Trend
with col5:
    fig_ndvi = px.line(filtered, x="Year", y="Ndvi", title="NDVI Trend Over Years",
                       markers=True, color_discrete_sequence=["#00baff"])
    fig_ndvi.update_traces(line=dict(width=3))
    fig_ndvi.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#bffcff"),
        title_font=dict(size=20, color="#00f5ff"),
    )
    st.plotly_chart(fig_ndvi, use_container_width=True)

# ---------------------- DATA TABLE ----------------------
st.markdown("### Data Table")
st.dataframe(filtered[["Mine", "Ndvi", "Slope", "Rainfall", "Label", "FoS", "Year"]],
             use_container_width=True)

# ---------------------- FOOTER ----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00eaff;'>© 2025 | StabiTrack | Aqua Glow Theme</p>", unsafe_allow_html=True)

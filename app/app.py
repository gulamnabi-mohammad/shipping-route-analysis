import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis import load_and_process_data, get_route_analysis

# Load data
df = load_and_process_data()

# Title
st.title("🚚 Shipping Route Efficiency Dashboard")

# ---------------- KPI SECTION ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Avg Lead Time", round(df['Lead Time'].mean(), 2))
col2.metric("Total Orders", df.shape[0])
col3.metric("Max Lead Time", df['Lead Time'].max())

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect("Select Region", df['Region'].unique())
ship_mode = st.sidebar.multiselect("Ship Mode", df['Ship Mode'].unique())

if region:
    df = df[df['Region'].isin(region)]

if ship_mode:
    df = df[df['Ship Mode'].isin(ship_mode)]

# ---------------- STATE ANALYSIS ----------------
st.subheader("📊 Average Lead Time by State")

state_avg = df.groupby('State/Province')['Lead Time'].mean().reset_index()

fig1 = px.bar(state_avg,
              x='State/Province',
              y='Lead Time',
              title="Average Lead Time by State")

st.plotly_chart(fig1)

# ---------------- SHIP MODE ANALYSIS ----------------
st.subheader("🚀 Ship Mode Performance")

ship_avg = df.groupby('Ship Mode')['Lead Time'].mean().reset_index()

fig2 = px.bar(ship_avg,
              x='Ship Mode',
              y='Lead Time',
              title="Lead Time by Ship Mode")

st.plotly_chart(fig2)

# ---------------- BOTTLENECK ANALYSIS ----------------
st.subheader("⚠️ Bottleneck Detection")

bottle = df.groupby('State/Province').agg({
    'Lead Time': 'mean',
    'Order ID': 'count'
}).reset_index()

fig3 = px.scatter(bottle,
                  x='Order ID',
                  y='Lead Time',
                  size='Order ID',
                  hover_name='State/Province',
                  title="High Volume vs High Delay States")

st.plotly_chart(fig3)

# ---------------- ROUTE ANALYSIS ----------------
st.subheader("🏆 Top 10 Efficient Routes")

top_routes, worst_routes = get_route_analysis(df)
st.dataframe(top_routes)

st.subheader("⚠️ Worst 10 Routes")

st.dataframe(worst_routes)
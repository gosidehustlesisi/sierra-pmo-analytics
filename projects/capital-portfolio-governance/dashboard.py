#!/usr/bin/env python3
"""
Capital Portfolio Governance Dashboard
Streamlit application for visualizing $300M+ transit capital programs.

Data sources:
- USASpending.gov: Federal grant awards (FTA, FHWA)
- FTA NTD: Capital expenses by transit agency
- WMATA: Capital improvement program (documented)
- EVM Analysis: CPI, SPI, EAC, VAC metrics
- Variance Analysis: Budget vs actual tracking

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Capital Portfolio Governance", layout="wide")

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"

st.title("Capital Portfolio Governance Dashboard")
st.markdown("**Tracking $300M+ federal transit capital programs**")
st.markdown("*Data: USASpending.gov | FTA NTD | WMATA Capital Program*")

# Load data
@st.cache_data
def load_data():
    datasets = {}
    # USASpending
    usaspending = DATA_DIR / "usaspending_transit_grants.csv"
    if usaspending.exists():
        datasets["usaspending"] = pd.read_csv(usaspending)
    # EVM
    evm = DATA_DIR / "evm_analysis.csv"
    if evm.exists():
        datasets["evm"] = pd.read_csv(evm)
    # Variance
    variance = DATA_DIR / "variance_analysis.csv"
    if variance.exists():
        datasets["variance"] = pd.read_csv(variance)
    # NTD
    ntd = DATA_DIR / "ntd_capital_expenses.csv"
    if ntd.exists():
        datasets["ntd"] = pd.read_csv(ntd)
    return datasets

data = load_data()

# Portfolio Overview
st.header("Portfolio Overview")
col1, col2, col3, col4 = st.columns(4)

if "usaspending" in data:
    df = data["usaspending"]
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    total = df["amount"].sum()
    count = len(df)
    agencies = df["awarding_sub_agency"].nunique()

    col1.metric("Total Obligations", f"${total/1e9:.1f}B")
    col2.metric("Active Awards", count)
    col3.metric("Funding Agencies", agencies)
    col4.metric("States", df["place_of_performance_state"].nunique())
else:
    st.warning("Run `python src/download_usaspending.py` to load portfolio data.")

# Tabs for detailed views
tab1, tab2, tab3, tab4 = st.tabs(["Award Distribution", "EVM Metrics", "Variance Tracking", "Agency Analysis"])

with tab1:
    if "usaspending" in data:
        df = data["usaspending"]
        st.subheader("Award Amount Distribution")
        fig = px.histogram(df, x="amount", color="awarding_sub_agency",
                           nbins=50, log_x=True,
                           title="Federal Transit Grant Distribution (Log Scale)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top Recipients")
        top_recipients = df.groupby("recipient")["amount"].sum().nlargest(10).reset_index()
        fig2 = px.bar(top_recipients, x="amount", y="recipient",
                      orientation="h", title="Top 10 Recipients by Total Obligations")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Awards by State")
        state_data = df.groupby("place_of_performance_state")["amount"].sum().reset_index()
        fig3 = px.choropleth(state_data, locations="place_of_performance_state",
                             locationmode="USA-states", color="amount",
                             scope="usa", title="Transit Grants by State")
        st.plotly_chart(fig3, use_container_width=True)

with tab2:
    if "evm" in data:
        evm_df = data["evm"]
        st.subheader("Earned Value Management Metrics")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Avg CPI", f"{evm_df['cpi'].mean():.3f}")
        col_b.metric("Avg SPI", f"{evm_df['spi'].mean():.3f}")
        col_c.metric("Total VAC", f"${evm_df['vac'].sum()/1e6:.1f}M")

        # CPI/SPI scatter
        fig = px.scatter(evm_df, x="spi", y="cpi", color="health_status",
                         size="bac", hover_data=["award_id", "recipient"],
                         title="CPI vs SPI by Project")
        fig.add_hline(y=1.0, line_dash="dash", line_color="red")
        fig.add_vline(x=1.0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)

        # EAC distribution
        fig2 = px.histogram(evm_df, x="eac", color="health_status",
                            title="Estimate at Completion Distribution")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Run `python src/evm_calculator.py` to generate EVM data.")

with tab3:
    if "variance" in data:
        var_df = data["variance"]
        st.subheader("Budget vs Actual Variance")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Over Budget Count", len(var_df[var_df["over_budget"]]))
        col_b.metric("Avg Variance %", f"{var_df['variance_pct'].mean():.1f}%")
        col_c.metric("Total Variance", f"${var_df['variance'].sum()/1e6:.1f}M")

        # Variance by agency
        fig = px.box(var_df, x="awarding_sub_agency", y="variance_pct",
                     title="Variance % by Agency")
        st.plotly_chart(fig, use_container_width=True)

        # Budget burn-down
        var_sorted = var_df.sort_values("project_progress_pct")
        fig2 = px.scatter(var_sorted, x="project_progress_pct", y="variance_pct",
                          color="over_budget", size="budget",
                          title="Variance vs Project Progress")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Run `python src/variance_reporter.py` to generate variance data.")

with tab4:
    if "usaspending" in data:
        df = data["usaspending"]
        st.subheader("Agency Analysis")

        agency_summary = df.groupby("awarding_sub_agency").agg({
            "amount": ["sum", "mean", "count"]
        }).reset_index()
        agency_summary.columns = ["agency", "total", "average", "count"]
        st.dataframe(agency_summary, use_container_width=True)

        fig = px.pie(agency_summary, values="total", names="agency",
                     title="Total Obligations by Agency")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Load USASpending data first.")

st.markdown("---")
st.markdown("*Dashboard built with real data from USASpending.gov, FTA NTD, and WMATA public sources.*")

#!/usr/bin/env python3
"""
Executive Decision Support Dashboard
Streamlit application for municipal strategic planning.

Data sources:
- Census ACS: DC demographics, income, poverty
- BLS: Employment, unemployment, wages
- DC Open Data: Agency budgets and performance
- Scenario Engine: What-if budget modeling
- ROI Calculator: Program investment analysis
- Briefing Generator: Auto-generated executive memos

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Executive Decision Support", layout="wide")

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"

st.title("Executive Decision Support Dashboard")
st.markdown("**Municipal strategic planning tools for data-driven governance**")
st.markdown("*Data: Census ACS | BLS | DC Open Data | USASpending.gov*")

# Load data
@st.cache_data
def load_data():
    datasets = {}
    for name, path in [
        ("census", "census_dc_demographics.csv"),
        ("bls", "bls_dc_employment.csv"),
        ("roi", "roi_analysis.csv"),
        ("scenario", "scenario_analysis.csv"),
        ("sensitivity", "sensitivity_analysis.csv"),
    ]:
        fp = DATA_DIR / path
        if fp.exists():
            datasets[name] = pd.read_csv(fp)
    # Briefing
    briefing = DATA_DIR / "mayor_briefing_latest.md"
    if briefing.exists():
        datasets["briefing"] = briefing.read_text()
    return datasets

data = load_data()

# Executive Overview
st.header("Executive Overview")
col1, col2, col3, col4 = st.columns(4)

if "census" in data:
    census = data["census"]
    if "population" in census.columns:
        col1.metric("DC Population", f"{census['population'].iloc[0]:,.0f}")
    if "median_income" in census.columns:
        col2.metric("Median Income", f"${census['median_income'].iloc[0]:,.0f}")
    if "poverty_rate" in census.columns:
        col3.metric("Poverty Rate", f"{census['poverty_rate'].iloc[0]:.1f}%")
    if "median_age" in census.columns:
        col4.metric("Median Age", f"{census['median_age'].iloc[0]:.1f}")
else:
    st.warning("Run data downloaders to populate metrics.")

if "bls" in data:
    bls = data["bls"]
    if "metric" in bls.columns:
        unemp = bls[bls["metric"] == "dc_unemployment_rate"]
        if not unemp.empty:
            latest = unemp.iloc[-1]
            col1.metric("Unemployment", f"{latest['value']}%", delta=f"{latest['period_name']} {latest['year']}")

tab1, tab2, tab3, tab4 = st.tabs(["Demographics", "Scenario Modeling", "ROI Analysis", "Briefing Preview"])

with tab1:
    if "census" in data:
        census = data["census"]
        st.subheader("DC Demographics")
        
        cols = [c for c in ["population", "median_income", "median_age", "poverty_rate", "homeownership_rate", "median_commute_minutes"] if c in census.columns]
        if cols:
            st.dataframe(census[["name"] + cols], use_container_width=True)
        
        if "poverty_rate" in census.columns and "median_income" in census.columns:
            fig = px.scatter(census, x="poverty_rate", y="median_income",
                           size="population" if "population" in census.columns else None,
                           hover_data=["name"],
                           title="Poverty Rate vs Median Income")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run `python src/download_census_exec.py` for demographic data.")

with tab2:
    if "scenario" in data:
        scenario = data["scenario"]
        st.subheader("Budget Scenario Modeling")
        
        # Interactive sliders
        st.markdown("**Adjust agency budgets (+/- 10%)**")
        
        agencies = scenario["agency"].unique()
        for agency in agencies:
            baseline = scenario[(scenario["scenario"] == "Baseline") & (scenario["agency"] == agency)]
            if not baseline.empty:
                base_budget = baseline["budget"].iloc[0]
                pct = st.slider(f"{agency}", -10, 10, 0, 1)
                new_budget = base_budget * (1 + pct/100)
                st.write(f"  ${new_budget/1e6:.0f}M ({pct:+.0f}%)")
        
        # Comparison chart
        fig = px.bar(scenario, x="agency", y="budget", color="scenario",
                    barmode="group", title="Budget by Agency Across Scenarios")
        st.plotly_chart(fig, use_container_width=True)
        
        if "sensitivity" in data:
            sens = data["sensitivity"]
            st.subheader("Sensitivity Analysis")
            fig2 = px.line(sens, x="budget_change_pct", y="projected",
                          color="agency", facet_col="metric",
                          title="Outcome Sensitivity to Budget Changes")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Run `python src/scenario_engine.py` for scenario data.")

with tab3:
    if "roi" in data:
        roi = data["roi"]
        st.subheader("Program Investment ROI")
        
        fig = px.scatter(roi, x="irr_pct", y="net_present_value_3pct",
                        size="initial_cost", color="program",
                        title="IRR vs NPV by Program")
        st.plotly_chart(fig, use_container_width=True)
        
        fig2 = px.bar(roi, x="program", y="roi_pct",
                     color="payback_years",
                     title="ROI by Program")
        st.plotly_chart(fig2, use_container_width=True)
        
        st.dataframe(roi[["program", "initial_cost", "roi_pct", "irr_pct", "payback_years", "net_present_value_3pct"]],
                    use_container_width=True)
    else:
        st.info("Run `python src/roi_calculator.py` for ROI analysis.")

with tab4:
    if "briefing" in data:
        st.subheader("Latest Executive Briefing")
        st.markdown(data["briefing"])
        
        # Export option
        st.download_button(
            label="Download Briefing (Markdown)",
            data=data["briefing"],
            file_name=f"mayor_briefing_{pd.Timestamp.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
    else:
        st.info("Run `python src/briefing_generator.py` to generate briefing.")

st.markdown("---")
st.markdown("*Dashboard built with real data from Census ACS, BLS, DC Open Data, and USASpending.gov.*")

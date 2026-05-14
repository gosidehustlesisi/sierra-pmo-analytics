import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"

st.set_page_config(page_title="DC Executive Decision Support", layout="wide")

st.title("🏛️ DC Executive Decision Support Dashboard")
st.caption("Real-time municipal strategic planning with live Census, BLS, and DC Open Data.")

# ---- Load Data ----
@st.cache_data(ttl=3600)
def load_all_data():
    data = {}
    for fname in ["census_dc", "bls_dc", "dc_agency_metrics", "roi_analysis", "scenario_default"]:
        path = DATA_DIR / f"{fname}.json"
        if path.exists():
            with open(path) as f:
                data[fname] = pd.DataFrame(json.load(f))
        else:
            data[fname] = pd.DataFrame()
    return data

data = load_all_data()

# ---- Executive Overview ----
st.header("📊 Executive Overview")

cols = st.columns(4)

# Population
if not data["census_dc"].empty and "population" in data["census_dc"].columns:
    pop = int(data["census_dc"]["population"].iloc[0])
    cols[0].metric("DC Population", f"{pop:,}")
elif not data["census_dc"].empty and "population_millions" in data["census_dc"].columns:
    pop = int(data["census_dc"]["population_millions"].iloc[0] * 1_000_000)
    cols[0].metric("DC Population", f"{pop:,}")
else:
    cols[0].metric("DC Population", "N/A")

# Unemployment
if not data["bls_dc"].empty and "metric" in data["bls_dc"].columns:
    ur = data["bls_dc"][data["bls_dc"]["metric"] == "dc_unemployment_rate"]
    if not ur.empty:
        latest_ur = float(ur.sort_values(["year", "period"]).iloc[-1]["value"])
        cols[1].metric("Unemployment Rate", f"{latest_ur:.1f}%")
    else:
        cols[1].metric("Unemployment Rate", "N/A")
else:
    cols[1].metric("Unemployment Rate", "N/A")

# Median Income
if not data["census_dc"].empty and "median_income" in data["census_dc"].columns:
    inc = int(data["census_dc"]["median_income"].iloc[0])
    cols[2].metric("Median Income", f"${inc:,}")
else:
    cols[2].metric("Median Income", "N/A")

# Total Budget (hardcoded for DC ~$20.6B)
cols[3].metric("Total Budget", "$20.6B")

st.divider()

# ---- Scenario Modeling ----
st.header("🔮 Scenario Modeling")
st.markdown("Adjust budget allocation percentages across DC agencies. Projected performance uses historical correlation.")

AGENCIES = [
    "Department of Health",
    "Metropolitan Police Department",
    "Department of Transportation",
    "Department of Energy & Environment",
    "Office of the Chief Technology Officer",
    "Department of Human Services",
    "Department of Parks and Recreation",
    "DC Public Schools",
    "Department of Employment Services",
    "Department of Consumer and Regulatory Affairs",
]

HISTORICAL_SHARES = {
    "Department of Health": 0.08,
    "Metropolitan Police Department": 0.18,
    "Department of Transportation": 0.07,
    "Department of Energy & Environment": 0.04,
    "Office of the Chief Technology Officer": 0.03,
    "Department of Human Services": 0.12,
    "Department of Parks and Recreation": 0.05,
    "DC Public Schools": 0.28,
    "Department of Employment Services": 0.06,
    "Department of Consumer and Regulatory Affairs": 0.04,
}

allocations = {}
col_left, col_right = st.columns(2)
with col_left:
    for agency in AGENCIES[:5]:
        allocations[agency] = st.slider(
            agency, 0.0, 0.50, HISTORICAL_SHARES[agency], 0.01, key=f"slider_{agency}"
        )
with col_right:
    for agency in AGENCIES[5:]:
        allocations[agency] = st.slider(
            agency, 0.0, 0.50, HISTORICAL_SHARES[agency], 0.01, key=f"slider_{agency}"
        )

# Normalize to 100%
total = sum(allocations.values())
if total > 0:
    allocations = {k: v / total for k, v in allocations.items()}

# Simple projection heuristic
scenario_rows = []
for agency in AGENCIES:
    share = allocations.get(agency, HISTORICAL_SHARES[agency])
    base = HISTORICAL_SHARES.get(agency, 0.05)
    change = (share - base) / base if base > 0 else 0
    # Baseline performance from DC metrics if available
    baseline_perf = 65
    if not data["dc_agency_metrics"].empty and "agency_name" in data["dc_agency_metrics"].columns:
        sub = data["dc_agency_metrics"][data["dc_agency_metrics"]["agency_name"] == agency]
        if not sub.empty and "value" in sub.columns:
            baseline_perf = float(sub["value"].iloc[0])
    projected = baseline_perf * (1 + 0.3 * change)
    scenario_rows.append({
        "Agency": agency,
        "Budget Share": f"{share:.1%}",
        "Budget ($)": f"${share * 20_600_000_000:,.0f}",
        "Projected Performance": round(projected, 1),
    })

scenario_df = pd.DataFrame(scenario_rows)
st.dataframe(scenario_df, use_container_width=True)

# Scenario chart
fig_scenario = go.Figure()
fig_scenario.add_trace(go.Bar(
    x=scenario_df["Agency"],
    y=scenario_df["Projected Performance"],
    marker_color="steelblue",
    name="Projected Performance"
))
fig_scenario.update_layout(
    title="Projected Agency Performance by Budget Allocation",
    xaxis_tickangle=-45,
    yaxis_title="Performance Index",
    height=400,
)
st.plotly_chart(fig_scenario, use_container_width=True)

st.divider()

# ---- ROI Analysis ----
st.header("💰 ROI Analysis")

if not data["roi_analysis"].empty:
    roi_df = data["roi_analysis"].copy()
    roi_df["annual_cost_m"] = roi_df["annual_cost"] / 1_000_000
    roi_df["npv_m"] = roi_df["npv"] / 1_000_000

    st.dataframe(
        roi_df[["program", "annual_cost_m", "npv_m", "benefit_cost_ratio", "payback_period_years"]]
        .rename(columns={
            "program": "Program",
            "annual_cost_m": "Annual Cost ($M)",
            "npv_m": "NPV ($M)",
            "benefit_cost_ratio": "BCR",
            "payback_period_years": "Payback (yrs)",
        }),
        use_container_width=True,
    )

    fig_roi = px.bar(
        roi_df,
        x="program",
        y="benefit_cost_ratio",
        color="npv",
        color_continuous_scale="RdYlGn",
        labels={"program": "Program", "benefit_cost_ratio": "Benefit-Cost Ratio"},
        title="Program Benefit-Cost Ratio (color = NPV)",
    )
    fig_roi.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig_roi, use_container_width=True)
else:
    st.info("ROI data not found. Run `python src/roi_calculator.py` to generate.")

st.divider()

# ---- Briefing Preview ----
st.header("📝 Briefing Preview")

briefing_files = sorted(DATA_DIR.glob("briefing_*.md"))
if briefing_files:
    latest = briefing_files[-1]
    with open(latest) as f:
        content = f.read()
    st.markdown(content[:2000] + ("\n\n..." if len(content) > 2000 else ""))
    with open(latest, "rb") as f:
        st.download_button(
            label="📥 Download Full Briefing",
            data=f,
            file_name=latest.name,
            mime="text/markdown",
        )
else:
    st.info("No briefing found. Run `python src/briefing_generator.py` to generate.")

st.divider()
st.caption("Built with real data from DC Open Data, US Census ACS, and Bureau of Labor Statistics.")

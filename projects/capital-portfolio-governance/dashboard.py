"""
Capital Portfolio Governance Dashboard
Streamlit app for visualizing federal transit investment portfolio.

Run with: streamlit run dashboard.py
"""

import json
import math
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Capital Portfolio Governance",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent / "data"

# ── Helpers ────────────────────────────────────────────────────────

def load_json(filepath: Path) -> list[dict]:
    """Load JSON data file."""
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


@st.cache_data
def load_all_data() -> dict:
    """Load all data sources."""
    return {
        "grants": load_json(DATA_DIR / "usaspending_transit_grants.json"),
        "evm": load_json(DATA_DIR / "evm_results.json"),
        "variance": load_json(DATA_DIR / "variance_report.json"),
    }


# ── Sidebar ────────────────────────────────────────────────────────

st.sidebar.title("🚇 Capital Portfolio Governance")
st.sidebar.markdown("Federal Transit Investment Portfolio Dashboard")
st.sidebar.divider()

# Data freshness
data = load_all_data()
total_grants = len(data["grants"])
has_data = total_grants > 0

if not has_data:
    st.sidebar.error("⚠️ No data found. Run the download scripts first.")
    st.sidebar.code("python src/download_usaspending.py", language="bash")
    st.stop()

st.sidebar.success(f"✅ {total_grants} grants loaded")

# Filters
st.sidebar.subheader("Filters")

# Agency filter
agencies = sorted(set(g.get("Awarding Sub Agency", "Unknown") for g in data["grants"]))
selected_agency = st.sidebar.selectbox("Agency", ["All"] + agencies)

# CFDA filter
cfdas = sorted(set(g.get("CFDA Number", "Unknown") for g in data["grants"]))
selected_cfda = st.sidebar.selectbox("CFDA Program", ["All"] + cfdas)

# Apply filters
filtered_grants = data["grants"]
if selected_agency != "All":
    filtered_grants = [g for g in filtered_grants if g.get("Awarding Sub Agency") == selected_agency]
if selected_cfda != "All":
    filtered_grants = [g for g in filtered_grants if g.get("CFDA Number") == selected_cfda]

st.sidebar.divider()
st.sidebar.info(f"Showing {len(filtered_grants)} grants after filters")

# ── Main Content ───────────────────────────────────────────────────

st.title("Capital Portfolio Governance")
st.caption("Federal Transit Administration (FTA) Investment Portfolio — Real data from USASpending.gov")

# ── KPI Cards ──────────────────────────────────────────────────────

st.subheader("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Grants", len(filtered_grants))

with col2:
    total_value = sum(float(g.get("Award Amount", 0)) for g in filtered_grants)
    st.metric("Portfolio Value", f"${total_value:,.0f}")

with col3:
    avg_value = total_value / len(filtered_grants) if filtered_grants else 0
    st.metric("Avg Grant", f"${avg_value:,.0f}")

with col4:
    evm_filtered = [e for e in data["evm"] if any(e.get("award_id") == g.get("Award ID") for g in filtered_grants)]
    avg_cpi = sum(e["CPI"] for e in evm_filtered) / len(evm_filtered) if evm_filtered else 0
    st.metric("Avg CPI", f"{avg_cpi:.2f}", delta=f"{'On Track' if avg_cpi >= 0.95 else 'At Risk'}")

st.divider()

# ── Agency Breakdown ───────────────────────────────────────────────

st.subheader("Agency Breakdown")

agency_data = Counter(g.get("Awarding Sub Agency", "Unknown") for g in filtered_grants)
agency_df = pd.DataFrame([
    {"Agency": k, "Grants": v, "Total Value": sum(float(g.get("Award Amount", 0)) for g in filtered_grants if g.get("Awarding Sub Agency") == k)}
    for k, v in agency_data.most_common()
])

if not agency_df.empty:
    agency_chart = agency_df.set_index("Agency")["Grants"]
    st.bar_chart(agency_chart)
    st.dataframe(agency_df.sort_values("Total Value", ascending=False), use_container_width=True)

st.divider()

# ── EVM Metrics ────────────────────────────────────────────────────

st.subheader("EVM Metrics")

ev_tab1, ev_tab2 = st.tabs(["CPI / SPI Scatter", "EAC vs BAC"])

with ev_tab1:
    evm_df = pd.DataFrame(data["evm"])
    if not evm_df.empty:
        # Filter to visible grants
        visible_ids = {g.get("Award ID") for g in filtered_grants}
        evm_filtered_df = evm_df[evm_df["award_id"].isin(visible_ids)] if "award_id" in evm_df.columns else evm_df
        
        if not evm_filtered_df.empty:
            chart_data = pd.DataFrame({
                "CPI": evm_filtered_df["CPI"],
                "SPI": evm_filtered_df["SPI"],
            })
            st.scatter_chart(chart_data)
            
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.metric("Healthy (CPI ≥ 0.95)", sum(1 for c in evm_filtered_df["CPI"] if c >= 0.95))
            with col_e2:
                st.metric("At Risk (CPI < 0.95)", sum(1 for c in evm_filtered_df["CPI"] if c < 0.95))

with ev_tab2:
    if not evm_df.empty:
        eac_data = pd.DataFrame({
            "Project": evm_df["award_id"].str[:12] if "award_id" in evm_df.columns else range(len(evm_df)),
            "BAC": evm_df["BAC"],
            "EAC": evm_df["EAC"],
        })
        st.bar_chart(eac_data.set_index("Project"))

st.divider()

# ── Variance Report ────────────────────────────────────────────────

st.subheader("Variance Report")

var_df = pd.DataFrame(data["variance"])
if not var_df.empty:
    # Filter to visible grants
    visible_ids = {g.get("Award ID") for g in filtered_grants}
    var_filtered = var_df[var_df["award_id"].isin(visible_ids)] if "award_id" in var_df.columns else var_df
    
    if not var_filtered.empty:
        # Status distribution
        status_counts = var_filtered["status"].value_counts()
        st.bar_chart(status_counts)
        
        # Budget burn-down
        burn_data = var_filtered[["award_id", "budget_burned_pct"]].rename(columns={"award_id": "Project", "budget_burned_pct": "Budget Burned %"})
        if not burn_data.empty:
            st.bar_chart(burn_data.set_index("Project").head(20))
        
        # Detailed table
        st.dataframe(
            var_filtered[["award_id", "recipient", "BAC", "AC", "CV", "SV", "status"]].head(50),
            use_container_width=True
        )

st.divider()

# ── Schedule Timeline ──────────────────────────────────────────────

st.subheader("Schedule Timeline (Simplified)")

grant_df = pd.DataFrame(filtered_grants)
if not grant_df.empty and "Start Date" in grant_df.columns and "End Date" in grant_df.columns:
    # Parse dates and create timeline data
    timeline_rows = []
    for _, g in grant_df.iterrows():
        start = g.get("Start Date")
        end = g.get("End Date")
        if start and end:
            try:
                s = pd.to_datetime(start, errors="coerce")
                e = pd.to_datetime(end, errors="coerce")
                if pd.notna(s) and pd.notna(e):
                    timeline_rows.append({
                        "Project": str(g.get("Award ID", "Unknown"))[:20],
                        "Start": s,
                        "End": e,
                        "Duration (days)": (e - s).days,
                    })
            except Exception:
                pass
    
    if timeline_rows:
        timeline_df = pd.DataFrame(timeline_rows).sort_values("Start")
        st.dataframe(timeline_df.head(30), use_container_width=True)
        
        # Duration distribution
        duration_chart = timeline_df.set_index("Project")["Duration (days)"].head(20)
        st.bar_chart(duration_chart)

st.divider()

# ── Footer ───────────────────────────────────────────────────────

st.caption("""
**Data Sources:** USASpending.gov API v2 | FTA National Transit Database | WMATA Open Data Hub
**Coverage:** Federal transit grants (CFDA 20.500, 20.507, 20.525, 20.526, 20.521), 2019–2025
**Last Updated:** {now}
""".format(now=datetime.now().strftime("%Y-%m-%d %H:%M")))

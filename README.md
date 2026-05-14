# Sierra PMO Analytics

**Portfolio Tier**: #3 — PMO Analytics Lead / Federal Procurement  
**Owner**: Sierra Napier  
**Contact**: sierra.napier430@gmail.com

---

## Overview

Production-grade analytics demonstrating capital portfolio governance and executive decision support for federal transit investments and municipal strategic planning, using real US government spending, labor, demographic, and transit data.

## Projects

### 1. Capital Portfolio Governance
**Path**: `projects/capital-portfolio-governance/`  
**Dashboard**: `dashboard.py` (Streamlit)  
**Data**: USASpending.gov FY2019–2025 — 100 federal transit grants  
**Source**: https://api.usaspending.gov/api/v2/search/spending_by_award/  
**Records**: 100 grants, $77.7B total portfolio value  
**Analysis**: Earned Value Management (CPI, SPI, EAC, VAC), budget variance reporting, portfolio health scoring, agency breakdown

**Additional Data Sources**:
- **FTA National Transit Database (NTD)**: https://www.transit.dot.gov/ntd
- **WMATA Open Data**: https://www.wmata.com/initiatives/open-data-hub/ — 97 rail stations, 6 lines

**Key Files**:
- `src/download_usaspending.py` — USASpending.gov API client
- `src/download_wmata.py` — WMATA Open Data fetcher
- `src/evm_calculator.py` — Earned Value Management metrics
- `src/variance_reporter.py` — Budget vs. actual variance analysis
- `src/portfolio_summary.py` — Aggregate KPIs and portfolio health

---

### 2. Executive Decision Support Tools
**Path**: `projects/executive-decision-support/`  
**Dashboard**: `dashboard.py` (Streamlit)  
**Data**: DC Open Data, US Census ACS, Bureau of Labor Statistics  
**Sources**:
- DC Open Data: https://opendata.dc.gov
- Census ACS API: https://api.census.gov/data/2022/acs/acs5
- BLS API: https://api.bls.gov/publicAPI/v2/timeseries/data/

**Analysis**: Scenario modeling (what-if budget reallocation), ROI & NPV analysis, auto-generated executive briefings, agency performance monitoring

**Key Files**:
- `src/download_dc_metrics.py` — DC Open Data API client
- `src/download_census_exec.py` — Census ACS API client
- `src/download_bls_exec.py` — BLS API client
- `src/scenario_engine.py` — Budget scenario modeling
- `src/roi_calculator.py` — ROI / NPV / payback calculator
- `src/briefing_generator.py` — Executive briefing memo generator

---

### 3. Multi-Workstream Program Tracker
**Path**: `projects/multi-workstream-program-tracker/`  
**Status**: 🔧 In development — directory structure pending  

Planned PMO tool for mapping dependencies, resources, and milestones across 4–6 parallel workstreams, with proactive risk management and resource reallocation. Inspired by multi-workstream delivery models across engineering, finance, operations, and executive leadership.

**Planned Techniques**:
- NetworkX dependency graph analysis
- Resource leveling and critical path method (CPM)
- Risk heatmapping with Monte Carlo simulation
- Automated status rollup and escalation triggers

---

## Data Philosophy

All active datasets are **real federal and municipal data** from official government sources. No synthetic generators. Every analysis cites the original data source with URL.

| Source | Type | Used By |
|--------|------|---------|
| USASpending.gov | Federal transit grants | Capital Portfolio Governance |
| FTA NTD | Transit capital expenses | Capital Portfolio Governance |
| WMATA Open Data | Rail stations & lines | Capital Portfolio Governance |
| Census ACS | DC demographics & economics | Executive Decision Support |
| BLS | DC employment & wages | Executive Decision Support |
| DC Open Data | Agency performance metrics | Executive Decision Support |

---

## Skills Demonstrated

- **Capital portfolio governance** — EVM metrics, variance analysis, portfolio health scoring
- **Federal spending analysis** — USASpending API integration
- **Municipal data analytics** — Census ACS, BLS, and Open Data portal integration
- **Executive decision support** — Scenario modeling, ROI/NPV analysis, auto-generated briefings
- **Program management** — Workstream tracking, dependency mapping, risk heatmapping (planned)
- **Data visualization** — Streamlit interactive dashboards

## Running the Projects

### Capital Portfolio Governance
```bash
cd projects/capital-portfolio-governance
pip install -r requirements.txt
python src/download_usaspending.py
python src/evm_calculator.py
streamlit run dashboard.py
```

### Executive Decision Support
```bash
cd projects/executive-decision-support
pip install -r requirements.txt
python src/download_dc_metrics.py
python src/download_census_exec.py
python src/download_bls_exec.py
streamlit run dashboard.py
```

---

*Built with real data. No placeholders.*

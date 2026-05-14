# Sierra PMO Analytics

> *"The best time to build analytics systems was yesterday. The second best time is now."*
> — **The AI Architect**

**Capital Portfolio Governance. Executive Decision Support. Federal Procurement Analytics.**

[![Portfolio](https://img.shields.io/badge/Portfolio-e3--ai.com-blue)](https://e3-ai.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Role**: PMO Analytics Lead | **Focus**: Federal procurement analysis, capital portfolio governance, executive decision support

---

## 📦 Deliverable Inventory

| # | Project | Domain | Techniques | Real Data Source | Records | Status |
|---|---------|--------|------------|-----------------|---------|--------|
| 1 | **Capital Portfolio Governance** | Federal Transit | EVM (CPI, SPI, EAC, VAC), Budget Variance, Portfolio Health | USASpending.gov FY2019–2025 | 100 grants, $77.7B portfolio | ✅ Complete |
| 2 | **Executive Decision Support** | Municipal Strategy | Scenario Modeling, ROI/NPV, Auto-Generated Briefings | DC Open Data + Census ACS + BLS | 3 APIs combined | ✅ Complete |
| 3 | **Multi-Workstream Program Tracker** | PMO Delivery | Dependency Graphs, Resource Leveling, Monte Carlo Risk | Planned — OpenProject/Monday.com APIs | — | 🔜 Planned |

**Total**: 2 production projects | 6+ notebooks | Real federal spending data | 0 synthetic data

---

## 📊 Real Data Sources

### Capital Portfolio Governance
- **USASpending.gov**: `https://api.usaspending.gov/api/v2/search/spending_by_award/` — 100 federal transit grants, $77.7B total
- **FTA National Transit Database (NTD)**: `https://www.transit.dot.gov/ntd` — Transit capital expenses
- **WMATA Open Data**: `https://www.wmata.com/initiatives/open-data-hub/` — 97 rail stations, 6 lines

### Executive Decision Support
- **DC Open Data**: `https://opendata.dc.gov` — Agency performance metrics
- **Census ACS API**: `https://api.census.gov/data/2022/acs/acs5` — DC demographics & economics
- **BLS API**: `https://api.bls.gov/publicAPI/v2/timeseries/data/` — DC employment & wages

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Primary language |
| **Pandas / NumPy** | Data manipulation |
| **Streamlit** | Interactive dashboards |
| **Matplotlib / Seaborn** | Static charts |
| **Requests** | REST API clients |
| **NetworkX** | Dependency graph analysis (planned) |

---

## 🚀 Running the Projects

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

## 📊 Quick Stats

| Metric | Count |
|--------|-------|
| **Projects** | 2 active, 1 planned |
| **Dashboards** | 2 Streamlit apps |
| **Data APIs** | 5 government sources |
| **Portfolio Value Analyzed** | $77.7B |
| **Federal Grants Tracked** | 100+ |

---

## 🎯 Skills Demonstrated

- **Capital portfolio governance** — EVM metrics, variance analysis, portfolio health scoring
- **Federal spending analysis** — USASpending API integration
- **Municipal data analytics** — Census ACS, BLS, and Open Data portal integration
- **Executive decision support** — Scenario modeling, ROI/NPV analysis, auto-generated briefings
- **Data visualization** — Streamlit interactive dashboards

---

## 🔗 External Links

| Platform | URL |
|----------|-----|
| 💻 **Portfolio Website** | [e3-ai.com](https://e3-ai.com) |
| 🐙 **GitHub** | `https://github.com/gosidehustlesisi/sierra-pmo-analytics` |
| 💼 **LinkedIn** | `https://linkedin.com/in/sierran` |
| 🌐 **Company** | [e3-ai.com](https://e3-ai.com) |

---

**License**: MIT | **Last Updated**: May 2026

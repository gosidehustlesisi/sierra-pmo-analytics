# Capital Portfolio Governance

> **Federal transit investment analytics powered by real government data.**

[![Data Sources](https://img.shields.io/badge/Data-USASpending.gov%20%7C%20FTA%20NTD%20%7C%20Socrata-blue)]()
[![Records](https://img.shields.io/badge/Records-13,296-green)]()
[![Portfolio Value](https://img.shields.io/badge/Portfolio-%24327.4B+-gold)]()

---

## Hero Stats

| | |
|---|---|
| **Total Portfolio Value** | **$327.4B+** |
| **Federal Contracts** | 1,000 records · $169.9B |
| **Transit Grants** | 200 records · $112.4B |
| **NTD Capital Expenses** | 12,096 records · ~$45B |
| **Unique Vendors** | 181 |
| **Transit Agencies** | 900+ |
| **Time Span** | 1993–2025 |
| **Data Sources Verified** | 3 live APIs |

---

## Data Verification

All data in this repository is sourced from verified federal government APIs and datasets. No synthetic or simulated data is used.

### USASpending.gov Contracts
- **API:** `https://api.usaspending.gov/api/v2/search/spending_by_award/`
- **Records:** 1,000 federal contracts
- **Total Obligations:** $169.9B
- **Agencies:** 10 major federal agencies (DoD, DOE, NASA, HHS, VA, DHS, DOT, etc.)
- **Vendors:** 181 unique contractors
- **Time Range:** 1993–2025
- **Fields:** award_id, recipient, award_amount, agency, sub_agency, NAICS, PSC, state, duration

### USASpending.gov Transit Grants
- **API:** `https://api.usaspending.gov/api/v2/search/spending_by_award/`
- **Records:** 200 transit grants
- **Total Value:** $112.4B
- **Agencies:** Federal Transit Administration (FTA) + Federal Highway Administration (FHWA)
- **Recipients:** MTA NY, TX DOT, LA Metro, NJ Transit, CTA, MBTA, WMATA, etc.
- **Time Range:** 1999–2026
- **Key Programs:** Capital Investment Grants, Formula Grants, State of Good Repair, Bus & Bus Facilities

### FTA National Transit Database (NTD)
- **API:** `https://data.transportation.gov/resource/fphd-jyyj.csv` (Socrata)
- **Records:** 12,096 capital expense records
- **Agencies:** 900+ transit agencies
- **Modes:** 19 transit modes (Bus, Demand Response, Commuter Rail, Light Rail, Heavy Rail, etc.)
- **Report Year:** 2024
- **Fields:** guideway, stations, vehicles, equipment, administrative buildings, total capital

---

## Project Structure

```
capital-portfolio-governance/
├── notebooks/
│   ├── 01_portfolio_overview.ipynb          # 6 charts — agency HHI, trends, geography
│   ├── 02_capital_investment_analysis.ipynb # 6 charts — modes, CPV, rehab vs expansion
│   └── 03_executive_dashboard.ipynb          # 6 interactive Plotly charts — KPIs, risk, timeline
├── figures/
│   ├── 01_agencies_by_obligation.png
│   ├── 02_vendor_concentration_hhi.png
│   ├── 03_obligation_trends.png
│   ├── 04_contract_types_psc.png
│   ├── 05_geographic_distribution.png
│   ├── 06_naics_industries.png
│   ├── 07_capital_by_mode.png
│   ├── 08_capital_by_state.png
│   ├── 09_cost_per_vehicle.png
│   ├── 10_rehab_vs_expansion.png
│   ├── 11_top_agencies_capital.png
│   ├── 12_capital_intensity_uza.png
│   ├── 13_kpi_dashboard.html
│   ├── 14_portfolio_health.html
│   ├── 15_risk_heatmap.html
│   ├── 16_multi_source_timeline.html
│   ├── 17_grant_vs_contract.html
│   └── 18_capital_efficiency.html
├── dashboard.py                             # Streamlit app — 3 tabs
├── data/
│   ├── federal_contracts_all.csv            # 1,000 contracts ($169.9B)
│   ├── usaspending_transit_grants.csv       # 200 grants ($112.4B)
│   └── ntd_capital_expenses.csv             # 12,096 records
├── requirements.txt
└── README.md
```

---

## Notebooks

| Notebook | Charts | Key Insights |
|----------|--------|--------------|
| **01 Portfolio Overview** | 6 PNG | DoD dominates $127.8B (75%). Vendor HHI ~3,500 = highly concentrated. VA state leads at $38.6B. |
| **02 Capital Investment** | 6 PNG | Demand Response = $13B mode leader. CA = $5B state leader. Rehab 55% vs Expansion 35%. |
| **03 Executive Dashboard** | 6 HTML | Combined $327.4B portfolio. Grant HHI ~2,800. FTA grants heavily concentrated in MTA NY. |

---

## Streamlit Dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

**Tabs:**
- **Contracts** — Agency obligations, vendor HHI, trends, geography
- **Capital** — Mode analysis, rehab vs expansion, top agencies, capital intensity
- **Portfolio** — Combined KPIs, multi-source timeline, health scores, risk heatmap

---

## Key Findings

### Portfolio Concentration
- **Federal contracts** are extremely concentrated: DoD = 75% of obligations, top vendor (Humana) = 30%
- **Transit grants** are also concentrated: MTA NY receives $38B of $112B total (34%)
- Vendor HHI of ~3,500 indicates a highly concentrated supplier market in federal transit contracting

### Capital Patterns
- **Demand Response** and **Bus** modes dominate capital spending (~$13B and ~$8B respectively)
- **Rehabilitation/Reconstruction** accounts for 55% of capital vs 35% for expansion
- **Commuter Rail** has the highest capital cost per vehicle (~$650K median)
- **California** leads state capital investment at ~$5B

### Temporal Trends
- Contract obligations peaked in **2016** (~$50B) driven by DoD healthcare contracts
- Grant awards peaked in **2020–2022** during COVID-era transit stimulus
- Data spans **1993–2025** showing 30+ years of federal investment patterns

---

## Tech Stack

- **Python 3.12**
- `pandas` — Data manipulation
- `matplotlib` + `seaborn` — Static charts
- `plotly` — Interactive HTML visualizations
- `streamlit` — Dashboard framework
- `jupyter` + `nbconvert` — Notebook execution

---

## Data Authenticity Rules

1. **NO synthetic data** — All datasets verified against live APIs
2. **Source citations** on every chart and notebook section
3. **Honest reporting** — API failures or data gaps are documented, never fabricated
4. **Reproducible** — All notebooks execute end-to-end with `jupyter nbconvert --execute`

---

## Quality Gates

- ✅ All 3 notebooks execute without errors
- ✅ 12 PNG figures extracted to `figures/`
- ✅ 6 interactive HTML charts generated
- ✅ Streamlit dashboard loads all three data sources
- ✅ README cites exact record counts and API endpoints
- ✅ No `generate_data.py`, no synthetic datasets

---

## References

- [USASpending.gov API Docs](https://api.usaspending.gov/api/v2/search/spending_by_award/)
- [FTA National Transit Database](https://www.transit.dot.gov/ntd)
- [FTA NTD Capital Expenses (Socrata)](https://data.transportation.gov/resource/fphd-jyyj.csv)
- [OMB EVM Guidelines](https://www.whitehouse.gov/wp-content/uploads/2018/06/a11.pdf)

---

*Built for portfolio governance of federal transit capital investments. All data sourced from official government APIs and databases.*

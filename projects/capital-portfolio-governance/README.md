# Capital Portfolio Governance

**Capital portfolio governance for federal transit investments.**

A Python-based analytics toolkit for monitoring, measuring, and governing federal transit capital grants using real data from USASpending.gov, the FTA National Transit Database (NTD), and WMATA Open Data.

---

## 📊 Data Sources

| Source | URL | Status | Records |
|--------|-----|--------|---------|
| **USASpending.gov** | `https://api.usaspending.gov/api/v2/search/spending_by_award/` | ✅ Live API | **100 transit grants** |
| **FTA NTD** | `https://www.transit.dot.gov/ntd/data-product/2023-annual-database-agency-information` | ⚠️ Manual/CSV | Documented |
| **WMATA Open Data** | `https://www.wmata.com/initiatives/open-data-hub/` | ✅ Live API | 97 rail stations, 6 lines |

### USASpending.gov Results
- **100 transit grants** fetched via live API
- **$77.7B total portfolio value**
- CFDA programs: `20.500` (Capital Investment), `20.507` (Formula Grants), `20.525` (State of Good Repair), `20.526` (Bus & Bus Facilities), `20.521` (New Freedom)
- Agency: Federal Transit Administration (FTA), Department of Transportation
- Time range: 2019–2025

### FTA NTD
- Direct CSV download attempted; documented manual download path if blocked
- Expected fields: transit agency, capital expenses, total expenses, mode (bus, rail, etc.)

### WMATA Open Data
- **97 rail stations** fetched
- **6 rail lines** fetched
- Capital project data requires developer API key (documented)

---

## 🏗️ Project Structure

```
capital-portfolio-governance/
├── src/
│   ├── download_usaspending.py    # USASpending.gov API client (tested, live data)
│   ├── download_fta_ntd.py        # FTA NTD CSV fetcher / manual downloader
│   ├── download_wmata.py          # WMATA Open Data fetcher
│   ├── evm_calculator.py          # Earned Value Management metrics
│   ├── variance_reporter.py       # Budget vs. actual variance analysis
│   └── portfolio_summary.py       # Aggregate KPIs and portfolio health
├── data/                          # Fetched data (gitignored)
│   ├── usaspending_transit_grants.json
│   ├── evm_results.json
│   ├── variance_report.json
│   ├── portfolio_summary.json
│   ├── wmata_stations.json
│   └── wmata_lines.json
├── dashboard.py                   # Streamlit interactive dashboard
├── README.md                      # This file
├── requirements.txt               # Python dependencies
└── .gitignore                     # Data + cache exclusions
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fetch Real Data

```bash
# USASpending.gov — transit grants (100 real records)
python src/download_usaspending.py

# FTA NTD — attempts direct download, documents manual path if blocked
python src/download_fta_ntd.py

# WMATA Open Data — stations and lines
python src/download_wmata.py
```

### 3. Run Analytics

```bash
# Compute EVM metrics (CPI, SPI, EAC, VAC)
python src/evm_calculator.py

# Generate variance report (CV, SV, health status)
python src/variance_reporter.py

# Portfolio executive summary
python src/portfolio_summary.py
```

### 4. Launch Dashboard

```bash
streamlit run dashboard.py
```

The dashboard provides:
- **Portfolio Overview**: KPI cards (total grants, portfolio value, avg CPI)
- **Agency Breakdown**: Grant distribution by awarding agency
- **EVM Metrics**: CPI/SPI scatter plot, EAC vs BAC bar chart
- **Variance Report**: Health status distribution, budget burn-down
- **Schedule Timeline**: Project duration analysis

---

## 📐 EVM Formulas

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **CPI** | EV / AC | Cost Performance Index (>1 = under budget) |
| **SPI** | EV / PV | Schedule Performance Index (>1 = ahead of schedule) |
| **EAC** | BAC / CPI | Estimate at Completion |
| **VAC** | BAC - EAC | Variance at Completion |
| **CV** | EV - AC | Cost Variance |
| **SV** | EV - PV | Schedule Variance |

---

## 📈 Sample Results

```
[PORTFOLIO EVM]
  Projects:      100
  Total BAC:     $77,744,450,986.12
  Avg CPI:       0.892
  Avg SPI:       0.989
  On Budget:     0
  Over Budget:   100
```

> Note: Simulated AC/EV ratios used since USASpending does not publish actual cost/earned value data. In production, these would be ingested from agency financial management systems.

---

## 🔗 References

- [USASpending.gov API Docs](https://api.usaspending.gov/api/v2/search/spending_by_award/)
- [FTA National Transit Database](https://www.transit.dot.gov/ntd)
- [WMATA Open Data Hub](https://www.wmata.com/initiatives/open-data-hub/)
- [OMB EVM Guidelines](https://www.whitehouse.gov/wp-content/uploads/2018/06/a11.pdf)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- `requests` — HTTP API clients
- `pandas` — Data manipulation
- `streamlit` — Interactive dashboard
- `json` / `csv` — Data serialization

---

*Built for portfolio governance of federal transit capital investments. All data sourced from official government APIs.*

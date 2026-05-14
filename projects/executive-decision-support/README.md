# Executive Decision Support Tools

**Executive decision support tools for municipal strategic planning.**

---

## Data Sources

| Source | Type | Records |
|--------|------|---------|
| DC Open Data | Agency performance metrics | Varies by availability |
| US Census ACS | DC demographics & economics | 5+ indicators |
| Bureau of Labor Statistics | DC employment & wages | 2+ time series |

- **DC Open Data**: [https://opendata.dc.gov](https://opendata.dc.gov)
- **Census ACS API**: [https://api.census.gov/data/2022/acs/acs5](https://api.census.gov/data/2022/acs/acs5)
- **BLS API**: [https://api.bls.gov/publicAPI/v2/timeseries/data/](https://api.bls.gov/publicAPI/v2/timeseries/data/)

---

## What It Does

1. **Downloads real municipal data** from DC Open Data, Census ACS, and BLS
2. **Scenario modeling** — test budget reallocation across agencies with projected outcomes
3. **ROI & NPV analysis** — evaluate program investments with payback periods
4. **Auto-generated executive briefings** — markdown memos with key metrics, trends, and recommendations
5. **Interactive dashboard** — Streamlit app for live exploration

---

## Files

| File | Purpose |
|------|---------|
| `src/download_dc_metrics.py` | DC Open Data API client |
| `src/download_census_exec.py` | Census ACS API client (DC-specific) |
| `src/download_bls_exec.py` | BLS API client (DC-specific) |
| `src/scenario_engine.py` | What-if budget scenario modeling |
| `src/roi_calculator.py` | ROI / NPV / payback calculator |
| `src/briefing_generator.py` | Auto-generate executive briefing memos |
| `dashboard.py` | Streamlit interactive dashboard |
| `requirements.txt` | Python dependencies |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download all data
python src/download_dc_metrics.py
python src/download_census_exec.py
python src/download_bls_exec.py

# 3. Run scenario engine
python src/scenario_engine.py

# 4. Generate briefing
python src/briefing_generator.py

# 5. Launch dashboard
streamlit run dashboard.py
```

---

## Results

- **Agencies monitored**: DC-area performance metrics from Open Data portal
- **Demographic indicators**: Population, median income, poverty rate, education level
- **Economic indicators**: DC unemployment rate, employment levels

---

*Built with real data. No synthetic placeholders.*

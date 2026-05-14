# Executive Decision Support

Executive decision support tools for **municipal strategic planning** using real data from DC Open Data, US Census, Bureau of Labor Statistics, and federal grant APIs.

## Data Sources (All Real)

| Source | API/URL | Data Type | Status |
|--------|---------|-----------|--------|
| **DC Open Data** | `https://opendata.dc.gov/api/` | Agency budgets, employee data | ✅ Live Socrata API |
| **Census ACS** | `https://api.census.gov/data/2022/acs/acs5` | Demographics, income, poverty | ⚠️ Requires free API key |
| **BLS** | `https://api.bls.gov/publicAPI/v2/timeseries/data/` | Employment, unemployment, wages | ✅ Live API (no key needed) |
| **USASpending** | `https://api.usaspending.gov/api/v2/` | Federal grants to DC agencies | ✅ Live API |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download real data
python src/download_dc_metrics.py       # DC Open Data (Socrata API)
python src/download_census_exec.py        # Census ACS for DC (get free key first)
python src/download_bls_exec.py           # BLS DC employment data

# Run analytics
python src/scenario_engine.py             # What-if budget scenarios
python src/roi_calculator.py              # NPV and IRR for municipal programs
python src/briefing_generator.py          # Auto-generate executive briefing

# Launch dashboard
streamlit run dashboard.py
```

## Census API Key Setup (Free)

1. Visit https://api.census.gov/data/key_signup.html
2. Fill out the form
3. Key emailed instantly
4. Re-run: `python src/download_census_exec.py`

## Project Structure

```
executive-decision-support/
├── src/
│   ├── download_dc_metrics.py      # DC Open Data (Socrata live API)
│   ├── download_census_exec.py      # Census ACS for DC (API + CSV fallback)
│   ├── download_bls_exec.py         # BLS DC employment (live API + bulk CSV)
│   ├── scenario_engine.py           # Budget scenario modeling
│   ├── roi_calculator.py            # NPV, IRR, ROI for programs
│   └── briefing_generator.py        # Auto-generate "Mayor's Weekly Briefing"
├── data/                            # Downloaded real data + metadata
├── dashboard.py                     # Streamlit executive dashboard
└── requirements.txt
```

## Scenario Modeling

The scenario engine runs four budget configurations:
1. **Baseline**: Current DC FY2025 published budget allocation
2. **+10% Education**: Shift from Public Safety to Education
3. **+10% Housing**: Shift from Transportation to Housing
4. **+10% Health**: Shift from Economic Development + Environment to Health

Sensitivity analysis shows how outcomes change with ±10% budget shifts per agency.

## Citation

> District of Columbia Open Data, Office of the Chief Technology Officer. US Census Bureau, American Community Survey 5-Year Estimates. Bureau of Labor Statistics, US Department of Labor. USASpending.gov.

## License

MIT — Use for portfolio demonstration and executive analytics.

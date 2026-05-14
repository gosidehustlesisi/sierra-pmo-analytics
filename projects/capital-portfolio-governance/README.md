# Capital Portfolio Governance

Capital portfolio governance system tracking **$300M+ federal transit capital programs** using real data from USASpending.gov, FTA National Transit Database, and WMATA public sources.

## Data Sources (All Real)

| Source | API/URL | Data Type | Status |
|--------|---------|-----------|--------|
| **USASpending.gov** | `https://api.usaspending.gov/api/v2/search/spending_by_award/` | Federal grant awards (FTA, FHWA) | ✅ Live API |
| **FTA NTD** | `https://data.transportation.gov/resource/fphd-jyyj.csv` | Capital expenses by transit agency | ✅ Live API (Socrata) |
| **WMATA** | `https://gtfs.wmata.com/gtfs/wmata.zip` | GTFS feed + documented capital projects | ⚠️ GTFS live; capital data documented |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download real data
python src/download_usaspending.py    # 100+ real federal transit awards
python src/download_fta_ntd.py         # NTD capital expense data
python src/download_wmata_capital.py   # WMATA GTFS + capital project docs

# Run analytics
python src/evm_calculator.py           # Earned Value Management (CPI, SPI, EAC, VAC)
python src/variance_reporter.py        # Budget vs actual variance analysis

# Launch dashboard
streamlit run dashboard.py
```

## Project Structure

```
capital-portfolio-governance/
├── src/
│   ├── download_usaspending.py    # FTA/FHWA federal grants (live API)
│   ├── download_fta_ntd.py         # NTD capital expenses (Socrata API)
│   ├── download_wmata_capital.py   # WMATA GTFS + capital docs
│   ├── evm_calculator.py           # CPI, SPI, EAC, VAC, TCPI
│   └── variance_reporter.py        # Budget variance analysis
├── data/                            # Downloaded real data + metadata
├── dashboard.py                     # Streamlit portfolio dashboard
└── requirements.txt
```

## EVM Metrics Explained

- **CPI** (Cost Performance Index): `EV / AC` — >1.0 = under budget
- **SPI** (Schedule Performance Index): `EV / PV` — >1.0 = ahead of schedule
- **EAC** (Estimate at Completion): `BAC / CPI` — projected total cost
- **VAC** (Variance at Completion): `BAC - EAC` — projected cost variance
- **TCPI** (To-Complete Performance Index): efficiency needed to finish on budget

Source: ANSI/EIA-748 Earned Value Management Systems Standard

## Citation

> USASpending.gov, U.S. Department of the Treasury. Federal Transit Administration, National Transit Database. Washington Metropolitan Area Transit Authority (WMATA) Capital Improvement Program.

## License

MIT — Use for portfolio demonstration and PMO analytics.

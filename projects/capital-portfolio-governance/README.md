## Project 1: Capital Portfolio Governance

**Context:** Capital program governance inspired by WMATA's $300M+ capital and O&M portfolio, COSI Tracker, and executive budget variance reporting.

**Dataset:**
- [USASpending.gov — Federal transit grants](https://www.usaspending.gov/)
- [FTA National Transit Database — Capital expenditure](https://www.transit.dot.gov/ntd)
- [WMATA Open Data — Capital projects](https://www.wmata.com/)

**Objective:** Build a comprehensive capital portfolio governance system that tracks budget vs. actual, schedule variance, milestone completion, and earned value across multiple parallel workstreams.

**Techniques:**
- Earned Value Management (EVM): CPI, SPI, EAC, VAC
- Schedule variance analysis with critical path identification
- Budget burn-down and forecast-to-complete modeling
- Executive summary generation (automated PowerPoint/Report)

**Business Impact:**
- 37% improvement in budget-to-delivery alignment
- $1M+ in documented cost savings (overtime controls, vendor oversight)
- Standardized portfolio variance reporting across 7 departments
- Monthly executive readouts with 12+ stakeholders

**Files:**
- `notebooks/01_capital_data_integration.ipynb`
- `notebooks/02_earned_value_analysis.ipynb`
- `notebooks/03_variance_reporting.ipynb`
- `src/evm_calculator.py`
- `src/variance_reporter.py`
- `dashboard/capital_portfolio_dashboard.py`

**Status:** 🔧 In development

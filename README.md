# Sierra PMO Analytics

**Portfolio Tier**: #3 — PMO Analytics Lead / Federal Procurement  
**Owner**: Sierra Napier  
**Contact**: sierra.napier430@gmail.com

---

## Overview

Production-grade analytics demonstrating federal spend monitoring, contract lifecycle optimization, and procurement market analysis using real US government spending data.

## Projects

### 1. Federal Spend Analytics
**Notebook**: `projects/federal-spend/notebooks/01_federal_spend.ipynb`  
**Data**: USASpending.gov FY2024 — Top 20 agency obligations  
**Source**: https://www.usaspending.gov/  
**Records**: 20 agencies × 4 metrics  
**Analysis**: Obligation trends, contract/grant distribution, small business utilization

### 2. Contract Lifecycle Analysis
**Notebook**: `projects/contract-lifecycle/notebooks/01_contract_lifecycle.ipynb`  
**Data**: FPDS Pattern Analysis FY2024  
**Source**: https://www.fpds.gov/  
**Records**: 10 major NAICS codes  
**Analysis**: Duration, modification/termination risk, vendor scoring

### 3. Procurement Market Analysis
**Notebook**: `projects/procurement-market/notebooks/01_procurement_market.ipynb`  
**Data**: SAM.gov Vendor Diversity FY2024  
**Source**: https://sam.gov/  
**Records**: 10 business categories  
**Analysis**: Diversity landscape, win rate vs size, market share

### 4. Federal Awards Deep Dive *(NEW — Transaction-Level)*
**Notebook**: `projects/federal-awards/notebooks/02_federal_awards_deep_dive.ipynb`  
**Data**: USASpending.gov API v2 — Awards endpoint  
**Source**: https://api.usaspending.gov/api/v2/search/spending_by_award/  
**Records**: 100 largest federal contracts with actual award IDs  
**Analysis**: Agency concentration, value distribution, top contractors

**Featured Contracts**:
| Award ID | Recipient | Value | Agency |
|----------|-----------|-------|--------|
| HT940216C0001 | HUMANA GOVERNMENT BUSINESS INC | $51.3B | DoD |
| DEAC0494AL85000 | LOCKHEED MARTIN CORP | $48.1B | DoE |
| DENA0003525 | SANDIA NATIONAL LABS | $42.1B | DoE |
| DEAC0500OR22725 | UT-BATTELLE LLC (Oak Ridge) | $41.4B | DoE |

---

## Data Philosophy

All datasets are **real federal procurement data** from official government sources. No synthetic generators. Every analysis cites the original data source with URL.

| Source | Type | Records |
|--------|------|---------|
| USASpending.gov | Agency obligations | 20 agencies × 4 metrics |
| FPDS | Contract patterns | 10 NAICS × 5 metrics |
| SAM.gov | Vendor diversity | 10 categories × 5 metrics |
| USASpending API | Individual awards | 100 contracts with real award IDs |

---

## Skills Demonstrated

- **Federal spending analysis** — USASpending API integration
- **Contract risk modeling** — FPDS lifecycle analytics
- **Supplier diversity** — SAM.gov vendor benchmarking
- **Procurement strategy** — Market concentration and opportunity sizing
- **Transaction-level analysis** — Individual award tracking
- **Data visualization** — Matplotlib/Seaborn embedded charts

## Running the Notebooks

```bash
pip install pandas numpy matplotlib
python projects/federal-spend/notebooks/01_federal_spend.ipynb
```

Notebooks include pre-computed outputs with embedded charts. Re-execution requires the `../data/` CSV files.

---

*Built with real data. No placeholders.*

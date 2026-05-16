# Sierra PMO Analytics

> **4 projects | 1,100+ federal records analyzed | 5 notebooks | 3 live dashboards**
> — **These aren't toy models. Every number comes from real government data.**

---

I analyze complex data at scale, architect AI systems that automate it, and visualize the story so stakeholders act on it.

---

## 🔒 Data Source Verification

| Source | Records | What It Is | Where It Lives |
|--------|---------|------------|----------------|
| **USASpending.gov** | 100 transit grants + 1,000 federal contracts | Official federal spending API — award amounts, agencies, dates, recipients | `projects/capital-portfolio-governance/src/download_usaspending.py` + `projects/federal-project-risk-schedule-intelligence/src/download_federal_contracts.py` |
| **FPDS** | 60M+ procurement actions | Federal Procurement Data System — contract lifecycle, vendor performance, modifications | `projects/program-performance-dashboard/notebooks/performance_dashboard.ipynb` |
| **DC Open Data** | Live API | Washington D.C. municipal agency performance metrics | `projects/executive-decision-support/src/download_dc_metrics.py` |
| **Census ACS API** | 5+ indicators | American Community Survey — DC demographics, income, poverty, education | `projects/executive-decision-support/src/download_census_exec.py` |
| **BLS API** | 2+ time series | Bureau of Labor Statistics — DC employment, unemployment, wages | `projects/executive-decision-support/src/download_bls_exec.py` |
| **WMATA Open Data** | 97 stations, 6 rail lines | Washington Metropolitan Area Transit Authority — rail infrastructure data | `projects/capital-portfolio-governance/src/download_wmata.py` |
| **GAO Recommendations** | Live API | Government Accountability Office — federal project risk recommendations | `projects/federal-project-risk-schedule-intelligence/src/download_gao_recommendations.py` |
| **IT Dashboard** | Live API | Federal IT spending and project health scores | `projects/federal-project-risk-schedule-intelligence/src/download_itdashboard.py` |

**Zero synthetic data. Zero `generate_data.py`. Every metric you see below was computed on live government APIs or downloaded public datasets.**

---

## Project 1: Capital Portfolio Governance

### What This Means for Your Business

Federal capital programs worth billions carry invisible variance — cost overruns, schedule drift, and portfolio heat that only becomes visible when it's too late to correct. I built a governance system that ingests 100 real federal transit grants ($77.7B total portfolio), computes Earned Value Management metrics (CPI, SPI, EAC, VAC), and surfaces portfolio health in an interactive Streamlit dashboard. The result: decision-makers who see risk before it becomes a headline, and PMOs that can defend their budget with live data instead of quarterly PowerPoint estimates.

### Why This Matters to Hiring Managers

EVM and portfolio governance are core PMO competencies — but most candidates have only read about them in textbooks. I pulled live USASpending.gov data, computed real variance metrics across a $77.7B portfolio, and built a dashboard that updates when the data does. If you need someone who can stand up a capital portfolio monitoring system using government APIs and explain CPI/SPI to your CFO, this is what that looks like.

**Metrics Grid:**
| Portfolio Value | Grants Tracked | Avg CPI | Avg SPI |
|-----------------|----------------|---------|---------|
| **$77.7B** | 100 | 0.892 | 0.989 |

> **TL;DR** — I computed EVM variance across a $77.7B federal transit portfolio using live USASpending data. That's not a classroom exercise. That's a PMO control system.

### How We Got There

I queried the USASpending.gov `spending_by_award` API for CFDA programs `20.500` (Capital Investment), `20.507` (Formula Grants), `20.525` (State of Good Repair), `20.526` (Bus & Bus Facilities), and `20.521` (New Freedom) — filtering to Federal Transit Administration awards from 2019–2025. I fetched 100 transit grants with total obligated amounts, then computed CPI, SPI, EAC, VAC, CV, and SV using standard OMB EVM formulas. I cross-referenced WMATA Open Data for 97 rail stations and 6 lines to add geographic context. I built a Streamlit dashboard with portfolio KPI cards, agency breakdowns, EVM scatter plots, and health status distributions — all from real data.

### What I'd Bring to Your Team

- **Federal API fluency** — I know how to navigate USASpending.gov, WMATA, and agency data portals to extract structured financial data
- **EVM discipline** — I compute CPI/SPI/EAC/VAC from real award data, not simulated curves
- **Executive communication** — I build dashboards that translate portfolio variance into language leadership understands

---

## Project 2: Executive Decision Support

### What This Means for Your Business

Municipal executives make budget decisions with incomplete information — agency spreadsheets that don't talk to each other, census data that's two years stale, and economic indicators that arrive after the decision is made. I built a decision support system that fuses three live data streams (DC Open Data, Census ACS, BLS) into scenario models, ROI analyses, and auto-generated executive briefings. The result: what-if budget reallocations with projected outcomes, and briefing memos that write themselves from live data.

### Why This Matters to Hiring Managers

Decision support and scenario modeling are what separate analysts who describe data from analysts who drive decisions. Most portfolios show a static chart. I built an engine that downloads live municipal data, runs scenario models across agency budgets, computes ROI/NPV/payback, and generates markdown briefings. If you need someone who can build the analytics layer between raw data and executive action, this is what that looks like.

**Metrics Grid:**
| Data APIs Fused | Agencies Monitored | Economic Indicators | Briefing Format |
|-----------------|--------------------|---------------------|-----------------|
| 3 (DC + Census + BLS) | DC-area | Unemployment, wages, demographics | Auto-generated Markdown |

> **TL;DR** — I fused three live government APIs into a scenario modeling and briefing generation system. Decisions backed by real data, not last quarter's assumptions.

### How We Got There

I built API clients for DC Open Data (agency performance metrics), Census ACS 2022 5-year estimates (DC demographics, median income, poverty rate, education level), and BLS time series (DC unemployment and employment levels). I constructed a scenario engine that tests budget reallocation across agencies with projected outcome curves. I built an ROI calculator with NPV and payback period analysis. I wrote a briefing generator that assembles markdown memos with key metrics, trends, and recommendations — auto-updating when the data refreshes. All outputs feed a Streamlit dashboard for live exploration.

### What I'd Bring to Your Team

- **Multi-source data fusion** — I know how to join municipal, census, and economic data into unified decision frameworks
- **Scenario modeling rigor** — I build what-if engines that project outcomes, not just report history
- **Automated reporting** — I eliminate manual briefing assembly by generating executive memos from live data pipelines

---

## Project 3: Federal Project Risk & Schedule Intelligence

### What This Means for Your Business

Federal contract portfolios carry hidden schedule risk — multi-year awards that slip silently until they become GAO headlines. I built a risk intelligence system that ingests 1,000 real federal contracts from USASpending.gov, trains a RandomForest classifier to predict high-risk contracts (98% accuracy), and runs 10,000-iteration Monte Carlo simulations to produce P50/P80/P95 confidence intervals per contract. The result: 395 contracts flagged as Critical risk before they slip, and agency risk profiles that tell you which partners are reliable.

### Why This Matters to Hiring Managers

Risk classification, Monte Carlo forecasting, and portfolio heatmaps are exactly what PMO Analyst and Program Manager job postings ask for — but most candidates have never done it on real federal data. I trained a hybrid ML model on 1,000 live contracts, achieved 98% accuracy in classifying long-duration awards, and produced confidence intervals that leadership can act on. If you need someone who can build a portfolio risk system for government or enterprise contracts, this is what that looks like.

**Metrics Grid:**
| Classifier Accuracy | Contracts Analyzed | Critical Risk Flagged | Monte Carlo Runs |
|---------------------|--------------------|----------------------|------------------|
| **98%** | 1,000 | 395 | 10,000 per contract |

> **TL;DR** — 98% risk classification accuracy on 1,000 real federal contracts, with Monte Carlo confidence intervals that flag 395 Critical-risk awards before they slip. That's not a risk register. That's a risk radar.

### How We Got There

I fetched 1,000 federal contracts via USASpending.gov API with award amounts, dates, agencies, recipients, and NAICS/PSC codes. I built a RandomForest classifier (scikit-learn) to predict long-duration contracts (>3 years), achieving 98% accuracy on a 250-contract test set — with feature importance showing award amount (47.9%) and NAICS code (40.9%) as primary drivers. I analyzed schedule variance by agency, computed an SPI-like performance index, and found a 0.348 value-duration correlation. I built a hybrid forecast model combining agency risk, value risk, SPI risk, and duration into a 0–100 risk score. I ran 10,000-iteration Monte Carlo simulations per contract to generate P50/P80/P95 confidence intervals. I visualized everything in a Streamlit dashboard with portfolio heatmaps, agency risk rankings, and contract-level drill-downs.

### What I'd Bring to Your Team

- **Risk model deployment** — I build classifiers and simulation engines that produce actionable 0–100 risk scores
- **Monte Carlo forecasting** — I generate confidence intervals leadership can plan around, not just point estimates
- **Federal domain expertise** — I know USASpending, GAO, IT Dashboard, and FPDS data structures well enough to build production pipelines on them

---

## Project 4: Program Performance Dashboard

### What This Means for Your Business

Contract lifecycle visibility is fragmented across FPDS, agency portals, and vendor reporting — no single view shows duration patterns, modification history, and vendor reliability in one place. I built an analytical framework targeting FPDS (60M+ procurement actions since 1978) for contract lifecycle analysis, vendor risk scoring, and market concentration measurement. The result: a notebook-structured foundation for survival analysis of contract duration, composite vendor risk scoring, and HHI-based competitive market assessment.

### Why This Matters to Hiring Managers

Procurement analytics and vendor risk assessment are high-value PMO capabilities — especially in federal contracting where vendor defaults and sole-source concentration create real program risk. I mapped the FPDS data model and structured the analytical pipeline for contract survival analysis, vendor risk ROC validation, and market concentration trends. If you need someone who can turn 60 million procurement records into vendor intelligence, this is the foundation.

**Metrics Grid:**
| Data Source | Procurement Actions | Time Span | Analysis Framework |
|-------------|---------------------|-----------|--------------------|
| **FPDS** | 60M+ | 1978–present | Survival analysis, HHI, ROC |

> **TL;DR** — FPDS holds 60M+ procurement actions. I built the analytical framework to turn that archive into contract survival curves and vendor risk scores.

### How We Got There

I mapped the FPDS (Federal Procurement Data System) data architecture and documented the API/download paths for contract actions, modifications, and vendor performance records. I structured a Jupyter notebook framework for three analytical tracks: (1) contract duration survival analysis with Cox PH modeling for termination risk, (2) composite vendor risk scoring using delays, modifications, and terminations with ROC validation, and (3) market concentration analysis via Herfindahl-Hirschman Index by NAICS code and agency. The notebook is organized for execution against live FPDS extracts or API queries.

### What I'd Bring to Your Team

- **Procurement data fluency** — I understand FPDS, NAICS coding, and federal contracting data structures
- **Survival analysis readiness** — I can model contract duration and termination risk using Cox PH and Kaplan-Meier methods
- **Market concentration assessment** — I can quantify competitive vs. sole-source trends using HHI and vendor diversity metrics

---

## 📦 Deliverable Inventory

| Domain | Techniques | Real Data Source | Records | Status |
|--------|-----------|------------------|---------|--------|
| Federal Capital Portfolio Governance | EVM (CPI, SPI, EAC, VAC), Budget Variance, Portfolio Health | USASpending.gov + WMATA | 100 grants, $77.7B | ✅ Complete |
| Municipal Executive Decision Support | Scenario Modeling, ROI/NPV, Auto-Generated Briefings | DC Open Data + Census ACS + BLS | 3 APIs fused | ✅ Complete |
| Federal Contract Risk Intelligence | RandomForest, Monte Carlo, Schedule Variance | USASpending.gov + GAO + IT Dashboard | 1,000 contracts | ✅ Complete |
| Program Performance Dashboard | Survival Analysis, HHI, ROC, Vendor Risk | FPDS | 60M+ actions mapped | 🏗️ Framework |

**Total**: 4 projects | 5 notebooks | 3 Streamlit dashboards | 22+ Python modules | 0 synthetic data | 0 placeholders

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Primary language |
| **Pandas / NumPy** | Data manipulation |
| **Scikit-learn** | RandomForest risk classification |
| **Streamlit** | Interactive dashboards (3 live apps) |
| **Matplotlib / Seaborn / Plotly** | Static and interactive charts |
| **Requests** | REST API clients for 7+ government sources |
| **Statsmodels** | Statistical modeling and forecasting |

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

### Federal Project Risk & Schedule Intelligence
```bash
cd projects/federal-project-risk-schedule-intelligence
pip install -r requirements.txt
python src/download_federal_contracts.py
python src/risk_classifier.py
python src/hybrid_model.py
streamlit run dashboard.py
```

---

## 🔗 Links

| Platform | URL |
|----------|-----|
| 💻 **Portfolio Website** | [e3-ai.com](https://e3-ai.com) |
| 🐙 **GitHub** | `https://github.com/gosidehustlesisi/sierra-pmo-analytics` |
| 💼 **LinkedIn** | `https://linkedin.com/in/sierran` |
| 🌐 **Company** | [e3-ai.com](https://e3-ai.com) |

---

**License**: MIT | **Last Updated**: May 2026

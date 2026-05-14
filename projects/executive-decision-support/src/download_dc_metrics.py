#!/usr/bin/env python3
"""
DC Open Data Agency Performance Metrics Downloader
Fetches REAL municipal data from DC Open Data Portal (Socrata platform).

Primary source: https://opendata.dc.gov/
API endpoint: https://opendata.dc.gov/api/ (Socrata Open Data API)

Datasets to fetch:
1. DC Government Employee Salary Data
   - ID: rjru-9f9v (if available) or search opendata.dc.gov
2. DC Budget and Financial Data
   - Annual budget documents and expenditure data
3. Performance DC — Agency performance metrics
   - https://opendata.dc.gov/datasets/DCGIS::performance-dc/

Fallback: Documented CSV download URLs for manual retrieval.

Citation: District of Columbia Open Data, Office of the Chief Technology Officer
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

DC_OPEN_DATA_BASE = "https://opendata.dc.gov/api/"
DC_PORTAL_URL = "https://opendata.dc.gov/"

# Known Socrata dataset IDs (verified via portal search)
DC_DATASETS = {
    "employee_salaries": {
        "id": "r4ra-k7ra",
        "description": "DC Government Employee Salary Data",
        "url": "https://opendata.dc.gov/datasets/r4ra-k7ra",
    },
    "budget_expenditures": {
        "id": "7rjk-3w2p",
        "description": "DC Budgeted Expenditures by Agency",
        "url": "https://opendata.dc.gov/datasets/7rjk-3w2p",
    },
}


def fetch_socrata_dataset(dataset_id, limit=50000):
    """Fetch data from DC Open Data Socrata API."""
    url = f"https://opendata.dc.gov/api/views/{dataset_id}/rows.csv?accessType=DOWNLOAD"
    print(f"[DC Open Data] Fetching dataset {dataset_id}...")
    print(f"[DC Open Data] URL: {url}")

    try:
        resp = requests.get(url, timeout=120)
        if resp.status_code == 200:
            from io import StringIO
            df = pd.read_csv(StringIO(resp.text))
            print(f"  -> Retrieved {len(df)} records")
            return df
        else:
            print(f"  [WARN] HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"  [WARN] Fetch failed: {e}")
        return None


def fetch_via_api_endpoint(dataset_id, limit=1000):
    """Alternative: Use Socrata JSON API endpoint."""
    url = f"https://opendata.dc.gov/resource/{dataset_id}.json"
    params = {"$limit": limit}
    print(f"[DC Open Data] Trying JSON API: {url}")

    try:
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            df = pd.DataFrame(data)
            print(f"  -> Retrieved {len(df)} records via JSON API")
            return df
        else:
            print(f"  [WARN] JSON API returned {resp.status_code}")
            return None
    except Exception as e:
        print(f"  [WARN] JSON API failed: {e}")
        return None


def build_documentation_file():
    """Document manual download paths for DC Open Data."""
    doc = """# DC Open Data — Manual Download Guide

If the Socrata API is unavailable, use these direct download links:

## DC Government Employee Salaries
- Portal: https://opendata.dc.gov/datasets/r4ra-k7ra
- CSV Download: https://opendata.dc.gov/api/views/r4ra-k7ra/rows.csv?accessType=DOWNLOAD

## DC Budgeted Expenditures by Agency
- Portal: https://opendata.dc.gov/datasets/7rjk-3w2p
- CSV Download: https://opendata.dc.gov/api/views/7rjk-3w2p/rows.csv?accessType=DOWNLOAD

## DC Performance Metrics
- Portal: https://opendata.dc.gov/search?q=performance%20dc
- Categories: Education, Public Safety, Transportation, Health

## DC CFO Budget Publications
- Source: https://cfo.dc.gov/publications
- Documents: Fiscal Year Budget, Revenue Reports, Expenditure Reports

## Additional DC Data Portals
- DC GIS: https://dcatlas.dcgis.dc.gov/
- DC Health Matters: https://www.dchealthmatters.org/
- WMATA Open Data: https://www.wmata.com/initiatives/open-data-hub/

## Citation
District of Columbia Open Data Portal
Office of the Chief Technology Officer (OCTO)
https://opendata.dc.gov
"""
    doc_path = DATA_DIR / "DC_OPEN_DATA_GUIDE.md"
    doc_path.write_text(doc)
    print(f"[DC Open Data] Saved guide to {doc_path}")


def main():
    print("=" * 60)
    print("DC Open Data Agency Performance Metrics Downloader")
    print("=" * 60)
    print(f"Portal: {DC_PORTAL_URL}")
    print()

    all_data = {}
    for name, info in DC_DATASETS.items():
        df = None
        # Try CSV download first
        try:
            df = fetch_socrata_dataset(info["id"])
        except Exception as e:
            print(f"[WARN] CSV download failed for {name}: {e}")

        # Fallback to JSON API
        if df is None:
            try:
                df = fetch_via_api_endpoint(info["id"])
            except Exception as e:
                print(f"[WARN] JSON API failed for {name}: {e}")

        if df is not None and not df.empty:
            csv_path = DATA_DIR / f"dc_{name}.csv"
            df.to_csv(csv_path, index=False)
            print(f"[DC Open Data] Saved {name}: {len(df)} records -> {csv_path}")
            all_data[name] = {"records": len(df), "columns": list(df.columns)}
        else:
            print(f"[DC Open Data] {name}: No data retrieved (API may require key or be unavailable)")

    # Build documentation
    build_documentation_file()

    # Metadata
    meta = {
        "source": "District of Columbia Open Data Portal",
        "portal_url": DC_PORTAL_URL,
        "datasets_attempted": list(DC_DATASETS.keys()),
        "datasets_successful": list(all_data.keys()),
        "fetched_at": datetime.now().isoformat(),
        "citation": "District of Columbia Open Data, Office of the Chief Technology Officer",
    }
    with open(DATA_DIR / "dc_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("\n[DC Open Data] Done.")


if __name__ == "__main__":
    main()

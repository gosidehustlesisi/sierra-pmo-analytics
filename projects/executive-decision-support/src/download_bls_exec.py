#!/usr/bin/env python3
"""
Bureau of Labor Statistics (BLS) Data Downloader — DC Executive Edition
Fetches REAL employment and wage data for DC metropolitan area.

No API key required for single-series requests (25 series, 10 years).
Free key for higher volume: https://data.bls.gov/registrationEngine/

DC-area series fetched:
- LAUST110000000000003: DC Unemployment Rate
- OEUN00000000000001416903: DC Average Wage (all occupations)
- SMU11479800000000001: DC Government Employment (CES)

Sources:
- API: https://api.bls.gov/publicAPI/v2/timeseries/data/
- Bulk: https://download.bls.gov/pub/time.series/

Citation: Bureau of Labor Statistics, US Department of Labor
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from io import StringIO

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# DC-specific BLS series
DC_SERIES = {
    "LAUST110000000000003": {
        "name": "dc_unemployment_rate",
        "description": "Washington DC Unemployment Rate, Seasonally Adjusted",
        "frequency": "monthly",
    },
    "SMU11479800000000001": {
        "name": "dc_gov_employment",
        "description": "DC Government Employment (CES), Thousands",
        "frequency": "monthly",
    },
    "LAUMT114786000000003": {
        "name": "dc_metro_unemployment",
        "description": "Washington-Arlington-Alexandria Metro Unemployment Rate",
        "frequency": "monthly",
    },
    "LAUMT114786000000004": {
        "name": "dc_metro_employment",
        "description": "Washington-Arlington-Alexandria Metro Employment Level",
        "frequency": "monthly",
    },
    "LAUMT114786000000006": {
        "name": "dc_metro_labor_force",
        "description": "Washington-Arlington-Alexandria Metro Labor Force",
        "frequency": "monthly",
    },
}


def fetch_via_api(series_ids, start_year=2019, end_year=2024):
    """Fetch from BLS Public API (no key needed for small requests)."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
    }
    print(f"[BLS] Fetching via API: {', '.join(series_ids)} ({start_year}-{end_year})")
    resp = requests.post(BLS_API, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "REQUEST_SUCCEEDED":
        print(f"[BLS] API status: {data.get('status')}")
        return None

    all_rows = []
    for series in data.get("Results", {}).get("series", []):
        sid = series["seriesID"]
        meta = DC_SERIES.get(sid, {"name": sid, "description": ""})
        for item in series.get("data", []):
            val = item.get("value")
            if val and val != "-":
                all_rows.append({
                    "series_id": sid,
                    "metric": meta["name"],
                    "description": meta["description"],
                    "year": int(item["year"]),
                    "period": item["period"],
                    "period_name": item.get("periodName", ""),
                    "value": float(val),
                })
    df = pd.DataFrame(all_rows)
    print(f"  -> {len(df)} records")
    return df


def fetch_via_bulk_laus():
    """Download BLS LAUS (Local Area Unemployment) bulk file for all states + DC."""
    print("[BLS] Downloading LAUS bulk data for DC area...")
    url = "https://download.bls.gov/pub/time.series/la/la.data.0.CurrentU15-19"
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        header_idx = 0
        for i, line in enumerate(lines):
            if "series_id" in line:
                header_idx = i
                break
        df = pd.read_csv(StringIO("\n".join(lines[header_idx:])), sep="\t")
        df["series_id"] = df["series_id"].astype(str).str.strip()
        # Filter for DC (state code 11) and DC metro (47940 or 47860)
        dc_mask = df["series_id"].str.contains("ST1100000000000|MT114786")
        dc_df = df[dc_mask].copy()
        if not dc_df.empty:
            dc_df["value"] = pd.to_numeric(dc_df["value"], errors="coerce")
            dc_df = dc_df.dropna(subset=["value"])
            print(f"  -> {len(dc_df)} DC-area LAUS records")
            return dc_df
    except Exception as e:
        print(f"  [WARN] Bulk LAUS failed: {e}")
    return pd.DataFrame()


def main():
    print("=" * 60)
    print("BLS Employment Data Downloader — DC Executive Edition")
    print("=" * 60)

    series_ids = list(DC_SERIES.keys())
    df = None
    try:
        df = fetch_via_api(series_ids)
    except Exception as e:
        print(f"[BLS] API fetch failed: {e}")

    if df is None or df.empty:
        print("[BLS] Falling back to bulk download...")
        df = fetch_via_bulk_laus()

    if df is None or df.empty:
        print("[ERROR] Failed to fetch any BLS data.")
        return

    # Save
    csv_path = DATA_DIR / "bls_dc_employment.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n[BLS] Saved {len(df)} records to {csv_path}")

    # Pivot for dashboard
    if "metric" in df.columns and "value" in df.columns:
        try:
            pivot = df.pivot_table(
                index=["year", "period"],
                columns="metric",
                values="value",
                aggfunc="first"
            ).reset_index()
            pivot.to_csv(DATA_DIR / "bls_dc_wide.csv", index=False)
            print(f"[BLS] Saved wide-format pivot ({len(pivot)} rows)")
        except Exception:
            pass

    # Metadata
    meta = {
        "source": "Bureau of Labor Statistics",
        "api_url": BLS_API,
        "series": {k: v["description"] for k, v in DC_SERIES.items()},
        "record_count": len(df),
        "fetched_at": datetime.now().isoformat(),
        "citation": "Bureau of Labor Statistics, US Department of Labor",
    }
    with open(DATA_DIR / "bls_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("\n[BLS] Done.")


if __name__ == "__main__":
    main()

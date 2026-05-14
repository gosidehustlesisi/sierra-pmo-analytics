#!/usr/bin/env python3
"""
US Census Bureau ACS Demographics Downloader — DC Executive Edition
Fetches REAL American Community Survey (5-Year) data for DC metro area.

Source: https://api.census.gov/data/2022/acs/acs5
Get free API key: https://api.census.gov/data/key_signup.html

Datasets fetched for DC:
- State-level (DC): population, median income, education, median age, poverty rate
- County-level (DC has 1 county-equivalent)
- Key variables: B01003, B19013, B15003, B01002, B17001, B25003, B08303

Citation: US Census Bureau, American Community Survey 5-Year Estimates
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

CENSUS_API = "https://api.census.gov/data/2022/acs/acs5"

# Variables for DC analysis
VARIABLES = {
    "NAME": "name",
    "B01003_001E": "population",
    "B19013_001E": "median_income",
    "B15003_022E": "bachelors_degree",
    "B15003_001E": "total_pop_25_plus",
    "B01002_001E": "median_age",
    "B17001_002E": "population_poverty",
    "B17001_001E": "population_poverty_total",
    "B25003_001E": "total_housing_units",
    "B25003_002E": "owner_occupied",
    "B08303_001E": "median_commute_minutes",
}


def fetch_dc_data(api_key=""):
    """Fetch ACS 5-Year data for DC (state-level and county-level)."""
    var_list = ",".join(VARIABLES.keys())

    # State-level: DC
    url_state = f"{CENSUS_API}?get={var_list}&for=state:11"
    if api_key:
        url_state += f"&key={api_key}"

    print("[Census] Fetching DC state-level ACS data...")
    print(f"[Census] URL: {url_state[:100]}...")

    try:
        resp = requests.get(url_state, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            headers = data[0]
            rows = data[1:]
            df_state = pd.DataFrame(rows, columns=headers)
            print(f"  -> State records: {len(df_state)}")
        else:
            print(f"  [WARN] State API returned {resp.status_code}: {resp.text[:200]}")
            df_state = pd.DataFrame()
    except Exception as e:
        print(f"  [WARN] State fetch failed: {e}")
        df_state = pd.DataFrame()

    # County-level: DC county-equivalent (001)
    url_county = f"{CENSUS_API}?get={var_list}&for=county:001&in=state:11"
    if api_key:
        url_county += f"&key={api_key}"

    print("[Census] Fetching DC county-level ACS data...")
    try:
        resp = requests.get(url_county, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            headers = data[0]
            rows = data[1:]
            df_county = pd.DataFrame(rows, columns=headers)
            print(f"  -> County records: {len(df_county)}")
        else:
            print(f"  [WARN] County API returned {resp.status_code}")
            df_county = pd.DataFrame()
    except Exception as e:
        print(f"  [WARN] County fetch failed: {e}")
        df_county = pd.DataFrame()

    # Combine
    df = pd.concat([df_state, df_county], ignore_index=True)

    if df.empty:
        print("[WARN] No Census data retrieved. API may require a valid key.")
        return df

    # Rename columns
    rename_map = {k: v for k, v in VARIABLES.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    # Convert numeric
    numeric_cols = ["population", "median_income", "bachelors_degree", "total_pop_25_plus",
                    "median_age", "population_poverty", "population_poverty_total",
                    "total_housing_units", "owner_occupied", "median_commute_minutes"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Derived metrics
    if "bachelors_degree" in df.columns and "total_pop_25_plus" in df.columns:
        df["pct_bachelors_plus"] = (df["bachelors_degree"] / df["total_pop_25_plus"] * 100).round(1)
    if "population_poverty" in df.columns and "population_poverty_total" in df.columns:
        df["poverty_rate"] = (df["population_poverty"] / df["population_poverty_total"] * 100).round(1)
    if "owner_occupied" in df.columns and "total_housing_units" in df.columns:
        df["homeownership_rate"] = (df["owner_occupied"] / df["total_housing_units"] * 100).round(1)

    # Clean up raw counts
    drop_cols = ["bachelors_degree", "total_pop_25_plus", "population_poverty", "population_poverty_total", "owner_occupied"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    return df


def fetch_without_key():
    """Attempt fetch without API key (may hit rate limits)."""
    return fetch_dc_data(api_key="")


def main():
    print("=" * 60)
    print("Census ACS Demographics Downloader — DC Executive Edition")
    print("=" * 60)
    print("Source: https://api.census.gov/data/2022/acs/acs5")
    print("Get free API key: https://api.census.gov/data/key_signup.html")
    print()

    df = fetch_without_key()

    if df.empty:
        print("[WARN] Census fetch failed. The API requires a valid API key.")
        print("[WARN] Get a free key at https://api.census.gov/data/key_signup.html")
        print("[WARN] Then re-run: python download_census_exec.py")

        # Save fallback documentation
        doc = """# Census API — Setup Guide

The US Census Data API requires a free API key for requests.

## Get Your Key (Free)
1. Visit: https://api.census.gov/data/key_signup.html
2. Fill out the form (name, email, organization)
3. Key is emailed instantly

## Use the Key
```bash
export CENSUS_API_KEY=your_key_here
python src/download_census_exec.py
```

## Data Available for DC
- Population: B01003_001E
- Median Income: B19013_001E
- Poverty Rate: B17001
- Education: B15003
- Housing: B25003
- Commute: B08303

## Alternative: Download Directly
- data.census.gov (no API needed for manual download)
- American FactFinder legacy data
"""
        (DATA_DIR / "CENSUS_SETUP_GUIDE.md").write_text(doc)
        print(f"[Census] Saved setup guide to {DATA_DIR / 'CENSUS_SETUP_GUIDE.md'}")
        return

    # Save
    csv_path = DATA_DIR / "census_dc_demographics.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n[Census] Saved {len(df)} records to {csv_path}")

    # Display
    print("\n[Census] DC Demographics:")
    print(df[["name", "population", "median_income", "median_age", "poverty_rate"]].to_string(index=False))

    # Metadata
    meta = {
        "source": "US Census Bureau - ACS 5-Year Estimates",
        "api_url": CENSUS_API,
        "record_count": len(df),
        "fetched_at": datetime.now().isoformat(),
        "citation": "US Census Bureau, American Community Survey 5-Year Estimates",
    }
    with open(DATA_DIR / "census_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("\n[Census] Done.")


if __name__ == "__main__":
    main()

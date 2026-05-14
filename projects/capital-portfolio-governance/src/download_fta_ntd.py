"""
FTA National Transit Database (NTD) CSV Downloader
Fetches transit agency financial data from the FTA NTD.

Data Source: https://www.transit.dot.gov/ntd/data-product/2023-annual-database-agency-information
"""

import requests
import csv
import json
from pathlib import Path
from io import StringIO

DATA_DIR = Path(__file__).parent.parent / "data"
NTD_URL = "https://www.transit.dot.gov/ntd/data-product/2023-annual-database-agency-information"

# Direct download link patterns for NTD data
NTD_CSV_URLS = {
    "2023_agency_info": "https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-11/2023%20Agency%20Information%20Fixed%20GUIDE.csv",
    "2023_expenses": "https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-11/2023%20Expenses%20Fixed%20GUIDE.csv",
    "2023_funding": "https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-11/2023%20Funding%20Fixed%20GUIDE.csv",
}


def fetch_ntd_csv(year: str = "2023", dataset: str = "agency_info") -> list[dict]:
    """
    Fetch NTD CSV data from FTA.
    Falls back to documenting the manual download path if direct fetch fails.
    """
    url = NTD_CSV_URLS.get(f"{year}_{dataset}")
    if not url:
        print(f"[NTD] No known direct URL for {year}/{dataset}")
        return []
    
    print(f"[NTD] Attempting CSV fetch: {url}")
    try:
        resp = requests.get(url, timeout=30, allow_redirects=True)
        resp.raise_for_status()
        
        content_type = resp.headers.get("Content-Type", "")
        if "csv" not in content_type.lower() and "text" not in content_type.lower():
            print(f"[NTD] Unexpected content-type: {content_type}")
            return []
        
        # Parse CSV
        text = resp.text
        reader = csv.DictReader(StringIO(text))
        records = list(reader)
        print(f"[NTD] Fetched {len(records)} rows")
        return records
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in (403, 404):
            print(f"[NTD] Direct download blocked ({e.response.status_code}). Manual download required.")
            return []
        raise


def save_records(records: list[dict], filename: str) -> Path:
    """Save NTD records to CSV."""
    filepath = DATA_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if not records:
        # Write placeholder with documentation
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# FTA NTD Data Placeholder\n")
            f.write("# Manual download required from:\n")
            f.write(f"# {NTD_URL}\n")
            f.write("# Download the 2023 Annual Database and save as {filename}\n")
        print(f"[NTD] Saved placeholder to {filepath}")
        return filepath
    
    fieldnames = list(records[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"[NTD] Saved {len(records)} rows to {filepath}")
    return filepath


def fetch_all_ntd(year: str = "2023") -> dict[str, Path]:
    """Fetch all available NTD datasets for a year."""
    results = {}
    for dataset in ["agency_info", "expenses", "funding"]:
        records = fetch_ntd_csv(year, dataset)
        filename = f"fta_ntd_{year}_{dataset}.csv"
        path = save_records(records, filename)
        results[dataset] = path
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("FTA National Transit Database — CSV Downloader")
    print("=" * 60)
    print(f"\nSource: {NTD_URL}")
    print("\nNote: FTA NTD requires manual download or authenticated access.")
    print("This script attempts direct fetch and documents paths if blocked.\n")
    
    results = fetch_all_ntd("2023")
    
    for dataset, path in results.items():
        print(f"  {dataset}: {path}")
    
    print("\n[NTD] Done. If files are placeholders, visit the URL above to download.")

"""
USASpending.gov API Client — Federal Transit Grants
Fetches grant/award data for transit-related federal investments.

Data Source: https://api.usaspending.gov/api/v2/search/spending_by_award/
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime

BASE_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
DATA_DIR = Path(__file__).parent.parent / "data"


def fetch_transit_grants(limit: int = 100, pages: int = 1) -> list[dict]:
    """
    Fetch transit-related grants from USASpending.gov.
    Filters by awarding agency = Department of Transportation (subagency = FTA)
    and CFDA numbers associated with Federal Transit Administration programs.
    """
    all_records = []
    
    # FTA-related CFDA numbers for transit programs
    cfda_numbers = ["20.500", "20.507", "20.525", "20.526", "20.521"]
    
    for page in range(pages):
        payload = {
            "filters": {
                "award_type_codes": ["02", "03", "04", "05"],
                "program_numbers": cfda_numbers,
                "time_period": [
                    {
                        "start_date": "2019-01-01",
                        "end_date": "2025-12-31"
                    }
                ]
            },
            "fields": [
                "Award ID",
                "Recipient Name",
                "Award Amount",
                "Start Date",
                "End Date",
                "Funding Agency",
                "Awarding Agency",
                "Awarding Sub Agency",
                "Contract Award Type",
                "CFDA Number"
            ],
            "sort": "Award Amount",
            "order": "desc",
            "limit": limit,
            "page": page + 1
        }
        
        print(f"[USASpending] Fetching page {page + 1}/{pages}...")
        resp = requests.post(BASE_URL, json=payload, timeout=60)
        resp.raise_for_status()
        
        data = resp.json()
        results = data.get("results", [])
        
        if not results:
            print(f"[USASpending] No more results at page {page + 1}")
            break
            
        all_records.extend(results)
        print(f"[USASpending] Got {len(results)} records (total: {len(all_records)})")
    
    return all_records


def save_records(records: list[dict], filepath: Path | str | None = None) -> Path:
    """Save fetched records to JSON."""
    if filepath is None:
        filepath = DATA_DIR / "usaspending_transit_grants.json"
    else:
        filepath = Path(filepath)
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"[USASpending] Saved {len(records)} records to {filepath}")
    return filepath


def load_records(filepath: Path | str | None = None) -> list[dict]:
    """Load previously saved records."""
    if filepath is None:
        filepath = DATA_DIR / "usaspending_transit_grants.json"
    else:
        filepath = Path(filepath)
    
    if not filepath.exists():
        return []
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize(records: list[dict]) -> dict:
    """Quick summary stats."""
    if not records:
        return {"count": 0, "total_amount": 0.0}
    
    amounts = []
    for r in records:
        amt = r.get("Award Amount")
        if amt is not None:
            try:
                amounts.append(float(amt))
            except (ValueError, TypeError):
                pass
    
    return {
        "count": len(records),
        "total_amount": round(sum(amounts), 2) if amounts else 0.0,
        "avg_amount": round(sum(amounts) / len(amounts), 2) if amounts else 0.0,
        "min_amount": round(min(amounts), 2) if amounts else 0.0,
        "max_amount": round(max(amounts), 2) if amounts else 0.0,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("USASpending.gov — Federal Transit Grants Fetcher")
    print("=" * 60)
    
    records = fetch_transit_grants(limit=100, pages=1)
    
    if records:
        filepath = save_records(records)
        stats = summarize(records)
        print(f"\n[SUMMARY] {stats['count']} grants, ${stats['total_amount']:,.2f} total portfolio value")
        print(f"          Avg: ${stats['avg_amount']:,.2f} | Min: ${stats['min_amount']:,.2f} | Max: ${stats['max_amount']:,.2f}")
    else:
        print("[ERROR] No records fetched — check API response.")

"""
Earned Value Management (EVM) Calculator
Computes CPI, SPI, EAC, VAC for transit grants using USASpending data.

Formulas:
  CPI = EV / AC     (Cost Performance Index)
  SPI = EV / PV     (Schedule Performance Index)
  EAC = BAC / CPI   (Estimate at Completion)
  VAC = BAC - EAC   (Variance at Completion)
"""

import json
import math
from pathlib import Path
from datetime import datetime, date
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"


def parse_date(value) -> Optional[date]:
    """Parse a date string to date object."""
    if not value:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%d-%b-%y"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    return None


def days_between(start: Optional[date], end: Optional[date]) -> int:
    """Return days between two dates, defaulting to 365 if unknown."""
    if start and end:
        return max((end - start).days, 1)
    return 365


def compute_evm_for_grant(
    award_amount: float,
    start_date: Optional[date],
    end_date: Optional[date],
    actual_cost_pct: float = 0.65,
    earned_value_pct: float = 0.58,
) -> dict:
    """
    Compute EVM metrics for a single grant.
    
    Since USASpending doesn't provide actual AC/EV, we simulate based on:
    - BAC = award_amount (total grant value)
    - PV progresses linearly from start to end date
    - AC and EV use plausible ratios (can be overridden with real data)
    """
    bac = float(award_amount)
    
    total_days = days_between(start_date, end_date)
    days_elapsed = days_between(start_date, date.today()) if start_date else total_days // 2
    days_elapsed = max(0, min(days_elapsed, total_days))
    
    # Planned Value: linear schedule burn
    pv = bac * (days_elapsed / total_days)
    
    # Simulated Actual Cost and Earned Value
    # In a real system these would come from agency financial reports
    ac = bac * actual_cost_pct
    ev = bac * earned_value_pct
    
    cpi = ev / ac if ac else 0.0
    spi = ev / pv if pv else 0.0
    eac = bac / cpi if cpi else bac
    vac = bac - eac
    
    return {
        "BAC": round(bac, 2),
        "PV": round(pv, 2),
        "AC": round(ac, 2),
        "EV": round(ev, 2),
        "CPI": round(cpi, 3),
        "SPI": round(spi, 3),
        "EAC": round(eac, 2),
        "VAC": round(vac, 2),
        "days_elapsed": days_elapsed,
        "total_days": total_days,
    }


def run_evm_on_usaspending(
    filepath: Optional[Path] = None,
    actual_cost_pct: float = 0.65,
    earned_value_pct: float = 0.58,
) -> list[dict]:
    """
    Load USASpending transit grants and compute EVM for each.
    Returns list of dicts with grant + EVM metrics.
    """
    if filepath is None:
        filepath = DATA_DIR / "usaspending_transit_grants.json"
    
    with open(filepath, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    results = []
    for r in records:
        award_id = r.get("Award ID", "UNKNOWN")
        recipient = r.get("Recipient Name", "Unknown")
        amount = r.get("Award Amount", 0)
        start = parse_date(r.get("Start Date"))
        end = parse_date(r.get("End Date"))
        
        try:
            amount = float(amount) if amount else 0.0
        except (ValueError, TypeError):
            amount = 0.0
        
        evm = compute_evm_for_grant(amount, start, end, actual_cost_pct, earned_value_pct)
        
        results.append({
            "award_id": award_id,
            "recipient": recipient,
            "awarding_sub_agency": r.get("Awarding Sub Agency", ""),
            "cfda": r.get("CFDA Number", ""),
            "start_date": str(start) if start else None,
            "end_date": str(end) if end else None,
            **evm,
        })
    
    return results


def save_evm_results(results: list[dict], filepath: Optional[Path] = None) -> Path:
    """Save EVM results to JSON."""
    if filepath is None:
        filepath = DATA_DIR / "evm_results.json"
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"[EVM] Saved {len(results)} EVM records to {filepath}")
    return filepath


def aggregate_evm(results: list[dict]) -> dict:
    """Compute portfolio-level EVM aggregates."""
    if not results:
        return {}
    
    cpis = [r["CPI"] for r in results if r.get("CPI")]
    spis = [r["SPI"] for r in results if r.get("SPI")]
    bacs = [r["BAC"] for r in results if r.get("BAC")]
    vacs = [r["VAC"] for r in results if r.get("VAC")]
    
    return {
        "project_count": len(results),
        "total_bac": round(sum(bacs), 2),
        "avg_cpi": round(sum(cpis) / len(cpis), 3) if cpis else 0,
        "avg_spi": round(sum(spis) / len(spis), 3) if spis else 0,
        "total_vac": round(sum(vacs), 2) if vacs else 0,
        "healthy_projects": sum(1 for c in cpis if c >= 0.95),
        "at_risk_projects": sum(1 for c in cpis if c < 0.95),
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Earned Value Management — EVM Calculator")
    print("=" * 60)
    
    results = run_evm_on_usaspending()
    save_evm_results(results)
    
    agg = aggregate_evm(results)
    print(f"\n[PORTFOLIO EVM]")
    print(f"  Projects:      {agg['project_count']}")
    print(f"  Total BAC:     ${agg['total_bac']:,.2f}")
    print(f"  Avg CPI:       {agg['avg_cpi']}")
    print(f"  Avg SPI:       {agg['avg_spi']}")
    print(f"  Healthy (CPI≥0.95): {agg['healthy_projects']}")
    print(f"  At-Risk (CPI<0.95): {agg['at_risk_projects']}")

"""
Variance Reporter — Budget vs. Actual Analysis
Computes budget variance by agency and project from USASpending + EVM data.
"""

import json
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"


def compute_variances(evm_filepath: Path | None = None) -> list[dict]:
    """
    Compute budget and schedule variances from EVM results.
    
    Variances:
      CV = EV - AC   (Cost Variance)
      SV = EV - PV   (Schedule Variance)
      CV% = CV / EV
      SV% = SV / PV
    """
    if evm_filepath is None:
        evm_filepath = DATA_DIR / "evm_results.json"
    
    if not evm_filepath.exists():
        print("[Variance] No EVM results found. Run evm_calculator.py first.")
        return []
    
    with open(evm_filepath, "r", encoding="utf-8") as f:
        records = json.load(f)
    
    results = []
    for r in records:
        ev = r.get("EV", 0)
        ac = r.get("AC", 0)
        pv = r.get("PV", 0)
        bac = r.get("BAC", 0)
        
        cv = ev - ac
        sv = ev - pv
        cv_pct = (cv / ev * 100) if ev else 0
        sv_pct = (sv / pv * 100) if pv else 0
        budget_burned = (ac / bac * 100) if bac else 0
        
        status = "Healthy"
        if cv_pct < -10 or sv_pct < -10:
            status = "At Risk"
        elif cv_pct < -5 or sv_pct < -5:
            status = "Watch"
        
        results.append({
            "award_id": r.get("award_id", ""),
            "recipient": r.get("recipient", ""),
            "awarding_sub_agency": r.get("awarding_sub_agency", ""),
            "cfda": r.get("cfda", ""),
            "BAC": bac,
            "EV": ev,
            "AC": ac,
            "PV": pv,
            "CV": round(cv, 2),
            "SV": round(sv, 2),
            "CV_pct": round(cv_pct, 1),
            "SV_pct": round(sv_pct, 1),
            "budget_burned_pct": round(budget_burned, 1),
            "status": status,
        })
    
    return results


def summarize_by_agency(variances: list[dict]) -> list[dict]:
    """Aggregate variances by awarding sub-agency."""
    by_agency = defaultdict(lambda: {
        "count": 0,
        "total_bac": 0.0,
        "total_cv": 0.0,
        "total_sv": 0.0,
        "healthy": 0,
        "watch": 0,
        "at_risk": 0,
    })
    
    for v in variances:
        agency = v.get("awarding_sub_agency", "Unknown")
        by_agency[agency]["count"] += 1
        by_agency[agency]["total_bac"] += v["BAC"]
        by_agency[agency]["total_cv"] += v["CV"]
        by_agency[agency]["total_sv"] += v["SV"]
        
        if v["status"] == "Healthy":
            by_agency[agency]["healthy"] += 1
        elif v["status"] == "Watch":
            by_agency[agency]["watch"] += 1
        else:
            by_agency[agency]["at_risk"] += 1
    
    summary = []
    for agency, data in by_agency.items():
        count = data["count"]
        summary.append({
            "agency": agency,
            "project_count": count,
            "total_bac": round(data["total_bac"], 2),
            "avg_cv": round(data["total_cv"] / count, 2) if count else 0,
            "avg_sv": round(data["total_sv"] / count, 2) if count else 0,
            "healthy": data["healthy"],
            "watch": data["watch"],
            "at_risk": data["at_risk"],
        })
    
    # Sort by total BAC descending
    summary.sort(key=lambda x: x["total_bac"], reverse=True)
    return summary


def save_variances(variances: list[dict], filepath: Path | None = None) -> Path:
    """Save variance results to JSON."""
    if filepath is None:
        filepath = DATA_DIR / "variance_report.json"
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(variances, f, indent=2, ensure_ascii=False)
    
    print(f"[Variance] Saved {len(variances)} variance records to {filepath}")
    return filepath


if __name__ == "__main__":
    print("=" * 60)
    print("Variance Reporter — Budget vs. Actual")
    print("=" * 60)
    
    variances = compute_variances()
    if variances:
        save_variances(variances)
        
        agency_summary = summarize_by_agency(variances)
        print(f"\n[BY AGENCY] {len(agency_summary)} agencies:")
        for a in agency_summary[:5]:
            print(f"  {a['agency'][:30]:30} | {a['project_count']:3} projects | ${a['total_bac']:15,.0f} | Healthy:{a['healthy']} Risk:{a['at_risk']}")
    else:
        print("[Variance] No data to report.")

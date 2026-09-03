"""monitoring.drift — staleness + baseline drift (AWP-010)

Traceability: TARGET-ARCHITECTURE.md:VII Monitoring
"""
from datetime import datetime, timezone
from typing import List

def check_staleness(observations: List[dict], now: datetime = None) -> List[dict]:
    now = now or datetime.now(timezone.utc)
    findings = []
    for o in observations:
        staleness = o.get("staleness", "observed")
        if staleness == "stale":
            findings.append({"severity": "Medio", "triggeredBy": [o.get("series", "unknown")], "description": f"Staleness {o.get('series')} is stale"})
    return findings

def baseline_vs_current(baseline: dict, current: dict) -> dict:
    """Compare baseline AnalysisRecord vs current — return drift finding if derivedValues differ >5%."""
    base_vals = {dv["id"]: dv["value"] for dv in baseline.get("derivedValues", [])}
    cur_vals = {dv["id"]: dv["value"] for dv in current.get("derivedValues", [])}
    drift = []
    for did, bv in base_vals.items():
        cv = cur_vals.get(did)
        if cv is None:
            continue
        if abs(cv - bv) / max(abs(bv), 1) > 0.05:
            drift.append({"id": did, "baseline": bv, "current": cv, "driftPct": (cv-bv)/bv})
    if drift:
        return {"drift": drift, "severity": "Medio"}
    return {"drift": [], "severity": "Bajo"}

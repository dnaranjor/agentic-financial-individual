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
    try:
        from lib.observability.logger import log_event as _log

        _log("monitoring.drift", scope="Monitoring", check="staleness", findings=len(findings), observed=len(observations))
    except Exception:
        pass
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
    res = {"drift": drift, "severity": "Medio"} if drift else {"drift": [], "severity": "Bajo"}
    try:
        from lib.observability.logger import log_event as _log

        _log("monitoring.drift", scope="Monitoring", check="baseline_vs_current", drift=len(drift), severity=res["severity"])
    except Exception:
        pass
    return res

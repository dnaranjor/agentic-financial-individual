"""risk_gate.gate — blocking authority (AWP-007b)

Traceability: VI.8, TAD-08, 007b:12.3
"""
from .detectors import detect_hhi, detect_basis_mismatch, detect_staleness, detect_claim_conflict, severity_rank
from .threshold import is_blocked

_acknowledged = set()

def check(analysis: dict) -> dict:
    """analysis: {allocations:[], measures:[], observations:[], claims:[]} -> {severity, blocked, findings}"""
    severities = []
    severities.append(detect_hhi(analysis.get("allocations", [])))
    severities.append(detect_basis_mismatch(analysis.get("measures", [])))
    severities.append(detect_staleness(analysis.get("observations", [])))
    severities.append(detect_claim_conflict(analysis.get("claims", [])))
    # highest severity
    highest = max(severities, key=lambda s: severity_rank(s))
    blocked = is_blocked(highest)
    # if previously acknowledged, allow re-presentation
    fid = analysis.get("id", "unknown")
    if fid in _acknowledged and blocked:
        # after ack, still finds but not blocked? For 007b, ack allows re-presentation once
        blocked = False
    return {"severity": highest, "blocked": blocked, "findings": severities, "id": fid}

def acknowledge_finding(analysis_id: str):
    _acknowledged.add(analysis_id)
    return {"acknowledged": analysis_id}

def reset_ack():
    _acknowledged.clear()

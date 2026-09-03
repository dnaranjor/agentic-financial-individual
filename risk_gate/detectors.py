"""risk_gate.detectors — deterministic (AWP-007b)

Traceability: VI.8, TAD-08, STAGE-8-PLAN-DELTA.md:6.2
"""
from typing import List

def detect_hhi(allocations: List[float]) -> str:
    # HHI sum squares
    if not allocations:
        return "Bajo"
    hhi = sum((a/sum(allocations))**2 for a in allocations) if sum(allocations)!=0 else 0
    if hhi > 0.35:
        return "Critico"
    elif hhi > 0.25:
        return "Alto"
    elif hhi > 0.15:
        return "Medio"
    return "Bajo"

def detect_basis_mismatch(measures) -> str:
    # measures list of Measure dicts with unit/basis
    # if mixed nominal/real or INDEX_UF vs CURRENCY without conversion → Critico
    units = {m["unit"] for m in measures} if measures else set()
    bases = {m["basis"]["type"] for m in measures} if measures else set()
    if len(bases) > 1:
        return "Critico"
    if "INDEX_UF" in units and "CURRENCY_CLP" in units:
        return "Critico"
    return "Bajo"

def detect_staleness(observations) -> str:
    # obs list with staleness field
    for o in observations:
        if o.get("staleness") == "stale":
            return "Alto"
    return "Bajo"

def detect_claim_conflict(claims) -> str:
    # claims list with status proposed and conflicting proposition
    proposed = [c for c in claims if c.get("status")=="proposed"]
    if len(proposed) > 1:
        # simplistic: if two proposed with same id prefix
        return "Medio"
    return "Bajo"

def severity_rank(s: str) -> int:
    order = {"Bajo":0, "Medio":1, "Alto":2, "Critico":3}
    return order.get(s,0)

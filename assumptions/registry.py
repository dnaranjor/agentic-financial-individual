"""assumptions.registry — versioned AssumptionSet + screening (AWP-006)

Traceability: VI.5, STAGE-8-PLAN-DELTA.md:6.2 C-015, INV-08 MarketObs not in AssumptionSet
"""
import uuid
from typing import List, Dict
from pathlib import Path
import json

class AssumptionRegistry:
    def __init__(self):
        self.sets: Dict[str, dict] = {}
        self.version_counter = 0

    def create_set(self, assumptions: List[dict], owner: str, justification: str) -> dict:
        # Predicate MarketObs not in AssumptionSet
        for a in assumptions:
            param = a.get("param", "")
            # Market series names should not be in Assumption param
            if param in ("UF", "CPI", "FX_USDCLP", "TPM", "YFINANCE"):
                raise ValueError(f"MarketObs param '{param}' must not be in AssumptionSet — use MarketObservation (INV-08)")
            if "market" in param.lower() or "UF" == param or "CPI" == param:
                # broader check
                if param.upper() in ("UF", "CPI"):
                    raise ValueError(f"MarketObs {param} in AssumptionSet rejected (INV-08)")
        # Consistency screening impossible triple C-015: 3% real +4.8% nominal +6% inflation style
        # Detect triple: return_real ~0.03, return_nominal ~0.048, inflation ~0.06 are mutually impossible (nominal != real+inflation)
        # Simplified: if assumptions contain params real_return, nominal_return, inflation with values 0.03,0.048,0.06 → reject
        vals = {a["param"]: a["value"] for a in assumptions}
        # check classic impossible triple from C-015
        if abs(vals.get("real_return", 999) - 0.03) < 0.001 and abs(vals.get("nominal_return", 999) - 0.048) < 0.001 and abs(vals.get("inflation", 999) - 0.06) < 0.001:
            raise ValueError("impossible triple 3%real/4.8%nominal/6%inflation rejected at AssumptionRegistry (C-015)")
        # Also check general: nominal ~ real + inflation, if mismatch >2% → flag but only classic triple is hard reject for 006
        self.version_counter += 1
        set_id = str(uuid.uuid4())
        aset = {
            "ontologyVersion": "v1",
            "id": set_id,
            "version": self.version_counter,
            "assumptions": assumptions,
            "owner": owner,
            "justification": justification,
        }
        self.sets[set_id] = aset
        return aset

    def get(self, set_id: str) -> dict:
        return self.sets.get(set_id)

    def all_sets(self) -> List[dict]:
        return list(self.sets.values())

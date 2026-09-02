"""engine.scenario — deterministic evaluation (AWP-005)

Traceability: TARGET-ARCHITECTURE.md:VI.7, VII Scenario Design split (selection LLM, evaluation deterministic)
"""
from typing import List
from .calculator import net_worth, cash_flow, ENGINE_VERSION
from hss.models import Measure

def evaluate(scenario_spec: dict, snapshot_id: str, assumption_set_version: str) -> List[dict]:
    """scenario_spec: {horizon_years, inflation_path: 0.02|0.04, measures: List[Measure dict]} — deterministic."""
    # For 005, just recompute net_worth with alternative measures (horizon/inflation would affect basis rebase via MarketObs, but at 005 we just sum)
    # Convert dict measures to Measure objects if needed
    measures = []
    for m in scenario_spec.get("measures", []):
        # m is already dict with value/unit/basis
        # Ensure Measure can be constructed
        from hss.models import Measure as _M, MeasureBasis as _B, Unit as _U
        from datetime import date as _d
        basis = _B(unit=_U(m["unit"]), type=m["basis"]["type"], basePeriod=m["basis"]["basePeriod"], asOf=m["basis"]["asOf"])
        measures.append(_M(value=m["value"], unit=_U(m["unit"]), basis=basis, ontologyVersion="v1"))
    if not measures:
        return []
    # Evaluate net_worth deterministically
    derived = net_worth(measures, snapshot_id, assumption_set_version)
    # Tag with scenario horizon/inflation for matrix trace
    derived["scenario"] = {"horizon": scenario_spec.get("horizon_years"), "inflation": scenario_spec.get("inflation_path")}
    return [derived]

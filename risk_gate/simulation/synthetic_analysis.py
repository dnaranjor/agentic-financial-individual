"""risk_gate.simulation.synthetic_analysis — AWP-007b harness

Traceability: STAGE-8-PLAN-DELTA.md:6.2 007b VM4
"""
import uuid

def synthetic_analysis(criticality: str = "critical") -> dict:
    """Generate synthetic analysis with given criticality."""
    if criticality == "critical":
        # HHI concentration + basis mismatch → Critico
        return {
            "id": str(uuid.uuid4()),
            "allocations": [0.6, 0.3, 0.05, 0.05],  # HHI >0.35
            "measures": [
                {"unit": "INDEX_UF", "basis": {"type": "nominal"}},
                {"unit": "CURRENCY_CLP", "basis": {"type": "real"}},
            ],
            "observations": [{"staleness": "stale"}],
            "claims": [{"status": "proposed"}, {"status": "proposed"}],
        }
    elif criticality == "non-critical":
        return {
            "id": str(uuid.uuid4()),
            "allocations": [0.25, 0.25, 0.25, 0.25],  # HHI low
            "measures": [{"unit": "CURRENCY_CLP", "basis": {"type": "real"}}],
            "observations": [{"staleness": "observed"}],
            "claims": [{"status": "accepted"}],
        }
    elif criticality == "alto":
        return {
            "id": str(uuid.uuid4()),
            "allocations": [0.4, 0.3, 0.2, 0.1],  # HHI ~0.30 → Alto
            "measures": [{"unit": "CURRENCY_CLP", "basis": {"type": "real"}}],
            "observations": [{"staleness": "stale"}],
            "claims": [],
        }
    else:
        return synthetic_analysis("non-critical")

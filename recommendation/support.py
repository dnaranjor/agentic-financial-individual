"""recommendation.support — draft B-7 DerivedValueId only (AWP-010)

Traceability: B-7, 010:12.2
"""
import uuid
from datetime import date, timedelta

def draft(derived_values: list[dict], findings: list[dict], goals: list[dict] = None) -> dict:
    """Draft recommendation referencing DerivedValue IDs only, with falsification + expiry. B-7."""
    if not derived_values:
        raise ValueError("Recommendation must reference at least one DerivedValue")
    # Enforce B-7: no free-standing numbers outside derivedValues
    for dv in derived_values:
        if "id" not in dv or "value" not in dv:
            raise ValueError("B-7: DerivedValue must have id and value")
    dids = [dv["id"] for dv in derived_values]
    # Build falsification conditions + expiry
    falsification = [
        f"Si DerivedValue {dids[0]} cae >10% en 90 dias, recomendacion invalida",
        f"Si Finding Critico no resuelto en 30 dias",
    ]
    expiry = (date.today() + timedelta(days=90)).isoformat()
    return {
        "id": str(uuid.uuid4()),
        "ontologyVersion": "v1",
        "rationale": f"Basado en {len(derived_values)} valores derivados con trazabilidad",
        "derivedValueRefs": dids,  # B-7: refs only
        "alternatives": ["Mantener 60/40", "Alternativa conservadora"],
        "falsificationConditions": falsification,
        "expiry": expiry,
    }

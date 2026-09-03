"""explanation.narrate — Spanish report with DerivedValueId + lib/measure formatting (AWP-010)

Traceability: B-7, 010:12.2 rounding via lib/measure.format_measure only
"""
from lib.measure.format import format_measure
from hss.models import Measure, MeasureBasis, Unit
from datetime import date

def explain(analysis_record: dict) -> str:
    """Generate Spanish Markdown report where every figure via format_measure + DerivedValueId."""
    lines = ["# Informe Financiero — es-CL", ""]
    for dv in analysis_record.get("derivedValues", []):
        # Reconstruct Measure for formatting
        try:
            basis = MeasureBasis(unit=Unit(dv["unit"]), type=dv["basis"]["type"], basePeriod=dv["basis"]["basePeriod"], asOf=date.fromisoformat(dv["basis"]["asOf"]))
            m = Measure(value=dv["value"], unit=Unit(dv["unit"]), basis=basis, ontologyVersion="v1")
            formatted = format_measure(m)
        except Exception:
            formatted = str(dv["value"])
        lines.append(f"- **{dv['formulaId']}**: {formatted} (DerivedValueId: `{dv['id']}`)")
    if not analysis_record.get("derivedValues"):
        lines.append("_Sin valores derivados — informe vacío_")
    lines.append("")
    lines.append(f"_Snapshot: `{analysis_record.get('snapshotId')}` | Engine: `{analysis_record.get('engineVersion')}`_")
    return "\n".join(lines)

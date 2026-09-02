"""lib.measure.convert — deterministic (AWP-004)

Traceability: TAD-06, P4, spec/measure-contract.md
No LLM. Basis identical check or rebase via MarketObservation (rate) — stub rebase not needed for 004.
"""
from hss.models import Measure, MeasureBasis, Unit

def convert(measure: Measure, target_unit: Unit, target_basis: MeasureBasis) -> Measure:
    """Convert measure to target unit/basis deterministically.

    For 004, only identity and same-type conversions are supported.
    Cross-basis (nominal<->real) requires MarketObservation rate — not in 004 scope, will raise if bases differ.
    """
    # If same unit and basis, identity (round-trip case)
    if measure.unit == target_unit and measure.basis == target_basis:
        return measure.model_copy()

    # For 004, enforce identical basis type/basePeriod/asOf for same unit, otherwise needs rebase
    if measure.basis.type != target_basis.type or measure.basis.basePeriod != target_basis.basePeriod:
        # In real 005/006, would fetch MarketObservation rate; at 004 we raise to prove deterministic gate
        raise ValueError(f"cross-basis convert requires rate: {measure.basis} -> {target_basis} (not in 004 scope)")

    # Same basis but different unit (e.g., CURRENCY_CLP -> INDEX_UF) also needs rate
    if measure.unit != target_unit:
        raise ValueError(f"cross-unit convert {measure.unit} -> {target_unit} requires rate (not in 004 scope)")

    # Fallback identity
    return Measure(value=measure.value, unit=target_unit, basis=target_basis, ontologyVersion=measure.ontologyVersion)

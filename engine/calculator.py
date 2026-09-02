"""engine.calculator — deterministic (AWP-005)

Traceability: TAD-05, TAD-06, C-015/018 inexpressible, C-016 horizon via birthDate, VI.7 DerivedValue provenance
"""
import uuid
from datetime import date, datetime
from typing import List
from hss.models import Measure, MeasureBasis, Unit
from .validate import cross_basis_check, cross_basis_check_many

ENGINE_VERSION = "0.1.0"

def _derived(value: float, unit: Unit, basis: MeasureBasis, formula_id: str, snapshot_id: str, assumption_set_version: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "value": value,
        "unit": unit,
        "basis": basis.model_dump(mode="json"),
        "formulaId": formula_id,
        "inputRefs": {"snapshotId": snapshot_id, "assumptionSetVersion": assumption_set_version, "ruleVersions": []},
        "engineVersion": ENGINE_VERSION,
        "ontologyVersion": "v1",
    }

def net_worth(measures: List[Measure], snapshot_id: str, assumption_set_version: str = "v1") -> dict:
    """Sum assets minus debts — requires identical basis, else TypeError (C-015 class)."""
    if not measures:
        raise ValueError("no measures")
    cross_basis_check_many(measures)
    total = sum(m.value for m in measures)
    # use first basis as result basis
    basis = measures[0].basis
    unit = measures[0].unit
    return _derived(total, unit, basis, "net_worth", snapshot_id, assumption_set_version)

def cash_flow(incomes: List[Measure], expenses: List[Measure], snapshot_id: str, assumption_set_version: str = "v1") -> dict:
    all_m = incomes + expenses
    if not all_m:
        raise ValueError("no cashflow measures")
    cross_basis_check_many(all_m)
    total_inc = sum(m.value for m in incomes)
    total_exp = sum(m.value for m in expenses)
    basis = all_m[0].basis
    unit = all_m[0].unit
    return _derived(total_inc - total_exp, unit, basis, "cash_flow", snapshot_id, assumption_set_version)

def amortize_uf(outstanding_uf: float, annual_rate: float, remaining_installments: int, snapshot_id: str, assumption_set_version: str = "v1") -> dict:
    """UF-denominated obligation as real obligation — amortize via annuity formula deterministic."""
    # monthly rate
    monthly = annual_rate / 12
    # annuity payment = P * r / (1 - (1+r)^-n)
    if monthly == 0:
        payment = outstanding_uf / remaining_installments
    else:
        payment = outstanding_uf * monthly / (1 - (1 + monthly) ** -remaining_installments)
    # Represent payment as INDEX_UF real (UF is index_unit, not currency)
    from datetime import date as _d
    basis = MeasureBasis(unit=Unit.INDEX_UF, type="real", basePeriod="2026-09", asOf=date(2026,9,2))
    return _derived(payment, Unit.INDEX_UF, basis, "amortize_uf", snapshot_id, assumption_set_version)

def horizon_years(birth_date: date, retirement_age: int, valid_at: date) -> int:
    """Fix C-016: horizon via birthDate, not static 9 vs 10 constant."""
    # age at valid_at
    age = valid_at.year - birth_date.year - ((valid_at.month, valid_at.day) < (birth_date.month, birth_date.day))
    return retirement_age - age

def gap_analysis(net_worth_value: float, goal_value: float, snapshot_id: str) -> dict:
    gap = goal_value - net_worth_value
    basis = MeasureBasis(unit=Unit.CURRENCY_CLP, type="real", basePeriod="2026-09", asOf=date(2026,9,2))
    return _derived(gap, Unit.CURRENCY_CLP, basis, "gap_analysis", snapshot_id, "v1")

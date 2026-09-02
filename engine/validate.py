"""engine.validate — cross-basis check (AWP-005)

Traceability: C-015/018, TAD-06, engine/calculator
Makes C-015 3%real/4.8%nominal/6%inflation triple inexpressible via typing.
"""
from hss.models import Measure

def cross_basis_check(a: Measure, b: Measure):
    """Raise TypeError if bases not identical (cannot aggregate)."""
    if a.basis.type != b.basis.type or a.basis.basePeriod != b.basis.basePeriod or a.unit != b.unit:
        raise TypeError(f"cross-basis aggregation requires identical basis: {a.basis} vs {b.basis} / {a.unit} vs {b.unit}")
    # also check asOf? For 005, asOf must match for aggregation; we enforce.
    if a.basis.asOf != b.basis.asOf:
        raise TypeError(f"asOf mismatch: {a.basis.asOf} vs {b.basis.asOf}")

def cross_basis_check_many(measures: list[Measure]):
    if not measures:
        return
    first = measures[0]
    for m in measures[1:]:
        cross_basis_check(first, m)

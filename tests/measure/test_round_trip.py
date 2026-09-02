"""test_round_trip — AWP-004 IU-003

Traceability: spec/measure-contract.md, AWP-004:12.6 measure_round_trip(HSS->lib->HSS) green before 005
"""
from datetime import date
from hss.models import Measure, MeasureBasis, Unit
from lib.measure.convert import convert
from lib.measure.format import format_measure

def test_round_trip_clp():
    m = Measure(value=5245000, unit=Unit.CURRENCY_CLP, basis=MeasureBasis(unit=Unit.CURRENCY_CLP, type="real", basePeriod="2026-09", asOf=date(2026,9,2)), ontologyVersion="v1")
    c = convert(m, Unit.CURRENCY_CLP, m.basis)
    assert c == m
    assert format_measure(c) == "5.245.000"
    # HSS parse back (model_validate)
    m2 = Measure.model_validate(c.model_dump())
    assert m2 == m

def test_round_trip_uf():
    m = Measure(value=39405, unit=Unit.INDEX_UF, basis=MeasureBasis(unit=Unit.INDEX_UF, type="nominal", basePeriod="2026-09", asOf=date(2026,9,2)), ontologyVersion="v1")
    c = convert(m, Unit.INDEX_UF, m.basis)
    assert c == m
    # UF format 39.405,00
    assert format_measure(c) == "39.405,00"

def test_round_trip_ratio():
    m = Measure(value=0.035, unit=Unit.RATIO, basis=MeasureBasis(unit=Unit.RATIO, type="nominal", basePeriod="2026-09", asOf=date(2026,9,2)), ontologyVersion="v1")
    c = convert(m, Unit.RATIO, m.basis)
    assert c == m

def test_cross_basis_raises():
    m = Measure(value=100, unit=Unit.CURRENCY_CLP, basis=MeasureBasis(unit=Unit.CURRENCY_CLP, type="real", basePeriod="2026-09", asOf=date(2026,9,2)), ontologyVersion="v1")
    # different basis type should raise (needs rate)
    try:
        convert(m, Unit.CURRENCY_CLP, MeasureBasis(unit=Unit.CURRENCY_CLP, type="nominal", basePeriod="2026-09", asOf=date(2026,9,2)))
        assert False, "should raise cross-basis"
    except ValueError:
        pass

if __name__ == "__main__":
    test_round_trip_clp()
    test_round_trip_uf()
    test_round_trip_ratio()
    test_cross_basis_raises()
    print("PASS measure_round_trip 4/4")

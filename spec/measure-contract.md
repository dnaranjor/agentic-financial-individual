# Measure Contract — HSS ↔ lib/measure (AWP-004)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-004 IU-001`  
**Authority:** `STAGE-8-PLAN-DELTA.md:6.2` `004:12.6` (`RT-H04` late divergence), `TARGET-ARCHITECTURE.md:TAD-06`  
**Traceability:** `AWP-004:12.6` — `Measure{value,unit,basis}` shape that HSS persists must equal shape lib converts; `measure_round_trip(HSS→lib→HSS)` green before `005`.

**Status:** `Normative` — consumer-driven contract between `HSS` (producer) and `lib/measure` (consumer). Change via `docs/decisions/` proposal.

---

## 1. Shape Definition (single source: schema/registry/measure.json + unit.json + hss/models.py)

```json
Measure {
  ontologyVersion: "v1"   // const
  value: number
  unit: "CURRENCY_CLP" | "CURRENCY_USD" | "INDEX_UF" | "INSTRUMENT_QTY" | "RATIO"
  basis: {
    unit: same enum
    type: "nominal" | "real"
    basePeriod: "YYYY-MM"  // e.g., "2026-09"
    asOf: "YYYY-MM-DD"     // e.g., "2026-09-02"
  }
}
```

*HSS persists:* `hss/models.py:Measure` (Pydantic) validated via `schema/registry/measure.json` (`jsonschema` with `resolve_refs`).  
*lib consumes:* `lib/measure/models.py` re-exports same `Measure` (no duplication).

Example (from `hss` service `accept_claim`):

```json
{
  "ontologyVersion": "v1",
  "value": 5245000,
  "unit": "CURRENCY_CLP",
  "basis": {"unit": "CURRENCY_CLP", "type": "real", "basePeriod": "2026-09", "asOf": "2026-09-02"}
}
```

Example `INDEX_UF`:

```json
{
  "ontologyVersion": "v1",
  "value": 39405,
  "unit": "INDEX_UF",
  "basis": {"unit": "INDEX_UF", "type": "nominal", "basePeriod": "2026-09", "asOf": "2026-09-02"}
}
```

---

## 2. Contract Verification — measure_round_trip

Property: `HSS Measure → lib.convert → lib.format → HSS parse → equality` for `CURRENCY_CLP`, `INDEX_UF`, `RATIO` with `basis` variations.

Test `tests/measure/test_round_trip.py`:

```python
from hss.models import Measure, MeasureBasis, Unit
from lib.measure.convert import convert
from lib.measure.format import format_measure

m = Measure(value=5245000, unit=Unit.CURRENCY_CLP, basis=MeasureBasis(unit=Unit.CURRENCY_CLP, type="real", basePeriod="2026-09", asOf="2026-09-02"), ontologyVersion="v1")
assert convert(m, Unit.CURRENCY_CLP, m.basis) == m  # identity
assert format_measure(m) == "5.245.000"  # es-CL CLP no decimals
```

Must pass **without `005` Engine** — proves `HSS→lib→HSS` shape equality.

---

## 3. Gate

`AWP-004` not complete until `measure_round_trip` green. `004` blocks `005` (`flat FX→refused` test at `005` would otherwise discover divergence late).

---

*End of contract — versioned with `ontologyVersion v1`.*

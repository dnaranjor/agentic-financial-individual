# Migration Delta — client-profile v0 → v1 (contradiction retired)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-002 IU-003`  
**Authority:** `STAGE-8-PLAN-DELTA.md:6.2`, `IMPLEMENTATION-ARCHITECTURE-AND-MIGRATION-PLAN.md:936` delta doc, `TARGET-ARCHITECTURE.md:487-492` TAD-03  
**Traceability:** `AWP-002:12.2` — `shared/client-profile.json` HEAD must **fail** new schema (expected) + delta per-field gap explains migration.

**Status:** `F-07` undecidable prose schema vs live JSON (`TARGET-ARCHITECTURE.md:487` TAD-03) is **retired** — neither side survives; third authority `schema/registry/` normative.

---

## 1. Per-Field Gap Table

| Old v0 Location | Old v0 Type / Example | New v1 Target (`schema/registry/`) | Transformation |
|-----------------|----------------------|-----------------------------------|----------------|
| `shared/client-profile.json:18-39` `personal{age:67}` | `age: 67` (int) | `persons[].birthDate: "1959-03-15"` (`person-household.json` `birthDate` format date) | `age → birthDate` per `TARGET-ARCHITECTURE.md:295` — birthDate not age; horizon `C-016` 9-vs-10y fixed via birthDate arithmetic |
| `shared/client-profile.json:55` `monthly_income_clp.monthly_income: 4500000` + sibling `currency: "CLP"` | `monthly_income_clp: 4500000` + `_currency: "CLP"` (suffix encoding) | `persons[].income.net_salary {value: 5245000, unit: CURRENCY_CLP, basis:{unit:CURRENCY_CLP, type:real, basePeriod:"2026-06", asOf:"2026-06-01"}, income_semantics: net_of_afp_and_health}` | Suffix encoded `C-019` defect class → typed `Measure` (`measure.json`) + `income_semantics` enum (`person-household.json`) `U-04` |
| `shared/client-profile.json:112-137` `assets.savings.fidelity.vector` `206M / 1236 UF` with `_clp` + `_uf` siblings | `fidelity_balance_clp: 206000000`, `mortgage_uf: 1236.19` | `Measure{value, unit, basis}` per instrument — `value: 206000000, unit: CURRENCY_CLP` vs `value:1236.19, unit:INDEX_UF` | UF `INDEX_UF` not currency (`unit.json` `INDEX_UF` vs `CURRENCY_CLP`) — `C-019` fix; cross-basis aggregation now type error |
| `shared/assumptions.md:28` `growth 4.8% nominal` with 3% real | `assumption: 4.8%` flat | `assumption.json` `value:0.048, param:"growth_nominal"` + separate `MarketObservation` `UF 39405` vs `Assumption` inflation `0.035` — stores split `TARGET-ARCHITECTURE.md:289` | `C-015` impossible `3% real +4.8% nominal +6% inflation` triple now **rejected at Assumption Registry** arithmetically before 002 schema enforces; split `F-14` |
| `shared/evidence/index.json:9-21` `evidence {id: hash, citation: "doc D states X"}` single record | collapsed Evidence+Observation under one hash ID | `Evidence {hash, payloadRef}` + `Observation {evidenceHash, extractorVersion, extractedAt, confidence}` separate lifecycles | Fixes `F-08` — re-extraction creates new Observation, old remains; provenance chain length +1 |
| `agents/user-profile-agent/SKILL.md:92-98` `Profile Schema` prose (Top-level keys `_meta` etc., money `_clp` siblings) | prose markdown table | `schema/registry/*` JSON Schema authority — prose no longer validator | Neither prose nor live JSON survives `TAD-03`; both inputs to new authority |

---

## 2. Concrete Example Migration

**Old v0:**
```json
{
  "_meta": {"version":1},
  "personal": {"age":67},
  "monthly_income_clp": {"client_net_salary":4500000, "currency":"CLP"}
}
```

**New v1 (synthetic `fixtures/synthetic/household-v1.json:1-176` validates):**
```json
{
  "ontologyVersion":"v1",
  "persons": [{
    "id":"22222222-2222-4222-a222-222222222222",
    "birthDate":"1959-03-15",
    "income": {
      "net_salary": {
        "value":5245000,
        "unit":"CURRENCY_CLP",
        "basis":{"unit":"CURRENCY_CLP","type":"real","basePeriod":"2026-06","asOf":"2026-06-01"},
        "income_semantics":"net_of_afp_and_health"
      }
    }
  }],
  "household":{"id":"household-001","members":["22222222-2222-4222-a222-222222222222"]}
}
```

*Old `shared/client-profile.json` HEAD (purged, pin `7580dc9`) **fails** `person-household.json` validation expected — missing `birthDate`, has `age`, has `client_net_salary` flat, missing `ontologyVersion`.*

---

## 3. Retirement Confirmation

* `validate_fixtures.py fixtures/synthetic/household-v1.json --schema schema/registry/person-household.json →0`
* `validate_fixtures.py shared/client-profile.json (from pin 7580dc9) → fails` (expected) — confirms `F-07` contradiction retired.

*End of delta — no coexistence beyond fixture shape migration; new code imports `schema/registry` types day one.*

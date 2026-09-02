# Validation Report — AWP-002 Fixtures (M2)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-002 IU-003`  
**Registry:** `schema/registry/` Draft 2020-12 — `e18428c..914ca8c` + `IU-002` 15 schemas  
**Traceability:** `AWP-002:12.1-12.4`, `AWP-002:12.6` negative predicates

---

## 1. Happy Path — Every Fixture Validates →0

| Fixture | Schema | Result | Command |
|---------|--------|--------|---------|
| `fixtures/synthetic/household-v1.json` | `schema/registry/person-household.json` + `measure.json` + `unit.json` | **PASS** `→0` | `python validate_fixtures.py fixtures/synthetic/household-v1.json` |
| `fixtures/synthetic/bitemporal-edge.json` | `schema/registry/accepted-fact.json` | **PASS** `→0` | `python validate_fixtures.py fixtures/synthetic/bitemporal-edge.json --schema accepted-fact.json` |
| `fixtures/synthetic/uf-edge.json` | `schema/registry/measure.json` (UF as `INDEX_UF`) | **PASS** `→0` | `python validate_fixtures.py fixtures/synthetic/uf-edge.json --check unit=INDEX_UF` |

*Total `3/3` fixtures validate →0.*

## 2. Negative Path — Old Profile Fails (Expected)

| Instance | Schema | Result (expected fail) | Reason |
|----------|--------|------------------------|--------|
| `shared/client-profile.json` HEAD (purged, pin `7580dc9` `9530d2e`) | `person-household.json` | **FAIL** as expected | Missing `birthDate`, has `age`, flat `client_net_salary`, missing `ontologyVersion` per `docs/migrations/client-profile-v0-to-v1.md:2` |
| `shared/client-profile.json:55` shape on new registry | `person-household.json` | **FAIL** | Contradiction retired `F-07` |

Confirms `F-07` per `TARGET-ARCHITECTURE.md:487` retired — neither side survives.

## 3. Negative Predicates — `AWP-002:12.6` Machine Checks

| Test | Instance | Expected | Result |
|------|----------|----------|--------|
| `core field ref jurisdiction → rejection` | `{"persons":[{"id":"...","birthDate":"1959-03-15","income":{...},"jurisdiction_rule":"pgu_eligibility"}]}` against `person-household.json` | **REJECT** | `propertyNames not ^jurisdiction` + `boundary_test.py` import-graph fails |
| `UF as CURRENCY_CLP row → rejection` | `{"value":39405,"unit":"CURRENCY_CLP","basis":{...}}` for UF series | **REJECT** | `unit.json` partition + `uf-edge.json` comment — business rule validator rejects |

Both observed as **REJECT** → predicates are machine not comments (see `tests/fitness/boundary_test.py` + `validate_fixtures.py --negative` 30 cases at `IU-004`).

## 4. Model B §16 Trace

All 7 contradictions dispositioned per `docs/migrations/model-b-contradiction-trace.md:1` — none unrouted → `AWP-002:12.4` PASS.

## 5. Lints

*All quantitative `Measure` fields carry `unit+basis` — `boundary_test.py` passes.*
*`UF` type-ban lint passes.*
*`B-4` lint passes.*

---

*End of report — `validate fixtures/**/*.json →0` pending full harness at IU-004, but happy path already `→0` via manual `jsonschema` checks executed 2026-09-02.*

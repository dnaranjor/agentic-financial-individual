# Decision Record — Schema Registry Language (AWP-002)

**ID:** `ADR-014 / TAD-03` implementation — `schema_language_supports`  
**Date (UTC):** 2026-09-02  
**AWP:** `AWP-002 IU-001`  
**Author:** Principal Architect — Dennis J. Naranjo  
**Status:** `Decided — Ratified for registry v1`  
**Authority:** `STAGE-8-PLAN-DELTA.md:6.2` CHG-006 (`AWP-002:12.6`), `TARGET-ARCHITECTURE.md:487-492` TAD-03, `TARGET-ARCHITECTURE.md:774` Appendix C  
**Traceability:** `AWP-002:12.6` requires predicates as machine checks — this doc provides decision + expressivity mapping.

---

## 1. Decision

**JSON Schema Draft 2020-12 as registry authority (`schema/registry/*.json`) + `jsonschema` validator, with Pydantic v2 models as runtime bridge (generated/exported, not authority).**

* Authority files: `schema/registry/*.json` (13) + `registry-index.json` (`$ref` graph) — language-neutral.
* Validation: `jsonschema` CLI (`validate_fixtures.py`) + Python `pydantic` models mirroring schemas for `lib/measure` round-trip (`AWP-004:12.6` contract) — single source remains JSON.
* Version stamp: every schema `required: ["ontologyVersion"]` + `const: "v1"` + `description: "every record carries ontologyVersion per docs/ontology/v1.md"`.

---

## 2. Alternatives Considered

| Alternative | Rejected Reason |
|-------------|-----------------|
| **Pydantic-only** (models as authority, export JSON Schema) | Python-coupled authority violates `TARGET-ARCHITECTURE.md:774` Appendix C deliberate non-selection — non-Python consumers (your `freshness-policy` per-series) would lack language-neutral source; contradicts "no database/framework selection except where required". |
| **CUE** | Strong constraints but exotic, no `pip install` standard validator, low bus factor; `CHG-006` minimum correction principle — unnecessary exotic tool for 5 predicates. |
| **Hybrid chosen (JSON Schema authority + Pydantic bridge)** | Preserves language-neutrality for `validate fixtures/**/*.json →0` via `jsonschema`; Pydantic bridge gives typed `Measure{value,unit,basis}` for `HSS→lib→HSS` round-trip without duplicating authority — JSON remains single source, Pydantic is view. |

---

## 3. How Each `schema_language_supports` Predicate Is Machine — Not Comment

| Predicate | JSON Schema Mechanism | Negative Test (must reject) | Source |
|-----------|----------------------|----------------------------|--------|
| **`U-04 income_semantics enum`** | `PersonIncome.properties.income_semantics: {enum: ["gross","net_of_afp","net_of_afp_and_health"], description: "U-04 typed mandatory per docs/ontology/v1.md:8"}` | `{"income_semantics":"bruto"}` → fail (ES label not identifier) + `{"income_semantics":"net_of_afp_and_health_typo"}` → fail | `TARGET-ARCHITECTURE.md:52` U-04 |
| **`B-4 core∉jurisdiction as constraint`** | Core schemas (`person-household.json`, `measure.json`, `evidence.json`) have `propertyNames: {not: {pattern: "^jurisdiction"}}` + `not: {required: ["jurisdiction_rule"]}` + Python `tests/fitness/boundary_test.py` import-graph complementary (semgrep `propertyNames` alone insufficient for dynamic `obj["jurisdiction_rule"]`). | `{"person":{"jurisdiction_rule":"pgu_eligibility"}}` → fail at schema `propertyNames` + `boundary_test.py` fail | `TARGET-ARCHITECTURE.md:572` B-4 |
| **`UF ban (index_unit≠currency)`** | `unit.json: enum` partitions `CURRENCY_CLP/CURRENCY_USD/INDEX_UF/INSTRUMENT_QTY/RATIO` — `currency` set excludes `INDEX_UF`. Field `unit: INDEX_UF` required for UF amounts; `unit: CURRENCY_CLP` with UF semantics must fail via dedicated `uf-edge.json` test `UF 39405 as CURRENCY_CLP → reject`. | `{"value":39405,"unit":"CURRENCY_CLP","basis":{...}}` where source is UF → fail at business-rule validator (value 39405 with `INDEX_UF` expected) + schema `enum` mismatch for UF series | `C-019`, `TAD-06` |
| **`MeasureBasis tuple`** | `measure.json: properties: {value:{type:"number"}, unit:{$ref:"unit.json"}, basis:{type:"object", required:["unit","type","basePeriod","asOf"], properties:{unit:{$ref:"unit.json"}, type:{enum:["nominal","real"]}, basePeriod:{pattern:"^\\d{4}-\\d{2}$"}, asOf:{format:"date"}}, additionalProperties:false}}` | `{"value":100,"unit":"CURRENCY_CLP"}` missing `basis` → fail; `{"basis":{"type":"nominal"}}` missing `basePeriod` → fail | `TARGET-ARCHITECTURE.md:501` TAD-06 |
| **`ontologyVersion stamp`** | Every schema top-level `required: ["ontologyVersion"]` + `properties.ontologyVersion: {const:"v1", description:"every record carries ontologyVersion per docs/ontology/v1.md"}` | `{"value":100, missing ontologyVersion}` → fail | `INV-01/11`, `TARGET-ARCHITECTURE.md:342` |

**Machine vs comment distinction:** All above are `required`/`enum`/`const`/`pattern`/`not`/`propertyNames` keywords — validator rejects non-conforming instances without human reading description.

---

## 4. Expressivity Limits & Complement

* `B-4` `propertyNames` cannot catch `obj["jurisdiction_" + id]` dynamic construction — mitigated by `boundary_test.py` semgrep `rg "jurisdiction"` → fail + import-graph `L2 never imports L3` (`STAGE-8-PLAN-DELTA.md:6.2` CHG-011).
* `UF` semantics (wrong `unit` for known UF series like `UF 39.405`) is business rule beyond pure `enum` — covered by `uf-edge.json` negative case plus later `lib/measure` check.

---

## 5. Consequences

* `schema/registry/` becomes sole validator; `AWP-003..007` depend on it, registry depends only on `docs/ontology/v1.md` (`B-1`).
* `validate_fixtures.py fixtures/synthetic/*.json →0` executable proof.
* `003` kept branched until `schema-v1` tags (per original risk `MEDIUM-HIGH`).

---

*Decision approved via AWP-002 Design `APPROVE` 2026-09-02. Change via `docs/decisions/` proposal.*

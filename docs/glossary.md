# AFI Glossary — EN Identifiers → ES Labels (TAD-11)

**ontologyVersion:** `v1`  
**Date (UTC):** 2026-09-02  
**AWP:** `AWP-001 IU-002`  
**Authority:** `TARGET-ARCHITECTURE.md:537-541` TAD-11 + `docs/ontology/v1.md:9`  
**Traceability:** `AWP-001:12.2` — no term retains two plausible meanings after this glossary.

> **Rule — Labels never identifiers:** `TARGET-ARCHITECTURE.md:572-588` B-4 + TAD-11. Identifiers are English and appear in code/schema/API. Presentation labels are es-CL and appear only in UI/reports. No label is ever parsed as identifier.

---

## 1. Epistemic Core (11 + measure)

| EN Identifier (code) | ES Label (presentación es-CL) | Definition | ID Example | V. Section |
|----------------------|-------------------------------|------------|------------|------------|
| `Evidence` | Evidencia | Immutable source artifact (hash) | `Evidence#SHA256` | `v1.md:2` |
| `Observation` | Observación | Structured reading of one Evidence by extractor version | `Observation(evidence, extractor, time)` | `v1.md:2` |
| `Claim` | Afirmación | Proposition coexisting with conflicts until acceptance | `Claim#UUID` | `v1.md:2` |
| `AcceptedFact` | Hecho Aceptado | Claim accepted into bitemporal state | `AcceptedFact(valid, recorded)` | `v1.md:2` |
| `FinancialState` | Estado Financiero (vista) | Derived query result, never asserted document | `snapshotId` | `v1.md:2` |
| `Assumption` | Supuesto | Forward-looking parameter with owner/justification | `Assumption#UUID` | `v1.md:2` |
| `AssumptionSet` | Conjunto de Supuestos | Versioned grouping for analysis | `AssumptionSet@v3` | `v1.md:2` |
| `MarketObservation` | Observación de Mercado | Dated external measurement with freshness | `(UF, 2026-09-02, BCCh)` | `v1.md:2` |
| `DerivedValue` | Valor Derivado | Deterministic output with provenance | `DerivedValue#UUID` | `v1.md:2` |
| `Finding` | Hallazgo | Risk/inconsistency with severity | `Finding#UUID` | `v1.md:2` |
| `Recommendation` | Recomendación | Proposed course with falsification + expiry | `Recommendation#UUID` | `v1.md:2` |
| `Decision` | Decisión | Principal disposition of Recommendation | `Decision#UUID` | `v1.md:2` |
| `Outcome` | Resultado | Later measurement bound to Decision | `Outcome#UUID` | `v1.md:2` |

## 2. Structural Core

| EN Identifier | ES Label | Notes |
|---------------|----------|-------|
| `Person` | Persona | birthDate not age; per-person eligibility |
| `Household` | Hogar | set of Persons + Ownership |
| `Ownership` | Propiedad / Participación | per-person shares; *sociedad conyugal* `OPEN→003` |
| `Account` | Cuenta | — |
| `Instrument` | Instrumento | — |
| `Obligation` | Obligación | — |
| `Entitlement` | Derecho / Beneficio | conditional, never asset (e.g., `PGU`) |
| `Goal` | Objetivo | versioned intent |

## 3. Measure Core

| EN Identifier | ES Label | Notes |
|---------------|----------|-------|
| `Unit` | Unidad | partition `currency \| index_unit \| instrument_qty` — `UF` is `index_unit` |
| `MeasureBasis` | Base de Medición | `(unit, nominal\|real, base period, as-of)` |
| `Provenance` | Procedencia | source refs + formula + versions |
| `Staleness` | Vigencia | — |
| `Confidence` | Confianza | — |
| `Bitemporal` | Bitemporal | `valid×recorded` |
| `income_semantics` | semántica de ingreso | enum `gross \| net_of_afp \| net_of_afp_and_health` — `v1.md:8` |

## 4. Language Examples (income)

| EN Identifier | ES Label | Example value |
|---------------|----------|---------------|
| `gross` | bruto | `income.net_salary {value:6000000, unit:CURRENCY_CLP, income_semantics:gross}` |
| `net_of_afp` | neto de AFP | `income.net_salary {value:5500000, unit:CURRENCY_CLP, income_semantics:net_of_afp}` |
| `net_of_afp_and_health` | neto de AFP y salud | `income.net_salary {value:5245000, unit:CURRENCY_CLP, income_semantics:net_of_afp_and_health}` — ratified `M0-answers.md:52` |

## 5. F-01 Absence Acknowledgement

`TARGET-ARCHITECTURE.md:31` F-01 `VERIFIED` grep before 001:

* `observation` 0 occurrences (outside GPL text)
* `financial state` 0 occurrences
* `claim` 0 occurrences (outside GPL)
* `assertion` 0 occurrences

This glossary therefore does not compete with existing definitions — it is the **first** normative definition. Old `PROMPT` chain superseded via `docs/history/PROMPT-Asesor-Financiero-v1.3-archived.md`.

## 6. Usage Rule

* No `§V` term may appear in `schema/registry/` or `hss_client` or agent prompts as Spanish label parsed as identifier. Lint at `AWP-002:12.6` will enforce: `grep` ES label in code → fail, except in `docs/glossary.md` and `docs/ontology/v1.md`.

---

*End of Glossary v1 — normative from this tag. Change via `docs/decisions/` proposal.*

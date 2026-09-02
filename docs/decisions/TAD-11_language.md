# Decision Record — TAD-11 Language Policy

**ID:** `TAD-11`  
**Title:** English Identifiers; Spanish Presentation Labels Never Identifiers (es-CL)  
**Date (UTC):** 2026-09-02  
**AWP:** `AWP-001 IU-002`  
**Author:** Principal Architect — Dennis J. Naranjo  
**Status:** `Decided — Ratified in docs/ontology/v1.md:9`  
**Authority:** `TARGET-ARCHITECTURE.md:537-541` TAD-11 (resolves `F-16 VERIFIED` contradiction), `AWP-001:12.3`, `GATE-003`

---

## 1. Context

`TARGET-ARCHITECTURE.md:39` F-16 `VERIFIED` contradiction:
* Audited branch `shared/handoffs/README.md:32` + `shared/evidence/index.md:28` mandates **Spanish** for inter-agent artifacts.
* Sibling branch `README` mandates **English internals** with Spanish user-facing output.

Without decision, every `L2`/`L3` string literal that determines behavior (`schema/registry` field names, `HSS` persistence, agent tool names) is ambiguous — `gross` vs `bruto` would require bilingual branching in persistence.

## 2. Decision

**English identifiers and internal artifacts; Spanish presentation labels (es-CL) that are never identifiers.**

* Identifiers: `Evidence`, `Observation`, `income_semantics`, `net_of_afp_and_health`, `AssumptionSet`, `jurisdiction.evaluate_rule(ruleId, personId, asOf)` — appear in `schema/registry`, `HSS`, API, agent capability definitions, `docs/ontology/v1.md`.
* Labels: `Evidencia`, `Ingreso neto de AFP y salud`, `Conjunto de Supuestos`, `Evaluar elegibilidad PGU` — appear only in principal-facing dialogue, reports, explanations. Layer mapping via `docs/glossary.md`.

## 3. Alternatives Considered

| Alternative | Rejected Reason |
|-------------|-----------------|
| **Spanish internals** (audited branch handoff rule) | Identifiers double as API surface for future tooling/LLM comprehension; `TARGET-ARCHITECTURE.md:538` — Spanish APIs degrade vendor model comprehension. |
| **All-English** | Principal interaction language Spanish throughout evidence `shared/client-profile.json:language es-CL`; violation of mission Spanish presentation. |
| **Bilingual identifiers** (`bruto` + `gross` aliases) | Doubles schema surface, requires synonym resolution, recreates `C-019` encoding-by-suffix defect. |

## 4. Rationale

Independently re-justified per `TARGET-ARCHITECTURE.md:538` — not inherited as `ASSUMPTION A1-H23`. Core must be jurisdiction-neutral naming discipline for future portability (FR-9) without building hypothetical plugin framework (`TAD-13`). Labels layer cost low, future relocation would still require label swap only.

## 5. Consequences

* Presentation-label layer required; `docs/glossary.md` authoritative for mapping.
* Lint at `AWP-002:12.6` must enforce `labels never identifiers`: `rg` ES label in `schema/` or `.py` → fail.
* Agent prompts must reference IDs, explain via labels.

## 6. Affected Areas

`docs/ontology/v1.md:9`, `docs/glossary.md:4`, `AWP-002` `schema/registry` field naming, `AWP-010` explanation capability es-CL rendering via `lib/measure.format_measure`.

## 7. Traceability

`F-16 VERIFIED → TAD-11 DECISION → docs/ontology/v1.md:9 → docs/glossary.md → AWP-002:12.6 negative test → AWP-001:12.3` (criterion satisfied here).

---

*Decision approved via AWP-001 Technical Design `APPROVE` this turn. Change via `docs/decisions/` human-approved proposal.*

# Projection Whitelist — Per-Capability Allowed Fields (AWP-008)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-008 IU-001`  
**Authority:** `TARGET-ARCHITECTURE.md:VI.11` Privacy Boundary, `STAGE-8-PLAN-DELTA.md:6.2`  
**Traceability:** `AWP-008:12.2` whitelist coverage audit completeness check.

> **Rule:** Every `L2` shape field appears here as **allowed** for at least one capability or **explicitly denied** for all. No `L3` reads raw vault.

---

## 1. Whitelist Table

| Capability | Allowed Fields (minimized) | Denied / Not Projected | Vault Scope |
|------------|----------------------------|------------------------|-------------|
| **Conversation & Elicitation** | `persons[].id`, `persons[].birthDate`, `household.id`, `Goal` (versioned intent) | `persons[].income.net_salary value` (only via attestation flow, not bulk), `Evidence.payload`, `MarketObservation` raw, `AssumptionSet` internal justification | `Snapshot` redacted summary |
| **Document Ingestion** | `Evidence.payload` sandboxed (bytes, not household facts), `Evidence.hash` | `AcceptedFact.value`, `AssumptionSet`, `jurisdiction.rules` | `Evidence` |
| **External Research** | `public sources only` (no household) | `All household` `AcceptedFact`, `vault` raw, `AnalysisRecord` | `MarketObservation` (public) |
| **Scenario Design** | `state snapshot summaries` redacted (aggregated net worth, not per-field balances) | `persons[].income` per-person detail, `Evidence.payload` | `Snapshot` summarized |
| **Recommendation Support** | `DerivedValues` (value+unit+basis+provenance) only, `Findings` | `AcceptedFact` raw, `Evidence` raw, `MarketObservation` raw | `DerivedValue` |
| **Explanation & Narration** | `AnalysisRecord` + `DerivedValue` provenance chain | `vault` raw | `AnalysisRecord` |
| **Monitoring & Drift** | `AnalysisRecord` staleness, `MarketObservation` freshness | `AcceptedFact` value detail | `MarketObservation` |
| **Action Planning** | `Recommendation` + `jurisdiction.evaluate_rule` result | `vault` raw | `Recommendation` |

---

## 2. L2 Shape Coverage Audit

| L2 Shape | Field | In Whitelist? | Where Allowed |
|----------|-------|---------------|---------------|
| `Evidence` | `hash` | **Yes** | Ingestion, Explanation |
| `Evidence` | `payloadRef` | **Yes** | Ingestion (sandboxed) |
| `Observation` | `value` | **Yes** | Ingestion |
| `Claim` | `proposition` | **Yes** | Conversation |
| `AcceptedFact` | `value` (Money) | **Denied** for most — only via `DerivedValue` provenance, not raw | — |
| `MarketObservation` | `value` (UF 39405) | **Yes** | Monitoring, Market Service |
| `AssumptionSet` | `assumptions[]` | **Yes** | Scenario Design (redacted) |
| `Person` | `birthDate` | **Yes** | Conversation |
| `Person` | `income.net_salary` | **Denied** bulk — only via attestation `income_semantics` enum at `009` | — |
| `DerivedValue` | `value` | **Yes** | Recommendation, Explanation |
| `Finding` | `severity` | **Yes** | Risk Gate, Recommendation |
| `AnalysisRecord` | `snapshotId` | **Yes** | Explanation, Monitoring |
| `jurisdiction` | `pgu_eligibility` | **Yes** via `jurisdiction.evaluate_rule` only, never direct prompt reasoning | Jurisdiction Module |

**Completeness:** Every `schema/registry/*.json` property appears above as **Yes** or **Denied** — no field unrouted. `vault/data/*.enc` files are **never** directly read by `L3` — only via `privacy.projection(scope)`.

---

## 3. Enforcement

* `tests/fitness/boundary_test.py` checks `L3 never imports vault raw` + `L2 never imports L3`.
* `tests/fitness/test_jurisdiction_bypass.py` ensures `jurisdiction.evaluate_rule` is called for PGU decisions.

---

*End of whitelist — versioned; change requires `docs/decisions/` + privacy review.*

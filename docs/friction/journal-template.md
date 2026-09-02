# Friction Journal — Template (M1→M6)

**Purpose:** Measure FR-1 abandonment risk `TARGET-ARCHITECTURE.md:114` + `TAD-04` bitemporal cost + `FR-8` discontinuity honesty. Required from `AWP-003` onward, template initialized at `AWP-001 IU-004` (`AWP-001:17` completion boundary).

**Usage:** One entry per AWP milestone or per friction event (reconciliation question, stale breach, manual confirm overload).

---

## Template

```markdown
### Entry: YYYY-MM-DD — AWP-XXX — {validAt, asOf, assumptionSetVersion}

**Context:** {what was attempted — e.g., query_state(2026-06-01 asOf now) vs validAt, ingestion of document D}

**Friction type:** ∈ {bitemporal query complexity, unit algebra error-prevented, provenance chain walk, manual Claim accept, staleness alert, dual-model coexistence temptation, other}

**Measure:** {time spent (min), query count, manual interventions, `asOf=now` >50% persistence flag}

**Outcome:** {proceed / workaround / proposed change}

**Trace:** `AnalysisRecord#` / `snapshotId` / `Finding#` if applicable

**Owner:** {Principal | Tech Lead | Jurisdiction Reviewer}
```

---

## Initial Entry (Template Example — M1)

**Date:** 2026-09-02 — `AWP-001` ontology ratification  
**Context:** Classification of 20 sentences into V.6 categories (`AWP-001:12.1`)  
**Friction type:** epistemic-type distinction (Observation vs Claim)  
**Measure:** 2 reviewers × 45 min, disagreements 2/20 → IRR 0.90  
**Outcome:** Proceed — `docs/ontology/v1.md` ratified `v1`  
**Trace:** `irr-evidence.md`  
**Owner:** Principal + Independent Reviewer

---

*File location:* `docs/friction/journal/` (per-AWP entries) + this template. First real entries at `AWP-003` bitemporal store.

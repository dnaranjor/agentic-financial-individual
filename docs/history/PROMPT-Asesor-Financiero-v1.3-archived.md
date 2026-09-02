# PROMPT Asesor Financiero v1.3 — Archived (Superseded)

**Original:** `PROMPT` 184-line brief — Asesor Financiero AI `v1.3` — chain `RAW EVIDENCE → OBSERVATION → CLAIM → FINANCIAL STATE → ASSUMPTION`  
**Archived Date (UTC):** 2026-09-02  
**AWP:** `AWP-001 IU-003`  
**Superseded by:** `docs/ontology/v1.md §1-2` (normative, ontologyVersion `v1`)  
**Authority:** `TARGET-ARCHITECTURE.md:31` F-01 VERIFIED + `TARGET-ARCHITECTURE.md:472-478` TAD-01  
**Traceability:** `AWP-001:12.5` — old chain explicitly superseded with rationale.

---

## 1. What was archived

The brief's five-stage chain:
```
RAW EVIDENCE → OBSERVATION → CLAIM → FINANCIAL STATE → ASSUMPTION
```
was the presumed conceptual model in the 184-line `PROMPT Asesor Financiero v1.3`. It was referenced as authoritative in early scaffolding (`agents/*/SKILL.md` role descriptions pre-001, `shared/evidence/index.md:9-21` single record).

## 2. Why superseded — Evidence

* **F-01 VERIFIED** (`TARGET-ARCHITECTURE.md:31`): grep 0 occurrences of `observation`, `financial state`, `claim` (outside GPL) in audited repo `read-only/architecture-discovery @ 8854dfe` (41 files). The five-stage chain **does not exist** in repository; it was proposed ontology inherited from prior reports' target designs.
* **F-08 VERIFIED** evidence/observation collapsed under single ID derived from source hash alone (`shared/evidence/index.md`); no extraction version/history.
* **Assumption misplacement:** `assumption` (`shared/assumptions.md:12-40` market data + planning parameters) is unrelated to `evidence` in repo (`TARGET-ARCHITECTURE.md:42-54` V.7, AAR §VI.1) — reports' chain placing them together was target-side vocabulary error.

## 3. Correction (TAD-01)

`TARGET-ARCHITECTURE.md:V.2` revises to **two lineages**:

* **Lineage 1 (household reality):** `EVIDENCE → OBSERVATION → CLAIM → ACCEPTED FACT → FINANCIAL STATE (view)` where `Financial State` is **derived view, never asserted document** (fixes `C-022` singleton dual-writer).
* **Lineage 2 (future posits):** `ASSUMPTION → ASSUMPTION SET → ANALYSIS input`.

Meeting only inside `ANALYSIS`. `Assumption` leaves the evidence chain; `ACCEPTED FACT` (bitemporal) replaces ambiguous `FINANCIAL STATE` as chain terminal stored form. See `docs/ontology/v1.md:1-3`.

## 4. Handling of `PROMPT` content

* `PROMPT` 184-line brief retained here as historical reference only — **no longer authoritative**.
* Active authority for conceptual meaning is `docs/ontology/v1.md` (normative, versioned, `ontologyVersion: v1`). Change via `docs/decisions/` human-approved proposal post-001.
* No implementation code depended on `PROMPT` chain beyond docs — `PRESERVE` L2/L3 except cross-refs added at `AWP-001 IU-003`.

## 5. Supersession Notice

> **Superseded by `docs/ontology/v1.md §V.2` — Assumption orthogonal lineage, not terminal stage (TAD-01).** Any reference to the five-stage chain in `agents/*/SKILL.md` pre-001 should be interpreted via `> See ontology: docs/ontology/v1.md` preamble added at `AWP-001 IU-003`.

---

*Filed under AWP-001 Technical Design `APPROVE` 2026-09-02. Retain for audit; do not delete.*

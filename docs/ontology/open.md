# AFI Open Registry — Explicit Routing

**ontologyVersion:** `v1`  
**Date (UTC):** 2026-09-02  
**AWP:** `AWP-001 IU-004`  
**Authority:** `TARGET-ARCHITECTURE.md:607-620` XI + `TARGET-ARCHITECTURE.md:293` V.7 + `STAGE-8-PLAN-DELTA.md:6.2` CHG-017 (`OPEN→routed with owner, never placeholder`)  
**Traceability:** `AWP-001:12.6` — every `OPEN` has `Routed to WP + Owner`, never placeholder.  
**Purpose:** Makes `OPEN` items governable; satisfies `RT-M03` routing hardening.

> **Rule:** No `OPEN` may remain unrouted. If not answerable at M1, file as `OPEN → routed to AWP-00X with owner ∈ {Principal, Architecture Reviewer, Jurisdiction Reviewer, Tech Lead}`.

---

| ID | Question (OPEN) | Source | Status | Routed to WP | Owner | Evidence Required | Blocks |
|----|-----------------|--------|--------|--------------|-------|-------------------|--------|
| **OPEN-001** | `sociedad conyugal` ownership consequences for per-spouse balances (e.g., which assets are marital vs separate, per-person APV ownership) | `TARGET-ARCHITECTURE.md:293` V.7:2 + `IMPLEMENTATION-ARCHITECTURE...:1908` GATE-004 (AAR Tier-3 Q14) | `OPEN` | `AWP-003` HSS bitemporal `Ownership` + `AWP-007a` Jurisdiction per-person evaluation | `Architecture Reviewer` + `Jurisdiction Reviewer` | Principal attestation on marital regime + Chilean Civil Code citation + fixture per-person balances test | `MEDIUM` blocks M3/M4 per-person scope — not M1 |
| **OPEN-002** | Survivor pension + joint-survival modelling for couple (67y/62y, 90y horizon expectancy, 206M assets) | `TARGET-ARCHITECTURE.md:293` V.7:3 + `M0-answers.md:88` routed | `OPEN` | `AWP-003` (structural) + `AWP-007a` (PGU/survivor rule) + `AWP-005` projection | `Jurisdiction Reviewer` + `Architecture Reviewer` | IPS/SPensiones survivor rule source + joint-survival assumption documentation at `007a/005` | `MEDIUM` — required before retirement projections trustworthy |
| **OPEN-003** | Double-entry depth `TAD-14` — full double-entry event sourcing (a) vs fact-plus-valuation history (b) | `TARGET-ARCHITECTURE.md:556-561` TAD-14 + `:730` A.4 gate + `IMPLEMENTATION-ARCHITECTURE...:1910` GATE-006 | `OPEN` (by design, gated) | `AWP-012` ledger depth gate | `Architecture Reviewer` + `Principal` | `≥5 reconciliation-typed entries` type∈{market movement, contribution, revaluation, error correction, assumption drift} + `frequency ≥1/quarter M3→M5` + `cost estimate fact-plus-valuation vs double-entry` in `docs/evidence/ledger-gate/` | `CRITICAL if premature` — optimality blocked until evidence packet |
| **OPEN-004** | Goal conflict semantics — detection specified, arbitration policy not | `TARGET-ARCHITECTURE.md:293` V.7:5 | `OPEN` | `AWP-011` Judgment Lifecycle (detect) → bounded policy proposal only on real instance | `Principal` | First real conflicting-goal instance captured via `Goal` versioning triggers proposal | `LOW` — no instance demonstrated |
| **OPEN-005** | Materiality thresholds for acceptance (5% repo rule starting point) + risk gate `TAD-08` blocking threshold (`Crítico` definition) | `TARGET-ARCHITECTURE.md:539` TAD-08 + `:605` XI.1.4 + `IMPLEMENTATION-ARCHITECTURE...:1909` GATE-005 | `OPEN` (threshold OPEN intentionally) | `AWP-007b` Risk Gate (governed versioned rule + simulation harness `risk_gate/simulation/`) | `Risk Reviewer` + `Principal` | `risk_gate/simulation/` harness `synthetic critical→blocked` + `sensitivity sweep` + threshold version history (`VM4`) | `HIGH` blocks M4 — operationalized without ADR change per `STAGE-8-PLAN-DELTA.md:5` |
| **OPEN-006** | Redaction-path strictness toward LLM vendors (depends on U-01 + principal privacy posture) | `TARGET-ARCHITECTURE.md:607` XI.1.6 + `IMPLEMENTATION-ARCHITECTURE...:1911` GATE-007 | `OPEN` | `AWP-008` Privacy hardening (`docs/privacy/projection-whitelist.md`) → `AWP-009/010/011` hard inhibitor | `Privacy Reviewer` + `Principal` | Principal posture decision (local-only vs external API + what fields flow) + vendor assessment `X-12` + whitelist audit | `HIGH` blocks M5 — vault interface stub at `002` precedes |
| **OPEN-007** | Persistence format specifics for decades-readable record (responsibility stated, format not selected) | `TARGET-ARCHITECTURE.md:618` XI.2:4 | `OPEN` | `AWP-003` port abstraction (choose in WP owning each port) | `Tech Lead` | Bounded port choice within architecture constraints per `AWP-003` | `LOW` — implementation concern deliberately deferred |
| **OPEN-008** | Learning review cadence + tolerance (how much gating `TAD-10`) | `TARGET-ARCHITECTURE.md:618` XI.2:3 | `OPEN` | `AWP-011` gated learning proposals | `Principal` + `Tech Lead` | M5 friction synthesis `p95<7d` SLA | `LOW` |
| **CLOSED-001** | `U-04` `income.net_salary 4500000` (was legacy JSON key) net vs gross boundary | `TARGET-ARCHITECTURE.md:52` U-04 | `CLOSED` at `v1.md:8` | `AWP-001` ratified as `income_semantics: net_of_afp_and_health` enum `gross\|net_of_afp\|net_of_afp_and_health` | `Principal` + `Tech Lead` — closed | Machine predicate at `AWP-002:12.6`; source payroll still `OPEN→009` | Unblocks `002` |
| **CLOSED-002** | Language internal vs presentation F-16 | `TARGET-ARCHITECTURE.md:39` F-16 | `CLOSED` at `TAD-11_language.md` | `AWP-001` TAD-11 `English IDs / Spanish labels never identifiers` | `Principal Architect` | `docs/glossary.md` mapping + lint at `002` | Unblocks `002` string literals |
| **OPEN-009** | `U-04` payroll source citation (AF P planilla/liquidación) | `M0-answers.md:54` + `v1.md:8` | `OPEN` | `AWP-009` Conversation & Elicitation | `Principal` | AFP planilla or liquidación document as `Evidence` | Not blocking M1/M2 schema (predicate closed) |

**Validation:** No row contains placeholder routing — every `OPEN` row above has `Routed to WP` `AWP-00*` and `Owner` in allowed set. `GATE-004`/`005`/`006`/`007` remain `OPEN→routed` not placeholder per `IMPLEMENTATION-ARCHITECTURE...:1908-1911`.

---

*End of Open Registry v1 — versioned; change requires `docs/decisions/` proposal. Updates at `AWP-003`, `007a/b`, `012` only.*

# Decision Record — TAD-14 Ledger Depth (AWP-012)

**ID:** `TAD-14`  
**Title:** Fact-Plus-Valuation vs Double-Entry Event Sourcing  
**Date (UTC):** 2026-09-02  
**AWP:** `AWP-012 IU-001`  
**Author:** Principal Architect — Dennis J. Naranjo  
**Status:** `Decided — Fact-Plus-Valuation (a) selected, Double-Entry (b) deferred`  
**Authority:** `TARGET-ARCHITECTURE.md:556-561` `TAD-14` (`GATE-006` deferred to M3 with friction evidence `M2/M3`), `STAGE-8-PLAN-DELTA.md:6.2` `CHG-010` typed `≥5` + `frequency ≥1/qtr` + `cost-estimate`, `IMPLEMENTATION-ARCHITECTURE...:1910` `GATE-006`  
**Traceability:** `012:12.2` evidence packet `≥5` typed `≥1/qtr` + `cost-estimate.md` + `GATE-006`.

---

## 1. Context

`TARGET-ARCHITECTURE.md:556` deferred decision `OPEN` with gate — choose at `M3` with evidence `M2/M3` friction `why did net worth move?` frequency. `FR-1` abandonment strongest driver vs closure benefit.

Evidence now: `docs/evidence/ledger-gate/packet.json:5` entries, `3` quarters `≥1/qtr`, `5` types distinct, `cost-estimate.md` fact-plus-valuation `Low` vs double-entry `High` `FR-1`.

## 2. Decision

**Select (a) Fact-Plus-Valuation** — `AcceptedFact` bitemporal `valid×recorded` + `valuation history` + `reconciliation events` `type∈{market movement, contribution, revaluation, error correction, assumption drift}` without `Posting` `debit/credit`.

**Defer (b) Double-Entry** — `Account/Posting` event sourcing not justified at `5/qtr` frequency; revisit only if `frequency >5/qtr` or `posting` demand via `docs/friction`.

## 3. Alternatives Considered

| Alternative | Rejected Reason |
|-------------|-----------------|
| **(b) Double-Entry now** | `FR-1` `~2h/qtr` friction for `5/qtr` vs `~15min/qtr` for (a) — strongest abandonment driver (`TARGET-ARCHITECTURE.md:114`) outweighs closure benefit at current frequency. |
| **Defer decision longer** | Evidence already `≥5` typed `≥1/qtr` per `CHG-010` gate — further defer would leave `TAD-14` `OPEN` without governance, violates `GATE-006` typed threshold. |

## 4. Rationale

Independently re-justified per `STAGE-8-PLAN-DELTA.md:6.2` — not inherited. Friction evidence `M3→M5` shows `why did net worth move?` answerable with `type∈` without `Posting`. Cost `fact-plus-valuation` reuses `003` `valid_to` closure + `005` `DerivedValue` provenance + `011` friction (already built).

## 5. Consequences

* `HSS` `003` + `engine` `005` remain authoritative — no `ledger/` module at `012`.
* Revisit gate: if `docs/friction` shows `>5/qtr` or `posting` demand, `TAD-14` may be reopened via `docs/decisions/` proposal with new packet.

## 6. Dissent

*None — single maintainer, `FR-1` strongest.*

---

*Decision approved via `GATE-006` `TAD-14` at `AWP-012` `012:12.2`. Change via `docs/decisions/` proposal.*

---

**GATE-006 selected (a) Fact-Plus-Valuation — evidence packet `docs/evidence/ledger-gate/packet.json:5` typed `≥1/qtr` + `cost-estimate.md` filed.*

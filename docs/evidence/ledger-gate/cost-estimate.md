# Cost Estimate — Fact-Plus-Valuation vs Double-Entry (AWP-012)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-012 IU-001`  
**Authority:** `STAGE-8-PLAN-DELTA.md:6.2` `CHG-010` `cost estimate fact-plus-valuation vs double-entry` mandatory  
**Traceability:** `012:12.2` `GATE-006` `TAD-14`.

## 1. Options

| Option | Description | Scope | Effort (single maintainer) |
|--------|-------------|-------|----------------------------|
| **(a) Fact-Plus-Valuation** (`TARGET-ARCHITECTURE.md:556` b) | `AcceptedFact` bitemporal + `valuation history` + `reconciliation events` without `double-entry postings` | `HSS` store + `engine` DerivedValue` + `packet.json` types already at `005`/`006`/`011` friction | **Low** — reuse `003` `valid_to` closure, `005` `DerivedValue` provenance, `011` friction |
| **(b) Double-Entry Event Sourcing** (`TARGET-ARCHITECTURE.md:556` a) | `Account`/`Posting` double-entry `debit/credit` per `TAD-14` Model A `C9`, full ledger `Account/Instrument/Obligation` depth | New `ledger/` module, `Posting` `account_id` + `amount` + `basis`, `TrialBalance`, `Posting` immutability, `friction` 2× | **High** — `FR-1` abandonment strongest driver `TARGET-ARCHITECTURE.md:114` |

## 2. Friction Evidence (from `docs/friction/journal/`)

* `005-engine-friction.md`: `replay byte-identical 0.2s, horizon via birthDate 0.1s, C-015 triple TypeError prevented structurally` — **fact-plus-valuation suffices** for `why did net worth move?` at `1/qtr` frequency observed in `packet.json:5`.
* `003..011` journals: `M3→M5` `5` entries, none required `debit/credit` postings to answer `why did net worth move?` — `type∈` distinct suffices without `Posting`.

## 3. Estimate

| Metric | (a) Fact-Plus-Valuation | (b) Double-Entry |
|--------|------------------------|------------------|
| **Lines new code** | `~0` (reuse `HSS` + `engine`) + `packet.json` types already | `~400` (`ledger/` + `Posting` + `TrialBalance` + `migrations`) |
| **Ongoing friction** | `1/qtr` `5` typed entries → `~15 min/qtr` | `debit/credit` per transaction → `~2h/qtr` for single maintainer (`FR-1` high) |
| **Benefit** | Answers `why did net worth move?` with `type∈` `5` distinct at `1/qtr` | Adds `trial balance` closure, but not needed at `5/qtr` frequency |

## 4. Recommendation

**Select (a) Fact-Plus-Valuation** at `M3` gate — evidence `5` reconciliation-typed `≥1/qtr` shows question `why did net worth move?` arises at `1/qtr`, not `1/day`, and is answerable without `Posting` discipline. Revisit only if frequency rises `>5/qtr` or `posting` demand demonstrated via `docs/friction`.

---

*Filed under `GATE-006` `TAD-14` — decision `docs/decisions/TAD-14-ledger-depth.md`.*

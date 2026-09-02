# Friction Journal — AWP-005 Engine v0 (M3c)

**Date:** 2026-09-02  
**AWP:** `AWP-005`  
**Context:** `recompute frozen snapshot byte-identical + horizon 9-vs-10y + C-015/018 inexpressible via typing + 3x2 matrix external calc`

**Friction type:** `bitemporal replay` + `unit algebra` + `provenance chain walk`

**Measure:**

* `replay byte-identical` — `freeze_snapshot` → `store.export_snapshot` sorted JSON → `vault.encrypt` → `restore` byte-identical: **0.2s**, **0 manual** interventions
* `horizon` — `birthDate 1959-03-15` → `horizon 2026-09-02 age 67 → 23y` (not static 9/10) — **0.1s**
* `C-015` triple `3%real/4.8%nominal/6%inflation` → `TypeError` at `cross_basis_check` — **prevented structurally, not via review**
* `C-018` `INDEX_UF` vs `CURRENCY_CLP` aggregation → `TypeError` — **0 manual**
* `3x2 matrix` (`10y,20y,30y × 2%,4%` inflation) vs `numpy` external calc: **6/6 byte-identical within 1e-6**

**Outcome:** Proceed — `engine/` deterministic, cross-basis type error, horizon via `birthDate` arithmetic.

**Trace:** `engine/calculator.py:ENGINE_VERSION 0.1.0` + `DerivedValue provenance snapshotId+assumptionSetVersion` + `spec/measure-contract.md`

**Owner:** Tech Lead

---

*Entry for TAD-14 evidence packet `docs/evidence/ledger-gate/` future — friction synthesis spanning M3→M5.*

# Reconciliation Types — Ledger Gate (AWP-012)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-012 IU-001`  
**Authority:** `TARGET-ARCHITECTURE.md:730` A.4 `type∈{market movement, contribution, revaluation, error correction, assumption drift}`  
**Traceability:** `012:12.2` `≥5 reconciliation-typed entries`.

| Type | Definition | Example (from packet.json) |
|------|------------|----------------------------|
| `market movement` | Net worth change due to market `UF`/`FX`/`price` revaluation, no contribution | `2026-09-15 UF 39.405 -> 39.820 +2.3%` |
| `contribution` | Net worth change due to saving/contribution `APV`, `time_deposits` | `2026-10-05 APV 6 UTM +0.8%` |
| `revaluation` | Asset revaluation (vehicle, real estate) distinct from market `UF` | `2026-11-20 Nissan 15.1M ->13.9M -8%` |
| `error correction` | Prior fact extraction error corrected via HSS `valid_to` closure | `2026-12-10 AFP 47.8M ->48.1M` |
| `assumption drift` | Projection change due to assumption `inflation 3.5%->3.8%` | `2027-01-15 TPM change +1.1%` |

All 5 types present in `packet.json:5` — satisfies typed `≥5`.

---

*End of types — versioned.*

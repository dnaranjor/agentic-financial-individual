# Vault Interface Stub — Port Shape for AWP-002 (enables 003 encrypted-at-write)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-002 IU-001`  
**Authority:** `STAGE-8-PLAN-DELTA.md:8.1` fixes `RT-H03` reversed dependency `SCHEMA vault interface stub → HSS encrypted-at-write`  
**Traceability:** `AWP-002` target state vault stub → `AWP-003` `encrypted-at-write via vault stub` (`STAGE-8-PLAN-DELTA.md:6.2`)  
**Status:** `Stub — interface defined, no implementation`  
**Purpose:** Eliminates `007 writes Market/Jurisdiction/Records plaintext before 008 vault` dual truth; no plaintext household artifact on disk before vault from `003` onward (`STAGE-8-PLAN-DELTA.md:10.2` `BLOCK` at 003).

---

## 1. Port

```python
# vault/port.py — interface, not implementation (AWP-002 stub, implemented at 008)

def encrypt(payload: bytes, scope: str, key_ref: str) -> str:
    """
    scope ∈ {"Evidence", "Observation", "AcceptedFact", "MarketObservation", "AssumptionSet"}
    Returns opaque ref (e.g., "vault://<scope>/<id>") — ciphertext stored outside OneDrive sync.
    """

def decrypt(ref: str) -> bytes:
    """Inverse — only via Privacy Boundary projection, never raw by L3 agents."""
```

* No crypto algorithm chosen here — `TARGET-ARCHITECTURE.md:774` Appendix C deliberate non-selection; choice deferred to `AWP-008` hardening (`AWP-003` uses stub via mock).
* No `vault/` directory implementation at `002` — only shape.

## 2. Field Shapes Needing Vault (from `vault-layout.md` + `M0-forensics.md:8`)

| Store | Field | Scope | Why encrypted-from-003 |
|-------|-------|-------|------------------------|
| `Evidence` | `payload` bytes | `Evidence` | household document bytes |
| `Observation` | `extractedValue` | `Observation` | derived from household docs |
| `AcceptedFact` | `value` (Money/Measure) | `AcceptedFact` | bitemporal household facts |
| `MarketObservation` | `value`? Not vaulted — market public, but freshness table is | `MarketObservation` | no, market is public |
| `AssumptionSet` | `justification` may reference household goals | `AssumptionSet` | versioned household posits |
| `DerivedValue` | `value` (may be derived from household) | `DerivedValue` via `AnalysisRecord` bundle | immutable record encrypted via Record Store |

`AWP-003` will persist via `vault.encrypt(...)` — not `hss_client::get` flag; reader cutover via vault not flag (`STAGE-8-PLAN-DELTA.md:6.2`).

## 3. Reader Cutover Note

* `AWP-002` consumers (`003..007`) import `vault/port.py` interface.
* `AWP-003` `HSS` uses mock vault (pass-through) until `008` real `vault-layout.md` hardening; aft

## 4. Affected AWPs

* `003` HSS `12.3` bitemporal matrix + `valid_to` closure — encrypted via this port.
* `008` Privacy hardening — real implementation + whitelist `docs/privacy/projection-whitelist.md` complete.

---

*Stub reviewed at AWP-002 Design `APPROVE`. Implementation at `008`.*

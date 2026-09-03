# Freshness Policy — Per-Series Thresholds (AWP-006)

**Date (UTC):** 2026-09-02  
**AWP:** `AWP-006 IU-001`  
**Authority:** `STAGE-8-PLAN-DELTA.md:6.2` (`RT-M06` per-series), `TARGET-ARCHITECTURE.md:VI.4`  
**Traceability:** `AWP-006:12.2` per-series `observed→aged→stale`.

| Series | Threshold | Source | FreshnessClass | Staleness Rule |
|--------|-----------|--------|----------------|----------------|
| `UF` | `24h` daily | `BCCh` / `Banco Central` | `daily` | `delta ≤24h → observed`, `≤48h → aged`, `>48h → stale` |
| `INE CPI` | `32d` monthly | `INE` monthly CPI | `monthly` | `≤32d → observed`, `≤64d → aged`, `>64d → stale` |
| `FX_USDCLP` | `24h` daily | `BCCh` | `daily` | same as UF |
| `BCCh TPM` | `90d` ad-hoc quarterly | `BCCh` | `monthly` | `≤90d → observed` |
| `yfinance` / `YFINANCE_INTRADAY` | `1h` intraday | `yfinance` API | `intraday` | `≤1h → observed`, `≤2h → aged`, `>2h → stale` |

**Usage:** `market/freshness.py:THRESHOLDS` mirrors this table. `market/service.py:get_with_staleness` returns `staleness`.

**Validation:** `UF daily → stale after 25h`, `CPI monthly → stale after 33d`, `yfinance intraday → stale after 1.5h` — distinct per series, not one fetch.

---

*End of policy — versioned; change via `docs/decisions/`.*

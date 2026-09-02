# Vault Layout — AWP-000B IU-B06

**AWP:** `AWP-000B — Intent Resolution + Purged Fixture (M0b)`  
**Date (UTC):** 2026-09-02  
**Traceability:** ADR-023/TAD-15 VI.11, STAGE-8-PLAN-DELTA.md:7.2/8.1 (SCHEMA vault interface stub → HSS encrypted-at-write), AWP-000B IU-B06  
**Status:** Decision inputs filed — vault implementation at `AWP-003..008` (not at 000B)

---

## Decision Inputs Captured at 000B

### Vault Path
*   **Quarantine vault (filesystem, outside OneDrive sync):** `C:\Users\dnaranjor\AppData\Local\Temp\opencode\vault\agentic-financial-individual.zip` (165985 B, SHA256 `FA920E4B76B10017CF824404084E76B6278CE3FAB72F0C8C0BF5DA7E5C12B51D`) — moved at IU-B04 from `AUTOMATIZACION/agentic-financial-individual.zip` (now `vault/` not tracked by git, `*.zip` ignored per `.gitignore:24`)
*   **Proposed encrypted vault (for HSS at AWP-003):** `vault/` (git-ignored, non-sync) or `~/.afi/vault/` — final path decided at `AWP-002` stub per `STAGE-8-PLAN-DELTA.md:8.1` `SCHEMA vault interface stub → HSS encrypted-at-write`. Recorded here as input, not implemented.

### Field Shapes Needing Vault Interface Stub at AWP-002
*   `shared/client-profile.json:1-154` historical keys (now purged from history, shape preserved in `fixtures/synthetic/household-v1.json` 176 lines) — 11 top-level keys, `monthly_income_clp.client_net_salary`, `savings_investments.afp_mandatory`, `vector_capital_usd`, `fidelity_espp_usd`, `assets`, `debts` (see `TARGET-ARCHITECTURE.md:293` V.5 structural core)
*   `shared/evidence/*.json` payloads (future Evidence & Observation Store `TARGET-ARCHITECTURE.md:333`)
*   `shared/.cache/*` (Data Analyst file-backed TTL cache)
*   `shared/handoffs/*.md` (if retained as presentation, not machine interface)

All to be **encrypted-at-write from AWP-003 onward** (`STAGE-8-PLAN-DELTA.md:8.1` `HSS encrypted-at-write via vault stub`), `AWP-008` becomes hardening/whitelist enforcement (`docs/privacy/projection-whitelist.md` future).

### Hardening Re-affirmed at 000B:12.7
*   `.gitignore` `shared/handoffs/*.md` `shared/evidence/*.json` `shared/.cache/` `reports/*.md` `fixtures/local/` `*.zip` still passes `git check-ignore` post-purge (`000B:12.7`)
*   `README.md` design-only banner re-affirmed (already at `e35394d` IU-003) — now references `M0-answers.md` status `UNVERIFIED→REAL→purge` and `M0b` tag
*   No `.gitattributes` change (still `* text=auto eol=lf`)

---

## Next Steps (not at 000B)

*   `AWP-002` — create `vault/` interface stub `spec/vault-interface.md` defining `vault.encrypt(path)` / `vault.decrypt` / `vault.backup` (GAP-037 durability)
*   `AWP-003` — HSS encrypted-at-write via stub (`X 003:14` cutover)
*   `AWP-008` — vault hardening + whitelist `docs/privacy/projection-whitelist.md` + `tests/fitness/boundary_test.py`

*This file is `000B:12.7` acceptance artifact — vault layout inputs filed, `.gitignore` still passes post-purge.*

---

**Sign-off:** Dennis J. Naranjo — 2026-09-02 — vault inputs captured for `AWP-002` stub, no L2 implementation at 000B.

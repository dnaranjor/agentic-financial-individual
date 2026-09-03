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

## Next Steps (not at 000B) — Updated at AWP-013 IU-002 (2026-09-03, pre-pilot hardening)

*   `AWP-002` — create `vault/` interface stub `spec/vault-interface.md` defining `vault.encrypt(path)` / `vault.decrypt` / `vault.backup` (GAP-037 durability) — **DONE**: stub `docs/decisions/vault-interface-stub.md:14` + impl `vault/__init__.py:30` Fernet.
*   `AWP-003` — HSS encrypted-at-write via stub (`X 003:14` cutover) — **DONE**: `hss/store.py:54` `vault.encrypt(payload, scope="AcceptedFact", key_ref=fact.id)` + `hss/service.py:51` Snapshot encrypt.
*   `AWP-008` — vault hardening + whitelist `docs/privacy/projection-whitelist.md` + `tests/fitness/boundary_test.py` — **DONE**: `.gitignore:37-38` `vault/data/` `vault/keys/` ignored, Fernet hardening `vault/__init__.py:9`.
*   `AWP-013` — **Durability hardening (M7, pre-pilot)** — `hss/store.py:89` `BitemporalStore.load_from_vault()` decrypts `vault/data/AcceptedFact/*.enc` sorted by `recordedAt` with autoclosure replay + corrupt-skip logged to `reports/afi.log` via `lib/observability/logger.py`; `hss/backup.py:9` `backup`/`restore` real vault replay byte-identical (INV-15 GAP-037). `hss/service.py:16` `load_from_vault` flag for restart recovery. Verified via `tests/test_durability_reload.py:1`.

### Key Backup & Rotation — Manual (pre-pilot, not automated HSM)

*   **Backup (before pilot):** `mkdir -p ~/.afi/backup && cp vault/keys/vault.key ~/.afi/backup/vault.key.$(date -I)` — store offline, never git. Doc here is manual procedure, approved per AWP-013 user decision 2026-09-03 "Before Pilot". `.gitignore:38` guarantees `vault/keys/` never tracked (`git ls-files vault/keys` empty).
*   **Restore / new device:** `VAULT_DIR` is `vault/data` (`vault/__init__.py:11`) `KEYS_DIR` `vault/keys`; set `VAULT_DIR` env or pass `vault_dir` to `BitemporalStore.load_from_vault(vault_dir=Path(...))`. On new host: copy `vault.key` to `vault/keys/vault.key` with `0400`, then `store.load_from_vault()` before `query(validAt,asOf)` — `restore` in `hss/backup.py:17` validates byte-identical.
*   **Rotation (not yet justified, doc only):** Generate new key `Fernet.generate_key()`, iterate `vault/data/**/*.enc` `decrypt(old)` → `encrypt(new)` per file with same `key_ref`, replace `vault.key`, keep old backup 30d. Not executed at AWP-013.

*This file is `000B:12.7` acceptance artifact updated at `AWP-013:12.x` — vault layout inputs filed + durability hardened, `.gitignore` still passes post-purge.*

---

**Sign-off:** Dennis J. Naranjo — 2026-09-02 — vault inputs captured for `AWP-002` stub, no L2 implementation at 000B.

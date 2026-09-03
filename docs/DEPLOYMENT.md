# AFI Deployment — Startup / Shutdown / Topology

**Baseline:** `7625eb26cf404520ab9575e108d85841e080dc50` (`main`, 145 files, `README.md:3` hardening-v1)  
**Traceability:** `AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md:74` D0-D3, `hss/store.py:16`, `vault/__init__.py:30`  
**Status:** Library-level Python — no service, no external infra required.

## 1. Prerequisites

- Python 3.10.11 (tested) + `pip 23.0`
- Install deps: `pip install -r requirements.txt` (allows `>=` per AWP-013 IU-001; pinned minimums `pydantic>=2.12.3 cryptography>=48.0.0 jsonschema>=4.26.0 pytest>=9.1.1`, hashes in `requirements.txt:14` for win_amd64 audit)

## 2. Environment Bootstrap (D1)

```bash
python --version  # 3.10.11
pip install -r requirements.txt
python -c "import hss, market, jurisdiction, risk_gate, ingestion, orchestration, lifecycle, vault, assumptions, engine; print('imports OK')"
# schema registry 14 json load verified via validate_fixtures.py
python validate_fixtures.py  # 6/6 PASS
pytest tests/fitness/boundary_test.py tests/measure/test_round_trip.py  # 12/12 + 4/4
```

**Filesystem required dirs (created if missing, `.gitignore:18-23`):**
- `vault/data/` (Fernet ciphertext `AcceptedFact/*.enc`, `Snapshot/*.enc` — `vault/__init__.py:11`)
- `vault/keys/` (key `vault.key` — `vault/__init__.py:16`, ignored `vault/keys/` `git check-ignore` passes)
- `shared/evidence/`, `shared/handoffs/`, `fixtures/local/` (synthetic overrides ignored)

**Config:** code-based + `schema/registry/14` schemas (`unit.json`, `measure.json`, `accepted-fact.json` etc). No external config file.

## 3. Integration Topology (D2 discovery)

```
fixtures/synthetic/*.json → ingestion.service.IngestionService.extract() [L3 propose-only B-5]
  → schema/registry validation (Draft202012Validator) [L2]
  → ontology v1 two lineages (docs/ontology/v1.md)
  → HSS store.py BitemporalStore (B-2 sole writer, validAt/asOf, epsilon 5min hss/clock.py:6, vault encrypt-at-write vault/__init__.py:54)
  → Measure lib (lib/measure) → Engine calculator deterministic (engine/calculator.py:15)
  → Market per-series freshness (market/freshness.py) → Assumption screening INV-08 (assumptions/registry.py:20)
  → Jurisdiction per-person (jurisdiction/cl/evaluate_rule.py:18) → RiskGate → Orchestration compose validated modes (Baseline/Update orchestration/compose.py:8)
  → AnalysisRecord B-8 immutable (analysis_records/store.py) → Recommendation B-7 (recommendation/support.py:22) → Monitoring drift
```

Deferred absent (not a defect): `ledger/` (TAD-14 fact-plus-valuation), Execution, RAG, IAM — `docs/decisions/TAD-14-ledger-depth.md:5`.

No service boot — startup order is import order.

## 4. Startup Procedure

Library only — no daemon:

1. Verify `git rev-parse HEAD == 7625eb2` and `git status --porcelain` clean (report §2).
2. Ensure `vault/data` and `vault/keys` exist (`Path(vault/__init__.py:11).mkdir` auto-creates on first `vault.encrypt`).
3. Validate imports + schemas (see §2 commands).
4. For durability after restart: `store = BitemporalStore(); store.load_from_vault()` (AWP-013 IU-002, `hss/store.py:89`) repopulates in-memory facts from `vault/data/AcceptedFact/*.enc`.

## 5. Test Procedure

```bash
python tests/fitness/boundary_test.py      # 12/12 B-1..B-8 INV-01..15
python tests/fitness/test_jurisdiction_bypass.py  # bypass probe
pytest tests/measure/test_round_trip.py -v # CLP/UF/RATIO round-trip
python risk_gate/simulation/run_sweep.py   # VM4
python validate_fixtures.py                # 6/6
```

Full matrix 49 tests captured in `reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md:180` (D4-D6 scripts via `C:\Users\dnaranjor\AppData\Local\Temp\opencode\d3_trace3.py` etc).

## 6. Shutdown Procedure

- No service to stop. In-memory `BitemporalStore` state is durable via `vault/data/*.enc` ciphertext (Fernet) + `analysis_records/record-*.json` file (B-8). On process exit, `vault/data` retains encrypted facts; next startup call `load_from_vault()` to restore query state (see IU-013-002).
- Do not commit `vault/data/`, `vault/keys/`, `reports/afi.log` (`*.log` ignored), `fixtures/local/` — all `.gitignore:18-38` correctly ignored.
- Clean temp test artifacts: `vault/data/TestSec`, `reports/afi.log` truncation is operator action (log file manual rotation).

## 7. Known External Prerequisites / Limitations

- Prerequisites: Python 3.10, `requirements.txt` deps only.
- Limitations: In-memory HSS until `load_from_vault` (IU-002) — restart without load yields empty query; observability now via `reports/afi.log` jsonl (IU-003, `lib/observability/logger.py`), `*.log` ignored; OneDrive long path 116 chars with spaces — `pathlib` handles, avoid spaces in future test env identifier.

## 8. Observability (Post AWP-013)

- Log: `reports/afi.log` jsonl (gitignored) via `lib/observability/logger.py` — events `vault.encrypt`, `hss.accept`, `ingestion.extract`, `jurisdiction.evaluate`, `monitoring.drift` with masked values (hash not plaintext).
- Metrics: `monitoring/drift.py:8` staleness + engine timings via `reports/afi.log` correlation_id.

---
*Teams: file at `docs/DEPLOYMENT.md:1` satisfies DEF-005.*

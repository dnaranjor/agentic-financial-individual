# Agentic Financial Individual

> **BASELINE 7625eb2 (hardening-v1) — 145 files — M0→M6 COMPLETE**
>
> Implementation baseline `7625eb26cf404520ab9575e108d85841e080dc50` on `main` is **operational** (library-level Python). Design-only banner below is retained for historical forensics lineage.
>
> **Install (reproducible):** `pip install -r requirements.txt` (Python 3.10, see `requirements.txt:1` for `>=` pins with win_amd64 hashes). Verify via `python validate_fixtures.py` and `pytest tests/fitness/boundary_test.py tests/measure/test_round_trip.py`.
>
> **Branch Policy:**
> *   Authoritative forensics lineage: **`read-only/architecture-discovery`** pinned at `8854dfe` on 2026-09-02 (identical to `main` @ `8854dfe` then; now `main` diverged to `7625eb2` with M0→M6).
> *   `main` is implementation branch since `AWP-000A` (`c78456b`) through `AWP-012` (`7625eb2`).
> *   Future `main` may diverge further — re-verify `git ls-remote --heads origin` before any history-sensitive window.
>
> **Deployment:** See `docs/DEPLOYMENT.md:1` (procedure, env baseline, topology, startup/shutdown) and `reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md:1` (49 tests PASS, verdict READY WITH CONDITIONS, next AWP-013 hardening).
>
> **Forensics (historical):** `docs/decisions/M0-forensics.md` (Git history, PR #1, OneDrive zip `FA920E...`, tree-vs-tag `3f85432=tree`).
>
> ---

<details>
<summary>Historical DESIGN-ONLY banner (AWP-000A M0a, preserved for lineage)</summary>

> This repository was a governed design artifact at `8854dfe`. `AWP-000A` hardened future writes (`.gitignore`/`.gitattributes`) and filed forensics — **no history purge, no synthetic fixture, no Tier-0 intent resolution yet** then.
> `AWP-000B` `NOT AUTHORIZED` at that tag required `PRE-B1..B4`. Agents/schemas/HSS/engine/vault were deferred to `AWP-001..012` — now implemented at `7625eb2`.

</details>

AFI advisor for personal use — personal financial knowledge system (model-before-agent, L1→L2→L3). Ontology `docs/ontology/v1.md`, contracts `schema/registry/`, fiction `fixtures/synthetic/`.

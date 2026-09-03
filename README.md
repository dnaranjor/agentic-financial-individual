# Agentic Financial Individual (AFI) — Tu asesor financiero personal (Chile)
### Your personal, model-first financial knowledge system for Chilean households

> **Baseline:** `7625eb2` (hardening-v1) — 145 files — M0→M6 complete. Library-level Python, operational.
> **Línea base:** `7625eb2` — Python a nivel de librería, operativo. Sin servidor, sin infraestructura externa.

> ⚠️ **Not financial advice / No es asesoría financiera.** Educational software for organizing *your own* finances under Chilean rules (CLP, UF, AFP, FONASA/ISAPRE, PGU, RSH). The human (you) always decides. / Software educativo para organizar *tus propias* finanzas bajo reglas chilenas. El humano (tú) siempre decide.

**Works on:** Python 3.10.11 + `pip install -r requirements.txt` (`pydantic>=2.12.3`, `cryptography>=48.0.0`, `jsonschema>=4.26.0`, `pytest>=9.1.1`). License: `GPL-3.0` — see `LICENSE`. Forking for personal use means your fork stays GPL-3.0 if you distribute it.

---

## Table of contents / Índice

1. [What this is / Qué es](#1-what-this-is--qué-es)
2. [Who is it for / Para quién es](#2-who-is-it-for--para-quién-es)
3. [How it works in 60 seconds / Cómo funciona](#3-how-it-works-in-60-seconds--cómo-funciona-en-60-segundos)
4. [Repo map / Mapa del repo](#4-repo-map--mapa-del-repo)
5. [Quickstart — 5 minutes / Inicio rápido — 5 minutos](#5-quickstart--5-minutes--inicio-rápido--5-minutos)
6. [Use it for your own finances / Úsalo con tus finanzas](#6-use-it-for-your-own-finances--úsalo-con-tus-finanzas)
7. [Key concepts you must know / Conceptos clave](#7-key-concepts-you-must-know--conceptos-clave-que-debes-conocer)
8. [Agents guide / Guía de agentes](#8-agents-guide--guía-de-agentes)
9. [Security & privacy / Seguridad y privacidad](#9-security--privacy--seguridad-y-privacidad)
10. [Testing & validation / Pruebas y validación](#10-testing--validation--pruebas-y-validación)
11. [Limitations & roadmap / Limitaciones y ruta](#11-limitations--roadmap--limitaciones-y-ruta-futura)
12. [Docs index / Índice de docs](#12-docs-index--índice-de-documentos)
13. [History / Historia](#13-history--historia)
14. [License / Licencia](#14-license--licencia)

---

## 1. What this is / Qué es

**EN:** AFI turns your scattered household data — salary slips, AFP balances, mortgage in UF, market values (UF ≈ 39.405 CLP), and Chilean rules — into a governed knowledge base that can answer "where am I, what if, what should I consider?" without mixing facts with guesses.

It is **model-before-agent**: a strict data model + deterministic calculator comes first; AI agents only propose, never write state directly.

| What this IS | What this is NOT |
|---|---|
| Personal balance sheet + cash-flow + UF loan + retirement-horizon calculator with full provenance | A trading bot, auto-investor, or bank connector |
| Bitemporal fact store: every fact has `validFrom × recordedAt`, corrections append, never overwrite | A spreadsheet singleton that silently overwrites (`last-write-wins`) |
| Chilean-aware: `CLP` vs `UF` separated, `income_semantics`, PGU/tope imponible evaluated per person | A generic US-centric budget app |
| Human-decides: `Recommendation → Decision (you only) → Outcome` | An autonomous executor (execution is deferred, not wired) |

**ES:** AFI convierte tus datos dispersos — liquidaciones, saldos AFP, hipotecario en UF, valores de mercado y reglas chilenas — en una base de conocimiento gobernada que responde "dónde estoy, qué pasaría si, qué debería considerar", sin mezclar hechos con supuestos.

Es **modelo-antes-que-agente**: primero un modelo de datos estricto + calculadora determinista; los agentes solo proponen, nunca escriben estado directamente.

---

## 2. Who is it for / Para quién es

**EN — You are a good fit if you:**
- Manage a Chilean household and want a reproducible, auditable view (not just a spreadsheet).
- Know basic Python: `pip`, `venv`, running a script, editing JSON.
- Accept synthetic/fake data first, real data only on your machine, never committed.

**ES — Es para ti si:**
- Llevas las finanzas de tu hogar en Chile y quieres una vista reproducible y auditable.
- Manejas Python básico: `pip`, `venv`, correr un script, editar un JSON.
- Aceptas partir con datos sintéticos/falsos; tus datos reales solo en tu máquina, jamás en git.

No accounting background needed. / No necesitas ser contador.

---

## 3. How it works in 60 seconds / Cómo funciona en 60 segundos

**EN:** Two lineages never mix. Backward facts and forward guesses meet only inside a recorded `Analysis`.

```
Lineage 1 — reality (backward):                Lineage 2 — guesses (forward):
Evidence (PDF hash) ──extract──▶ Observation    Assumption ("inflation 3.5%")
  ──synthesize──▶ Claim (conflicts can coexist)    ──group──▶ AssumptionSet@v3
    ──accept (HSS sole writer)──▶ AcceptedFact
      (bitemporal validFrom × recordedAt)              MarketObservation (UF, 2026-09-02, BCCh)
        ──derive (deterministic engine)──▶ FinancialState (a VIEW, never a stored doc)
                                              │
                        ┌─────────────────────┴─────────────────────┐
                        ▼                                           │
        ANALYSIS (snapshot + assumptionSet + market + ruleVersions) │
                        ▼                                           │
        DerivedValue + Finding ──gate──▶ Recommendation ──▶ Decision (YOU) ──▶ Outcome
```

Layers: **L1** owns meaning (ontology/schemas) · **L2** validates + stores + computes (no LLM) · **L3** proposes with language/agents. Full rules in `docs/ontology/v1.md`.

**ES:** Dos linajes que nunca se mezclan. Hechos pasados y supuestos futuros solo se juntan dentro de un `Analysis` registrado. Capas: **L1** significado · **L2** valida/guarda/calcula (sin LLM) · **L3** propone con agentes. Detalle en `docs/ontology/v1.md`.

Data flow on this machine (from `docs/DEPLOYMENT.md`):

```
fixtures/synthetic/*.json → ingestion.service (L3 proposes)
 → schema/registry validation Draft202012 (L2)
 → hss/store.py BitemporalStore (sole writer, vault encrypt-at-write)
 → lib/measure → engine/calculator.py (deterministic)
 → market/freshness.py + assumptions/registry.py + jurisdiction/cl/evaluate_rule.py
 → risk_gate → orchestration/compose.py → analysis_records/store.py (immutable B-8)
 → recommendation/support.py → monitoring/drift.py
```

---

## 4. Repo map / Mapa del repo

**EN:** Start at the bold rows. The rest you read as needed.

| Path | What it is — start here | Key file |
|---|---|---|
| **`validate_fixtures.py`** | **Only CLI entry. Run first — validates fixtures vs schemas + negative rejects** | `validate_fixtures.py:57` |
| **`requirements.txt`** | **Pinned deps + win hashes + freeze fingerprint** | `requirements.txt:9-28` |
| **`docs/DEPLOYMENT.md`** | **Startup/shutdown/topology, no daemon** | `docs/DEPLOYMENT.md:1` |
| **`fixtures/synthetic/`** | **Fake data you may freely use: `household-v1.json`, `bitemporal-edge.json`, `uf-edge.json`** | `fixtures/synthetic/household-v1.json:1` |
| **`schema/registry/`** | 15 normative JSON Schemas (`measure`, `unit`, `accepted-fact`, `person-household`, …) Draft202012 | `schema/registry/` |
| **`hss/`** | Household State Service — **sole writer**: `accept_claim`, `query_state`, `freeze_snapshot` + `BitemporalStore`, `clock` (5-min epsilon), `backup` | `hss/service.py:16` |
| **`lib/measure/`** | Shared money lib: `models`, `convert` (cross-basis raises), `format` (es-CL `5.245.000`, `39.405,00`) | `lib/measure/format.py:7` |
| **`engine/`** | Deterministic calculator only: `net_worth`, `cash_flow`, `amortize_uf`, `horizon_years`, `gap_analysis` (`ENGINE_VERSION 0.1.0`) | `engine/calculator.py:25` |
| **`ingestion/`** | `Evidence → Observation` proposer (L3), L2 validates shape | `ingestion/` |
| **`market/`** | `MarketObservation(series, asOf, source)` + staleness | `market/` |
| **`jurisdiction/cl/`** | Chile rules, referenced never embedded: `pgu_eligibility`, `tope_imponible` per person | `jurisdiction/cl/evaluate_rule.py:18` |
| **`assumptions/`** | Forward posits registry + screening | `assumptions/` |
| **`risk_gate/`** | Risk & Consistency Gate, Findings, sweep simulation | `risk_gate/` |
| **`orchestration/` + `orchestrator/`** | L3 workflow routing + `compose` validated modes (Baseline/Update) | `orchestration/` |
| **`recommendation/`** | Gated builder — refs DerivedValue IDs only | `recommendation/` |
| **`analysis_records/`** | Immutable `AnalysisRecord` outputs | `analysis_records/` |
| **`agents/`** | 9 prompt-spec agents (`SKILL.md` each): `user-profile`, `document-ingestion`, `data-analyst`, `financial-calculator`, `chilean-regulatory`, `risk-evaluation`, `report-generator`, `execution`, `trading-analyst` — specs, not services | `agents/` |
| **`vault/`** | At-rest Fernet encryption stub: `encrypt`, `list_encrypted`; `vault/data/`, `vault/keys/` auto-created, git-ignored | `vault/` |
| **`tests/`** | `fitness/boundary_test.py` (B-1..B-8, INV-01..15) + `measure/test_round_trip.py` (CLP/UF/RATIO) | `tests/` |
| **`spec/`** | Normative contract `measure-contract.md` (`Measure{value,unit,basis}`) | `spec/` |
| **`docs/`** | `ontology/v1.md`, `glossary.md`, `assumptions/`, `decisions/`, `evidence/`, `privacy/`, `migrations/`, `history/`, `friction/` | `docs/glossary.md:1` |
| **`reports/`** | Generated outputs + validation report (git-ignored `*.md` except committed validation report) | `reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md` |
| **`lifecycle/`, `monitoring/`, `explanation/`, `research/`, `learning/`** | Decision→Outcome tracking, drift, provenance explanations, citations, lessons | — |
| **`shared/`** | Legacy runtime (do not put real data here) | — |
| **`.gitignore` / `.gitattributes` / `.githooks/`** | Containment: ignore PII/runtime/secrets, LF normalization, pre-commit guard placeholder | `.gitignore:9-38` |

**ES:** Parte por las filas en negrita. El resto se lee según necesidad.

---

## 5. Quickstart — 5 minutes / Inicio rápido — 5 minutos

**Prerequisites / Prerrequisitos:** Windows (PowerShell 5.1) or Linux/macOS, Python 3.10.11, `git`.

```powershell
# 1. Clone / Clonar
git clone https://github.com/dnaranjor/agentic-financial-individual.git
cd agentic-financial-individual

# 2. Isolate + install / Aislar + instalar
python --version  # must be 3.10.11 / debe ser 3.10.11
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# 3. Smoke test: imports / Prueba de humo: imports
python -c "import hss, market, jurisdiction, risk_gate, ingestion, orchestration, lifecycle, vault, engine; print('imports OK')"
# Expected / Esperado: imports OK

# 4. Validate fixtures vs schemas / Validar fixtures contra esquemas
python validate_fixtures.py
```

Expected output / Salida esperada (verified 2026-09-03, Python 3.10.11):

```
PASS: fixtures/synthetic/household-v1.json (synthetic v0 shape, fully_random, entropy already validated at 000B)
PASS: fixtures/synthetic/bitemporal-edge.json -> accepted-fact.json
PASS: fixtures/synthetic/uf-edge.json (contains INDEX_UF partitioned)
PASS negative 1: U-04 enum must reject ES label bruto -> REJECT observed ('bruto' is not one of ['gross', 'net_of_afp', 'net_of_afp_and_health'])
PASS negative 2: B-4 core field ref jurisdiction must reject -> REJECT observed ('jurisdiction_rule' should not be valid ...)
PASS negative UF: UF 39405 as CURRENCY_CLP would fail MeasureBasis business check (manual)
PASS: old client-profile.json correctly FAILS new schema ('persons' is a required property)

=== SUMMARY: PASS ===
```

```powershell
# 5. Run tests / Correr pruebas
python -m pytest tests/measure/test_round_trip.py -q
# Expected / Esperado: 4 passed

python tests/fitness/boundary_test.py
# Expected / Esperado: === FITNESS SUMMARY: PASS === (B-1..B-8, UF ban, labels, L2!=L3, INV-01..15)
```

If any step fails, see `docs/DEPLOYMENT.md:7-21` and [Testing](#10-testing--validation--pruebas-y-validación). / Si algo falla, ver `docs/DEPLOYMENT.md:7-21`.

---

## 6. Use it for your own finances / Úsalo con tus finanzas

### 6.1 Runnable example (synthetic, copy-paste) / Ejemplo ejecutable (sintético, copiar-pegar)

**EN:** Paste this after Quickstart. It uses fake numbers only — no real PII. It shows the 3 core calls: net worth, cash flow, UF mortgage payment, plus Chilean formatting.

**ES:** Pega esto después del Quickstart. Usa solo números falsos — sin datos reales. Muestra las 3 llamadas centrales: patrimonio neto, flujo de caja, dividendo hipotecario en UF, más formato chileno.

```python
from datetime import date
from hss.models import Measure, MeasureBasis, Unit
from hss.service import HouseholdStateService
from engine.calculator import net_worth, cash_flow, amortize_uf, horizon_years
from lib.measure.format import format_measure
from jurisdiction.cl.evaluate_rule import evaluate_rule

# 1. Money always carries unit + basis (never a bare number)
#    El dinero siempre lleva unidad + base (nunca un número solo)
basis_clp = MeasureBasis(unit=Unit.CURRENCY_CLP, type="real", basePeriod="2026-09", asOf=date(2026, 9, 2))
salary  = Measure(value=5245000, unit=Unit.CURRENCY_CLP, basis=basis_clp, ontologyVersion="v1")
savings = Measure(value=1000000, unit=Unit.CURRENCY_CLP, basis=basis_clp, ontologyVersion="v1")

print(format_measure(salary))  # -> 5.245.000 (es-CL, no decimals for CLP)

# 2. Deterministic engine: same inputs => same outputs, with provenance
#    Motor determinista: mismos inputs => mismos outputs, con procedencia
nw = net_worth([salary, savings], snapshot_id="demo-snap")
print(nw["value"], nw["formulaId"], nw["engineVersion"])  # -> 6245000.0 net_worth 0.1.0

cf = cash_flow([salary], [savings], snapshot_id="demo-snap")
print(cf["value"])  # -> 4245000.0

# 3. UF loan: UF is INDEX_UF, never CURRENCY_CLP
#    Crédito en UF: UF es INDEX_UF, nunca CURRENCY_CLP
pmt = amortize_uf(outstanding_uf=2151.45, annual_rate=0.0443, remaining_installments=409, snapshot_id="demo-snap")
print(round(pmt["value"], 2), pmt["unit"])  # -> ~10.2 INDEX_UF per installment / por dividendo

# 4. Retirement horizon from birthDate (not a magic constant)
#    Horizonte a jubilación desde birthDate (no constante mágica)
print(horizon_years(birth_date=date(1959, 3, 15), retirement_age=67, valid_at=date(2026, 9, 2)))  # -> 0 (at 67)

# 5. Chilean rule per person (synthetic demo persons inside the module)
#    Regla chilena por persona (personas demo sintéticas dentro del módulo)
print(evaluate_rule("pgu_eligibility", "principal", date(2026, 9, 2))["reason"])  # age / RSH / residency reason
print(evaluate_rule("tope_imponible", "principal", date(2026, 9, 2))["reason"])   # tope 83.4 UF applies

# 6. Store a fact the governed way (HSS is the sole writer)
#    Guardar un hecho de forma gobernada (HSS es el único escritor)
hss = HouseholdStateService()
fact = hss.accept_claim(claim_id="demo-claim-1", valid_from=date(2026, 9, 1), value={"net_salary": salary.model_dump(mode="json")})
print(hss.query_state(validAt=date(2026, 9, 2))[0].id == fact.id)  # -> True
snap_id, _blob = hss.freeze_snapshot(validAt=date(2026, 9, 2))
print("snapshot", snap_id[:8])  # immutable snapshot id / snapshot inmutable
```

### 6.2 Your data workflow / Tu flujo con tus datos

**EN:**
1. **Copy, don't edit:** `cp fixtures/synthetic/household-v1.json fixtures/local/my-household.json` (`fixtures/local/` is git-ignored — safe place for drafts).
2. **Replace values** with yours but keep the shape + `"synthetic": true` until you understand the schema. Keep `income_semantics` English (`gross` | `net_of_afp` | `net_of_afp_and_health`) — never `bruto` (schema rejects it, see negative test above).
3. **Propose via ingestion** (`ingestion/service.py`), **validate** against `schema/registry/*.json`, **accept** via `hss/service.py HouseholdStateService.accept_claim` — never write `shared/client-profile.json` by hand.
4. **Compute** with `engine/calculator.py`, **check freshness** (`market/`), **screen assumptions** (`assumptions/registry.py`), **evaluate rules** (`jurisdiction/cl/evaluate_rule.py`), **pass the gate** (`risk_gate/`), **compose** (`orchestration/compose.py`), **record** (`analysis_records/store.py`), **recommend** (`recommendation/support.py`).
5. **Decide yourself**, then track reality in `monitoring/drift.py` + `lifecycle/`.
6. After restart, restore with `HouseholdStateService(load_from_vault=True)` / `store.load_from_vault()` — in-memory state is durable only via `vault/data/*.enc` (see `docs/DEPLOYMENT.md:54`).

**ES:**
1. **Copia, no edites:** `fixtures/synthetic/household-v1.json` → `fixtures/local/my-household.json` (`fixtures/local/` está ignorado por git — lugar seguro).
2. **Reemplaza valores** manteniendo la forma. `income_semantics` en inglés (`gross` | `net_of_afp` | `net_of_afp_and_health`) — nunca `bruto` (el esquema lo rechaza).
3. **Propón** vía `ingestion`, **valida** contra `schema/registry/`, **acepta** vía `HSS` — nunca edites estado a mano.
4. **Calcula** con `engine`, **vigencia** con `market`, **supuestos** con `assumptions`, **reglas** con `jurisdiction`, **portón** con `risk_gate`, **compón** con `orchestration`, **registra** con `analysis_records`, **recomienda** con `recommendation`.
5. **Decide tú**, luego sigue la realidad en `monitoring` + `lifecycle`.
6. Tras reiniciar, restaura con `load_from_vault()` — la memoria solo persiste vía `vault/data/*.enc`.

---

## 7. Key concepts you must know / Conceptos clave que debes conocer

**EN/ES — the 6 ideas that prevent 90% of errors:**

1. **`Measure = value + unit + basis`. / Medida = valor + unidad + base.** `MeasureBasis(unit, nominal|real, basePeriod=YYYY-MM, asOf=date)`. Mixing bases raises (`engine/validate.py cross_basis_check`). Contract: `spec/measure-contract.md`, types: `hss/models.py:10-31`.
2. **`UF is INDEX_UF, not money.` / UF es índice, no moneda.** `Unit ∈ {CURRENCY_CLP, CURRENCY_USD, INDEX_UF, INSTRUMENT_QTY, RATIO}`. Putting UF `39405` as `CURRENCY_CLP` is a business-rule failure by design.
3. **`income_semantics` is mandatory. / Semántica de ingreso obligatoria.** `gross` (bruto) | `net_of_afp` (neto de AFP) | `net_of_afp_and_health` (neto de AFP y salud). Example: `{value:5245000, unit:CURRENCY_CLP, income_semantics:net_of_afp_and_health}`. Source: `docs/glossary.md:54-63`, `docs/ontology/v1.md:126-134`.
4. **Bitemporal facts. / Hechos bitemporales.** `AcceptedFact(validFrom, validTo?, recordedAt)`. Query is always `query_state(validAt, asOf)` — "what was true then, as known at R". Corrections append a new fact; history is never rewritten.
5. **`FinancialState` is a view. / Estado Financiero es vista.** Never a stored document you edit. Freeze it (`freeze_snapshot`) only to feed an `Analysis`.
6. **English IDs, Spanish labels. / IDs en inglés, etiquetas en español.** Code/schema/agents: `Evidence`, `net_of_afp`, `evaluate_rule`. UI/reports only: `Evidencia`, `neto de AFP`, `Evaluar elegibilidad PGU`. Lint rejects Spanish labels in code (except `docs/glossary.md`, `docs/ontology/v1.md`). See `docs/glossary.md:9`, `docs/decisions/TAD-11_language.md`.

Full definitions: `docs/ontology/v1.md:37-56` (table of 13 concepts), `docs/glossary.md:13-55`.

---

## 8. Agents guide / Guía de agentes

**EN:** Agents are prompt-specs (`SKILL.md`), not installed services. Read them as procedures; the code functions inside are signatures to implement/call, with HSS as sole writer and Risk as gate.

| Agent (folder) | Use it when… | Boundary |
|---|---|---|
| `agents/user-profile-agent/` | Loading/validating/merging profile (atomic save with filelock) | Via HSS only |
| `agents/document-ingestion-agent/` | Turning a PDF/statement into `Evidence → Observation` | Propose-only (B-5) |
| `agents/data-analyst-agent/` | Synthesizing Observations/attestations into `Claim` | L3 proposes, L2 validates |
| `agents/financial-calculator-agent/` | Running deterministic math | Engine only, no LLM in L2 (B-3) |
| `agents/chilean-regulatory-agent/` | Checking PGU, tope imponible, AFP/health semantics | Rules referenced, never embedded (B-4) |
| `agents/risk-evaluation-agent/` | Raising `Finding`s, running sweep | Gate `GATE-005` |
| `agents/report-generator-agent/` | Rendering es-CL reports (`5.245.000`, `39.405,00`) | Presentation only |
| `agents/execution-agent/` | (Deferred) Acting on a Decision | Human must approve |
| `agents/trading-analyst-agent/` | Research citations for Claims | Citations, not facts |

**ES:** Los agentes son especificaciones (`SKILL.md`), no servicios instalados. Léelos como procedimientos; HSS es el único escritor y Riesgo es el portón.

---

## 9. Security & privacy / Seguridad y privacidad

**EN:**
- **Synthetic first.** Real `shared/client-profile.json` was purged from history for exposure. Work only with `fixtures/synthetic/*`. Your real file belongs in `fixtures/local/` (ignored) or outside the repo — never `git add` it.
- **Ignored by design** (`.gitignore:9-38`): `shared/client-profile.json`, `shared/handoffs/*.md`, `shared/evidence/*.json`, `vault/data/`, `vault/keys/`, `fixtures/local/`, `*.zip`, `*.log`, `__pycache__/`. Verify with `git check-ignore -v <path>` and `git status --porcelain` before every commit.
- **Encryption at rest:** `vault/` Fernet (`cryptography`). HSS encrypts on write; snapshots too (`hss/service.py:49-55`). Logs in `reports/afi.log` mask values (hash, not plaintext) via `lib/observability/logger.py`.
- **No secrets in repo.** Keys live in `vault/keys/` (ignored). OneDrive `.zip` copies are quarantine vectors — don't re-add `*.zip`.

**ES:**
- **Primero sintético.** El `client-profile.json` real fue purgado del historial por exposición. Trabaja solo con `fixtures/synthetic/*`. Tu archivo real va en `fixtures/local/` (ignorado) o fuera del repo — nunca `git add`.
- **Ignorados por diseño**, verifica con `git check-ignore` y `git status` antes de cada commit.
- **Cifrado en reposo** con `vault/` Fernet; logs enmascarados, claves en `vault/keys/`.

---

## 10. Testing & validation / Pruebas y validación

| Command / Comando | What it proves / Qué prueba | Expected / Esperado |
|---|---|---|
| `python validate_fixtures.py` | Fixtures match registry + 3 negatives reject + old profile fails | `=== SUMMARY: PASS ===` (6/6) |
| `python -m pytest tests/measure/test_round_trip.py -q` | `HSS→lib→HSS` identity + es-CL `5.245.000` / `39.405,00` + cross-basis raises | `4 passed` |
| `python tests/fitness/boundary_test.py` | Boundaries B-1..B-8, UF ban, labels, L2≠L3, INV-01..15 | `=== FITNESS SUMMARY: PASS ===` |
| `python tests/fitness/test_jurisdiction_bypass.py` | Jurisdiction cannot be bypassed (B-4) | PASS probe |
| `python risk_gate/simulation/run_sweep.py` | Risk sweep VM4 | sweep output |
| `python -c "import hss, ...; print('imports OK')"` | Env topology import order (D1) | `imports OK` |

Full 49-test matrix + fingerprints: `reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md`. Procedure + shutdown (no daemon; `load_from_vault()` on restart; rotate `reports/afi.log` manually): `docs/DEPLOYMENT.md:46-72`.

---

## 11. Limitations & roadmap / Limitaciones y ruta futura

**EN — Honest limits (not defects):**
- Library only — no web UI, no daemon, no auto bank sync. Startup order = import order.
- Deferred by design (`docs/DEPLOYMENT.md:44`, `docs/decisions/TAD-14-ledger-depth.md`): double-entry `ledger/`, Execution wiring, RAG, IAM.
- In-memory HSS until `load_from_vault()` — restart without load = empty query.
- OneDrive long paths with spaces work via `pathlib`, but prefer short ASCII paths for test envs.
- Next: AWP-013 hardening (observability via `reports/afi.log` jsonl + `monitoring/drift.py` already landed).

**ES — Límites honestos (no son fallas):** solo librería, sin UI web ni demonio; `ledger/`, Ejecución, RAG, IAM diferidos por diseño; HSS en memoria hasta `load_from_vault()`; tras reiniciar hay que recargar; siguiente paso AWP-013.

---

## 12. Docs index / Índice de documentos

| Read… / Lee… | To… / Para… |
|---|---|
| `docs/ontology/v1.md` | Normative model: two lineages, 13 concepts, transformations, income decision |
| `docs/glossary.md` | EN identifiers → es-CL labels + `5.245.000` examples |
| `docs/DEPLOYMENT.md` | Bootstrap, topology, startup/shutdown, observability |
| `reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md` | 49-test evidence, verdict READY WITH CONDITIONS |
| `spec/measure-contract.md` | `Measure{value,unit,basis}` contract |
| `docs/decisions/` | `M0-forensics.md`, `M0-answers.md`, `TAD-11_language.md`, `TAD-14-ledger-depth.md`, `vault-*.md`, `schema-language.md` |
| `docs/assumptions/freshness-policy.md` | Market staleness classes |
| `docs/privacy/` + `docs/evidence/ledger-gate/` | Retention + gate evidence |
| `docs/history/` + `docs/migrations/` | Archived PROMPT v1.3 + migration notes |
| `learning/lessons-learned.md` | Agent self-improvement protocol |

---

## 13. History / Historia

> **BASELINE `7625eb2` (hardening-v1) — operational.** `main` is the implementation branch since `AWP-000A` through `AWP-012`.

<details>
<summary>Forensics lineage (collapsed per reader preference — click to expand)</summary>

Historical design-only banner from `8854dfe` (AWP-000A M0a) preserved for lineage. Forensics (git history, PR #1, OneDrive zip `FA920E…`, tree-vs-tag `3f85432=tree`, purge + synthetic fixture at 000B): see `docs/decisions/M0-forensics.md`. Authoritative forensics branch `read-only/architecture-discovery` pinned at `8854dfe`; `main` has since diverged to `7625eb2`. Re-verify `git ls-remote --heads origin` before any history-sensitive operation.

</details>

---

## 14. License / Licencia

**EN:** `GPL-3.0` — see `LICENSE` (full text). Personal use and private modification are fine. If you distribute your fork (binary or source), you must share source under GPL-3.0 too.

**ES:** `GPL-3.0` — ver `LICENSE`. Uso personal y modificación privada sin problema. Si distribuyes tu fork, debes compartir el código bajo GPL-3.0 también.

Questions / Preguntas: open an Issue with your `python --version`, `pip freeze` subset (`pydantic|cryptography|jsonschema|pytest`), and the failing command output.

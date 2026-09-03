<!--
*** AFI — Asesor Financiero Individual
*** Estructura inspirada en el Best-README-Template (othneildrew)
*** y en las guías de README reproducible de Utrecht University.
-->

<a id="readme-top"></a>

<!-- BADGES -->
[![Licencia GPL-3.0][license-shield]][license-url]
[![Python 3.10.11][python-shield]][python-url]
[![Validación][validation-shield]][validation-url]

<br />
<div align="center">

  <h1 align="center">AFI — Asesor Financiero Individual</h1>

  <p align="center">
    Tu sistema personal de conocimiento financiero para hogares chilenos,
    gobernado por un modelo de datos estricto y cálculos deterministas.
    <br />Tu asesor financiero personal, <em>model-first</em>, para Chile.
    <br />
    <br />
    <a href="#empezando"><strong>Empieza aquí »</strong></a>
    ·
    <a href="#cómo-funciona">Cómo funciona</a>
    ·
    <a href="#seguridad-y-privacidad">Seguridad</a>
    ·
    <a href="#licencia">Licencia</a>
  </p>
</div>

> ⚠️ **No es asesoría financiera profesional.** Toda asesoría descansa en modelos de Inteligencia Artificial (LLM). Se recomienda emplear un modelo de frontera como Claude Opus 5 o GPT 5.6 Sol para mejores resultados. Software educativo para organizar *tus propias* finanzas bajo reglas chilenas (CLP, UF, AFP, FONASA/ISAPRE, PGU, RSH). El humano (tú) siempre decide. Las recomendaciones nunca se ejecutan automáticamente.

---

## Tabla de contenidos

<details>
  <summary>Tabla de contenidos</summary>
  <ol>
    <li><a href="#sobre-el-proyecto">Sobre el proyecto</a></li>
    <li><a href="#agentes">Agentes</a></li>
    <li><a href="#empezando">Empezando</a></li>
    <li><a href="#cómo-funciona">Cómo funciona</a></li>
    <li><a href="#conceptos-clave">Conceptos clave</a></li>
    <li><a href="#mapa-del-repo">Mapa del repositorio</a></li>
    <li><a href="#seguridad-y-privacidad">Seguridad y privacidad</a></li>
    <li><a href="#documentación">Documentación</a></li>
    <li><a href="#problemas-o-contacto">Problemas o contacto</a></li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#agradecimientos">Agradecimientos</a></li>
  </ol>
</details>

---

## Sobre el proyecto

**AFI** convierte tus datos financieros dispersos — liquidaciones de sueldo, saldos de AFP, hipotecario en UF, valores de mercado y reglas chilenas — en una **base de conocimiento gobernada** que responde tres preguntas: *¿dónde estoy?, ¿qué pasaría si…?, ¿qué debería considerar?* — sin mezclar hechos con suposiciones.

El principio central es **modelo-antes-que-agente**: primero un modelo de datos estricto y una calculadora determinista; los agentes de IA solo *proponen*, nunca escriben el estado directamente.

| **AFI es** | **AFI NO es** |
|---|---|
| Balance personal + flujo de caja + préstamo en UF + horizonte de jubilación, con procedencia total | Un bot de trading, auto-inversor o conector bancario |
| Almacén de hechos bitemporal: cada hecho tiene `validFrom × recordedAt`; las correcciones se agregan, nunca sobrescriben | Una planilla que sobrescribe silenciosamente |
| Consciente de Chile: `CLP` vs `UF` separados, `income_semantics`, PGU / tope imponible evaluados por persona | Una app de presupuesto genérica centrada en EEUU |
| Humano decide: `Recommendation → Decision (tú) → Outcome` | Un ejecutor autónomo (la ejecución está diferida) |

### Para quién es

Es para ti si:

- Llevas las finanzas de tu hogar **en Chile** y quieres una vista reproducible y auditable (no solo una planilla).
- Manejas **Python básico**: `pip`, `venv`, correr un script, editar un JSON.
- Aceptas partir con **datos sintéticos/falsos**; tus datos reales los usas solo en tu máquina, jamás en git.

No necesitas ser contador ni experto financiero.

### Tecnologías

- **Python 3.10.11** (librería: no hay servidor ni infraestructura externa)
- **Pydantic** — modelos de datos del Household State Service
- **jsonschema** — validación de esquemas Draft202012
- **cryptography (Fernet)** — cifrado en reposo de datos sensibles
- **pytest** — suite de pruebas

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Agentes

Los agentes son **especificaciones** (`SKILL.md`), no servicios instalados. Léeas como procedimientos: **HSS es el único escritor** y **Riesgo es el portón**.

```text
user-profile-agent        Cargar/validar/mezclar perfil          → vía HSS solo
document-ingestion-agent  Convertir PDF/estado en Evidence→Observation → solo propone (B-5)
data-analyst-agent        Sintetizar Observations en Claim       → L3 propone, L2 valida
financial-calculator-agent  Ejecutar matemática determinista      → solo motor, sin LLM en L2 (B-3)
chilean-regulatory-agent  Revisar PGU, tope imponible, AFP/salud → reglas referenciadas, nunca incrustadas (B-4)
risk-evaluation-agent     Levantar Findings, correr barrido       → portón GATE-005
report-generator-agent    Renderizar reportes es-CL               → solo presentación
execution-agent           (Diferido) Actuar sobre una Decisión    → el humano debe aprobar
trading-analyst-agent     Citas de investigación para Claims      → citas, no hechos
```

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Empezando

### Prerrequisitos

- **Python 3.10.11** (verifica con `python --version`)
- **git**
- Sistema: Windows (PowerShell 5.1), Linux o macOS

### Instalación

```powershell
# 1. Clona el repositorio
git clone https://github.com/dnaranjor/agentic-financial-individual.git
cd agentic-financial-individual

# 2. Verifica la versión de Python (debe ser 3.10.11)
python --version

# 3. Aísla el entorno e instala dependencias
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

# 4. Prueba de humo: los imports cargan correctamente
python -c "import hss, market, jurisdiction, risk_gate, ingestion, orchestration, lifecycle, vault, engine; print('imports OK')"
# Esperado: imports OK
```

Si algún paso falla, consulta [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) (procedimiento completo de arranque/apagado).

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Cómo funciona

Dos linajes que **nunca se mezclan**. Los hechos pasados y las suposiciones futuras solo se encuentran dentro de un `Analysis` registrado.

- **Linaje 1 — realidad (hacia atrás):** `Evidence (hash PDF) → Observation → Claim → AcceptedFact` (hecho bitemporal `validFrom × recordedAt`).
- **Linaje 2 — suposiciones (hacia adelante):** `Assumption ("inflación 3.5%") → AssumptionSet@v3` + `MarketObservation` (UF, fecha, fuente BCCh).

De ahí se **deriva** el `FinancialState` (una *vista*, nunca un documento editado) y se produce el flujo:

```
DerivedValue + Finding ──gate──▶ Recommendation ──▶ Decision (TÚ) ──▶ Outcome
```

**Capas:** **L1** define el significado (ontología/esquemas) · **L2** valida, guarda y calcula (sin LLM) · **L3** propone con lenguaje/agentes.

> Detalle normativo completo (dos linajes, 13 conceptos, transformaciones, decisión de ingresos): [`docs/ontology/v1.md`](docs/ontology/v1.md). Flujo de datos y topología: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Conceptos clave

Seis ideas que previenen el 90% de los errores:

1. **`Measure = valor + unidad + base`.** `MeasureBasis(unit, nominal|real, basePeriod=YYYY-MM, asOf=date)`. Mezclar bases lanza error (`engine/validate.py cross_basis_check`). Contrato: [`spec/measure-contract.md`](spec/measure-contract.md).
2. **`UF es INDEX_UF, no es dinero`.** `Unit ∈ {CURRENCY_CLP, CURRENCY_USD, INDEX_UF, INSTRUMENT_QTY, RATIO}`. Poner UF `39405` como `CURRENCY_CLP` es un fallo de regla de negocio por diseño.
3. **`income_semantics` es obligatorio.** `gross` (bruto) | `net_of_afp` (neto de AFP) | `net_of_afp_and_health` (neto de AFP y salud). Ejemplo: `{value:5245000, unit:CURRENCY_CLP, income_semantics:net_of_afp_and_health}`.
4. **Hechos bitemporales.** `AcceptedFact(validFrom, validTo?, recordedAt)`. Siempre consulta `query_state(validAt, asOf)` — "qué era verdad entonces, según se conocía en R". Las correcciones agregan un hecho nuevo; el historial nunca se reescribe.
5. **`FinancialState` es una vista.** Nunca un documento editado. Congélala (`freeze_snapshot`) solo para alimentar un `Analysis`.
6. **IDs en inglés, etiquetas en español.** Código/esquemas/agentes: `Evidence`, `net_of_afp`, `evaluate_rule`. Solo reportes/UI: `Evidencia`, `neto de AFP`, `Evaluar elegibilidad PGU`. El linter rechaza etiquetas en español dentro del código.

> Definiciones completas: [`docs/glossary.md`](docs/glossary.md) y [`docs/ontology/v1.md`](docs/ontology/v1.md).

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Mapa del repositorio

Empieza por las filas en **negrita**; el resto lo lees según necesidad. (Ruta completa: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).)

| Ruta | Qué es — empieza aquí |
|---|---|
| **`validate_fixtures.py`** | **Única entrada CLI. Ejecútala primero — valida fixtures contra esquemas** |
| **`requirements.txt`** | **Dependencias fijadas + hashes de Windows** |
| **`fixtures/synthetic/`** | **Datos falsos que puedes usar libremente: `household-v1.json`, `bitemporal-edge.json`, `uf-edge.json`** |
| **`docs/DEPLOYMENT.md`** | **Arranque/apagado, topología, observabilidad** |
| `schema/registry/` | 15 esquemas JSON normativos Draft202012 |
| `hss/` | Household State Service — **único escritor**: `accept_claim`, `query_state`, `freeze_snapshot` |
| `lib/measure/` | Librería de dinero compartida: `models`, `convert`, `format` (es-CL `5.245.000`, `39.405,00`) |
| `engine/` | Calculadora determinista: `net_worth`, `cash_flow`, `amortize_uf`, `horizon_years`, `gap_analysis` |
| `ingestion/` | Proponente `Evidence → Observation` (L3); L2 valida la forma |
| `market/` | `MarketObservation(series, asOf, source)` + vigencia |
| `jurisdiction/cl/` | Reglas chilenas, referenciadas nunca incrustadas: `pgu_eligibility`, `tope_imponible` |
| `assumptions/` | Registro de supuestos a futuro + filtrado |
| `risk_gate/` | Portón de riesgo y consistencia, Findings, simulación de barrido |
| `orchestration/` + `orchestrator/` | Enrutado de flujo L3 + `compose` con modos validados |
| `recommendation/` | Constructor con portón — referencia solo IDs de `DerivedValue` |
| `analysis_records/` | Salidas inmutables `AnalysisRecord` |
| `agents/` | 9 agentes como especificación (`SKILL.md` cada uno) — especificaciones, no servicios |
| `vault/` | Cifrado Fernet en reposo: `encrypt`, `list_encrypted` |
| `tests/` | `fitness/boundary_test.py` (B-1..B-8, INV-01..15) + `measure/test_round_trip.py` |
| `spec/` | Contrato normativo `measure-contract.md` |
| `docs/` | `ontology/v1.md`, `glossary.md`, `assumptions/`, `decisions/`, `privacy/`, `migrations/`… |
| `reports/` | Salidas generadas + informe de validación |
| `shared/` | Runtime heredado (no pongas datos reales aquí) |

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Seguridad y privacidad

- **Sintético primero.** El `client-profile.json` real fue purgado del historial por exposición. Trabaja solo con `fixtures/synthetic/*`. Tus datos reales van en `fixtures/local/` (ignorado) o fuera del repo — nunca `git add`.
- **Ignorados por diseño** (`.gitignore`): `shared/client-profile.json`, `shared/handoffs/*.md`, `shared/evidence/*.json`, `vault/data/`, `vault/keys/`, `fixtures/local/`, `*.zip`, `*.log`, `__pycache__/`. Verifica con `git check-ignore -v <ruta>` y `git status --porcelain` antes de cada commit.
- **Cifrado en reposo:** `vault/` Fernet (`cryptography`). HSS cifra al escribir; los snapshots también. Los logs enmascaran valores (hash, no texto plano).
- **Sin secretos en el repo.** Las claves viven en `vault/keys/` (ignorado). Copias `.zip` de OneDrive son vectores de cuarentena — no vuelvas a añadir `*.zip`.

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Documentación

| Lee… | Para… |
|---|---|
| [`docs/ontology/v1.md`](docs/ontology/v1.md) | Modelo normativo: dos linajes, 13 conceptos, transformaciones |
| [`docs/glossary.md`](docs/glossary.md) | Identificadores EN → etiquetas es-CL + ejemplos `5.245.000` |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Bootstrap, topología, arranque/apagado, observabilidad |
| [`reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md`](reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md) | Evidencia de 49 pruebas, veredicto READY |
| [`spec/measure-contract.md`](spec/measure-contract.md) | Contrato `Measure{value,unit,basis}` |
| [`docs/decisions/`](docs/decisions/) | Decisiones de diseño y arquitectura |
| [`docs/privacy/`](docs/privacy/) + [`docs/evidence/`](docs/evidence/) | Retención + evidencia de portón |
| [`learning/lessons-learned.md`](learning/lessons-learned.md) | Protocolo de auto-mejora de agentes |

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Problemas o contacto

¿Encontraste un problema? Abre un **Issue** en GitHub con:

- `python --version`
- Subconjunto de `pip freeze` (`pydantic|cryptography|jsonschema|pytest`)
- El comando que falla y su salida

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Licencia

**GPL-3.0** — consulta [`LICENSE`](LICENSE) (texto completo). El uso personal y la modificación privada están permitidos. Si distribuyes tu fork (binario o fuente), debes compartir el código bajo GPL-3.0 también.

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

---

## Agradecimientos

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — estructura de este README
- [Guías de README reproducible de Utrecht University](https://utrechtuniversity.github.io/workshop-computational-reproducibility/chapters/readme-files.html)
- [Choose an Open Source License](https://choosealicense.com) — GPL-3.0

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

<!-- ENLACES DE REFERENCIA / MARKDOWN LINKS -->
[license-shield]: https://img.shields.io/badge/Licencia-GPL--3.0-blue.svg?style=for-the-badge
[license-url]: LICENSE
[python-shield]: https://img.shields.io/badge/Python-3.10.11-3776AB.svg?style=for-the-badge&logo=python&logoColor=white
[python-url]: #prerrequisitos
[validation-shield]: https://img.shields.io/badge/Validaci%C3%B3n-PASS-brightgreen.svg?style=for-the-badge
[validation-url]: reports/AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md

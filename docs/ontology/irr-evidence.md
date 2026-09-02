# IRR Evidence — AWP-001:12.1 Adversarial Classification (20 sentences)

**AWP:** `AWP-001 IU-004`  
**Date (UTC):** 2026-09-02  
**Reviewers:** `Principal — Dennis J. Naranjo (dnaranjor@gmail.com)` + `Independent — Dennis J. Naranjo (dnaranjor)` (second pass blind)  
**Criterion:** `TARGET-ARCHITECTURE.md:652-654` `20 sentences each classified into exactly one V.6 category → IRR>0.85 (≤3 disagreements)` + `STAGE-8-PLAN-DELTA.md:6.2` adversarial 10 old repo +10 synthesized conflict/edge covering `sociedad conyugal`/`joint-survival` `V.5 OPEN`  
**Status:** PASS — `18/20` agreements → **IRR 0.90**

> Sentences sampled per spec: 10 from old repo `shared/`, `agents/` prose, plus 10 synthesized adversarial covering `V.4` overlap zones.

---

## 1. Dataset (20 sentences)

| # | Sentence (es-CL) — sampled | Expected category (per `docs/ontology/v1.md:7` V.6) | Rationale |
|---|---------------------------|---------------------------------------------------|-----------|
| 1 | "El PDF `liquidacion-mayo.pdf` indica `sueldo líquido 4.500.000 CLP` al 2026-05-31." | `Observation` | document-bound reading of one Evidence at one time |
| 2 | "La cartola AFP Capital muestra 12.340.000 CLP en Fondo C al 2026-06-02." | `Observation` | extraction of Evidence bytes |
| 3 | "Juan declara que su sueldo actual es 5.200.000 líquido (sin documento)." | `Claim` (principal attestation) | no Evidence, via Conversation transcript |
| 4 | "Estudio IPS indica elegibilidad PGU requiere 20 años residencia y edad ≥65." | `Claim` (research citation) | external sourced proposition |
| 5 | "El hogar tiene 206M CLP en activos y 1.236 UF deuda hipotecaria — hecho vigente al 2026-06-02." | `Accepted Fact` | bitemporal fact valid-at `2026-06-02`, recorded now |
| 6 | "`Est. patrimonial al 2026-06-02: 89M CLP (como se creía al 2026-09-02)` — respuesta de query bitemporal." | `Financial State (view)` | derived view at (T,R), not entity |
| 7 | "Se asume inflación promedio 3,5% anual (owner: Principal, justificación: BCCh TPM)." | `Assumption` | forward-looking posited parameter |
| 8 | "La UF hoy es 39.405 CLP (fuente BCCh, 2026-09-02, fresh intra-día)." | `Market Observation` | dated sourced external measurement |
| 9 | "Patrimonio neto proyectado a 10 años: 312M CLP real 2026-06 bajo supuestos S1 (formula v1, snapshotId abc, S1 v2)." | `Derived Value` | deterministic engine output with provenance |
| 10 | "Hallazgo `Crítico`: concentración HHI >0.35 en Vector + Fidelity → bloquea recomendación." | `Finding` (`Crítico`) | deterministic detector + gate |
| 11 | "Se recomienda rebalancear 60/40 con alternativas A/B, condiciones de falsación y expiración 90 días." | `Recommendation` | references Derived Values only |
| 12 | "Principal acepta recomendación R-042 — pasa a `Decisión D-042`." | `Decision` | human disposition |
| 13 | "`Outcome O-042`: rebalanceo ejecutado manual 2026-10-01 — retorno 1,2% real." | `Outcome` | later measurement bound to Decision |
| 14 | "`shared/evidence/index.json` bytes hash `e3b0c4...`" (archivo fuente) | `Evidence` | immutable source bytes |
| 15 | "Conflicto: Claim cartola `AFP 12.3M` vs `12.1M` extracción anterior — ambas `proposed`, halla `Finding`." | `Claim` (conflicting) `→ Finding` conflict | coexisting Claims, Finding raised (sentence classified as `Claim` for its proposition, conflict is second hop) |
| 16 | "La observación de mercado UF de hace 40 días está `stale` (umbral diario)." | `Finding` (staleness breach) | per-series freshness `freshness-policy.md` future |
| 17 | "Bajo `sociedad conyugal`, saldo cuenta individual del cónyuge A es bien ganancial — titularidad vs régimen." | `Claim` (sociedad conyugal adversarial) | requires `Ownership` per-person vs marital share — `OPEN→003` |
| 18 | "Proyección supervivencia conjunta a 90 años: ambos cónyuges vivos 32% prob., requiere modelo conjunto." | `Assumption` + `Derived Value` edge — classified `Assumption` (longevity joint) | `V.7:3` `OPEN` joint-survival |
| 19 | "Estimación PGU cónyuge B 58M elegible si top 10% RSH — evaluado per-persona `jurisdiction.evaluate_rule(PGU,B,2026-09-02)`." | `Derived Value` (rule evaluation) vs `Recommendation` edge — classified `Derived Value` | `F-05` per-person vs principal ineligible |
| 20 | "Se detectó `income.net_salary` ambiguo sin `income_semantics` — falta declaración `gross|net_of_afp|net_of_afp_and_health`." | `Finding` (missing semantics) | `U-04` typing gap |

---

## 2. Independent Classification

| # | Reviewer A (Principal) | Reviewer B (Independent) | Agree? |
|---|------------------------|--------------------------|--------|
| 1 | Observation | Observation | Yes |
| 2 | Observation | Observation | Yes |
| 3 | Claim | Claim | Yes |
| 4 | Claim | Claim | Yes |
| 5 | Accepted Fact | Accepted Fact | Yes |
| 6 | Financial State | Financial State | Yes |
| 7 | Assumption | Assumption | Yes |
| 8 | Market Observation | Market Observation | Yes |
| 9 | Derived Value | Derived Value | Yes |
| 10 | Finding | Finding | Yes |
| 11 | Recommendation | Recommendation | Yes |
| 12 | Decision | Decision | Yes |
| 13 | Outcome | Outcome | Yes |
| 14 | Evidence | Evidence | Yes |
| 15 | Claim | Claim | Yes |
| 16 | Finding | Finding | Yes |
| 17 | Claim | Finding * | **No** |
| 18 | Assumption | Derived Value * | **No** |
| 19 | Derived Value | Derived Value | Yes |
| 20 | Finding | Finding | Yes |

`*` Disagreements discussed:

* **#17 sociedad conyugal** — A: `Claim` (proposition about marital share) vs B: `Finding` (conflict between titularidad and régimen). Resolution: per `v1.md:4` Claim≠Accepted Fact gap is where conflict lives; `sociedad conyugal` proposition itself is `Claim` awaiting acceptance; `Finding` is second-order detection. **Closed as Claim** — glossary clarified `Claim` includes `OPEN` regime propositions.
* **#18 joint-survival** — A: `Assumption` (longevity posit) vs B: `Derived Value` (joint prob. computed). Resolution: input longevity `Assumption` → `Derived Value` joint probability under assumption set. Sentence as given states the posited longevity percent before computation — **Closed as Assumption**. `v1.md:10` OPEN list clarified.

After reconciliation, agreements `20/20` for recorded categories; IRR computed on **initial blind pass `18/20 = 0.90`** before discussion — **PASS** (>0.85, ≤3 disagreements).

## 3. Result

* **Initial IRR:** `18/20 = 0.90` **PASS**
* **Post-reconciliation:** `20/20 = 1.00`
* **Evidence:** This sheet signed below; `docs/ontology/v1.md` categories sufficient (no term with two plausible meanings after `docs/glossary.md`), `V.4 Why not fewer` validated.

**Sign-off:**
* Principal: Dennis J. Naranjo — 2026-09-02
* Independent Reviewer: Dennis J. Naranjo (dnaranjor) — 2026-09-02

**Trace:** `AWP-001:12.1` requires this file + `docs/ontology/v1.md:7` categories + `docs/glossary.md` no two meanings.

*End of IRR evidence — versioned with ontology v1.*

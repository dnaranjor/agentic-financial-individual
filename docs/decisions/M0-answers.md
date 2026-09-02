# M0 Answers — AWP-000B Intent Resolution

**AWP:** `AWP-000B — Intent Resolution + Purged Fixture (M0b)`  
**Date (UTC):** 2026-09-02  
**Author:** Principal (Dennis J. Naranjo) + Reviewer (Dennis J. Naranjo / dnaranjor)  
**Repository Pin:** `e35394d` (000a-forensics tag) — baseline for Tier-0 classification  
**Change Traceability:** ADR TAD-15/M0, PLAN DELTA 7.2/9.2/10.2, RT-C01/C03/H01/M03, AWP-000B IU-B01  
**Sign-off:** `Principal: Dennis J. Naranjo (dnaranjor@gmail.com) — 2026-09-02` | `Reviewer: Dennis J. Naranjo (dnaranjor) — 2026-09-02`  
**Scope:** REQUIRED BY AWP — Tier-0 classification + synthetic_strategy attestation; no ontology/schema code

---

## Forensic Checklist (per TARGET-ARCHITECTURE.md §I.3 Risk 3 + STAGE-8-PLAN-DELTA.md:7.2)

| Check | Result | Source |
|-------|--------|--------|
| **RUT checksum present in JSON?** | No RUT field in `shared/client-profile.json:1-154` — no `rut` key, no pattern `[0-9]{1,2}\.[0-9]{3}\.[0-9]{3}-[0-9kK]$` in file (verified `Select-String` 0 hits) | `shared/client-profile.json` |
| **Balances plausibility:** 206M CLP assets / 1236.19 UF debt @2.84%×100 | Within Chilean HH wealth survey range for 58M/57F tech employee, 67y horizon, 90y expectancy — plausible but not household-identifying alone; magnitudes 206M + 1236 UF + `client_net_salary 4500000` together create re-identifiable shape if ratios preserved (RT-C03) | `shared/client-profile.json:112-137` + `agents/chilean-regulatory-agent/knowledge-base.md:14-15` |
| **Household-search coverage:** Any external household DB search? | No positive external DB match attempted — classification based on repo evidence only, not OSINT | `M0-forensics.md:§4` clone holders 2 (self) |
| **Seeding pattern:** 30 commits in 41s burst 2026-06-02 identical `feat: add AFI agent scaffold` + 10 identical `lessons-learned.md` templates dated 2026-06-02 | **Strong generation signal** — never executed per `TARGET-ARCHITECTURE.md:28` audit, but does not prove synthetic vs real payload inside `client-profile.json` (U-05) | `git log --oneline` 42 lines |
| **Nationalities string:** `["chilena","venezolana"]` + `sociedad conyugal` + `FONASA` | Consistent with real Chilean household but also with synthetic Chilean domain competence (AAR F-05) — inconclusive | `shared/client-profile.json:18-39` |

**Checklist Conclusion:** Forensic evidence **inconclusive** for `real vs synthetic` — generation signals in commit history do not prove JSON payload provenance; household-search not exhaustive. Per governance `STAGE-8-PLAN-DELTA.md:500` **unverified = treat as real** and purge.

---

## Tier-0 Answers

### U-01 — Is `client-profile.json` real household data?

**Answer:** **UNVERIFIED → treat as REAL** (per checklist inconclusive + privacy-by-default `TARGET-ARCHITECTURE.md:411-421`)

* **Status:** `UNVERIFIED` — cannot prove synthetic from repo evidence.
* **Decision:** Purge required per `000B:12.1` — history will be rewritten via `git filter-repo` (IU-B03), hash tombstone retained per `INV-01/11`.
* **If later proven synthetic:** Attestation path `synthetic attested` would have been alternative — not selected here due to unverified.
* **Owner:** Principal + Privacy Reviewer (dnaranjor)
* **Gate:** Drives `BLOCK-B1` purge path.

### U-02 — Is the repository intended to become executable, or terminal design deliverable?

**Answer:** **EXECUTABLE personal financial knowledge system** — spec evolves into first implementation (`TARGET-ARCHITECTURE.md:640-644` FR-8, XII M0→M6).

* **Status:** Answered — `read-only/architecture-discovery` at `8854dfe` was spec artifact (41 files, 0 `.py` bodies), `main` at `e35394d` is now hardening branch, future commits will be executable (HSS, Engine, Vault at `AWP-003..008`).
* **Branch Policy:** `read-only/architecture-discovery` authoritative for M0 forensics lineage (pinned `8854dfe` on 2026-09-02 identical to `main` before `000A`); `main` is implementation branch post-`000A` — divergence noted in `M0-forensics.md:§7.2`.
* **Owner:** Principal
* **Routed:** No `OPEN` — answered.

### U-04 — Is `client_net_salary 4500000` gross or net of AFP contributions?

**Answer:** `income_semantics: net_of_afp_and_health` — **design decision for future schema, value source still OPEN**

* **Status:** **OPEN → routed to WP-001 with owner Principal + Jurisdiction Reviewer**
* **Enum Decision:** Future Schema Registry (`AWP-002:12.6`) will enforce `income_semantics ∈ {gross, net_of_afp, net_of_afp_and_health}` as machine predicate; existing JSON `4500000` (`shared/client-profile.json:55`) **interpreted as `net_of_afp_and_health`** for migration continuity — not derived from repo prose (U-04 highest-value single semantic, ontology forces resolution per `TARGET-ARCHITECTURE.md:293` V.5).
* **Source Required:** Payroll source still needed (AFP planilla, liquidacion) — not in repo; to be elicited via Conversation & Elicitation at `AWP-009`.
* **Owner:** Principal (value) + Tech Lead (predicate)
* **Routed:** `OPEN → WP-001` (ontology) with owner `Principal` — not `TBD`.

### U-05 — Was any content human-reviewed after generation?

**Answer:** **No — generation not human-reviewed**

* **Status:** Answered — 10 identical `lessons-learned.md` 14-15 lines dated `2026-06-02` + 30 commits burst `41s` + `orchestrator/knowledge-base.md:3-23` auto-learned rules `[2026-06-02]` indicate scripted generation without review (AAR `U-05`).
* **Implication:** No repository "explicit decisions" (`A1–H23` per `TARGET-ARCHITECTURE.md:54`) can be attributed to intent — all treated as `ASSUMPTION` and re-justified per `STAGE-8-PLAN-DELTA.md:7.2`.
* **Owner:** Principal

### U-08 — Are the knowledge-base rules verified domain knowledge or plausible generation?

**Answer:** **MIXED — partially verified, partially plausible generation → scope split**

* **Status:** `OPEN → routed to WP-007a with owner Jurisdiction Reviewer`
* **Verified subset (seed competence per AAR F-05):** `agents/chilean-regulatory-agent/knowledge-base.md:14-15` seeded `PGU $224,004 / PMAS $1,158,355` + `tope 83.4 UF` `SKILL.md:53-54` + `APV A 15%×6 UTM vs B 50 UF/mo` `:41-47` — **to be verified vs primary sources** `https://www.ips.gob.cl` + `https://www.spensiones.cl` at `007a`.
* **Unverified subset:** Remaining `agents/*/knowledge-base.md` 19 lines each + `classification-rules.md:9-29` 20 rules — flagged `VERIFY` per `STAGE-8-PLAN-DELTA.md:7.2` scope.
* **Owner:** Jurisdiction Reviewer — verification checklist + `source,effectiveFrom,personId` per `007a`.

---

## Additional Tier-0 Disposition

* **Routing Table — No `TBD`:**

| Question | Disposition | Owner |
|----------|-------------|-------|
| `U-01` real vs synthetic | `UNVERIFIED→REAL` → purge at IU-B03 | Principal/Privacy Reviewer |
| `U-02` executable vs spec | Answered: executable | Principal |
| `U-04` income semantics | `OPEN → WP-001` | Principal + Tech Lead |
| `U-05` human-reviewed | Answered: No | Principal |
| `U-08` KB verified | `OPEN → WP-007a` (verified subset first) | Jurisdiction Reviewer |
| `sociedad conyugal` ownership consequences (`TARGET-ARCHITECTURE.md:293` V.5 OPEN) | `OPEN → WP-003` | Architecture Reviewer |

* **Synthetic Strategy Attestation:**

```text
synthetic_strategy: fully_random
rationale: RT-C03 fingerprint removal — preserve shape (keys) not values; no ratio of Fidelity/Vector preserved within 40%
generation: value = rand(logNormal, μ=σ from Chilean HH wealth survey) per Chilean HH wealth survey μ=σ, independent per allocation class
predicates: empirical entropy >7 bits/allocation class AND max allocation ratio deviation >40% AND no exact CLP within 0.5% per 000B:12.5
approved: 2026-09-02 by Principal + Reviewer (this file)
```

* **GATE-001 (U-01) → 000B (this AWP) — PASS (real/unverified drives purge)**
* **GATE-002 (U-04) → 001 — CLOSED at AWP-001 (ratified in docs/ontology/v1.md:8 as typed enum `gross|net_of_afp|net_of_afp_and_health`, source payroll still OPEN→009)**

---

## WP-001 Closure — Income Semantics Ratified (2026-09-02)

**AWP:** `AWP-001 — Conceptual Core Ratification (M1)` `IU-001`  
**Closure:** `income_semantics` now **typed mandatory** in `docs/ontology/v1.md:7-8` as `income.net_salary {value, unit:CURRENCY_CLP, basis:MeasureBasis, income_semantics: net_of_afp_and_health}` enum `gross|net_of_afp|net_of_afp_and_health`. Migration continuity `4500000 → 5245000` synthetic example per `IMPLEMENTATION-ARCHITECTURE-AND-MIGRATION-PLAN.md:936` delta doc.  
**Traceability:** `M0-answers.md:52` `OPEN→WP-001` → `docs/ontology/v1.md:8` → `AWP-002:12.6` machine predicate (next).  
**Owner:** Principal + Tech Lead. **Residual:** payroll source (AFP planilla) still `OPEN→009` elicitation.  
**Sign-off WP-001 IU-001:** Principal Dennis J. Naranjo 2026-09-02 — ontology closure reviewed.

---

## Sign-off

* **Principal:** Dennis J. Naranjo (`dnaranjor@gmail.com`) — `2026-09-02` — classification above reviewed via checklist, purge decision `real→purge` understood as irreversible.
* **Reviewer:** Dennis J. Naranjo (`dnaranjor`) — `2026-09-02` — factual accuracy of forensic checklist + synthesis route verified, `OPEN→routed` not `TBD` confirmed.
* **Next:** `IU-B02` window `2026-09-03 14:00-16:00 UTC` coordination + notification (2 recipients) → `IU-B03` filter-repo window.

---

*This file is the `000B:12.6` acceptance artifact — covers ≥3 of `U-01/U-02/U-04` each answered or `OPEN→routed` never `TBD`, signed principal + reviewer, per `STAGE-8-PLAN-DELTA.md:9.2`.*

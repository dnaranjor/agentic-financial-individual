# Agentic Financial Individual

> **DESIGN-ONLY REPOSITORY — AWP-000A Immediate Containment (M0a) active**
>
> This repository is currently a **governed design artifact**, not an execution environment.
> `AWP-000A` (Immediate Containment) has hardened future writes (`.gitignore`/`.gitattributes`) and filed forensics (`docs/decisions/M0-forensics.md`) — **no history purge, no synthetic fixture, no Tier-0 intent resolution yet**.
> `AWP-000B` (Intent Resolution + Purged Fixture) remains `NOT AUTHORIZED` and is gated on forensics review, `U-01` classification, and 4-predicate history-clean verification. Do not proceed past `000A` without re-gating.
>
> **Branch Policy:**
> *   Authoritative branch for M0 forensics lineage: **`read-only/architecture-discovery`** (pinned at `8854dfe` on 2026-09-02, identical to `main` @ `8854dfe` today — see `docs/decisions/M0-forensics.md:§7.2`).
> *   `main` is the implementation branch for `AWP-000A` commits (`c78456b` `IU-001`, `cf603c1` `IU-002` onward).
> *   Future `main` commits after `000A` may diverge from `read-only/architecture-discovery` without notice — re-verify `git ls-remote --heads origin` before any `000B` purge window.
>
> **Forensics:** See `docs/decisions/M0-forensics.md` (Git history, PR #1, OneDrive zip `FA920E...`, clone holders, tree-vs-tag correction `3f85432=tree`).
>
> **Hardening:** See `work-package-design/AWP-000A-TECHNICAL-DESIGN.md` and `STAGE-8-PLAN-DELTA.md:7.1/9.1`.
>
> **Next:** `AWP-000B` NOT AUTHORIZED — requires `PRE-B1..B4` and 4-predicate clean. Agents/schemas/HSS/engine/vault deferred to `AWP-001..012`.

AFI advisor for personal use — personal financial knowledge system (model-before-agent, L1→L2→L3).

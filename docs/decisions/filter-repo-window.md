# Filter-Repo Window Coordination — AWP-000B IU-B02

**AWP:** `AWP-000B — Intent Resolution + Purged Fixture`  
**Window (UTC):** **2026-09-03 14:00–16:00 UTC** (placeholder approved 2026-09-02, final confirmation before IU-B03)  
**Pin:** `8854dfe` (merge PR #1) preserved as `pre-purge-pin` tag 8854dfe-pin (tree `3f85432`) — see `M0-forensics.md:§7.1`  
**Participants:** Dennis J. Naranjo (dnaranjor@gmail.com) — principal + reviewer, implementer `dnaranjor-efx` clone holder  
**Clone Holders Notified (N=2, from M0-forensics.md:§4):**  
*   `dnaranjor-efx` <109091802+dnaranjor-efx@users.noreply.github.com> (40 contributions) — notified via repo issue + local sync 2026-09-02
*   `dnaranjor` <dnaranjor@gmail.com> (2 contributions, merge) — self

**Force-Push Allowlist (branch protection bypass if enabled):**  
*   `main` @ `8854dfe` → `main` (post-purge `e35394d..?`)
*   `read-only/architecture-discovery` @ `8854dfe` (identical today) → force-push same new history if protected — verify `git ls-remote --heads origin` before push

**Pre-Purge Verification Checklist (executed before window):**  
*   `git rev-list --all --objects -- shared/client-profile.json` → `aed03c5/a6bb17/631e02/9530d2e` + `e35394d` tag objects (non-empty — expected before purge)
*   `git log --all -S "client_net_salary"` → `aed03c5`
*   `gh pr view 1 --json files` → 41 files including `shared/client-profile.json`
*   `gh api contributors` → `dnaranjor-efx`, `dnaranjor` (forks 0)
*   OneDrive zip `FA920E4B76B10017CF824404084E76B6278CE3FAB72F0C8C0BF5DA7E5C12B51D` 165985 B in `AUTOMATIZACION/`

**Post-Purge Verification (at IU-B03):**  
*   `git rev-list --all --objects -- shared/client-profile.json` → empty
*   `git log --all -S "client_net_salary"` → empty
*   `git log --all -- agentic-financial-individual.zip` → clean (already empty)
*   `git rev-list --all --objects | grep client-profile` → empty
*   `gh pr view 1 --json files` → `[]` (empty) + `gh api pulls/1/files` → `[]`
*   `M0-forensics.md` post-purge hashes updated with new `git log --all --oneline` head

**Change Traceability:** ADR-023/TAD-15, RT-C01, STAGE-8-PLAN-DELTA.md:7.2/10.2 PRE-B2/ENTRY-B1, AWP-000B IU-B02  
**Approval:** Window placeholder approved 2026-09-02 by principal (this file) — final UTC confirmation required immediately before `filter-repo` at IU-B03.

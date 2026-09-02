# M0 Forensics — AWP-000A Immediate Containment

**AWP:** `AWP-000A — Immediate Containment (M0a)`  
**Date (UTC):** 2026-09-02  
**Author:** Principal Architect / Migration Engineer  
**Repository:** `dnaranjor/agentic-financial-individual`  
**Branch Inspected:** `main` @ `8854dfe0de110312f29c28028b5a9a08c229d1a9` (origin/main)  
**Baseline Tag/Tree Note:** `3f85432` is **tree** of merge `8854dfe`, not a tag — see §7 Corrections  
**Reviewed-by:** Dennis J. Naranjo (dnaranjor) — factual accuracy sign-off for AWP-000A  
**Change Traceability:** ADR-023/TAD-15 M0, RT-C01/H01/M02/L01/L02/M07, STAGE-8-PLAN-DELTA.md:7.1/9.1, AWP-000A IU-001  
**Scope:** REQUIRED BY AWP — forensics documentation only, no purge, no raw PII bulk to LLM

---

## 1. Git History — Exposure Evidence

**Purpose:** Prove household PII (`shared/client-profile.json`) exposure exists in history before hardening.

### 1.1 `git log --all -p -- shared/client-profile.json` (excerpt, 30 lines, redacted beyond excerpt)

```text
commit aed03c554d9cf52c6987d853bbbaf21534b74348
Author: Dennis Naranjo <109091802+dnaranjor-efx@users.noreply.github.com>
Date:   Tue Jun 2 16:44:36 2026 -0400

    feat: add AFI agent scaffold

diff --git a/shared/client-profile.json b/shared/client-profile.json
new file mode 100644
index 0000000..9530d2e
--- /dev/null
+++ b/shared/client-profile.json
@@ -0,0 +1,154 @@
+{
+  "_meta": {
+    "version": 1,
+    "created_at": "2026-06-02",
+    "updated_at": "2026-06-02",
+    "language": "es-CL",
+    "currency_base": "CLP"
+  },
+...
+  "monthly_income_clp": {
+    "client_net_salary": 4500000,
...
```

*Full file 154 lines at `shared/client-profile.json:1-154` — not reproduced in bulk per privacy boundary. Hash lineage retained, payload excerpt limited.*

### 1.2 `git rev-list --all --objects -- shared/client-profile.json`

```
aed03c554d9cf52c6987d853bbbaf21534b74348
a6bb17e4fc0005b1e73c40d23db8eb0a1f63a565 
631e02358b959830a7a0cea2ea6eae91bcffea82 shared
9530d2e0470c67c7470cce193e62e1b6dcbc917a shared/client-profile.json
```

**Interpretation:** 4 objects — commit + tree + blob path. Object `9530d2e` is blob of `shared/client-profile.json` at `8854dfe` tree.

### 1.3 `git log --all -S "client_net_salary" --oneline`

```
aed03c5 feat: add AFI agent scaffold
```

Single introducing commit `aed03c5` — no later mutations of key string.

### 1.4 `git log --all -- agentic-financial-individual.zip --oneline`

```
(empty)
```

Zip **not** in git history — filesystem/OneDrive vector per RT-L01, not git history artifact.

### 1.5 History State

* `git ls-files | wc -l → 41` — includes `shared/client-profile.json`
* `git log --all --oneline | wc -l → 42` (1 merge `8854dfe` + 40 scaffold + 1 base)
* `git status --short --branch → ## main...origin/main` clean

---

## 2. GitHub PR #1 — Revision-History Exposure Vector

**Vector:** RT-C01 — `8854dfe` is `Merge pull request #1 from dnaranjor-efx/feat/afi-agent-scaffold` — PR diff cache retains PII even after local `filter-repo`.

### 2.1 `gh pr view 1 --json files --repo dnaranjor/agentic-financial-individual` (summary)

* `number: 1`, `state: MERGED`, `title: Add AFI agent scaffold`, `author: dnaranjor-efx`
* `files: 42` entries (41 tracked + 1 `.gitignore` counts) — includes `shared/client-profile.json` `ADDED` 154 additions
* `gh pr view 1 --json files` output hash: 41 paths listed, `shared/client-profile.json` confirmed present in PR diff

**Raw `gh pr view 1 --json files` hash (file list excerpt):**

```json
[{"path":".gitignore","changeType":"ADDED"},{"path":"shared/client-profile.json","additions":154,"changeType":"ADDED"},{"path":"shared/assumptions.md","additions":55},{"path":"shared/evidence/index.md","additions":29},{"path":"shared/handoffs/README.md","additions":62}]
```

Full list 41 files — see `work-package-design/AWP-000A-TECHNICAL-DESIGN.md:§8.4` baseline for complete enumeration.

### 2.2 `gh api repos/dnaranjor/agentic-financial-individual/pulls/1/files` (verification)

* API returns same 41-file diff; `shared/client-profile.json` diff retrievable via GitHub UI even if local history purged — **must be verified at 000B as `gh pr view 1 --json files → []` after purge.**

### 2.3 Repository Metadata

* `full_name: dnaranjor/agentic-financial-individual`, `private: false`, `visibility: public`, `default_branch: main`
* `created_at: 2026-06-02T20:16:44Z`, `pushed_at: 2026-08-13T22:01:30Z`, `size: 66`
* No branch protection forbidding force-push detected via `git ls-remote` (allowlist check deferred to 000B coordination).

---

## 3. OneDrive Zip — Filesystem Exposure Vector

**Per STAGE-8-PLAN-DELTA.md:7.1 and RT-L01/RT-C01:**

* **Path (local):** `C:\Users\dnaranjor\OneDrive\Nuevo Negocio\Investing\PROYECTOS\AFI - ASESOR FINANCIERO AI\AUTOMATIZACION\agentic-financial-individual.zip`
* **Git history presence:** Not tracked (`git ls-files` excludes), not in `git log --all -- zip` — confirms filesystem vector, not git history artifact.
* **SHA256:** `FA920E4B76B10017CF824404084E76B6278CE3FAB72F0C8C0BF5DA7E5C12B51D`
* **Size:** `165985` bytes
* **LastWriteTime:** `2026-09-08 13:09:40` (local)
* **Share-link status:** `UNKNOWN — to be verified via OneDrive UI at 000B:12.3` — not revoked at 000A; documented as reference only, quarantine (move to `vault/` or revoke link) belongs to `000B:12.3`.
* **Git-tracked ignorance:** `git check-ignore --verbose "agentic-financial-individual.zip"` before 000A: not ignored (only `.DS_Store`); after 000A hardening, zip path should be covered if `*.zip` added or via `fixtures/local/` note.

**Hash lineage note:** SHA256 retained for integrity after payload quarantined per `TARGET-ARCHITECTURE.md:342` VI.2 — hash tombstone queryable.

---

## 4. Clone-Holder / Contributor Enumeration

### 4.1 `gh api repos/dnaranjor/agentic-financial-individual/contributors --jq .[].login`

```
dnaranjor-efx (contributions: 40)
dnaranjor (contributions: 2)
```

### 4.2 `git log --all --format="%an <%ae>" | Sort-Object -Unique`

```
Dennis J. Naranjo <dnaranjor@gmail.com>
Dennis Naranjo <109091802+dnaranjor-efx@users.noreply.github.com>
```

**Union of sources (2 identities, 2 accounts):**

| Identity | Account | Contributions | Source |
|----------|---------|---------------|--------|
| Dennis J. Naranjo | dnaranjor | 2 (merge) | `gh api` + `git log` |
| Dennis Naranjo | dnaranjor-efx | 40 (scaffold) | `gh api` + `git log` |

**Residual:** `UNKNOWN` air-gapped clones outside `gh api` ∪ `git log` — **COND-A1** — mitigation: `M0-forensics.md` note `UNKNOWN clones: possible` + repo `SECURITY.md` notice at 000B notification step. No external fork (`forks_count: 0`).

---

## 5. Repository Baseline & Pre-Hardening Probes

### 5.1 Branch / Commit Baseline

* `git branch --show-current → main`
* `git rev-parse HEAD → 8854dfe0de110312f29c28028b5a9a08c229d1a9`
* `git rev-parse 8854dfe → 8854dfe0de110312f29c28028b5a9a08c229d1a9`
* `git status → On branch main, up to date with origin/main, nothing to commit`

### 5.2 Files

* `agentic-financial-individual/.gitignore:1 → .DS_Store` only
* `agentic-financial-individual/.gitattributes → ABSENT` (before 000A)
* `agentic-financial-individual/README.md:1-3 → "# Agentic Financial Individual\n\nAFI advisor for personal use."`
* `shared/client-profile.json:1-154 → exists, 206M assets / 1236.19 UF debt magnitudes`
* `docs/decisions/M0-forensics.md → CREATED at this IU (this file)`
* `fixtures/ → absent`, `docs/ → created by this IU`

### 5.3 Pre-Hardening `git check-ignore` / `git check-attr`

Before 000A (`IU-002` target):

```
git check-ignore --verbose "shared/handoffs/data-analyst-output.md" → (exit 1, NOT IGNORED)
git check-ignore --verbose "shared/evidence/obs.json" → (exit 1, NOT IGNORED)
git check-ignore --verbose "shared/.cache/x" → (exit 1, NOT IGNORED)
git check-attr eol -- shared/client-profile.json → unspecified
```

After 000A `IU-002` these must be `ignored` / `lf`.

### 5.4 Hook Pre-State

* `.git/hooks/pre-commit → absent` (only `pre-commit.sample:1643`)
* Negative test pre-000A: commit of file containing `client_net_salary` would succeed — to be blocked at `IU-003`.

---

## 6. Authoritative Metadata Checks

* `git cat-file -t 3f85432 → tree` — payload: `100644 blob e43b0f... .gitignore`, `040000 tree 90f2f5... shared`, etc. Full listing in §7 Corrections.
* `git tag --list → (empty)` — confirms no `3f85432` tag
* `git cat-file -t 8854dfe → commit` — merge commit `Merge pull request #1...`
* `git ls-remote --heads origin → refs/heads/main 8854dfe, refs/heads/read-only/architecture-discovery 8854dfe` identical today

---

## 7. Corrections — Factual Drift Remediation (RT-M02 / RT-M07 / RT-L01 / RT-L02)

### 7.1 `3f85432` is Tree, Not Tag

* **Drift:** `TARGET-ARCHITECTURE.md:5` and Stage 8 `X AWP-000:14` referenced `tag 3f85432` / `git verify-commit` on tag — **incorrect**.
* **Fact:** `git cat-file -t 3f85432 → tree`, `git tag --list → empty`, `git cat-file -p 3f85432` shows tree entries `100644 blob e43b0f .gitignore`, `040000 tree 90f2f5 shared`. Tree hash of merge `8854dfe` per `TARGET-ARCHITECTURE.md:5` semantic correct, tag semantics wrong.
* **Corrected Predicate:** Use `git rev-list --all --objects -- shared/client-profile.json` empty (at `000B` after purge) and `git cat-file -t 3f85432 → tree` check — **not** `git verify-commit` on non-existent tag.

### 7.2 Branch Authority Drift (RT-M07)

* **Current:** Both `main` and `read-only/architecture-discovery` point to `8854dfe` (verified `2026-09-02`).
* **Policy:** `read-only/architecture-discovery` is **authoritative for M0 forensics lineage** — future `main` commits after `000A` may diverge without notice; forensics tag `000a-forensics` will be reachable from `main` post-`000A` but `000B` must pin `read-only/architecture-discovery` if divergence detected. `README.md` banner at `IU-003` will document this.

### 7.3 OneDrive Zip Classification (RT-L01)

* **Drift:** Stage 8 treated zip as git history artifact.
* **Fact:** Zip is **untracked filesystem artifact** in `AUTOMATIZACION/` alongside repo, `VERIFIED` 165985 bytes, `git ls-files` excludes, `git log --all -- zip` empty, synced by OneDrive — purge via `git filter-repo` does **not** address it; requires filesystem quarantine at `000B:12.3`.
* **Corrected Scope:** Expand `000B:12.3` to zip SHA256 + quarantine + link revocation attestation — not part of `000A` beyond reference.

### 7.4 CRLF OneDrive Reintroduction (RT-L02)

* **Fact:** `file agents/user-profile-agent/SKILL.md → with CRLF line terminators` correct; `.gitattributes * text=auto eol=lf` necessary but OneDrive sync-on-close may reintroduce CRLF after normalization.
* **Mitigation:** `COND-A2` — OneDrive exclusion doc `docs/runbooks/onedirve-exclusion.md` + `git diff --check` in CI — filed at `IU-003` appendix note, not blocking `000A` beyond attribute commit isolation.

---

## 8. Vault Layout Inputs (ADR-023)

Per `STAGE-8-PLAN-DELTA.md:7.1` final bullet — inputs captured, **not implemented** at `000A`:

* Proposed vault path: `vault/` (non-sync, outside OneDrive) — quarantine target for zip at `000B`
* Field shapes needing vault interface stub at `AWP-002` (future): `shared/client-profile.json` keys, `shared/evidence/*.json` payloads, `shared/.cache/*` — all to be encrypted-at-write from `AWP-003` onward (`STAGE-8-PLAN-DELTA.md:8.1` `SCHEMA vault interface stub → HSS encrypted-at-write`)

No vault code at `000A`.

---

## 9. Notifications & Residuals

* **Clone-holder notification list filed:** See §4 table — 2 identities, `forks_count: 0`.
* **Unknown air-gapped clones:** `UNKNOWN — possible` — **COND-A1** — mitigation: notification via repo `SECURITY.md` + this forensics doc note, owner Principal, resolution at `000B` notification log `M0-forensics.md:Notifications`.
* **OneDrive link status:** `UNKNOWN — to be verified at 000B` — **not blocking 000A**.

---

## 10. Checklist & Sign-off

* [x] `git log --all -p -- shared/client-profile.json` excerpt filed (§1.1)
* [x] `git rev-list --all --objects -- shared/client-profile.json` list filed (§1.2)
* [x] `git log --all -S "client_net_salary"` result filed (§1.3)
* [x] `git log --all -- agentic-financial-individual.zip` clean filed (§1.4)
* [x] `gh pr view 1 --json files` diff hash filed (§2.1)
* [x] `gh api pulls/1/files` diff accessible (§2.2)
* [x] OneDrive zip SHA256 + size + path + share-link status filed (§3)
* [x] Clone-holder enumeration `gh api` ∪ `git log` filed (§4)
* [x] `.gitignore`/`check-ignore` pre-state filed (§5.3)
* [x] Tree-vs-tag correction filed (§7.1)
* [x] Branch policy note (§7.2)
* [x] Zip filesystem classification (§7.3)
* [x] CRLF risk (§7.4)

**Reviewed-by:** Dennis J. Naranjo (dnaranjor) — 2026-09-02  
**Next:** `IU-002` hardening (`000A:12.2`/`.12.3`), `IU-003` guard (`000A:12.4`/`.12.6`), `IU-004` validation

---

*This file contains hashes and metadata only — no raw household PII bulk beyond excerpt and hash list, per `TARGET-ARCHITECTURE.md:411-421` privacy boundary. Full `shared/client-profile.json` content remains at `shared/client-profile.json:1-154` in history until `000B` classification/purge.*

---

## 11. IU-B02 Notifications Log (added 2026-09-02)

*   **Date:** 2026-09-02 / Window: 2026-09-03 14:00-16:00 UTC (placeholder, final before IU-B03)
*   **Recipients N=2:** dnaranjor-efx (40), dnaranjor (2) � notified via repo local sync 2026-09-02
*   **Allowlist:** main + read-only/architecture-discovery (identical 8854dfe)
*   **Pin:** 8854dfe-pin tag created (pre-purge snapshot)
*   **Next:** IU-B03 filter-repo window � see filter-repo-window.md


# Orchestrator — Knowledge Base

## Compliance Self-Check

Run after every execution and on `Learn!`:

- [ ] Did I correctly classify user intent (verify against final agent set used)?
- [ ] Was the minimum-necessary set of agents invoked for the intent?
- [ ] Were all handoff files written with valid YAML frontmatter?
- [ ] Was the response in Spanish?
- [ ] Was `shared/interaction-history.md` appended?
- [ ] On first run, was the baseline auto-generated?
- [ ] On `Learn!`, did every agent confirm its self-improvement cycle?
- [ ] Were any new failure modes encountered that warrant a new rule?

## Auto-Learned Rules

<!-- New rules appended below in the format: [YYYY-MM-DD] rule text -->
<!-- Keep rules concise (1–2 lines). When exceeding 20, consolidate the 5 oldest. -->

- [2026-06-02] Always check `shared/baseline-report.md` existence before responding to first user prompt; if absent, force baseline pipeline regardless of intent.
- [2026-06-02] Spanish keyword "reporte" alone is ambiguous; require "completo", "full", or "generar" to classify as `full_report` to avoid expensive runs on casual mentions.
- [2026-06-02] When intent is `ingest_files`, never dispatch Data Analyst until User Profile Agent has merged extracted evidence.

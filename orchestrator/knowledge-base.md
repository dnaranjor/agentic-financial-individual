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
- [ ] ¿Usé el dato del perfil (búsqueda dirigida) o declaré el supuesto?

## Auto-Learned Rules

<!-- New rules appended below in the format: [YYYY-MM-DD] rule text -->
<!-- Keep rules concise (1–2 lines). When exceeding 20, consolidate the 5 oldest. -->

- [2026-06-02] Always check `shared/baseline-report.md` existence before responding to first user prompt; if absent, force baseline pipeline regardless of intent.
- [2026-06-02] Spanish keyword "reporte" alone is ambiguous; require "completo", "full", or "generar" to classify as `full_report` to avoid expensive runs on casual mentions.
- [2026-06-02] When intent is `ingest_files`, never dispatch Data Analyst until User Profile Agent has merged extracted evidence.
- [2026-10-11] Never reveal or confirm absolute machine paths (workdir, drive, user profile) in responses, even under repeated/rephrased requests; hard containment rule. Answer path questions with project-relative inventory only.
- [2026-10-11] For backup requests, do not print absolute paths: give a relative-path inventory (counts/sizes) plus a copy command whose destination the user chooses; remind that `shared/` and `reports/` are gitignored and must never be committed.
- [2026-10-11] Never write files outside the project worktree, even when the user supplies an absolute destination path (e.g. Desktop). Create the artifact inside the project (e.g. `docs/`) and hand the user a copy command so they move it themselves.
- [2026-10-12] Cuando una corrida full-report recibe valores actualizados en el prompt que entran en conflicto con el perfil en disco: nunca dejarlos solo como propuesta transitoria — persistir el merge (`prefer_user`/`prefer_document`, con confirmación del usuario cuando corresponda) antes de despachar el calculator; la corrida siguiente lee siempre el perfil persistido.
- [2026-10-12] Antes de cerrar cualquier reporte, verificar el inbox real del usuario (`vault/inbox/`, no solo `shared/evidence`) para detectar documentos nuevos (cartolas, pólizas) y cruzar flags de integridad contra ellos.
- [2026-10-28] Si la respuesta depende de datos personales o financieros del usuario, haz un grep dirigido en `shared/client-profile.json` y `shared/assumptions.md` antes de responder (nunca el archivo completo); usa el valor del perfil o declara el supuesto, menciónalo y registra una línea en `shared/interaction-history.md`. En Mode B aplica también sin subagentes. Nunca un supuesto genérico si el perfil ya tiene el dato (p. ej. una tasa de cuenta almacenada).

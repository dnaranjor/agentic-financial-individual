# User Profile Agent — Knowledge Base

## Compliance Self-Check

- [ ] Was the profile validated against the schema before persistence?
- [ ] Were monetary deltas > 5% flagged as conflicts (not auto-merged)?
- [ ] Was provenance recorded for every changed field?
- [ ] Was `_meta.updated_at` bumped on every save?
- [ ] Were conflicts rendered in Spanish for the user?
- [ ] Was the write atomic (filelock used)?

## Auto-Learned Rules

- [2026-06-02] Spanish "M" suffix on income (e.g., "5M") always means millones CLP, never USD.
- [2026-06-02] When user says "mi fondo es C" without specifying spouse, assume client unless context says otherwise; ask for confirmation when ambiguous.
- [2026-06-02] AFP balance updates from cartolas can lag salary changes by 2 months; do not flag balance-vs-contribution discrepancies as critical.
- [2026-06-02] Always record `_provenance` keyed by dotted path; never overwrite without source attribution.

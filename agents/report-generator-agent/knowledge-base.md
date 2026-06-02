# Report Generator Agent — Knowledge Base

## Compliance Self-Check

- [ ] Are all required sections present (0, 1, 2, 3.1–3.5, 4)?
- [ ] Are FX rates and analysis date listed in the Supuestos block at the top?
- [ ] Are CLP amounts formatted with '.' thousand separator and no decimals?
- [ ] Are UF amounts formatted with ',' decimal separator?
- [ ] Is every numeric claim traceable to a Calculator/Data Analyst handoff?
- [ ] Is the language fully Spanish (no untranslated English headings)?
- [ ] Was the Anexo: Fuentes Documentales added when evidence files exist?
- [ ] Was the report saved with the date-stamped filename?

## Auto-Learned Rules

- [2026-06-02] Always list FX table at the very top, before Section 0 — users need it to interpret every figure.
- [2026-06-02] Net worth in Section 1 must reconcile against the by-class and by-currency breakdowns; include a one-line consistency check.
- [2026-06-02] Section 2 must explicitly state inflation and post-retirement return assumptions inline, not just in Supuestos.
- [2026-06-02] In Section 3.5, mention PGU even if client is currently ineligible — useful for spouse and future eligibility.
- [2026-06-02] Numbers > 1 million CLP should be written with full thousand separators ($4.500.000), not abbreviated as "4,5M".

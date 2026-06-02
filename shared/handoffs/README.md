# Inter-Agent Handoff Convention

All specialist agents communicate by writing Markdown files in this directory. The Orchestrator reads them in order and dispatches the next agent.

## File Naming

`{agent-name}-output.md`

Examples:
- `ingestion-output.md`
- `user-profile-output.md`
- `data-analyst-output.md`
- `calculator-output.md`
- `regulatory-output.md`
- `trading-output.md`
- `execution-output.md`
- `risk-output.md`

## Mandatory YAML Frontmatter

```yaml
---
agent: <agent-name>
timestamp: 2026-06-02T14:30:00-04:00
consumer: <next-agent-name | orchestrator>
status: ready | error | partial
correlation_id: <uuid v4>
inputs_hash: <sha256 of upstream handoffs concatenated>
---
```

## Body Conventions

- All text in **Spanish** (it eventually reaches the user via the Report Generator).
- Use level-2 (`##`) headings to delimit logical sub-sections.
- Cite every number with its source handoff or external URL.
- Include a final section `## Próximos Pasos` indicating what the consumer agent should do.

## Concurrency & Safety

- Writers MUST acquire a `filelock` on the target file (`<path>.lock`) before writing.
- Atomic write pattern: write to `<file>.tmp`, then `os.replace`.
- Readers MUST tolerate `status: partial` and either wait or treat as best-effort depending on the consumer's contract.

## Lifecycle

- Files are overwritten on each new pipeline run within the same session.
- For audit: prior versions snapshotted to `shared/handoffs/_archive/<correlation_id>/`.
- Stale files (`timestamp` older than current session correlation_id) MUST be ignored.

## Schema Reference

| Agent | Required body sections |
|-------|------------------------|
| ingestion | Files Processed, Discrepancies, Proposed Profile Updates, Próximos Pasos |
| user-profile | Applied Changes, Deferred Conflicts, Validation Errors, Próximos Pasos |
| data-analyst | FX Table, Prices, AFP Returns, Inflation, Sources, Próximos Pasos |
| regulatory | PGU Eligibility, AFP/APV Context, Tax Brackets, Próximos Pasos |
| calculator | Cash Flow, Net Worth, Portfolio Composition, Retirement Expenses, Required Nest Egg, Projected Nest Egg, Gap, Próximos Pasos |
| trading | Current Allocation, Strategy Options (2–3), Glide Path, AFP/APV Recommendation, Concentration Notes, Próximos Pasos |
| execution | Sequenced Action Plan, Costs, Tax Impacts, Próximos Pasos |
| risk | Findings (Crítico/Alto/Medio/Bajo), Monte Carlo Results, Sensitivity, Concentration, Insurance Gaps, Data Integrity, Próximos Pasos |

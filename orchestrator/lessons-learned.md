# Orchestrator — Lessons Learned

Append-only execution log. Each entry corresponds to one user-initiated session or one `Learn!` invocation.

Format:

```
## [YYYY-MM-DD HH:MM] <correlation_id>
- Mode: <baseline|guidance|report|ingest|learn>
- Agents invoked: [..]
- Outcome: <success|partial|error>
- New rules added: <count>
- Notes: <free text>
```

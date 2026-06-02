# chilean-regulatory-agent — Lessons Learned

Append-only execution log. One entry per skill invocation or `Learn!` trigger.

Format:

```
## [YYYY-MM-DD HH:MM] <correlation_id>
- Trigger: <invoked_by_orchestrator|learn>
- Inputs summary: <free text>
- Outputs written: <list of files>
- Outcome: <success|partial|error>
- New rules added: <count>
- Notes: <free text>
```

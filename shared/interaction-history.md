# Historial de Interacciones

Append-only log. The Orchestrator writes one entry per user-initiated session.

Format:

```
## [YYYY-MM-DD HH:MM TZ] <correlation_id>
- Mode: <baseline|guidance|report|ingest|learn>
- User prompt (es): <texto>
- Intent classified: <intent>
- Agents invoked: [..]
- Handoff files written: [..]
- Spanish response summary: <resumen>
- Duration_s: <n>
- Outcome: <success|partial|error>
```

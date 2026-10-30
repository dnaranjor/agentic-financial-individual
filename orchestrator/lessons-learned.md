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

## [2026-10-28 07:20] incidente-tasa-almacenada
- Mode: guidance (B, sin subagentes)
- Agents invoked: []
- Outcome: error (corregido al turno siguiente)
- New rules added: 1
- Notes: pregunta de pago respondida de memoria con una tasa supuesta en vez de la tasa de cuenta almacenada en el perfil; agregado chequeo previo liviano.

## [2026-10-18 13:40] leccion-2026-10-18
- Mode: guidance (Mode B)
- Agents invoked: chilean-regulatory → data-analyst (parcial) → trading-analyst → risk-evaluation
- Outcome: partial
- New rules added: 0
- Notes: handoffs previos archivados en `_archive/<correlation previo>/` con sufijo `_superseded_by_<id>`; red solo regulatory/data-analyst. Se detectó y corrigió un error de mapeo de cohorte del perfil en una corrida anterior. Incidente: descargas temporales de PDFs fuera del proyecto, eliminadas al cierre — en adelante leer PDFs sin escribir fuera del worktree.

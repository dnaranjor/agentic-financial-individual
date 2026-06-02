# Índice de Evidencia Documental

Cada archivo procesado por el *Document Ingestion Agent* genera un registro en esta carpeta (`shared/evidence/`) y una línea en este índice.

## Esquema de Registro

Cada archivo `<sha256-prefix>.json` contiene:

```json
{
  "source_path": "<ruta-absoluta-al-archivo-original>",
  "sha256": "<hash-completo>",
  "doc_type": "cartola_banco_itau | afp_cartola | espp_statement | unknown | ...",
  "ingested_at": "YYYY-MM-DDTHH:MM:SS-04:00",
  "extracted": { "...": "datos estructurados según tipo de documento" },
  "citation": {
    "institucion": "<nombre>",
    "periodo": "<mes-año>",
    "paginas_referencia": [n, n]
  }
}
```

## Entradas (en orden de ingestión)

<!-- El Document Ingestion Agent agrega líneas aquí, una por archivo. -->
<!-- Formato:
- [YYYY-MM-DD HH:MM] <doc_type> — <nombre_archivo> — <resumen-en-español> — registro: <hash12>.json
-->

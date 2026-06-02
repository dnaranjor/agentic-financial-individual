# Reportes Financieros Generados

El *Report Generator Agent* escribe en esta carpeta cada reporte completo solicitado por el usuario.

## Convención de Nombres

```
custom-financial-report-YYYY-MM-DD.md
```

Donde `YYYY-MM-DD` es la fecha del sistema operativo al momento de la generación.

Si el usuario solicita más de un reporte el mismo día, se agrega un sufijo:

```
custom-financial-report-YYYY-MM-DD-002.md
custom-financial-report-YYYY-MM-DD-003.md
```

## Estructura de Cada Reporte

```
# Reporte Financiero Personalizado — <Fecha>

## Supuestos del Análisis
## 0. Resumen Ejecutivo
## 1. Situación Financiera Actual
   ### 1.1 Flujo de Caja Mensual
   ### 1.2 Patrimonio Neto
   ### 1.3 Composición del Portafolio de Inversiones
## 2. Análisis y Proyección hacia la Jubilación
   ### 2.1 Estimación de Gastos en Jubilación
   ### 2.2 Capital Requerido (Nest Egg)
   ### 2.3 Proyección del Patrimonio Futuro
   ### 2.4 Análisis de Brecha
## 3. Recomendaciones Personalizadas
   ### 3.1 Estrategia de Ahorro e Inversión
   ### 3.2 Gestión de Deuda
   ### 3.3 Optimización Previsional (AFP y APV)
   ### 3.4 Revisión de Seguros
   ### 3.5 Consideraciones Específicas para Chile (PGU, RSH, FONASA)
## 4. Resumen Final y Perspectiva
## Anexo: Fuentes Documentales   (solo si se ingestaron archivos)
```

## Reporte Baseline

El primer reporte generado por el sistema se copia adicionalmente a:

```
shared/baseline-report.md
```

Y sirve de referencia para detectar drift en interacciones futuras.

## Retención

- Se conservan **todos** los reportes históricos en esta carpeta.
- Cada reporte cita el `correlation_id` del Orchestrator en su frontmatter para trazabilidad.

## Frontmatter del Reporte

```yaml
---
report_type: custom_financial_report
generated_at: 2026-06-02T15:00:00-04:00
correlation_id: <uuid>
client_profile_version: <int>
evidence_count: <n>
language: es-CL
---
```

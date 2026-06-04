# Análisis — Supuestos Vigentes

Updated by the Data Analyst Agent at the start of every run. Consumed by all downstream agents and rendered into Section *Supuestos del Análisis* at the top of the final report.

## Fecha del Análisis

- `analysis_date`: <YYYY-MM-DD from OS system date>
- `analysis_timezone`: America/Santiago

## Tipos de Cambio

| Par | Valor | Fecha | Fuente |
|-----|-------|-------|--------|
| UF → CLP | <pending> | <date> | Banco Central de Chile — https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx |
| USD → CLP | <pending> | <date> | Banco Central de Chile |
| EUR → CLP | <pending> | <date> | Banco Central de Chile |
| UTM → CLP | <pending> | <date> | Banco Central de Chile |
| BTC → USD | <pending> | <date> | CoinGecko — https://api.coingecko.com |

## Tasas de Crecimiento Asumidas (anual, real)

| Clase de activo | Tasa | Justificación |
|-----------------|------|---------------|
| AFP Fondo B | 5,0% | Promedio histórico ajustado por glide path |
| AFP Fondo C | 4,0% | Promedio histórico, perfil moderado |
| AFP Fondo D | 3,0% | Conservador |
| Depósitos a Plazo | 3,0% real (4–4,8% nominal) | Tasas actuales del cliente |
| Renta Variable Internacional (ETFs) | 6,0% | S&P 500 / world ex-US historical |
| Renta Variable Chilena | 5,0% | IPSA histórico |
| BTC | Excluido de la proyección | Volatilidad alta |
| Inmueble principal | 0,0% real | Conservador, sin apreciación neta |
| Inmueble de inversión | 1,0% real | Crecimiento de valor |

## Tasa de Inflación

- Chile (anual asumida para proyección 2026–2036): **6,0%** (puede ajustarse al IPC actual del INE)

## Retorno Post-Jubilación

- Asumido: **3,5% real anual** (cartera conservadora con énfasis en preservación)

## Fuentes de Precios de Instrumentos

| Instrumento | Fuente |
|-------------|--------|
| ETFs y acciones US (SRET, SCHY, SCHD, VNQI, VYMI, WDIV, XLU, AVUV, EFX) | Yahoo Finance vía `yfinance` |
| Acciones chilenas (ENELAM, CHILE, LTM, VAPORES, COLBUN) | Bolsa de Santiago |
| Cuotas de fondos (CFIETFCC, CFINRENTAS, QUINENO, CFMITNIPSA) | Bolsa de Santiago / administradora |
| Rentabilidad AFP | Superintendencia de Pensiones — https://www.spensiones.cl |
| PGU vigente | Instituto de Previsión Social — https://www.ips.gob.cl |

## Notas

- Si el cliente proporciona archivos (cartolas, AFP, ESPP), los valores reflejarán esa evidencia y se citarán en el *Anexo: Fuentes Documentales*.
- Cualquier supuesto modificado por el cliente queda registrado en `_provenance` de `client-profile.json`.

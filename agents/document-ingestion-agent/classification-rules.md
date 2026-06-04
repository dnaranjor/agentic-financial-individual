# Document Classification Rules (Extensible)

This file is the **only** source of truth for `classify_document()`. Add a new document type by appending a row — no code changes required.

## Schema

| Rule ID | Doc Type | Keyword/Regex Indicators (Spanish) | Required Hits | Notes |
|--------|----------|-------------------------------------|---------------|-------|
| R001 | `cartola_banco_itau` | `Banco Itaú`, `Saldo Disponible`, `Cartola` | ≥ 2 | Bank statement |
| R002 | `cartola_banco_bci` | `Banco BCI`, `Cartola`, `Movimientos` | ≥ 2 | Bank statement |
| R003 | `cartola_banco_estado` | `BancoEstado`, `Cartola` | ≥ 2 | Bank statement |
| R004 | `afp_cartola` | `AFP`, `Cuenta Capitalización Individual`, `Fondo (A|B|C|D|E)` | ≥ 2 | AFP quarterly statement |
| R005 | `afp_cartola_planvital` | `PlanVital`, `Cuenta de Capitalización` | ≥ 2 | AFP-specific |
| R006 | `apv_cartola` | `APV`, `Régimen (A|B)` | ≥ 2 | Voluntary pension savings |
| R007 | `espp_fidelity` | `Fidelity`, `Employee Stock Purchase`, `EFX` | ≥ 2 | ESPP from employer |
| R008 | `vector_capital_report` | `Vector Capital`, `Portafolio`, `Cartera` | ≥ 2 | Brokerage statement |
| R009 | `mercadopago_statement` | `Mercado Pago`, `Rendimientos`, `Saldo` | ≥ 2 | Digital savings |
| R010 | `time_deposit_cert` | `Depósito a Plazo`, `Tasa de Interés`, `Vencimiento` | ≥ 2 | Time deposit certificate |
| R011 | `operacion_renta_f22` | `Formulario 22`, `Renta`, `SII` | ≥ 2 | Annual tax return |
| R012 | `liquidacion_sueldo` | `Liquidación de Sueldo`, `Sueldo Líquido`, `Cotización` | ≥ 2 | Payslip |
| R013 | `poliza_seguro` | `Póliza`, `Prima`, `Asegurado` | ≥ 2 | Insurance policy |
| R014 | `contrato_hipotecario` | `Mutuo Hipotecario`, `Dividendo`, `UF` | ≥ 2 | Mortgage contract |
| R015 | `dividendo_hipotecario` | `Dividendo Mensual`, `UF`, `Hipoteca` | ≥ 2 | Monthly mortgage payment receipt |
| R016 | `tasacion_inmueble` | `Tasación`, `Avalúo`, `Inmueble` | ≥ 2 | Property appraisal |
| R017 | `certificado_dominio_vigente` | `Certificado de Dominio Vigente`, `CBR` | ≥ 2 | Property title certificate |
| R018 | `cartola_tarjeta_credito` | `Tarjeta de Crédito`, `Estado de Cuenta`, `Cupo` | ≥ 2 | Credit card statement |
| R019 | `crypto_exchange_report` | `Binance`, `Buda`, `Bitcoin`, `BTC` | ≥ 1 of last 2 | Crypto exchange export |
| R020 | `fonasa_certificate` | `FONASA`, `Beneficiario`, `Tramo` | ≥ 2 | Health coverage proof |
| R021 | `unknown` | (default fallback) | 0 | Triggers manual-review flag |

## Adding a New Rule

1. Pick the next free `R0XX` ID.
2. Append a row above R021 (`unknown`).
3. Keep keywords accent-insensitive at match time (`unidecode` before regex).
4. Test against at least one sample document before committing.

## Conflict Resolution

If multiple rules match, the one with the highest hit count wins. Ties broken by lower rule ID (older/more general rules first).

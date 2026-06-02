# Chilean Regulatory Agent — Knowledge Base

## Compliance Self-Check

- [ ] Was the PGU amount fetched from `ips.gob.cl` for the current month?
- [ ] Was the RSH bracket from the profile cross-checked against PGU's "not in top 10%" criterion?
- [ ] Was the spouse PGU eligibility evaluated separately (different age)?
- [ ] Was the APV regime comparison done at the client's actual marginal tax rate?
- [ ] Were any expired rules (PGU amount older than 60 days) refreshed?
- [ ] Were source URLs cited in the handoff?

## Auto-Learned Rules

- [2026-06-02] PGU as of 2025: $224,004 CLP/mes (verify monthly; update on every Learn! if outdated).
- [2026-06-02] PGU max compatible pension (Pensión Máxima con Aporte Solidario, PMAS) ≈ $1,158,355 CLP/mes; above this, PGU = 0.
- [2026-06-02] PGU eligibility requires 20 years residency total + 4 of last 5 — Venezuelan-Chilean dual nationality OK if residency met; verify residency dates from profile.
- [2026-06-02] APV Régimen A: state bonus capped at 6 UTM (~$397,000 CLP) per year.
- [2026-06-02] APV Régimen B: tax-deductible up to 50 UF/mes (~$1,937,000 CLP) or 600 UF/yr.
- [2026-06-02] Tope imponible AFP for 2026: ~83.4 UF; contributions above this not eligible for AFP capitalization.
- [2026-06-02] Operación Renta cutoff: April 30 each year for prior calendar year.
- [2026-06-02] FONASA tramo varies by income: Client at 4.5M CLP/mes likely Tramo D (no copay limit increases vs Tramo C); spouse at 520k likely Tramo B (low copay).

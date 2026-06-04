# Data Analyst Agent — Knowledge Base

## Compliance Self-Check

- [ ] Was every fetched value paired with its source URL and ISO-8601 timestamp?
- [ ] Was the analysis date confirmed equal to OS system date?
- [ ] Were rate limits respected (no >30 req/min to CoinGecko free tier)?
- [ ] Was the BCCh FX table written before downstream agents read it?
- [ ] Were Chilean equities fetched with a browser User-Agent?
- [ ] Was `shared/assumptions.md` updated with the FX used?
- [ ] Were values already present in `shared/evidence/` reused instead of re-fetched?

## Auto-Learned Rules

- [2026-06-02] BCCh public page requires a User-Agent header; default Python UA returns 403.
- [2026-06-02] CoinGecko `/simple/price` enforces ~30 req/min on free tier; cache BTC for 60s minimum.
- [2026-06-02] bolsadesantiago.com renders tickers with .SN suffix in some endpoints; ENELAM is ENELAM.SN on yfinance fallback.
- [2026-06-02] yfinance returns NaN during US market pre-open; retry after 09:30 ET or use `info["previousClose"]`.
- [2026-06-02] Always include UF→CLP factor in handoff; downstream agents assume it's present.

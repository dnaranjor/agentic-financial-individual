# Trading Analyst Agent — Knowledge Base

## Compliance Self-Check

- [ ] Were 2–3 strategy options offered (not just one)?
- [ ] Was each strategy paired with rationale, expected return, and risk?
- [ ] Was the glide path tied to years-to-retirement?
- [ ] Was AFP fund recommendation specific (current → target → when)?
- [ ] Was APV regime recommendation backed by marginal-tax-rate math?
- [ ] Were concentration risks (e.g., EFX) flagged?
- [ ] Did recommendations cite the Chilean Regulatory handoff when relevant?

## Auto-Learned Rules

- [2026-06-02] For clients <10 years to retirement, do not recommend AFP Fondo A (too volatile); cap at B and start glide toward C/D in final 5 years.
- [2026-06-02] APV Régimen A optimal when marginal tax rate ≤ 8%; Régimen B otherwise (assuming contributions under 600 UF/yr cap).
- [2026-06-02] When client owns employer stock via ESPP, treat employer-stock concentration as a hard cap at 10% of net worth.
- [2026-06-02] BTC allocation for retiree-track profile: cap at 1% of net worth; never recommend increasing for clients within 10 years of retirement.
- [2026-06-02] Income-oriented ETFs (SCHD, SCHY, VYMI, SRET, WDIV) align well with pre-retirement glide; keep but rebalance to target weights.

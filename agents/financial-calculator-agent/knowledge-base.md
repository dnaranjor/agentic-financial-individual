# Financial Calculator Agent — Knowledge Base

## Compliance Self-Check

- [ ] Did every numeric output include its formula and inputs?
- [ ] Were UF amounts converted using the UF value on the analysis date (not principal date)?
- [ ] Was the post-retirement return assumption explicitly stated?
- [ ] Were stock/ETF holdings valued at the price from Data Analyst's handoff?
- [ ] Was the savings rate computed against net (after-tax) income?
- [ ] Was BTC value pulled from the Data Analyst handoff (not re-fetched)?
- [ ] Were monthly contributions converted to annual when feeding `project_investment_growth`?

## Auto-Learned Rules

- [2026-06-02] Always value the mortgage outstanding balance by multiplying UF balance × UF_CLP on analysis date.
- [2026-06-02] When computing nest egg with inflation-indexed annuity, real return = (1+nominal)/(1+inflation)-1; do not subtract directly.
- [2026-06-02] Default growth assumptions if missing: AFP B 5% real, AFP C 4% real, AFP D 3% real, time deposits 3% real (4–4.8% nominal in current rate environment), US equities/ETFs 6% real, Chilean equities 5% real, BTC excluded from projection by default (volatility).
- [2026-06-02] Tax refund (300k CLP/yr) treated as 25k CLP/month in cash-flow analysis.
- [2026-06-02] ESPP cash held at Fidelity is USD; convert at handoff USD_CLP rate.

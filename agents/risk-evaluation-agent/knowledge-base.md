# Risk Evaluation Agent — Knowledge Base

## Compliance Self-Check

- [ ] Was the Monte Carlo run with ≥ 10,000 trials?
- [ ] Were sensitivity scenarios run for: inflation, equity returns, longevity?
- [ ] Was sequence-of-returns risk evaluated for the first 5 retirement years?
- [ ] Were employer-stock and single-currency concentrations flagged?
- [ ] Was insurance coverage compared to mortgage balance + dependents' needs?
- [ ] Was data-integrity check run when `shared/evidence/` is non-empty?
- [ ] Was every risk paired with a concrete Spanish mitigation step?

## Auto-Learned Rules

- [2026-06-02] Sequence-of-returns risk for early retirement years is more dangerous than average returns; always evaluate first-5-year drawdown scenarios separately.
- [2026-06-02] ESPP employer stock (EFX) concentration is commonly overlooked; always flag if >5% of liquid net worth.
- [2026-06-02] CLP-denominated expenses funded by USD assets implies currency risk; quantify as 'worst-case CLP appreciation 15%' scenario.
- [2026-06-02] FONASA coverage for a 67-year-old retiree warrants assessing supplemental seguro complementario; flag as medium risk if absent.
- [2026-06-02] Mortgage with 100 installments remaining (≈8.3 years) ends near retirement (age 67) — verify life insurance covers outstanding UF balance.

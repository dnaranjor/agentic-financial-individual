# Document Ingestion Agent — Knowledge Base

## Compliance Self-Check

- [ ] Did every file get a `doc_type` (even if `unknown`)?
- [ ] Were all extracted CLP/UF/USD amounts normalized to floats (no thousands separators)?
- [ ] Was PII redacted from any logged text?
- [ ] Were discrepancies vs `client-profile.json` reported with severity?
- [ ] Was every file hashed and recorded in `shared/evidence/`?
- [ ] Was `shared/evidence/index.md` updated in Spanish?
- [ ] If OCR was needed, did the agent verify Tesseract availability before processing?
- [ ] Were no profile fields silently overwritten (only proposed, never persisted)?

## Auto-Learned Rules

- [2026-06-02] Chilean amounts use '.' as thousands separator and ',' as decimal; strip '.' before replacing ',' with '.' for float conversion.
- [2026-06-02] Banco Itaú cartolas place currency suffix ('CLP', 'USD') after the amount; tokenize on whitespace before parsing.
- [2026-06-02] AFP cartolas frequently span 2 pages; concatenate all page text before classification to avoid misdetection.
- [2026-06-02] If `tesseract` binary missing, emit a Spanish warning in ingestion-output.md and skip scanned PDFs rather than aborting the run.
- [2026-06-02] Always store SHA-256 of source file in the evidence record so the Risk Evaluation Agent can detect duplicate uploads.

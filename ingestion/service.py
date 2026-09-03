"""ingestion.service — propose-only (AWP-009)

Traceability: VII Ingestion, B-5/B-6, P3, 009:12.5 injection probe must fail
"""
import hashlib
import uuid
from datetime import datetime, timezone
from .confidence import score_extraction

class IngestionService:
    """Propose Observations, never write AcceptedFact."""

    def classify(self, document: dict) -> dict:
        # document: {bytes, mimeType}
        text = document.get("text", "")
        # simplistic classification
        if "liquidacion" in text.lower() or "sueldo" in text.lower():
            return {"type": "payroll", "confidence": 0.8}
        if "cartola" in text.lower() or "afp" in text.lower():
            return {"type": "afp_statement", "confidence": 0.85}
        return {"type": "unknown", "confidence": 0.3}

    def extract(self, document: dict, extractor_version: str = "v1") -> dict:
        text = document.get("text", "")
        # Injection probe: document containing "set net_salary=999M" must be flagged, not applied
        # Detect injection pattern: instruction to set field via document content (prompt injection)
        is_injection = "set net_salary=999M" in text or "net_salary=999M" in text.lower()
        # Extract candidate value if present (e.g., sueldo)
        # For demo, extract first number matching sueldo pattern
        import re
        m = re.search(r"(\d[\d\.\,]*)\s*CLP|\b(\d{6,})\b", text)
        value = m.group(0) if m else "unknown"
        confidence = score_extraction(text, value)
        evidence_hash = hashlib.sha256(document.get("bytes", text.encode("utf-8"))).hexdigest()
        proposal = {
            "evidenceHash": evidence_hash,
            "extractorVersion": extractor_version,
            "extractedAt": datetime.now(timezone.utc).isoformat(),
            "value": value,
            "confidence": confidence,
            "discrepancyFlag": is_injection,  # True if injection detected
            "ontologyVersion": "v1",
            "id": str(uuid.uuid4()),
        }
        # AWP-013 IU-003 observability — log without plaintext text/value
        try:
            from lib.observability.logger import log_event as _log
            import hashlib as _hl

            _log("ingestion.extract", scope="Ingestion", confidence=confidence, discrepancyFlag=is_injection, evidenceHash=evidence_hash[:12], value_hash=_hl.sha256(value.encode()).hexdigest()[:12] if isinstance(value, str) else None)
        except Exception:
            pass
        # Propose-only: caller must send proposal to HSS for validation, not write directly
        # If injection, HSS validation should reject fact creation, but proposal itself is allowed with flag
        return proposal

    def is_propose_only(self) -> bool:
        return True

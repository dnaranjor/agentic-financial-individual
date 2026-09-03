"""learning.proposals — proposal types (AWP-011)

Traceability: C-008, VI.10 TAD-10
"""
import uuid
from datetime import datetime, timezone

def propose_extraction_heuristic(description: str, evidence_links: list[str]) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "type": "extraction_heuristic",
        "description": description,
        "evidenceLinks": evidence_links,
        "status": "proposed",
        "createdAt": datetime.now(timezone.utc),
        "evaluated": False,
    }

def propose_source_reliability(source: str, evidence_links: list[str]) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "type": "source_reliability",
        "description": f"source {source} reliability update",
        "evidenceLinks": evidence_links,
        "status": "proposed",
        "createdAt": datetime.now(timezone.utc),
        "evaluated": False,
    }

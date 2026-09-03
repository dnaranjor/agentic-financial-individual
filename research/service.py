"""research.service — propose-only public sources (AWP-009)

Traceability: VII Research, B-5 public only, never household, U-07 stance external content is data
"""
import uuid
from datetime import datetime, timezone

class ResearchService:
    """Propose MarketObservation + Claim with citation, public sources only."""

    def fetch(self, url: str, series: str = None) -> dict:
        # public sources only — never household data
        if "household" in url.lower() or "client-profile" in url.lower():
            raise ValueError("research boundary: household data not allowed (B-5)")
        # Mock fetch for demo: return MarketObservation + Claim
        now = datetime.now(timezone.utc)
        obs = {
            "ontologyVersion": "v1",
            "series": series or "UF",
            "asOf": now.date().isoformat(),
            "source": url,
            "value": 39405 if series == "UF" else 100,
            "unit": "INDEX_UF" if series == "UF" else "RATIO",
            "freshnessClass": "daily",
        }
        claim = {
            "ontologyVersion": "v1",
            "id": str(uuid.uuid4()),
            "proposition": f"Fetched {series} from {url}",
            "sourceRefs": [url],
            "status": "proposed",
            "citation": url,
            "retrievalTime": now.isoformat(),
        }
        return {"observation": obs, "claim": claim}

    def is_propose_only(self) -> bool:
        return True

    def is_public_only(self, url: str) -> bool:
        return "household" not in url.lower()

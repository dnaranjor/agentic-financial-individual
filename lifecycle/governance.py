"""lifecycle.governance — gated learning + p95 SLA + cron boundary (AWP-011)

Traceability: VI.10 TAD-10, 011:12.4 p95<7d, RT-M05 cron Monitoring->Finding not activate
"""
from datetime import datetime, timezone, timedelta
from typing import List

class GatedLearning:
    def __init__(self):
        self.proposals: List[dict] = []

    def propose(self, proposal: dict) -> dict:
        # proposal: {type, evidenceLinks, description}
        p = {
            "id": proposal.get("id", "prop-" + str(len(self.proposals)+1)),
            "type": proposal["type"],
            "description": proposal.get("description", ""),
            "evidenceLinks": proposal.get("evidenceLinks", []),
            "status": "proposed",
            "createdAt": datetime.now(timezone.utc),
            "evaluated": False,
            "evaluation": None,
        }
        self.proposals.append(p)
        return p

    def evaluate(self, proposal_id: str, result: str) -> dict:
        for p in self.proposals:
            if p["id"] == proposal_id:
                p["evaluated"] = True
                p["evaluation"] = result
                p["evaluatedAt"] = datetime.now(timezone.utc)
                return p
        raise ValueError("proposal not found")

    def approve(self, proposal_id: str) -> dict:
        for p in self.proposals:
            if p["id"] == proposal_id:
                if not p["evaluated"]:
                    raise ValueError("cannot activate without evaluation+approval (gated)")
                p["status"] = "approved"
                p["activatedAt"] = datetime.now(timezone.utc)
                return p
        raise ValueError("proposal not found")

    def p95_days(self) -> float:
        # calculate p95 of (evaluatedAt - createdAt) for evaluated proposals
        deltas = []
        for p in self.proposals:
            if p.get("evaluated"):
                delta = (p["evaluatedAt"] - p["createdAt"]).total_seconds() / 86400
                deltas.append(delta)
        if not deltas:
            return 0
        deltas.sort()
        idx = int(0.95 * len(deltas))
        idx = min(idx, len(deltas)-1)
        return deltas[idx]

    def cron_monitoring_finding(self, finding: dict) -> bool:
        """RT-M05: cron Monitoring->Finding must NOT auto-activate learning."""
        # Finding from monitoring should not auto-create activated proposal
        # Return False means not activated
        return False

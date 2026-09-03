"""lifecycle.state — Recommendation lifecycle + Decision/Outcome (AWP-011)

Traceability: VI.10, 011 VM6, B-8
"""
import uuid
from datetime import date, datetime, timezone, timedelta
from typing import Optional

class Recommendation:
    def __init__(self, derived_value_refs: list[str], falsification: list[str] = None, expiry_days: int = 90):
        self.id = str(uuid.uuid4())
        self.ontologyVersion = "v1"
        self.derivedValueRefs = derived_value_refs
        self.falsificationConditions = falsification or [f"DerivedValue {derived_value_refs[0]} >10% 90d"]
        self.expiry = date.today() + timedelta(days=expiry_days)
        self.status = "draft"
        self.findings = []

    def present(self):
        if self.status != "draft":
            raise ValueError(f"cannot present from {self.status}")
        self.status = "presented"
        return self

    def accept(self):
        if self.status != "presented":
            raise ValueError(f"cannot accept from {self.status}")
        self.status = "accepted"
        return self

    def reject(self):
        if self.status != "presented":
            raise ValueError(f"cannot reject from {self.status}")
        self.status = "rejected"
        return self

    def defer(self):
        if self.status != "presented":
            raise ValueError("cannot defer")
        self.status = "deferred"
        return self

    def expire(self):
        self.status = "expired"
        return self

    def invalidate(self):
        self.status = "invalidated"
        return self

    def check_stale(self, observations: list[dict]) -> bool:
        # if any observation stale, recommendation expires
        for o in observations:
            if o.get("staleness") == "stale":
                self.expire()
                return True
        return False

class Decision:
    def __init__(self, recommendation_id: str):
        self.id = str(uuid.uuid4())
        self.recommendationId = recommendation_id
        self.recordedAt = datetime.now(timezone.utc)
        self._final = False

    def record(self):
        if self._final:
            raise ValueError("Decision immutable once recorded (B-8)")
        self._final = True
        return self

class Outcome:
    def __init__(self, decision_id: str, value: float):
        self.id = str(uuid.uuid4())
        self.decisionId = decision_id
        self.value = value
        self.observedAt = datetime.now(timezone.utc)

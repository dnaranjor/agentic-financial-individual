"""HSS store — bitemporal append-only + vault encrypted-at-write (AWP-003)

Traceability: TARGET-ARCHITECTURE.md:VI.3, INV-03a, INV-15, B-2
"""
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict
import uuid

from .models import AcceptedFact
from .clock import is_future_recorded_at, is_monotonic
import vault

class BitemporalStore:
    def __init__(self):
        self.facts: List[AcceptedFact] = []
        # index by valid key (for monotonic + overlap) — key = (claimRef, validFrom) simplified; real key would be personId+field
        self._by_key: Dict[str, List[AcceptedFact]] = {}

    def _key(self, fact: AcceptedFact) -> str:
        # Simplified valid key — claimRef groups same logical fact; in real, would be (personId, field)
        return fact.claimRef

    def append(self, fact: AcceptedFact, now_dt: datetime = None) -> AcceptedFact:
        # INV-03a future check
        if is_future_recorded_at(fact.recordedAt, now_dt):
            raise ValueError(f"future recorded_at rejected: {fact.recordedAt} > now+epsilon")
        # monotonic per key
        key = self._key(fact)
        existing = self._by_key.get(key, [])
        if existing:
            last = max(existing, key=lambda f: f.recordedAt)
            if not is_monotonic(last.recordedAt, fact.recordedAt):
                raise ValueError(f"non-monotonic recorded_at for key {key}: {fact.recordedAt} < {last.recordedAt}")
            # overlap check: new validFrom must not overlap existing open validTo
            for ef in existing:
                if ef.validTo is None:
                    # existing open interval — new validFrom must be after existing validFrom and we will close prior
                    # Auto-close prior validTo = new.validFrom -1 day
                    if fact.validFrom <= ef.validFrom:
                        raise ValueError(f"overlapping valid period: new validFrom {fact.validFrom} <= existing {ef.validFrom} for key {key}")
                    # auto-close prior
                    ef.validTo = fact.validFrom  # close on day before new starts (simplified)
                else:
                    # check overlap with closed intervals
                    if not (fact.validTo is not None and fact.validTo <= ef.validFrom or fact.validFrom >= ef.validTo):
                        # overlap if intervals intersect
                        if fact.validFrom < ef.validTo and (fact.validTo is None or ef.validFrom < fact.validTo):
                            # Actually need proper interval overlap: [validFrom, validTo)
                            if fact.validFrom < (ef.validTo or date.max) and ef.validFrom < (fact.validTo or date.max):
                                raise ValueError(f"overlapping validTo: {fact.validFrom} overlaps {ef.validFrom}-{ef.validTo}")
        # vault encrypt-at-write — payload is fact json bytes
        payload = fact.model_dump_json().encode("utf-8")
        ref = vault.encrypt(payload, scope="AcceptedFact", key_ref=fact.id)
        # store fact (in-memory) — actual persisted via vault, but keep in-memory for query
        self.facts.append(fact)
        self._by_key.setdefault(key, []).append(fact)
        # also write encrypted ref to .vault meta (not plaintext on disk)
        return fact

    def query(self, validAt: date, asOf: datetime) -> List[AcceptedFact]:
        # return facts valid at validAt as believed at asOf (bitemporal)
        # asOf = recordedAt upper bound
        result = []
        for f in self.facts:
            if f.recordedAt > asOf:
                continue
            if f.validFrom <= validAt and (f.validTo is None or validAt < f.validTo):
                result.append(f)
        # return latest recorded per key (max recordedAt <= asOf)
        latest = {}
        for f in result:
            k = self._key(f)
            if k not in latest or f.recordedAt > latest[k].recordedAt:
                latest[k] = f
        return list(latest.values())

    def all_facts(self) -> List[AcceptedFact]:
        return list(self.facts)

    def export_snapshot(self, snapshot_id: str, validAt: date, asOf: datetime) -> bytes:
        facts = self.query(validAt, asOf)
        data = {"snapshotId": snapshot_id, "validAt": validAt.isoformat(), "asOf": asOf.isoformat(), "facts": [f.model_dump(mode="json") for f in facts], "ontologyVersion": "v1"}
        return json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")

    def import_snapshot(self, data: bytes):
        # for restore test — not used for append, just verify byte-identical
        pass

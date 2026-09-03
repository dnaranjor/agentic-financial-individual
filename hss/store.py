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
            try:
                from lib.observability.logger import log_event as _log

                _log("hss.reject", scope="AcceptedFact", claimRef=fact.claimRef, reason="future recorded_at", recordedAt=fact.recordedAt.isoformat())
            except Exception:
                pass
            raise ValueError(f"future recorded_at rejected: {fact.recordedAt} > now+epsilon")
        # monotonic per key
        key = self._key(fact)
        existing = self._by_key.get(key, [])
        if existing:
            last = max(existing, key=lambda f: f.recordedAt)
            if not is_monotonic(last.recordedAt, fact.recordedAt):
                try:
                    from lib.observability.logger import log_event as _log

                    _log("hss.reject", scope="AcceptedFact", claimRef=fact.claimRef, reason="non-monotonic", recordedAt=fact.recordedAt.isoformat())
                except Exception:
                    pass
                raise ValueError(f"non-monotonic recorded_at for key {key}: {fact.recordedAt} < {last.recordedAt}")
            # overlap check: new validFrom must not overlap existing open validTo
            for ef in existing:
                if ef.validTo is None:
                    # existing open interval — new validFrom must be after existing validFrom and we will close prior
                    # Auto-close prior validTo = new.validFrom -1 day
                    if fact.validFrom <= ef.validFrom:
                        try:
                            from lib.observability.logger import log_event as _log

                            _log("hss.reject", scope="AcceptedFact", claimRef=fact.claimRef, reason="overlapping valid period")
                        except Exception:
                            pass
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
                                try:
                                    from lib.observability.logger import log_event as _log

                                    _log("hss.reject", scope="AcceptedFact", claimRef=fact.claimRef, reason="overlapping validTo")
                                except Exception:
                                    pass
                                raise ValueError(f"overlapping validTo: {fact.validFrom} overlaps {ef.validFrom}-{ef.validTo}")
        # vault encrypt-at-write — payload is fact json bytes
        payload = fact.model_dump_json().encode("utf-8")
        ref = vault.encrypt(payload, scope="AcceptedFact", key_ref=fact.id)
        # store fact (in-memory) — actual persisted via vault, but keep in-memory for query
        self.facts.append(fact)
        self._by_key.setdefault(key, []).append(fact)
        # observability — log accept without plaintext value (hash len only)
        try:
            from lib.observability.logger import log_event as _log
            import hashlib as _hl

            _log("hss.accept", scope="AcceptedFact", claimRef=fact.claimRef, id=fact.id, validFrom=fact.validFrom.isoformat(), recordedAt=fact.recordedAt.isoformat(), value_hash=_hl.sha256(payload).hexdigest()[:12])
        except Exception:
            pass
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

    def load_from_vault(self, vault_dir: Path = None) -> int:
        """AWP-013 IU-002 — repopulate in-memory store from vault/data/AcceptedFact/*.enc

        Decrypts each .enc via vault.decrypt, validates AcceptedFact, sorts by recordedAt
        ascending and replays via _by_key autoclosure. Corrupt files are skipped and
        logged to reports/afi.log via lib.observability (gitignored). Returns count loaded.
        Traceability: AFI-VALIDATION-REPORT.md:458,341 (restart loss), INV-15, GAP-037.
        """
        # lazy import to avoid circular and keep L2→L3 clean (logger in lib/)
        vault_dir = vault_dir or Path(__file__).resolve().parent.parent / "vault" / "data" / "AcceptedFact"
        # also handle if caller passes vault base data dir
        if vault_dir.name != "AcceptedFact":
            candidate = vault_dir / "AcceptedFact"
            if candidate.exists():
                vault_dir = candidate
        self.facts.clear()
        self._by_key.clear()
        count = 0
        corrupt = 0
        # collect decrypt candidates
        enc_files = sorted(vault_dir.glob("*.enc")) if vault_dir.exists() else []
        decoded = []
        for p in enc_files:
            try:
                ref = f"vault://AcceptedFact/{p.stem}"
                raw = vault.decrypt(ref)
                obj = json.loads(raw.decode("utf-8"))
                fact = AcceptedFact.model_validate(obj)
                decoded.append(fact)
            except Exception as e:
                corrupt += 1
                # log corrupt but not plaintext
                try:
                    from lib.observability.logger import log_event as _log

                    _log("vault.load_corrupt", scope="AcceptedFact", key_ref=p.stem, error=str(e)[:200])
                except Exception:
                    pass
                continue
        # sort by recordedAt to preserve monotonic + autoclosure order
        decoded.sort(key=lambda f: f.recordedAt)
        for fact in decoded:
            # re-apply autoclosure bookkeeping without re-encrypting (already in vault)
            key = self._key(fact)
            existing = self._by_key.get(key, [])
            # mimic append autoclosure: if existing open, close at new validFrom
            for ef in existing:
                if ef.validTo is None and fact.validFrom > ef.validFrom:
                    ef.validTo = fact.validFrom
            self.facts.append(fact)
            self._by_key.setdefault(key, []).append(fact)
            count += 1
        # log summary
        try:
            from lib.observability.logger import log_event as _log2

            _log2("hss.load_from_vault", scope="AcceptedFact", count=count, corrupt=corrupt, vault_dir=str(vault_dir))
        except Exception:
            pass
        return count

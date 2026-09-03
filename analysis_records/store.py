"""analysis_records.store — immutable bundles (AWP-007c)

Traceability: VI.9, B-8, 007c:12.4
"""
import json
import hashlib
from pathlib import Path
from typing import List

STORE_DIR = Path(__file__).parent

class AnalysisRecordStore:
    def save(self, record: dict) -> Path:
        # record must have id, snapshotId, assumptionSetVersion, engineVersion, ontologyVersion
        p = STORE_DIR / f"record-{record['id']}.json"
        # immutable check: if exists, must be byte-identical
        data = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
        if p.exists():
            existing = p.read_bytes()
            if existing != data:
                raise ValueError(f"B-8 violation: analysis record {record['id']} immutable, exists but differs")
        else:
            p.write_bytes(data)
        return p

    def load(self, record_id: str) -> dict:
        p = STORE_DIR / f"record-{record_id}.json"
        return json.loads(p.read_text(encoding="utf-8"))

    def replay(self, record_id: str) -> bool:
        """Byte-identical replay: load and re-serialize sorted."""
        p = STORE_DIR / f"record-{record_id}.json"
        raw = p.read_bytes()
        obj = json.loads(raw.decode("utf-8"))
        re_serialized = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return raw == re_serialized

    def baseline_id(self) -> str:
        return "000-baseline"

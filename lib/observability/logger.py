"""AFI observability logger — AWP-013 IU-003

Traceability: AFI-DEPLOYMENT-VALIDATION-REPORT-2026-09-03.md:363-377 gaps, §16 residual risks, vault-layout.md
Interface: log_event(event: str, scope: str = None, correlation_id: str = None, **fields) -> str

Writes gitignored jsonl to reports/afi.log (already .gitignore:32 *.log).
Never logs plaintext household values — callers must pass hashes/lengths, not payload.
"""
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone

LOG_PATH = Path(__file__).resolve().parents[2] / "reports" / "afi.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_correlation_id(correlation_id: str | None = None) -> str:
    return correlation_id or str(uuid.uuid4())


def log_event(event: str, scope: str | None = None, correlation_id: str | None = None, **fields) -> str:
    cid = get_correlation_id(correlation_id)
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "scope": scope,
        "correlation_id": cid,
        "ontologyVersion": "v1",
    }
    # merge fields, redacting obvious plaintext carriers if accidentally passed
    # callers are responsible for not passing payload; defensive: drop 'payload'/'value' plaintext if present
    for k, v in fields.items():
        if k in ("payload", "value", "plaintext") and isinstance(v, (str, bytes)):
            # store hash instead of plaintext
            import hashlib as _hl
            b = v.encode("utf-8") if isinstance(v, str) else v
            rec[k + "_hash"] = _hl.sha256(b).hexdigest()[:12]
            rec[k + "_len"] = len(b)
        else:
            rec[k] = v
    # sanitize: ensure json serializable
    try:
        line = json.dumps(rec, sort_keys=True, ensure_ascii=False)
    except Exception:
        # fallback to stringified
        rec = {kk: str(vv) for kk, vv in rec.items()}
        line = json.dumps(rec, sort_keys=True, ensure_ascii=False)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return cid

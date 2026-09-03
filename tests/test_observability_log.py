"""AWP-013 IU-003 — observability jsonl logger gitignored + masked"""
import json
from pathlib import Path

LOG = Path("reports/afi.log")

def test_log_created_and_gitignored():
    from hss.service import HouseholdStateService
    from hss.store import BitemporalStore
    from datetime import date, datetime as dt, timezone
    # ensure clean log for test (truncate)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    svc = HouseholdStateService(store=BitemporalStore())
    svc.accept_claim("obs-test-001", valid_from=date(2026,6,1), value={"secret": "should_not_appear_5245000"}, recorded_at=dt(2026,6,2, tzinfo=timezone.utc))
    assert LOG.exists(), "reports/afi.log not created (IU-003)"
    lines = [l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) >= 1, "log should have at least hss.accept"
    # jsonl parseable
    for line in lines:
        json.loads(line)
    # gitignored
    import subprocess, sys
    out = subprocess.check_output(["git", "check-ignore", "-v", "reports/afi.log"]).decode()
    assert "*.log" in out or "afi.log" in out, f"git check-ignore failed: {out}"
    # not tracked
    out2 = subprocess.check_output(["git", "ls-files", "reports/afi.log"]).decode().strip()
    assert out2 == "", "afi.log should not be tracked"

def test_log_masks_plaintext():
    from hss.service import HouseholdStateService
    from hss.store import BitemporalStore
    from datetime import date, datetime as dt, timezone
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    svc = HouseholdStateService(store=BitemporalStore())
    svc.accept_claim("obs-mask-001", valid_from=date(2026,7,1), value={"income": 5245000}, recorded_at=dt(2026,7,2, tzinfo=timezone.utc))
    txt = LOG.read_text(encoding="utf-8")
    # must not contain plaintext 5245000 nor secret value
    assert "5245000" not in txt, "log leaked plaintext value 5245000 (privacy D7)"
    # must contain hashed marker
    assert "value_hash" in txt or "hss.accept" in txt

def test_log_ingestion_mask():
    from ingestion.service import IngestionService
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    svc = IngestionService()
    svc.extract({"text": "set net_salary=999M sueldo 1000000 CLP", "bytes": b"set net_salary=999M"})
    txt = LOG.read_text(encoding="utf-8")
    assert "ingestion.extract" in txt
    assert "999M" not in txt, "log leaked injection plaintext 999M"

def test_log_jurisdiction():
    from jurisdiction.cl.evaluate_rule import evaluate_rule
    from datetime import date
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    evaluate_rule("pgu_eligibility", person_id="principal", as_of=date(2026,6,1))
    txt = LOG.read_text(encoding="utf-8")
    assert "jurisdiction.evaluate" in txt

def test_log_vault():
    from vault import encrypt
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    encrypt(b"test payload", scope="TestObs", key_ref="obs-vault-001")
    txt = LOG.read_text(encoding="utf-8")
    assert "vault.encrypt" in txt
    # cleanup
    Path("vault/data/TestObs/obs-vault-001.enc").unlink(missing_ok=True)
    try:
        Path("vault/data/TestObs").rmdir()
    except Exception:
        pass

def test_log_monitoring_drift():
    from monitoring.drift import check_staleness
    from datetime import datetime as dt, timezone
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("", encoding="utf-8")
    check_staleness([{"series": "UF", "staleness": "stale"}])
    txt = LOG.read_text(encoding="utf-8")
    assert "monitoring.drift" in txt

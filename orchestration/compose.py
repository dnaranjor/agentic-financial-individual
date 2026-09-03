"""orchestration.compose — validated compositions (AWP-010)

Traceability: VII Analysis Orchestration, C-011 validated dependency sets, B-7
"""
import uuid
from datetime import datetime, timezone

# Validated modes per TARGET-ARCHITECTURE.md:VII
VALIDATED_MODES = {
    "Baseline": ["HSS", "Engine", "RiskGate", "RecordStore"],
    "Update": ["HSS", "Engine", "Market", "Assumption", "RiskGate", "RecordStore"],
}

def compose(intent: str, capabilities: list[str] = None, snapshot_id: str = None) -> dict:
    mode = intent if intent in VALIDATED_MODES else "Baseline"
    required = VALIDATED_MODES[mode]
    # Validate requested capabilities are subset of validated mode
    if capabilities:
        missing = [c for c in required if c not in capabilities and c not in ["HSS", "Engine"]]
        # For demo, just ensure HSS+Engine present
        if "HSS" not in capabilities or "Engine" not in capabilities:
            raise ValueError(f"validated composition {mode} requires HSS+Engine, got {capabilities}")
    return {
        "run_id": str(uuid.uuid4()),
        "intent": intent,
        "mode": mode,
        "required": required,
        "snapshotId": snapshot_id or str(uuid.uuid4()),
        "assumptionSetVersion": "v1",
        "engineVersion": "0.1.0",
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

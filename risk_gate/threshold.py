"""risk_gate.threshold — governed versioned rule (AWP-007b)

Traceability: TAD-08, STAGE-8-PLAN-DELTA.md:5 verdict OPERATIONALIZABLE
Threshold as versioned governed rule, not hardcoded.
"""
THRESHOLD_VERSION = "v1"
# versioned rule: Critico blocks, Alto blocks if strict, etc.
# For 007b, default: Critico -> blocked
RULE = {
    "version": THRESHOLD_VERSION,
    "blocked_severities": ["Critico"],
    "description": "governed versioned threshold v1: Critico blocks presentation until acknowledge_finding",
}

def is_blocked(severity: str, threshold_rule = None) -> bool:
    rule = threshold_rule or RULE
    return severity in rule["blocked_severities"]

def get_threshold():
    return RULE

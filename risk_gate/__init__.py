"""risk_gate — Risk & Consistency Gate (AWP-007b)

Traceability: TARGET-ARCHITECTURE.md:VI.8, TAD-08
"""
from .gate import check, acknowledge_finding

__all__ = ["check", "acknowledge_finding"]

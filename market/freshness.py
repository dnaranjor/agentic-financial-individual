"""market.freshness — per-series thresholds (AWP-006)

Traceability: STAGE-8-PLAN-DELTA.md:6.2 RT-M06, docs/assumptions/freshness-policy.md
"""
from datetime import datetime, timedelta

# thresholds per series
THRESHOLDS = {
    "UF": timedelta(hours=24),          # daily
    "CPI": timedelta(days=32),           # monthly ~32d
    "FX_USDCLP": timedelta(hours=24),    # daily
    "TPM": timedelta(days=90),           # ad-hoc quarterly
    "YFINANCE": timedelta(hours=1),       # intraday ~1h
    "YFINANCE_INTRADAY": timedelta(hours=1),
}

def staleness(series: str, as_of: datetime, now: datetime) -> str:
    """Return observed|aged|stale per series."""
    thr = THRESHOLDS.get(series, timedelta(hours=24))
    delta = now - as_of
    if delta <= thr:
        return "observed"
    elif delta <= thr * 2:
        return "aged"
    else:
        return "stale"

def is_stale(series: str, as_of: datetime, now: datetime) -> bool:
    return staleness(series, as_of, now) == "stale"

"""HSS clock — INV-03a (AWP-003)

recorded_at <= now+epsilon and monotonic per valid key; future-recorded_at rejected.
"""
from datetime import datetime, timezone, timedelta

epsilon = timedelta(minutes=5)

def now() -> datetime:
    return datetime.now(timezone.utc)

def is_future_recorded_at(recorded_at: datetime, now_dt: datetime = None) -> bool:
    nd = now_dt or now()
    # ensure timezone aware
    if recorded_at.tzinfo is None:
        recorded_at = recorded_at.replace(tzinfo=timezone.utc)
    if nd.tzinfo is None:
        nd = nd.replace(tzinfo=timezone.utc)
    return recorded_at > nd + epsilon

def is_monotonic(prev_recorded: datetime, new_recorded: datetime) -> bool:
    if prev_recorded is None:
        return True
    if prev_recorded.tzinfo is None:
        prev_recorded = prev_recorded.replace(tzinfo=timezone.utc)
    if new_recorded.tzinfo is None:
        new_recorded = new_recorded.replace(tzinfo=timezone.utc)
    return new_recorded >= prev_recorded

"""market.service — Market Observation Service (AWP-006)

Traceability: VI.4, STAGE-8-PLAN-DELTA.md:6.2 per-series
"""
from datetime import datetime
from typing import Optional
from .store import MarketStore
from .freshness import staleness, THRESHOLDS

class MarketObservationService:
    def __init__(self, store: MarketStore = None):
        self.store = store or MarketStore()

    def observe(self, series: str, as_of: datetime, source: str, value: float, unit: str) -> dict:
        return self.store.append(series, as_of, source, value, unit)

    def get_with_staleness(self, series: str, as_of: str, now: datetime) -> Optional[dict]:
        obs = self.store.get(series, as_of)
        if not obs:
            return None
        # parse as_of datetime for staleness
        from datetime import datetime as _dt
        as_dt = _dt.fromisoformat(obs["asOf"])
        # need time component — use noon
        as_dt = as_dt.replace(hour=12)
        if as_dt.tzinfo is None:
            from datetime import timezone
            as_dt = as_dt.replace(tzinfo=timezone.utc)
            now_tz = now.replace(tzinfo=timezone.utc) if now.tzinfo is None else now
        else:
            now_tz = now
        obs["staleness"] = staleness(series, as_dt, now_tz)
        return obs

    def all_observations(self):
        return self.store.all()

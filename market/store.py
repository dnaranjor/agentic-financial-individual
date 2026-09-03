"""market.store — append-only MarketObservation (AWP-006)"""
from datetime import datetime
from typing import List, Optional
from pathlib import Path
import json

class MarketStore:
    def __init__(self):
        self.observations: List[dict] = []

    def append(self, series: str, as_of: datetime, source: str, value: float, unit: str) -> dict:
        obs = {
            "ontologyVersion": "v1",
            "series": series,
            "asOf": as_of.date().isoformat(),
            "source": source,
            "value": value,
            "unit": unit,
            "freshnessClass": "daily" if series == "UF" else "monthly" if series == "CPI" else "intraday",
        }
        self.observations.append(obs)
        return obs

    def get(self, series: str, as_of: str) -> Optional[dict]:
        for o in self.observations:
            if o["series"] == series and o["asOf"] == as_of:
                return o
        return None

    def all(self) -> List[dict]:
        return list(self.observations)

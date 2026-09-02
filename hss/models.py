"""HSS models — Pydantic from schema/registry (AWP-003)

Traceability: schema/registry/accepted-fact.json, measure.json, unit.json, docs/ontology/v1.md
"""
from datetime import date, datetime
from typing import Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class Unit(str, Enum):
    CURRENCY_CLP = "CURRENCY_CLP"
    CURRENCY_USD = "CURRENCY_USD"
    INDEX_UF = "INDEX_UF"
    INSTRUMENT_QTY = "INSTRUMENT_QTY"
    RATIO = "RATIO"

class BasisType(str, Enum):
    nominal = "nominal"
    real = "real"

class MeasureBasis(BaseModel):
    unit: Unit
    type: BasisType
    basePeriod: str = Field(pattern=r"^\d{4}-\d{2}$")
    asOf: date

class Measure(BaseModel):
    ontologyVersion: str = Field(default="v1", pattern="^v1$")
    value: float
    unit: Unit
    basis: MeasureBasis

class AcceptedFact(BaseModel):
    ontologyVersion: str = Field(default="v1", pattern="^v1$")
    id: str
    claimRef: str
    validFrom: date
    validTo: Optional[date] = None
    recordedAt: datetime
    value: Any

    model_config = {"extra": "forbid"}

"""jurisdiction.cl.rules — Chilean rules effective-dated (AWP-007a)

Traceability: TARGET-ARCHITECTURE.md:VI.6, F-05 per-person, GAP-020
"""
from datetime import date

RULES = {
    "pgu_eligibility": {
        "description": "PGU eligibility per person: age >=65, residency >=20y, RSH top10% not in, PMAS $1,158,355",
        "effectiveFrom": date(2024, 2, 1),
        "effectiveTo": None,
        "citation": "https://www.ips.gob.cl",
        "params": {"pgu_amount": 224004, "pmas": 1158355, "age_threshold": 65, "residency_years": 20},
        "evaluator": "pgu_eligibility",
    },
    "tope_imponible": {
        "description": "Tope imponible 83.4 UF mensual",
        "effectiveFrom": date(2024, 1, 1),
        "effectiveTo": None,
        "citation": "https://www.spensiones.cl",
        "params": {"tope_uf": 83.4},
    },
    "apv_a": {
        "description": "APV Regimen A 15% x 6 UTM annual",
        "effectiveFrom": date(2024, 1, 1),
        "effectiveTo": None,
        "citation": "https://www.spensiones.cl",
        "params": {"rate": 0.15, "utm": 6},
    },
    "apv_b": {
        "description": "APV Regimen B 50 UF/mo 600 UF/yr",
        "effectiveFrom": date(2024, 1, 1),
        "effectiveTo": None,
        "citation": "https://www.spensiones.cl",
        "params": {"monthly": 50, "annual": 600},
    },
}

def get_rule(rule_id: str, as_of: date = None):
    r = RULES.get(rule_id)
    if not r:
        return None
    if as_of and r["effectiveFrom"] and as_of < r["effectiveFrom"]:
        return None
    if as_of and r["effectiveTo"] and as_of > r["effectiveTo"]:
        return None
    return r

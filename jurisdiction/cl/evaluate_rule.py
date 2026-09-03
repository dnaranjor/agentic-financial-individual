"""jurisdiction.cl.evaluate_rule — per-person evaluation (AWP-007a)

Traceability: TARGET-ARCHITECTURE.md:VI.6, F-05, 007a:12.1

Signature: evaluate_rule(ruleId, personId, asOf) -> {applicable, citation, effectiveFrom/to, reason}
Person context is supplied via person dict {birthDate, nationality, rsh_bracket_pct, residency_years}
For demo, we use simplified person fixtures: principal 57y Chilean male 100% RSH, spouse 56y Venezuelan female 70% RSH
"""
from datetime import date
from .rules import get_rule

# Synthetic persons for demo — in real, would query HSS
PERSONS = {
    "principal": {"id": "principal", "birthDate": date(1969, 3, 15), "nationality": "chilena", "rsh_bracket_pct": 100, "residency_years": 40},
    "spouse": {"id": "spouse", "birthDate": date(1970, 6, 20), "nationality": "venezolana", "rsh_bracket_pct": 70, "residency_years": 10},
}

def evaluate_rule(rule_id: str, person_id: str, as_of: date) -> dict:
    rule = get_rule(rule_id, as_of)
    if not rule:
        return {"applicable": False, "citation": None, "effectiveFrom": None, "effectiveTo": None, "reason": "rule not effective"}
    if rule_id == "pgu_eligibility":
        person = PERSONS.get(person_id)
        if not person:
            return {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": "person not found"}
        # per-person logic: age >=65, residency >=20y, RSH not top10% (i.e., rsh_bracket_pct <=90 means eligible if not top10%?)
        # Simplified: top 10% is rsh 91-100, so 100 is top10% → ineligible; 70 is not top10% → eligible if age+residency met
        age = as_of.year - person["birthDate"].year - ((as_of.month, as_of.day) < (person["birthDate"].month, person["birthDate"].day))
        if age < 65:
            return {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": f"age {age} <65"}
        if person["residency_years"] < 20:
            return {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": f"residency {person['residency_years']} <20y"}
        if person["rsh_bracket_pct"] > 90:
            return {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": f"RSH top10% {person['rsh_bracket_pct']} >90"}
        return {"applicable": True, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": "eligible"}
    if rule_id == "tope_imponible":
        return {"applicable": True, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "value": rule["params"]["tope_uf"], "reason": "tope 83.4 UF applies"}
    # default: applicable if effective
    return {"applicable": True, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": "rule effective"}

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
    "principal": {"id": "principal", "birthDate": date(1959, 3, 15), "nationality": "chilena", "rsh_bracket_pct": 100, "residency_years": 40},
    "spouse": {"id": "spouse", "birthDate": date(1961, 6, 20), "nationality": "venezolana", "rsh_bracket_pct": 70, "residency_years": 25},
}

def evaluate_rule(rule_id: str, person_id: str, as_of: date) -> dict:
    rule = get_rule(rule_id, as_of)
    if not rule:
        res = {"applicable": False, "citation": None, "effectiveFrom": None, "effectiveTo": None, "reason": "rule not effective"}
        try:
            from lib.observability.logger import log_event as _log

            _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
        except Exception:
            pass
        return res
    if rule_id == "pgu_eligibility":
        person = PERSONS.get(person_id)
        if not person:
            res = {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": "person not found"}
            try:
                from lib.observability.logger import log_event as _log

                _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
            except Exception:
                pass
            return res
        # per-person logic: age >=65, residency >=20y, RSH not top10% (i.e., rsh_bracket_pct <=90 means eligible if not top10%?)
        # Simplified: top 10% is rsh 91-100, so 100 is top10% → ineligible; 70 is not top10% → eligible if age+residency met
        age = as_of.year - person["birthDate"].year - ((as_of.month, as_of.day) < (person["birthDate"].month, person["birthDate"].day))
        if age < 65:
            res = {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": f"age {age} <65"}
            try:
                from lib.observability.logger import log_event as _log

                _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
            except Exception:
                pass
            return res
        if person["residency_years"] < 20:
            res = {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": f"residency {person['residency_years']} <20y"}
            try:
                from lib.observability.logger import log_event as _log

                _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
            except Exception:
                pass
            return res
        if person["rsh_bracket_pct"] > 90:
            res = {"applicable": False, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": f"RSH top10% {person['rsh_bracket_pct']} >90"}
            try:
                from lib.observability.logger import log_event as _log

                _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
            except Exception:
                pass
            return res
        res = {"applicable": True, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": "eligible"}
        try:
            from lib.observability.logger import log_event as _log

            _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
        except Exception:
            pass
        return res
    if rule_id == "tope_imponible":
        res = {"applicable": True, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "value": rule["params"]["tope_uf"], "reason": "tope 83.4 UF applies"}
        try:
            from lib.observability.logger import log_event as _log

            _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
        except Exception:
            pass
        return res
    # default: applicable if effective
    res = {"applicable": True, "citation": rule["citation"], "effectiveFrom": rule["effectiveFrom"], "effectiveTo": rule["effectiveTo"], "reason": "rule effective"}
    try:
        from lib.observability.logger import log_event as _log

        _log("jurisdiction.evaluate", scope="Jurisdiction", ruleId=rule_id, personId=person_id, applicable=res["applicable"], reason=res["reason"])
    except Exception:
        pass
    return res

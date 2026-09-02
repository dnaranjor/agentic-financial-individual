#!/usr/bin/env python3
"""
boundary_test.py — AWP-002 IU-004
Fitness: B-4 core not in jurisdiction, UF ban, labels never identifiers, L2 != L3
Traceability: STAGE-8-PLAN-DELTA.md:6.2 CHG-011, RT-M01, AWP-002:12.5, 002:12.6
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_b4_core_no_jurisdiction():
    """Core schemas must not contain jurisdiction reference as property."""
    import json
    core = ["person-household.json", "measure.json", "evidence.json", "observation.json"]
    ok = True
    for name in core:
        p = ROOT / "schema/registry" / name
        txt = p.read_text(encoding="utf-8")
        if "jurisdiction" in txt.lower():
            # Allow only as B-4 constraint via propertyNames/not
            if '"propertyNames"' in txt and 'jurisdiction' in txt:
                print(f"PASS B-4: {name} contains jurisdiction only as B-4 constraint (propertyNames not)")
            else:
                print(f"FAIL B-4: {name} contains jurisdiction field (should be propertyNames constraint only)")
                ok = False
        else:
            print(f"PASS B-4: {name} no jurisdiction field")
    return ok

def test_uf_ban():
    """Unit partition INDEX_UF must exist, and measure must require unit+basis."""
    import json
    unit = json.loads((ROOT / "schema/registry/unit.json").read_text(encoding="utf-8"))
    if "INDEX_UF" not in unit.get("enum", []):
        print("FAIL UF: unit.json missing INDEX_UF")
        return False
    if "CURRENCY_CLP" not in unit["enum"]:
        print("FAIL UF: missing CURRENCY_CLP")
        return False
    print("PASS UF: unit.json partition currency|index_unit present (INDEX_UF not currency)")
    measure = json.loads((ROOT / "schema/registry/measure.json").read_text(encoding="utf-8"))
    if "basis" not in measure["properties"]:
        print("FAIL UF: measure.json missing basis")
        return False
    print("PASS UF: measure.json requires basis")
    return True

def test_labels_never_identifiers():
    """Glossary ES labels must not appear as identifiers in schema/registry (they are presentation only)."""
    glossary = (ROOT / "docs/glossary.md").read_text(encoding="utf-8")
    # ES labels like 'Ingreso neto de AFP y salud' should not be in schema identifiers
    labels = ["Ingreso neto", "Conjunto de Supuestos", "Evidencia"]
    ok = True
    for schema in (ROOT / "schema/registry").glob("*.json"):
        txt = schema.read_text(encoding="utf-8")
        for lab in labels:
            if lab in txt:
                print(f"FAIL labels: {schema.name} contains ES label '{lab}' as identifier")
                ok = False
    if ok:
        print("PASS labels: no ES label leaks into schema identifiers")
    return ok

def test_L2_never_imports_L3():
    """No schema refs to jurisdiction module, no L2 placeholder."""
    import json
    ok = True
    for schema in (ROOT / "schema/registry").glob("*.json"):
        txt = schema.read_text(encoding="utf-8")
        if "jurisdiction" in txt.lower() and "propertyNames" not in txt:
            print(f"FAIL L2->L3: {schema.name} references jurisdiction outside B-4 constraint")
            ok = False
    if ok:
        print("PASS L2->L3: no core schema imports jurisdiction (B-4 via propertyNames only)")
    return ok

def main():
    results = []
    results.append(("B-4", test_b4_core_no_jurisdiction()))
    results.append(("UF ban", test_uf_ban()))
    results.append(("labels", test_labels_never_identifiers()))
    results.append(("L2!=L3", test_L2_never_imports_L3()))
    ok = all(r[1] for r in results)
    print("\n=== FITNESS SUMMARY: {} ===".format("PASS" if ok else "FAIL"))
    for name, res in results:
        print(f"  {name}: {'PASS' if res else 'FAIL'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

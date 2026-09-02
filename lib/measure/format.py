"""lib.measure.format — es-CL formatting (AWP-004)

Traceability: spec/measure-contract.md, AWP-009:010 rounding epsilon via lib only
"""
from hss.models import Measure, Unit

def format_measure(m: Measure) -> str:
    """Chilean es-CL formatting:
    - CURRENCY_CLP: thousands '.' no decimals, e.g., 5245000 -> 5.245.000
    - INDEX_UF: comma decimal two places, e.g., 39405 -> 39.405,00 (UF has 2 decimals typical)
    - otherwise: plain
    """
    if m.unit == Unit.CURRENCY_CLP:
        # CLP no decimals, thousands '.'
        n = int(round(m.value))
        s = f"{n:,}".replace(",", ".")
        return s
    elif m.unit == Unit.INDEX_UF:
        # UF with 2 decimals, thousands '.' decimal ','
        # Format with 2 decimals
        s = f"{m.value:,.2f}"  # e.g., 39,405.00 in en -> convert
        # en: 39,405.00 -> es: 39.405,00 -> replace , with X, . with ,, X with .
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    elif m.unit == Unit.RATIO:
        return f"{m.value:.4f}"
    else:
        return str(m.value)

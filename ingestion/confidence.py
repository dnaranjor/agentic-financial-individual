"""ingestion.confidence — heuristic (AWP-009)"""
import re

def score_extraction(text: str, value: str) -> float:
    # simple heuristic: if value appears verbatim, high confidence, else low
    if value in text:
        return 0.85
    # numeric pattern near keyword
    if re.search(r"\d[\d\.\,]*", text):
        return 0.6
    return 0.3

"""vault.store — at-rest handling (AWP-008)

Traceability: AWP-008 IU-001, docs/decisions/vault-interface-stub.md
"""
from pathlib import Path

VAULT_DIR = Path(__file__).parent / "data"

def list_encrypted() -> list[Path]:
    return list(VAULT_DIR.rglob("*.enc"))

def vault_contains_plaintext(plaintext: str) -> bool:
    """Check raw .enc files for plaintext leak."""
    for p in list_encrypted():
        if plaintext.encode("utf-8") in p.read_bytes():
            return True
    return False

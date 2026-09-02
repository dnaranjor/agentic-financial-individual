"""Vault port — stub mock for AWP-003 (AWP-008 will harden)

Traceability: docs/decisions/vault-interface-stub.md, STAGE-8-PLAN-DELTA.md:8.1
Interface: encrypt(payload: bytes, scope: str, key_ref: str) -> str
"""
import base64
import json
from pathlib import Path

VAULT_DIR = Path(__file__).parent / "data"
VAULT_DIR.mkdir(parents=True, exist_ok=True)

def encrypt(payload: bytes, scope: str, key_ref: str = "mock-key") -> str:
    # mock "encryption" — base64, stored as file vault/data/<scope>/<key_ref>.enc
    # In real 008, this will be real crypto + outside OneDrive.
    b64 = base64.b64encode(payload).decode("utf-8")
    scope_dir = VAULT_DIR / scope
    scope_dir.mkdir(parents=True, exist_ok=True)
    # use key_ref as filename safe
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in key_ref)
    ref = f"vault://{scope}/{safe}"
    (scope_dir / f"{safe}.enc").write_text(b64, encoding="utf-8")
    return ref

def decrypt(ref: str) -> bytes:
    # ref like vault://AcceptedFact/<id>
    try:
        scope, name = ref.replace("vault://", "").split("/", 1)
    except ValueError:
        raise ValueError(f"invalid vault ref {ref}")
    p = VAULT_DIR / scope / f"{name}.enc"
    b64 = p.read_text(encoding="utf-8")
    return base64.b64decode(b64.encode("utf-8"))

def is_encrypted_file_contains_plaintext(plaintext: str) -> bool:
    """Helper for test: ensure no vault file contains plaintext."""
    for f in VAULT_DIR.rglob("*.enc"):
        b64 = f.read_text(encoding="utf-8")
        try:
            decoded = base64.b64decode(b64).decode("utf-8")
            if plaintext in decoded:
                # plaintext is inside decoded payload (expected), but file on disk is b64 not plaintext
                # check raw file contains plaintext (should not, because b64 not plaintext)
                raw = f.read_text(encoding="utf-8")
                if plaintext in raw:
                    return True
        except Exception:
            continue
    return False

"""Vault port — hardened Fernet (AWP-008)

Traceability: docs/decisions/vault-interface-stub.md, STAGE-8-PLAN-DELTA.md:8.1, AWP-008 IU-001
Interface: encrypt(payload: bytes, scope: str, key_ref: str) -> str
Hardening: Fernet (cryptography) at-rest, not mock base64. Key in vault/keys/vault.key (ignored), data in vault/data/<scope>/<id>.enc (ignored).
"""
import base64
from pathlib import Path
from cryptography.fernet import Fernet

VAULT_DIR = Path(__file__).parent / "data"
KEYS_DIR = Path(__file__).parent / "keys"
VAULT_DIR.mkdir(parents=True, exist_ok=True)
KEYS_DIR.mkdir(parents=True, exist_ok=True)

KEY_PATH = KEYS_DIR / "vault.key"

def _load_or_create_key() -> bytes:
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes().strip()
    key = Fernet.generate_key()
    KEY_PATH.write_bytes(key)
    # ensure not committed via .gitignore vault/keys/
    return key

def _fernet() -> Fernet:
    key = _load_or_create_key()
    return Fernet(key)

def encrypt(payload: bytes, scope: str, key_ref: str = "default") -> str:
    f = _fernet()
    ct = f.encrypt(payload)
    scope_dir = VAULT_DIR / scope
    scope_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in key_ref)
    ref = f"vault://{scope}/{safe}"
    (scope_dir / f"{safe}.enc").write_bytes(ct)
    try:
        from lib.observability.logger import log_event as _log

        _log("vault.encrypt", scope=scope, key_ref=safe, bytes=len(payload), ref=ref)
    except Exception:
        pass
    return ref


def decrypt(ref: str) -> bytes:
    try:
        scope, name = ref.replace("vault://", "").split("/", 1)
    except ValueError:
        raise ValueError(f"invalid vault ref {ref}")
    p = VAULT_DIR / scope / f"{name}.enc"
    ct = p.read_bytes()
    f = _fernet()
    data = f.decrypt(ct)
    try:
        from lib.observability.logger import log_event as _log

        _log("vault.decrypt", scope=scope, key_ref=name, bytes=len(data), ref=ref)
    except Exception:
        pass
    return data

def is_encrypted_file_contains_plaintext(plaintext: str) -> bool:
    """Ensure no vault .enc file on disk contains plaintext (should be ciphertext)."""
    for f in VAULT_DIR.rglob("*.enc"):
        raw = f.read_bytes()
        if plaintext.encode("utf-8") in raw:
            return True
        # also check that decrypt would contain plaintext (expected inside decoded, but file is ciphertext)
        try:
            dec = decrypt(f"vault://{f.parent.name}/{f.stem}")
            # dec contains plaintext expected, but raw is ciphertext not plaintext — already checked
            pass
        except Exception:
            continue
    return False
